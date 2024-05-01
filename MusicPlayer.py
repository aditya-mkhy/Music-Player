from threading import Thread
import socket, os, sys

from datetime import datetime
from pathlib import Path



def clientOpen(file):
    conn = socket.socket()
    conn.settimeout(0.1)
    try:
        conn.connect(("localhost", 8099))
        conn.sendall(f"--Play--88564--{file}".encode())
        return 1
    except Exception as e:
        return 0

    finally:
        conn.close()



sendARGV = None
try:
    print(f"Argvs==> {sys.argv}")
    path=sys.argv[1]
    print(f'The Paths==> {path}')
    if os.path.splitext(path)[1] == '.mp3':
        if os.path.exists(path):
            sendARGV = path
            print(f'The Paths open==> {path}')
            if clientOpen(path):
                sys.exit(1)
except Exception as e:
    print(f"E== At args{e}")

from tkinter import Label,Tk,StringVar,Button,Frame,Menu,PhotoImage,Scale,Listbox,Entry,Text,Toplevel,Scrollbar,Canvas
from tkinter.ttk import Style,Progressbar,Scale as ttk_Scale
from tkinter import ttk
import subprocess
from random import choice
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,TIT2,TLEN,TCON,TPE1,TALB,TPUB,WPUB,TDRL,APIC
from tkinter.filedialog import  askdirectory ,askopenfilenames
from tkinter import messagebox
from json import loads
from ctypes import windll
from youtubesearchpython import VideosSearch ,ResultMode#pip install youtube-search-python
from PIL import ImageTk, Image
from requests import get as requests_get
from tkinter.colorchooser import askcolor
from time import ctime,sleep,time
from cryptography.fernet import Fernet
from functools import partial as functools_partial
from webbrowser import open as open_file
import pyaudio
import io as io_import
from tkinter.ttk import Style as ttk_Style,Progressbar, Scale as ttk_Scale
from pytube import YouTube , Playlist
import json







def resource_path(relative_path):
    path=os.path.dirname(sys.executable)    
    return path+'/'+relative_path

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class DataBabse(dict):
    def __init__(self) -> None:

        self.file_name = "data/db.music"
        self.path = resource_path(self.file_name)

        self.load()


    def read(self):
        with open(self.path, "r") as ff:
            try:
                return json.loads(ff.read())
            except:
                print("Invalid Json")
                self.init_schema()


    def load(self):
        self.update(self.read())

    def write(self, data):
        with open(self.path, "w") as tf:
            tf.write(json.dumps(data))

    def commit(self):
        self.write(self)

    def init_schema(self):
        self.schema = {
            "repeat" : "all", # rep_song_val
            "vol" : 50, #volume
            "current" : 0, #playingsongindex__
            "added" : [], #added_song
            "playlist" : {
                "Downloads" : [],
            }, #playist__directory
            "recent" : [], #recent_song_plays_list
            "show" : "no", #recent_song_plays_list
        }

        self.write(self.schema)
        self.load()



class ServerMusic:
    def __init__(self) -> bool:
        self.host = "localhost"
        self.port = 8099    

    def recving(self, conn, addr):
        print("Got_ConnectionFrom ==>", addr)
        data = conn.recv(1024).decode()
        conn.close()
        #--Play--88564--c:/sms/sf.mp3
        if "--Play--88564--" in data:
            file = data.replace("--Play--88564--", "")
            print("File ==> ", file)
            if os.path.exists(file):
                global songlist, playingsongindex__
                try:
                    index = songlist.index(file)
                except Exception as e:
                    print("Errpr90",e)
                    add_song_to_songlist(file)

                    try:
                        index = songlist.index(file)
                    except Exception as e:
                        print("Errpr900",e)
                        index = None
                        
                if index != None:
                    playingsongindex__ = index
                    mixer.music.stop()
                    play_music(file)
                else:
                    print("Erroor9090")
            else:
                print("File Not Found..")
        else:
            print("Error in Data...")


    def Server(self):
        print("@@__Starting__Server__@@")
        self.network = socket.socket()
        self.network.bind((self.host, self.port))
        self.network.listen(100)
        try:
            while True:
                try:
                    conn, addr = self.network.accept()
                    Thread(target=self.recving,  args=(conn, addr), daemon=True).start()

                except socket.timeout:
                    print("----@--> Time OUT")
                    
                except KeyboardInterrupt:
                    print("--KeyboardInterrupt Deceted.. Stoping Server---")
                    try:
                        self.network.shutdown(1)
                    except:
                        pass
                    self.network.close()
                    exit()
                    
        except KeyboardInterrupt:
            print("KeyboardInterrupt Deceted.. Stoping Server")
            try:
                self.network.shutdown(1)
            except:
                pass
            self.network.close()


 

def addsong_crtl_f(event=None):# add song form a folder
    path=askdirectory(title='Open_folder_to_add_music_to_playlist')
    print(path)
    add_song_to_songlist(path)

def add_song_to_songlist(path):
    def add_song_to_playlist(path):
        global songlist ,totalsonginlist__ 
        songlist.append(path)
        name=os.path.basename(path)
        srch_songlist.append(name)
        src_listbox.insert('end',name)
        listbox.insert('end',(name))        
        if totalsonginlist__ % 2 == 0:
            listbox.itemconfig(totalsonginlist__, background='grey20', fg='white')
            src_listbox.itemconfig(totalsonginlist__, background='grey20', fg='white')
        totalsonginlist__+=1
    if os.path.exists(path):
        if os.path.isfile(path):
            if path.endswith(".mp3"):
                add_song_to_playlist(path)            
        elif os.path.isdir(path):
            for file_path in os.listdir(path):
                if file_path.endswith(".mp3"):
                    full_path=path+'\\'+file_path
                    add_song_to_playlist(full_path)

    
def check_song_in_songlist(file):
    global songlist ,totalsonginlist__ , playingsongindex__
    rt='no'
    file_name=os.path.basename(file)
    
    n=0    
    for path in songlist:
        path=os.path.basename(path)
        if path == file_name:            
            rt=n 
            break
        else:
            n+=1
    return rt
                   
def add_1_song_plist(event=None,path=None):
    path_a=path
    if path_a ==None:
        path_a=askopenfilenames(title = "Select_music_file",filetypes = (("Music Files", "*.mp3"),))
    else:
        pass
    number_of_song=0
    for path in path_a:
        if os.path.exists(path):
            number_of_song+=1
    n__=0
    for path in path_a:
        print(path)
        if os.path.exists(path) :
            n__+=1
            index=check_song_in_songlist(path)
            global totalsonginlist__ , playingsongindex__ ,songlist ,rep_song_val
            if index == 'no':
                try:
                    add_song_to_songlist(path)
                    if event != None and event != "argv":
                        global added_song
                        added_song.append(path)
                        print('added_song___________________')

                    if  n__ ==number_of_song:
                        if event =='argv':
                            c='yes'
                        else:
                            c=messagebox.askquestion(title='Play Song !',
                                            message='Song Added in playlist\n Do you want to play it')
                        if c =='yes':                        
                            index =len(songlist)-1
                            print('lengtegth_of_list==',index+1)
                            playingsongindex__=index
                            
                            play_music(songlist[index])
                            listbox.see(index)
                        else:
                            pass
                        pass
                    
                    else:
                        pass
                        
     
                except Exception as e:
                    print(e)                    
                    messagebox.showerror(title=' Error !',
                                    message='An error occured during playing song\n      please choose another one \n          or try again')
            else:
                if event =='argv':
                    c='yes'
                else:
                    c=messagebox.askquestion(title='Play Song !',
                                message='This File is Already exist in playlist\n Do you want to play it')
                
                    
                if c =='yes':

                    playingsongindex__=index
                    listbox.see(index)
                    play_music(songlist[index])
                else:
                    pass
            
            

        
        else:
            if os.path.exists(path):
                print('True________++++++++++++++++++++++++++++++')
            else:
                print('not_exista____')
            if path =='':
                pass
            else:
                
                messagebox.showerror(title=' Error !',
                                    message='Someting went wrong, \n Please try again ')
                
        
def stop_music(event=None):
    global stopButton
    stopButton = True
    mixer.music.stop()

def left_key_comm(event=None):
    v=v_scale.get()
    v_scale.set(v-2)
    return "break"

def right_key_comm(event=None):
    v=v_scale.get()
    v_scale.set(v+2)
    return "break"

def inc_dec_volume(value):    
    def remove_icon(v):
        if v==1:
            vol70_but.grid_remove()
            vol100_but.grid_remove()
            vol20_but.grid()
        elif v==2:
            vol20_but.grid_remove()
            vol100_but.grid_remove()
            vol70_but.grid()
        elif v==3:
            vol20_but.grid_remove()
            vol70_but.grid_remove()
            vol100_but.grid()
        else:
            pass
        global volume_icon
        
        volume_icon=v
    global volume , volume_icon
    volume=int(value.split('.')[0])
    if volume == 0:
        volume_icon=0
        mute()
    elif volume <= 30:
        if volume_icon == 1:
            pass
        else:
            remove_icon(1)
    elif volume >= 30 and volume <= 70 :
        if volume_icon == 2:
            pass
        else:
            remove_icon(2)
    elif volume >= 70 :
        if volume_icon == 3:
            pass
        else:
            remove_icon(3)
    else:
        pass
    mixer.music.set_volume(volume/100)
    volume_information.configure(text=(str(volume)+' %'))

    
def p_key_pause(event=None):
    global play_pause_val
    if  play_pause_val == 'unpause':
        pause_song()
    elif play_pause_val == 'pause':
        unpause_song()
    else:
        pass
            
def unpause_song(event=None):
    global pauseButtonStatus, play_pause_val
    play_pause_val='unpause'
    play_but.grid_remove()
    pause_but.grid()
    if event != 'ch':
        if mixer.music.get_busy() == 0:
            if not pauseButtonStatus:
                play_music_start()
    else:
        pass
    mixer.music.unpause()
    pauseButtonStatus = False
    try:
        global pause_butd ,play_butd 
        play_butd.grid_remove()
        pause_butd.grid()
    
    except:
        pass
    
def pause_song(event=None):
    global pauseButtonStatus, play_pause_val
    pause_but.grid_remove()
    play_but.grid()
    global play_pause_val
    play_pause_val='pause'
    pauseButtonStatus = True
    mixer.music.pause()
    try:
        global pause_butd ,play_butd        
        pause_butd.grid_remove()
        play_butd.grid()
    except:
        pass
    
def previous_song(event=None):
    mixer.music.stop()
    global songlist , totalsonginlist__ , playingsongindex__  , rep_song_val
    if totalsonginlist__ == 0:
        print('playlist is empty')
    else:
        if playingsongindex__ == 0:
            index=len(songlist)-1
        else:
            index=playingsongindex__ - 1
            
        path=songlist[index]
        playingsongindex__=index
        play_music(path)    
    
def next_song(event=None):
    mixer.music.stop()
    
    global songlist ,totalsonginlist__ , playingsongindex__   ,rep_song_val
    
    if totalsonginlist__ == 0:
        print('playlist is empty')
    else:            
        if  (totalsonginlist__ -1) == playingsongindex__:
            index=0
        else:
            index=playingsongindex__ + 1
        path=songlist[index]
        playingsongindex__=index
        play_music(path)
        
        



def m_key_muteUnmute(event=None):
    m=mixer.music.get_volume()
    if m == 0.0 :
        unmute()
    else:
        mute()
def mute(event=None):
    vol20_but.grid_remove()
    vol70_but.grid_remove()
    vol100_but.grid_remove()
    mute_but.grid()
    volume=v_scale.get()

    mixer.music.set_volume(0.0)
def unmute(event=None):
    global volume
    mute_but.grid_remove()
    if volume==0:
        volume=10
    if volume <= 30:
        vol20_but.grid()
    elif volume > 20 and volume <= 70 :
        vol70_but.grid()
    elif volume > 70:
        vol100_but.grid()
    else:
        pass
    mixer.music.set_volume(volume/100)


def show_hide_paylist(event=None):
    global paylist_state
    if paylist_state=='show':
        listbox.place_forget()
        fram1.pack_forget()
        fram1.pack(side='bottom',fill='x')
        paylist_state='hide'
    elif paylist_state=='hide':
        listbox.place(x=10,y=10)
        fram1.pack_forget()
        fram1.pack(side='bottom',fill='x')
        paylist_state='show'
    else:
        pass

    
def rep_song_all():
    global rep_song_val
    rep_song_val='all'
    rep_song0_but.grid_remove()
    rep_songall_but.grid()    


def rep_song_1():
    global rep_song_val
    rep_song_val='one'
    rep_songall_but.grid_remove()
    rep_song1_but.grid()


def rep_song_0():
    global rep_song_val
    rep_song_val='0'
    rep_song1_but.grid_remove()
    rep_song0_but.grid()


def add_song_to_playlist_onstart(added_song_):
    path=str(Path.home())+'\\Music'
    add_song_to_songlist(path)
    tem_list=[]
    for song in added_song_:
        if os.path.exists(song):
            if song in songlist:
                pass
            else:
                tem_list.append(song)
                add_song_to_songlist(song)
            
        else:
            pass
    global added_song
    added_song=tem_list
    tem_list=None # remove data in tem_list

def play_music(file,msg=None):
    global song_count
    song_count+=1
    mixer.music.stop()
    global playingsongindex__ , deselect_song_v
    if deselect_song_v =='':
        deselect_song_v=playingsongindex__      
    else:
        try:
            if deselect_song_v % 2 == 0 :
                listbox.itemconfig(deselect_song_v,bg='grey20',fg='white',selectbackground='#00ccff')
            else:
                listbox.itemconfig(deselect_song_v,bg='grey15',fg='goldenrod',selectbackground='#00ccff')
            try:
                d=listbox.curselection()
                for a in d:
                    listbox.selection_clear(a, a)
            except:
                pass
        except:
            pass
        
     
    listbox.selection_set(playingsongindex__, playingsongindex__)
    listbox.see(playingsongindex__)
    deselect_song_v=playingsongindex__
    listbox.itemconfig(playingsongindex__,fg='black',bg='#996600',selectbackground='grey80')
    audio=MP3(file)
    global audio_length
    audio_length=audio.info.length
    global channels
    channels=audio.info.channels
    freq=audio.info.sample_rate
    progressbar.config(from_=0,to=audio_length*1000)
    global frequency
    if frequency != freq :
        frequency=freq
        mixer.quit()
        global sound_output_device
        if sound_output_device =='default':
            mixer.init(frequency=freq,channels=channels)
        else:
            try:
                mixer.init(devicename=sound_output_device,frequency=freq,channels=channels)
            except:
                mixer.init(frequency=freq,channels=channels)

                
        global volume
        mixer.music.set_volume(volume/100)
    global playing_file
    mixer.music.load(file)
    playing_file=file
    mixer.music.play()
    t1 = Thread(target=name_slider_thread,args=(audio_length,file,song_count,),daemon = True) 
    t1.start()
    add_cover_image_in_label(file)
    global screen_info_widget,recent_song_plays_list
    
    if file in recent_song_plays_list:
        recent_song_plays_list.remove(file)
        
    recent_song_plays_list.insert(0,file)
    
    if len(recent_song_plays_list) >40:
        recent_song_plays_list.pop()
        
    if screen_info_widget == 'recent_plays':
        global press_paly_buttton
        if press_paly_buttton==False:
            show_recent_song_window()
    save_status_data_in_file()
                
        
def add_cover_image_in_label(file):
    global screen_info_widget ,play_frame_playlist_icon_label
    if  screen_info_widget == 'User_Playlist':
        
        global music_covor_image
        music = ID3(file)
        title=str(music.get("TIT2"))

        author=str(music.get("TPE1"))
        category=str(music.get("TCON"))
        published=str(music.get("TDRL"))

        if title =="None":
            title=os.path.basename(file)
            author="M_A_Music_Payer"
            category=''
            published=''
        
        play_frame_playlist_name_label.config(text=title.replace("_"," "),font=('',22,'bold italic'))
        text=str(author)+"\n"+str(category)+"  .  "+str(published)        
        play_frame_num_song_label.config(text=text,font=('',11,'bold italic'),fg="magenta2")

        global play_gif_status

        if play_gif_status !=True:
            try:
                data=music.getall("APIC")[0].data
                load = Image.open(io_import.BytesIO(data))
                load=load.resize((380,220), Image.Resampling.LANCZOS)
                try:
                    del music_covor_image
                except:
                    pass
                music_covor_image = ImageTk.PhotoImage(load,master=root)            
                play_frame_playlist_icon_label.config(image=music_covor_image,bg='black')
            except:
                play_frame_playlist_icon_label.configure(image=play_frame_playlist_icon)
    else:
        pass
        

        
def play_looping_song():
    global songlist ,totalsonginlist__ , playingsongindex__   ,rep_song_val, stopButton, pauseButtonStatus
    if stopButton:
        stopButton = False
        pauseButtonStatus = False
        
        print("MusicStopped..",pauseButtonStatus)
    else:
        if rep_song_val=='all':
            next_song()
        elif rep_song_val=='one':
            path=songlist[playingsongindex__]
            play_music(path)
        else:
            pass
    
def play_music_start(event=None):
    global songlist   , playingsongindex__
    if totalsonginlist__ == 0:
        print('playlist is empty')
    else:            
        path=songlist[playingsongindex__]
        play_music(path)

def sec_in_mint(sec):
    
    mint=sec//60
    sec=sec-mint*60
    if mint < 10 :
        mint='0'+str(mint)
    else:
        mint=str(mint)
    if sec < 10:
        sec='0'+str(sec)
    else:
        sec=str(sec)

    return (mint+':'+sec)


def name_slider_thread(songlength , name,song_count_thr): 
    global pauseButtonStatus, play_pause_val, song_count, sound_output_device_value
    name , ext=os.path.splitext(os.path.basename(name))
    name=name[:40]
    name_len=len(name)
    con_name=''
    l=0
    songlength=int(songlength)
    end_timeLabel.config(text=sec_in_mint(songlength))
    start_timeLabel.config(text='00:00')
    progressbar.set(0)
    n=0
    unpause_song('ch')
    global sc
    while True:        
        if song_count_thr !=song_count:
            song_count_thr='break'
            break
        if sound_output_device_value==True:
            sleep(0.05)
        else:
            if mixer.music.get_busy() or pauseButtonStatus:
                if play_pause_val=='pause':
                    sleep(0.07)
                else:
                    sleep(0.1)
                    n+=1
                    if n ==  10:
                        n=0
                        v=progressbar.get()
                        start_timeLabel.config(text=sec_in_mint(int((v)//1000)))
                        progressbar.set(v+1000)
                    if n == 0 or n== 2 or n == 4 or n== 6 or n==8:
                        if l == name_len :
                            con_name=''
                            l=0
                        else:
                            con_name=con_name+name[l]
                            l+=1
                            st_but.config(text=con_name)
                            try:
                                sc.title(con_name)
                            except:
                                pass
                        
                    
                
            else:
                break

    if song_count_thr=='break':
        pass
    else:
        pause_song()
        start_timeLabel.config(text='00:00')
        st_but.config(text=name[:14])
        progressbar.set(0)
        play_looping_song()

def listbox_command(event=None):
    index=listbox.curselection()
    index=index[0]
    global songlist ,totalsonginlist__ , playingsongindex__  ,rep_song_val
    path=songlist[int(index)]
    playingsongindex__=index
    play_music(path)


def listbox_xview(column):
    global totalsonginlist__
    if totalsonginlist__ > 13:
        if column <= 12 :
            listbox.yview(0)
        else: 
            index=column-12
            listbox.yview(index)
    else:
        pass


def hide_play_window(event=None):
    global second_screen_show_val
    second_screen_show_val='no'
    global sc
    sc.destroy()

def play_window(event=None):
    global second_screen_show_val
    if second_screen_show_val=='yes':
        print('Value True')
        pass
    else:
        second_screen_show_val=='yes'
        play_window_create()

     
def play_window_create(event=None):
    global sc ,prev_butd_photo,prev_butd ,pause_photod,pause_butd ,pause_butd ,play_butd
    
    def pause_songd(event=None):
        pause_song()            

    def unpause_songd(event=None):
        unpause_song()
    def on_closing_sc():
        global second_screen_show_val
        second_screen_show_val='no'
        global sc
        sc.destroy()


      
    sc=Tk()
    sc.title('M_A_/-Music Player 🎵')
    sc.wm_attributes('-alpha',0.6)
    sc.geometry(('550x72+400+100'))
    sc.resizable(False,False)
    sc.bind('<Key>', on_release)

    sc.wm_attributes('-topmost',True)
    sc.wm_attributes('-transparentcolor', 'brown')
    sc.config(bg='brown')

    prev_butd_photo = PhotoImage(file = resource_path("data/previous.png"),master=sc)
    prev_butd_photo = prev_butd_photo.subsample(2,2)
    prev_butd=Button(sc,bd=0,bg='white',image=prev_butd_photo,activebackground='sky blue',cursor='sb_left_arrow',
                     command=previous_song,height=40,width=40)
    prev_butd.place(x=0,y=10)
    pause_lpd=Label(sc,text='',bg='brown')
    pause_lpd.place(x=250,y=1)
    
    pause_photod = PhotoImage(file = resource_path("data/pause.png"),master=sc)
    pause_photod = pause_photod.subsample(2,2)
    pause_butd=Button(pause_lpd,image=pause_photod,bg='brown',bd=0,activebackground=task_bg,
                      cursor='hand2',command=pause_songd)
    pause_butd.grid(row=0,column=0)
    pause_butd.grid_remove()

    play_photod = PhotoImage(file = resource_path("data/play.png"),master=sc)
    play_photod = play_photod.subsample(2,2)
    play_butd=Button(pause_lpd,bg='brown',image=play_photod,bd=0,activebackground=task_bg,cursor='hand2',
                    command=unpause_songd)
    play_butd.grid(row=0,column=0)
    next_photod = PhotoImage(file = resource_path("data/next.png"),master=sc)
    next_photod = next_photod.subsample(2,2)
    next_butd=Button(sc,bg='white',bd=0,image=next_photod
                     ,activebackground='cyan',cursor='sb_right_arrow',
                     command=next_song,height=40,width=40)
    next_butd.place(x=500,y=10)
    global second_screen_show_val ,play_pause_val
    second_screen_show_val='yes'
    if play_pause_val=='unpause':
        unpause_songd()
    sc.protocol("WM_DELETE_WINDOW", on_closing_sc)
    sc.mainloop()
    return True


def on_closing_root(s=True, again=False):
    if s:
        global rep_song_val
        save_status_data_in_file()
    try:
        mixer.music.stop()
    except:
        pass
    try:
        sc.destroy()
    except:
        pass
    try:
        root.destroy()
    except:
        pass
    if again:
        open_file(sys.argv[0])
    sys.exit(1)


def search_song(event=None):
    text=ent_search_win.get()
    text=((text.lower()).replace('_',' ')).split(' ')
    src_listbox.delete(0,'end')
    n=0
    for i in srch_songlist:
        i_=i.lower()
        l=0
        for words in text:                
            if words in i_:
                l+=1
        if len(text)== l:
            src_listbox.insert('end',i)
            
            if n % 2 == 0:
                src_listbox.itemconfig(n,background='grey20',fg='white')
            n+=1
    try:
        src_listbox.select_set('0')
    except:
        pass
                
        
def enter_search_cmd(event=None):
    song_name=src_listbox.get(0, 0)
    song_name=song_name[0]
    listbox_search_cmd(song_name)
    
def listbox_search_cmd(event=None):
    try:
        if '.mp3' in event:
            song_name=event            
    except:
        index=src_listbox.curselection()
        index=index[0]
        song_name=src_listbox.get(index, index)
        song_name=song_name[0]
    global songlist
    index=''
    file=''
    t=0
    for path in songlist:
        if song_name in path:
            file=path
            index=t
            break
        else:
            pass
        t+=1         
    global playingsongindex__  ,rep_song_val    
    playingsongindex__=index
    play_music(file)
    listbox.yview(index-4)
    
def bind_listbox_key():
    listbox.bind("<p>",previous_song)
    listbox.bind("<m>",m_key_muteUnmute)
    listbox.bind("<r>",unpause_song)
    listbox.bind("<n>",next_song)
    listbox.bind("<b>",previous_song)
    listbox.bind("<s>",stop_music)
    listbox.bind("<space>",p_key_pause)
    listbox.bind("<d>",play_window)
    root.bind("<Key>",on_release)


def unbind_listbox_key():
    listbox.unbind("<p>")
    listbox.unbind("<m>")
    listbox.unbind("<r>")
    listbox.unbind("<n>")
    listbox.unbind("<b>")
    listbox.unbind("<s>")
    listbox.unbind("<t>")
    listbox.unbind("<space>")
    listbox.unbind("<d>")
    root.bind("<Key>",on_release)


def search_Window(event=None):
    global paylist_state
    global search_Window_value
    if search_Window_value=='hide':
        search_Window_value='show'
        paylist_state='none'
        listbox.pack_forget()                
        src_listbox.pack(expand=True,fill='both',padx=0)
        unbind_listbox_key()
        
    elif search_Window_value=='show':
        search_Window_value='hide'
        paylist_state='show'
        src_listbox.pack_forget()
        listbox.pack(expand=True,fill='both',padx=0)
        bind_listbox_key()
        
        
    else:
        pass

def stop__(event=None):
    play_window_create().on_closing_sc()


def popup_menu(event):
    global root 
    popup_menu = Menu(root,bg='white',tearoff = 0,font=('',16))
    global play_pause_val
    if play_pause_val=='pause':
        popup_menu.add_command(label = "Play      ",command = unpause_song)
    elif play_pause_val=='unpause':
        popup_menu.add_command(label = "Pause     ",command = pause_song)
    else:
        pass
    popup_menu.add_command(label =     "Stop      ",command =stop_music )
    global v
    if mixer.music.get_volume() == 0.0 :
        popup_menu.add_command(label = "Unmute    ",command = m_key_muteUnmute)
    else:
        popup_menu.add_command(label = "Mute      ",command =m_key_muteUnmute)
    popup_menu.add_separator()
    popup_menu.add_command(label = "Remove",
                           command = lambda:delete_file('rem'))
    popup_menu.add_command(label = "Delete" ,
                           command = lambda:delete_file('del'))
    popup_menu.add_separator()
    
    if second_screen_show_val=='no':
        popup_menu.add_command(label = "Show play_window ",command = play_window)
    elif second_screen_show_val=='yes':
        popup_menu.add_command(label = "Hide play_window ",command = hide_play_window)
    else:
        pass
    popup_menu.add_separator()
    global screen_info_widget
    if screen_info_widget=='listbox':
        global search_icon
        popup_menu.add_command(label = "Search song         ",image=search_icon,compound = 'right',
                               command = show_search_window)
    elif screen_info_widget=='search_win':
        global playlist_popup
        popup_menu.add_command(label = "Playlist                 ",image=playlist_popup
                               ,compound = 'right',command = show_playlist_window)
        
    else:
        pass        
    popup_menu.tk_popup(event.x_root,event.y_root) 


    
def delete_file(t):
    index=listbox.curselection()
    index=index[0]
    global songlist ,added_song
    songname=songlist[index]
    if t =='del':
        title='Delete this Song'
    else:
        title='Remove this song'
    c=messagebox.askquestion(title=title,
                                message='Are you sure you want to '+ title +'\n\n'+songname)
    if c=='yes':
        global playingsongindex__        
        n=0
        for song in added_song:
            if song==songname:
                added_song.pop(n)
                break
            else:
                pass
        if playingsongindex__== index:
            global deselect_song_v ,totalsonginlist__
            next_song()
            deselect_song_v=index
            playingsongindex__=index
        totalsonginlist__=totalsonginlist__-1
        songlist.pop(index)
        global srch_songlist
        srch_songlist.pop(index)
        listbox.delete(index,index)
        if t =='del':                        
            os.remove(songname)
        else:
            pass
    else:
        pass


def autor(event=None):
    r=Tk()
    r.config(bg='white')
    r.title('Aditya_Mukhiya_@Author_email- Mahadevadityamukhiya@gmail.com')
    t='''@ Shortcut Keys\n
1)  Ctrl+O    -  Add a new song to playlist
2)  Ctrl+F    -  Add  Music folder
3)  Ctrl+S    -  Search Song
4)  Left key  -  Volume Down
5)  Right key -  Volume Up
6)  S key     -  Stop Music
7)  P key     -  previous song
8)  N key     -  Next song
9)  B key     -  previous song
10) D key     -  play window/shotcut window
11) M key     -  Mute/Unmute
'''
    l=Label(r,text=t,bg='white',fg='blue',font=('',20), anchor="e", justify='left').pack()
    r.mainloop()


        

def show_playlist_window(event=None):
    global screen_info_widget
    listbox.focus_set()
    if screen_info_widget == 'listbox':
        pass
    else:             
        show_screen_widget(screen='listbox')
        search_win_variable.set('Search music')   
    



def feedback(event):
    def close(event=None):
        nonlocal feed_wind
        feed_wind.destroy()
                           

    def sent():
        def x():
            nonlocal feed
            feed_wind.destroy()
        nonlocal text_box ,but ,but_close,feed
        print(" calledd....")
        text=text_box.get('1.0','end')
        but.config(text='Sending........................', command="")
        feed.update()
        st = 55
        but.config( command = thr_sent)
        if st== 55:
            but.config(text='Please, connect to internet and then try again')
            feed_wind.update()
            return 0
        elif st == 58: 
            but.config(text='“Thank You for Your Feedback”')
        elif st == 54:
            but.config(text='Server under maintenance. Please try after some time.', fg="green")
        elif st == 53:
            but.config(text='Something went wrong. Please Try Agan After Some time.")', fg="red")
        else:
            print("Error--FeedBack-unknown-result", st)
        feed_wind.update()
        but.config(command=x)
        

    def thr_sent(event=None):
        th_sent=Thread(target=sent,daemon = True)
        th_sent.start()

    def bouble_click_lab_wid(event=None):
        nonlocal lab_x,lab_y
        lab_x=event.x
        lab_y=event.y
        
    def move_feedback_win(event=None):
        nonlocal feed_wind , lab_x,lab_y
        w=(feed_wind.winfo_geometry()).split('+')
        feed_wind.geometry(('+'+str((int(w[1])+event.x-lab_x))+'+'+str((int(w[2])+event.y)-lab_y)))

    try:

        root.attributes('-disabled', 1)                      
        feed_wind=Toplevel()
        feed_wind.overrideredirect(True)
        lab_x=0
        lab_y=0
        feed_wind.geometry('+'+str(root.winfo_width()//4)+'+'+str(root.winfo_height()//4))
        feed=Frame(feed_wind,relief='solid',width=1)
        lab=Label(feed,text='Feedback__M_A_/-Music Player',bg='grey50',fg='black',font=('',15),height=1,anchor='w')
        lab.pack(fill='x',side='top')
        lab.bind('<B1-Motion>',move_feedback_win)
        lab.bind('<Button-1>', bouble_click_lab_wid)
        but_close=Button(lab,text='X',font=('',13),command=close,bg='white',fg='red',activebackground='red',
                         activeforeground='black',bd=0,relief='flat')
        but_close.pack(side='right')
        text_box=Text(feed,bg='white',fg='black',font=('',15),bd=10,height=7,relief='sunken',width=60)
        text_box.pack(expand=True,fill='both',side='top')
        but=Button(feed,text='Send feedback',font=('',20),command=thr_sent,bg='skyblue',fg='dark green')
        but.pack(fill='x',side='bottom')
        feed.pack(fill='both',expand=True)
        feed_wind.grab_set()
        
    finally:
        
        root.attributes('-disabled', 0)
        
    
    
    
    

def save_status_data_in_file():
    global volume  ,playingsongindex__ ,added_song ,second_screen_show_val
    global rep_song_val ,second_screen_show_val,playist__directory, database
    
    database["repeat"]=rep_song_val
    database["vol"]=volume
    database["current"]=playingsongindex__
    database["show"]=second_screen_show_val
    database["added"]=added_song
    database["playlist"]=playist__directory
    database["recent"]=recent_song_plays_list

    database.commit()

    
    
def get_saved_status_data():
    global sendARGV, database
    if sendARGV == None:
        Thread(target=add_song_to_playlist_onstart, args=(database['added'], ), daemon=True).start()

    status=False
    global mixer, sdl2_audio
    import pygame._sdl2.audio as sdl2_audio
    from pygame import mixer

    mixer.init()

    v_scale.set(database['vol'])
    if sendARGV != None:
        status=True
        print("Argument==>", sendARGV)
        add_1_song_plist(event='argv',path=[sendARGV])
        Thread(target=add_song_to_playlist_onstart, args=(database['added'], ), daemon=True).start()

    if status==False:        
        global playingsongindex__ , songlist    
        playingsongindex__ = database['current']
        if playingsongindex__ < len(songlist):
            listbox.selection_set(playingsongindex__, playingsongindex__)
            listbox.yview(playingsongindex__-4)
        else:
            playingsongindex__=0
            listbox.selection_set(playingsongindex__, playingsongindex__)
    dark_title_bar()
    rep_song_valc=database['repeat']
    if rep_song_valc == '0':
        pass
    else:
        global rep_song_val
        if rep_song_valc == 'all':
            rep_song_val='all'
            rep_song0_but.grid_remove()
            rep_song1_but.grid_remove()
            rep_songall_but.grid()   
        elif rep_song_valc == 'one':
            rep_song_val='one'
            rep_song0_but.grid_remove()
            rep_songall_but.grid_remove()
            rep_song1_but.grid()
        else:
            pass
        
    second_screen_show_val=database['show']
    if second_screen_show_val =='yes':
        play_window()
    else:
        pass
    

    Thread(target=musicServer.Server, daemon=True).start()
    print("After..Server....")
    

        
def set_val(event):
    progressbar.event_generate('<Button-3>', x=event.x, y=event.y)
    event=progressbar.get()
    event=str(event).split('.')
    mixer.music.play(1,int(event[0])/1000)
    global play_pause_val
    if play_pause_val=='pause':
        unpause_song()
    
def set_val_v_scale(event):
    v_scale.event_generate('<Button-3>', x=event.x, y=event.y)




    
def on_release(event):
    global search_Window_value
    key=event.keysym
    if key == 'XF86AudioPlay':
        p_key_pause()

    elif key == "XF86AudioNext":
        next_song()
    elif key =="XF86AudioPrev":
        previous_song()
    else:
        if  search_Window_value=='show':
            search_song()
        else:
            pass
        
def choose_speaker(speaker):
    if "*" in speaker:
        pass
    else:
        global sound_output_device,frequency
        sound_output_device=speaker[3:]
        if not mixer.music.get_busy():
            frequency=0
            pass
        else:
            
            global channels,playing_file
            if frequency== '' or playing_file == None:
                print('playing_none')
                pass
            else:
                global sound_output_device_value
                sound_output_device_value=True
                try:
                    mixer.quit()
                except:
                    pass
                if sound_output_device=='default':
                    mixer.init(frequency=frequency,channels=channels)
                else:
                    mixer.init(devicename=sound_output_device,frequency=frequency,channels=channels)

                mixer.music.load(playing_file)
                event=progressbar.get()
                event=str(event).split('.')
                global volume
                mixer.music.set_volume(volume/100)
                mixer.music.play(1,int(event[0])/1000)
                sound_output_device_value=False



def three_dot_command_pop_up_menu(event=None):
    popup_menu = Menu(root,bg='grey20',fg='white',font=('',12),activeborderwidth=3,borderwidth=0,
                            relief="flat",tearoff = 0, )
################    
    audio_deive_menu = Menu(popup_menu,bg='grey20',fg='white',tearoff = 0,font=('',13))
    global sound_output_device ,window_transparency
    if sound_output_device =='default':
        l='*  Default'
    else:
        l='   Default'
    audio_deive_menu.add_command(label = l, command= functools_partial( choose_speaker, '   default'))

    num = sdl2_audio.get_audio_device_names(0)
    
    for i in range(len(num)):
        names =num[i]
        if sound_output_device == names:
            names='*  '+str(names)
        else:
            names='   '+names
        audio_deive_menu.add_command(label =names , command=functools_partial( choose_speaker, names))
           
    popup_menu.add_cascade(label="Audio Devices ", menu=audio_deive_menu)
########
    transparency_window = Menu(popup_menu,bg='white',fg='black',tearoff = 0,font=('',13))
    for i in range(10, 110, 10):
        transparency_window.add_radiobutton(label=f"{i}% transparency ",value=i,variable=window_transparency
                                        ,command=change_transparency_of_window)

    popup_menu.add_cascade(label="Window Transparency", menu=transparency_window)
    popup_menu.add_separator()
    c=root.attributes()
    if c[6]=='-fullscreen':
        if c[7] ==0:
            popup_menu.add_command(label = "Full Screen mode",command=lambda: full_screen_mode(True))
        elif c[7] ==1:
            popup_menu.add_command(label = "Exit Full Screen mode",command=lambda: full_screen_mode(False))
    else:
        print(c)
        
    
    if c[10]=='-topmost':
        if c[11] ==0:
            popup_menu.add_command(label = "Topmost mode",command=lambda: topmost_window(True))
        elif c[11] ==1:
            popup_menu.add_command(label = "Exit Topmost mode",command=lambda: topmost_window(False))
    else:
        print(c)

    popup_menu.add_command(label = "Create New Playlist",command=lambda:
                           input_pop_up_window(action='create',button_name=None))
    popup_menu.add_separator()

    popup_menu.tk_popup(event.x_root,event.y_root)
    
    
def change_transparency_of_window():
    value=window_transparency.get()
    root.wm_attributes('-alpha',int(value)/100)
    
def full_screen_mode(value):
    root.attributes("-fullscreen", value)
    if value==True:
        text='is Activated'
    else:
        text='is Deactivated'
 
def topmost_window(value):
    root.attributes("-topmost", value)
    if value==True:
        text='is Activated'
    else:
        text='is Deactivated'
      
def print_widget_under_mouse(event=None):
    x,y = root.winfo_pointerxy()
    widget = root.winfo_containing(x,y)
    color=(askcolor(title='Pick a colour'))[1]
    def wid(widget,color):
        try:
            widget.config(bg=color)
        except:
            if 'scale' in str(widget):
                style_Scale.configure('custom.Horizontal.TScale',background=color)            
        for widget in widget.winfo_children():
            try:
                widget.config(bg=color)
            except:
                if 'scale' in str(widget):
                    style_Scale.configure('custom.Horizontal.TScale',background=color)
                
            
            wid(widget,color)

    wid(widget,color)
    

def trasparet_a_colour(event=None):
    global transparent, transparentcol
    if transparent:
        transparent=False
    else:
        transparent = True
    widget=root
    def wid(widget,transparentcol):
        try:
            widget.config(bg=transparentcol)
        except:
            if 'scale' in str(widget):
                style_Scale.configure('custom.Horizontal.TScale',background=transparentcol)            
        for widget in widget.winfo_children():
            try:
                widget.config(bg=transparentcol)
            except:
                if 'scale' in str(widget):
                    style_Scale.configure('custom.Horizontal.TScale',background=transparentcol)
                
            
            wid(widget,transparentcol)

    wid(widget,transparentcol)
    root.wm_attributes("-transparentcolor",transparentcol )

    
def show_screen_widget(event=None,screen=None):
    global listbox,current_playlist_on_root
    if screen != None:
        global screen_info_widget,search_Window_value
        if screen == 'listbox':
            try:
                configure_user_created_listbox(False)
            except:
                pass
            src_listbox.pack_forget()
            recent_frame.pack_forget()
            Frame_for_user_created_listbox.pack_forget()

            
            listbox.pack(expand=True,fill='both',padx=0)
            root.unbind('<Key>')
            screen_info_widget='listbox'
            bind_listbox_key()
            search_Window_value='hide'
            current_playlist_on_root='listbox'

        elif screen =="recent_plays":
            try:
                configure_user_created_listbox(False)
            except:
                pass
            
            src_listbox.pack_forget()
            listbox.pack_forget()
            Frame_for_user_created_listbox.pack_forget()
            
            recent_frame.pack(expand=True,fill='both')
            root.unbind('<Key>')
            screen_info_widget='recent_plays'
            bind_listbox_key()
            search_Window_value='hide'
            current_playlist_on_root='recent_plays'
            
            recent_frame.pack(expand=True,fill='both',padx=0)
            
            

            
        elif screen == 'search_win':
            try:
                configure_user_created_listbox(False)
            except:
                pass
            listbox.pack_forget()
            recent_frame.pack_forget()
            Frame_for_user_created_listbox.pack_forget()
            src_listbox.pack(expand=True,fill='both',padx=0)
            ent_search_win.focus_force()
            src_listbox
            screen_info_widget='search_win'
            current_playlist_on_root='search_win'
            unbind_listbox_key()
            search_Window_value='show'

        elif screen =='youtube':
            try:
                configure_user_created_listbox(False)
            except:
                pass
            
            listbox.pack_forget()
            src_listbox.pack_forget()
            recent_frame.pack_forget()
            Frame_for_user_created_listbox.pack_forget()
            screen_info_widget='youtube'
            root.unbind('<Key>')
            current_playlist_on_root='youtube'
            search_Window_value='hide'
            unbind_listbox_key()
            
        elif screen =="User_Playlist":
            try:
                configure_user_created_listbox(False)
            except:
                pass
            src_listbox.pack_forget()
            listbox.pack_forget()
            recent_frame.pack_forget()
            root.unbind('<Key>')
            screen_info_widget='User_Playlist'
            bind_listbox_key()
            search_Window_value='hide'
            Frame_for_user_created_listbox.pack(expand=True,fill='both')
            search_win_variable.set('Search music')   

            


def move_item_from_listbox(event,master,listbox):
    event=master.winfo_pointerxy()
    global song_move_win , widget_information ,root_geometry_information
    global created_directory_button_list ,lab___ ,reMoving_song_name, BUTTONbg, BUTTONfg
    activate=False
    try:
        if song_move_win == 'yes':
            pass
        activate=False
    except:
        activate=True
        pass
        
    
    if activate==True:
        global screen_info_widget , songlist,src_listbox
        if screen_info_widget=='search_win':
            index=src_listbox.curselection()
            index=index[0]
            song_name=src_listbox.get(index, index)
            song_name=song_name[0]
            
            index=''
            file=''
            t=0
            for path in songlist:
                if song_name in path:
                    file=path
                    index=t
                    break
                else:
                    pass
                t+=1
            text=song_name
            index=index
            
        else:        
                    
            text=listbox.curselection()
            index=text[0]
            text=listbox.get(text[0])
        global Moving_song_name 
        Moving_song_name=songlist[int(index)]
        
        song_move_win=Toplevel()
        song_move_win.overrideredirect(True)
        song_move_win.wm_attributes('-alpha',0.9)
        back_col='deep sky blue'
        song_move_win.geometry('+'+str(event[0])+'+'+str(event[1]))

        frame = Canvas(song_move_win,bg='deep pink',bd=0,width=900,height=65,highlightthickness=0)
            
        frame.pack(fill='both',expand=True)
        custom_shape_canvas(parent=frame,width=900,height=65,rad=25,padding=3,bg=back_col)

        lab___=Label(frame,text=text[:50],bg=back_col,fg='white',font=('',20),width=44,anchor='w')
        lab___.place(x=30,y=10)
        song_move_win.wm_attributes('-transparentcolor', 'deep pink')

        root.bind('<ButtonRelease-1>',relese)
        widget_information={}

        r_x=root.winfo_rootx()
        r_y=root.winfo_rooty()
        r_w=r_x+30+root.winfo_width()
        r_h=r_y+30+root.winfo_height()
        
        root_geometry_information=[r_x-30,r_w,r_y-60,r_h]

        for button in created_directory_button_list:            
            x=button.winfo_rootx()
            y=button.winfo_rooty()
            x_m=x+button.winfo_width()
            y_m=y+button.winfo_height()
            widget_information[button]=[x,x_m,y,y_m]


            
    else:
        reMoving_song_name=False
        song_move_win.geometry('+'+str(event[0]-20)+'+'+str(event[1]-25))
        if event[0] < root_geometry_information[0] or event[0] > root_geometry_information[1] or event[1] < root_geometry_information[2] or event[1] > root_geometry_information[3] :
            lab___.config(fg='red')
            reMoving_song_name=True
            

        if reMoving_song_name != True:
            bh=False
            for button in widget_information:            
                butn_bord=widget_information[button]                        
                if event[0]  >=  butn_bord[0]   and   event[0] <= butn_bord[1]:
                    if  event[1] >= butn_bord[2] and event[1] <= butn_bord[3] :
                        bh=True
                        lab___.config(fg='green4')
                        button.config(bg='green yellow')                    
                    else:
                        button.config(bg=BUTTONbg)
                        if bh==True:
                            pass
                        else:                        
                            lab___.config(fg='white')
                else:
                    button.config(bg=BUTTONbg)
                    if bh==True:
                        pass
                    else:                    
                        lab___.config(fg='white')


        
        

        

def relese(event=None):
    global song_move_win ,created_directory_button_list ,Moving_song_name
    global playist__directory,reMoving_song_name,playlist
    try:
        if song_move_win== "":
            pass
        song_move_win.destroy()
        root.unbind('<Button-1>')
        i=0
        root.unbind('<ButtonRelease-1>')
        if reMoving_song_name == True:        
            if current_playlist_on_root  in   playist__directory.keys():
                indx=0
                for file in playist__directory[current_playlist_on_root]:
                    indx+=1
                    if file==Moving_song_name:
                        t=1
                        break                    
                if indx != 0:
                    indx=indx-1
                    playist__directory[current_playlist_on_root].pop(indx)
                    move_to=listbox.yview(indx)[0]
                    user_created_listbox_command(current_playlist_on_root,refresh=True)
                    save_status_data_in_file()
                    if mixer.music.get_busy():
                        global playingsongindex__
                        if playingsongindex__ == indx:
                            next_song()
                            listbox.yview_moveto(move_to)
                        else:
                            if playingsongindex__ > indx:
                                listbox.select_set(playingsongindex__-1)
                                listbox.yview(playingsongindex__-1)
                            else:
                                listbox.select_set(playingsongindex__)
                                listbox.yview(playingsongindex__)
                    else:
                        if len(songlist) >= indx:
                            indx=indx-1

                        listbox.select_set(indx)
                            
                        listbox.yview(indx)
                        
                            
                        

                else:
                    print('File not found')
            else:
                indx=songlist.index(Moving_song_name)
                songlist.pop(indx)
                move_to=listbox.yview()[0]
                listbox.delete(0,'end')
                global totalsonginlist__
                totalsonginlist__=0
                def add_song_to_playlist_(path):
                    global totalsonginlist__

                     
                    name=os.path.basename(path)
                    listbox.insert('end',(name[:90])) #       
                    if totalsonginlist__ % 2 == 0:
                        listbox.itemconfig(totalsonginlist__,background='grey20',fg='white')
                    totalsonginlist__+=1
        
                for path in songlist:
                    
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            if path.endswith(".mp3"):
                                add_song_to_playlist_(path)
                listbox.select_set(indx-1)
                listbox.yview(indx-1)
                

        else:
            for button in created_directory_button_list:
                if button['bg'] == 'green yellow':
                    conf=False
                    l=0
                    for file in playist__directory[button['text']]:
                        if file ==Moving_song_name:
                            conf=True
                            break
                        l+=1

                    if conf == True:
                        #print('File already exists')
                        user_created_listbox_command(button['text'])
                        listbox.select_set(l)
                        listbox.yview(l)
                    else:                                        
                        playist__directory[button['text']].append(Moving_song_name)
                        user_created_listbox_command(button['text'])
                        listbox.select_set('end')
                        listbox.yview(listbox.size())
                        save_status_data_in_file()
                else:
                    pass
                i+=1
    except Exception as e:
        print(e)
    finally:
        try:
            del song_move_win,Moving_song_name
        except:
            pass
    

def motion(event):
    x, y = event.x, event.y
    print('{}, {}'.format(x, y))
    

def add_song_in_user_created_listbox(created_playlist,button_text_name):
    global user_created_listbox,fav_plalist
    user_created_listbox.delete(0,'end')
    tem_list_song=[]
    def add_song_to_playlist_(path):
        nonlocal tem_list_song
        global fav_plalist ,user_totalsonginlist__,user_created_listbox
        tem_list_song.append(path)
        name=os.path.basename(path)
        user_created_listbox.insert('end',(name[:90])) #       
        if user_totalsonginlist__ % 2 == 0:
            user_created_listbox.itemconfig(user_totalsonginlist__,background="grey22",fg='white')
        user_totalsonginlist__+=1
        
    for path in created_playlist:
        
        if os.path.exists(path):
            if os.path.isfile(path):
                if path.endswith(".mp3"):
                    add_song_to_playlist_(path)

    fav_plalist=tem_list_song
    playist__directory[button_text_name]=tem_list_song
    save_status_data_in_file()

def popup_menu_for_create_del_rename_playlist(event=None,button_name=None):
    print(button_name)
    
    create_playlist_popup_menu = Menu(root,bg='grey30',fg='lightyellow2', bd=0, tearoff = 0,font=('',15), activeborderwidth=5,
                                        )
    
    create_playlist_popup_menu.add_command(label ="Create Playlist +",command = lambda :
        command_popup_menu_for_create_del_rename_playlist(action='create',button_name=button_name) )
    create_playlist_popup_menu.add_separator()

    create_playlist_popup_menu.add_command(label ="Rename Playlist  ",command = lambda :
        command_popup_menu_for_create_del_rename_playlist(action='rename',button_name=button_name) )
    create_playlist_popup_menu.add_separator()
    
    create_playlist_popup_menu.add_command(label ="Delete Playlist  ",command = lambda :
         command_popup_menu_for_create_del_rename_playlist(action='delete',button_name=button_name) )
    
    create_playlist_popup_menu.tk_popup(event.x_root,event.y_root) 


    
def show_search_window(event=None):
    global screen_info_widget
    if screen_info_widget == 'search_win':
        ent_search_win.focus_force()
        pass
    else:
        search_win_variable.set('')
        show_screen_widget(screen='search_win')
        
                    
    
def configure_user_created_listbox(state):
    global fav_plalist , user_totalsonginlist__,user_created_listbox
    
    global songlist,totalsonginlist__, listbox
    global duplicate_songlist ,duplicate_totalsonginlist__ , duplicate_listbox
    user_created_listbox.focus_force()    
    if state==True:
        try:
            if duplicate_songlist==" ":
                pass
        except:
            duplicate_songlist=songlist
            duplicate_totalsonginlist__=totalsonginlist__
            duplicate_listbox=listbox
        songlist=fav_plalist
        totalsonginlist__=user_totalsonginlist__
        listbox=user_created_listbox
        bind_listbox_key()
        listbox.bind('<B1-Motion>', lambda event : move_item_from_listbox(event,root,listbox))

        
    elif state == False:
        songlist=duplicate_songlist
        totalsonginlist__=duplicate_totalsonginlist__
        listbox=duplicate_listbox
        del duplicate_songlist
        global created_directory_button_list, BUTTONbg, BUTTONfg
        for b in created_directory_button_list:
            b.config(bg=BUTTONbg,fg=BUTTONfg)


          
    
def custom_shape_canvas(parent=None,width=300,height=100,rad=50,padding=3,bg='red'):
    color=bg
    cornerradius=rad
    rad = 2*cornerradius
    parent.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,
                           padding+cornerradius,padding,width-padding-cornerradius,padding,
                           width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,
                           width-padding-cornerradius,height-padding,padding+cornerradius,height-padding),
                          fill=color, outline=color)

    parent.create_arc((padding,padding+rad,padding+rad,padding), start=90, extent=90, fill=color,
                      outline=color)
    parent.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90,
                      fill=color, outline=color)
    parent.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270,
                      extent=90, fill=color, outline=color)
    parent.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90,
                      fill=color, outline=color)
    
def input_pop_up_window(action=None,button_name=None):
    def on_enter(e,button):
        if button=="ok":
            e.widget['background'] = 'grey85'
            e.widget['fg'] = 'blue2'
            
        elif button=="cancel":
            e.widget['background'] = 'grey85'
            e.widget['fg'] = 'blue2'
            
        elif button=="ent":
            if not e.widget.focus_get() == e.widget:
                e.widget['fg'] = 'blue2'

        
    def on_leave(e,button=None):
        if button=="ent":
            if not e.widget.focus_get() == e.widget:
                e.widget['fg'] = 'black'
                

        elif button=="cancel":
            e.widget['background'] = '#0065ff'
            e.widget['fg'] = 'black'
            e.widget['bd'] = 2
            
        if button=="ok":
            e.widget['background'] = '#0065ff'
            e.widget['fg'] = 'black'
##        
##        else:
##            e.widget['background'] = 'grey60'

    def destroy_pop_up_window(event=None):        
        nonlocal pop_up_window
        pop_up_window.destroy()

    def focus_in_command(event=None):
        nonlocal input_text ,ent
        t=input_text.get().strip()

        if t in ["Please enter Name","PlayList is allready exist","Enter Name"] or "already exists" in t:
            input_text.set('')
            ent.config(fg='blue')
        else:
            pass
        
    def bouble_click_pop_up_window(event=None):
        nonlocal lab_x,lab_y
        lab_x=event.x
        lab_y=event.y
        
    def move_pop_up_window(event=None):
        nonlocal pop_up_window , lab_x,lab_y
        w=(pop_up_window.winfo_geometry()).split('+')
        pop_up_window.geometry(('+'+str((int(w[1])+event.x-lab_x))+'+'+str((int(w[2])+event.y)-lab_y)))



############################################        
        
    def ok_butn_command(event=None):
        nonlocal action ,cancel_but        
        nonlocal input_text ,result ,button_name
        global playist__directory, created_directory_button_list,root, BUTTONbg, BUTTONfg, BUTTONbgEn, BUTTONfgEn
        
        text=input_text.get().strip()
        result=text
        if text =='' or text in ["Please enter Name","PlayList is allready exist","Enter Name"] or "already exists" in text:
            input_text.set('Please enter Name')
            cancel_but.focus_force()
            
            
        else:
            if action =='create':
                print("Action Creating....")
                for key in playist__directory:
                    if key==text:
                        text=False
                if text==False:
                    input_text.set('PlayList is allready exist')
                    cancel_but.focus_force()
                else:
                    print("Creating....")
                    playist__directory[text]=[]
                    i=len(created_directory_button_list)
                    but_cc=Button(playlist_scrollable_frame,text=text,bg=BUTTONbg,
                                       width=360,font=('',16,'bold'),compound='left',anchor='w',
                                       fg=BUTTONfg,bd=0,relief='flat',image=Created_Playlist_button_img,
                                       command= functools_partial (user_created_listbox_command, text ,False),
                                       padx=13,pady=4, cursor="hand2")
                    but_cc.pack(side='bottom',anchor='w',fill='x',expand=True)


                    but_cc.bind("<Enter>", lambda event: color_change_enter_leave(event,
                                                        bg=BUTTONbgEn,fg=BUTTONfgEn,nbg='dodger blue',
                                                                                   nfg='white'))
                    but_cc.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                        bg=BUTTONbg,fg=BUTTONfg,nbg='dodger blue',
                                                                                  nfg='white'))


                    but_cc.bind("<Button-3>",functools_partial(popup_menu_for_create_del_rename_playlist ,button_name=text))
                    created_directory_button_list.append(but_cc)
                    but_cc.bind("<MouseWheel>", lambda event : playlist_scroll_window.scroll(event))
                    save_status_data_in_file()
                    user_created_listbox_command(text,i)
                    destroy_pop_up_window()
                    #updating_frame_height_of_playlist_button
                    playlist_scroll_window.configure_height(event=True)
                    print("Creating...45.")


            elif action =='rename':
                nonlocal button_name
                st=False
                for key in playist__directory:
                    if key==text:
                        st=True
                if st==True:
                    input_text.set('{} already exists'.format(text))
                    cancel_but.focus_force()
                else:
                    n=0
                    st=False
                    for key in playist__directory:
                        if key==button_name:
                            st=True
                            break
                        else:
                            n+=1
                    #___________

                    playist__directory[text] = playist__directory[button_name]                    
                    del playist__directory[button_name]
                    
                    created_directory_button_list[n].config(text=text,fg='green2',
                                command= functools_partial (user_created_listbox_command, text ,n))
                    created_directory_button_list[n].bind("<Button-3>",functools_partial(
                        popup_menu_for_create_del_rename_playlist ,button_name=text))
                    save_status_data_in_file()
                    destroy_pop_up_window()
                    user_created_listbox_command(text,n)
                    #updating_frame_height_of_playlist_button
                    playlist_scroll_window.configure_height(event=True)

         
        
    result='Aditya'
    try:
        lab_x,lab_y=0,0
        back_col=choice(['cyan','goldenrod'])
        root.attributes('-disabled', 1)        
        pop_up_window=Toplevel()
        pop_up_window.overrideredirect(True)
        pop_up_window.geometry('+'+str(root.winfo_width()//3)+'+'+str(root.winfo_height()//3))
        pop_up_window.config(bg='deep pink')
    
        frame = Canvas(pop_up_window,bg='deep pink',bd=0,width=750,height=300,highlightthickness=0)
            
        frame.pack(fill='both',expand=True)
        
        custom_shape_canvas(parent=frame,width=750,height=300,rad=50,padding=3,bg=back_col)
        
        l=Label(frame,bg=back_col,bd=0,fg='black',font=('bold',30,'bold italic'))
        l.place(x=100,y=30)

        input_text = StringVar()
        ent=Entry(frame,textvariable = input_text,bd=1,relief='sunken', justify ='left',font=('',28,'bold')
                  ,bg='grey99',fg='black',width=25)
        ent.place(x=24,y=120)
        ent.bind("<FocusIn>",focus_in_command)
        ent.bind("<Enter>", lambda event : on_enter(event,'ent'))
        ent.bind("<Leave>", lambda event : on_leave(event,'ent'))
        ent.bind('<Return>',ok_butn_command)

        if action =='create':
            input_text.set('Enter Name')
            l.config(text='Create New Playlist ')
            
        elif action =='rename':
            input_text.set(button_name)
            l.config(text='Rename Playlist  ')
        
        
        
        frame_butn=Frame(frame,relief='flat',bd=0,bg=back_col,height=50,width=400)
        frame_butn.place(x=330,y=230)
        
        frame_butn.bind("<Enter>", lambda event : on_enter(event,'frame_butn'))
        frame_butn.bind("<Leave>", lambda event : on_leave(event,'frame_butn'))
        
        cancel_but=Button(frame_butn,text='  Close  ',command=destroy_pop_up_window,font=('',13,'')
                          ,bg='#0065ff',bd=3, relief="flat", cursor="hand2")
        cancel_but.place(x=270,y=0)
        
        
        ok_but=Button(frame_butn,text='    Ok      ', command=ok_butn_command,font=('',13,''),
                      bg='#0065ff',bd=3,relief='flat', cursor="hand2")
        ok_but.place(x=110,y=0)
        
        ok_but.bind("<Enter>", lambda event : on_enter(event,'ok'))
        ok_but.bind("<Leave>", lambda event : on_leave(event,'ok'))
        
        cancel_but.bind("<Enter>", lambda event : on_enter(event,'cancel'))
        cancel_but.bind("<Leave>", lambda event : on_leave(event,'cancel'))
        
        pop_up_window.bind('<B1-Motion>',move_pop_up_window)
        pop_up_window.bind('<Button-1>', bouble_click_pop_up_window)
        
        pop_up_window.wm_attributes('-transparentcolor', 'deep pink')
        pop_up_window.grab_set()
        root.wait_window(pop_up_window)
        root.focus_force()

    except Exception as e:
        print(e)
    finally:        
        root.attributes('-disabled', 0)
        return result
    
    
def command_popup_menu_for_create_del_rename_playlist(event=None,action=None,button_name=None):    
    if action=="create":
        result=input_pop_up_window(action=action,button_name=button_name)
        print('____{',result,'}______')
    elif action=="rename":
        if button_name == 'Downloads':
            pass
        else:
            input_pop_up_window(action="rename",button_name=button_name)
        
    elif action=="delete":
        if button_name == 'Downloads':
            pass
        else:
            global playist__directory
            button_count=0
            for key in playist__directory:
                if key == button_name:
                    c=messagebox.askquestion(title='Delete Playlist',message=' Playlist : '+str(key)+
                                             '\n\n Are you sure you want to delete this playlist?')
                    if c =='yes':
                        playist__directory.pop(key)
                        global created_directory_button_list
                        created_directory_button_list[button_count].destroy()
                        show_screen_widget(screen='listbox')
                        created_directory_button_list.pop(button_count)
                        save_status_data_in_file()
                        #updating_frame_height_of_playlist_butto
                        playlist_scroll_window.configure_height(event=True)

                        break
                    else:
                        pass
                    
                else:
                    button_count+=1                    
        
    else:
        pass
    
def color_change_enter_leave(event=None,bg=None,fg=None,nbg=None,nfg=None):
    if event==None:
        pass
    else:
        try:
            if bg != None:
                if nbg != event.widget['bg']:
                    if event.type.name == "Leave":
                        global transparent
                        if transparent:
                            global transparentcol
                            event.widget['bg']=transparentcol
                        else:
                            event.widget['bg']=bg
                    else:
                        event.widget['bg']=bg
            if fg!= None:
                if nfg != event.widget['fg']:
                    event.widget['fg']=fg
        except Exception as e:
            print(e)
                
def play_gif(gif_name='dancing_girl',after=1):
    gif_data_dict={'dancing_girl':[86,'dance.gif','white']}
    frames = [PhotoImage(file=resource_path("data/"+gif_data_dict[gif_name][1]),
                         format = 'gif -index %i' %(i)) for i in range(gif_data_dict[gif_name][0])]
    frameCnt=gif_data_dict[gif_name][0]
    indx=0
    play_frame_playlist_icon_label.configure(bg='white')
    while True:
        global play_pause_val,play_gif_status
        if play_gif_status==False:
            play_frame_playlist_icon_label.configure(image=play_frame_playlist_icon,bg='black')
            break
        else:
            if mixer.music.get_busy() and play_pause_val != 'pause':
                
                frame = frames[indx]
                indx += 1
                if indx == frameCnt:
                    indx = 0
                play_frame_playlist_icon_label.configure(image=frame)
            sleep(after/11)
            
def play_gif_or_stop(event=None):
    global play_gif_status
    if play_gif_status==False:
        play_gif_status=True
        thy=Thread(target=play_gif,args=('dancing_girl',1,),daemon = True)
        thy.start()
        
    elif play_gif_status==True:
        play_gif_status=False
        
        

def user_created_listbox_command(button_text_name,refresh=False):
    global screen_info_widget , created_directory_button_list ,current_playlist_on_root, BUTTONfg, BUTTONbg
    if screen_info_widget != 'User_Playlist':
        show_screen_widget(event=None,screen='User_Playlist')
    global fav_plalist ,user_totalsonginlist__    
    user_totalsonginlist__=0
    if refresh==True:
        current_playlist_on_root='refresh'

    if current_playlist_on_root != button_text_name:    
        fav_plalist=playist__directory[button_text_name]
        current_playlist_on_root=button_text_name
        
        add_song_in_user_created_listbox(fav_plalist,button_text_name)
        
        play_frame_num_song_label.config(text=(str(len(fav_plalist))+'  Songs in playlist'),
                                         fg='white',anchor='e',font=('',11,'bold'))
        play_frame_playlist_name_label.config(text=button_text_name,font=('',30,'bold italic'),
                                              fg='white')
        configure_user_created_listbox(True)
        global play_gif_status
        if play_gif_status==False:
            if str(play_frame_playlist_icon_label['image']) != str(play_frame_playlist_icon):
                play_frame_playlist_icon_label.configure(image=play_frame_playlist_icon)
        
    for b in created_directory_button_list:
        if b['text'] == button_text_name:
            b.config(bg='dodger blue',fg='white')
        else:
            b.config(bg=BUTTONbg,fg=BUTTONfg)
    if show_recent_song_window_button['bg']=="orange":
        show_recent_song_window_button.config(bg=BUTTONbg,fg=BUTTONfg)

            
def play_all_butn_command(event=None):
    button_name=play_frame_playlist_name_label['text']
    print(button_name)
    listbox.select_set(0)
    rep_song_all()
    listbox_command(event=None)
    
def rename_butn_command(event=None):
    command_popup_menu_for_create_del_rename_playlist(action='rename',
                                    button_name=play_frame_playlist_name_label['text'])

def delete_butn_command(event=None):
    command_popup_menu_for_create_del_rename_playlist(action='delete',
                                    button_name=play_frame_playlist_name_label['text'])

def add_to_butn_command(event=None):
    popup_menu_for_create_del_rename_playlist(event=event,
                            button_name=play_frame_playlist_name_label['text'])

   



class playlist_scroll_window:
    def scroll(event):
        playlist_canvas.yview("scroll",-1*int(event.delta/120),"units")

    def configure_height(event=None):
        height=int(root.winfo_height())-560
        global playlist_canvas_root_height
        
        if playlist_canvas_root_height != height or event ==True:
            playlist_canvas_root_height=height
            hg=(60*len(created_directory_button_list))

            if hg <= height:
                playlist_canvas.config(height=hg)
            else:
                playlist_canvas.config(height=height)


#__________________________________________________________________________________________
def dwn_scroll_window_gr(event):
    global dwn_canvas_gr
    dwn_canvas_gr.yview("scroll",-1*int(event.delta/120),"units")


    

    

def enter_gr(event):
    global enter_on_button_st
    if enter_on_button_st !=True:
        global screen_pop_button , button_recent_popup
        
        enter_on_button_st=False
        try:
            screen_pop_button.destroy()
        except:
            pass
            
        screen_pop_button=Toplevel()

        global pop_up_play_photo
        button_recent_popup = Button(screen_pop_button,image=pop_up_play_photo,bg='green',fg='green',
                            bd=0,activebackground='green', cursor="hand2")
        button_recent_popup.pack(side='top')
        screen_pop_button.wm_attributes('-transparentcolor', 'green')
        screen_pop_button.config(bg='green',bd=0)
        screen_pop_button.wm_attributes('-alpha',0.8)
              
        screen_pop_button.config(bg='green',relief='raised',bd=0)
        screen_pop_button.overrideredirect(True)


        global playing_file,recent_song_plays_list

        path=str(event.widget['text'])

        if playing_file != None:        
            if path ==playing_file:
                global pop_up_pause_photo
                button_recent_popup.config(image=pop_up_pause_photo,
                                    command=lambda : pause_pop_button_command(event,button_recent_popup))
            else:
                button_recent_popup.config(command=lambda : play_music_gr(event,button_recent_popup))
        else:
            button_recent_popup.config(command=lambda : play_music_gr(event,button_recent_popup))

        
        button_recent_popup.bind('<Enter>',enter_popUP_button)
        button_recent_popup.bind('<Leave>',lambda event_x :Thread(target=leave_popUP_button,
                                                                  args=(event_x,)
                                                                  ).start())
        

        x=event.widget.winfo_rootx()+120
        y=event.widget.winfo_rooty()+52
        screen_pop_button.geometry(f'+{x}+{y}')
        event.widget.config(relief='sunken')

    
    
def leave_gr(event):
    sleep(0.001)
    global screen_pop_button ,enter_on_button_st
    if enter_on_button_st != True:
        try:
            screen_pop_button.destroy()
        except:
            pass
        event.widget.config(relief='flat')
        enter_on_button_st=False
        
def enter_popUP_button(event):
    global enter_on_button_st
    enter_on_button_st=True

def leave_popUP_button(event):
    sleep(0.001)
    global enter_on_button_st
    enter_on_button_st=False 
        
def pause_pop_button_command(event,button_recent_popup):
    pause_song()
    global pop_up_play_photo
    button_recent_popup.config(image=pop_up_play_photo)
    button_recent_popup.config(command=lambda : play_pop_button_command_after_pause(event,
                                                button_recent_popup))

def play_pop_button_command_after_pause(event,button_recent_popup):
    unpause_song()
    global pop_up_pause_photo
    button_recent_popup.config(image=pop_up_pause_photo)
    button_recent_popup.config(command=lambda : pause_pop_button_command(event,button_recent_popup))

    
def play_music_gr(event,button_recent_popup):
    global press_paly_buttton,pop_up_pause_photo 
    press_paly_buttton=True    
    button_recent_popup.config(image=pop_up_pause_photo)
    path=str(event.widget['text'])
    global recent_song_plays_list, playingsongindex__  ,songlist
    playingsongindex__=songlist.index(path)
    play_music(path)
    press_paly_buttton=False
    button_recent_popup.config(command=lambda : pause_pop_button_command(event,button_recent_popup))
    


    
def screen_gr(recent_frame):
    global image_list_gr,dwn_scrollable_frame_gr,dwn_canvas_gr

    dwn_canvas_gr =Canvas(recent_frame,bg='grey20',width=530,height=0,bd=0,highlightthickness=0)
    dwn_canvas_gr.pack( fill="both",expand=True,side="left")


    dwn_scrollable_frame_gr =Frame(dwn_canvas_gr,bg='grey20')
    recent_frame.bind("<Enter>",destroy_screen_pop_button)
    dwn_scrollable_frame_gr.bind("<Configure>",lambda e: dwn_canvas_gr.configure(
        scrollregion=dwn_canvas_gr.bbox("all")))

    dwn_canvas_gr.create_window((0, 0), window=dwn_scrollable_frame_gr, anchor="nw")
    dwn_canvas_gr.bind("<MouseWheel>",dwn_scroll_window_gr)
    dwn_scrollable_frame_gr.bind("<MouseWheel>",dwn_scroll_window_gr)
    
def configure_gr(event=None):
    width=(root_2.winfo_width())+25
    no_of_win_in_column=width//315
    global no_of_column_win ,dwn_scrollable_frame_gr
    if no_of_column_win != no_of_win_in_column:
        dwn_scrollable_frame_gr.config(padx=0)
        no_of_column_win=no_of_win_in_column        
        padx_row=10
        no_of_win_in_column=no_of_win_in_column-1

        global recent_song_plays_list,frames_in_song_dict_gr
        row=0
        column=-1

        for file in recent_song_plays_list:
            try:
                column+=1
                widget=frames_in_song_dict_gr[file]
                widget.grid_configure(row=row,column=column,padx=10,pady=10)
                if no_of_win_in_column==column:
                    column=-1
                    row+=1
            except Exception as e:
                print('Error[8081][IN_configue_recent_win]  : ',e)
 
        

        
def create_music_icon_in_playlist_gr(parent,file,row,column):
    global frame_gr,frames_in_song_list_gr,image_list_gr
    bg="#661400"
    frame_gr=Frame(parent, bg=bg, padx=2, pady=2)
    frame_gr.grid(row=row,column=column,padx=8,pady=10)
    frame_gr.bind("<MouseWheel>",dwn_scroll_window_gr)
    try:
        music = ID3(file)
        try:
            data=music.getall("APIC")[0].data
            load=(Image.open(io_import.BytesIO(data))).resize((300,
                                                      180),Image.Resampling.LANCZOS)
            name=(((str(music.get("TIT2")).replace('_M_A_Music_Player.mp3','')).replace('_',' ')[:40]).lower()).title()


        except:
            load = (Image.open(resource_path("data/mahadev_pic.png"))).resize((300,180),Image.Resampling.LANCZOS)
            name=(((str(os.path.basename(file)).replace('_M_A_Music_Player.mp3','')).replace('_',' '
                                                            )[:40]).lower()).title()

        music_covor_image = ImageTk.PhotoImage(load,master=recent_frame)
        image_list_gr.append(music_covor_image)
        ww = 33
        l=Label(frame_gr,text=str(file),image=image_list_gr[(len(image_list_gr)-1)],bd=4,bg=bg,
                font=('',0), )
        l.pack(side='top', expand=True)
        
        bb=Label(frame_gr,text=name,font=('',9,'italic'),fg='white',bg=bg,anchor='w',
                justify='center',width=ww,height=1,bd=0)
        bb.pack(side='bottom')
        l.bind("<MouseWheel>",dwn_scroll_window_gr)
        bb.bind("<MouseWheel>",dwn_scroll_window_gr)
        l.bind("<Enter>",enter_gr)
        l.bind('<Leave>',lambda event : Thread(target=leave_gr,args=(event,)).start())
        
        frames_in_song_dict_gr[file]=frame_gr

    except Exception as e:
        print('Error:[File_Image ] : ',e)
        pass
    frames_in_song_list_gr.append(frame_gr)
    
        
def add_data_in_recent_plays_frame():
    global enter_on_button_st,recent_frame

    enter_on_button_st=False
    width=(root_2.winfo_width())+25
    global dwn_canvas_gr
    no_of_win_in_column=width//328
    
    no_of_column_win=no_of_win_in_column
    no_of_win_in_column=no_of_win_in_column-1
    global dwn_scrollable_frame_gr , frames_in_song_dict_gr ,recent_song_plays_list
    row=0
    column=-1
    for file in recent_song_plays_list:
        if os.path.exists(file):
            column+=1
            try:
                widget=frames_in_song_dict_gr[file]
                widget.grid_configure(row=row,column=column,padx=10,pady=10)
            except:
                create_music_icon_in_playlist_gr(dwn_scrollable_frame_gr,file,row,column)
            if no_of_win_in_column==column:
                column=-1
                row+=1
            root.update()
            

        else:
            print('File Not Found :',file)

    recent_frame.bind("<Configure>",configure_gr)

    
    
def destroy_screen_pop_button(event=None):
    try:
        screen_pop_button.destroy()
    except:
        pass

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
def show_recent_song_window():
    global screen_info_widget,dwn_canvas_gr, BUTTONfg, BUTTONbg
    if screen_info_widget == 'recent_plays':
        pass
    else:
        show_screen_widget(screen='recent_plays')
    #__clearing__window
    
    for children in dwn_scrollable_frame_gr.winfo_children():
        children.grid_forget()
    dwn_canvas_gr.yview_moveto(0.0)
    #_updating_some_variable
    for b in created_directory_button_list:
        b.config(bg=BUTTONbg,fg=BUTTONfg)    
    global frames_in_song_list_gr    
    frames_in_song_list_gr.clear()
    show_recent_song_window_button.config(bg='orange',fg='white')
    add_data_in_recent_plays_frame()


def leftPress(event =None):
    print("LeftKey Pressed...")
    return "break"

def rightPress(event =None):
    print("Right Pressed...")
    return "break"


def dark_title_bar():
    global root
    """
    MORE INFO:
    https://docs.microsoft.com/en-us/windows/win32/api/dwmapi/ne-dwmapi-dwmwindowattribute
    """
    root.update()
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    set_window_attribute = ct.windll.dwmapi.DwmSetWindowAttribute
    get_parent = ct.windll.user32.GetParent
    hwnd = get_parent(root.winfo_id())
    rendering_policy = DWMWA_USE_IMMERSIVE_DARK_MODE
    value = 2
    value = ct.c_int(value)
    set_window_attribute(hwnd, rendering_policy, ct.byref(value),
                         ct.sizeof(value))


import ctypes as ct


database = DataBabse()

windll.shcore.SetProcessDpiAwareness(True)

current_playlist_on_root='listbox'
channels=None
playing_file=None
sound_output_device='default'
sound_output_device_value=False
play_thread_song_status='stop'
stop_sli_prog_th='f'        
rep_song_val='0'
stop_song_tread='f'
volume=40
volume_icon=2
paylist_state='show'
songlist=[]
srch_songlist=[]
added_song=[]
totalsonginlist__=0
playingsongindex__=0
deselect_song_v=''
frequency=''
transparent = False

transparentcol='tan1'

task_bg=choice(['orange','pink3','gold','cyan2'])
activebg=task_bg
play_pause_val='pause'
stopButton = False

pauseButtonStatus = False
sc=None
t1=''
second_screen_show_val='no'
search_Window_value='hide'

screen_info_widget='listbox'
change_youtube_index=''
audio_length=10000
song_count=0
user_totalsonginlist__=0
play_gif_status=False
frames_in_song_list_gr=[]
#___________
press_paly_buttton=False
enter_on_button_st=False
no_of_column_win=0
image_list_gr=[]
frames_in_song_dict_gr={}


musicServer = ServerMusic()
###################  Window   ##
root=Tk()
root.title('Music Player 🎵')
root.geometry('1695x800+100+40')
root.config(bg="grey10")
phototitle = PhotoImage(file =resource_path("data/music_new.png"),master=root)
root.iconphoto(True, phototitle)
window_transparency=StringVar()

fram1=Frame(root,bg='grey10',bd=0,height='120')
fram1.pack(side='bottom',fill='x')

root_2=Frame(root,bg='grey10',bd=0)
root_2.pack(fill='both',side='right',expand=True)

root_1_bg= "grey25"

root_1=Frame(root,bg=root_1_bg,bd=0)
root_1.pack(ipadx=0,side='left',fill='y')

st_but=Button(fram1,text='Start 🎵',bg=choice(['cyan','orange',"cornflower blue"]),bd=0,
              fg=choice(['white','black','purple2']),font=('',28,'bold'), cursor="hand2"
              ,command=lambda: play_music_start('restart_music'),height=0,width=12)#cornflower blue
try:
    st_but.config(activebackground=task_bg+'2')
    activebg=task_bg+'2'
except:
    activebg=task_bg
######################################################

############################################

task_fram1=Frame(fram1,bd=0,bg=task_bg)
task_fram1.pack(side='right',fill='both',expand=True)

st_but.pack(side='left',fill='both',ipadx=5)

task_fram=Frame(task_fram1,bg=task_bg,bd=0,height=0)
task_fram.pack(side='top',fill='x')

root_3=Frame(task_fram1,bg=task_bg,bd=0,height=0)
root_3.pack(side='bottom',fill='x')
## Repaet song#
start_timeLabel=Label(root_3,text='00:00',bg=task_bg,fg='black',font=('',13),anchor='e')
start_timeLabel.pack(side='left',fill='both',expand=True,padx=15,ipadx=10)






img_slider = PhotoImage('img_slider',file=resource_path('data/recb1.png') , master=root)
# active slider
img_slider_active =PhotoImage('img_slider_active', file=resource_path('data/recb2.png'), master=root)

style_Scale = ttk.Style(root)
style_Scale.theme_use('alt')

# create scale element
style_Scale.element_create('custom.Horizontal.Scale.slider', 'image', img_slider,
                     ('active', img_slider_active))


# create custom layout

style_Scale.layout('custom.Horizontal.TScale',
             [('Horizontal.Scale.trough',
               {'sticky': 'nswe',
                'children': [('custom.Horizontal.Scale.slider',
                              {'side': 'left', 'sticky': ''})]})])
style_Scale.configure('custom.Horizontal.TScale', background=task_bg, foreground='white',
                troughcolor='white')

style_Scale.configure("black.Horizontal.TProgressbar", background='royalblue',thickness=4)


progressbar=ttk_Scale(root_3,style='custom.Horizontal.TScale',
                      from_=0,to=audio_length*1000, value=1000,length=300,
                      orient='horizontal', cursor="hand2")

progressbar.pack(side='left',fill='x',expand=True)
progressbar.bind('<Button-1>', set_val)
progressbar.bind('<B1-Motion>', set_val)


end_timeLabel=Label(root_3,text='00:00',bg=task_bg,fg='black',anchor='w',font=('',13))
end_timeLabel.pack(side='left',fill='both',expand=True,padx=15,ipadx=80)

######################### progressbar

repeat_lp=Label(task_fram,bg=task_bg)
repeat_lp.pack(side='left',expand=True)

rep_song1_img = PhotoImage(file = resource_path("data/repeat1.png"),master=root)
rep_song1_img = rep_song1_img.subsample(2,2)
rep_song1_but=Button(repeat_lp,image=rep_song1_img,bd=0,activebackground='white',cursor='hand2',
                 command=rep_song_0,height=47,width=47)
try:
    rep_song1_but.config(bg=(task_bg+'3'))
except:
    rep_song1_but.config(bg='lightgrey')
rep_song1_but.grid(row=0,column=0)
rep_song1_but.grid_remove()


rep_songall_img = PhotoImage(file = resource_path("data/repeat.png"),master=root)
rep_songall_img = rep_songall_img.subsample(3,3)
rep_songall_but=Button(repeat_lp,image=rep_songall_img,bd=0,activebackground='white',cursor='hand2'
                       ,command=rep_song_1,height=47,width=47)
try:
    rep_songall_but.config(bg=(task_bg+'3'))
except:
    rep_songall_but.config(bg='lightgrey')
rep_songall_but.grid(row=0,column=0)
rep_songall_but.grid_remove()

rep_song0_img = PhotoImage(file = resource_path("data/repeat.png"),master=root)
rep_song0_img = rep_song0_img.subsample(3,3)
rep_song0_but=Button(repeat_lp,image=rep_song0_img,bg=task_bg,bd=0,activebackground=task_bg,cursor='hand2'
                       ,command=rep_song_all,height=47,width=47)
rep_song0_but.grid(row=0,column=0)

####
prev_photo = PhotoImage(file = resource_path("data/previous.png"),master=root)
prev_photo = prev_photo.subsample(2,2)
prev_but=Button(task_fram,image=prev_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=previous_song)
prev_but.pack(side='left',expand=True)

################################# button #################
pause_lp=Label(task_fram,text='',bg=task_bg)
pause_lp.pack(side='left',expand=True)
pause_photo = PhotoImage(file = resource_path("data/pause.png"),master=root)
pause_photo = pause_photo.subsample(2,2)
pause_but=Button(pause_lp,image=pause_photo,bg=task_bg,bd=0,activebackground=task_bg,cursor='hand2',
                 command=pause_song)
pause_but.grid(row=0,column=0)
pause_but.grid_remove()
play_photo = PhotoImage(file = resource_path("data/play.png"),master=root)
play_photo = play_photo.subsample(2,2)
play_but=Button(pause_lp,image=play_photo,bg=task_bg,bd=0,activebackground=task_bg,cursor='hand2',
                command=unpause_song)
play_but.grid(row=0,column=0)

####
next_photo = PhotoImage(file = resource_path("data/next.png"),master=root)
next_photo = next_photo.subsample(2,2)
next_but=Button(task_fram,image=next_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=next_song)
next_but.pack(side='left',expand=True)

volume_information=Label(task_fram,text='',bg=task_bg,fg='black',width=5)
volume_information.pack(side='right',padx=0)

#####scale widget for volume
v_scale=ttk_Scale(task_fram,from_=0, to=100,style='custom.Horizontal.TScale',command=inc_dec_volume,length=60)
v_scale.pack(side='right',fill='x',expand=True,padx=0)

v_scale.bind('<Button-1>', set_val_v_scale)


######speaker
speaker_lp=Label(task_fram,bg=task_bg)
speaker_lp.pack(side='right')
mute_photo = PhotoImage(file = resource_path("data/mute.png"),master=root)
mute_photo = mute_photo.subsample(11,11)
mute_but=Button(speaker_lp,image=mute_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=unmute)
mute_but.grid(row=0,column=0)
mute_but.grid_remove()
vol20_photo = PhotoImage(file = resource_path("data/volume1.png"),master=root)
vol20_photo = vol20_photo.subsample(11,11)
vol20_but=Button(speaker_lp,image=vol20_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=mute)
vol20_but.grid(row=0,column=0)
vol20_but.grid_remove()

vol100_photo = PhotoImage(file = resource_path("data/volume3.png"),master=root)
vol100_photo = vol100_photo.subsample(11,11)
vol100_but=Button(speaker_lp,image=vol100_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=mute)
vol100_but.grid(row=0,column=0)
vol100_but.grid_remove()

vol70_photo = PhotoImage(file = resource_path("data/volume2.png"),master=root)
vol70_photo = vol70_photo.subsample(11,11)
vol70_but=Button(speaker_lp,image=vol70_photo,bg=task_bg,bd=0,activebackground=activebg,cursor='hand2',
                 command=mute)
vol70_but.grid(row=0,column=0)




##################################  ListBox
listbox = Listbox(root_2,bg='grey15',fg='goldenrod',font=('',17),activestyle='none',bd=0,cursor='hand2'
                  ,disabledforeground='white',highlightbackground='white',highlightcolor='white',
                  highlightthickness=0,selectbackground='#00ccff',selectborderwidth=10,
                  selectforeground='darkgreen',
                  relief='flat'
                  )
listbox.pack(expand=True,fill='both',padx=0)
listbox.bind('<Double-1>',listbox_command)
bind_listbox_key()
root_1.bind("<Button-1>",show_playlist_window)
listbox.bind("<Button-3>",popup_menu)
listbox.bind('<B1-Motion>', lambda event : move_item_from_listbox(event,root,listbox))
listbox.bind('<Left>', left_key_comm)
listbox.bind('<Right>', right_key_comm)
listbox.bind('<Return>', listbox_command)


srch_label=Label(root,bg='white')#,width=70,height=10

src_listbox = Listbox(root_2,bg='grey15',fg='goldenrod',font=('',17),bd=0,cursor='hand2',activestyle='none',
                  disabledforeground='white',highlightbackground='white',highlightcolor='white',
                  highlightthickness=0,selectbackground='#00ccff',selectborderwidth=10,
                  selectforeground='darkgreen',relief='flat',)

src_listbox.bind('<Double-1>',listbox_search_cmd)
src_listbox.bind('<B1-Motion>', lambda event : move_item_from_listbox(event,root,listbox))
src_listbox.bind('<Left>', left_key_comm)
src_listbox.bind('<Right>', right_key_comm)

search_icon = PhotoImage(file = resource_path("data/search.png"),master=root)
search_icon = search_icon.subsample(1,1)


search_win_variable=StringVar()
ent_search_win=Entry(root_1,bg='grey20',fg='white',font=('',18),textvariable=search_win_variable,
          highlightthickness=0,highlightcolor='grey45',bd=1
          ,exportselection=0,width=21, insertbackground="grey90", relief="sunken")
ent_search_win.place(x=3,y=10)
ent_search_win.bind('<Return>',enter_search_cmd)
ent_search_win.bind("<FocusIn>", show_search_window)

search_icon1 = PhotoImage(file = resource_path("data/search.png"),master=root)
ent_label_img=Button(ent_search_win,bg='grey20',image=search_icon1,bd=0,height=32,cursor='hand2',command=enter_search_cmd)
ent_label_img.place(x=360,y=3)
search_win_variable.set('Search music')

song_icon = PhotoImage(file = resource_path("data/music1.png"),master=root)
song_icon_label=Label(root_1,bg=root_1_bg,image=song_icon,width=360,height=180,
                      font=('',22))
song_icon_label.place(x=0,y=130)
song_icon_label.bind("<Button-1>",show_playlist_window)
######################################################################################
three_dot_img = PhotoImage(file = resource_path("data/3_dot1.png"),master=root)
three_dot_img_but=Label(song_icon_label,bg=root_1_bg, bd=0,image=three_dot_img)
three_dot_img_but.bind('<Button-1>',three_dot_command_pop_up_menu)
three_dot_img_but.place(x=8,y=0)

#### Youtube video download

Frame_for_created_directory_button_list=Frame(root_1,bg='green',bd=0)
Frame_for_created_directory_button_list.place(x=0,y=320)


Created_Playlist_button_img = PhotoImage(file = resource_path("data/playlist_butn.png"),master=root)

created_directory_button_list=[]

file_path_data=str(Path.home())+"\\music_player.mapl"
if os.path.exists(file_path_data):
    pass
else:        
    file_path_data=resource_path("data/music_player.mapl")
    
data=open(file_path_data, 'r')

###____Adding_Song_in_playlist
add_song_th=Thread(target=get_saved_status_data, daemon = True)
add_song_th.start()

##_____scrollable_frame_for_playlist_name
##data.close()
BUTTONbg = "grey45"
BUTTONfg = "black"
BUTTONbgEn = "grey55"
BUTTONfgEn = "black"

recent_song_plays_list = database['recent']
recent_button_img = PhotoImage(file = resource_path("data/clock.png"),master=root).subsample(1,1)
show_recent_song_window_button=Button(Frame_for_created_directory_button_list,bg=BUTTONbg,
                               width=345,font=('',16,'bold'),compound='left',anchor='w',
                               fg=BUTTONfg,bd=0,relief='flat',image=recent_button_img,
                               command= show_recent_song_window,
                               padx=13,pady=5,text='Recent Plays', cursor="hand2")
show_recent_song_window_button.pack(side='top',anchor='w',fill='x')

show_recent_song_window_button.bind("<Enter>", lambda event: color_change_enter_leave(event,
                                                    bg='grey65',fg='black',nbg='orange',
                                                                               nfg='white'))
show_recent_song_window_button.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                    bg=BUTTONbg,fg='black',nbg='orange',
                                                                              nfg='white'))




playlist_canvas =Canvas(Frame_for_created_directory_button_list,bg='grey25',bd=0, closeenough=0,highlightthickness=0, 
                        confine=1, )
playlist_canvas.pack(fill="both",expand=True)


playlist_scrollable_frame =Frame(playlist_canvas,bg='grey25')


playlist_scrollable_frame.bind("<Configure>",lambda e: playlist_canvas.configure(
    scrollregion=playlist_canvas.bbox("all")))

playlist_canvas.create_window((0, 0), window=playlist_scrollable_frame, anchor="nw")

playlist_canvas.bind("<MouseWheel>", lambda event : playlist_scroll_window.scroll(event))
               
playlist_canvas_root_height=0        
        
        
        

playist__directory=database['playlist']

i=0

for key in playist__directory:
    if key == 'Downloads':
        pack='top'
    else:
        pack='bottom'
    Created_Playlist_button=Button(playlist_scrollable_frame,text=key,bg=BUTTONbg,
                                   width=360,font=('',16,'bold'),compound='left',anchor='w',
                                   fg=BUTTONfg,bd=0,relief='flat',image=Created_Playlist_button_img,
                                   command= functools_partial (user_created_listbox_command, key, False),
                                   padx=13,pady=4, cursor="hand2")
    Created_Playlist_button.pack(side=pack,expand=True,anchor='w',fill='x')
    Created_Playlist_button.bind(
        "<Button-3>",functools_partial(popup_menu_for_create_del_rename_playlist ,button_name=key))
    Created_Playlist_button.bind("<Enter>", lambda event: color_change_enter_leave(event,
                                                        bg=BUTTONbgEn,fg=BUTTONfgEn,nbg='dodger blue',
                                                                                   nfg='white'))
    Created_Playlist_button.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                        bg=BUTTONbg,fg=BUTTONfg,nbg='dodger blue',
                                                                                  nfg='white'))

    Created_Playlist_button.bind("<MouseWheel>", lambda event : playlist_scroll_window.scroll(event))
    created_directory_button_list.append(Created_Playlist_button)
    i+=1



play_frame_bg='grey9'
Frame_for_user_created_listbox=Frame(root_2,bg=play_frame_bg)

Frame_for_user_created_playlist_info=Frame(Frame_for_user_created_listbox,bg=play_frame_bg,
                                           relief='flat',bd=0)
Frame_for_user_created_playlist_info.pack(expand=True,fill='both',side='top')


play_frame_playlist_info_frame=Frame(Frame_for_user_created_playlist_info,bg=play_frame_bg,relief='flat',bd=0)
play_frame_playlist_info_frame.pack(side='right',expand=True,fill='both')

play_frame_playlist_icon_frame=Frame(Frame_for_user_created_playlist_info,bg=play_frame_bg,
                                     relief='flat',bd=0,width=300)
play_frame_playlist_icon_frame.pack(side='left',)

play_frame_playlist_icon = ImageTk.PhotoImage(Image.open( resource_path("data/dj-booth2.png")).resize((300,220),Image.Resampling.LANCZOS), master=root)            

play_frame_playlist_icon_label=Label(play_frame_playlist_icon_frame,image=play_frame_playlist_icon,
                                    bg=play_frame_bg)
play_frame_playlist_icon_label.pack(side='left',ipadx=5,pady=5, ipady=5,expand=True)
play_frame_playlist_icon_label.bind('<Double-1>',play_gif_or_stop)
play_frame_playlist_icon_label.bind("<Enter>", lambda event:color_change_enter_leave(event,bg='grey35',
                                                                                     nbg='white'))
play_frame_playlist_icon_label.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                                    bg=play_frame_bg,nbg='white'))

play_frame_playlist_name_label11=Frame(play_frame_playlist_info_frame,bg=play_frame_bg,
                                     relief='flat',bd=0,height=70)
play_frame_playlist_name_label11.pack(side='top',anchor='w',fill='x',padx=15,pady=0)

play_frame_playlist_name_label=Label(play_frame_playlist_name_label11,text=' Mahadev Aditya',
                                    bg=play_frame_bg,fg='white',font=('',26,'bold italic'),anchor='w',
                                     justify="left",compound='left')

play_frame_playlist_name_label.place(x=0,y=13)
play_frame_playlist_name_label.bind("<Enter>", lambda event:color_change_enter_leave(event,fg='cyan'))
play_frame_playlist_name_label.bind("<Leave>", lambda event:color_change_enter_leave(event,fg='white'))

       

play_frame_num_song_label=Label(play_frame_playlist_info_frame,text=' 20  Songs in playlist',
                                    bg=play_frame_bg,fg='white',anchor='w',font=('',11,'bold'),
                                justify="left",compound='left')#play_frame_bg
play_frame_num_song_label.pack(side='top',anchor='w',padx=20,pady=5)



play_frame_playAllSong_icon = PhotoImage(file = resource_path("data/play_all.png"),master=root)    
play_frame_playAllSong_butn=Button(play_frame_playlist_info_frame,text='  Play All',
                bd=0,relief='flat',bg=play_frame_bg,fg='cyan',font=('',13,'bold italic')
                ,compound='left',image=play_frame_playAllSong_icon,activebackground='grey50',
                activeforeground='dodger blue',command=play_all_butn_command)
play_frame_playAllSong_butn.pack(side='left',anchor='w',ipadx=15,padx=10,pady=20,expand=True)    
play_frame_playAllSong_butn.bind("<Enter>", lambda event:color_change_enter_leave(event,
                                                    bg='grey30',fg='white'))
play_frame_playAllSong_butn.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                    bg=play_frame_bg,fg='cyan'))


play_frame_AddToPlaylist_icon = PhotoImage(file = resource_path("data/add_to.png"),master=root)    
play_frame_AddToPlaylist_butn=Button(play_frame_playlist_info_frame,text='  Add to',
                bd=0,relief='flat',bg=play_frame_bg,fg='cyan',font=('',13,'bold italic')
                ,compound='left',image=play_frame_AddToPlaylist_icon,activebackground='grey50',
                activeforeground='maroon1')
play_frame_AddToPlaylist_butn.pack(side='left',anchor='w',ipadx=10,pady=20,expand=True)
play_frame_AddToPlaylist_butn.bind('<Button-1>',add_to_butn_command)
play_frame_AddToPlaylist_butn.bind("<Enter>", lambda event:color_change_enter_leave(event,
                                                    bg='grey35',fg='gold'))
play_frame_AddToPlaylist_butn.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                    bg=play_frame_bg,fg='cyan'))



play_frame_rename_icon = PhotoImage(file = resource_path("data/pencil.png"),master=root)    
play_frame_rename_butn=Button(play_frame_playlist_info_frame,text='  Rename',
                bd=0,relief='flat',bg=play_frame_bg,fg='cyan2',font=('',13,'bold italic')
                ,compound='left',image=play_frame_rename_icon,activebackground='grey60',
                activeforeground='green',command=rename_butn_command)
play_frame_rename_butn.pack(side='left',anchor='w',ipadx=10,pady=20,expand=True)    
play_frame_rename_butn.bind("<Enter>", lambda event:color_change_enter_leave(event,
                                                    bg='grey30',fg='orange'))
play_frame_rename_butn.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                    bg=play_frame_bg,fg='cyan2'))


play_frame_delete_icon = PhotoImage(file = resource_path("data/delete.png"),master=root)    
play_frame_delete_butn=Button(play_frame_playlist_info_frame,text='  Delete',
                bd=0,relief='flat',bg=play_frame_bg,fg='cyan',font=('',13,'bold italic')
                ,compound='left',image=play_frame_delete_icon,activebackground='grey80',
                activeforeground='red',command=delete_butn_command)
play_frame_delete_butn.pack(side='left',anchor='w',ipadx=10,pady=20,expand=True)

play_frame_delete_butn.bind("<Enter>", lambda event:color_change_enter_leave(event,
                                                    bg='grey30',fg='red'))
play_frame_delete_butn.bind("<Leave>", lambda event:color_change_enter_leave(event,
                                                    bg=play_frame_bg,fg='cyan'))

##_______________________________________________________________________________________________    
Frame_for_user_created_playlist_play=Frame(Frame_for_user_created_listbox,bg='grey15',bd=0)
Frame_for_user_created_playlist_play.pack(expand=True,fill='both',side='top', pady=0)




user_created_listbox = Listbox(Frame_for_user_created_playlist_play,bg='grey15',fg='goldenrod',font=('',17),activestyle='none',bd=0,cursor='hand2'
                  ,disabledforeground='white',highlightbackground='white',highlightcolor='white',
                  highlightthickness=0,selectbackground='#00ccff',selectborderwidth=10,
                  selectforeground='darkgreen',
                  relief='flat'
                  )
user_created_listbox.pack(expand=True,fill='both', side="top")

user_created_listbox.bind('<Double-1>',listbox_command)
user_created_listbox.bind("<Button-3>",popup_menu)
user_created_listbox.bind('<Return>', listbox_command)
user_created_listbox.bind('<Left>', left_key_comm)
user_created_listbox.bind('<Right>', right_key_comm)


you_id=Entry(root_1, bg=root_1_bg, width=384, font=("", 1), relief="flat", cursor="arrow")
you_id.pack(side='bottom', padx=0, pady=0, fill="x")

############### Bind Button
root.bind('<Left>',left_key_comm)
root.bind('<Right>',right_key_comm)
root.bind("<Control-o>",add_1_song_plist)#lambda x:
root.bind("<Control-s>",search_Window)
root.bind("<Control-f>",addsong_crtl_f)
root.bind("<Control-h>",autor)
root.bind("<Control-Shift-f>",feedback )
root.bind("<Control-Shift-F>",feedback )
root.bind("<Key>",on_release)
root.bind("<Control-t>",trasparet_a_colour)
root.bind("<Control-T>",trasparet_a_colour)


##################################:
root.bind("<Control-Shift-c>",print_widget_under_mouse)
root.bind("<Control-Shift-C>",print_widget_under_mouse)
######

##################################  pygame.

root.protocol("WM_DELETE_WINDOW", on_closing_root)

search_icon = PhotoImage(file = resource_path("data/search.png"),master=root)
search_icon = search_icon.subsample(1,1)
playlist_popup = PhotoImage(file = resource_path("data/playlist_popup.png"),master=root)
playlist_popup = playlist_popup.subsample(1,1)

root.bind("<Configure>",lambda event:playlist_scroll_window.configure_height(event))



recent_frame=Frame(root_2, bg="grey20")#root_gr
screen_gr(recent_frame)
recent_frame.bind("<Enter>",destroy_screen_pop_button)
#__pop_up_button_image_for_recent_play
pop_up_pause_photo = PhotoImage(file = resource_path("data/pause_pop_up.png"),master=root)
pop_up_pause_photo = pop_up_pause_photo.subsample(2,2)

pop_up_play_photo = PhotoImage(file = resource_path("data/play_pop_up.png"),master=root)
pop_up_play_photo = pop_up_play_photo.subsample(2,2)
#______________________________________________________   
# 
# print
root.mainloop()
