import codecs
import struct

def isengnum(char):
    charset=u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
    if char in charset:
        return True
    else:
        return False

def iseng(char):
    charset=u'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_;#@*~!$%^&()-_=+'+'\xE3\x80\x90'.decode('utf8')
    if char in charset:
        return True
    else:
        return False

def allareeng(charlist):
    ret=True
    for char in charlist:
        ret=ret and iseng(char)
    return ret
    
def outputlist(stringlist1,stringlist2=None):
    textfile=file('1.txt','w')
    textfile.write(codecs.BOM_UTF8)
    i=0
    while i < len(stringlist1):
        if stringlist2:
            textfile.write((stringlist1[i]+','+stringlist2[i]+'\n').encode('utf8'))
        else:            
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
def name_list(command):
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
        i+=1
    return names

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

def get_filename(command):
    start=command.rfind(u'\\')
    end=command.rfind(u'.')
    return command[start+1:end]

def parse_script(command):
    global i
    i=1
    name=u''
    #name_list=name_mapping('name_list.txt')
    script=[]
    content=''
    while i < len(command):
        if len(command[i])!=0:
            if not iseng(command[i][0]):
                if command[i-1][0]!='\xE3\x80\x90'.decode('utf8'):
                    script.append('br')
        script.append(command[i])
        i+=1
    return script

def my_cmp(E1, E2):
    if E1.startswith(u'CH'):
        return -1
    elif E2.startswith(u'CH'):
        return 1
    else:
        return cmp(E1, E2)    #compare weight of each 2-tuple
                    #return the negative result of built-in cmp function
                    #thus we get the descend order
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
            chara_list.sort(my_cmp)
            chara_command='#chara '
            k=0
            for j in range(len(chara_list)-1,-1,-1):
                chara_command+=str(k)
                k+=1
                layernum=k
                chara_command+=','
                chara_command+=chara_list[j]
                chara_command+=','
                chara_command+=str((2*j+1)*50/len(chara_list))
                if chara_list[j].endswith(u'M'):
                    layernum+=5
                elif chara_list[j].endswith(u'L'):
                    layernum+=10
                chara_command+=','+str(layernum)+','
            chara_command+='400'
        else:
            if chara_command!='':
                script.append(chara_command)
            chara_command=''
            if command[i].startswith('#chara_cls a') or command[i].startswith('#bg '):
                chara_list=[]
            script.append(command[i])
        i+=1
    return script

def extract_file(filename):
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
        names.append(del_blank(command[:-1]))
    configfile.close()
    return names

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
command=extract_file('yosuga.txt')
script=parse_script(command)
outputlist(script)
#split_file('1.txt','00_a001.txt')


##outputlist(addr,command)
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














