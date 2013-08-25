import pygame, sys, random, time, codecs, string, os, random, struct
import key_codes, e32
from pygame.locals import *
import traceback

try:
    import android
except ImportError:
    android = None

try:
    import pygame.mixer as mixer
except ImportError:
    import android.mixer as mixer

KMdaRepeatForever=0

class Keyboard(object):
    def __init__(self):
        global staticimg,screensize,globalconfig
        self._keyboard_state={}
        self._downs={}
        self._last_pos=(0,0)
        self._pen_down=False
        self._pen_up=False
        keypadsize = staticimg['keypad'].get_size()
        self.keyrects=[]
        if globalconfig['keypad_bottom']==0:
            if globalconfig['keypad_num']==7:
                self.button_codes=[pygame.K_1,pygame.K_3,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_SPACE,pygame.K_DOWN]
            else:
                self.button_codes=[pygame.K_ESCAPE,pygame.K_0,pygame.K_1,pygame.K_3,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_SPACE,pygame.K_DOWN]
            for i in range(0,globalconfig['keypad_num']):
                self.keyrects.append((screensize[0],int(screensize[1]*i/globalconfig['keypad_num']),screensize[0]+keypadsize[0],int(screensize[1]*(i+1)/globalconfig['keypad_num'])))
        else:
            self.button_codes=[pygame.K_ESCAPE,pygame.K_0,pygame.K_1,pygame.K_3,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_UP,pygame.K_SPACE,pygame.K_DOWN]
            for i in range(0,globalconfig['keypad_num']):
                self.keyrects.append((int(screensize[0]*i/globalconfig['keypad_num']),screensize[1],int(screensize[0]*(i+1)/globalconfig['keypad_num']),screensize[1]+keypadsize[1]))
    def key_map(self, scancode):
        if scancode==key_codes.EScancodeSelect:
            return [key_codes.EScancodeSelect,key_codes.EScancode5, pygame.K_RETURN, pygame.K_SPACE]
        elif scancode==key_codes.EScancodeUpArrow:
            return [key_codes.EScancodeUpArrow,key_codes.EScancode2]
        elif scancode==key_codes.EScancodeDownArrow:
            return [key_codes.EScancodeDownArrow,key_codes.EScancode8]
        elif scancode==key_codes.EScancodeLeftArrow:
            return [key_codes.EScancodeLeftArrow,key_codes.EScancode4]
        elif scancode==key_codes.EScancodeRightArrow:
            return [key_codes.EScancodeRightArrow,key_codes.EScancode6]
        elif scancode==key_codes.EScancode1:
            return [key_codes.EScancode1,pygame.K_LCTRL]
        elif scancode==key_codes.EScancode0:
            return [key_codes.EScancode0,pygame.K_F4]
        else:
            return [scancode]
    def handle_event(self):
        global running, screensize, canvas, staticimg, bgmloop, sfx, anime, quitbind
        events  = pygame.event.get()
        if android:
            if android.check_pause():
                if mixer.music.get_busy():
                    mixer.music.stop()
                    music_paused=True
                else:
                    music_paused=False
                VO_STP()
                SE_STP()
                android.wait_for_resume()
                if music_paused:
                    mixer.music.play()
                update_screen()
                update_screen()
            #loop music
            if bgmloop and (not mixer.music.get_busy()):
                mixer.music.play()
            #loop se
            if (sfx['loop']) and (not get_busy_channel(sfx['channelid'])) and sfx['filename']!='':
                if sfx['repeattime']<8:
                    sfx['repeattime']+=1
                    sfxsound=mixer.Sound(sfx['filename'])
                    sfx['channelid']=sfxsound.play()
                else:
                    sfx['repeattime']=0
                    sfx['loop']=False
                    sfx['filename']=''
        #draw anime
        if anime.ison():
            anime.draw()
        #Handle events
        for ev in events :
            if ev.type == pygame.KEYDOWN:
                self.handle_down(ev.key)
            elif ev.type == pygame.KEYUP:
                    self.handle_up(ev.key)
            elif ev.type == pygame.QUIT:
                if quitbind:
                    running=False
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button==1:
                    if quitbind:
                        self.draw_rect(ev.pos)
                        self.handle_down(self.pos_to_key(ev.pos))
                    else:
                        if self.draw_rect(ev.pos):
                            self.handle_down(self.pos_to_key(ev.pos))
                        else:
                            self._last_pos=ev.pos
                            self._pen_down=True
                if ev.button==3:
                    if quitbind:
                        self.handle_down(pygame.K_0)
                    else:
                        self.handle_down(pygame.K_ESCAPE)
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button==1:
                    update_screen()
                    self.handle_up(self.pos_to_key(ev.pos))
                    if not quitbind:
                        self._last_pos=ev.pos
                        self._pen_up=True
            elif ev.type == pygame.MOUSEMOTION:
                if ev.pos[0]>0 and ev.pos[1]>0:
                    self._last_pos=ev.pos
                    
    def handle_down(self,code):
        global running, quitbind, stringres
        if not self.is_down(code):
            self._downs[code]=self._downs.get(code,0)+1
        self._keyboard_state[code]=1
        if code==pygame.K_ESCAPE and quitbind:
                selectid=query(stringres[u'HINT'],stringres[u'SAVE_BRFORE_EXIT'],[stringres[u'SAVE'],stringres[u'DONT_SAVE'],stringres[u'CANCEL']])
                if selectid==0:
                    save_index(0)
                    running=False
                elif selectid==1:
                    running=False
        if code==pygame.K_3:
            Auto_Play()
    def handle_up(self,code):
        self._keyboard_state[code]=0
        self._keyboard_state[key_codes.EScancode1]=0
    def is_down(self,scancode):
        self.handle_event()
        ret=False
        for i in self.key_map(scancode):
            ret=ret or self._keyboard_state.get(i,0)
        return ret
    def pen_down(self):
        ret=self._pen_down
        self._pen_down=False
        return ret
    def pen_up(self):
        ret=self._pen_up
        self._pen_up=False
        return ret
    def get_last_pos(self):
        return self._last_pos
    def pressed(self,scancode):
        self.handle_event()
        ret=False
        for i in self.key_map(scancode): 
            if self._downs.get(i,0):
                self._downs[i]-=1
                ret=ret or True
            else:
                ret=ret or False
        return ret
    def clear_downs(self):
        self._downs={}
        self._keyboard_state={}
    def pos_to_key(self,pos):
        global quitbind
        for i in range(0,len(self.keyrects)):
            keyrect=self.keyrects[i]
            if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                return self.button_codes[i]
        if quitbind:
            return pygame.K_SPACE
        else:
            return pygame.K_RCTRL
    def draw_rect(self,pos):
        global canvas
        for i in range(0,len(self.keyrects)):
            keyrect=self.keyrects[i]
            if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                canvas.fill((128,128,128), (keyrect[0],keyrect[1],keyrect[2]-keyrect[0],keyrect[3]-keyrect[1]))
                pygame.display.flip()
                return True
        return False

class Animation(object):
    def __init__(self):
        global screensize
        self.animeon=False
        self.timer = time.clock()
        self.animimg = pygame.Surface(screensize)
        self.target=(0,0)
        self.loop=False
        self.imgname=u''
    
    def redraw(self):
        global canvas, final_img
        self.animimg.blit(final_img,(0,0))
        self.animimg.blit(self.imgsequence,self.target, self.source_range[self.counter])
        canvas.blit(self.animimg,(0,0))
        
    def draw(self):
        if time.clock() >= self.timer+self.interval:
            self.redraw()
            pygame.display.flip()
            self.counter+=1
            if self.counter>=self.seqlen:
                if self.loop:
                    self.counter=0
                else:
                    self.off()
                    return
            self.timer=time.clock()
        
    def on(self, imgname, seqlen, xpos, ypos, interval, loop):
        global GAME_PATH, gameconfig
        if self.ison():
            self.off()        
        if (not os.path.exists(os.path.join(GAME_PATH,u'system',imgname+'.png'))) or gameconfig[u'anime']==0:
            return
        self.animeon=True
        self.imgname=imgname
        self.counter=0
        self.seqlen=seqlen
        self.loop=loop
        self.interval=float(interval)/1000.0
        self.source_range=[]
        self.target=(xpos, ypos)
        self.imgsequence=load_image(os.path.join(GAME_PATH,u'system',imgname+'.png'), is_alpha=True)
        for i in range(0, self.seqlen):
            self.source_range.append(( (0,i*get_image_height(self.imgsequence)/self.seqlen), (get_image_width(self.imgsequence),get_image_height(self.imgsequence)/self.seqlen) ))
        self.timer = time.clock()

    def off(self, imgname='all'):
        self.animeon=False
        try:
            del self.imgsequence
            del self.masksequence
        except:
            pass

    def ison(self):
        return self.animeon
    def isloop(self):
        return self.loop
    def getsave(self):
        return self.imgname+','+str(self.seqlen)+','+str(self.target[0])+','+str(self.target[1])+','+str(int(self.interval*1000))

#A simple slider
class Slider(object):
    #Constructs the object
    def __init__(self, rect, textpos, value_range, value=0):
        global screensize
        self.rect = pygame.Rect(screensize[0]*rect[0]/100,screensize[1]*rect[1]/100,screensize[0]*rect[2]/100,screensize[1]*rect[3]/100)
        self.textpos = pygame.Rect(screensize[0]*textpos[0]/100,screensize[1]*textpos[1]/100,screensize[0]*textpos[2]/100,screensize[1]*textpos[3]/100)
        self.slider = load_image("slider.png", is_alpha=True)
        self.ypos = self.rect[1]+(self.rect[3]-self.slider.get_size()[1])/2
        self.xpos = self.rect[0]+self.rect[2]*(value-value_range[0])/(value_range[1]-value_range[0])
        self.value = value
        self.value_range = value_range
        self.clicked = False

    def inrange(self, pos):
        return self.rect.collidepoint(pos)
    def activate(self):
        self.clicked = True
    def deactivate(self):
        self.clicked = False
    def update(self,pos):
        if self.clicked:
            if pos[0]<self.rect[0]:
                self.xpos=self.rect[0]
            elif pos[0]>self.rect[0]+self.rect[2]:
                self.xpos=self.rect[0]+self.rect[2]
            else:
                self.xpos=pos[0]
            self.value = self.value_range[0]+(self.xpos - self.rect[0])*(self.value_range[1]-self.value_range[0])/self.rect[2]
    def get_value(self):
        return self.value
    def render(self, surface):
        surface.blit(self.slider, (self.xpos-self.slider.get_size()[0]/2, self.ypos))
        text=str(self.value)
        measure_result=measure_text(text)
        text_origin=( self.textpos[0]+(self.textpos[2]-measure_result[0][2]+measure_result[0][0])/2,self.textpos[1]+(self.textpos[3]-measure_result[0][3]+measure_result[0][1])/2)
        draw_text(text,text_origin=text_origin,color=(255,255,255),on_canvas=False)

#A simple checkbox
class Checkbox(object):
    #Constructs the object
    def __init__(self, rect, value=True):
        global screensize
        self.rect = pygame.Rect(screensize[0]*rect[0]/100,screensize[1]*rect[1]/100,screensize[0]*rect[2]/100,screensize[1]*rect[3]/100)
        self.check = load_image("checkbox.png", is_alpha=True)
        self.value = value

    def inrange(self, pos):
        return self.rect.collidepoint(pos)
    def activate(self):
        self.value = not self.value
    def deactivate(self):
        return
    def update(self,pos):
        return
    def get_value(self):
        return int(self.value)
    def render(self, surface):
        if self.value:
            surface.blit(self.check, (self.rect[0]+(self.rect[2]-self.check.get_size()[0])/2, self.rect[1]+(self.rect[3]-self.check.get_size()[1])/2))

def ConfigForm():
    global final_img,staticimg,gameconfig,keyboard,screensize
    modify_game_config(False)
    controls={'fontsize':Slider((49,15,42,7),(36,15,7,7),(10,30),gameconfig['fontsize']),
              'textspeed':Slider((49,29,42,7),(36,29,7,7),(0,5),gameconfig[u'textspeed']),
              'fontaa':Checkbox((37,44,5,8),gameconfig[u'fontaa']),
              'font':Checkbox((37,54,5,8),gameconfig[u'font']),
              'grayselected':Checkbox((37,65,5,8),gameconfig[u'grayselected']),
              'hint':Checkbox((82,44,5,8),gameconfig[u'hint']),
              'playvideo':Checkbox((82,54,5,8),gameconfig[u'playvideo'])}
    configimg=load_image("config.png", width=screensize[0], height=screensize[1], is_alpha=True)
    final_img.blit(staticimg['tempimg'],(0,0))
    draw_image(configimg, on_canvas=False)
    staticimg['oldimg'].blit(final_img,(0,0))
    looping=True
    while looping:
        #Let's not overload the CPU
        pygame.time.wait(20)
        if android:
            if android.check_pause():
                android.wait_for_resume()
        #Get input
        events  = pygame.event.get()
        for ev in events:
            if ev.type == QUIT:
                pygame.quit()
                return
            elif ev.type == pygame.KEYDOWN:
                if ev.key==pygame.K_ESCAPE or ev.key==pygame.K_SPACE or ev.key==pygame.K_RETURN:
                    looping=False
                    break
            elif ev.type == pygame.MOUSEBUTTONDOWN:
                if ev.button==1:
                    if ev.pos[0]>screensize[0] or ev.pos[1]>screensize[1]:
                        looping=False
                        break
                    for name in controls:
                        if controls[name].inrange(ev.pos):
                            controls[name].activate()
                            controls[name].update(ev.pos)
                            break
                elif ev.button==3:
                    looping=False
                    break
            elif ev.type == pygame.MOUSEBUTTONUP:
                if ev.button==1:
                    for name in controls:
                        controls[name].deactivate()
            elif ev.type == pygame.MOUSEMOTION:
                for name in controls:
                    controls[name].update(ev.pos)
        final_img.blit(staticimg['oldimg'],(0,0))
        for name in controls:
            controls[name].render(final_img)
        update_screen()
    for name in controls:
        gameconfig[name]=controls[name].get_value()
    write_game_config()
    modify_game_config(True)
    set_font()
    keyboard.clear_downs()

def update_screen():
    global final_img, canvas, screensize, anime, staticimg, globalconfig
    if anime.ison():
        anime.redraw()
    else:
        canvas.blit(final_img,(0,0))
    if staticimg['keypad']:
        if globalconfig['keypad_bottom']==0:
            canvas.blit(staticimg['keypad'], (screensize[0],0))
        else:
            canvas.blit(staticimg['keypad'], (0,screensize[1]))
    pygame.display.flip()

def draw_text(char_list,text_origin=(0,0),color=(255,255,255),on_canvas=True, on_final_img=True):
    global canvas,textfont,final_img,gameconfig
    if len(char_list)==0:
        return
    try:
        text = textfont.render(char_list, gameconfig[u'fontaa'], color)
        if bool(gameconfig[u'font']):
            if (color[0]+color[1]+color[2]<256):#dark text, white shadow
                basecolor=(255,255,255)
            else:
                basecolor=(0,0,0)
            base = textfont.render(char_list, gameconfig[u'fontaa'], basecolor)
            offset=max(1,int(gameconfig[u'fontsize']/16))
            base_origin=(text_origin[0]+offset,text_origin[1]+offset)
        if on_final_img:
            if bool(gameconfig[u'font']):
                final_img.blit(base, base_origin)
            final_img.blit(text, text_origin)
        if on_canvas:
            if bool(gameconfig[u'font']):
                canvas.blit(base, base_origin)
            canvas.blit(text, text_origin)
            pygame.display.flip()
        del text
    except:
        print 'Error while drawing',char_list

def draw_image(img,img_origin=(0,0),on_canvas=True, on_final_img=True):
    #draws an image to the screen, the image should be pre-rotated to fit the rotation of the screen, but the img_origin is for normal landscape
    global canvas,final_img
    if on_final_img:
        final_img.blit(img, img_origin)
        if on_canvas:
            update_screen()
    else:
        if on_canvas:
            canvas.blit(img, img_origin)
            pygame.display.flip()

def display_cursor(cursororigin, wait_for_vo=False):
    global keyboard, staticimg, final_img, background, vo, auto_play, gameconfig, running
    if keyboard.is_down(key_codes.EScancode1):
        return
    cursororigin=(cursororigin[0],cursororigin[1]+gameconfig[u'fontsize']/4)
    space=(0,1,3,5,6,5,3,1)
    start_time=time.clock()
    back_img=pygame.Surface((get_image_width(staticimg['message_cursor']),get_image_height(staticimg['message_cursor'])+max(space)))
    back_img.blit(final_img,(0,0),(cursororigin,get_image_size(back_img)))
    draw_image(staticimg['message_cursor'],img_origin=cursororigin)
    temp_img=pygame.Surface(back_img.get_size())
    e32.ao_yield()
    i=0
    if gameconfig[u'prefetching']:
        Prefetching()
        if (vo!=None and get_busy_channel(vo)):
            Prefetching()
    while running:
        if keyboard.pressed(key_codes.EScancodeSelect) or keyboard.pressed(key_codes.EScancode1):
            break
        if keyboard.pressed(key_codes.EScancode0):
            Menu()
            break
        if keyboard.pressed(key_codes.EScancodeLeftArrow):
            hide_msgbox()
        if auto_play and (not background) and ( (not wait_for_vo) or (not get_busy_channel(vo)) ):
            #e32.ao_sleep(0.5)
            end_time=time.clock()
            if end_time-start_time>0.8:
                break
        origin=(0,space[i])
        temp_img.blit(back_img,(0,0))
        temp_img.blit(staticimg['message_cursor'],origin)
        draw_image(temp_img,img_origin=cursororigin)
        e32.ao_sleep(0.1)
        i=(i+1)%len(space)
    draw_image(back_img,img_origin=cursororigin)

#this function draws a paragraph that may contain \n character. both per-caracter and instance display is supported. a rect area is needed.
def draw_paragraph(paragraph, topleft, bottomright, color, on_canvas=True):
    global gameconfig, textfont, keyboard, final_img, staticimg
    #check if the coordinates are legal
    if topleft[0]>bottomright[0] or topleft[1]>bottomright[1]:
        print 'illegal coordinates of topleft and bottomright'
        return (0,0)
    line_num=0
    offset=max(1,int(gameconfig[u'fontsize']/16))
    staticimg['paragraph_img'].fill((255,255,255,0))
    for line in paragraph:
        #for each line in char_list, draw them char by char if no key is pressed
        #textorigin is the start point of each line
        measure_result=measure_text(line)
        textorigin=(topleft[0],topleft[1]+(gameconfig[u'fontsize']+1)*(line_num))
        text = textfont.render(line, gameconfig[u'fontaa'], color)
        if bool(gameconfig[u'font']):
            baseorigin=(textorigin[0]+offset,textorigin[1]+offset)
            base = textfont.render(line, gameconfig[u'fontaa'], (255-color[0],255-color[1],255-color[2]))
            staticimg['paragraph_img'].blit(base, baseorigin)
        staticimg['paragraph_img'].blit(text, textorigin)
        line_num+=1
    final_img.blit(staticimg['paragraph_img'],(0,0))
    if on_canvas:
        update_screen()
    textorigin=(topleft[0]+measure_result[1],textorigin[1])
    if textorigin[0] > bottomright[0]-gameconfig[u'fontsize']:
        textorigin=(topleft[0],textorigin[1]+gameconfig[u'fontsize']+1)
    return textorigin

def measure_text(text, maxwidth=-1):
    global textfont,gameconfig
    if maxwidth<=0:
        textsize=textfont.size(text)
        return ( (0,0,textsize[0],textsize[1]), textsize[0], len(text))
    else:
        i=min(len(text),maxwidth//gameconfig[u'fontsize'])
        if textfont.size(text[0:i])[0]<maxwidth:
            while i<=len(text) and textfont.size(text[0:i])[0]<maxwidth:
                i=i+1
            i=i-1
        else:
            while i>0 and textfont.size(text[0:i])[0]>=maxwidth:
                i=i-1
            i=i+1
        textsize=textfont.size(text[0:i])
        return ( (0,0,textsize[0],textsize[1]), textsize[0], i)

##        i=0
##        while i<=len(text) and textfont.size(text[0:i])[0]<maxwidth:
##            i+=1
##        i-=1
##        textsize=textfont.size(text[0:i])
##        return ( (0,0,textsize[0],textsize[1]), textsize[0], i)
    
def get_image_width(img):
    return img.get_width()

def get_image_height(img):
    return img.get_height()

def get_image_size(img):
    return img.get_size()

def load_keypad(autoon=False):
    global screensize,globalconfig,staticimg,gameconfig
    greycolor=(128,128,128)
    if android:
        if gameconfig.has_key(u'imagesize'):
            displayinfo=pygame.display.Info()
            if globalconfig['keypad_horizontal']==1 and (displayinfo.current_h-displayinfo.current_w*gameconfig[u'imagesize'][1]/gameconfig[u'imagesize'][0] >= displayinfo.current_w/18):
                globalconfig['keypad_bottom']=1
                globalconfig['keypad_num']=9
                if globalconfig['original_ratio']==1:
                    keypad_thickness=displayinfo.current_h-displayinfo.current_w*gameconfig[u'imagesize'][1]/gameconfig[u'imagesize'][0]
                else:
                    keypad_thickness=displayinfo.current_w/18
            else:
                if globalconfig['keypad_extend']==1:
                    globalconfig['keypad_num']=9
                else:
                    globalconfig['keypad_num']=7
                if globalconfig['original_ratio']==1:
                    keypad_thickness=max( displayinfo.current_h/globalconfig['keypad_num'], displayinfo.current_w-displayinfo.current_h*gameconfig[u'imagesize'][0]/gameconfig[u'imagesize'][1] )
                else:
                    keypad_thickness=displayinfo.current_h/globalconfig['keypad_num']
        else:
            globalconfig['keypad_num']=7
            globalconfig['keypad_bottom']=0
            keypad_thickness=screensize[1]/globalconfig['keypad_num']
    else:
        globalconfig['keypad_bottom']=0
        globalconfig['keypad_num']=9
        keypad_thickness=screensize[1]/globalconfig['keypad_num']
    #calculate keypad size
    if globalconfig['keypad_bottom']==0:
        if globalconfig['keypad_num']==7:
            tempimg=load_image("keypad1.png", width=None, height=screensize[1], is_alpha=True)
        else:
            tempimg=load_image("keypad2.png", width=None, height=screensize[1], is_alpha=True)
        staticimg['keypad']=pygame.Surface((keypad_thickness,screensize[1]))
        staticimg['keypad'].fill((0,0,0))
        if autoon:
            staticimg['keypad'].fill(greycolor,(0,(globalconfig['keypad_num']-6)*screensize[1]/globalconfig['keypad_num'],get_image_width(staticimg['keypad']),screensize[1]/globalconfig['keypad_num']))
        for i in range(1,globalconfig['keypad_num']):
            pygame.draw.line(staticimg['keypad'],(255,255,255),(0,i*screensize[1]/globalconfig['keypad_num']),(get_image_width(staticimg['keypad']),i*screensize[1]/globalconfig['keypad_num']),1)
        staticimg['keypad'].blit(tempimg,((keypad_thickness-get_image_width(tempimg))/2,0))
    else:
        tempimg=load_image("keypad3.png", width=screensize[0], height=None, is_alpha=True)
        staticimg['keypad']=pygame.Surface((screensize[0],keypad_thickness))
        staticimg['keypad'].fill((0,0,0))
        if autoon:
            staticimg['keypad'].fill(greycolor,(3*screensize[0]/globalconfig['keypad_num'],0,screensize[0]/globalconfig['keypad_num'],get_image_height(staticimg['keypad'])))
        for i in range(1,globalconfig['keypad_num']):
            pygame.draw.line(staticimg['keypad'],(255,255,255),(i*screensize[0]/globalconfig['keypad_num'],0),(i*screensize[0]/globalconfig['keypad_num'],get_image_height(staticimg['keypad'])),1)
        staticimg['keypad'].blit(tempimg,(0,(keypad_thickness-get_image_height(tempimg))/2))

def load_select_image(filename,seqlen):
    selectimg=load_image(os.path.join(GAME_PATH,'system',filename+'.png'), is_alpha=True)
    imagelist=[]
    for i in range(0,seqlen):
        tempimg=pygame.Surface((get_image_width(selectimg)/2,get_image_height(selectimg)/seqlen),flags=pygame.SRCALPHA)
        tempimg.blit(selectimg,(0,0), (
            (0,i*get_image_height(selectimg)/seqlen),
            (get_image_width(selectimg)/2,get_image_height(selectimg)/seqlen) ) )
        highlightimg=pygame.Surface((get_image_width(selectimg)/2,get_image_height(selectimg)/seqlen),flags=pygame.SRCALPHA)
        highlightimg.blit(selectimg,(0,0), (
            (get_image_width(selectimg)/2,i*get_image_height(selectimg)/seqlen),
            (get_image_width(selectimg),get_image_height(selectimg)/seqlen) ) )
        imagelist.append(tempimg)
        imagelist.append(highlightimg)
    return imagelist
    
def load_select_images(filenamelist):
    imagelist=[]
    for filename in filenamelist:
        selectimg=load_image(os.path.join(GAME_PATH,'system',filename+'.png'), is_alpha=True)
        tempimg=pygame.Surface((get_image_width(selectimg)/2,get_image_height(selectimg)),flags=pygame.SRCALPHA)
        tempimg.blit(selectimg,(0,0), ( (0,0),(get_image_width(selectimg)/2,get_image_height(selectimg)) ) )
        highlightimg=pygame.Surface((get_image_width(selectimg)/2,get_image_height(selectimg)),flags=pygame.SRCALPHA)
        highlightimg.blit(selectimg,(0,0), ( (get_image_width(selectimg)/2,0),(get_image_width(selectimg)/2,get_image_height(selectimg)) ) )
        imagelist.append(tempimg)
        imagelist.append(highlightimg)
    return imagelist

def load_image(imgfilename, width=None, height=None, is_alpha=False, imgtype='chara'):
    global screensize,scalemode,scaleratio,gameconfig
    if not os.path.exists(imgfilename):
        query(stringres[u'WARNING'],stringres[u'CAN_NOT_FIND']+imgfilename,[stringres[u'OK']])
        image=pygame.Surface(screensize)
        image.fill((0,0,0))
        return image
    #if type(imgfilename)==unicode:
    #    imgfilename=imgfilename.encode('gbk')
    image=pygame.image.load(imgfilename)
    if is_alpha:
        image=image.convert_alpha()
    else:
        image=image.convert(24)
    if width!=None and height!=None:
        if width!=image.get_width() or height!=image.get_height():
            if scalemode==2:
                image=pygame.transform.smoothscale(image, (width,height))
            else:
                image=pygame.transform.scale(image, (width,height))
        else:
            pass
    elif width==None and height!=None:
        if height!=image.get_height():
            if scalemode==2:
                image=pygame.transform.smoothscale(image, (height*get_image_width(image)/get_image_height(image),height))
            else:
                image=pygame.transform.scale(image, (height*get_image_width(image)/get_image_height(image),height))
        else:
            pass
    elif width!=None and height==None:
        if width!=image.get_width():
            if scalemode==2:
                image=pygame.transform.smoothscale(image, (width,width*get_image_height(image)/get_image_width(image)))
            else:
                image=pygame.transform.scale(image, (width,width*get_image_height(image)/get_image_width(image)))
        else:
            pass
    else:
        width=get_image_width(image)
        height=get_image_height(image)
        #if imgtype=='bg':
        img_scaleratio=scaleratio
        #else:
        #    img_scaleratio=(screensize[1],gameconfig[u'imagesize'][1])
        if scalemode==0:
            pass
        elif scalemode==1:
            image=pygame.transform.scale(image, (width*img_scaleratio[0]/img_scaleratio[1],height*img_scaleratio[0]/img_scaleratio[1]))
        elif scalemode==2:
            image=pygame.transform.smoothscale(image, (width*img_scaleratio[0]/img_scaleratio[1],height*img_scaleratio[0]/img_scaleratio[1]))
    return image

def save_image(image_obj, imagepath):
    try:
        pygame.image.save(image_obj, imagepath)
        return True
    except:
        return False

def BGLoad(bgindex,bgfilename,percentorig=(0,0)):
    global cache, save, gameconfig, final_img, bgorigin, screensize, staticimg
    if not save.has_key(u'bg') or save[u'bg']!=bgfilename:
        save[u'bg']=bgfilename
        if cache['bg'].has_key(bgfilename):
            staticimg['bg']=cache['bg'][bgfilename]['res']
            cache['bg'][bgfilename]['usetime']-=1
            if cache['bg'][bgfilename]['usetime']==0:
                del cache['bg'][bgfilename]
        else:
            unpack_file(bgfilename,u'bgformat')
            staticimg['bg']=load_image(os.path.join(GAME_PATH,'bg',bgfilename+gameconfig[u'bgformat']),imgtype='bg')
    save[u'bgpercentorig']=percentorig
    if percentorig!=(0,0):
        bgorigin=( -percentorig[0]*get_image_width(staticimg['bg'])/100 , -percentorig[1]*get_image_height(staticimg['bg'])/100 )
    else:
        bgorigin=((screensize[0]-get_image_width(staticimg['bg']))/2, (screensize[1]-get_image_height(staticimg['bg']))/2)

def MASK(length, new_img, mask_img, img_origin=(0,0)):
    global final_img, keyboard, staticimg, in_fade_out, bgorigin
    if keyboard.is_down(key_codes.EScancode1) or length<20 or in_fade_out:
        draw_image(new_img,img_origin=img_origin,on_canvas=not in_fade_out)
        e32.ao_yield()
        return
    else:
        length=float(length)/2000.0
    staticimg['oldimg'].blit(final_img,(0,0))
    maskorigin=((screensize[0]-get_image_width(mask_img))/2, (screensize[1]-get_image_height(mask_img))/2)
    #oldimg to mask
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        level=int(255*(current_time-start_time)/length)
        staticimg['tempimg'].fill((level,level,level))
        staticimg['tempimg'].blit(mask_img, maskorigin, None, pygame.BLEND_MIN)
        final_img.blit(staticimg['oldimg'], (0,0))
        final_img.blit(staticimg['tempimg'], (0,0), None, pygame.BLEND_SUB)
        update_screen()
        current_time=time.clock()
    #mask to black
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        level=int(255*(current_time-start_time)/length)
        staticimg['tempimg'].fill((level,level,level))
        staticimg['tempimg'].blit(mask_img, maskorigin, None, pygame.BLEND_MAX)
        final_img.blit(staticimg['oldimg'], (0,0))
        final_img.blit(staticimg['tempimg'], (0,0), None, pygame.BLEND_SUB)
        update_screen()
        current_time=time.clock()
    #black to mask
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        level=255-int(255*(current_time-start_time)/length)
        staticimg['tempimg'].fill((level,level,level))
        staticimg['tempimg'].blit(mask_img, maskorigin, None, pygame.BLEND_MAX)
        final_img.blit(new_img, img_origin)
        final_img.blit(staticimg['tempimg'], (0,0), None, pygame.BLEND_SUB)
        update_screen()
        current_time=time.clock()
    #black to mask
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        level=255-int(255*(current_time-start_time)/length)
        staticimg['tempimg'].fill((level,level,level))
        staticimg['tempimg'].blit(mask_img, maskorigin, None, pygame.BLEND_MIN)
        final_img.blit(new_img, img_origin)
        final_img.blit(staticimg['tempimg'], (0,0), None, pygame.BLEND_SUB)
        update_screen()
        current_time=time.clock()
    draw_image(new_img,img_origin=img_origin)
    e32.ao_yield()

def set_font():
    global textfont, gameconfig, GAME_PATH
    fontfilename=os.path.join(os.getcwd(),'default.ttf')
    if GAME_PATH!=None:
        if os.path.exists(os.path.join(GAME_PATH,'system','default.ttf')):
            fontfilename=os.path.join(GAME_PATH,'system','default.ttf')
    textfont = pygame.font.Font(fontfilename, gameconfig['fontsize'])

def CHAScroll(chaindex, length, startpos, endpos, beginalpha, mode):
    #startpos and endpos are percent of the bg size
    global final_img, chara, staticimg, keyboard
    if keyboard.is_down(key_codes.EScancode1):
        length=0.01
    else:
        length=float(length)/1000.0
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        xpos=startpos[0]+(endpos[0]-startpos[0])*(current_time-start_time)/length
        ypos=startpos[1]+(endpos[1]-startpos[1])*(current_time-start_time)/length
        CHASetPos(chaindex,xpos,ypos,mode)
        CHADisp(transition=None)
        current_time=time.clock()
    CHASetPos(chaindex,endpos[0],endpos[1],mode)
    CHADisp(transition=None)
    e32.ao_yield()

def Load_system_images():
    global staticimg,gameconfig
    change_message_box()
    #load message cursor
    staticimg['message_cursor']=load_image(os.path.join(GAME_PATH,'system','message_cursor.png'), height=gameconfig[u'fontsize'], is_alpha=True)
    #load option image
    staticimg['menuimg']=load_image(os.path.join(GAME_PATH,'system','menu.png'), is_alpha=True)

def change_message_box(msgbox=u'message',namebox=u'name'):
    global staticimg,screensize,gameconfig,save
    save[u'msgbox']=msgbox
    save[u'namebox']=namebox
    #load message box
    staticimg['messagebox']=load_image(os.path.join(GAME_PATH,u'system',msgbox+u'.png'), width=screensize[0],is_alpha=True)
    if get_image_height(staticimg['messagebox'])>screensize[1]:
        staticimg['messagebox']=load_image(os.path.join(GAME_PATH,u'system',msgbox+u'.png'), width=screensize[0],height=screensize[1],is_alpha=True)
    #load message name box
    staticimg['message_name']=load_image(os.path.join(GAME_PATH,u'system',namebox+u'.png'), height=int(gameconfig[u'fontsize']*1.7),is_alpha=True)

def BGMPlay(bgmfilename,playtime=0):
    global save, gameconfig, bgmloop, bgmstart
    try:
        if mixer.music.get_busy():
            mixer.music.stop()
        bgmlowername=bgmfilename #.lower()
        save[u'bgm']=bgmlowername
        bgm_path=os.path.join(GAME_PATH,'bgm',bgmlowername+gameconfig[u'bgmformat'])
        #if type(bgm_path)==unicode:
        #    bgm_path=bgm_path.encode('gbk')
        if not os.path.exists(bgm_path):
            print 'Can not find bgm file'
            return
        mixer.music.load(bgm_path)
        mixer.music.play(playtime-1)
        bgmstart=time.clock()
        if playtime==0:
            bgmloop=True
    except:
        print 'Error while playing bgm file'

def BGMStop():
    global save, bgmloop
    save[u'bgm']=u''
    bgmloop=False
    if mixer.music.get_busy():
        mixer.music.stop()

def delay_until(end_time):
    global bgmstart
    if not mixer.music.get_busy():
        return
    #end_time is an int value, in ms,
    end_time_s=end_time/1000.0+bgmstart
    e32.reset_inactivity()
    current_time=time.clock()
    print "delay_until", bgmstart, current_time, end_time_s
    if current_time<end_time_s:
        delay=end_time_s-current_time
        e32.ao_sleep(delay)

def stop_channel(channel_id):
    try:
        if android and channel_id!=None:
            mixer.Channel(channel_id).stop()
    except:
        print 'Error while stopping channel',channel_id

def get_busy_channel(channel_id):
    try:
        if android and channel_id!=None:
            return mixer.Channel(channel_id).get_busy()
        else:
            return False
    except:
        return False

def SE_WAIT():
    global sfx,keyboard
    #wait until the current se is stopped or key pressed
    if not sfx:
        return
    if not keyboard.is_down(key_codes.EScancode1):
        while (not keyboard.pressed(key_codes.EScancodeSelect) and get_busy_channel(sfx['channelid']) and sfx['filename']!='' ) :
            e32.ao_sleep(0.1)
            e32.reset_inactivity()
            end_time=time.clock()

def SE_STA(sefilename, duration=None, times=1):
    global sfx, gameconfig
    try:
        SE_STP()
        unpack_file(sefilename,u'seformat')
        sepath=os.path.join(GAME_PATH,'se',sefilename+gameconfig[u'seformat'])
        #if type(sepath)==unicode:
        #    sepath=sepath.encode('gbk')
        if not os.path.exists(sepath):
                print 'Can not find sound effect file'
                return
        sfxsound=mixer.Sound(sepath)
        sfx['channelid']=sfxsound.play()
        sfx['filename']=sepath
        if times==0:
            sfx['loop']=True
    except:
        print 'Error while playing se file'

def SE_STP():
    global sfx
    try:
        sfx['loop']=False
        sfx['repeattime']=0
        stop_channel(sfx['channelid'])
    except:
        print 'Error while stopping se file'

def VO_STA(vofilename):
    global vo,keyboard,gameconfig,cache
    try:
        if not keyboard.is_down(key_codes.EScancode1):
            vofilename=vofilename.upper()
            purge_voice()
            if cache['vo'].has_key(vofilename):
                vosound=cache['vo'][vofilename]['res']
                cache['vo'][vofilename]['usetime']-=1
                if cache['vo'][vofilename]['usetime']==0:
                    del cache['vo'][vofilename]
            else:
                unpack_file(vofilename,u'voiceformat')
                vopath=os.path.join(GAME_PATH,'voice',vofilename+gameconfig[u'voiceformat'])
                #if type(vopath)==unicode:
                #    vopath=vopath.encode('gbk')
                if not os.path.exists(vopath):
                    print 'Can not find voice file'
                    return
                stop_channel(vo)
                vosound=mixer.Sound(vopath)
            vo=vosound.play()
    except:
        print 'Error while playing voice file'

def VO_STP():
    global vo
    stop_channel(vo)
    vo=None

def PlayMovie(videofilename):
    if android:
        videopath=os.path.join(GAME_PATH,'video',videofilename+'.mp4')
        try:
            android.play_video(videopath)
        except:
            print 'Error while playing video file'
        update_screen()

def Select(choices, hint=u'HINT_NONE'):
    global keyboard, final_img, gameconfig, textfont, cache, f, screensize
    optionimg=load_image(os.path.join(GAME_PATH,'system','option.png'), is_alpha=True)
    img_size=(get_image_width(optionimg),get_image_height(optionimg))
    img_origin=((screensize[0]-img_size[0])/2,40)
    select_text=SelectText(choices,topleft=img_origin,bottomright=(img_origin[0]+img_size[0],img_origin[1]+img_size[1]),textcolor=gameconfig[u'textcolor'],hint=hint)
    draw_image(optionimg,img_origin=img_origin, on_canvas=False)
    ret=select_text.select()
    del select_text
    return ret

def bind_quit():
    global quitbind
    quitbind=True

def unbind_quit():
    global quitbind
    quitbind=False

def query(title_text,text,buttons):
    global final_img,staticimg,screensize,gameconfig
    staticimg['oldimg'].blit(final_img,(0,0))
    queryimg=load_image('dialog.png', width=screensize[0]*7/10, is_alpha=True)
    queryimgsize=queryimg.get_size()
    n=len(buttons)
    if n<3:
        buttonimg=load_image('button.png', height=queryimgsize[1]/5)
    else:
        buttonimg=load_image('button_s.png', height=queryimgsize[1]/5)
    buttonimgsize=buttonimg.get_size()
    #display dialog
    queryimg_origin=((screensize[0]-queryimgsize[0])/2,(screensize[1]-queryimgsize[1])/2)
    final_img.blit(queryimg,queryimg_origin)
    #display title
    measure_result=measure_text(title_text)
    text_origin=(queryimg_origin[0]+(queryimgsize[0]-measure_result[0][2]+measure_result[0][0])/2,
                 queryimg_origin[1]+(queryimgsize[1]*31/165-measure_result[0][3]+measure_result[0][1])/2 )
    draw_text(title_text,color=(255,255,255),text_origin=text_origin,on_canvas=False)
    #draw buttons
    buttonrects=[]
    for i in range(0,n):
        buttoncenter=( queryimg_origin[0]+queryimgsize[0]*(2*i+1)/2/n, queryimg_origin[1]+queryimgsize[1]*140/165 )
        final_img.blit(buttonimg,(buttoncenter[0]-buttonimgsize[0]/2,buttoncenter[1]-buttonimgsize[1]/2))
        measure_result=measure_text(buttons[i])
        text_origin=(buttoncenter[0]-(measure_result[0][2]-measure_result[0][0])/2,buttoncenter[1]-(measure_result[0][3]-measure_result[0][1])/2)
        draw_text(buttons[i],color=(255,255,255),text_origin=text_origin,on_canvas=False)
        buttonrects.append(pygame.Rect(buttoncenter[0]-buttonimgsize[0]/2,buttoncenter[1]-buttonimgsize[1]/2,buttonimgsize[0],buttonimgsize[1]))
    #display content
    oldfontsize=gameconfig[u'fontsize']
    oldfont=gameconfig[u'font']
    if len(text)>30:
        gameconfig[u'fontsize']=queryimgsize[0]/18
    gameconfig[u'font']=0
    set_font()
    pages=split_paragraph(text,queryimgsize[0]*98/100,queryimgsize[1]*100/165)
    draw_paragraph(pages[0], (queryimg_origin[0]+queryimgsize[0]*2/100,queryimg_origin[1]+queryimgsize[1]*31/165),
                   (queryimg_origin[0]+queryimgsize[0],queryimg_origin[1]+queryimgsize[1]) , (0,0,0), False)
    update_screen()
    looping=True
    while looping:
        events  = pygame.event.get()
        for ev in events :
            if ev.type == pygame.MOUSEBUTTONUP:
                if ev.button==1:
                    for i in range(0,n):
                        if buttonrects[i].collidepoint(ev.pos):
                            ret=i
                            looping=False
                            break
        e32.ao_sleep(0.1)
    final_img.blit(staticimg['oldimg'],(0,0))
    gameconfig[u'fontsize']=oldfontsize
    gameconfig[u'font']=oldfont
    set_font()
    return ret

def modify_game_config(tobak=True):
    global gameconfig, gameconfigbak
    if tobak:
        #backup gameconfig
        gameconfigbak[u'platform']=gameconfig[u'platform']
        gameconfigbak[u'prefetching']=gameconfig[u'prefetching']
        gameconfigbak[u'fontsize']=gameconfig[u'fontsize']
        gameconfigbak[u'msgtb']=gameconfig[u'msgtb']
        gameconfigbak[u'msglr']=gameconfig[u'msglr']
        gameconfigbak[u'nameboxorig']=gameconfig[u'nameboxorig']
        #modify gameconfig
        gameconfig[u'platform']=u'pygame'
        gameconfig[u'prefetching']=1
        gameconfig[u'fontsize']=gameconfig[u'fontsize']*screensize[1]/360
        gameconfig[u'msgtb']=(gameconfig[u'msgtb'][0]*screensize[1]/360, gameconfig[u'msgtb'][1]*screensize[1]/360)
        gameconfig[u'msglr']=(gameconfig[u'msglr'][0]*screensize[0]/540, gameconfig[u'msglr'][1]*screensize[0]/540)
        gameconfig[u'nameboxorig']=(gameconfig[u'nameboxorig'][0]*screensize[0]/540, gameconfig[u'nameboxorig'][1]*screensize[1]/360)
    else:
        #restore gameconfig
        gameconfig[u'platform']=gameconfigbak[u'platform']
        gameconfig[u'prefetching']=gameconfigbak[u'prefetching']
        gameconfig[u'fontsize']=gameconfigbak[u'fontsize']
        gameconfig[u'msgtb']=gameconfigbak[u'msgtb']
        gameconfig[u'msglr']=gameconfigbak[u'msglr']
        gameconfig[u'nameboxorig']=gameconfigbak[u'nameboxorig']

def error_log(text):
    global LOG_PATH
    try:
        logfile=file(LOG_PATH,'a')
        logfile.write(text+'\r\n')
        logfile.close()
    except:
        pass

def create_nomedia(folder):
    global GAME_PATH
    try:
        if os.path.exists(os.path.join(GAME_PATH,folder)):
            if not os.path.exists(os.path.join(GAME_PATH,folder,'.nomedia')):
                nomediafile=file(os.path.join(GAME_PATH,folder,'.nomedia'),'w')
                nomediafile.close()
    except:
        pass

def cache_add_sel(choices,hint,cache_pos,bak_pos):
    return

def cache_add(type,filename,cache_pos,bak_pos):
    global cache, gameconfig
    if cache[type].has_key(filename):
        cache[type][filename]['cache_pos']=cache_pos
        cache[type][filename]['usetime']+=1
    else:
        if type=='bg':
            unpack_file(filename,u'bgformat')
            temp_bg=load_image(os.path.join(GAME_PATH,'bg',filename+gameconfig[u'bgformat']))
            cache[type][filename]={'res':temp_bg, 'cache_pos':cache_pos, 'usetime':1}
        if type=='chara':
            unpack_file(filename,u'charaformat')
            temp_chara=load_image(os.path.join(GAME_PATH,'chara',filename+gameconfig[u'charaformat']),is_alpha=True)
            cache[type][filename]={'res':temp_chara, 'cache_pos':cache_pos, 'usetime':1}
        if type=='vo':
            filename=filename.upper()
            unpack_file(filename,u'voiceformat')
            if not os.path.exists(os.path.join(GAME_PATH,'voice',filename+gameconfig[u'voiceformat'])):
                print 'Can not find voice file',filename
                return
            try:
                temp_vo=mixer.Sound(os.path.join(GAME_PATH,'voice',filename+gameconfig[u'voiceformat']))
                cache[type][filename]={'res':temp_vo, 'cache_pos':cache_pos, 'usetime':1}
            except:
                pass
        if type=='bgm':
            pass

#=========================================================
#                Platform half-independent code
#=========================================================

class SelectText(object):
    def __init__(self,textlist,topleft,bottomright,textcolor=(255,255,255),init_highlight=-1,hint=u'HINT_NONE',hint_origin=(0,40),varlist=None):
        global final_img
        self.resultmap=[]
        if varlist!=None:
            self.textlist=[]
            for i in range(0, len(textlist)):
                if varlist[i]:
                    self.textlist.append(textlist[i])
                    self.resultmap.append(i)
        else:
            self.textlist=textlist
            for i in range(0, len(textlist)):
                self.resultmap.append(i)
        self.topleft=topleft
        self.bottomright=bottomright
        self.highlightpos=init_highlight
        if init_highlight==-1:
            self.menuenable=True
        else:
            self.menuenable=False
        self.hint=hint
        self.textcolor=textcolor
        self.clock=time.clock()
        self.hintbool=[]
        self.dstarealist=[]
        for i in range(0, len(self.textlist)):
            self.dstarealist.append((
                self.topleft[0],
                (self.bottomright[1]+self.topleft[1]-len(self.textlist)*(gameconfig[u'fontsize']+3))/2+i*(gameconfig[u'fontsize']+3),
                self.bottomright[0],
                (self.bottomright[1]+self.topleft[1]-len(self.textlist)*(gameconfig[u'fontsize']+3))/2+(i+1)*(gameconfig[u'fontsize']+3)
                ))
        if gameconfig[u'platform']==u'pygame':
            self.oldimg=pygame.Surface(final_img.get_size())
            self.backupimg=pygame.Surface(final_img.get_size())
            self.highlightimg=load_image(os.path.join(GAME_PATH,'system','sel_highlight.png'), is_alpha=True)
        else:
            self.oldimg=Image.new(final_img.size)
            self.backupimg=Image.new(final_img.size)
            self.highlightimg=load_image(os.path.join(GAME_PATH,'system','sel_highlight.png'))
            self.highlightimg_mask=load_image(os.path.join(GAME_PATH,'system','sel_highlight_mask.png'), is_mask=True)
        if hint!=u'HINT_NONE' and hint!=u'HINT_NULL':
            self.hintimg=[]
            if gameconfig[u'platform']==u'pygame':
                for i in range(0,4):
                    self.hintimg.append(load_image(os.path.join(GAME_PATH,'system',hint+str(i)+u'.png'), is_alpha=True))
            else:
                self.hintimg_mask=[]
                for i in range(0,4):
                    self.hintimg.append(load_image(os.path.join(GAME_PATH,'system',hint+str(i)+u'.png')))
                    self.hintimg_mask.append(load_image(os.path.join(GAME_PATH,'system',hint+str(i)+u'_mask.png'), is_mask=True))
            self.hint_origin=hint_origin
            self.hintsequence=0
            for i in range(0,len(self.textlist)):
                if self.textlist[i][0]=='\xe2\x97\x8B'.decode('utf8'):
                    self.hintbool.append(True)
                else:
                    self.hintbool.append(False)
                self.textlist[i]=self.textlist[i][1:]

    def display(self):
        global final_img, textfont, gameconfig, globalsave
        final_img.blit(self.oldimg,(0,0))
        for i in range(0,len(self.textlist)):
            measure_result=measure_text(self.textlist[i])
            text_origin=((self.topleft[0]+self.bottomright[0]-measure_result[1])/2,(self.bottomright[1]+self.topleft[1]-len(self.textlist)*(gameconfig[u'fontsize']+3))/2+i*(gameconfig[u'fontsize']+3))
            if self.highlightpos==i:
                img_origin=((self.topleft[0]+self.bottomright[0]-get_image_width(self.highlightimg))/2,text_origin[1]+(gameconfig[u'fontsize']-get_image_height(self.highlightimg))/2)
                if gameconfig[u'platform']==u'pygame':
                    draw_image(self.highlightimg, img_origin=img_origin,on_canvas=False)
                else:
                    draw_image(self.highlightimg,img_mask=self.highlightimg_mask, img_origin=img_origin,on_canvas=False)
            if (self.generate_sel_code(i) in globalsave[u'selected']) and gameconfig[u'grayselected'] and self.menuenable:
                textcolor=(184,181,167)
            else:
                textcolor=self.textcolor
            draw_text(self.textlist[i],color=textcolor,text_origin=text_origin,on_canvas=False)
        self.backupimg.blit(final_img,(0,0))
        update_screen()
        self.clock=0.01

    def display_hint(self):
        global final_img, gameconfig
        if gameconfig[u'hint'] and self.hint!=u'HINT_NONE' and self.hint!=u'HINT_NULL' and self.highlightpos in range(0,len(self.textlist)) and time.clock() > self.clock+0.5:
            self.clock=time.clock()
            final_img.blit(self.backupimg,(0,0))
            if self.hintbool[self.highlightpos] and self.hintsequence>1:#circle
                self.hintsequence=0
            elif not self.hintbool[self.highlightpos] and self.hintsequence<2:#cross
                self.hintsequence=2
            if gameconfig[u'platform']==u'pygame':
                draw_image(self.hintimg[self.hintsequence],img_origin=self.hint_origin,on_canvas=False)
            else:
                draw_image(self.hintimg[self.hintsequence],img_mask=self.hintimg_mask[self.hintsequence], img_origin=self.hint_origin,on_canvas=False)
            update_screen()
            if self.hintsequence==0:
                self.hintsequence=1
            elif self.hintsequence==1:
                self.hintsequence=0
            elif self.hintsequence==2:
                self.hintsequence=3
            else:
                self.hintsequence=2

    def select(self):
        global keyboard, running, globalsave
        keyboard.clear_downs()
        self.oldimg.blit(final_img,(0,0))
        self.display()
        unbind_quit()
        pen_down=False
        while running:            
            if keyboard.pressed(key_codes.EScancodeSelect) and self.highlightpos in range(0,len(self.textlist)):
                break;
            if keyboard.pressed(key_codes.EScancodeDownArrow):
                #if the highlight entry is at the bottom of the screen
                if self.highlightpos>=len(self.textlist)-1:
                    self.highlightpos=0
                else:
                    self.highlightpos+=1
                self.display()
            if keyboard.pressed(key_codes.EScancodeUpArrow):
                #if the highlight entry is at the top of the screen
                if self.highlightpos<=0:
                    self.highlightpos=len(self.textlist)-1
                else:
                    self.highlightpos-=1
                self.display()
            if keyboard.pen_down():
                pen_down=True
            if pen_down:
                pos=keyboard.get_last_pos()
                on_button=False
                for i in range(0,len(self.dstarealist)):
                    keyrect=self.dstarealist[i]
                    if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                        on_button=True
                        if self.highlightpos!=i:
                            self.highlightpos=i
                            self.display()
                        break
                if not on_button:
                    self.highlightpos=-1
                    self.display()
            if keyboard.pen_up():
                pen_down=False
                pos=keyboard.get_last_pos()
                keyrect=self.dstarealist[self.highlightpos]
                if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                    break
            if self.menuenable:
                if keyboard.pressed(key_codes.EScancode0):
                    self.menu()
                    self.display()
            else:
                if keyboard.pressed(key_codes.EScancodeRightSoftkey):
                    self.highlightpos=len(self.textlist)-1
                    self.display()
                    break;
            self.display_hint()
            e32.ao_sleep(0.01)
            e32.ao_yield()
        bind_quit()
        ret=self.generate_sel_code(self.highlightpos)
        if self.menuenable and (ret not in globalsave[u'selected']):
            globalsave[u'selected'].append(ret)
        keyboard.clear_downs()
        return self.resultmap[self.highlightpos]

    def menu(self):
        global keyboard, screensize, GAME_PATH, save, staticimg, stringres
        img_size=get_image_size(staticimg['menuimg'])
        img_origin=((screensize[0]-img_size[0])/2,40)
        select_text=SelectText([stringres[u'MENU_SAVE'],stringres[u'CANCEL']],
                               topleft=img_origin,
                               bottomright=(img_origin[0]+img_size[0],img_origin[1]+img_size[1]),
                               init_highlight=0)
        draw_image(staticimg['menuimg'],img_origin=img_origin, on_canvas=False)
        ret=select_text.select()
        if ret==0:
            templinenum=save[u'linenum']
            save[u'linenum']-=len(self.textlist)+1
            Save()
            save[u'linenum']=templinenum
        del select_text
        keyboard.clear_downs()

    def generate_sel_code(self,pos):
        global save, f
        ret=os.path.basename(f.name)[:-3]+str(save[u'linenum']-len(self.textlist)+pos)
        return ret


class SelectList(object):
    def __init__(self,textlist,iconlist=None,iconmask=None):
        global screensize
        self.textlist=textlist
        self.startpos=0
        self.endpos=min(3,len(self.textlist)-1)
        self.highlightpos=0
        self.iconlist=iconlist
        self.dstarealist=[]
        for i in range(0, 4):
            self.dstarealist.append((
                0,
                i*screensize[1]/4,
                screensize[0],
                (i+1)*screensize[1]/4
                ))
        if gameconfig[u'platform']==u'pygame':
            self.highlightimg=pygame.Surface((screensize[0],screensize[1]//4),pygame.SRCALPHA)
            self.highlightimg.fill((255,255,255,56))
            self.blackbg=pygame.Surface(screensize,pygame.SRCALPHA)
            self.blackbg.fill((0,0,0,160))
        else:
            self.iconmask=iconmask
            self.blackbg=Image.new(screensize)
            self.blackbg.clear((0,0,0))
            self.blackbg_mask=Image.new(screensize,'L')
            self.blackbg_mask.clear((160,160,160))
            self.highlightimg=Image.new((screensize[0],screensize[1]//4))
            self.highlightimg.clear((255,255,255))
            self.highlightimg_mask=Image.new((screensize[0],screensize[1]//4),'L')
            self.highlightimg_mask.clear((56,56,56))

    def display(self):
        global final_img, screensize, staticimg
        final_img.blit(staticimg['bg_img'],(0,0))
        if gameconfig[u'platform']==u'pygame':
            draw_image(self.blackbg,img_origin=(0,0),on_canvas=False)
            draw_image(self.highlightimg,img_origin=(0,self.highlightpos*screensize[1]//4),on_canvas=False)
        else:
            draw_image(self.blackbg,img_mask=self.blackbg_mask,img_origin=(0,0),on_canvas=False)
            draw_image(self.highlightimg,img_mask=self.highlightimg_mask,img_origin=(0,self.highlightpos*screensize[1]//4),on_canvas=False)
        for i in range(self.startpos,self.endpos+1):
            if self.iconlist!=None:
                if gameconfig[u'platform']==u'pygame':
                    draw_image(self.iconlist[i],img_origin=(1,screensize[1]/8-get_image_height(self.iconlist[i])/2+(i-self.startpos)*screensize[1]/4),on_canvas=False)
                else:
                    draw_image(self.iconlist[i],img_mask=self.iconmask, img_origin=(1,screensize[1]/8-get_image_height(self.iconlist[i])/2+(i-self.startpos)*screensize[1]/4),on_canvas=False)
                topleft=(get_image_width(self.iconlist[i])+3,2+(i-self.startpos)*screensize[1]/4)
                bottomright=(screensize[0],(i-self.startpos+1)*screensize[1]/4)
            else:
                topleft=(2,2+(i-self.startpos)*screensize[1]/4)
                bottomright=(screensize[0],(i-self.startpos+1)*screensize[1]/4)
            pages=split_paragraph(self.textlist[i],bottomright[0]-topleft[0],bottomright[1]-topleft[1])
            draw_paragraph(pages[0], topleft, bottomright, (255,255,255),on_canvas=False)
        update_screen()
        e32.ao_yield()

    def select(self,highlightpos=None):
        global keyboard
        pen_down=False
        if highlightpos!=None:
            if highlightpos>=3:
                self.startpos=highlightpos-3
                self.endpos=highlightpos
                self.highlightpos=3
            else:
                self.startpos=0
                self.endpos=min(3,len(self.textlist)-1)
                self.highlightpos=highlightpos
        self.display()
        keyboard.clear_downs()
        unbind_quit()
        while True:
            if keyboard.pressed(key_codes.EScancodeRightSoftkey):
                bind_quit()
                return -1
            if keyboard.pressed(key_codes.EScancodeSelect):
                break;
            if keyboard.pressed(key_codes.EScancodeDownArrow):
                #if the highlight entry is at the bottom of the screen
                if self.highlightpos==3:
                    #still has entries below
                    if self.endpos<len(self.textlist)-1:
                        self.startpos+=1
                        self.endpos+=1
                    else:
                        self.startpos=0
                        self.endpos=min(3,len(self.textlist)-1)
                        self.highlightpos=0
                else:
                    if self.highlightpos<len(self.textlist)-1:
                        self.highlightpos+=1
                    else:
                        self.highlightpos=0
                self.display()
            if keyboard.pressed(key_codes.EScancodeUpArrow):
                #if the highlight entry is at the top of the screen
                if self.highlightpos==0:
                    #still has entries above
                    if self.startpos>0:
                        self.startpos-=1
                        self.endpos-=1
                    else:
                        self.startpos=max(0,len(self.textlist)-4)
                        self.endpos=len(self.textlist)-1
                        self.highlightpos=self.endpos-self.startpos
                else:
                    if self.highlightpos>0:
                        self.highlightpos-=1
                self.display()
            if keyboard.pressed(key_codes.EScancodeRightArrow):
                #if still has entries below
                if self.endpos<len(self.textlist)-4:
                    self.startpos+=4
                    self.endpos+=4
                else:
                    self.startpos=max(len(self.textlist)-4,0)
                    self.endpos=len(self.textlist)-1
                    self.highlightpos=self.endpos-self.startpos
                self.display()
            if keyboard.pressed(key_codes.EScancodeLeftArrow):
                #if still has entries above
                if self.startpos>3:
                    self.startpos-=4
                    self.endpos-=4
                else:
                    self.startpos=0
                    self.endpos=min(len(self.textlist)-1,3)
                    self.highlightpos=0
                self.display()
            if keyboard.pen_down():
                pen_down=True
            if pen_down:
                pos=keyboard.get_last_pos()
                for i in range(0,len(self.dstarealist)):
                    keyrect=self.dstarealist[i]
                    if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                        if self.highlightpos!=i and i+self.startpos>=0 and i+self.startpos<len(self.textlist):
                            self.highlightpos=i
                            self.display()
                        break
            if keyboard.pen_up():
                pen_down=False
                pos=keyboard.get_last_pos()
                keyrect=self.dstarealist[self.highlightpos]
                if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                    break
            e32.ao_sleep(0.01)
        bind_quit()
        return self.startpos+self.highlightpos

class SelectImg(object):
    def __init__(self,imagelist,dstoriginlist,varlist=None,init_highlight=0):
        global final_img
        if gameconfig[u'platform']==u'pygame':
            self.oldimg=pygame.Surface(final_img.get_size())
        else:
            self.oldimg=Image.new(final_img.size)
        self.imagelist=imagelist
        self.varlist=varlist
        self.highlightpos=init_highlight
        self.seqlen=len(dstoriginlist)
        self.dstoriginlist=[]
        self.dstarealist=[]
        self.source_range=[]
        self.source_range_selected=[]
        havetrue=False
        if init_highlight==-1:
            self.menuenable=True
        else:
            self.menuenable=False
        for i in range(0, self.seqlen):
            self.dstoriginlist.append((dstoriginlist[i][0]-get_image_width(self.imagelist[2*i])/2,dstoriginlist[i][1]-get_image_height(self.imagelist[2*i])/2))
            self.dstarealist.append((dstoriginlist[i][0]-get_image_width(self.imagelist[2*i])/2,
                                     dstoriginlist[i][1]-get_image_height(self.imagelist[2*i])/2,
                                     dstoriginlist[i][0]+get_image_width(self.imagelist[2*i])/2,
                                     dstoriginlist[i][1]+get_image_height(self.imagelist[2*i])/2))
            havetrue=havetrue or varlist[i]
        if not havetrue:
            for i in range(0, self.seqlen):
                self.varlist[i]=True

    def display(self):
        global final_img
        if gameconfig[u'platform']==u'pygame':
            final_img.blit(self.oldimg,(0,0))
            for i in range(0,self.seqlen):
                if self.varlist[i]:
                    if self.highlightpos==i:
                        final_img.blit(self.imagelist[2*i+1],self.dstoriginlist[i])
                    else:
                        final_img.blit(self.imagelist[2*i],self.dstoriginlist[i])
        else:
            final_img.blit(self.oldimg)
            for i in range(0,self.seqlen):
                if self.varlist[i]:
                    if self.highlightpos==i:
                        final_img.blit(self.imagelist[4*i+2], target=self.dstoriginlist[i], mask=self.imagelist[4*i+3], scale=0)
                    else:
                        final_img.blit(self.imagelist[4*i], target=self.dstoriginlist[i], mask=self.imagelist[4*i+1], scale=0)
        update_screen()

    def select(self):
        global keyboard, running
        keyboard.clear_downs()
        self.oldimg.blit(final_img,(0,0))
        self.display()
        unbind_quit()
        pen_down=False
        while running:
            if keyboard.pressed(key_codes.EScancodeSelect) and self.highlightpos in range(0,self.seqlen):
                break;
            if keyboard.pressed(key_codes.EScancodeDownArrow):
                self.next_select(1)
                while (not self.varlist[self.highlightpos]):
                    self.next_select(1)
                self.display()
            if keyboard.pressed(key_codes.EScancodeUpArrow):
                self.next_select(-1)
                while (not self.varlist[self.highlightpos]):
                    self.next_select(-1)
                self.display()
            if keyboard.pen_down():
                pen_down=True
            if pen_down:
                pos=keyboard.get_last_pos()
                on_button=False
                for i in range(0,len(self.dstarealist)):
                    keyrect=self.dstarealist[i]
                    if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                        on_button=True
                        if self.highlightpos!=i and self.varlist[i]:
                            self.highlightpos=i
                            self.display()
                if not on_button:
                    self.highlightpos=-1
                    self.display()
            if keyboard.pen_up():
                pen_down=False
                pos=keyboard.get_last_pos()
                keyrect=self.dstarealist[self.highlightpos]
                if pos[0]>keyrect[0] and pos[0]<keyrect[2] and pos[1]>keyrect[1] and pos[1]<keyrect[3]:
                    break
            if self.menuenable:
                if keyboard.pressed(key_codes.EScancode0):
                    self.menu()
                    self.display()
            else:
                if keyboard.pressed(key_codes.EScancodeRightSoftkey):
                    self.highlightpos=self.seqlen-1
                    while (not self.varlist[self.highlightpos]):
                        self.next_select(-1)
                    self.display()
                    break;
            e32.ao_sleep(0.01)
            e32.ao_yield()
        bind_quit()
        return self.highlightpos
    def next_select(self, inc):
        self.highlightpos+=inc
        #if the highlight entry is at the bottom of the screen
        if self.highlightpos>=self.seqlen:
            self.highlightpos=0
        #if the highlight entry is at the top of the screen
        if self.highlightpos<0:
            self.highlightpos=self.seqlen-1

    def menu(self):
        global keyboard, screensize, GAME_PATH, save, staticimg, stringres
        img_size=get_image_size(staticimg['menuimg'])
        img_origin=((screensize[0]-img_size[0])/2,40)
        select_text=SelectText([stringres[u'MENU_SAVE'],stringres[u'CANCEL']],
                               topleft=img_origin,
                               bottomright=(img_origin[0]+img_size[0],img_origin[1]+img_size[1]),
                               init_highlight=0)
        draw_image(staticimg['menuimg'],img_origin=img_origin, on_canvas=False)
        ret=select_text.select()
        if ret==0:
            templinenum=save[u'linenum']
            save[u'linenum']-=1
            Save()
            save[u'linenum']=templinenum
        del select_text
        keyboard.clear_downs()


class Album(object):
    def __init__(self,album_filename=u'album_list',album_bgname=u'albumbg'):
        global screensize,GAME_PATH,globalsave
        self.album=[]
        self.pagenum=0
        self.imgnum=0
        self.imgindex=0
        self.album_bgname=album_bgname
        self.cvThumb=load_image(os.path.join(GAME_PATH,'system','cvthumb.png'),width=screensize[0]*17/100, height=screensize[1]*17/100)
        configfile=file(os.path.join(GAME_PATH,'script',album_filename+'.txt'),'r')
        while True:
            line=configfile.readline()
            if len(line)==0:
                break
            if len(line)>3 and line[:3] == codecs.BOM_UTF8:
                command=line[3:].decode('utf8')
            else:
                command=line.decode('utf8')
            args=del_blank(command[:-1]).split(',')
            if args[0].isdigit():
                if len(self.album)<=int(args[0])-1:
                    self.album.append([])
                imgnum=int(args[1])
                imgentry={'title':args[2],'filename':[],'show':False}
                for i in range(3,3+imgnum):
                    args[i]=args[i].upper()
                    imgentry['filename'].append(args[i])
                    if args[i] in globalsave[u'evflag']:
                        imgentry['show']=True
                if len(args)>3+imgnum:
                    if args[3+imgnum]==u'1':
                        imgentry['show']=True
                self.album[int(args[0])-1].append(imgentry)
        configfile.close()
        self.get_albumbg(self.pagenum)

    def get_albumbg(self,pagenum):
        global globalsave,screensize, GAME_PATH
        if not os.path.exists(os.path.join(GAME_PATH,'system',self.album_bgname+'.png')):
            self.albumbg=load_image(os.path.join(GAME_PATH,'system',self.album_bgname+'_'+str(pagenum)+'.png'),screensize[0],screensize[1])
            for i in range( 0,len(self.album[pagenum]) ):
                if not self.album[pagenum][i]['show']:
                    line=i//5
                    col=i%5
                    if gameconfig[u'platform']==u'pygame':
                        self.albumbg.blit( self.cvThumb, (screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100))
                    else:
                        self.albumbg.blit( self.cvThumb, target=(screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100))
        else:
            #generate_albumbg
            self.albumbg=load_image(os.path.join(GAME_PATH,'system',self.album_bgname+'.png'),screensize[0],screensize[1])
            for i in range( 0,len(self.album[pagenum]) ):
                line=i//5
                col=i%5
                self.cvThumb=load_image(os.path.join(GAME_PATH,'bg',self.album[pagenum][i]['filename'][0]+gameconfig[u'bgformat']), width=screensize[0]*17/100, height=screensize[1]*17/100)
                if gameconfig[u'platform']==u'pygame':
                    self.albumbg.blit( self.cvThumb, (screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100))
                else:
                    self.albumbg.blit( self.cvThumb, target=(screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100))
            save_image(self.albumbg, os.path.join(GAME_PATH,'system',self.album_bgname+'_'+str(pagenum)+'.png'))

    def display_page(self):
        global final_img, screensize
        draw_image(self.albumbg,on_canvas=False)
        line=self.imgnum//5
        col=self.imgnum%5
        #each image is 17% screensize, left and right adjacent is 2% screenwidth, bottom and up adjacent is 2% screenwidth
        #start from 3% screensize
        if gameconfig[u'platform']==u'pygame':
            pygame.draw.rect(final_img, (0,255,0), ((screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100),
                                  (screensize[0]*17/100,screensize[1]*17/100)), 2)
        else:
            final_img.rectangle(( (screensize[0]*(3+19*col)/100,screensize[1]*(2+19*line)/100),
                                  (screensize[0]*(3+19*col+17)/100,screensize[1]*(2+19*line+17)/100)),
                                outline=(0,255,0),fill=None,width=2)
        measure_result=measure_text(self.album[self.pagenum][self.imgnum]['title'])
        text_origin=((screensize[0]-measure_result[1])/2,int(screensize[1]-gameconfig[u'fontsize']*1.5))
        draw_text(self.album[self.pagenum][self.imgnum]['title'],color=(255,255,255),text_origin=text_origin,on_canvas=False)
        update_screen()
        e32.ao_yield()
    def display_image(self,bgfilename,transition=u'BG_FADE', speed=u'BG_NORMAL'):
        global staticimg,screensize
        BGLoad(0,bgfilename)
        imgsize=get_image_size(staticimg['bg'])
        if imgsize[0]>gameconfig[u'imagesize'][0] or imgsize[1]>gameconfig[u'imagesize'][1]:
            SCROLL(3000, bgfilename, (0,0), 
                ( (imgsize[0]-screensize[0])*100/imgsize[0],(imgsize[1]-screensize[1])*100/imgsize[1] ))
        else:
            BGDisp(0,transition,speed)
    def pos_to_imgnum(self,pos,max_num):
        global screensize
        if pos[0]>screensize[0] or pos[1]>screensize[1]:
            return -1
        line=(pos[1]-screensize[1]*2/100)/(screensize[1]*19/100)
        col=(pos[0]-screensize[0]*3/100)/(screensize[0]*19/100)
        imgnum=line*5+col
        if imgnum>=0 and imgnum<=max_num:
            return imgnum
        else:
            return -1
    def select(self):
        global keyboard,final_img
        state=0
        pen_down=False
        unbind_quit()
        keyboard.clear_downs()
        self.display_page()
        while True:
            #select image interface
            if state==0:
                if keyboard.pressed(key_codes.EScancodeRightSoftkey):
                    break
                if keyboard.pressed(key_codes.EScancodeSelect):
                    if self.album[self.pagenum][self.imgnum]['show']:
                        self.imgindex=0
                        self.display_image(self.album[self.pagenum][self.imgnum]['filename'][self.imgindex],u'BG_NOFADE',u'BG_VERYFAST')
                        state=1
                if keyboard.pressed(key_codes.EScancodeDownArrow):
                    #if the highlight entry is at the bottom
                    if self.imgnum==len(self.album[self.pagenum])-1:
                        self.imgnum=0
                    else:
                        self.imgnum+=1
                    self.display_page()
                if keyboard.pressed(key_codes.EScancodeUpArrow):
                    #if the highlight entry is at the top
                    if self.imgnum==0:
                        self.imgnum=len(self.album[self.pagenum])-1
                    else:
                        self.imgnum-=1
                    self.display_page()
                if keyboard.pressed(key_codes.EScancodeRightArrow):
                    #increase pagenum
                    if self.pagenum==len(self.album)-1:
                        self.pagenum=0
                    else:
                        self.pagenum+=1
                    self.imgnum=0
                    self.get_albumbg(self.pagenum)
                    self.display_page()
                if keyboard.pressed(key_codes.EScancodeLeftArrow):
                    #decrease pagenum
                    if self.pagenum==0:
                        self.pagenum=len(self.album)-1
                    else:
                        self.pagenum-=1
                    self.imgnum=0
                    self.get_albumbg(self.pagenum)
                    self.display_page()
                if keyboard.pen_down():
                    pen_down=True
                if pen_down:
                    imgnum=self.pos_to_imgnum(keyboard.get_last_pos(),len(self.album[self.pagenum])-1)
                    if imgnum!=-1 and self.imgnum!=imgnum:
                        self.imgnum=imgnum
                        self.display_page()
                if keyboard.pen_up():
                    pen_down=False
                    imgnum=self.pos_to_imgnum(keyboard.get_last_pos(),len(self.album[self.pagenum])-1)
                    if imgnum!=-1 and self.album[self.pagenum][self.imgnum]['show']:
                        self.imgindex=0
                        self.display_image(self.album[self.pagenum][self.imgnum]['filename'][self.imgindex],u'BG_NOFADE',u'BG_VERYFAST')
                        state=1
            #watch image interface
            if state==1:
                if keyboard.pen_down():
                    pen_down=True
                if keyboard.pressed(key_codes.EScancodeSelect) or keyboard.pen_up():
                    pen_down=False
                    self.imgindex+=1
                    if self.imgindex>=len(self.album[self.pagenum][self.imgnum]['filename']):
                        self.imgindex=0
                        state=0
                        self.display_page()
                    else:
                        self.display_image(self.album[self.pagenum][self.imgnum]['filename'][self.imgindex])
                if keyboard.pressed(key_codes.EScancodeRightSoftkey):
                    self.imgindex=0
                    state=0
                    self.display_page()
            e32.ao_sleep(0.01)
        bind_quit()
        if os.path.exists(os.path.join(GAME_PATH,'system',self.album_bgname+'.png')):
            os.remove(os.path.join(GAME_PATH,'system',self.album_bgname+'.png'))
        return 

def BGDisp(bgindex, transition=u'BG_NOFADE', speed=u'BG_NORMAL'):
    #BG_NOFADE BG_FADE BG_ALPHA BG_BLIND_IN BG_BLIND_R
    #BG_VERYFAST BG_NORMAL BG_SLOW
    global staticimg,final_img, bgorigin, chara_on, in_fade_out, gameconfig, save
    if speed.isdigit():
        length=int(speed)
    elif speed==u'BG_VERYFAST':
        length=10
    elif speed==u'BG_SLOW':
        length=500
    else: #speed==u'BG_NORMAL'
        length=250
    if transition==u'BG_NOFADE' or in_fade_out:
        #print save[u'bg'], 'in fade out:',in_fade_out
        draw_image(staticimg['bg'],img_origin=bgorigin,on_canvas=not in_fade_out)
    elif transition==u'BG_ALPHA':
        ALPHA(length, staticimg['bg'], bgorigin)
    elif transition==u'BG_FADE':
        FADE(length)
        draw_image(staticimg['bg'],img_origin=bgorigin,on_canvas=not in_fade_out)
        FADE(length,is_fade_out=False)
    else:
        mask_path=os.path.join(GAME_PATH,'system',transition+u'.png')
        if os.path.exists(mask_path):
            if gameconfig[u'platform']==u'pygame':
                mask_img=load_image(mask_path)
            else:
                mask_img=load_image(mask_path, is_mask=True)
            MASK(length, staticimg['bg'], mask_img, bgorigin)
        else:
            ALPHA(length, staticimg['bg'], bgorigin)
    staticimg['bg_img'].blit(final_img,(0,0))
    chara_on=False

def ALPHA(length, new_img, img_origin=(0,0)):
    global final_img, keyboard, in_fade_out, gameconfig
    if keyboard.is_down(key_codes.EScancode1) or length<20 or in_fade_out:
        draw_image(new_img,img_origin=img_origin, on_canvas=not in_fade_out)
        e32.ao_yield()
        return
    length=float(length)/1000.0
    if gameconfig[u'platform']=='pygame':
        fade_mask=pygame.Surface(new_img.get_size())
        fade_mask.blit(new_img,(0,0))
        oldimg=pygame.Surface(final_img.get_size())
        oldimg.blit(final_img,(0,0))
    else:
        fade_mask=Image.new(final_img.size,'L')
        oldimg=Image.new(final_img.size)
        oldimg.blit(final_img)
    start_time=time.clock()
    current_time=start_time
    i=0
    while (current_time-start_time)<length:
        level=int(255*(current_time-start_time)/length)
        if gameconfig[u'platform']==u'pygame':
            fade_mask.set_alpha(level)
            final_img.blit(oldimg,(0,0))
            draw_image(fade_mask,img_origin=img_origin)
        else:
            fade_mask.clear((level,level,level))
            final_img.blit(oldimg)
            draw_image(new_img,img_mask=fade_mask,img_origin=img_origin)            
        i+=1
        current_time=time.clock()
    draw_image(new_img,img_origin=img_origin)
    e32.ao_yield()
#    print 'fps:',i/length

def FADE(length, color=None, is_fade_out=True):
    #length is the duration of fade process in ms, color is u'FADE_BLACK' or u'FADE_WHITE'
    global final_img, in_fade_out, gameconfig, fade_out_color, keyboard ,staticimg
    #allow_redraw=False 
    if keyboard.is_down(key_codes.EScancode1) or length<10:
        length=10
    elif length>10000:
        length=10000
    if color==None:
        if is_fade_out:
            color=(0,0,0)
        else:
            color=fade_out_color
    if gameconfig[u'platform']==u'pygame':
        staticimg['tempimg'].fill(color)
    else:
        staticimg['tempimg'].clear(color)
    staticimg['oldimg'].blit(final_img,(0,0))
    if is_fade_out:
        fade_out_color=color
        ALPHA(length, staticimg['tempimg'])
        in_fade_out=True
    else:
        in_fade_out=False
        draw_image(staticimg['tempimg'],on_canvas=False)
        ALPHA(length, staticimg['oldimg'])
        #allow_redraw=True

def Flush(colorstr,speed=0):
    global final_img, gameconfig, in_fade_out, staticimg
    if in_fade_out:
        return
    if colorstr==u'RED':
        color=(255,0,0)
    elif colorstr==u'WHITE':
        color=(255,255,255)
    elif colorstr==u'BLUE':
        color=(0,0,255)
    else:
        color=hexstr2color(colorstr)
    staticimg['tempimg'].blit(final_img,(0,0))
    if gameconfig[u'platform']==u'pygame':
        final_img.fill(color)
    else:
        final_img.clear(color)
    update_screen()
    if speed:
        e32.ao_sleep(float(speed)/1000.0)
    draw_image(staticimg['tempimg'])

def SCROLL(length, bgfilename, startpos, endpos):
    #startpos and endpos are percent of the bg size
    global final_img, staticimg, keyboard, gameconfig, save, chara, screensize, chara_on
    if chara_on and save[u'bg']==bgfilename:
        need_draw_chara=True
    else:
        CHASetInvisible(u'a')
        chara_on=False
        need_draw_chara=False
    BGLoad(0,bgfilename)
    if keyboard.is_down(key_codes.EScancode1):
        length=0.01
    else:
        length=float(length)/1000.0
    save[u'bgpercentorig']=endpos
    startpos=(startpos[0]*get_image_width(staticimg['bg'])/100,startpos[1]*get_image_height(staticimg['bg'])/100)
    endpos=(endpos[0]*get_image_width(staticimg['bg'])/100,endpos[1]*get_image_height(staticimg['bg'])/100)
    #draw charas on bg if any
    if need_draw_chara:
        if gameconfig[u'platform']==u'pygame':
            bgwithchara=pygame.Surface(staticimg['bg'].get_size())
            bgwithchara.blit(staticimg['bg'],(0,0))
        else:
            bgwithchara=Image.new(staticimg['bg'].size)
            bgwithchara.blit(staticimg['bg'],target=(0,0))
        chaindexseq=[]
        for chaindex in save[u'chara']:
            if not save[u'chara'][chaindex].has_key('layer'):
                save[u'chara'][chaindex]['layer']=1
            chaindexseq.append((chaindex,save[u'chara'][chaindex]['layer']))
        chaindexseq.sort(key=lambda x:x[1])
        for chaindexentry in chaindexseq:
            chaindex=chaindexentry[0]
            if save[u'chara'][chaindex]['chara_visible']:
                img_origin=(startpos[0]+chara[chaindex]['chara_origin'][0],startpos[1]+chara[chaindex]['chara_origin'][1])
                if gameconfig[u'platform']==u'pygame':
                    bgwithchara.blit(chara[chaindex]['chara_img'], img_origin)
                else:
                    bgwithchara.blit(chara[chaindex]['chara_img'],target=img_origin,mask=chara[chaindex]['chara_mask'])
            chara[chaindex]['chara_origin']=(startpos[0]-endpos[0]+chara[chaindex]['chara_origin'][0],startpos[1]-endpos[1]+chara[chaindex]['chara_origin'][1])
            save[u'chara'][chaindex]['chara_center']+=startpos[0]-endpos[0]
            save[u'chara'][chaindex]['chara_y']+=startpos[1]-endpos[1]
    else:
         bgwithchara=staticimg['bg']
    img_origin=startpos
    start_time=time.clock()
    current_time=start_time
    while (current_time-start_time)<length:
        xpos=(endpos[0]-startpos[0])*(current_time-start_time)/length
        ypos=(endpos[1]-startpos[1])*(current_time-start_time)/length
        img_origin=(-startpos[0]-xpos,-startpos[1]-ypos)
        draw_image(bgwithchara,img_origin=img_origin)
        current_time=time.clock()
    draw_image(bgwithchara,img_origin=(-endpos[0],-endpos[1]))
    if gameconfig[u'platform']==u'pygame':
        if need_draw_chara:
            staticimg['chara_img'].blit(bgwithchara,(0,0),(endpos,screensize))
        staticimg['bg_img'].blit(staticimg['bg'],(0,0),(endpos,screensize))
    else:
        if need_draw_chara:
            staticimg['chara_img'].blit(bgwithchara,source=(endpos,(endpos[0]+screensize[0],endpos[1]+screensize[1])))
        staticimg['bg_img'].blit(staticimg['bg'],source=(endpos,(endpos[0]+screensize[0],endpos[1]+screensize[1])))
    e32.ao_yield()

def QUAKE():
    global final_img, in_fade_out, gameconfig, keyboard
    if in_fade_out or keyboard.is_down(key_codes.EScancode1):
        return
    if gameconfig[u'platform']==u'pygame':
        staticimg['tempimg'].fill((0,0,0))
    else:
        staticimg['tempimg'].clear((0,0,0))
    staticimg['oldimg'].blit(final_img,(0,0))
    delay=0.06
    img_origins=[(-1,-2),(4,3),(6,-4),(5,3),(2,-1),(0,0)]
    for img_origin in img_origins:
        start_time=time.clock()        
        draw_image(staticimg['tempimg'],on_canvas=False)
        draw_image(staticimg['oldimg'],img_origin=img_origin)
        end_time=time.clock()
        if end_time-start_time < delay:
            e32.ao_sleep(delay-end_time+start_time)


def ShowCalender(bgfilename,text_origin,color=(64,128,177)):
    global final_img,  in_fade_out, screensize, bgsize, gameconfig, staticimg, bgorigin
    text_origin=pos_bg2screen((text_origin[0]*bgsize[0]/100,text_origin[1]*bgsize[1]/100))
    staticimg['oldimg'].blit(final_img,(0,0))
    staticimg['bg']=load_image(os.path.join(GAME_PATH,u'system',bgfilename+u'.png'))
    bgorigin=((screensize[0]-bgsize[0])/2, (screensize[1]-bgsize[1])/2)
    draw_image(staticimg['bg'], img_origin=bgorigin, on_canvas=False)
    game_date=get_game_date()
    
    if game_date!=(0,0):
        datestring=(str(game_date[0])+'\xE6\x9C\x88'+str(game_date[1])+'\xE6\x97\xA5').decode('utf8')
        tempfontsize=gameconfig[u'fontsize']
        gameconfig[u'fontsize']=int(tempfontsize*1.5)
        set_font()
        draw_text(datestring,text_origin=text_origin,color=color,on_canvas=False)
        gameconfig[u'fontsize']=tempfontsize
        set_font()
    staticimg['tempimg'].blit(final_img,(0,0))
    if not in_fade_out:
        final_img.blit(staticimg['oldimg'],(0,0))
        ALPHA(1000, staticimg['tempimg'])
        waitkey()

def ShowTitle():
    global save, final_img, in_fade_out, gameconfig, textfont
    draw_chara()
    measure_result=measure_text(save[u'title'])
    if gameconfig[u'platform']==u'pygame':
        staticimg['oldimg'].blit(final_img,(0,0))
    else:
        titlebg=load_image(GAME_PATH+u'system\\sel_highlight.png', width=4*gameconfig[u'fontsize']+measure_result[1],height=3*gameconfig[u'fontsize'])
        titlebg_mask=load_image(GAME_PATH+u'system\\sel_highlight_mask.png', width=4*gameconfig[u'fontsize']+measure_result[1],height=3*gameconfig[u'fontsize'] , is_mask=True)
        staticimg['oldimg'].blit(final_img,(0,0))
        draw_image(titlebg,img_mask=titlebg_mask,img_origin=(0,0), on_canvas=False)
    draw_text(save[u'title'],text_origin=(2*gameconfig[u'fontsize'],gameconfig[u'fontsize']), on_canvas=False)
    if in_fade_out:
        pass
    else:
        staticimg['tempimg'].blit(final_img,(0,0))
        final_img.blit(staticimg['oldimg'],(0,0))
        ALPHA(1000, staticimg['tempimg'])
        waitkey()
        ALPHA(1000, staticimg['oldimg'])

def ShowText(string,topleft,bottomright,color,fontsize,show_immediately=True):
    global final_img, chara, screensize, save, gameconfig, in_fade_out, staticimg
    bakfontsize=gameconfig[u'fontsize']
    gameconfig[u'fontsize']=fontsize*screensize[0]/320
    set_font()
    pages=split_paragraph(string,bottomright[0]-topleft[0],bottomright[1]-topleft[1])
    if show_immediately:
        textorigin=draw_paragraph(pages[0], topleft, bottomright, color, on_canvas=not in_fade_out)
    else:
        staticimg['tempimg'].blit(final_img,(0,0))
        textorigin=draw_paragraph(pages[0], topleft, bottomright, color, on_canvas=False)
        final_img.blit(staticimg['tempimg'],(0,0))
        textorigin=draw_onebyone(string, topleft, bottomright, color, None, False)
    #draw on textlayer
    #if textlayer doesn't exist, creat one
    chaindex=u'100'
    if not chara.has_key(chaindex):
        chara[chaindex]={}
        if gameconfig[u'platform']==u'pygame':
            chara[chaindex]['chara_img']=pygame.Surface(screensize,flags=pygame.SRCALPHA)
            chara[chaindex]['chara_img'].fill((255,255,255,0))
        else:
            chara[chaindex]['chara_img']=Image.new(screensize)
            chara[chaindex]['chara_mask']=Image.new(screensize,'L')
            chara[chaindex]['chara_img'].clear(color)
            chara[chaindex]['chara_mask'].clear((0,0,0))
    if not save[u'chara'].has_key(chaindex):
        save[u'chara'][chaindex]={}
        save[u'chara'][chaindex]['filename']=u'textlayer'
    save[u'chara'][chaindex]['chara_center']=screensize[0]/2
    save[u'chara'][chaindex]['chara_y']=0
    chara[chaindex]['chara_origin']=(0,0)
    CHASetVisible(chaindex)
    CHASetLayer(chaindex,100)
    if gameconfig[u'platform']==u'pygame':
        chara[chaindex]['chara_img'].blit(staticimg['paragraph_img'],(0,0))
    else:
        chara[chaindex]['chara_mask'].blit(staticimg['paragraph_img_mask'],mask=staticimg['paragraph_img_mask'])
    #done
    if not show_immediately:
        display_cursor(textorigin,True)
    e32.ao_yield()
    gameconfig[u'fontsize']=bakfontsize
    set_font()
    
def OffText():
    chaindex=u'100'
    if chara.has_key(chaindex):
        del chara[chaindex]
    if save[u'chara'].has_key(chaindex):
        del save[u'chara'][chaindex]

def message_before(name=None):
    global screensize, staticimg, gameconfig, save, textfont
    #prepare the underlying img
    draw_chara()
    if gameconfig[u'platform']==u'pygame':
        draw_image(staticimg['messagebox'],img_origin=(0,screensize[1]-get_image_height(staticimg['messagebox'])),on_canvas=False)
    else:
        draw_image(staticimg['messagebox'],img_mask=staticimg['messagebox_mask'],img_origin=(0,screensize[1]-get_image_height(staticimg['messagebox'])),on_canvas=False)
    #draw the name box
    if name==None:
        save[u'name']=u''
    else:
        save[u'name']=name
        measure_result=measure_text(name)
        name_origin=(gameconfig[u'nameboxorig'][0],screensize[1]-get_image_height(staticimg['messagebox'])-gameconfig[u'nameboxorig'][1]-get_image_height(staticimg['message_name']))
        nametext_origin=(name_origin[0]+(get_image_width(staticimg['message_name'])-measure_result[1])/2-1,name_origin[1]+(get_image_height(staticimg['message_name'])-(measure_result[0][3]-measure_result[0][1]))/2)
        if gameconfig[u'platform']==u'pygame':
            draw_image(staticimg['message_name'],img_origin=name_origin,on_canvas=False)
        else:
            draw_image(staticimg['message_name'],img_mask=staticimg['message_name_mask'],img_origin=name_origin,on_canvas=False)
        draw_text(name,nametext_origin,color=gameconfig[u'textcolor'],on_canvas=False)
    update_screen()

def read_game_config(gamefolder):
    global gameconfig,save
    gameconfigfile=file(os.path.join(gamefolder,'gameconfig.txt'),'r')
    while True:
        line=gameconfigfile.readline()
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        if command.startswith('#'):
            continue
        args=command.split(',')
        if args[0]==u'imagesize' or args[0]==u'nameboxorig':
            gameconfig[args[0]]=(int(args[1]),int(args[2]))
        elif args[0]==u'msgtb' or args[0]==u'msglr':
            if len(args)>2:
                gameconfig[args[0]]=(int(args[1]),int(args[2]))
        elif args[0]==u'font' or args[0]==u'fontsize' or args[0]==u'bgmvolume' or args[0]==u'vovolume' or args[0]==u'textspeed' or args[0]==u'prefetching' or args[0]==u'playvideo' or args[0]==u'fontaa' or args[0]==u'grayselected' or args[0]==u'hint':
            gameconfig[args[0]]=int(args[1])
        elif args[0]==u'textcolor':
            gameconfig[args[0]]=hexstr2color(args[1])
        else:
            gameconfig[args[0]]=args[1]
    gameconfigfile.close()

def read_global_config(configfilename):
    gameconfigfile=file(configfilename,'r')
    retdict={}
    while True:
        line=gameconfigfile.readline()
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        args=command.split(',')
        if args[0]==u'last_path':
            retdict[args[0]]=args[1]
        else:
            retdict[args[0]]=int(args[1])
    gameconfigfile.close()
    return retdict

def write_game_config():
    global gameconfig, save
    gameconfigfile=file(os.path.join(GAME_PATH,'gameconfig.txt'),'w')
    gameconfigfile.write(codecs.BOM_UTF8)
    for entry in gameconfig:
        entrytype=type(gameconfig[entry])
        if entrytype==str or entrytype==unicode:
            gameconfigfile.write((entry+','+gameconfig[entry]+'\r\n').encode('utf8'))
        elif entrytype==tuple:
            if entry==u'textcolor':
                gameconfigfile.write((entry+',#'+hex(gameconfig[entry][0]*256*256+gameconfig[entry][1]*256+gameconfig[entry][2])[2:]+'\r\n').encode('utf8'))
            else:
                gameconfigfile.write((entry+','+str(gameconfig[entry][0])+','+str(gameconfig[entry][1])+'\r\n').encode('utf8'))
        elif entrytype==int:
            gameconfigfile.write((entry+','+str(gameconfig[entry])+'\r\n').encode('utf8'))
    gameconfigfile.close()
    save_global()

def CHAload(chaindex, chafilename):
    global chara, screensize, cache, save, gameconfig
    #print "chaindex",chaindex
    chara[chaindex]={}
    if not save[u'chara'].has_key(chaindex):
        save[u'chara'][chaindex]={}
    save[u'chara'][chaindex]['filename']=chafilename
    if not save[u'chara'][chaindex].has_key('chara_center'):
        save[u'chara'][chaindex]['chara_center']=screensize[0]/2
    if cache['chara'].has_key(chafilename):
        chara[chaindex]['chara_img']=cache['chara'][chafilename]['res']
        if gameconfig[u'platform']!=u'pygame':
            chara[chaindex]['chara_mask']=cache['chara'][chafilename]['res_mask']
        cache['chara'][chafilename]['usetime']-=1
        if cache['chara'][chafilename]['usetime']==0:
            del cache['chara'][chafilename]
    else:
        unpack_file(chafilename,u'charaformat')
        if gameconfig[u'platform']==u'pygame':
            chara[chaindex]['chara_img']=load_image(os.path.join(GAME_PATH,u'chara',chafilename+gameconfig[u'charaformat']),is_alpha=True)
        else:
            unpack_file(chafilename+u'_mask',u'charamaskformat')
            chara[chaindex]['chara_img']=load_image(GAME_PATH+u'chara\\'+chafilename+gameconfig[u'charaformat'])
            chara[chaindex]['chara_mask']=load_image(GAME_PATH+u'chara\\'+chafilename+'_mask'+gameconfig[u'charamaskformat'], is_mask=True)
    save[u'chara'][chaindex]['chara_visible']=False

def CHADisp(transition=u'ALPHA',length=300):
    global chara, chara_on, staticimg, final_img, save, in_fade_out
    chara_on=False
    staticimg['oldimg'].blit(final_img,(0,0))
    draw_image(staticimg['bg_img'],on_canvas=False)
    chaindexseq=[]
    #smallest layer number is at the bottom
    for chaindex in save[u'chara']:
        if not save[u'chara'][chaindex].has_key('layer'):
            save[u'chara'][chaindex]['layer']=1
        chaindexseq.append((chaindex,save[u'chara'][chaindex]['layer']))
    chaindexseq.sort(key=lambda x:x[1])
    for chaindexentry in chaindexseq:
        chaindex=chaindexentry[0]
        if save[u'chara'][chaindex]['chara_visible']:
            if gameconfig[u'platform']==u'pygame':
                draw_image(chara[chaindex]['chara_img'],img_origin=chara[chaindex]['chara_origin'],on_canvas=False)
            else:
                draw_image(chara[chaindex]['chara_img'],img_mask=chara[chaindex]['chara_mask'],img_origin=chara[chaindex]['chara_origin'],on_canvas=False)
            chara_on=True
    staticimg['chara_img'].blit(final_img,(0,0))
    if (not in_fade_out):
        if transition=='ALPHA':
            final_img.blit(staticimg['oldimg'],(0,0))
            ALPHA(length, staticimg['chara_img'])
        else:
            update_screen()
    chara_on=True

def hide_msgbox():
    global gameconfig, final_img, keyboard, staticimg
    staticimg['oldimg'].blit(final_img,(0,0))
    draw_chara()
    update_screen()
    keyboard.clear_downs()
    while not (keyboard.pressed(key_codes.EScancodeLeftArrow) or keyboard.pressed(key_codes.EScancodeSelect)) :
        e32.ao_sleep(0.5)
    draw_image(staticimg['oldimg'])
    keyboard.clear_downs()


def Save():
    global final_img, globalsave, gameconfig, staticimg, stringres
    staticimg['oldimg'].blit(final_img,(0,0))
    savelist=read_save_list(1,100)
    selectlist=SelectList(savelist)
    selindex=selectlist.select(globalsave[u'latestsave']-1)
    if selindex!=-1:
        if gameconfig[u'platform']==u'pygame':
            if query(stringres[u'HINT'],stringres[u'SAVE_1']+str(selindex+1)+stringres[u'SAVE_2'],[stringres[u'OK'],stringres[u'CANCEL']])==0:
                globalsave[u'latestsave']=selindex+1
                save_index(selindex+1)
        else:
            if appuifw.query(stringres[u'SAVE_1']+str(selindex+1)+stringres[u'SAVE_2'],'query'):
                globalsave[u'latestsave']=selindex+1
                save_index(selindex+1)
                appuifw.note(stringres[u'SAVE_SUCCESS'],'conf')#save complete
    ALPHA(300, staticimg['oldimg'])

def ScreenShot(mode):
    global GAME_PATH, staticimg, gameconfig
    if not os.path.exists(os.path.join(GAME_PATH,u'save')):
        os.makedirs(os.path.join(GAME_PATH,u'save'))
    #find next available filename
    i=0
    while os.path.exists(os.path.join(GAME_PATH,u'save','screenshot'+str(i)+'.png')):
        i+=1
    shotfilename=os.path.join(GAME_PATH,u'save','screenshot'+str(i)+'.png')
    if mode==0:
        ret=save_image(staticimg['bg'],shotfilename)
    elif mode==1:
        ret=save_image(staticimg['chara_img'],shotfilename)
    elif mode==2:
        ret=save_image(staticimg['tempimg'],shotfilename)
    else:
        return
    if ret:
        if gameconfig[u'platform']==u'pygame':
            query(stringres[u'HINT'],stringres[u'SCREENSHOT_4']+shotfilename,[stringres[u'OK']])
        else:
            appuifw.note(stringres[u'SCREENSHOT_4']+shotfilename,'conf')#save complete

#=========================================================
#                Platform independent code
#=========================================================

class Musicbox(object):
    def __init__(self):
        self.musictitlelist=[]
        self.bgmlist=[]
        configfile=file(os.path.join(GAME_PATH,'script','music_list.txt'),'r')
        while True:
            line=configfile.readline()
            if len(line)==0:
                break
            if len(line)>3 and line[:3] == codecs.BOM_UTF8:
                command=line[3:].decode('utf8')
            else:
                command=line.decode('utf8')
            args=del_blank(command[:-1]).split(',')
            if len(args)==2:
                self.musictitlelist.append(args[1])
                self.bgmlist.append(args[0])
        configfile.close()

    def select(self):
        selectlist=SelectList(self.musictitlelist)
        selindex=0
        while True:
            selindex=selectlist.select(selindex)
            if selindex==-1:
                break
            else:
                BGMPlay(self.bgmlist[selindex],1)
        BGMStop()

def draw_chara():
    global staticimg, chara_on, final_img
    if chara_on:
        final_img.blit(staticimg['chara_img'],(0,0))
    else:
        final_img.blit(staticimg['bg_img'],(0,0))


def message_after(char_list,name=None):
    update_screen()
    save[u'message']=char_list
    AppendMessageLog(name,char_list)
    auto_save()
    e32.ao_yield()
    #set inactivity time to 0 to keep the screen light on
    e32.reset_inactivity()

def message(charlist,name=None):#(char_list,name=None,topleft, bottomright,show_immediately=False):
    global staticimg, gameconfig
    if charlist==u'':
        return
    consttextorigin=(gameconfig[u'msglr'][0],screensize[1]-get_image_height(staticimg['messagebox'])+gameconfig[u'msgtb'][0])
    constbottomright=(screensize[0]-gameconfig[u'msglr'][1],screensize[1]-gameconfig[u'msgtb'][1])
    if (gameconfig.has_key(u'textspeed') and gameconfig[u'textspeed']==5) or keyboard.is_down(key_codes.EScancode1):
        pages=split_paragraph(charlist,constbottomright[0]-consttextorigin[0],constbottomright[1]-consttextorigin[1])
        for lines in pages:
            message_before(name)
            textorigin=draw_paragraph(lines, consttextorigin, constbottomright, gameconfig[u'textcolor'])
            display_cursor(textorigin,True)
    else:
        message_before(name)
        textorigin=draw_onebyone(charlist, consttextorigin, constbottomright, gameconfig[u'textcolor'], name)
        display_cursor(textorigin,True)
    message_after(charlist,name)

def draw_onebyone(charlist, topleft, bottomright, color, name=None, redrawmesagebox=True):
    global running
    delay_time=[0.1,0.07,0.04,0.02,0,0]
    i=0
    line_num=0
    textorigin=topleft
    start_this_page=i
    key_pressed=False
    while running and i<len(charlist):
        if keyboard.pressed(key_codes.EScancodeSelect) or keyboard.pressed(key_codes.EScancode1):
            key_pressed=True
        start_time=time.clock()
        if i<len(charlist)-1:
            if charlist[i:i+2]=='\\n' or charlist[i:i+2]=='\\r':
                update_screen()
                #display cursor
                if charlist[i:i+2]=='\\n' and (not keyboard.is_down(key_codes.EScancode1)):
                    display_cursor(textorigin)
                key_pressed=False
                textorigin=(topleft[0], textorigin[1]+gameconfig[u'fontsize']+1)
                line_num+=1
                i+=2
                continue
        measure_result=measure_text(charlist[i])
        #if a single line exceed the width of rect, change a line
        if bottomright[0]-textorigin[0] < measure_result[1]:
            textorigin=(topleft[0], textorigin[1]+gameconfig[u'fontsize']+1)
            line_num+=1
        #if exceed the height of rect, change a page
        if bottomright[1] < textorigin[1] + gameconfig[u'fontsize']*0.8:
            #display cursor
            if not keyboard.is_down(key_codes.EScancode1):
                display_cursor(textorigin,True)
            if gameconfig.has_key(u'textspeed') and gameconfig[u'textspeed']==5:
                key_pressed=True
            else:
                key_pressed=False
            textorigin=topleft
            line_num=0
            if redrawmesagebox:
                message_before(name)
            else:
                draw_chara()
            start_this_page=i
        draw_text(charlist[i],text_origin=textorigin,color=color,on_canvas=not key_pressed)
        textorigin=(textorigin[0]+measure_result[1],textorigin[1])
        i+=1
        if not key_pressed:
            e32.ao_yield()
            end_time=time.clock()
            if end_time-start_time < delay_time[gameconfig[u'textspeed']]:
                e32.ao_sleep(delay_time[gameconfig[u'textspeed']]-end_time+start_time)
    update_screen()
    if textorigin[0] < bottomright[0]-gameconfig[u'fontsize']:
        textorigin=(textorigin[0]+3,textorigin[1])
    else:
        textorigin=(topleft[0],textorigin[1]+gameconfig[u'fontsize']+1)
    return textorigin

def split_paragraph(paragraph, width, height):
    global gameconfig
    #split by \n and \r
    char_list=[]
    i=0
    start=0
    while i<len(paragraph):
        if i<len(paragraph)-1 and paragraph[i:i+2]=='\\n':
            if i>start:
                char_list.append(paragraph[start:i])
            start=i+2
            i+=2
        elif i<len(paragraph)-1 and paragraph[i:i+2]=='\\r':
            if i>=start:
                char_list.append(paragraph[start:i])
            start=i+2
            i+=2
        else:
            i+=1
    if start<len(paragraph):
        char_list.append(paragraph[start:])
    line_num=0
    maxline=1+(height-gameconfig[u'fontsize']*0.2)//(gameconfig[u'fontsize']+1)
    pages=[]
    lines=[]
    for sentence in char_list:
        char_count=0
        while True:
            measure_result=measure_text(sentence[char_count:], maxwidth=width)
            lines.append(sentence[char_count:char_count+measure_result[2]])
            char_count+=measure_result[2]
            line_num+=1
            if line_num==maxline:
                pages.append(lines)
                lines=[]
                line_num=0
            if len(sentence)==char_count:
                break
    if lines!=[]:
        pages.append(lines)
    return pages

def waitkey():
    global keyboard
    if not keyboard.is_down(key_codes.EScancode1):
        delay=8
        start_time=time.clock()
        keyboard.clear_downs()
        end_time=time.clock()
        while (not keyboard.pressed(key_codes.EScancodeSelect) and (end_time-start_time < delay) ) :
            e32.ao_sleep(1)
            end_time=time.clock()
            
def hexstr2color(string):
    #this convert a hex color code to dec int value
    #eg. #53798F to 5470607
    try:
        rgbint=int(string[1:], 16)
    except:
        rgbint=16777215
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

def intstr2color(string):
    #this convert a hex color code to dec int value
    #eg. #53798F to 5470607
    try:
        rgbint=int(string)
    except:
        rgbint=16777215
    return (rgbint // 256 // 256 % 256, rgbint // 256 % 256, rgbint % 256)

def pos_bg2screen(pos_on_bg):
    return (pos_bg2screen_x(pos_on_bg[0]),pos_bg2screen_y(pos_on_bg[1]))
def pos_bg2screen_x(pos_on_bg_x):
    global screensize,bgsize,gameconfig
    if bgsize[0]==screensize[0]: #fit width, no need to change
        return pos_on_bg_x
    else:
        return pos_on_bg_x+(screensize[0]-bgsize[0])/2
def pos_bg2screen_y(pos_on_bg_y):
    global screensize,bgsize,gameconfig
    if bgsize[1]==screensize[1]: #fit height, no need to change
        return pos_on_bg_y
    else:
        return pos_on_bg_y+(screensize[1]-bgsize[1])/2

def pos_screen2bg(pos_on_screen):
    return (pos_screen2bg_x(pos_on_screen[0]),pos_screen2bg_y(pos_on_screen[1]))
def pos_screen2bg_x(pos_on_screen_x):
    global screensize,bgsize,gameconfig
    if bgsize[0]==screensize[0]: #fit width, no need to change
        return pos_on_screen_x
    else:
        return pos_on_screen_x-(screensize[0]-bgsize[0])/2
def pos_screen2bg_y(pos_on_screen_y):
    global screensize,bgsize,gameconfig
    if bgsize[1]==screensize[1]: #fit height, no need to change
        return pos_on_screen_y
    else:
        return pos_on_screen_y-(screensize[1]-bgsize[1])/2

#set the position of chara. mode 0:upperleft, mode 1:uppermiddle, mode 2:upperright, 
#                                             mode 3:middlemiddle, 
#                           mode 4:lowerleft, mode 5:lowermiddle, mode 6:lowerright
def CHASetPos(chaindex,xpos,ypos=0,mode=5):
    global save,chara,bgsize
    if not save[u'chara'].has_key(chaindex):
        return
    charasize=get_image_size(chara[chaindex]['chara_img'])
    #save[u'chara'][chaindex]['chara_center'] is the x pos of chara center on bg
    #save[u'chara'][chaindex]['chara_y'] is the distance of chara top to the bg top
    if mode==5:
        save[u'chara'][chaindex]['chara_center']=xpos
        save[u'chara'][chaindex]['chara_y']=bgsize[1]-charasize[1]-ypos
    elif mode==0:
        save[u'chara'][chaindex]['chara_center']=xpos+charasize[0]/2
        save[u'chara'][chaindex]['chara_y']=ypos
    elif mode==1:
        save[u'chara'][chaindex]['chara_center']=xpos
        save[u'chara'][chaindex]['chara_y']=ypos
    elif mode==2:
        save[u'chara'][chaindex]['chara_center']=bgsize[0]-xpos-charasize[0]/2
        save[u'chara'][chaindex]['chara_y']=ypos
    elif mode==3:
        save[u'chara'][chaindex]['chara_center']=xpos
        save[u'chara'][chaindex]['chara_y']=ypos-charasize[1]/2
    elif mode==4:
        save[u'chara'][chaindex]['chara_center']=xpos+charasize[0]/2
        save[u'chara'][chaindex]['chara_y']=bgsize[1]-charasize[1]-ypos
    else: #mode==6
        save[u'chara'][chaindex]['chara_center']=bgsize[0]-xpos-charasize[0]/2
        save[u'chara'][chaindex]['chara_y']=bgsize[1]-charasize[1]-ypos
    chara[chaindex]['chara_origin']=pos_bg2screen((save[u'chara'][chaindex]['chara_center']-charasize[0]/2, save[u'chara'][chaindex]['chara_y']))

#get the position of chara. mode 0:upperleft, mode 1:uppermiddle, mode 2:upperright, 
#                                             mode 3:middlemiddle, 
#                           mode 4:lowerleft, mode 5:lowermiddle, mode 6:lowerright
def CHAGetPos(chaindex,mode=5):
    global save,chara,bgsize
    if not save[u'chara'].has_key(chaindex):
        return (0,0)
    charasize=get_image_size(chara[chaindex]['chara_img'])
    if mode==5:
        xpos=save[u'chara'][chaindex]['chara_center']
        ypos=bgsize[1]-charasize[1]-save[u'chara'][chaindex]['chara_y']
    elif mode==0:
        xpos=save[u'chara'][chaindex]['chara_center']-charasize[0]/2
        ypos=save[u'chara'][chaindex]['chara_y']
    elif mode==1:
        xpos=save[u'chara'][chaindex]['chara_center']
        ypos=save[u'chara'][chaindex]['chara_y']
    elif mode==2:
        xpos=bgsize[0]-charasize[0]/2-save[u'chara'][chaindex]['chara_center']
        ypos=save[u'chara'][chaindex]['chara_y']
    elif mode==3:
        xpos=save[u'chara'][chaindex]['chara_center']
        ypos=save[u'chara'][chaindex]['chara_y']+charasize[1]/2
    elif mode==4:
        xpos=save[u'chara'][chaindex]['chara_center']-charasize[0]/2
        ypos=bgsize[1]-charasize[1]-save[u'chara'][chaindex]['chara_y']
    else: #mode==6
        xpos=bgsize[0]-charasize[0]/2-save[u'chara'][chaindex]['chara_center']
        ypos=bgsize[1]-charasize[1]-save[u'chara'][chaindex]['chara_y']
    return (xpos,ypos)
def CHAParsePos(chaindex,pos):
    #first check whether there is an operator
    global save
    xpos=None
    layer=None
    ret1=pos.find(u'+')
    ret2=pos.find(u'-')
    if ret1!=-1:
        operator=u'+'
        num=int(del_blank(pos[ret1+1:]))
        pos=del_blank(pos[:ret1])
    elif ret2!=-1:
        operator=u'-'
        num=int(del_blank(pos[ret2+1:]))
        pos=del_blank(pos[:ret2])
    else:
        operator=None
        num=0
    num=num*screensize[0]/320
    #check whether there is a layer indicator
    ret1=pos.find(u'_O')
    if ret1!=-1:
        layer=0
        pos=del_blank(pos[:ret1])
    else:
        if pos.startswith('CHR_'):
            layer=1
    #determins the charater center
    if pos==u'CHR_LEFT':
        xpos=screensize[0]/4
    elif pos==u'CHR_RIGHT':
        xpos=screensize[0]*3/4
    elif pos==u'CHR_CENTER':
        xpos=screensize[0]/2
    #calculate the final pos
    if operator==u'+':
        xpos+=num
    elif operator==u'-':
        xpos-=num
    if xpos==None:
        xpos=save[u'chara'][chaindex]['chara_center']
    CHASetPos(chaindex,xpos)
    if layer==None:
        if save[u'chara'][chaindex].has_key('layer'):
            layer=save[u'chara'][chaindex]['layer']
        else:
            layer=0
    CHASetLayer(chaindex,layer)

def CHASetVisible(chaindex):
    global save
    if save[u'chara'].has_key(chaindex):
        save[u'chara'][chaindex][u'chara_visible']=True

def CHASetInvisible(chaindex):
    global save,chara
    if chaindex==u'a':
        #for save_element in save[u'chara']:
        #    del save[u'chara'][save_element]['chara_visible']=False
        save[u'chara']={}
        chara={}
    else:
        if save[u'chara'].has_key(chaindex):
            save[u'chara'][chaindex][u'chara_visible']=False

def CHAResetPos(chaindex):
    global save,bgsize
    if chaindex==u'a':
        for save_element in save[u'chara']:
            save[u'chara'][save_element]['chara_center']=bgsize[0]/2
    else:
        if save[u'chara'].has_key(chaindex):
            save[u'chara'][chaindex][u'chara_center']=bgsize[0]/2

def CHAOffsetPos(chaindex,offset):
    global chara, save
    if save[u'chara'].has_key(chaindex) and chara.has_key(chaindex):
        chara[chaindex]['chara_origin']=pos_bg2screen((save[u'chara'][chaindex]['chara_center']-get_image_width(chara[chaindex]['chara_img'])/
2+offset[0], save[u'chara'][chaindex]['chara_y']+offset[1]))

def CHAQuake(chaindex_list,offsets,cycle=100):
    global screensize, keyboard
    if not keyboard.is_down(key_codes.EScancode1):
        delay=float(cycle)/1000.0
        for offset in offsets:
            start_time=time.clock()
            realoffset=(offset[0]*screensize[0]/540,offset[1]*screensize[1]/360)
            for chaindex in chaindex_list:
                CHAOffsetPos(chaindex,realoffset)
            CHADisp(transition=None)
            end_time=time.clock()
            if end_time-start_time < delay:
                e32.ao_sleep(delay-end_time+start_time)

def CHASetLayer(chaindex,layer):
    global save
    if not save[u'chara'].has_key(chaindex):
        save[u'chara'][chaindex]={}
    save[u'chara'][chaindex]['layer']=layer

def ChangeTitle(title_index):
    global save
    configfile=file(os.path.join(GAME_PATH,u'script','title_list.txt'),'r')
    save[u'title']=u''
    while True:
        line=configfile.readline()
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        args=command.split(',')
        if args[0]==title_index:
            save[u'title']=args[1]
            break
    configfile.close()

def auto_save():
    global autosave
    autosave+=1
    if autosave<0 or autosave>30:
        autosave=0
    elif autosave==30:
        save_index(0)

def save_index(save_index):
    global f, save, anime
    if not os.path.exists(os.path.join(GAME_PATH,u'save')):
        os.makedirs(os.path.join(GAME_PATH,u'save'))
    savefile=file(os.path.join(GAME_PATH,u'save',str(save_index)+u'.sav'),'w')
    savefile.write(codecs.BOM_UTF8)
    savefile.write((os.path.basename(f.name)+'\n').encode('utf8'))
    savefile.write((str(save[u'linenum'])+'\n').encode('utf8'))
    game_date=get_game_date()
    if game_date==(0,0):
        savefile.write('?,?\n'.encode('utf8'))
    else:
        savefile.write((str(get_game_date()[0])+','+str(get_game_date()[1])+',\n').encode('utf8'))
    current_time=time.localtime(time.time())
    for var in current_time:
        savefile.write((str(var)+',').encode('utf8'))
    savefile.write('\n'.encode('utf8'))
    if not save.has_key(u'title'):
        save[u'title']=u''
    savefile.write((save[u'title']+'\n').encode('utf8'))
    if save.has_key(u'bgm'):
        savefile.write((save[u'bgm']+'\n').encode('utf8'))
    else:
        savefile.write(('\n').encode('utf8'))
    savefile.write((save[u'bg']+','+str(save[u'bgpercentorig'][0])+','+str(save[u'bgpercentorig'][1])+'\n').encode('utf8'))
    savefile.write('chara_y,'.encode('utf8'))
    for chara_element in save[u'chara']:
        savefile.write((chara_element+','+save[u'chara'][chara_element][u'filename']+','+str(save[u'chara'][chara_element][u'chara_visible'])+','+str(save[u'chara'][chara_element]['chara_center'])+','+str(save[u'chara'][chara_element]['chara_y'])+','+str(save[u'chara'][chara_element][u'layer'])+',').encode('utf8'))
    savefile.write('\n'.encode('utf8'))
    if not save.has_key(u'name'):
        save[u'name']=''
    savefile.write((save[u'name']+'\n').encode('utf8'))
    if not save.has_key(u'message'):
        save[u'message']=''
    savefile.write((save[u'message']+'\n').encode('utf8'))
    for var in save[u'variables']:
        if not var.startswith(u'S'):
            savefile.write((var+','+str(save[u'variables'][var])+',').encode('utf8'))
    savefile.write('\n'.encode('utf8'))
    for var in save[u'callstack']:
        savefile.write((var[0]+','+str(var[1])+',').encode('utf8'))
    savefile.write('\n'.encode('utf8'))
    savefile.write((save[u'msgbox']+','+save[u'namebox']+'\n').encode('utf8'))
    #save anime
    if anime.ison() and anime.isloop():
        savefile.write(('anime,'+anime.getsave()+'\n').encode('utf8'))
    else:
        savefile.write('\n'.encode('utf8'))
    savefile.close()
    save_global()

def load_index(save_index):
    #if load succeeded, return true
    global f, save, gameconfig, anime, GAME_PATH
    if not os.path.exists(os.path.join(GAME_PATH,u'save')):
        os.makedirs(os.path.join(GAME_PATH,u'save'))
    savepath=os.path.join(GAME_PATH,u'save',str(save_index)+u'.sav')
    if not os.path.exists(savepath):
        return False
    if anime.ison():
        anime.off('temp')
    FADE(500)
    savefile=file(savepath,'r')
    line=savefile.readline()
    change_script(del_blank(line[3:].decode('utf8'))[:-4])
    linenum=int(del_blank(savefile.readline().decode('utf8')))
    jump_to_line(linenum)
    #read game date and real date
    command=savefile.readline()
    command=savefile.readline()
    save[u'title']=del_blank(savefile.readline().decode('utf8'))
    #read bgm
    command=del_blank(savefile.readline().decode('utf8'))
    if command!=u'':
        BGMPlay(command)
    else:
        BGMStop()
    #read bg
    command=del_blank(savefile.readline().decode('utf8'))
    args=split_parameter(command,'')
    if len(args)==1:
        BGLoad(0,args[0])
    else:
        BGLoad(0,args[0],(int(args[1]),int(args[2])))
    BGDisp(0,u'BG_NOFADE',u'BG_VERYFAST')
    #read chara
    CHASetInvisible(u'a')
    command=del_blank(savefile.readline().decode('utf8'))
    if not command.startswith(u'chara_y,'):
        #read old save chara format
        args=command.split(',')
        for i in range(0,len(args)/5):
            if not save[u'chara'].has_key(args[5*i]):
                save[u'chara'][args[5*i]]={}
            CHAload(args[5*i],args[5*i+1])
            CHASetPos(args[5*i],int(args[5*i+3]))
            CHASetLayer(args[5*i],int(args[5*i+4]))
            if args[5*i+2]==u'True':
                CHASetVisible(args[5*i])
            else:
                CHASetInvisible(args[5*i])
    else:
        #read new save chara format
        args=command.split(',')[1:]
        for i in range(0,len(args)/6):
            if not save[u'chara'].has_key(args[6*i]):
                save[u'chara'][args[6*i]]={}
            CHAload(args[6*i],args[6*i+1])
            CHASetPos(args[6*i],int(args[6*i+3]),int(args[6*i+4]),1)
            CHASetLayer(args[6*i],int(args[6*i+5]))
            if args[6*i+2]==u'True':
                CHASetVisible(args[6*i])
            else:
                CHASetInvisible(args[6*i])
    CHADisp()
    #read message
    save[u'name']=del_blank(savefile.readline().decode('utf8'))
    if save[u'name']==u'':
        save[u'name']=None
    save[u'message']=del_blank(savefile.readline().decode('utf8'))
    #read variables
    command=del_blank(savefile.readline().decode('utf8'))
    args=command.split(',')
    purge_variable()
    for i in range(0,len(args)/2):
        if not args[2*i].startswith(u'S'):
            save[u'variables'][args[2*i]]=int(args[2*i+1])
    #read callstack
    command=del_blank(savefile.readline().decode('utf8'))
    args=command.split(',')
    save[u'callstack']=[]
    for i in range(0,len(args)/2):
        save[u'callstack'].append((args[2*i],int(args[2*i+1])))
    #read msgbox
    command=savefile.readline().decode('utf8')
    if len(command)==0:
        save[u'msgbox']=u'message'
        save[u'namebox']=u'name'
    else:
        args=del_blank(command).split(',')
        if save[u'msgbox']!=args[0] or save[u'namebox']!=args[1]:
            save[u'msgbox']=args[0]
            save[u'namebox']=args[1]
            change_message_box(save[u'msgbox'],save[u'namebox'])
    #read anime
    command=savefile.readline().decode('utf8')
    if len(command)>1:
        args=del_blank(command).split(',')
        if args[0]==u'anime':
            anime.on(args[1],int(args[2]),int(args[3]),int(args[4]),int(args[5]),True)
    #close file
    savefile.close()
    FADE(500,is_fade_out=False)
    message(save[u'message'],name=save[u'name'])
    #save_global()
    return True

def save_global():
    global f, globalsave, save
    savefile=file(os.path.join(GAME_PATH,'save','global.sav'),'w')
    savefile.write(codecs.BOM_UTF8)
    #write evflag
    for flag in globalsave[u'evflag']:
        if flag!=u'':
            savefile.write((flag.upper()+',').encode('utf8'))
    savefile.write(('\n').encode('utf8'))
    #save globalvar
    for entry in save[u'variables']:
        if entry.startswith(u'S'):
            savefile.write((entry+','+str(save[u'variables'][entry])+',').encode('utf8'))
    savefile.write(('\n').encode('utf8'))
    #save latestsave
    savefile.write((str(globalsave[u'latestsave'])+'\n').encode('utf8'))
    #save selected
    for flag in globalsave[u'selected']:
        if flag!=u'':
            savefile.write((flag+',').encode('utf8'))
    savefile.write(('\n').encode('utf8'))
    #close file
    savefile.close()
    
def load_global():
    #if load succeeded, return true
    global f, globalsave, save
    try:
        globalsave={}
        savefile=file(os.path.join(GAME_PATH,'save','global.sav'),'r')
        line=savefile.readline()
        #read evflag
        globalsave[u'evflag']=line[3:].decode('utf8')[:-2].split(',')
        #read globalvar
        command=savefile.readline().decode('utf8')
        args=command[:-2].split(',')
        for i in range(0,len(args)/2):
            save[u'variables'][args[2*i]]=int(args[2*i+1])
        #read latestsave
        command=savefile.readline().decode('utf8')
        globalsave[u'latestsave']=int(command[:-1])
        #read selected
        command=savefile.readline().decode('utf8')
        globalsave[u'selected']=command[:-2].split(',')
        #close file
        savefile.close()
        return True
    except:
        globalsave={u'evflag':[],u'latestsave':0,u'selected':[]}
        return False

def purge_variable():
    global save
    save_global()
    save[u'variables']={}
    load_global()
    
def read_save_list(startsaveslot, saveslotnum):
    global screensize, gameconfig, stringres
    savelist=[]
    latestsavetime=0
    latestsave=0
    for i in range(startsaveslot,saveslotnum+1):
        savepath=os.path.join(GAME_PATH,'save',str(i)+u'.sav')
        if os.path.exists(savepath):
            try:
                savefile=file(savepath,'r')
                line=savefile.readline()#script path
                line=savefile.readline()#script linenum
                command=savefile.readline().decode('utf8')#game date
                if command[:-1]!=u'?,?':
                    args=command[:-1].split(',')
                    game_date=args[0]+'\xE6\x9C\x88'.decode('utf8')+args[1]+'\xE6\x97\xA5'.decode('utf8')
                else:
                    game_date=u''
                command=savefile.readline().decode('utf8')#real date
                args=command[:-2].split(',')
                real_date=('%04d\xE5\xB9\xB4%02d\xE6\x9C\x88%02d\xE6\x97\xA5  %02d:%02d:%02d'%(int(args[0]),int(args[1]),int(args[2]),int(args[3]),int(args[4]),int(args[5]))).decode('utf8')
                title=savefile.readline().decode('utf8')[:-1]#title
                limit=screensize[0]/gameconfig[u'fontsize']-6
                if len(title)>limit:
                    title=title[0:limit]+'\xE2\x80\xA6'.decode('utf8')
                line=savefile.readline()#bgm
                line=savefile.readline()#bg
                line=savefile.readline()#chara
                name=savefile.readline().decode('utf8')[:-1]#name
                message=savefile.readline().decode('utf8')[:-1].replace('\\n',' ')#message
                limit=screensize[0]/gameconfig[u'fontsize']-3
                if len(name+message)>limit:
                    message=message[0:limit-len(name)-1]+'\xE2\x80\xA6'.decode('utf8')
                savefile.close()
                if i==0:
                    autosave=stringres[u'AUTO_SAVE']
                else:
                    autosave=u''
                savetext=str(i)+u'. '+game_date+u'  '+title+autosave+u'\\n'+'\xE3\x80\x80'.decode('utf8')+name+'\xE2\x80\x9C'.decode('utf8')+message+'\xE2\x80\x9D'.decode('utf8')+u'\\n'+stringres[u'SAVE_TIME']+real_date
            except:
                savetext=str(i)+u'. NO DATA\\n'
        else:
            savetext=str(i)+u'. NO DATA\\n'
        savelist.append(savetext)
    return savelist

def Load():
    global globalsave
    savelist=read_save_list(0,100)
    selectlist=SelectList(savelist)
    selindex=selectlist.select(globalsave[u'latestsave'])
    if selindex==-1:
        return False
    else:
        if selindex > 0:
            globalsave[u'latestsave']=selindex
        return load_index(selindex)

def AppendMessageLog(namestr,messagestr):
    global messagelog
    if len(messagelog)>=50:
        messagelog.pop(0)
    if namestr:
        namestr=namestr+u' '
    else:
        namestr=u''
    messagelog.append(namestr+messagestr)
    
def ShowMessageLog():
    global messagelog
    selectlist=SelectList(messagelog)
    selectlist.select(len(messagelog)-1)

def wait(wait_time):
    #wait_time is an float value, in ms,
    global keyboard
    if not keyboard.is_down(key_codes.EScancode1):
        start_time=time.clock()
        purge_image(False, wait_time)
        e32.ao_yield()
        end_time=time.clock()
        delay=float(wait_time)/1000.0
        while (not keyboard.pressed(key_codes.EScancodeSelect) and (end_time-start_time < delay) ) :
            e32.ao_sleep(0.1)
            end_time=time.clock()

def Menu():
    global keyboard, screensize, GAME_PATH, gameconfig, staticimg, final_img, stringres
    staticimg['tempimg'].blit(final_img,(0,0))
    img_size=get_image_size(staticimg['menuimg'])
    img_origin=((screensize[0]-img_size[0])/2,40)
    select_text=SelectText([stringres[u'MENU_SAVE'],
                            stringres[u'MENU_LOAD'],
                            stringres[u'MENU_LOG'],
                            stringres[u'MENU_CONFIG'],
                            stringres[u'MENU_TITLE'],
                            stringres[u'MENU_SCREENSHOT'],
                            stringres[u'CANCEL']],
                           topleft=(img_origin[0],img_origin[1]+gameconfig[u'fontsize']),bottomright=(img_origin[0]+img_size[0],img_origin[1]+img_size[1]),init_highlight=0)
    draw_image(staticimg['menuimg'],img_origin=img_origin, on_canvas=False)
    #display current time on the menu
    try:
        timestr=time.strftime('%H:%M',time.localtime(time.time())).decode('ascii')
        draw_text(timestr, text_origin=(img_origin[0]+gameconfig[u'fontsize'],img_origin[1]+2), on_canvas=False)
    except:
        pass
    ret=select_text.select()
    if ret==0:
        Save()
        final_img.blit(staticimg['tempimg'],(0,0))
    elif ret==1:
        Load()
    elif ret==2:
        ShowMessageLog()
        final_img.blit(staticimg['tempimg'],(0,0))
    elif ret==3:
        ConfigForm()
        final_img.blit(staticimg['tempimg'],(0,0))
    elif ret==4:
        change_script(gameconfig[u'startscript'])
    elif ret==5:
        final_img.blit(staticimg['tempimg'],(0,0))
        draw_image(staticimg['menuimg'],img_origin=img_origin, on_canvas=False)
        select_text1=SelectText([stringres[u'SCREENSHOT_1'],
                                stringres[u'SCREENSHOT_2'],
                                stringres[u'SCREENSHOT_3'],
                                stringres[u'CANCEL']],
                               topleft=(img_origin[0],img_origin[1]+gameconfig[u'fontsize']),bottomright=(img_origin[0]+img_size[0],img_origin[1]+img_size[1]),init_highlight=0)
        ret1=select_text1.select()
        ScreenShot(ret1)
        final_img.blit(staticimg['tempimg'],(0,0))
    else:
        final_img.blit(staticimg['tempimg'],(0,0))
    del select_text

def get_game_date():
    global save, gameconfig
    if gameconfig[u'scripttype']==u'mo1':
        if save[u'variables'].has_key(u'F88') and save[u'variables'].has_key(u'F89'):
            if save[u'variables'][u'F88']>0 and save[u'variables'][u'F88']<13 and save[u'variables'][u'F89']>0 and save[u'variables'][u'F89']<32:
                return (save[u'variables'][u'F88'],save[u'variables'][u'F89'])
    elif gameconfig[u'scripttype']==u'mo2':
        if save[u'variables'].has_key(u'F8') and save[u'variables'].has_key(u'F9'):
            if save[u'variables'][u'F8']>0 and save[u'variables'][u'F8']<13 and save[u'variables'][u'F9']>0 and save[u'variables'][u'F9']<32:
                return (save[u'variables'][u'F8'],save[u'variables'][u'F9'])
    elif gameconfig[u'scripttype']==u'pymo':
        if save[u'variables'].has_key(u'FMONTH') and save[u'variables'].has_key(u'FDATE'):
            if save[u'variables'][u'FMONTH']>0 and save[u'variables'][u'FMONTH']<13 and save[u'variables'][u'FDATE']>0 and save[u'variables'][u'FDATE']<32:
                return (save[u'variables'][u'FMONTH'],save[u'variables'][u'FDATE'])
    return (0,0)

def read_game_info(gamefolder):
    gameconfigfile=file(os.path.join(gamefolder,'gameconfig.txt'),'r')
    while True:
        line=gameconfigfile.readline()
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=line[3:].decode('utf8')
        else:
            command=line.decode('utf8')
        args=del_blank(command).split(',')
        if args[0]==u'gametitle':
            gametitle=args[1]
    gameconfigfile.close()
    return (gamefolder,gametitle)

def SetEVFlag(bgfilename):
    global globalsave
    bgfilename=bgfilename.upper()
    if not (bgfilename in globalsave[u'evflag']):
        globalsave[u'evflag'].append(bgfilename)

def check_expression(exp):
    global save
    operandnum=0
    i=0
    tempvar=False
    operators=u'<>!='
    while exp[i] not in operators:
        i+=1
        if i>len(exp):
            print "No operator found in expression!"
            quit()
            break
    j=len(exp)
    while exp[j-1] not in operators:
        j-=1
        if j<=0:
            print "No operator found in expression!"
            quit()
            break
    operator=exp[i:j]
    operand1=del_blank(exp[:i])
    operand2=del_blank(exp[j:])
    if not save[u'variables'].has_key(operand1):
        print "No left operand",operand1,'to compare, create one'
        save[u'variables'][operand1]=0
        tempvar=True
    if operand2.isdigit():
        operandnum=int(operand2)
    else:
        if save[u'variables'].has_key(operand2):
            operandnum=save[u'variables'][operand2]
        else:
            print "No right operand",operand2,'to compare, return False'
            return False
    if operator==u'=' or operator==u'==':
        ret=(save[u'variables'][operand1]==operandnum)
    elif operator==u'>':
        ret=(save[u'variables'][operand1]>operandnum)
    elif operator==u'<':
        ret=(save[u'variables'][operand1]<operandnum)
    elif operator==u'>=':
        ret=(save[u'variables'][operand1]>=operandnum)
    elif operator==u'<=':
        ret=(save[u'variables'][operand1]<=operandnum)
    elif operator==u'<>' or operator==u'!' or operator==u'!=':
        ret=(save[u'variables'][operand1]!=operandnum)
    else:
        print "operator parse error",operator
        quit()
    if tempvar:
        del save[u'variables'][operand1]
    return ret

def del_blank(charlist):
    i=0
    startpos=0
    while i<len(charlist) and (charlist[i]==u' ' or charlist[i]==u'\t' or charlist[i]==u'\r' or charlist[i]==u'\n'):
        i+=1
        startpos=i
    i=len(charlist)-1
    endpos=i
    while i>=0 and (charlist[i]==u' ' or charlist[i]==u'\t' or charlist[i]==u'\r' or charlist[i]==u'\n'):
        i-=1
        endpos=i
    return charlist[startpos:endpos+1]

def del_escape_sequence(char_list):
    new_char_list=''
    numengchar=u'0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    i=0
    while i < len(char_list):
        if char_list[i]==u'%':
            i+=1
            while i < len(char_list) and (char_list[i] in numengchar):
                i+=1
        elif char_list[i]==u'\\':
            if char_list[i:i+3]==u'\\yf':
                new_char_list+='\xE2\x99\xAA'.decode('utf8')
                i+=3
            elif char_list[i:i+2]==u'\\.':
                new_char_list+='\xC2\xB7'.decode('utf8')
                i+=2
            elif char_list[i:i+3]==u'\\20':
                new_char_list+='\xE3\x80\x80'.decode('utf8')
                i+=3
            else:
                new_char_list+=char_list[i]
                i+=1
        elif i < len(char_list):
            new_char_list+=char_list[i]
            i+=1
    return new_char_list

def split_parameter(string,command):
    args=string[len(command):].split(',')
    ret=[]
    for arg in args:
        ret.append(del_blank(arg))
    return ret
        
def jump_to_label(position):
    global f,save
    origin_linenum=save[u'linenum']
    while True:
        line=f.readline()
        save[u'linenum']+=1
        #if not find until the end of file, search from beginning
        if len(line)==0:
            f.seek(0)
            save[u'linenum']=0
            line=f.readline()
            save[u'linenum']+=1
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        if command.startswith(u'#label '):
            if position==del_blank(command[7:]):
                break
        if save[u'linenum']==origin_linenum:
            if gameconfig[u'platform']!=u'pygame':
                appuifw.note(u'Label '+position+u' is not found!','error')
            break

def jump_to_line(linenum):
    global f,save
    save[u'linenum']=0
    while save[u'linenum']<linenum:
        f.readline()
        save[u'linenum']+=1

def Auto_Play(pos=(0,0)):
    global auto_play,staticimg,screensize,running
    if running:
        auto_play=not auto_play
        if auto_play:
            load_keypad(autoon=True)
        else:
            load_keypad(autoon=False)

def unpack_file(filename, filetype):
    global voindex,vopakfile,seindex,sepakfile,bgindex,bgpakfile,charaindex,charapakfile,GAME_PATH, gameconfig
    filename=filename.upper()
    #if gameconfig[u'platform']==u'pygame':
    #    destfilename=filename.lower()
    #else:
    destfilename=filename
    if filetype==u'bgformat':
        if bgpakfile==None:
            return
        if bgindex.has_key(filename):
            try:
                tempfile=file(os.path.join(GAME_PATH,'bg',destfilename+gameconfig[filetype]),'wb')
                bgpakfile.seek(bgindex[filename][0])
                tempfile.seek(0)
                tempfile.write(bgpakfile.read(bgindex[filename][1]))
                tempfile.close()
            except:
                print 'Error while unpacking bg resource. Memory card full?'
    if filetype==u'charaformat' or filetype==u'charamaskformat':
        if charapakfile==None:
            return
        if charaindex.has_key(filename):
            try:
                tempfile=file(os.path.join(GAME_PATH,'chara',destfilename+gameconfig[filetype]),'wb')
                charapakfile.seek(charaindex[filename][0])
                tempfile.seek(0)
                tempfile.write(charapakfile.read(charaindex[filename][1]))
                tempfile.close()
            except:
                print charaindex[filename]
                print 'Error while unpacking chara resource. Memory card full?'
    if filetype==u'voiceformat':
        if vopakfile==None:
            return
        if voindex.has_key(filename):
            try:
                tempfile=file(os.path.join(GAME_PATH,u'voice',destfilename+gameconfig[filetype]),'wb')
                vopakfile.seek(voindex[filename][0])
                tempfile.seek(0)
                tempfile.write(vopakfile.read(voindex[filename][1]))
                tempfile.close()
            except:
                print 'Error while unpacking voice resource. Memory card full?'
    if filetype==u'seformat':
        if sepakfile==None:
            return
        if seindex.has_key(filename):
            try:
                tempfile=file(os.path.join(GAME_PATH,'se',destfilename+gameconfig[filetype]),'wb')
                sepakfile.seek(seindex[filename][0])
                tempfile.seek(0)
                tempfile.write(sepakfile.read(seindex[filename][1]))
                tempfile.close()
            except:
                print 'Error while unpacking se resource. Memory card full?'


def rename_files(basepath):
    for root, dirs, files in os.walk(basepath):
        for filename in files:
            filepath = os.path.join(root, filename)
            filename = filename.lower()
            new_filepath = os.path.join(root, filename)
            try:
                os.rename(filepath, new_filepath)
            except:
                #print "Error renaming", filepath
                pass

def remove_null_end(srcstring):
    pos=srcstring.find('\0')
    if pos==-1:
        return srcstring
    else:
        return srcstring[:pos]

def load_pak_file(pakfilename):
    global GAME_PATH
    pakpath=os.path.join(GAME_PATH,pakfilename)
    if not os.path.exists(pakpath):
        print 'Files are not packaged into',pakfilename
        return None,None
    pakfile=file(pakpath,'rb')
    #read the voice file list
    filecount=struct.unpack('I',pakfile.read(4))[0]
    fileindex={}
    i=0
    while i< filecount:
        rawname=remove_null_end(pakfile.read(32))
        try:
            filename=rawname.decode('gbk')
        except:
            filename=rawname
        fileoffset=struct.unpack('I',pakfile.read(4))[0]
        filelength=struct.unpack('I',pakfile.read(4))[0]
        fileindex[filename]=(fileoffset,filelength)
        i+=1
    return pakfile,fileindex

def load_string_res(stringresfilename):
    global stringres
    stringresfile=file(stringresfilename,'r')
    stringres={}
    while True:
        line=stringresfile.readline()
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=line[3:].decode('utf8')
        else:
            command=line.decode('utf8')
        pos=command.find(',')
        if pos==-1:
            print 'load_string_res::No seperator found.'
            continue
        resname=del_blank(command[0:pos])
        rescontent=del_blank(command[pos+1:])
        stringres[resname]=rescontent
    stringresfile.close()
    return stringres

def purge_voice(isexit=False):
    global GAME_PATH,gameconfig,vopakfile
    VO_STP()
    if vopakfile==None or( not os.path.exists(os.path.join(GAME_PATH,'voice'))):
        return
    voicefiles=os.listdir(os.path.join(GAME_PATH,'voice'))
    for voicefilename in voicefiles:
        if voicefilename.endswith(gameconfig[u'voiceformat']):
            if isexit or (not cache['vo'].has_key(voicefilename[:-len(gameconfig[u'voiceformat'])])):
                try:
                    os.remove(os.path.join(GAME_PATH,'voice',voicefilename))
                except:
                    #print 'Error while deleting',voicefilename
                    pass

def purge_image(isexit=False,timelimit=0):
    global GAME_PATH,gameconfig,bgpakfile,charapakfile,sepakfile
    if timelimit!=0:
        start_time=time.clock()
        end_time=start_time + float(timelimit)/1000.0
    if bgpakfile!=None:
        voicefiles=os.listdir(os.path.join(GAME_PATH,'bg'))
        for voicefilename in voicefiles:
            if voicefilename.endswith(gameconfig[u'bgformat']):
                try:
                    os.remove(os.path.join(GAME_PATH,'bg',voicefilename))
                except:
                    #print 'Error while deleting',voicefilename
                    pass
                if timelimit!=0 and end_time < time.clock():
                    return
        if isexit:
            bgpakfile.close()
    if charapakfile!=None:
        voicefiles=os.listdir(os.path.join(GAME_PATH,'chara'))
        for voicefilename in voicefiles:
            if voicefilename.endswith(gameconfig[u'charaformat']) or voicefilename.endswith(gameconfig[u'charamaskformat']):
                try:
                    os.remove(os.path.join(GAME_PATH,'chara',voicefilename))
                except:
                    #print 'Error while deleting',voicefilename
                    pass
                if timelimit!=0 and end_time < time.clock():
                    return
        if isexit:
            charapakfile.close()
    if isexit and sepakfile!=None:
        voicefiles=os.listdir(os.path.join(GAME_PATH,'se'))
        for voicefilename in voicefiles:
            if voicefilename.endswith(gameconfig[u'seformat']):
                try:
                    os.remove(os.path.join(GAME_PATH,'se',voicefilename))
                except:
                    #print 'Error while deleting',voicefilename
                    pass
                if timelimit!=0 and end_time < time.clock():
                    return
        sepakfile.close()

def Prefetching():
    global gameconfig
    if gameconfig[u'scripttype']==u'mo1':
        PrefetchingMO1()
    elif gameconfig[u'scripttype']==u'mo2':
        PrefetchingMO2()
    elif gameconfig[u'scripttype']==u'pymo':
        PrefetchingPYMO()

def PrefetchingMO1():
    global cache,f,cache_pos, gameconfig
    bak_pos=f.tell()
    cache_purge(bak_pos)
    total_entry=0
    for temp_type in cache:
        if temp_type!='sel':
            total_entry+=len(cache[temp_type])
    if total_entry > 5:
        return
    if cache_pos<bak_pos:
        cache_pos=bak_pos
    f.seek(cache_pos)
    while True:
        line=f.readline()
        cache_pos=f.tell()
        if len(line)==0:
            break
        command=line.decode('utf8')
        #bg
        if command.startswith(u'#bg '):
            args=command[4:-1].split(',')
            cache_add('bg',args[0],cache_pos,bak_pos)
            break
        #csp
        if command.startswith(u'#csp '):
            args=command[5:-1].split(',')
            cache_add('chara',args[1],cache_pos,bak_pos)
            break
        #cspw
        if command.startswith(u'#cspw '):
            args=command[6:-1].split(',')
            cache_add('chara',args[2],cache_pos,bak_pos)
            cache_add('chara',args[3],cache_pos,bak_pos)
            break
        #vo
        if command.startswith(u'#vo '):
            cache_add('vo',command[4:-1],cache_pos,bak_pos)
            break
        #bgm
        if command.startswith(u'#bgm '):
            cache_add('bgm',command[5:-1],cache_pos,bak_pos)
            continue
        #sel
        if command.startswith(u'#sel '):
            args=command[5:-1].split(',')
            if len(args)==1:
                args.append(u'HINT_NONE')
            i=int(args[0])
            choices=[]
            while i>0:
                line=f.readline()
                if len(line)==0:
                    break
                choices.append(line.decode('utf8')[:-1])
                i-=1
            cache_pos=f.tell()
            cache_add_sel(choices,args[1],cache_pos,bak_pos)
            continue
    f.seek(bak_pos)

def PrefetchingMO2():
    global cache,f,cache_pos, gameconfig
    bak_pos=f.tell()
    cache_purge(bak_pos)
    total_entry=0
    for temp_type in cache:
        if temp_type!='sel':
            total_entry+=len(cache[temp_type])
    if total_entry > 5:
        return
    if cache_pos<bak_pos:
        cache_pos=bak_pos
    f.seek(cache_pos)
    while True:
        line=f.readline()
        cache_pos=f.tell()
        if len(line)==0:
            break
        command=line.decode('utf8')
        #bg
        if command.startswith(u'#BG_DSP '):
            args=del_blank(command[8:-1]).split(',')
            cache_add('bg',args[0],cache_pos,bak_pos)
            break
        #BG_PART
        if command.startswith(u'#BG_PART '):
            args=del_blank(command[9:-1]).split(',')
            cache_add('bg',args[0],cache_pos,bak_pos)
            break
        #csp
        if command.startswith(u'#CHR_DSP '):
            args=del_blank(command[9:-1]).split(',')
            if len(args[1])==7:
                args[1]=args[1][0:6]
            cache_add('chara',args[1],cache_pos,bak_pos)
            break
        #cspw
        if command.startswith(u'#CHR_DSPW '):
            args=del_blank(command[10:-1]).split(',')
            if len(args[1])>6:
                args[1]=args[1][0:6]
            if len(args[2])>6:
                args[2]=args[2][0:6]
            cache_add('chara',args[1],cache_pos,bak_pos)
            cache_add('chara',args[2],cache_pos,bak_pos)
            break
        #CHR_DSPM
        if command.startswith(u'#CHR_DSPM '):
            args=del_blank(command[10:-1]).split(',')
            for i in range (0,len(args)-1,3):
                cache_add('chara',args[i],cache_pos,bak_pos)
            break
        #vo
        if command.startswith(u'#VO_STA '):
            cache_add('vo',del_blank(command[8:-1]),cache_pos,bak_pos)
            break
        #bgm
        if command.startswith(u'#BGM_STA '):
            args=del_blank(command[9:-1]).split(',')
            cache_add('bgm',args[0],cache_pos,bak_pos)
            break
        #sel
        if command.startswith(u'#SELECT '):
            args=del_blank(command[8:-1]).split(',')
            if len(args)==1:
                args.append(u'HINT_NONE')
            i=int(args[0])
            choices=[]
            while i>0:
                line=f.readline()
                if len(line)==0:
                    break
                choices.append(line.decode('utf8')[:-1])
                i-=1
            cache_pos=f.tell()
            cache_add_sel(choices,args[1],cache_pos,bak_pos)
            break
    f.seek(bak_pos)
    
def PrefetchingPYMO():
    global cache,f,cache_pos, gameconfig
    bak_pos=f.tell()
    cache_purge(bak_pos)
    total_entry=0
    for temp_type in cache:
        if temp_type!='sel':
            total_entry+=len(cache[temp_type])
    if total_entry > 8:
        return
    if cache_pos<bak_pos:
        cache_pos=bak_pos
    f.seek(cache_pos)
    while True:
        line=f.readline()
        cache_pos=f.tell()
        if len(line)==0:
            break
        command=line.decode('utf8')
        #bg
        if command.startswith(u'#bg '):
            args=split_parameter(command,u'#bg ')
            cache_add('bg',args[0],cache_pos,bak_pos)
            break
        #chara
        if command.startswith(u'#chara '):
            args=split_parameter(command,u'#chara ')
            for i in range (1,len(args)-1,4):
                if args[i].upper()!=u'NULL':
                    cache_add('chara',args[i],cache_pos,bak_pos)
            break
        #chara_y
        if command.startswith(u'#chara_y '):
            args=split_parameter(command,u'#chara_y ')
            for i in range (2,len(args)-1,5):
                if args[i].upper()!=u'NULL':
                    cache_add('chara',args[i],cache_pos,bak_pos)
            break
        #chara_scroll 5,0,SM02AMA,0,0,50,0,1,400
        #chara_scroll 5,0,50,0,400
        if command.startswith(u'#chara_scroll '):
            args=split_parameter(command,u'#chara_scroll ')
            if len(args)==10:
                cache_add('chara',args[2],cache_pos,bak_pos)
            break
        #vo
        if command.startswith(u'#vo '):
            args=split_parameter(command,u'#vo ')
            cache_add('vo',args[0],cache_pos,bak_pos)
            break
        #bgm
        if command.startswith(u'#bgm '):
            args=split_parameter(command,u'#bgm ')
            cache_add('bgm',args[0],cache_pos,bak_pos)
            break
        #sel
        if command.startswith(u'#sel '):
            args=split_parameter(command,u'#sel ')
            if len(args)==1:
                args.append(u'HINT_NONE')
            i=int(args[0])
            choices=[]
            while i>0:
                line=f.readline()
                if len(line)==0:
                    break
                choices.append(line.decode('utf8')[:-1])
                i-=1
            cache_pos=f.tell()
            cache_add_sel(choices,args[1],cache_pos,bak_pos)
            break
    f.seek(bak_pos)

def cache_purge(bak_pos):
    global cache
    #purge if the entries are too old
    for type in cache.keys():
        if type!='sel':
            for temp_cache in cache[type].keys():
                if bak_pos > cache[type][temp_cache]['cache_pos']:
                    del cache[type][temp_cache]
                    #print 'purged because of too old: ',temp_cache,' ',len(cache[type])
    #purge if the select entries are too old
    if cache['sel']!=None and bak_pos > cache['sel']['cache_pos']:
        del cache['sel']
        cache['sel']=None
        #print 'purged select because of too old'

def change_script(filename):
    global f, save, GAME_PATH, cache, cache_pos, gameconfig
    if f:
        f.close()
    f=file(os.path.join(GAME_PATH,'script',filename+u'.txt'),'r')
    cache={'bg':{},'chara':{},'vo':{},'bgm':{},'sel':None}
    cache_pos=0
    save[u'linenum']=0
    purge_voice()
    purge_image()
    SE_STP()
    if filename==gameconfig[u'startscript']:
        purge_variable()

def push_call_stack():
    global f, save
    save[u'callstack'].append((os.path.basename(f.name)[:-4],save[u'linenum']))

def pop_call_stack():
    global f, save
    return save[u'callstack'].pop()

def ScriptParseMO1():
    global f,save,cache,cache_pos,withname,gameconfig,running, bgsize
    while running:
        line=f.readline()
        save[u'linenum']+=1
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        #change  
        if command.startswith(u'#change '):
            args=split_parameter(command,u'#change ')
            change_script(args[0])
            continue
        #end STF_AYAKA_PURE
        if command.startswith(u'#end '):
            args=split_parameter(command,u'#end ')
            change_script(args[0])
            continue
        #bg
        if command.startswith(u'#bg '):
            args=split_parameter(command,u'#bg ')
            if args[0].startswith(gameconfig[u'cgprefix']):
                SetEVFlag(args[0])
            BGLoad(0,args[0])
            BGDisp(0,args[1],args[2])
            CHASetInvisible(u'a')
            continue
        #bgtime
        if command.startswith(u'#bgtime '):
            args=split_parameter(command,u'#bgtime ')
            BGLoad(0,args[0])
            delay_until(int(args[1]))
            BGDisp(0,u'BG_ALPHA',u'BG_SLOW')
            CHASetInvisible(u'a')
            continue   
        #scroll B34a,0,0,100,0,10000
        if command.startswith(u'#scroll '):
            args=split_parameter(command,u'#scroll ')
            SCROLL(int(args[5]),args[0],startpos=(int(args[1]),int(args[2])),endpos=(int(args[3]),int(args[4])))
            if args[0].startswith(gameconfig[u'cgprefix']):
                SetEVFlag(args[0])
            continue     
        #fade_out
        if command.startswith(u'#fade_out '):
            args=split_parameter(command,u'#fade_out ')
            if args[1]==u'FADE_WHITE':
                FADE(int(args[0])*1000/60, color=(255,255,255))
            else:
                FADE(int(args[0])*1000/60, color=(0,0,0))
            continue 
        ##fade_out_sta
        if command.startswith(u'#fade_out_sta '):
            args=split_parameter(command,u'#fade_out_sta ')
            if args[1]==u'FADE_WHITE':
                FADE(int(args[0])*1000/60, color=(255,255,255))
            else:
                FADE(int(args[0])*1000/60, color=(0,0,0))
            continue
        #fade_in
        if command.startswith(u'#fade_in '):
            args=split_parameter(command,u'#fade_in ')
            if args[0].isdigit():
                FADE(int(args[0])*1000/60,is_fade_out=False)
            else:
                FADE(300,is_fade_out=False)
            continue
        #fade_in_sta 
        if command.startswith(u'#fade_in_sta'):
            FADE(300,is_fade_out=False)
            continue
        #csp
        if command.startswith(u'#csp '):
            args=split_parameter(command,u'#csp ')
            CHAload(args[0],args[1])
            CHAParsePos(args[0],args[2])
            CHASetVisible(args[0])
            CHADisp()
            continue
        #cpos 0,CHR_CENTER+5,6
        if command.startswith(u'#cpos '):
            args=split_parameter(command,u'#cpos ')
            CHAParsePos(args[0],args[1])
            CHADisp(transition=None)
            continue
        #csptime
        if command.startswith(u'#csptime '):
            args=split_parameter(command,u'#csptime ')
            CHAload(args[0],args[1])
            CHAParsePos(args[0],args[2])
            CHASetVisible(args[0])
            delay_until(int(args[3]))
            CHADisp()
            continue
        #crs
        if command.startswith(u'#crs '):
            args=split_parameter(command,u'#crs ')
            CHASetInvisible(args[0])
            CHAResetPos(args[0])
            CHADisp()
            continue
        #cspw
        if command.startswith(u'#cspw '):
            args=split_parameter(command,u'#cspw ')
            if not save[u'chara'].has_key(args[0]):
                save[u'chara'][args[0]]={}
            if not save[u'chara'].has_key(args[1]):
                save[u'chara'][args[1]]={}
            CHAload(args[0],args[2])
            CHASetPos(args[0],bgsize[0]/4)
            CHASetVisible(args[0])
            CHAload(args[1],args[3])
            CHASetPos(args[1],bgsize[0]*3/4)
            CHASetVisible(args[1])
            CHADisp()
            continue
        #cspwtime
        if command.startswith(u'#cspwtime '):
            args=split_parameter(command,u'#cspwtime ')
            if not save[u'chara'].has_key(args[0]):
                save[u'chara'][args[0]]={}
            if not save[u'chara'].has_key(args[1]):
                save[u'chara'][args[1]]={}
            CHAload(args[0],args[2])
            CHASetPos(args[0],bgsize[0]/4)
            CHAload(args[1],args[3])
            CHASetPos(args[1],bgsize[0]*3/4)
            CHASetVisible(args[0])
            CHASetVisible(args[1])
            delay_until(int(args[4]))
            CHADisp()
            continue
        #;	VIB_DOKA
        if command.startswith(u';\tVIB_DOKA'):
            QUAKE()
            continue    
        #woff
        if command.startswith(u'#woff'):
            #CHASetInvisible(u'a')
            SE_STP()
            continue
        #vo
        if command.startswith(u'#vo '):
            args=split_parameter(command,u'#vo ')
            VO_STA(args[0])
            continue
        #bgm
        if command.startswith(u'#bgm '):
            args=split_parameter(command,u'#bgm ')
            BGMPlay(args[0])
            continue
        #bgmonce
        if command.startswith(u'#bgmonce '):
            args=split_parameter(command,u'#bgmonce ')
            BGMPlay(args[0],1)
            continue
        #mst
        if command.startswith(u'#mst'):
            BGMStop()
            continue
        #eff
        if command.startswith(u'#eff '):
            args=split_parameter(command,u'#eff ')
            SE_STA(args[0])
            continue
        #;	SE_PLY		SE11,SE_NEAR
        if command.startswith(u';\tSE_PLY'):
            args=split_parameter(command,u';\tSE_PLY')
            SE_STA(args[0])
            continue
        #sst
        if command.startswith(u'#sst'):
            SE_STP()
            continue
        #say
        if command.startswith(u'*'):
            withname=False
        if len(command)>1 and (not command.startswith(u'#')) and (not command.startswith(u'*')) and (not command.startswith(u';')) :
            if command[0]=='\xe3\x80\x90'.decode('utf8'):  #E38090==left container
                name_text=command[1:command.find('\xe3\x80\x91'.decode('utf8'))]
                withname=True
                continue
            if withname==True:
                message(del_escape_sequence(command),name_text)
            else:
                message(del_escape_sequence(command))
            continue
        #sel
        if command.startswith(u'#sel '):
            args=split_parameter(command,u'#sel ')
            if len(args)==1:
                args.append(u'HINT_NONE')
            i=int(args[0])
            choices=[]
            while i>0:
                line=f.readline()
                save[u'linenum']+=1
                if len(line)==0:
                    break
                choices.append(del_blank(line.decode('utf8')))
                i-=1
            save[u'variables']['F91']=Select(choices,args[1])
            continue
        #set F88, 10
        if command.startswith(u'#set '):
            args=split_parameter(command,u'#set ')
            value=args[1]
            if value.isdigit():
                save[u'variables'][args[0]]=int(value)
            elif save[u'variables'].has_key(value):
                save[u'variables'][args[0]]=save[u'variables'][value]
            else:
                save[u'variables'][args[0]]=0
            continue
        #add F3,1
        if command.startswith(u'#add '):
            args=split_parameter(command,u'#add ')
            if not save[u'variables'].has_key(args[0]):
                print "No variable",args[0]
                continue
            save[u'variables'][args[0]]+=int(args[1].replace(' ',''))
            #print variables
            continue
        #if F91<>0,goto IF_LABEL_2
        if command.startswith(u'#if '):
            args=split_parameter(command,u'#if ')
            if check_expression(args[0]):
                jump_to_label(del_blank(args[1])[5:])
            continue
        #goto IF_LABEL_2_END
        if command.startswith(u'#goto '):
            args=split_parameter(command,u'#goto ')
            jump_to_label(args[0])
            continue
        #movie
        if command.startswith(u'#movie '):
            args=split_parameter(command,u'#movie ')
            PlayMovie(args[0])
            continue
        #title
        if command.startswith(u'#title '):
            args=split_parameter(command,u'#title ')
            ChangeTitle(args[0])
            continue
        #title_dsp
        if command.startswith(u'#title_dsp'):
            ShowTitle()
            continue
        #scr_calen EYE_6
        if command.startswith(u'#scr_calen'):
            args=split_parameter(command,u'#scr_calen ')
            ShowCalender(args[0],(60,42))
            continue
        #wait 240
        if command.startswith(u'#wait '):
            args=split_parameter(command,u'#wait ')
            e32.ao_sleep(float(args[0])/60.0)
            continue
        #waittime 240
        if command.startswith(u'#waittime '):
            args=split_parameter(command,u'#waittime ')
            delay_until(int(args[0]))
            continue
        #EXT_CALL KAO
        if command.startswith(u'#EXT_CALL '):
            args=split_parameter(command,u'#EXT_CALL ')
            push_call_stack()
            change_script(args[0])
            continue
        #;	RET
        if command.startswith(u';\tRET') or command.startswith(u';\t\tRET'):
            if len(save[u'callstack'])>0:
                args=pop_call_stack()
                change_script(args[0])
                jump_to_line(args[1])
            continue
        #select_text 3,Pure Story,Continue,Exit,10,160,160,240,4099060,0,HINT_NONE
        if command.startswith(u'#select_text '):
            args=split_parameter(command,u'#select_text ')
            selentry=[]
            for i in range(1,int(args[0])+1):
                selentry.append(args[i])
            select_text=SelectText(selentry,
                                   topleft=pos_bg2screen((int(args[i+1])*bgsize[0]/100,int(args[i+2])*bgsize[1]/100)),
                                   bottomright=pos_bg2screen((int(args[i+3])*bgsize[0]/100,int(args[i+4])*bgsize[1]/100)),
                                   textcolor=intstr2color(args[i+5]),init_highlight=int(args[i+6]),hint=args[i+7])
            save[u'variables']['F91']=select_text.select()
            del selentry
            del select_text
            continue
        #select_img 4,button,40,40,var0,40,50,var1,40,60,var2,40,70,var3,1
        if command.startswith(u'#select_img '):
            args=split_parameter(command,u'#select_img ')
            selentry=[]
            varentry=[]
            for i in range(2,3*int(args[0]),3):
                selentry.append(pos_bg2screen((int(args[i])*bgsize[0]/100,int(args[i+1])*bgsize[1]/100)))
                if args[i+2]=='0':
                    varentry.append(False)
                elif save[u'variables'].has_key(args[i+2]):
                    varentry.append(bool(save[u'variables'][args[i+2]]))
                else:
                    varentry.append(True)
            i+=3
            select_img=SelectImg(load_select_image(args[1],len(selentry)),selentry,varentry,int(args[i]))
            save[u'variables']['F91']=select_img.select()
            del selentry
            del select_img
            continue
        #load
        if command.startswith(u'#load'):
            Load()
            continue
        #ALBUM
        if command.startswith(u'#ALBUM'):
            album=Album()
            album.select()
            del album
            continue
        #MUSIC
        if command.startswith(u'#MUSIC'):
            music=Musicbox()
            music.select()
            del music
            continue

def ScriptParseMO2():
    global f,save,cache,cache_pos,withname,gameconfig,running, bgsize, in_fade_out
    while running:
        line=f.readline()
        save[u'linenum']+=1
        if len(line)==0:
            break
        if len(line)>3 and line[:3] == codecs.BOM_UTF8:
            command=del_blank(line[3:].decode('utf8'))
        else:
            command=del_blank(line.decode('utf8'))
        #GOTO_ENDING 
        if command.startswith(u'#GOTO_ENDING'):
            args=split_parameter(command,u'#GOTO_ENDING')
            e32.ao_sleep(1.0)
            in_fade_out=False
            if len(args)==2:
                change_script(args[1])
            else:
                change_script(gameconfig[u'startscript'])
            continue
        #change  
        if command.startswith(u'#change '):
            args=split_parameter(command,u'#change ')
            change_script(args[0])
            continue
        #bg
        if command.startswith(u'#BG_DSP '):
            args=split_parameter(command,u'#BG_DSP ')
            if args[0].startswith(gameconfig[u'cgprefix']):
                SetEVFlag(args[0])
            BGLoad(0,args[0])
            BGDisp(0, transition=u'BG_ALPHA', speed=u'BG_NORMAL')
            CHASetInvisible(u'a')
            continue
        #scroll B34a,0,0,100,0,10000
        if command.startswith(u'#scroll '):
            args=split_parameter(command,u'#scroll ')
            SCROLL(int(args[5]),args[0],startpos=(int(args[1]),int(args[2])),endpos=(int(args[3]),int(args[4])))
            if args[0].startswith(gameconfig[u'cgprefix']):
                SetEVFlag(args[0])
            continue
        #CG_DSP EV_TT13A,,10,CG_BTM
        if command.startswith(u'#CG_DSP '):
            args=split_parameter(command,u'#CG_DSP ')
            if args[0].startswith(gameconfig[u'cgprefix']):
                SetEVFlag(args[0])
            BGLoad(0,args[0])
            BGDisp(0, transition=u'BG_ALPHA', speed=u'BG_NORMAL')
            CHASetInvisible(u'a')
            continue
        #BG_PART
        if command.startswith(u'#BG_PART '):
            args=split_parameter(command,u'#BG_PART ')
            if args[0].startswith(u'EV_'):
                SetEVFlag(args[0])
            BGLoad(0,args[0],(int(args[1]),int(args[2])))
            BGDisp(0,transition=u'BG_ALPHA', speed=u'BG_NORMAL')
            CHASetInvisible(u'a')
            continue
        #bgtime
        if command.startswith(u'#bgtime '):
            args=split_parameter(command,u'#bgtime ')
            BGLoad(0,args[0])
            delay_until(int(args[1]))
            BGDisp(0,u'BG_ALPHA',u'BG_SLOW')
            CHASetInvisible(u'a')
            continue        
        #FLUSH RED
        if command.startswith(u'#FLUSH '):
            args=split_parameter(command,u'#FLUSH ')
            Flush(args)
            continue
        #FADE_OUT 75,FADE_BLACK
        if command.startswith(u'#FADE_OUT '):
            args=split_parameter(command,u'#FADE_OUT ')
            if len(args)<2:
                args.append(u'FADE_BLACK')
            if args[1]==u'FADE_WHITE':
                FADE(int(args[0])*1000/60, color=(255,255,255))
            else:
                FADE(int(args[0])*1000/60, color=(0,0,0))
            continue
        #FADE_IN 75
        if command.startswith(u'#FADE_IN '):
            args=split_parameter(command,u'#FADE_IN ')
            if args[0].isdigit():
                FADE(int(args[0])*1000/60,is_fade_out=False)
            else:
                FADE(300,is_fade_out=False)
            continue
        #CHR_DSP 1,SH18CMA,CHR_LEFT_O
        if command.startswith(u'#CHR_DSP '):
            args=split_parameter(command,u'#CHR_DSP ')
            if len(args[1])==7:
                args[1]=args[1][0:6]
            CHAload(args[0],args[1])
            if len(args)==2:
                args.append(u'')
            CHAParsePos(args[0],args[2])
            CHASetVisible(args[0])
            CHADisp()
            continue
        #csptime
        if command.startswith(u'#csptime '):
            args=split_parameter(command,u'#csptime ')
            CHAload(args[0],args[1])
            CHAParsePos(args[0],args[2])
            CHASetVisible(args[0])
            delay_until(int(args[3]))
            CHADisp()
            continue
        #CHR_POSC 0,CHR_RIGHT-5,4
        if command.startswith(u'#CHR_POSC '):
            args=split_parameter(command,u'#CHR_POSC ')
            CHAParsePos(args[0],args[1])
            CHADisp(transition=None)
            continue
        #CHR_ERS
        if command.startswith(u'#CHR_ERS '):
            args=split_parameter(command,u'#CHR_ERS ')
            if args[0]==u'3':
                args[0]=u'a'
            CHASetInvisible(args[0])
            CHAResetPos(args[0])
            CHADisp()
            continue
        #CHR_ERSW
        if command.startswith(u'#CHR_ERSW'):
            CHASetInvisible(u'a')
            CHADisp()
            continue
        #CHR_DSPW 0,SM02AMA,SN01AMA,CHR_LEFT,CHR_RIGHT
        if command.startswith(u'#CHR_DSPW '):
            args=split_parameter(command,u'#CHR_DSPW ')
            args.insert(1,str(1-int(args[0])))
            if len(args[2])>6:
                args[2]=args[2][0:6]
            if len(args[3])>6:
                args[3]=args[3][0:6]
            if not save[u'chara'].has_key(args[0]):
                save[u'chara'][args[0]]={}
            if not save[u'chara'].has_key(args[1]):
                save[u'chara'][args[1]]={}
            if len(args)==4:
                args.append(u'CHR_LEFT')
                args.append(u'CHR_RIGHT')
            if args[4]==u'':
                args[4]=u'CHR_LEFT'
            if args[5]==u'':
                args[5]=u'CHR_RIGHT'
            CHAload(args[0],args[2])
            CHAParsePos(args[0],args[4])
            CHASetVisible(args[0])
            CHAload(args[1],args[3])
            CHAParsePos(args[1],args[5])
            CHASetVisible(args[1])
            CHADisp()
            continue
        #CHR_DSPM SM02AMA,25,1,SN01AMA,75,2,20
        if command.startswith(u'#CHR_DSPM '):
            args=split_parameter(command,u'#CHR_DSPM ')
            for i in range (0,len(args)-1,3):
                if not save[u'chara'].has_key(str(i)):
                    save[u'chara'][str(i)]={}
                CHAload(str(i),args[i])
                CHASetPos(str(i),int(del_blank(args[i+1]))*bgsize[0]/100)
                CHASetLayer(str(i),int(del_blank(args[i+2])))
                CHASetVisible(str(i))
            CHADisp(length=int(args[len(args)-1])*17)
            continue
        #cspwtime
        if command.startswith(u'#cspwtime '):
            args=split_parameter(command,u'#cspwtime ')
            if not save[u'chara'].has_key(args[0]):
                save[u'chara'][args[0]]={}
            if not save[u'chara'].has_key(args[1]):
                save[u'chara'][args[1]]={}
            CHAload(args[0],args[2])
            CHASetPos(args[0],bgsize[0]/4)
            CHASetLayer(args[0],0)
            CHASetVisible(args[0])
            CHAload(args[1],args[3])
            CHASetPos(args[1],bgsize[0]*3/4)
            CHASetLayer(args[1],0)
            CHASetVisible(args[1])
            delay_until(int(args[4]))
            CHADisp()
            continue
        #VIB_COLLISION_L
        if command.startswith(u'#VIB_COLLISION_L'):
            QUAKE()
            continue    
        #woff
        #if command.startswith(u'#woff'):
        #    SE_STP()
        #    continue
        #VO_STA ME01022
        if command.startswith(u'#VO_STA '):
            args=split_parameter(command,u'#VO_STA ')
            VO_STA(args[0])
            continue
        #BGM_STA BGM15,85
        if command.startswith(u'#BGM_STA '):
            args=split_parameter(command,u'#BGM_STA ')
            BGMPlay(args[0])
            continue
        #bgmonce
        if command.startswith(u'#bgmonce '):
            args=split_parameter(command,u'#bgmonce ')
            BGMPlay(args[0],1)
            continue
        #BGM_STP 8
        if command.startswith(u'#BGM_STP'):
            BGMStop()
            continue
        #SE_STA SE00_16
        if command.startswith(u'#SE_STA '):
            args=split_parameter(command,u'#SE_STA ')
            if len(args)==1:
                SE_STA(args[0])
            else:
                args[1]=del_blank(args[1])
                if args[1].isdigit():
                    SE_STA(args[0],duration=int(args[1])*1000)
            continue
        #SE_STP
        if command.startswith(u'#SE_STP'):
            SE_STP()
            continue
        #say
        if command.startswith(u'*'):
            withname=False
        if len(command)>1 and (not command.startswith(u'#')) and (not command.startswith(u'@')) and (not command.startswith(u';')):
            command=del_escape_sequence(command)
            ret1=command.find('\xE3\x80\x8C'.decode('utf8'))  #%E3%80%8C==thin left container
            ret2=command.find('\xE3\x80\x8D'.decode('utf8'))  #%E3%80%8D==thin right container
            ret3=command.find('\xE3\x80\x8E'.decode('utf8'))  #%E3%80%8E==thick left container
            ret4=command.find('\xE3\x80\x8F'.decode('utf8'))  #%E3%80%8F==thick right container
            if ret1>0 and ret1<10 and ret2==len(command)-1:
                message(command[ret1:],command[:ret1])
            elif ret3>0 and ret3<10 and ret4==len(command)-1:
                message(command[ret3:],command[:ret3])
            else:
                message(command)
            continue
        #SELECT 2,HINT_NONE
        if command.startswith(u'#SELECT '):
            args=split_parameter(command,u'#SELECT ')
            if len(args)==1:
                args.append(u'HINT_NONE')
            i=int(args[0])
            choices=[]
            while i>0:
                line=f.readline()
                save[u'linenum']+=1
                if len(line)==0:
                    break
                choices.append(del_blank(line.decode('utf8')))
                i-=1
            save[u'variables']['F11']=Select(choices,args[1])
            continue
        #RSET F58,1
        if command.startswith(u'#RSET '):
            args=split_parameter(command,u'#RSET ')
            value=del_blank(args[1])
            if value.isdigit():
                save[u'variables'][args[0]]=int(value)
            elif save[u'variables'].has_key(value):
                save[u'variables'][args[0]]=save[u'variables'][value]
            else:
                save[u'variables'][args[0]]=0
            continue
        #add F11,S1
        if command.startswith(u'#add '):
            args=split_parameter(command,u'#add ')
            if not save[u'variables'].has_key(args[0]):
                print "No variable",args[0],'to add,create it.'
                save[u'variables'][args[0]]=0
            value=del_blank(args[1])
            if value.isdigit():
                save[u'variables'][args[0]]+=int(value)
            elif save[u'variables'].has_key(value):
                save[u'variables'][args[0]]+=save[u'variables'][value]
            else:
                print 'Error while add',args[1],'to',args[0]
            continue
        #sub F16,1
        if command.startswith(u'#sub '):
            args=split_parameter(command,u'#sub ')
            if not save[u'variables'].has_key(args[0]):
                print "No variable",args[0],'to sub,create it.'
                save[u'variables'][args[0]]=0
            value=del_blank(args[1])
            if value.isdigit():
                save[u'variables'][args[0]]-=int(value)
            elif save[u'variables'].has_key(value):
                save[u'variables'][args[0]]-=save[u'variables'][value]
            else:
                print 'Error while sub',args[1],'to',args[0]
            continue
        #if F11=0, goto HO01_0
        if command.startswith(u'#if '):
            args=split_parameter(command,u'#if ')
            if check_expression(del_blank(args[0])):
                jump_to_label(del_blank(args[1])[5:])
            continue
        #goto IF_LABEL_2_END
        if command.startswith(u'#goto '):
            args=split_parameter(command,u'#goto ')
            jump_to_label(args[0])
            continue
        #MOV_PLY MOV_OP03
        if command.startswith(u'#MOV_PLY '):
            args=split_parameter(command,u'#MOV_PLY ')
            PlayMovie(args[0])
            continue
        #TITLE
        if command.startswith(u'#TITLE '):
            args=split_parameter(command,u'#TITLE ')
            save[u'title']=args[0]
            continue
        #TITLE_DSP
        if command.startswith(u'#TITLE_DSP'):
            ShowTitle()
            continue
        #SCR_CALEN EYE_D
        if command.startswith(u'#SCR_CALEN '):
            ShowCalender(command[11:],(70,42))
            continue
        #WAIT 90
        if command.startswith(u'#WAIT '):
            wait(float(del_blank(command[6:]))*1000.0/70.0)
            continue
        #waittime 240
        if command.startswith(u'#waittime '):
            delay_until(int(del_blank(command[10:])))
            continue
        #EXT_CALL KAO
        if command.startswith(u'#EXT_CALL '):
            push_call_stack()
            change_script(del_blank(command[10:]))
            continue
        #;	RET
        if command.startswith(u';\tRET') or command.startswith(u';\t\tRET'):
            if len(save[u'callstack'])>0:
                args=pop_call_stack()
                change_script(args[0])
                jump_to_line(args[1])
            continue
        #WIN_OFF
        if command.startswith(u'#WIN_OFF'):
            CHADisp()
            continue
        #select_text 3,Pure Story,Continue,Exit,10,160,160,240,4099060,0,HINT_NONE
        if command.startswith(u'#select_text '):
            args=split_parameter(command,u'#select_text ')
            selentry=[]
            for i in range(1,int(args[0])+1):
                selentry.append(args[i])
            select_text=SelectText(selentry,
                                   topleft=pos_bg2screen((int(args[i+1])*bgsize[0]/100,int(args[i+2])*bgsize[1]/100)),
                                   bottomright=pos_bg2screen((int(args[i+3])*bgsize[0]/100,int(args[i+4])*bgsize[1]/100)),
                                   textcolor=intstr2color(args[i+5]),init_highlight=int(args[i+6]),hint=args[i+7])
            save[u'variables']['F11']=select_text.select()
            del selentry
            del select_text
            continue
        #select_img 4,button,40,40,var0,40,50,var1,40,60,var2,40,70,var3,1
        if command.startswith(u'#select_img '):
            args=split_parameter(command,u'#select_img ')
            selentry=[]
            varentry=[]
            for i in range(2,3*int(args[0]),3):
                selentry.append(pos_bg2screen((int(args[i])*bgsize[0]/100,int(args[i+1])*bgsize[1]/100)))
                if args[i+2]=='0':
                    varentry.append(False)
                elif save[u'variables'].has_key(args[i+2]):
                    varentry.append(bool(save[u'variables'][args[i+2]]))
                else:
                    varentry.append(True)
            i+=3
            select_img=SelectImg(load_select_image(args[1],len(selentry)),selentry,varentry,int(args[i]))
            save[u'variables']['F11']=select_img.select()
            del selentry
            del select_img
            continue
        #load
        if command.startswith(u'#load'):
            Load()
            continue
        #ALBUM
        if command.startswith(u'#ALBUM'):
            album=Album()
            album.select()
            del album
            continue
        #MUSIC
        if command.startswith(u'#MUSIC'):
            music=Musicbox()
            music.select()
            del music
            continue

def ScriptParsePYMO():
    global f,save,cache,cache_pos,withname,gameconfig,running, bgsize, in_fade_out,staticimg,final_img
    while running:
        line=f.readline()
        save[u'linenum']+=1
        try:
            if len(line)==0:
                break
            if len(line)>3 and line[:3] == codecs.BOM_UTF8:
                command=del_blank(line[3:].decode('utf8'))
            else:
                command=del_blank(line.decode('utf8'))
            #change  
            if command.startswith(u'#change '):
                change_script(del_blank(command[8:]))
                continue
            #bg
            if command.startswith(u'#bg '):
                args=split_parameter(command,u'#bg ')
                if len(args)==1:
                    args.append(u'BG_ALPHA')
                    args.append(u'300')
                if len(args)==3:
                    args.append(u'0')
                    args.append(u'0')
                if args[0].startswith(gameconfig[u'cgprefix']):
                    SetEVFlag(args[0])
                BGLoad(0,args[0],(int(args[3]),int(args[4])))
                BGDisp(0,transition=args[1], speed=args[2])
                CHASetInvisible(u'a')
                continue
            #scroll B34a,0,0,100,0,10000
            if command.startswith(u'#scroll '):
                args=split_parameter(command,u'#scroll ')
                SCROLL(int(args[5]),args[0],startpos=(int(args[1]),int(args[2])),endpos=(int(args[3]),int(args[4])))
                if args[0].startswith(gameconfig[u'cgprefix']):
                    SetEVFlag(args[0])
                continue
            #flash #FF0000,1000
            if command.startswith(u'#flash '):
                args=split_parameter(command,u'#flash ')
                if len(args)==1:
                    args.append(u'0')
                Flush(args[0],int(args[1]))
                continue
            #fade_out #000000,1000
            if command.startswith(u'#fade_out '):
                args=split_parameter(command,u'#fade_out ')
                if len(args)<2:
                    args.append(u'1000')
                FADE(int(args[1]), color=hexstr2color(args[0]))
                continue
            #fade_in 1000
            if command.startswith(u'#fade_in '):
                args=split_parameter(command,u'#fade_in ')
                if args[0].isdigit():
                    FADE(int(args[0]),is_fade_out=False)
                else:
                    FADE(1000,is_fade_out=False)
                continue
            #chara 0,SM02AMA,25,1,1,SN01AMA,75,2,400
            if command.startswith(u'#chara '):
                args=split_parameter(command,u'#chara ')
                for i in range (0,len(args)-1,4):
                    if args[i+1].upper()==u'NULL':
                        CHASetInvisible(args[i])
                        CHAResetPos(args[i])
                    else:
                        CHAload(args[i],args[i+1])
                        CHASetPos(args[i],int(args[i+2])*bgsize[0]/100)
                        CHASetLayer(args[i],int(args[i+3]))
                        CHASetVisible(args[i])
                CHADisp(length=int(args[len(args)-1]))
                continue
            #chara_y 3,0,SM02AMA,25,10,1,1,SN01AMA,75,20,2,400
            if command.startswith(u'#chara_y '):
                args=split_parameter(command,u'#chara_y ')
                for i in range (1,len(args)-1,5):
                    if args[i+1].upper()==u'NULL':
                        CHASetInvisible(args[i])
                        CHAResetPos(args[i])
                    else:
                        if not save[u'chara'].has_key(args[i]):
                            save[u'chara'][args[i]]={}
                        CHAload(args[i],args[i+1])
                        CHASetPos(args[i],int(args[i+2])*bgsize[0]/100,int(args[i+3])*bgsize[1]/100,int(args[0]))
                        CHASetLayer(args[i],int(args[i+4]))
                        CHASetVisible(args[i])
                CHADisp(length=int(args[len(args)-1]))
                continue
            #chara_scroll 5,0,SM02AMA,0,0,50,0,130,1,400
            #chara_scroll 5,0,50,0,400
            if command.startswith(u'#chara_scroll '):
                args=split_parameter(command,u'#chara_scroll ')
                if len(args)==10:
                    if not save[u'chara'].has_key(args[1]):
                        save[u'chara'][args[1]]={}
                    CHAload(args[1],args[2])
                    CHASetLayer(args[1],int(args[8]))
                    CHASetVisible(args[1])
                    CHAScroll(args[1], int(args[9]), (int(args[3])*bgsize[0]/100,int(args[4])*bgsize[1]/100),
                              (int(args[5])*bgsize[0]/100,int(args[6])*bgsize[1]/100), int(args[7]), int(args[0]))
                elif len(args)==5:
                    if save[u'chara'].has_key(args[1]):
                        CHASetVisible(args[1])
                        CHAScroll(args[1], int(args[4]), CHAGetPos(args[1],int(args[0])),
                                  (int(args[2])*bgsize[0]/100,int(args[3])*bgsize[1]/100), 0, int(args[0]))
                continue
            #chara_pos 0,43
            if command.startswith(u'#chara_pos '):
                args=split_parameter(command,u'#chara_pos ')
                if len(args)==2:
                    args.append('0')
                    args.append('5')
                CHASetPos(args[0],int(args[1])*bgsize[0]/100,int(args[2])*bgsize[1]/100,int(args[3]))
                CHADisp(transition=None)
                continue
            #chara_cls
            if command.startswith(u'#chara_cls '):
                args=split_parameter(command,u'#chara_cls ')
                CHASetInvisible(args[0])
                CHAResetPos(args[0])
                if len(args)<2:
                    CHADisp()
                else:
                    CHADisp(length=int(args[1]))
                continue
            #chara_quake 0,1
            if command.startswith(u'#chara_quake '):
                args=split_parameter(command,u'#chara_quake ')
                CHAQuake(args,[(-10,3),(10,3),(-6,2),(5,2),(-4,1),(3,0),(-1,0),(0,0)])
                continue
            #chara_down 0,1
            if command.startswith(u'#chara_down '):
                args=split_parameter(command,u'#chara_down ')
                CHAQuake(args,[(0,7),(0,16),(0,12),(0,16),(0,7),(0,0)])
                continue
            #chara_up 0,1
            if command.startswith(u'#chara_up '):
                args=split_parameter(command,u'#chara_up ')
                CHAQuake(args,[(0,-16),(0,0),(0,-6),(0,0)])
                continue
            #chara_anime 0,1
            if command.startswith(u'#chara_anime '):
                args=split_parameter(command,u'#chara_anime ')
                offsets=[]
                j=int(args[2])
                while j>0:
                    for i in range (3,len(args),2):
                        offsets.append((int(args[i]),int(args[i+1])))
                    j-=1
                CHAQuake([args[0]],offsets,int(args[1]))
                continue
            #quake
            if command.startswith(u'#quake'):
                QUAKE()
                continue 
            #vo ME01022
            if command.startswith(u'#vo '):
                args=split_parameter(command,u'#vo ')
                VO_STA(args[0])
                continue
            #bgm BGM15,1
            if command.startswith(u'#bgm '):
                args=split_parameter(command,u'#bgm ')
                if len(args)>1:
                    if args[1].isdigit() and int(args[1])==0:
                        BGMPlay(args[0],1)
                        continue
                BGMPlay(args[0])
                continue
            #bgm_stop
            if command.startswith(u'#bgm_stop'):
                BGMStop()
                continue
            #se SE00_16,1
            if command.startswith(u'#se '):
                args=split_parameter(command,u'#se ')
                if len(args)>1:
                    if args[1].isdigit() and int(args[1])==1:
                        SE_STA(args[0],times=KMdaRepeatForever)
                        continue
                SE_STA(args[0])
                continue
            #se_stop
            if command.startswith(u'#se_stop'):
                SE_STP()
                continue
            #say
            if command.startswith(u'#say '):
                args=split_parameter(command,u'#say ')
                if len(args)==1:
                    message(args[0])
                else:
                    message(args[1],name=args[0])
                continue
            #text string,0,50,#FF0000,16
            #text string,0,50,100,100,#FF0000,16,0
            if command.startswith(u'#text '):
                args=split_parameter(command,u'#text ')
                if save[u'variables'].has_key(args[0]):
                    args[0]=str(save[u'variables'][args[0]]).decode('utf8')
                if len(args)==5:
                    ShowText(args[0],(int(args[1])*screensize[0]/100,int(args[2])*screensize[1]/100),bgsize,hexstr2color(args[3]),int(args[4]),True)
                elif len(args)==8:
                    ShowText(args[0],(int(args[1])*screensize[0]/100,int(args[2])*screensize[1]/100),(int(args[3])*screensize[0]/100,int(args[4])*screensize[1]/100),hexstr2color(args[5]),int(args[6]),bool(int(args[7])))
                continue
            #text_off
            if command.startswith(u'#text_off'):
                OffText()
                CHADisp()
                continue
            #waitkey
            if command.startswith(u'#waitkey'):
                waitkey()
                continue
            #sel 2,HINT_NONE
            if command.startswith(u'#sel '):
                args=split_parameter(command,u'#sel ')
                if len(args)==1:
                    args.append(u'HINT_NONE')
                i=int(args[0])
                choices=[]
                while i>0:
                    line=f.readline()
                    save[u'linenum']+=1
                    if len(line)==0:
                        break
                    choices.append(del_blank(line.decode('utf8')))
                    i-=1
                save[u'variables']['FSEL']=Select(choices,args[1])
                continue
            #set F58,1
            if command.startswith(u'#set '):
                args=split_parameter(command,u'#set ')
                value=args[1]
                if value.isdigit():
                    save[u'variables'][args[0]]=int(value)
                elif save[u'variables'].has_key(value):
                    save[u'variables'][args[0]]=save[u'variables'][value]
                else:
                    save[u'variables'][args[0]]=0
                continue
            #add F11,S1
            if command.startswith(u'#add '):
                args=split_parameter(command,u'#add ')
                if not save[u'variables'].has_key(args[0]):
                    print "No variable",args[0],'to add,create it.'
                    save[u'variables'][args[0]]=0
                value=args[1]
                if value.isdigit():
                    save[u'variables'][args[0]]+=int(value)
                elif save[u'variables'].has_key(value):
                    save[u'variables'][args[0]]+=save[u'variables'][value]
                else:
                    print 'Error while add',args[1],'to',args[0]
                continue
            #sub F16,1
            if command.startswith(u'#sub '):
                args=split_parameter(command,u'#sub ')
                if not save[u'variables'].has_key(args[0]):
                    print "No variable",args[0],'to sub,create it.'
                    save[u'variables'][args[0]]=0
                value=args[1]
                if value.isdigit():
                    save[u'variables'][args[0]]-=int(value)
                elif save[u'variables'].has_key(value):
                    save[u'variables'][args[0]]-=save[u'variables'][value]
                else:
                    print 'Error while sub',args[1],'to',args[0]
                continue
            #rand F11,0,3
            if command.startswith(u'#rand '):
                args=split_parameter(command,u'#rand ')
                save[u'variables'][args[0]]=random.randint(int(args[1]), int(args[2]))
            #if F11=0, goto HO01_0
            if command.startswith(u'#if '):
                args=split_parameter(command,u'#if ')
                if check_expression(args[0]):
                    jump_to_label(del_blank(args[1][5:]))
                continue
            #goto IF_LABEL_2_END
            if command.startswith(u'#goto '):
                args=split_parameter(command,u'#goto ')
                jump_to_label(del_blank(args[0]))
                continue
            #movie MOV_OP03
            if command.startswith(u'#movie '):
                args=split_parameter(command,u'#movie ')
                PlayMovie(args[0])
                continue
            #TITLE
            if command.startswith(u'#title '):
                save[u'title']=del_blank(command[7:])
                continue
            #TITLE_DSP
            if command.startswith(u'#title_dsp'):
                ShowTitle()
                continue
            #date EYE_D,65,42,#000000
            if command.startswith(u'#date '):
                args=split_parameter(command,u'#date ')
                ShowCalender(args[0],(int(args[1]),int(args[2])),color=hexstr2color(args[3]))
                continue
            #wait 1000
            if command.startswith(u'#wait '):
                wait(float(del_blank(command[6:])))
                continue
            #wait_se
            if command.startswith(u'#wait_se'):
                SE_WAIT()
                continue
            #call KAO
            if command.startswith(u'#call '):
                args=split_parameter(command,u'#call ')
                push_call_stack()
                change_script(args[0])
                continue
            #ret
            if command.startswith(u'#ret'):
                if len(save[u'callstack'])>0:
                    args=pop_call_stack()
                    change_script(args[0])
                    jump_to_line(args[1])
                continue
            #select_text 3,Pure Story,Continue,Exit,10,160,160,240,#409900,0
            if command.startswith(u'#select_text '):
                args=split_parameter(command,u'#select_text ')
                selentry=[]
                for i in range(1,int(args[0])+1):
                    selentry.append(args[i])
                select_text=SelectText(selentry,
                                       topleft=pos_bg2screen((int(args[i+1])*bgsize[0]/100,int(args[i+2])*bgsize[1]/100)),
                                       bottomright=pos_bg2screen((int(args[i+3])*bgsize[0]/100,int(args[i+4])*bgsize[1]/100)),
                                       textcolor=hexstr2color(args[i+5]),init_highlight=int(args[i+6]),hint=u'HINT_NONE')
                save[u'variables']['FSEL']=select_text.select()
                del selentry
                del select_text
                continue
            #select_var 3,Pure Story,var1,Continue,var2,Exit,1,10,160,160,240,#409900,0
            if command.startswith(u'#select_var '):
                args=split_parameter(command,u'#select_var ')
                selentry=[]
                varentry=[]
                for i in range(1,2*int(args[0]),2):
                    selentry.append(args[i])
                    if args[i+1]=='0':
                        varentry.append(False)
                    elif save[u'variables'].has_key(args[i+1]):
                        varentry.append(bool(save[u'variables'][args[i+1]]))
                    else:
                        varentry.append(True)
                i+=1
                select_text=SelectText(selentry,
                                       topleft=pos_bg2screen((int(args[i+1])*bgsize[0]/100,int(args[i+2])*bgsize[1]/100)),
                                       bottomright=pos_bg2screen((int(args[i+3])*bgsize[0]/100,int(args[i+4])*bgsize[1]/100)),
                                       textcolor=hexstr2color(args[i+5]),init_highlight=int(args[i+6]),hint=u'HINT_NONE',varlist=varentry)
                save[u'variables']['FSEL']=select_text.select()
                del selentry
                del select_text
                continue
            #select_img 4,button,40,40,var0,40,50,var1,40,60,var2,40,70,var3,1
            if command.startswith(u'#select_img '):
                args=split_parameter(command,u'#select_img ')
                selentry=[]
                varentry=[]
                for i in range(2,3*int(args[0]),3):
                    selentry.append(pos_bg2screen((int(args[i])*bgsize[0]/100,int(args[i+1])*bgsize[1]/100)))
                    if args[i+2].isdigit():
                        if int(args[i+2])==0:
                            varentry.append(False)
                        else:
                            varentry.append(True)
                    elif save[u'variables'].has_key(args[i+2]):
                        varentry.append(bool(save[u'variables'][args[i+2]]))
                    else:
                        varentry.append(False)
                i+=3
                select_img=SelectImg(load_select_image(args[1],len(selentry)),selentry,varentry,int(args[i]))
                save[u'variables']['FSEL']=select_img.select()
                del selentry
                del select_img
                continue
            #select_imgs 4,button0,40,40,var0,button1,40,50,var1,button2,40,60,var2,1
            if command.startswith(u'#select_imgs '):
                args=split_parameter(command,u'#select_imgs ')
                filenameentry=[]
                selentry=[]
                varentry=[]
                for i in range(1,4*int(args[0]),4):
                    filenameentry.append(args[i])
                    selentry.append(pos_bg2screen((int(args[i+1])*bgsize[0]/100,int(args[i+2])*bgsize[1]/100)))
                    if args[i+3].isdigit():
                        if int(args[i+3])==0:
                            varentry.append(False)
                        else:
                            varentry.append(True)
                    elif save[u'variables'].has_key(args[i+3]):
                        varentry.append(bool(save[u'variables'][args[i+3]]))
                    else:
                        varentry.append(False)
                i+=4
                select_img=SelectImg(load_select_images(filenameentry),selentry,varentry,int(args[i]))
                save[u'variables']['FSEL']=select_img.select()
                del selentry
                del select_img
                continue
            #load
            if command.startswith(u'#load'):
                args=split_parameter(command,u'#load')
                if len(args)>0 and args[0].isdigit():
                    globalsave[u'latestsave']=int(args[0])
                    load_index(globalsave[u'latestsave'])
                else:
                    Load()
                continue
            #config
            if command.startswith(u'#config'):
                staticimg['tempimg'].blit(final_img,(0,0))
                ConfigForm()
                final_img.blit(staticimg['tempimg'],(0,0))
                continue
            #ablum
            if command.startswith(u'#album'):
                args=split_parameter(command,u'#album')
                if len(args)>0 and len(args[0])>0:
                    album=Album(args[0],args[0])
                else:
                    album=Album()
                album.select()
                del album
                continue
            #music
            if command.startswith(u'#music'):
                music=Musicbox()
                music.select()
                del music
                continue
            #textbox message2,name2
            if command.startswith(u'#textbox '):
                args=split_parameter(command,u'#textbox ')
                change_message_box(args[0],args[1])
                continue
            #anime_on 3,rain,10,10,300,1
            if command.startswith(u'#anime_on '):
                args=split_parameter(command,u'#anime_on ')
                anime.on(args[1],int(args[0]),pos_bg2screen_x(int(args[2])*bgsize[0]/100),pos_bg2screen_y(int(args[3])*bgsize[1]/100),int(args[4]),bool(int(args[5])))
                continue
            #anime_off rain
            if command.startswith(u'#anime_off '):
                anime.off()
                continue
        except:
            if gameconfig[u'platform']=='pygame':
                if android:
                    error_log(traceback.format_exc())
                else:
                    error_log(traceback.format_exc())
                    traceback.print_exc()
                if query(stringres[u'ERROR'],
                      stringres[u'SCRIPT_ERROR_1']+os.path.basename(f.name)+stringres[u'SCRIPT_ERROR_2']+str(save[u'linenum'])+stringres[u'SCRIPT_ERROR_6'],
                      [stringres[u'YES'],stringres[u'NO']])==1:
                    sys.exit(1)
            else:
                traceback.print_exc()
                if not appuifw.query(stringres[u'SCRIPT_ERROR_1']+os.path.basename(f.name)+stringres[u'SCRIPT_ERROR_2']+str(save[u'linenum'])+stringres[u'SCRIPT_ERROR_6'],'query'):
                    sys.exit(1)

#Following is main function

def main(platform='android'):
    global scalemode,scaleratio,keyboard,canvas,screensize,bgsize,final_img,staticimg,running,globalconfig,gameconfig,gameconfigbak,save,GAME_PATH,LOG_PATH,chara_on,f,sfx,bgmloop,bgmstart,vo,chara,cache,cache_pos,withname,in_fade_out,auto_play,fade_out_color,messagelog,vopakfile,voindex,seindex,sepakfile,bgpakfile,bgindex,charapakfile,charaindex,autosave,anime,quitbind,background,stringres
    final_img=None
    staticimg={'keypad':None}
    background=False
    sfx={'channelid':None,'loop':False,'filename':'','repeattime':0}
    bgmloop=False
    bgmstart=time.clock()
    vo=None
    f=None
    quitbind=True
    autosave=0
    engineversion=1.0
    gameconfig={u'font':1,u'fontaa':1,u'grayselected':1,u'hint':1,u'textspeed':3,u'textcolor':(255,255,255),u'cgprefix':u'EV_',u'vovolume':0,u'bgmvolume':0,u'msgtb':(6,0),u'msglr':(10,7),u'anime':1,u'platform':'pygame'}
    gameconfigbak={}
    GAME_PATH=None
    RES_PATH=u''
    #find LOG_PATH
    paths=os.getcwd()
    LOG_PATH=os.path.join(paths,'pymo.log')
    if android:
        platform='android'
    try:
        pygame.init()
        pygame.display.init()
        #setup window property
        globalconfig=read_global_config('globalconfig.txt')
        if platform=='android':
            scalemode=2
            displayinfo=pygame.display.Info()
            screensize=(displayinfo.current_w,displayinfo.current_h)
            canvas = pygame.display.set_mode(screensize)
        elif platform=='windows' or platform=='linux' or platform=='macos':
            scalemode=2
            screensize=(593,360)
            canvas = pygame.display.set_mode(screensize,pygame.HWSURFACE)
            pygame.display.set_caption('pymo '+str(engineversion)+' by chen_xin_ming')
        elif platform=='maemo' or platform=='meego':
            scalemode=1
            screensize=(800,480)
            canvas = pygame.display.set_mode(screensize,pygame.FULLSCREEN|pygame.HWSURFACE)
        stringres=load_string_res('stringres.txt')
        load_keypad()
        keypadsize = staticimg['keypad'].get_size()
        if globalconfig['keypad_bottom']==0:
            screensize=(screensize[0]-keypadsize[0],screensize[1])
        else:
            screensize=(screensize[0],screensize[1]-keypadsize[1])
        final_img=pygame.Surface(screensize)
        scaleratio=(screensize[1],360)
        gameconfig[u'fontsize']=20*scaleratio[0]/scaleratio[1]
        # Map the back button to the escape key.
        if platform=='android':
            android.init()
            android.map_key(android.KEYCODE_BACK, pygame.K_ESCAPE)
            android.map_key(android.KEYCODE_MENU, pygame.K_0)
        staticimg['bg_img']=pygame.Surface(screensize)
        staticimg['chara_img']=pygame.Surface(screensize)
        staticimg['oldimg']=pygame.Surface(screensize)
        staticimg['tempimg']=pygame.Surface(screensize)
        staticimg['paragraph_img']=pygame.Surface(screensize,flags=pygame.SRCALPHA)
        pygame.display.flip()
        pygame.display.flip()

        #detect folders containing games
        error_log(u'Game Start: Searching for Games...')
        anime=Animation()
        running=False
        save={u'linenum':0,u'chara':{},u'variables':{},u'callstack':[],u'msgbox':u'message',u'namebox':u'name',u'bgpercentorig':(0,0)}
        set_font()
        keyboard=Keyboard()
        # ####################
        # if on android, use android launcher, else use pymo launcher
        # ####################
        if platform=='android':
            GAME_PATH=globalconfig['last_path']
        else:
            gamelist=[]
            gametextlist=[]
            gameiconlist=[]
            for root, dirs, files in os.walk(paths):
                for filename in files:
                    if filename.lower()=='gameconfig.txt':
                        try:
                            game_info=read_game_info(root)
                            gamelist.append(game_info[0])
                            gametextlist.append(game_info[1])
                            gameiconlist.append(load_image(os.path.join(game_info[0],'icon.png'),is_alpha=True, imgtype='bg'))
                        except:
                            query(stringres[u'WARNING'],os.path.join(root, filename)+stringres[u'IS_BROKEN'],[stringres[u'OK']])
                            error_log("Warning: "+os.path.join(root, filename)+' is corrupted!')
            if len(gamelist)<1:
                if android:
                    query(stringres[u'ERROR'],stringres[u'GAME_NOTFOUND_ANDROID'],[stringres[u'OK']])
                else:
                    query(stringres[u'ERROR'],stringres[u'GAME_NOTFOUND'],[stringres[u'OK']])
                error_log('Error: No game found! Exit...')
                return
    
            #display game launcher to select a game
            gamelauncher=SelectList(gametextlist,iconlist=gameiconlist)
            gameid=gamelauncher.select()
            if gameid==-1:
                pygame.quit()
                return
            del gameiconlist
            del gametextlist
            del gamelauncher
            GAME_PATH=gamelist[gameid]
        #read the selected game config
        try:
            read_game_config(GAME_PATH)
        except:
            query(stringres[u'ERROR'],gamelist[gameid]+'/gameconfig.txt '+stringres[u'IS_BROKEN'],[stringres[u'OK']])
            error_log("Error: "+ gamelist[gameid]+'/gameconfig.txt '+'is corrupted')
            pygame.quit()
            return
        #remove the log file in SD card's root dir
        try:
            os.remove(LOG_PATH)
        except:
            pass
        LOG_PATH=os.path.join(GAME_PATH,'pymo.log')
        #see if game folder allows write
        try:
            tempfile=file(LOG_PATH,'w')
            tempfile.close()
        except IOError:
            query(stringres[u'WARNING'],stringres[u'READ_ONLY'],[stringres[u'OK']])
        chara_on=False
        if gameconfig.has_key(u'engineversion'):
            if float(gameconfig[u'engineversion'])>engineversion:
                query(stringres[u'ERROR'],stringres[u'VERSION_LOW_1']+gameconfig[u'engineversion']+stringres[u'VERSION_LOW_2'],[stringres[u'OK']])
                error_log( 'Please use pymo '+gameconfig[u'engineversion']+' or higher version')
                pygame.quit()
                return
        if gameconfig.has_key(u'platform'):
            if gameconfig[u'platform']==u's60v3':
                if query(stringres[u'WARNING'],stringres[u'PLATFORM_ERROR_V3'],[stringres[u'YES'],stringres[u'NO']])==1:
                    pygame.quit()
                    return
            elif gameconfig[u'platform']==u's60v5':
                if query(stringres[u'WARNING'],stringres[u'PLATFORM_ERROR_V5'],[stringres[u'YES'],stringres[u'NO']])==1:
                    pygame.quit()
                    return
        if platform=='android':
            for folder in ['bg','bgm','chara','se','system','voice','save','video']:
                create_nomedia(folder)
            load_keypad()
            keypadsize = staticimg['keypad'].get_size()
            if globalconfig['keypad_bottom']==0:
                screensize=(displayinfo.current_w-keypadsize[0],displayinfo.current_h)
            else:
                screensize=(displayinfo.current_w,displayinfo.current_h-keypadsize[1])
        elif platform=='windows' or platform=='linux' or platform=='macos':
            screensize = gameconfig[u'imagesize']
        if platform=='android' or platform=='windows' or platform=='linux' or platform=='macos':
            final_img=pygame.Surface(screensize)
            staticimg['bg_img']=pygame.Surface(screensize)
            staticimg['chara_img']=pygame.Surface(screensize)
            staticimg['oldimg']=pygame.Surface(screensize)
            staticimg['tempimg']=pygame.Surface(screensize)
            staticimg['paragraph_img']=pygame.Surface(screensize,flags=pygame.SRCALPHA)
            load_keypad()
            keypadsize = staticimg['keypad'].get_size()
            if globalconfig['keypad_bottom']==0:
                canvas = pygame.display.set_mode((screensize[0]+keypadsize[0],screensize[1]))
            else:
                canvas = pygame.display.set_mode((screensize[0],screensize[1]+keypadsize[1]))
            keyboard=Keyboard()
            anime=Animation()
        modify_game_config(True)
        chara_on=False
        f=None
        chara={}
        cache={'bg':{},'chara':{},'vo':{},'bgm':{},'sel':None}
        cache_pos=0
        messagelog=[]
        withname=False
        running=True
        in_fade_out=False
        auto_play=False
        fade_out_color=(255,255,255)

        set_font()
        load_global()
        if screensize[1]*gameconfig[u'imagesize'][0]/gameconfig[u'imagesize'][1]>=screensize[0]:
            #image is wider than screen, fit height
            scaleratio=(screensize[1],gameconfig[u'imagesize'][1])
            bgsize=(gameconfig[u'imagesize'][0]*screensize[1]/gameconfig[u'imagesize'][1],screensize[1])
        else:
            #screen is wider than image, fit width
            scaleratio=(screensize[0],gameconfig[u'imagesize'][0])
            bgsize=(screensize[0],gameconfig[u'imagesize'][1]*screensize[0]/gameconfig[u'imagesize'][0])
        #if this is the first time that game runs, convert all the filenames to lower case
        #if platform=='linux' or platform=='macos' or platform=='maemo' or platform=='meego':
        #    if not os.path.exists(os.path.join(GAME_PATH,'save','global.sav')):
        #        rename_files(GAME_PATH)
        
        bgpakfile,bgindex=load_pak_file(os.path.join('bg','bg.pak'))
        if platform!='android':
            BGLoad(0,u'logo1')
            BGDisp(0, transition=u'BG_ALPHA', speed=u'BG_NORMAL')
        else:
            BGLoad(0,u'logo2')
            BGDisp(0, transition=u'BG_ALPHA', speed=u'BG_NORMAL')
        Load_system_images()

        charapakfile,charaindex=load_pak_file(os.path.join('chara','chara.pak'))
        sepakfile,seindex=load_pak_file(os.path.join('se','se.pak'))
        if platform!='android':
            BGLoad(0,u'logo2')
            BGDisp(0, transition=u'BG_ALPHA', speed=u'BG_NORMAL')
        vopakfile,voindex=load_pak_file(os.path.join('voice','voice.pak'))
        purge_voice(True)
        f=file(os.path.join(GAME_PATH,'script',gameconfig[u'startscript']+u'.txt'),'r')
        if gameconfig[u'scripttype']==u'mo1':
            ScriptParseMO1()
        if gameconfig[u'scripttype']==u'mo2':
            ScriptParseMO2()
        if gameconfig[u'scripttype']==u'pymo':
            ScriptParsePYMO()
        
        anime.off()
        BGMStop()
        SE_STP()
        f.close()
        try:
            save_global()
            purge_voice(True)
            purge_image(True)
            if vopakfile!=None:
                vopakfile.close()
            os.remove(LOG_PATH)
        except:
            pass
    except:
        if f:
            posisionstr=stringres[u'SCRIPT_ERROR_1']+os.path.basename(f.name)+stringres[u'SCRIPT_ERROR_2']+str(save[u'linenum'])+stringres[u'SCRIPT_ERROR_3']
        else:
            posisionstr=''
        query(stringres[u'ERROR'],posisionstr+stringres[u'SCRIPT_ERROR_4']+LOG_PATH+stringres[u'SCRIPT_ERROR_5'],[stringres[u'OK']])
        if android:
            error_log(traceback.format_exc())
        else:
            error_log(traceback.format_exc())
            traceback.print_exc()
    pygame.quit()
    
if __name__ == "__main__":
    # platform could be windows, linux, macos, android, maemo and meego
    main(platform='windows')
