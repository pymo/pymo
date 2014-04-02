import codecs
import struct

def isengnum(char):
    charset=u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_'
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


def parse_script(command):
    global i
    i=12150
    name=u''
    name_list=name_mapping('name_list.txt')
    voice_list=name_mapping('voice.txt')
    script=[]
    bgdict={u"EZ13thm":(120,90),u"attention":(800,600),u"B01a":(800,600),u"B01b":(800,600),u"B01c":(800,600),u"B02a":(800,600),u"B02c":(800,600),u"B03a":(800,600),u"B03c":(800,600),u"B04a":(800,600),u"B04c":(800,600),u"B07a":(800,600),u"B07e":(800,600),u"B12a":(800,600),u"B12b":(800,600),u"B12c":(800,600),u"B13a":(800,600),u"B13b":(800,600),u"B14a":(800,600),u"B14b":(800,600),u"B15a":(800,600),u"B15b":(800,600),u"B16a":(800,600),u"B16c":(800,600),u"B17a":(800,600),u"B17b":(800,600),u"B18a":(800,600),u"B18b":(800,600),u"B19a":(800,600),u"B19b":(800,600),u"B20a":(1708,600),u"B21a":(800,600),u"B22a":(800,600),u"B23a":(800,600),u"B23b":(800,600),u"B25a":(800,600),u"B26a":(800,600),u"B27a":(800,1200),u"B27b":(800,1200),u"B27c":(800,1200),u"B27d":(800,1200),u"B28d":(800,1200),u"B32a":(800,600),u"B32b":(800,600),u"B32c":(800,600),u"B33a":(800,600),u"B33c":(800,600),u"B34a":(1766,600),u"B34b":(1766,600),u"B34c":(1766,600),u"B35a":(800,600),u"B35b":(800,600),u"B35c":(800,600),u"B37a":(800,1201),u"B39a":(800,600),u"B39b":(800,600),u"B40a":(800,600),u"B41c":(800,600),u"B42a":(800,600),u"B43a":(800,600),u"B44a":(800,600),u"B45a":(800,600),u"B46a":(800,600),u"B47a":(800,600),u"B48a":(800,600),u"B48c":(800,600),u"banner_web01":(259,77),u"banner_web02":(259,77),u"banner_web03":(259,77),u"banner_web04":(259,77),u"banner_web05":(259,77),u"banner_web06":(259,77),u"black":(800,600),u"blindBlack":(800,300),u"CLOUD_A":(800,600),u"countdown00":(259,77),u"countdown01":(259,77),u"countdown02":(259,77),u"countdown03":(259,77),u"countdown04":(259,77),u"countdown05":(259,77),u"countdown06":(259,77),u"countdown07":(259,77),u"countdown08":(259,77),u"countdown09":(259,77),u"countdown10":(259,77),u"countdown11":(259,77),u"countdown12":(259,77),u"countdown13":(259,77),u"countdown14":(259,77),u"countdownZZ":(259,77),u"EA05":(800,600),u"EA07":(800,600),u"EA08a":(800,1300),u"EA08b":(800,1300),u"EA08c":(800,1300),u"EA18a":(800,600),u"EA18b":(800,600),u"EA19a":(800,600),u"EA19aL":(1600,1200),u"EA19b":(800,600),u"EA19bL":(1600,1200),u"EA19c":(800,600),u"EA19cL":(1600,1200),u"EA20a":(800,600),u"EA20aL":(1600,1200),u"EA20b":(800,600),u"EA20bL":(1600,1200),u"EA21a":(800,600),u"EA21aL":(1600,1200),u"EA21b":(800,600),u"EA21bL":(1600,1200),u"EA21c":(800,600),u"EA21cL":(1600,1200),u"EA22a":(800,600),u"EA22aL":(1600,1200),u"EA22b":(800,600),u"EA22bL":(1600,1200),u"EA22c":(800,600),u"EA22cL":(1600,1200),u"EA22d":(800,600),u"EA22dL":(1600,1200),u"EA23a":(800,600),u"EA23aL":(1600,1200),u"EA23b":(800,600),u"EA23bL":(1600,1200),u"EA24a":(800,600),u"EA24aL":(1600,1200),u"EA24b":(800,600),u"EA24bL":(1600,1200),u"EA24c":(800,600),u"EA24cL":(1600,1200),u"EA24thm":(120,90),u"EA25a":(800,600),u"EA25aL":(1600,1200),u"EA25b":(800,600),u"EA25bL":(1600,1200),u"EA25c":(800,600),u"EA25cL":(1600,1200),u"EA25d":(800,600),u"EA25dL":(1600,1200),u"EA25thm":(120,90),u"EA26a":(800,600),u"EA26aL":(1600,1200),u"EA26b":(800,600),u"EA26bL":(1600,1200),u"EA26c":(800,600),u"EA26cL":(1600,1200),u"EA26d":(800,600),u"EA26dL":(1600,1200),u"EA26e":(800,600),u"EA26eL":(1600,1200),u"EA26f":(800,600),u"EA26fL":(1600,1200),u"EA26g":(800,600),u"EA26gL":(1600,1200),u"EA26h":(800,600),u"EA26hL":(1600,1200),u"EA26thm":(120,90),u"EA27a":(800,600),u"EA27aL":(1600,1200),u"EA27b":(800,600),u"EA27bL":(1600,1200),u"EA27c":(800,600),u"EA27cL":(1600,1200),u"EA27d":(800,600),u"EA27dL":(1600,1200),u"EA27e":(800,600),u"EA27eL":(1600,1200),u"EA27f":(800,600),u"EA27fL":(1600,1200),u"EA27g":(800,600),u"EA27gL":(1600,1200),u"EA27h":(800,600),u"EA27hL":(1600,1200),u"EA27thm":(120,90),u"EA28a":(800,600),u"EA28aL":(1600,1200),u"EA28b":(800,600),u"EA28bL":(1600,1200),u"EA28c":(800,600),u"EA28cL":(1600,1200),u"EA28d":(800,600),u"EA28dL":(1600,1200),u"EA28thm":(120,90),u"EA29a":(800,600),u"EA29aL":(1600,1200),u"EA29b":(800,600),u"EA29bL":(1600,1200),u"EA29c":(800,600),u"EA29cL":(1600,1200),u"EA29thm":(120,90),u"EC02a":(800,600),u"EC02b":(800,600),u"EC02c":(800,600),u"ED02a":(800,600),u"EE02a":(800,600),u"EE02b":(800,600),u"EE02c":(800,600),u"EE02d":(800,600),u"EyeCatchB":(800,100),u"EyeCatchT":(800,100),u"EZ04a":(800,600),u"EZ04b":(800,600),u"EZ07a":(800,600),u"EZ07aL":(1600,1200),u"EZ07b":(800,600),u"EZ07bL":(1600,1200),u"EZ08a":(800,600),u"EZ08aL":(1600,1200),u"EZ08b":(800,600),u"EZ08bL":(1600,1200),u"EZ08c":(800,600),u"EZ08cL":(1600,1200),u"EZ09a":(800,600),u"EZ09aL":(1600,1200),u"EZ09b":(800,600),u"EZ09bL":(1600,1200),u"EZ09c":(800,600),u"EZ09cL":(1600,1200),u"EZ09d":(800,600),u"EZ09dL":(1600,1200),u"EZ10":(800,600),u"EZ10L":(1600,1200),u"EZ11":(800,600),u"EZ11L":(1600,1200),u"EZ12a":(800,600),u"EZ12aL":(1600,1200),u"EZ12b":(800,600),u"EZ12bL":(1600,1200),u"EZ12c":(800,600),u"EZ12cL":(1600,1200),u"EZ12d":(800,600),u"EZ12dL":(1600,1200),u"EZ12e":(800,600),u"EZ12eL":(1600,1200),u"EZ12f":(800,600),u"EZ12fL":(1600,1200),u"EZ12thm":(120,90),u"EZ13a":(800,600),u"EZ13aL":(1600,1200),u"EZ13b":(800,600),u"EZ13bL":(1600,1200),u"EZ13c":(800,600),u"EZ13cL":(1600,1200),u"EZ13d":(800,600),u"EZ13dL":(1600,1200),u"EZ14a":(800,600),u"EZ14aL":(1600,1200),u"EZ14b":(800,600),u"EZ14bL":(1600,1200),u"EZ14c":(800,600),u"EZ14cL":(1600,1200),u"EZ14thm":(120,90),u"EZ15a":(800,600),u"EZ15aL":(1600,1200),u"EZ15b":(800,600),u"EZ15bL":(1600,1200),u"EZ15c":(800,600),u"EZ15cL":(1600,1200),u"EZ15d":(800,600),u"EZ15dL":(1600,1200),u"EZ15thm":(120,90),u"EZ16a":(800,600),u"EZ16aL":(1600,1200),u"EZ16b":(800,600),u"EZ16bL":(1600,1200),u"EZ16c":(800,600),u"EZ16cL":(1600,1200),u"EZ16d":(800,600),u"EZ16dL":(1600,1200),u"EZ16e":(800,600),u"EZ16eL":(1600,1200),u"EZ16thm":(120,90),u"EZ17a":(800,600),u"EZ17aL":(1600,1200),u"EZ17b":(800,600),u"EZ17bL":(1600,1200),u"EZ17c":(800,600),u"EZ17cL":(1600,1200),u"EZ17d":(800,600),u"EZ17dL":(1600,1200),u"EZ17e":(800,600),u"EZ17eL":(1600,1200),u"EZ17thm":(120,90),u"EZ20":(800,600),u"EZ20L":(1600,1200),u"EZ21a":(800,600),u"EZ21aL":(1600,1200),u"EZ21b":(800,600),u"EZ21bL":(1600,1200),u"EZ21c":(800,600),u"EZ21cL":(1600,1200),u"EZ21d":(800,600),u"EZ21dL":(1600,1200),u"EZ21e":(800,600),u"EZ21eL":(1600,1200),u"EZ22a":(800,600),u"EZ22aL":(1600,1200),u"EZ22b":(800,600),u"EZ22bL":(1600,1200),u"EZ22c":(800,600),u"EZ22cL":(1600,1200),u"EZ23a":(800,600),u"EZ23aL":(1600,1200),u"EZ23b":(800,600),u"EZ23bL":(1600,1200),u"EZ24a":(800,600),u"EZ24aL":(1600,1200),u"EZ24b":(800,600),u"EZ24bL":(1600,1200),u"EZ25a":(800,600),u"EZ25aL":(1600,1200),u"EZ25b":(800,600),u"EZ25bL":(1600,1200),u"EZ25c":(800,600),u"EZ25cL":(1600,1200),u"EZ25d":(800,600),u"EZ25dL":(1600,1200),u"EZ25e":(800,600),u"EZ25eL":(1600,1200),u"EZ25f":(800,600),u"EZ25fL":(1600,1200),u"EZ25g":(800,600),u"EZ25gL":(1600,1200),u"EZ25h":(800,600),u"EZ25hL":(1600,1200),u"EZ25i":(800,600),u"EZ25iL":(1600,1200),u"EZ25j":(800,600),u"EZ25jL":(1600,1200),u"EZ25k":(800,600),u"EZ25kL":(1600,1200),u"EZ25l":(800,600),u"EZ25lL":(1600,1200),u"EZ25thm":(120,90),u"EZ26a":(800,600),u"EZ26aL":(1600,1200),u"EZ26b":(800,600),u"EZ26bL":(1600,1200),u"EZ26c":(800,600),u"EZ26cL":(1600,1200),u"EZ26d":(800,600),u"EZ26dL":(1600,1200),u"EZ26thm":(120,90),u"EZ27a":(800,600),u"EZ27aL":(1600,1200),u"EZ27b":(800,600),u"EZ27bL":(1600,1200),u"EZ27c":(800,600),u"EZ27cL":(1600,1200),u"EZ27thm":(120,90),u"EZ28a":(800,600),u"EZ28aL":(1600,1200),u"EZ28b":(800,600),u"EZ28bL":(1600,1200),u"EZ28c":(800,600),u"EZ28cL":(1600,1200),u"EZ28d":(800,600),u"EZ28dL":(1600,1200),u"EZ28thm":(120,90),u"fancy01":(800,600),u"FRM_0510_":(120,90),u"FRM_0602":(240,105),u"FRM_0901":(306,230),u"FRM_0902":(306,230),u"FRM_0903":(306,230),u"FRM_0904":(306,230),u"FRM_0905":(306,230),u"FRM_0906":(306,230),u"FRM_0907":(306,230),u"FRM_0908":(306,230),u"FRM_0909":(306,230),u"FRM_0910":(306,230),u"FRM_0911":(306,230),u"FRM_0912":(306,230),u"FRM_0913":(306,230),u"FRM_0914":(306,230),u"FRM_0915":(306,230),u"FRM_0916":(306,230),u"FRM_0917":(306,230),u"FRM_0918":(306,230),u"FRM_0919":(306,230),u"FRM_0920":(306,230),u"FRM_0921":(306,230),u"FRM_0922":(306,230),u"FRM_0923":(306,230),u"FRM_0924":(306,230),u"FRM_0925":(306,230),u"FRM_0926":(306,230),u"masterup":(259,77),u"MOZCIR":(800,600),u"MOZCIR_":(800,600),u"SS_KARAOKE":(800,600),u"SS_KOZUE":(800,600),u"SS_SORA":(800,600),u"SS_YAHIRO":(800,600),u"title":(354,75),u"WALL01":(800,600),u"WALL02":(800,600),u"WALL03":(800,600),u"WALL04":(800,600),u"WALL05":(800,600),u"WALL06":(800,600),u"WALL07":(800,600),u"WALL08":(800,600),u"WALL09":(800,600),u"WALL10":(800,600),u"WALL11":(800,600),u"WALL12":(800,600),u"WALL13":(800,600),u"WALL14":(800,600),u"WALL15":(800,600),u"WALL16":(800,600),u"WALL17":(800,600),u"WALL18":(800,600),u"WALL19":(800,600),u"WALL20":(800,600),u"white":(800,600),u"WIP_BLTR":(800,600),u"WIP_BRTL":(800,600),u"WIP_BT":(800,600),u"WIP_LR":(800,600),u"WIP_MOZBT":(800,600),u"WIP_MOZH":(800,600),u"WIP_MOZLR":(800,600),u"WIP_MOZRL":(800,600),u"WIP_MOZTB":(800,600),u"WIP_MOZV":(800,600),u"WIP_RL":(800,600),u"WIP_TB":(800,600),u"WIP_TLBR":(800,600),u"WIP_TRBL":(800,600)}
    while i < len(command):
        #Audio
        if command[i]==u'ScPlayBgm':
            script.append('#bgm '+command[i-3])
        elif command[i]==u'ScPauseBgm' or command[i]==u'ScStopBgm':
            script.append('#bgm_stop')
        elif command[i]==u'ScPlayEnvSe':
            if command[i-2].isdigit():
                script.append('#se '+command[i-3].lower()+',0')
            else:
                script.append('#se '+command[i-2].lower()+',0')
        elif command[i]==u'ScPlaySe':
            script.append('#se '+command[i-2].lower())
        elif command[i]==u'ScStopSe' or command[i]==u'ScStopEnvSe':
            script.append('#se_stop')
        #Image
        elif command[i]==u'SetCg' and (command[i-3]!=u'ImageBoard' and command[i-3]!=u'pub1'):
            if command[i-1]==u'0' and command[i-2]==u'0':
                script.append('#bg '+command[i-3]+',BG_ALPHA,500')                
            else:
                script.append('#bg '+command[i-3]+',BG_ALPHA,500,'+str(int(command[i-2])*100/bgdict[command[i-3]][0])+','+str(int(command[i-1])*100/bgdict[command[i-3]][1]))
        elif command[i]==u'BlackOut':
            script.append('#bg black,BG_ALPHA,500')
        elif command[i]==u'WhiteOut':
            script.append('#bg white,BG_ALPHA,500')
        elif command[i]==u'Flush':
            if command[i-2]==u'RED':
                command[i-2]=u'#FF0000'
            else:
                command[i-2]=u'#FFFFFF'
            script.append('#flash '+command[i-2]+','+command[i-1])
        #chara
        elif command[i]==u'SetBustup':
            script.append('#CHR_DSP '+command[i-3])
        elif command[i]==u'BustupLeave' or command[i]==u'BustupClear':
            script.append('#chara_cls a')
        #misc
        elif command[i]==u'ScPlayMovie':
            script.append('#mov_play '+command[i-1])
        elif command[i]==u'Quake' or command[i]==u'Shake':
            script.append('#quake')
        elif command[i]==u'ScWait':
            script.append('#wait '+command[i-2])
        elif command[i]==u'Change':
            if command[i-1]!=u'EXIT_SCENARIO':
                script.append('#change '+command[i-1])
                script.append('#FILE '+command[i-1])
        elif command[i]==u'StaffRoll':
            script.append('#bg black,BG_ALPHA,500')
            script.append('#wait 2000')
            script.append('#bgm_stop')
            script.append('#bg logo2,BG_ALPHA,500')
            script.append('#change OINI')
            script.append('#FILE 00_001')
        elif command[i]==u'EyeCatchEnter':
            script.append('#chara_cls a,1000')
            script.append('#wait 1000')
            script.append('#chara 0,DATE,50,0,1000')
            script.append('#wait 4000')
            script.append('#bg black,BG_ALPHA,1000')
            script.append('#wait 1000')
        elif command[i]==u'WindowView':
            if command[i-1]==u'0':
                script.append('#textbox message,name')
            else:
                script.append('#textbox message2,name2')
        #Talk
        if command[i]==u'Talk':
            if isengnum(command[i-1][0]):
                name=name_list[del_blank(command[i-2])]
                if voice_list.has_key(command[i-1].upper()):
                    script.append('#vo '+voice_list[command[i-1].upper()])
                else:
                    print 'Can not find voice file ',command[i-1]
            else:
                name=name_list[del_blank(command[i-1])]
            if name!=u'':
                script.append('#say '+name+','+command[i+1])
            else:
                script.append('#say '+command[i+1])
        else:
            name==u''
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
            addr.append(str(i))
            i+=2*stringlen
        elif buf[i:i+3]=='\x02\x00\x06' and buf[i+3:i+5]!='\x00\x00':
            i+=3
            stringlen=struct.unpack('i',buf[i:i+4])[0]
            i+=4
            try:
                command.append(buf[i:2*stringlen+i].decode('utf-16'))
                addr.append(str(i))
            except:
                print i,stringlen
                pass
            i+=2*stringlen
        elif buf[i:i+3]=='\x02\x00\x04':
            i+=3
            command.append(str(struct.unpack('i',buf[i:i+4])[0]))
            addr.append(str(i))
            i+=4
        else:
            i+=1
    del buf
    outputlist(addr,command)
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
#command=extract_file('haruka.csx')
#script=parse_script(command)
#outputlist(modify_script(script))
split_file('1.txt','00_a001.txt')


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














