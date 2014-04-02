import codecs
import struct

def isengnum(char):
    charset=u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_#%-\\'
    if char in charset:
        return True
    else:
        return False

def iseng(char):
    charset=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    if char in charset:
        return True
    else:
        return False

def allareeng(charlist):
    ret=True
    for char in charlist:
        ret=ret and iseng(char)
    return ret
    
def outputlist(stringlist1):
    textfile=file('1.txt','w')
    textfile.write(codecs.BOM_UTF8)
    i=0
    while i < len(stringlist1):
        textfile.write((stringlist1[i]+'\n').encode('utf8'))
        i+=1
    textfile.close()

def del_blank(charlist):
    i=0
    startpos=0
    while i<len(charlist) and (charlist[i]==u' ' or charlist[i]==u'\t' or charlist[i]==u'\r' or charlist[i]==u'\0'):
        i+=1
        startpos=i
    i=len(charlist)-1
    endpos=i
    while i>=0 and (charlist[i]==u' ' or charlist[i]==u'\t' or charlist[i]==u'\r' or charlist[i]==u'\0'):
        i-=1
        endpos=i
    i=startpos
    newcharlist=''
    while i<endpos+1:
        if charlist[i]==u'\0':
            newcharlist+=u' '
        else:
            newcharlist+=charlist[i]
        i+=1
    return newcharlist

#list all the names
def name_list():
    names=[]
    i=0
    while i < len(command):
        if command[i]==u'Talk':
            if isengnum(command[i-1][0]):
                name=command[i-2]
            else:
                name=command[i-1]
            if del_blank(name) not in names:
                names.append(del_blank(name))
                print name
        i+=1
    outputlist(names)

def name_mapping(filename):
    configfile=file(filename,'r')
    names={}
    while True:
        line=configfile.readline()
        if len(line)==0:
            break
        if line[:3] == codecs.BOM_UTF8:
            command=line[3:].decode('utf8')
        else:
            command=line.decode('utf8')
        args=command[:-1].split(',')
        names[args[0]]=args[1]
    configfile.close()
    return names

def readyosugafile(filename):
    configfile=file(filename,'r')
    names=[]
    while True:
        line=configfile.readline()
        if len(line)==0:
            break
        if line[:3] == codecs.BOM_UTF8:
            command=line[3:].decode('utf8')
        else:
            command=line.decode('utf8')
        names.append(command[:-1])
    configfile.close()
    return names

def fixyosugafile(command):
    global i
    i=3397
    script=[]
    cachename=u''
    while i < len(command)-1:
        if len(command[i])>1:
            if command[i][0]=='\xE3\x80\x90'.decode('utf8'):
                if not isengnum(command[i][1]):
                    if cachename==u'':
                         cachename=command[i]
                    else:
                         print 'name conflict at line',i
            else:
                if isengnum(command[i][0]) and command[i][0:5]!=u'__SEL':
                    script.append(command[i])
                else:
                    script.append(cachename)
                    script.append(command[i])
                    cachename=u''
        else:
            print 'command not long enough at line',i
            
        i+=1
    return script

def parse_script(command):
    i=12000
    name=u''
    name_list=name_mapping('name_list.txt')
    voice_list=name_mapping('voice.txt')
    script=[]
    bgdict={u'EB06a':(800,858),u'EB06b':(800,858),u'EC06a':(800,969),u'EC06b':(800,969),u'B24a':(800,1200),u'B24a_':(800,1200),u'B27a':(800,1200),u'B27a_':(800,1200),u'B27b':(800,1200),u'B27b_':(800,1200),u'B27c':(800,1200),u'B27d':(800,1200),u'B28d':(800,1200),u'B37a':(800,1201),u'B37a_':(800,1201),u'EA08a':(800,1300),u'EA08b':(800,1300),u'EA08c':(800,1300),u'EA06a':(1069,866),u'EA06b':(1069,866),u'EA06c':(1069,866),u'B36a':(1400,600),u'B36a_':(1400,600),u'B36b':(1400,600),u'B20a':(1708,600),u'B20b':(1708,600),u'B34a':(1766,600),u'B34a_':(1766,600),u'B34b':(1766,600),u'B34c':(1766,600)}
    while i < len(command):
        #Audio
        if command[i]==u'ScPlayBgm':
            script.append('#BGM_STA '+command[i-2])
        elif command[i]==u'ScPauseBgm' or command[i]==u'ScStopBgm':
            script.append('#BGM_STP')
        elif command[i]==u'ScPlayEnvSe':
            if command[i-2].isdigit():
                script.append('#SE_STA '+command[i-3].lower()+',60')
            else:
                script.append('#SE_STA '+command[i-2].lower()+',60')
        elif command[i]==u'ScPlaySe':
            script.append('#SE_STA '+command[i-2].lower())
        elif command[i]==u'ScStopSe' or command[i]==u'ScStopEnvSe':
            script.append('#SE_STP')
        #Image
        elif command[i]==u'SetCg' and (command[i-3]!=u'ImageBoard' and command[i-3]!=u'pub1'):
            if command[i-1]==u'0' and command[i-2]==u'0':
                script.append('#BG_DSP '+command[i-3])                
            else:
                script.append('#BG_PART '+command[i-3]+','+str(int(command[i-2])*100/bgdict[command[i-3]][0])+','+str(int(command[i-1])*100/bgdict[command[i-3]][1]))
        elif command[i]==u'BlackOut':
            script.append('#BG_DSP BLACK')
        elif command[i]==u'WhiteOut':
            script.append('#BG_DSP WHITE')
        elif command[i]==u'Flush':
            script.append('#FLUSH '+command[i-2])
        #chara
        elif command[i]==u'SetBustup':
            script.append('#CHR_DSP '+command[i-3])
        elif command[i]==u'BustupLeave' or command[i]==u'BustupClear':
            script.append('#CHR_ERSW')
        #misc
        elif command[i]==u'OnGameClear':
            script.append('#BG_DSP BLACK')
            script.append('#WAIT 120')
            script.append('#BGM_STP')
            script.append('#RSET S01,1')
            script.append('#BG_DSP logo2')
            script.append('#WAIT 60')
            script.append('#change OINI')
            script.append('#FILE 00_001')
        elif command[i]==u'ScPlayMovie':
            script.append('#MOV_PLY '+command[i-1])
        elif command[i]==u'Quake' or command[i]==u'Shake':
            script.append('#VIB_COLLISION_L')
        elif command[i]==u'ScWait':
            script.append('#WAIT '+str(int(command[i-2])*60/1000))
        elif command[i]==u'Change':
            if command[i-1]!=u'EXIT_SCENARIO':
                script.append('#change '+command[i-1])
                if command[i-1]==u'00_g000':
                    script.append('#FILE 00_e009b')
                elif command[i-1]==u'00_g001':
                    script.append('#FILE 00_e013a')
                elif command[i-1]==u'00_g003':
                    script.append('#FILE 00_e018')
                elif command[i-1]==u'00_e009b':
                    script.append('#FILE 00_g001')
                elif command[i-1]==u'00_e013a':
                    script.append('#FILE 00_g003')
                elif command[i-1]==u'00_e018':
                    script.append('#FILE 00_z000')
                else:
                    script.append('#FILE '+command[i-1])
        elif command[i]==u'EyeCatchEnter':
            script.append('#CHR_DSPM DATE,50,0,60')
            script.append('#WAIT 240')
            script.append('#BG_DSP BLACK')
            script.append('#WAIT 60')
        #Talk
        if command[i]==u'Talk':
            if isengnum(command[i-1][0]):
                name=name_list[del_blank(command[i-2])]
                script.append('#VO_STA '+command[i-1])#voice_list[command[i-1]])
            else:
                name=name_list[del_blank(command[i-1])]
            if name!=u'':
                script.append(name+'\xE3\x80\x8C'.decode('utf8')+command[i+1]+'\xE3\x80\x8D'.decode('utf8'))
            else:
                script.append(command[i+1])
        else:
            name==u''
        i+=1
    return script

def chara_in_list(chara_list,chara):
    for i in range(0,len(chara_list)):
        if chara[0:2]==chara_list[i][0:2]:
            return i
    return -1

def modify_script(command):
    global chara_list
    script=[]
    chara_list=[]
    i=0
    chara_command=''
    while i < len(command):
        if command[i].startswith('#CHR_DSP '):
            chara=command[i][9:]
            j=chara_in_list(chara_list,chara)
            if j==-1:
                chara_list.append(chara)
            else:
                chara_list[j]=chara
            chara_list=sorted(chara_list)
            chara_command='#CHR_DSPM '
            for j in range(len(chara_list)-1,-1,-1):
                chara_command+=chara_list[j]
                chara_command+=','
                chara_command+=str((2*j+1)*50/len(chara_list))
                if chara_list[j].endswith(u'S'):
                    chara_command+=',0,'
                elif chara_list[j].endswith(u'M'):
                    chara_command+=',1,'
                else:
                    chara_command+=',2,'
            chara_command+='18'
        else:
            if chara_command!='':
                script.append(chara_command)
            chara_command=''
            if command[i].startswith('#CHR_ERSW') or command[i].startswith('#BG_DSP '):
                chara_list=[]
            script.append(command[i])
        i+=1
    return script

def extract_file(filename):
    f=file(filename,'rb')
    buf=f.read()
    f.close()
    i=0
    print len(buf),'bytes read!'
    command=[]
    addr=[]
    while i < len(buf):
        if buf[i:i+2]=='\x08\x05':
            i+=6
            stringlen=struct.unpack('i',buf[i:i+4])[0]
            i+=4
            command.append(buf[i:2*stringlen+i].decode('utf-16'))
            addr.append(i)
            i+=2*stringlen
        elif buf[i:i+3]=='\x02\x00\x06' and buf[i+3:i+5]!='\x00\x00':
            i+=3
            stringlen=struct.unpack('i',buf[i:i+4])[0]
            i+=4
            try:
                command.append(buf[i:2*stringlen+i].decode('utf-16'))
                addr.append(i)
            except:
                print i,stringlen
                pass
            i+=2*stringlen
        elif buf[i:i+3]=='\x02\x00\x04':
            i+=3
            command.append(str(struct.unpack('i',buf[i:i+4])[0]))
            addr.append(i)
            i+=4
        else:
            i+=1
    del buf
    return command

def split_file(filename,dstfilename):
    configfile=file(filename,'r')
    dstfile=file(dstfilename,'w')
    dstfile.write(codecs.BOM_UTF8)
    dstfile.write('\x3B\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE7\xBC\x96\xE5\x86\x99\xE8\x80\x85\xE4\xB8\xBA\x63\x68\x65\x6E\x5F\x78\x69\x6E\x5F\x6D\x69\x6E\x67\x2C\x20\xE6\xB1\x89\xE5\x8C\x96\xE6\x96\x87\xE6\x9C\xAC\xE7\x89\x88\xE6\x9D\x83\xE4\xB8\xBA\x5B\x53\x70\x68\x65\x72\x65\x20\xE4\xB8\xAD\xE6\x96\x87\xE5\x8C\x96\xE5\xA7\x94\xE5\x91\x98\xE4\xBC\x9A\x5D\xE6\x89\x80\xE6\x9C\x89\xEF\xBC\x8C\xE8\xAF\xB7\xE5\x8B\xBF\xE6\x93\x85\xE8\x87\xAA\xE4\xBF\xAE\xE6\x94\xB9\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE6\x88\x96\xE7\x9B\xB4\xE6\x8E\xA5\xE5\x8F\x91\xE5\xB8\x83\xE4\xBD\xBF\xE7\x94\xA8\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE5\x88\xB6\xE4\xBD\x9C\xE7\x9A\x84\xE4\xBA\xA7\xE5\x93\x81\x0D\x0A\x3B\xE5\xA6\x82\xE9\x9C\x80\xE8\xA6\x81\xE4\xBD\xBF\xE7\x94\xA8\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE5\x88\xB6\xE4\xBD\x9C\xE7\xA7\xBB\xE6\xA4\x8D\xE4\xBD\x9C\xE5\x93\x81\xEF\xBC\x8C\xE8\xAF\xB7\xE8\x81\x94\xE7\xB3\xBB\x63\x68\x65\x6E\x5F\x78\x69\x6E\x5F\x6D\x69\x6E\x67\x40\x31\x36\x33\x2E\x63\x6F\x6D\x0D\x0A')
    while True:
        line=configfile.readline()
        if len(line)==0:
            break
        if line[:3] == codecs.BOM_UTF8:
            command=line[3:].decode('utf8')
        else:
            command=line.decode('utf8')
        if command.startswith(u'#FILE '):
            dstfile.close()
            dstfile=file(command[6:-1]+'.txt','w')
            dstfile.write(codecs.BOM_UTF8)
            dstfile.write('\x3B\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE7\xBC\x96\xE5\x86\x99\xE8\x80\x85\xE4\xB8\xBA\x63\x68\x65\x6E\x5F\x78\x69\x6E\x5F\x6D\x69\x6E\x67\x2C\x20\xE6\xB1\x89\xE5\x8C\x96\xE6\x96\x87\xE6\x9C\xAC\xE7\x89\x88\xE6\x9D\x83\xE4\xB8\xBA\x5B\x53\x70\x68\x65\x72\x65\x20\xE4\xB8\xAD\xE6\x96\x87\xE5\x8C\x96\xE5\xA7\x94\xE5\x91\x98\xE4\xBC\x9A\x5D\xE6\x89\x80\xE6\x9C\x89\xEF\xBC\x8C\xE8\xAF\xB7\xE5\x8B\xBF\xE6\x93\x85\xE8\x87\xAA\xE4\xBF\xAE\xE6\x94\xB9\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE6\x88\x96\xE7\x9B\xB4\xE6\x8E\xA5\xE5\x8F\x91\xE5\xB8\x83\xE4\xBD\xBF\xE7\x94\xA8\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE5\x88\xB6\xE4\xBD\x9C\xE7\x9A\x84\xE4\xBA\xA7\xE5\x93\x81\x0D\x0A\x3B\xE5\xA6\x82\xE9\x9C\x80\xE8\xA6\x81\xE4\xBD\xBF\xE7\x94\xA8\xE6\xAD\xA4\xE8\x84\x9A\xE6\x9C\xAC\xE5\x88\xB6\xE4\xBD\x9C\xE7\xA7\xBB\xE6\xA4\x8D\xE4\xBD\x9C\xE5\x93\x81\xEF\xBC\x8C\xE8\xAF\xB7\xE8\x81\x94\xE7\xB3\xBB\x63\x68\x65\x6E\x5F\x78\x69\x6E\x5F\x6D\x69\x6E\x67\x40\x31\x36\x33\x2E\x63\x6F\x6D\x0D\x0A')
        else:
            dstfile.write(command.encode('utf8'))
    configfile.close()
    dstfile.close()
    
#main
command=extract_file('yosuga.csx')
script=parse_script(command)
outputlist(modify_script(script))
#split_file('1.txt','00_a001.txt')

#command=readyosugafile('yosuga.txt')
#script=fixyosugafile(command)
#outputlist(script)
###sort the command by frequency
##frequency={}
##i=0
##while i < len(command):
##    if allareeng(command[i]):
##        if frequency.has_key(command[i]):
##            frequency[command[i]]+=1
##        else:
##            frequency[command[i]]=1
##    i+=1
##sorted_frequency=sorted(frequency.items(),key=lambda d:d[1],reverse=True)
##outputlist(sorted_frequency)














