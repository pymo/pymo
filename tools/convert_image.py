from PIL import Image, ImageOps
import glob, os, shutil
import Tkinter, Tkconstants, tkFileDialog,tkMessageBox

def convert_pymo_to_png(src,filetype,dst):
    count=0
    for infile in glob.glob(os.path.join(src,filetype)):
        filename, ext = os.path.splitext(infile)
        if filename[-5:]!='_mask' and filename[-5:]!='_MASK':
            mask_filename=filename+'_mask'+ext
            if os.path.exists(mask_filename):
                baseimg = Image.open(infile).convert("RGBA")
                maskimg = Image.open(mask_filename).convert('L')
                datas = baseimg.getdata()
                alphadata = maskimg.getdata()
                newData = list()
                for i in range(0,len(datas)):
                    newData.append((datas[i][0],datas[i][1],datas[i][2],alphadata[i]))
                baseimg.putdata(newData)
                print os.path.join(dst,infile[len(src)+1:])
                baseimg.save(os.path.join(dst,infile[len(src)+1:]))
            else:
                shutil.copyfile(infile, os.path.join(dst,infile[len(src)+1:]))
            count+=1
    return count
            
class TkFileDialogExample(Tkinter.Frame):

    def __init__(self, root):

        Tkinter.Frame.__init__(self, root)

        # options for buttons
        button_opt = {'fill': Tkconstants.BOTH, 'padx': 5, 'pady': 5}

        self.filename = Tkinter.StringVar()
        self.outputdir = Tkinter.StringVar()
        self.initial_dir=""
        
        Tkinter.Label(self, text="Input file type:").grid(row=1, column=0, sticky='w', padx=5)
        self.filetype = Tkinter.StringVar()
        Tkinter.Entry(self, textvariable=self.filetype, width=5).grid(row=1, column=1,columnspan=1, pady=9, sticky='w', padx=7)
        self.filetype.set('*.png')
        
        Tkinter.Label(self, text="Input dir:").grid(row=2, column=0, sticky='w', padx=5)
        Tkinter.Entry(self, textvariable=self.filename, width=35).grid(row=2, column=1,columnspan=2, pady=9, sticky='w', padx=7)
        self.browse_button = Tkinter.Button(self, text="...",
                                    width=5,
                                    command=self.browse_script).grid(row=2,column=3,
                                    columnspan=1, padx=8, pady=3)
        
        Tkinter.Label(self, text="Output dir:").grid(row=3, column=0, sticky='w', padx=5)
        Tkinter.Entry(self, textvariable=self.outputdir, width=35).grid(row=3, column=1,columnspan=2, pady=9, sticky='w', padx=7)
        self.outputbrowse_button = Tkinter.Button(self, text="...",
                                    width=5,
                                    command=self.browse_output).grid(row=3,column=3,
                                    columnspan=1, padx=8, pady=3)

        self.create_button = Tkinter.Button(self, text="Convert", width=6,
                                    relief="raised",
                                    borderwidth=3, command=self.convert).grid(row=4,column=1)
    def browse_script(self):
        """ Opens the file browser window"""
        file_name = self.filename.get()
        file_or_dir_name = ""
        if file_name != "":
            if os.path.exists(file_name):
                self.initial_dir = file_name
            else:
                tkMessageBox.showerror("Failure",
                                       "File\Directory " + '"' + file_name +\
                                       '"' + " does not exist")
                return

        file_or_dir_name=tkFileDialog.askdirectory(initialdir=self.initial_dir)
        if file_or_dir_name:
            self.filename.set(file_or_dir_name)
    def browse_output(self):
        """ Opens the file browser window"""
        file_name = self.outputdir.get()
        file_or_dir_name = ""
        if file_name != "":
            if os.path.exists(file_name):
                self.initial_dir = file_name
            else:
                tkMessageBox.showerror("Failure",
                                       "File\Directory " + '"' + file_name +\
                                       '"' + " does not exist")
                return

        file_or_dir_name=tkFileDialog.askdirectory(initialdir=self.initial_dir)
        if file_or_dir_name:
            self.outputdir.set(file_or_dir_name)
    def convert(self):
        file_name = self.filename.get()
        outputdir = self.outputdir.get()
        filetype=self.filetype.get()
        count=convert_pymo_to_png(file_name,filetype,outputdir)
        tkMessageBox.showinfo("Done",str(count)+" files are saved.")


if __name__=='__main__':
    root = Tkinter.Tk()
    TkFileDialogExample(root).pack()
    root.title('pymo image converter(symbian to android)')
    root.mainloop()
