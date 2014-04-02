#!/usr/bin/env python

# Copyright (c) 2011 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

"""Android system-wide tracing utility.

This is a tool for capturing a trace that includes data from both userland and
the kernel.  It creates an HTML file for visualizing the trace.
"""

import errno, optparse, os, select, subprocess, sys, time, zlib, config

# This list is based on the tags in frameworks/native/include/utils/Trace.h.
trace_tag_bits = {
  'gfx':      1<<1,
  'input':    1<<2,
  'view':     1<<3,
  'webview':  1<<4,
  'wm':       1<<5,
  'am':       1<<6,
  'sync':     1<<7,
  'audio':    1<<8,
  'video':    1<<9,
  'camera':   1<<10,
}

def main():
  parser = optparse.OptionParser()
  parser.add_option('-o', dest='output_file', help='write HTML to FILE',
                    default='trace.html', metavar='FILE')
  parser.add_option('-t', '--time', dest='trace_time', type='int',
                    help='trace for N seconds', metavar='N')
  parser.add_option('-b', '--buf-size', dest='trace_buf_size', type='int',
                    help='use a trace buffer size of N KB', metavar='N')
  parser.add_option('-d', '--disk', dest='trace_disk', default=False,
                    action='store_true', help='trace disk I/O (requires root)')
  parser.add_option('-f', '--cpu-freq', dest='trace_cpu_freq', default=False,
                    action='store_true', help='trace CPU frequency changes')
  parser.add_option('-i', '--cpu-idle', dest='trace_cpu_idle', default=False,
                    action='store_true', help='trace CPU idle events')
  parser.add_option('-l', '--cpu-load', dest='trace_cpu_load', default=False,
                    action='store_true', help='trace CPU load')
  parser.add_option('-s', '--no-cpu-sched', dest='trace_cpu_sched', default=True,
                    action='store_false', help='inhibit tracing CPU ' +
                    'scheduler (allows longer trace times by reducing data ' +
                    'rate into buffer)')
  parser.add_option('-w', '--workqueue', dest='trace_workqueue', default=False,
                    action='store_true', help='trace the kernel workqueues ' +
                    '(requires root)')
  parser.add_option('--set-tags', dest='set_tags', action='store',
                    help='set the enabled trace tags and exit; set to a ' +
                    'comma separated list of: ' +
                    ', '.join(trace_tag_bits.iterkeys()))
  parser.add_option('--link-assets', dest='link_assets', default=False,
                    action='store_true', help='link to original CSS or JS resources '
                    'instead of embedding them')
  options, args = parser.parse_args()

  if options.set_tags:
    flags = 0
    tags = options.set_tags.split(',')
    for tag in tags:
      try:
        flags |= trace_tag_bits[tag]
      except KeyError:
        parser.error('unrecognized tag: %s\nknown tags are: %s' %
                     (tag, ', '.join(trace_tag_bits.iterkeys())))
    atrace_args = ['adb', 'shell', 'setprop', 'debug.atrace.tags.enableflags', hex(flags)]
    try:
      subprocess.check_call(atrace_args)
    except subprocess.CalledProcessError, e:
      print >> sys.stderr, 'unable to set tags: %s' % e
    print '\nSet enabled tags to: %s\n' % ', '.join(tags)
    print ('You will likely need to restart the Android framework for this to ' +
          'take effect:\n\n    adb shell stop\n    adb shell ' +
          'start\n')
    return

  atrace_args = ['adb', 'shell', 'atrace', '-z']
  if options.trace_disk:
    atrace_args.append('-d')
  if options.trace_cpu_freq:
    atrace_args.append('-f')
  if options.trace_cpu_idle:
    atrace_args.append('-i')
  if options.trace_cpu_load:
    atrace_args.append('-l')
  if options.trace_cpu_sched:
    atrace_args.append('-s')
  if options.trace_workqueue:
    atrace_args.append('-w')
  if options.trace_time is not None:
    if options.trace_time > 0:
      atrace_args.extend(['-t', str(options.trace_time)])
    else:
      parser.error('the trace time must be a positive number')
  if options.trace_buf_size is not None:
    if options.trace_buf_size > 0:
      atrace_args.extend(['-b', str(options.trace_buf_size)])
    else:
      parser.error('the trace buffer size must be a positive number')

  script_dir = os.path.dirname(os.path.abspath(sys.argv[0]))

  if options.link_assets:
    css = '\n'.join(linked_css_tag % (os.path.join(script_dir, f)) for f in config.css_in_files)
    js = '\n'.join(linked_js_tag % (os.path.join(script_dir, f)) for f in config.js_in_files)
  else:
    css_filename = os.path.join(script_dir, config.css_out_file)
    js_filename = os.path.join(script_dir, config.js_out_file)
    css = compiled_css_tag % (open(css_filename).read())
    js = compiled_js_tag % (open(js_filename).read())

  html_filename = options.output_file

  trace_started = False
  leftovers = ''
  adb = subprocess.Popen(atrace_args, stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
  dec = zlib.decompressobj()
  while True:
    ready = select.select([adb.stdout, adb.stderr], [], [adb.stdout, adb.stderr])
    if adb.stderr in ready[0]:
      err = os.read(adb.stderr.fileno(), 4096)
      sys.stderr.write(err)
      sys.stderr.flush()
    if adb.stdout in ready[0]:
      out = leftovers + os.read(adb.stdout.fileno(), 4096)
      out = out.replace('\r\n', '\n')
      if out.endswith('\r'):
        out = out[:-1]
        leftovers = '\r'
      else:
        leftovers = ''
      if not trace_started:
        lines = out.splitlines(True)
        out = ''
        for i, line in enumerate(lines):
          if line == 'TRACE:\n':
            sys.stdout.write("downloading trace...")
            sys.stdout.flush()
            out = ''.join(lines[i+1:])
            html_file = open(html_filename, 'w')
            html_file.write(html_prefix % (css, js))
            trace_started = True
            break
          elif 'TRACE:'.startswith(line) and i == len(lines) - 1:
            leftovers = line + leftovers
          else:
            sys.stdout.write(line)
            sys.stdout.flush()
      if len(out) > 0:
        out = dec.decompress(out)
      html_out = out.replace('\n', '\\n\\\n')
      if len(html_out) > 0:
        html_file.write(html_out)
    result = adb.poll()
    if result is not None:
      break
  if result != 0:
    print >> sys.stderr, 'adb returned error code %d' % result
  elif trace_started:
    html_out = dec.flush().replace('\n', '\\n\\\n').replace('\r', '')
    if len(html_out) > 0:
      html_file.write(html_out)
    html_file.write(html_suffix)
    html_file.close()
    print " done\n\n    wrote file://%s/%s\n" % (os.getcwd(), options.output_file)
  else:
    print >> sys.stderr, ('An error occured while capturing the trace.  Output ' +
      'file was not written.')

html_prefix = """<!DOCTYPE HTML>
<html>
<head i18n-values="dir:textdirection;">
<title>Android System Trace</title>
%s
%s
<style>
  .view {
    overflow: hidden;
    position: absolute;
    top: 0;
    bottom: 0;
    left: 0;
    right: 0;
  }
</style>
</head>
<body>
  <div class="view">
  </div>
  <script>
  var linuxPerfData = "\\
"""

html_suffix = """           dummy-0000  [000] 0.0: 0: trace_event_clock_sync: parent_ts=0.0\\n";
  </script>
</body>
</html>
"""

compiled_css_tag = """<style type="text/css">%s</style>"""
compiled_js_tag = """<script language="javascript">%s</script>"""

linked_css_tag = """<link rel="stylesheet" href="%s"></link>"""
linked_js_tag = """<script language="javascript" src="%s"></script>"""

if __name__ == '__main__':
  main()
