# -*- coding: utf-8 -*-
"""
Created on Mon Apr 06 17:20:21 2020
Updated on Wed Apr 29 15:37:00 2020

@author: Jae-Hyeong Lee
"""
### SSH Login ###
import paramiko

### OS, sys ###
import os
import sys

### Header for TimeStamp ###
import time
from datetime import datetime

### Header for TTS play ###
import winsound as ws
import wave
import pygame

### Global Var
path1 = os.getcwd()+"/fraud_alarm_1.txt"
path2 = os.getcwd()+"/fraud_alarm_2.txt"
cycle = 0
old_log_1 = {}
new_log_1 = {}
old_log_2 = {}
new_log_2 = {}
FLAG_c_num = 0
FLAG_list = [0,0,0,0]

### Window Console Font ###
from colorama import init, Fore
init(autoreset=True)
###-------------------------------- Object List 선언 및 Class 정의-------###
### 발신번호 Object List&Set ###
old_number_list=[]
old_num_set=set()
new_number_list=[]
new_num_set=set()
class c_number:
    number = 0
    called_count = 0
    call_try = 0
    complete_rate = 0
    AHT = 0
    def __init__(self, number, called_count, call_try, complete_rate, AHT):
        self.number = number
        self.called_count = called_count
        self.call_try = call_try
        self.complete_rate = complete_rate
        self.AHT = AHT  
        
    def __lt__(self, other):
        return self.called_count < other.called_count
    
    def __le__(self, other):
        return self.called_count <= other.called_count
    
    def __gt__(self, other):
        return self.called_count > other.called_count
    
    def __ge__(self, other):
        return self.called_count >= other.called_count
    
    def __eq__(self, other):
        return self.called_count == other.called_count
   
### 관리국가 Object List&Set ###
old_country_list=[]
old_country_set=set()
new_country_list=[]
new_country_set=set()
class country:
    last_call = "0000"
    number = 0
    cooperation = "XXX"
    country = "XXX"
    country_count = 0
    total_call = 0
    duration = 0
    prohibit = "X"

    def __init__(self, last_call, number, cooperation, country, country_count, total_call, duration, prohibit):
        self.last_call = last_call
        self.number = number
        self.cooperation = cooperation
        self.country =  country
        self.country_count = country_count
        self.total_call = total_call  
        self.duration = duration  
        self.prohibit = prohibit
        
    def __lt__(self, other):
        return self.number < other.number
    
    def __le__(self, other):
        return self.number <= other.number
    
    def __gt__(self, other):
        return self.number > other.number
    
    def __ge__(self, other):
        return self.number >= other.number
    
    def __eq__(self, other):
        return self.number == other.number

### 인터넷전화 Object List&Set ###
old_voip_list=[]
old_voip_set=set()
new_voip_list=[]
new_voip_set=set()
class voip:
    last_call = 0
    number = 0
    cooperation = "XXX"
    country = "XXX"
    country_count = 0
    total_call = 0
    duration = 0
    prohibit = "X"

    def __init__(self, last_call, number, cooperation, country, country_count, total_call, duration, prohibit):
        self.last_call = last_call
        self.number = number
        self.cooperation = cooperation
        self.country =  country
        self.country_count = country_count
        self.total_call = total_call  
        self.duration = duration  
        self.prohibit = prohibit
        
    def __lt__(self, other):
        return self.last_call < other.last_call
    
    def __le__(self, other):
        return self.last_call <= other.last_call
    
    def __gt__(self, other):
        return self.last_call > other.last_call
    
    def __ge__(self, other):
        return self.last_call >= other.last_call
    
    def __eq__(self, other):
        return self.last_call == other.last_call

### 유선상접 Object List&Set ###
old_wire_list=[]
old_wire_set=set()
new_wire_list=[]
new_wire_set=set()
class wire:
    last_call = 0
    number = 0
    cooperation = "XXX"
    country = "XXX"
    country_count = 0
    total_call = 0
    duration = 0
    prohibit = "X"

    def __init__(self, last_call, number, cooperation, country, country_count, total_call, duration, prohibit):
        self.last_call = last_call
        self.number = number
        self.cooperation = cooperation
        self.country =  country
        self.country_count = country_count
        self.total_call = total_call  
        self.duration = duration  
        self.prohibit = prohibit
        
    def __lt__(self, other):
        return self.last_call < other.last_call
    
    def __le__(self, other):
        return self.last_call <= other.last_call
    
    def __gt__(self, other):
        return self.last_call > other.last_call
    
    def __ge__(self, other):
        return self.last_call >= other.last_call
    
    def __eq__(self, other):
        return self.last_call == other.last_call        

### 무선상접 Object List&Set ###
old_wireless_list=[]
old_wireless_set=set()
new_wireless_list=[]
new_wireless_set=set()
class wireless:
    last_call = 0
    number = 0
    num_count = 0
    total_call = 0
    duration = 0
    prohibit = "X"

    def __init__(self, last_call, number, num_count, total_call, duration, prohibit):
        self.last_call = last_call
        self.number = number
        self.num_count = num_count
        self.total_call = total_call  
        self.duration = duration  
        self.prohibit = prohibit
        
    def __lt__(self, other):
        return self.last_call < other.last_call
    
    def __le__(self, other):
        return self.last_call <= other.last_call
    
    def __gt__(self, other):
        return self.last_call > other.last_call
    
    def __ge__(self, other):
        return self.last_call >= other.last_call
    
    def __eq__(self, other):
        return self.last_call == other.last_call        
###-------------------------------- Object List 선언 및 Class 정의-------###

### Print TimeStamp ###
def get_time():
    time_stamp = datetime.fromtimestamp(time.time())
    return time_stamp
### Play Beep Sound ###
def beepsound():
    freq = 1000    # range : 37 ~ 32767
    dur = 100     # ms
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
    ws.Beep(freq, dur) # winsound.Beep(frequency, duration)
### Play TTS ###

def play_sound_c_num(FLAG_c_num, FLAG_list) :   
    play_flag = int(sum(FLAG_list))
    
    if FLAG_c_num == 1 :
        clock = pygame.time.Clock()
        play_path = "DB/1.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)     
            
    if play_flag == 0 :
        clock = pygame.time.Clock()
        play_path = "DB/0.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)        

def play_sound(FLAG_list) :   
        
    if FLAG_list[0] == 1:
        clock = pygame.time.Clock()
        play_path = "DB/2.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)        
        
    if FLAG_list[1] == 1:
        clock = pygame.time.Clock()
        play_path = "DB/3.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)        
        
    if FLAG_list[2] == 1:   
        clock = pygame.time.Clock()
        play_path = "DB/4.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)        
        
    if FLAG_list[3] == 1:   
        clock = pygame.time.Clock()
        play_path = "DB/5.wav"
        file_wav = wave.open(play_path)
        frequency = file_wav.getframerate()
        pygame.mixer.init(frequency=frequency)
        pygame.mixer.music.load(play_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            clock.tick(70)      

    clock = pygame.time.Clock()
    play_path = "DB/0.wav"
    file_wav = wave.open(play_path)
    frequency = file_wav.getframerate()
    pygame.mixer.init(frequency=frequency)
    pygame.mixer.music.load(play_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        clock.tick(70)
      

def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

### Login Device ###
def update_log():
    #create Client
    ssh=paramiko.SSHClient()
    #Host Key setting
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    #Login Info.
    ssh.connect(hostname='xxx.xxx.xxx.xxx',port='xxxx', username='xxxx', password='xxxx')
    
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.exec_command("sh fraud-inc.sh > fraud_alarm.txt")    
    status = channel.recv_exit_status()
    if(status == 1):
        print(Fore.YELLOW+"1차 - 서버 접속 및 커맨드 실행 완료")
        sftp = ssh.open_sftp()
        sftp.get('xxxx/fraud_alarm.txt',path1)
        sftp.close()       
def update_log_2():
    #create Client
    ssh=paramiko.SSHClient()
    #Host Key setting
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())    
    #Login Info.
    ssh.connect(hostname='xxx.xxx.xxx.xxx',port='xxxx', username='xxxx', password='xxxx')
    
    transport = ssh.get_transport()
    channel = transport.open_session()
    channel.exec_command("sh fraud.sh > fraud_alarm.txt")    
    status = channel.recv_exit_status()
    if(status == 1):
        print(Fore.YELLOW+"2차 - 서버 접속 및 커맨드 실행 완료")
        sftp = ssh.open_sftp()
        sftp.get('xxxx/fraud_alarm.txt',path2)
        sftp.close()    

### Read Log ###
def read_log(path):
    temp_log = {}   
    f = open(path,'r',encoding='euc-kr')
    temp_log = f.read().splitlines()
    temp_log = ' '.join(temp_log).split()
    temp_log = remove_values_from_list(temp_log, '|')
    f.close()  
    return temp_log

### Parse Log ###
def parse_log_1():
    for i in range(16, len(old_log_1)-1,5):         
            c = c_number(old_log_1[i],old_log_1[i+1],old_log_1[i+2],old_log_1[i+3],old_log_1[i+4])
            old_number_list.append(c)
    for i in range(16, len(new_log_1)-1,5):         
            c = c_number(new_log_1[i],new_log_1[i+1],new_log_1[i+2],new_log_1[i+3],new_log_1[i+4])
            new_number_list.append(c)
def parse_log_2():
    token = "###"
    token_count = 0
    headline = ['###','FRUAD','FRAUD','TO','FROM','특별', '관리', '국가','인터넷전화', '유선', '무선', '상접','마지막통화', '발신번호', '사업자', '국가명', '국가수', '전체콜수', '통화시간', '차단여부','착신번호갯수']
    
    i=4
    while i<len(old_log_2) :        
        if (old_log_2[i] in headline):
            if (old_log_2[i] == token):
                token_count = token_count+1
                i=i+1
                continue
            else:
                i=i+1
                continue
        elif (token_count == 2):            
            if(old_log_2[i+8] not in headline):
                c = country(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_country_list.append(c)
                i=i+8
                continue
            elif(old_log_2[i+8]==token):
                c = country(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_country_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue
        elif (token_count == 4):    
            if(old_log_2[i+8] not in headline):                
                c = voip(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_voip_list.append(c)                
                i=i+8        
                continue
            elif(old_log_2[i+8]==token):
                c = voip(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_voip_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue
        elif (token_count == 6):

            if(old_log_2[i+8] not in headline):
                c = wire(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_wire_list.append(c)                
                i=i+8 
                continue
            elif(old_log_2[i+8]==token):
                c = wire(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5],old_log_2[i+6],old_log_2[i+7])
                old_wire_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue                      
        elif (token_count == 8):      
            c = wireless(old_log_2[i],old_log_2[i+1],old_log_2[i+2],old_log_2[i+3],old_log_2[i+4],old_log_2[i+5])
            old_wireless_list.append(c)  
            i=i+6                              
            if(i >= (len(old_log_2)-1)):
                break
            else:
                continue
        else:
            i=i+1
            continue
    i=4
    token_count = 0
    while i<len(new_log_2) :        
        if (new_log_2[i] in headline):
            if (new_log_2[i] == token):
                token_count = token_count+1
                i=i+1
                continue
            else:
                i=i+1
                continue
        elif (token_count == 2):            
            if(new_log_2[i+8] not in headline):
                c = country(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_country_list.append(c)
                i=i+8
                continue
            elif(new_log_2[i+8]==token):
                c = country(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_country_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue
        elif (token_count == 4):    
            if(new_log_2[i+8] not in headline):                
                c = voip(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_voip_list.append(c)                
                i=i+8        
                continue
            elif(new_log_2[i+8]==token):
                c = voip(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_voip_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue
        elif (token_count == 6):

            if(new_log_2[i+8] not in headline):
                c = wire(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_wire_list.append(c)                
                i=i+8 
                continue
            elif(new_log_2[i+8]==token):
                c = wire(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5],new_log_2[i+6],new_log_2[i+7])
                new_wire_list.append(c)
                i=i+8
                continue
            else:
                i=i+1
                continue                      
        elif (token_count == 8):      
            c = wireless(new_log_2[i],new_log_2[i+1],new_log_2[i+2],new_log_2[i+3],new_log_2[i+4],new_log_2[i+5])
            new_wireless_list.append(c)  
            i=i+6                              
            if(i >= (len(new_log_2)-1)):
                break
            else:
                continue
        else:
            i=i+1
            continue
        
### Compare Old VS. New ###
def is_diff_1(old_log, new_log):       
    parse_log_1()
    FLAG_c_num=0
    FLAG=0
    
    for i in range(0,len(old_number_list)):
        old_num_set.add(old_number_list[i].number)
    for i in range(0,len(new_number_list)):        
        new_num_set.add(new_number_list[i].number)
    
    same_list = list(old_num_set&new_num_set)
    diff_list_A = list(old_num_set-new_num_set)
    diff_list_B = list(new_num_set-old_num_set)
    
    if( len(old_number_list) != len(new_number_list)):
        print(Fore.RED+"###"+Fore.GREEN + "등록 발신번호 List - "+ Fore.RED + " Count 변화 발생###")
        if (len(old_number_list) > len(new_number_list)):
            if(len(new_number_list) == 0):
                print("#-----------------------------------------------------------#")                
                i=0                      
                while i<len(diff_list_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[i])
                    i=i+1                
                print("#-----------------------------------------------------------#")
                print("#등록 발번| 2차 조회- 없음")                    
                print("#-----------------------------------------------------------#")                      
            elif( (len(new_number_list) != 0) and (len(same_list) != 0)):
                i=0
                while i<len(same_list) :
                    print("#-----------------------------------------------------------#")
                    print("#등록 발번| 1차 조회-",(i+1),": ",same_list[i])
                    print("#등록 발번| 2차 조회-",(i+1),": ",same_list[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                    
                j=0                      
                while j<len(diff_list_A) :                    
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")     
                if( len(diff_list_B) != 0):
                    j=0
                    while j < len(diff_list_B):
                        print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[j])
                        i=i+1                                   
                        j=j+1
                print("#-----------------------------------------------------------#")                                          
            else:                                                   
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")   
        else:     
            if(len(old_number_list) == 0):                
                print("#-----------------------------------------------------------#")
                print("#등록 발번| 1차 조회- 없음")                                    
                i=0
                print("#-----------------------------------------------------------#")                
                while i<len(diff_list_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[i])
                    i=i+1                
                print("#-----------------------------------------------------------#")                                    
            elif( (len(old_number_list) != 0) and (len(same_list) != 0)):
                i=0
                while i<len(same_list) :
                    print("#-----------------------------------------------------------#")
                    print("#등록 발번| 1차 조회-",(i+1),": ",same_list[i])
                    print("#등록 발번| 2차 조회-",(i+1),": ",same_list[i])
                    i=i+1

                print("#-----------------------------------------------------------#")                
                if(len(diff_list_A) != 0):
                    j=0      
                    while j < len(diff_list_A):
                        print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[j])
                        i=i+1
                        j=j+1
                print("#-----------------------------------------------------------#")
                j=0                
                while j<len(diff_list_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[j])            
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                        
            print("Count :", len(new_number_list) - len(old_number_list))
            print("#-----------------------------------------------------------#")            
        FLAG_c_num = 1                      
    else:
        print(Fore.GREEN + "=====등록 발신번호 List - Count 변화 없음=====")
        if( old_num_set == new_num_set) :
            if( len(old_number_list) == 0):
                print(Fore.YELLOW + "=====등록 발신 번호 List - 등록데이터 없음 ====")                                        
                print("#-----------------------------------------------------------#")
                print("#등록 발번| 1차 조회- 없음")
                print("#등록 발번| 2차 조회- 없음")                                
                print("#-----------------------------------------------------------#")                            
            else:
                for i in range(0,len(same_list)):
                    print("#-----------------------------------------------------------#")
                    print("#등록 발번| 1차 조회-",(i+1),": ",same_list[i])
                    print("#등록 발번| 2차 조회-",(i+1),": ",same_list[i])                                
                print("#-----------------------------------------------------------#")            
            FLAG_c_num = 0           
        else:
            print(Fore.RED+"###"+Fore.GREEN + "등록 발신번호 List - "+ Fore.RED + "항목 변화 발생###")                      
                  
            if (len(same_list) == 0) :
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                                                  
            else:
                for i in range(0,len(same_list)):
                    print("#-----------------------------------------------------------#")
                    print("#등록 발번| 1차 조회-",(i+1),": ",same_list[i])
                    print("#등록 발번| 2차 조회-",(i+1),": ",same_list[i])                                                 
                print("#-----------------------------------------------------------#")            
                i=0      
                while i < len(diff_list_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                            
                i=0
                while i < len(diff_list_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")            
            FLAG_c_num = 1
    FLAG = FLAG_c_num
    return FLAG
        
def is_diff_2(old_log_2, new_log_2):       
    FLAG_list = [0,0,0,0]
    parse_log_2()
    
    """####################################################################"""
    ### 특별 관리 국가 ###
    for i in range(0,len(old_country_list)):
        old_country_set.add(old_country_list[i].number)
    for i in range(0,len(new_country_list)):        
        new_country_set.add(new_country_list[i].number)    
    same_list_country = list(old_country_set&new_country_set)
    diff_list_country_A = list(old_country_set-new_country_set)
    diff_list_country_B = list(new_country_set-old_country_set)     

    if( len(old_country_list) != len(new_country_list)):
        print(Fore.RED+"###"+Fore.GREEN + "특별 관리 국가 List - "+ Fore.RED + " Count 변화 발생###")        
        if (len(old_country_list) > len(new_country_list)):            
            if( len(new_country_list) == 0 ):
                print("#-----------------------------------------------------------#")                
                i=0                      
                while i<len(diff_list_country_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_country_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")
                print("#관리 국가| 2차 조회- 없음")                                             
                print("#-----------------------------------------------------------#")                      
            elif( (len(new_country_list) != 0) and (len(same_list_country) != 0)):
                i=0
                while i<len(same_list_country) :
                    print("#-----------------------------------------------------------#")
                    print("#관리 국가| 1차 조회-",(i+1),": ",same_list_country[i])
                    print("#관리 국가| 2차 조회-",(i+1),": ",same_list_country[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                    
                j=0
                while j < len(diff_list_country_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_country_A[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                            
                if (len(diff_list_country_B) != 0):
                    j=0
                    while j < len(diff_list_country_B):
                        print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_country_B[j])
                        i=i+1                                   
                        j=j+1
                print("#-----------------------------------------------------------#")                          
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_country_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_country_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_country_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_country_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                
        else:                
            if( len(old_country_list) == 0 ):            
                print("#-----------------------------------------------------------#")
                print("#관리 국가| 1차 조회- 없음")                
                i=0
                print("#-----------------------------------------------------------#")
                while i<len(diff_list_country_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_country_B[i])             
                    i=i+1                
                print("#-----------------------------------------------------------#")                    
            elif( (len(old_country_list) != 0) and (len(same_list_country) != 0)):          
                i=0
                while i<len(same_list_country) :
                    print("#-----------------------------------------------------------#")
                    print("#관리 국가| 1차 조회-",(i+1),": ",same_list_country[i])
                    print("#관리 국가| 2차 조회-",(i+1),": ",same_list_country[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                
             
                if(len(diff_list_country_A) != 0):
                    j=0      
                    while j < len(diff_list_country_A):
                        print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_country_A[j])
                        i=i+1
                        j=j+1
                print("#-----------------------------------------------------------#")                
                j=0                      
                while j<len(diff_list_country_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_country_B[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                                
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_country_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_country_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_country_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_country_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                          
        print("Count :", len(new_country_list) - len(old_country_list))
        print("#-----------------------------------------------------------#")            
        FLAG_list[0] = 1        
    else:
        print(Fore.GREEN + "=====특별 관리 국가 List - Count 변화 없음=====")
        if( old_country_set == new_country_set) :
            if( len(old_country_list) == 0):
                print(Fore.YELLOW + "=====특별 관리 국가 List - 등록데이터 없음 ====")                        
                print("#-----------------------------------------------------------#")
                print("#관리 국가| 1차 조회- 없음")
                print("#관리 국가| 2차 조회- 없음")                                
                print("#-----------------------------------------------------------#")                            
            else:            
                for i in range(0,len(same_list_country)):            
                    print("#-----------------------------------------------------------#")
                    print("#관리 국가| 1차 조회-",(i+1),": ",same_list_country[i])
                    print("#관리 국가| 2차 조회-",(i+1),": ",same_list_country[i])
                print("#-----------------------------------------------------------#")                         
        else:
            print(Fore.RED+"###"+Fore.GREEN + "특별 관리 국가 List - "+ Fore.RED + "항목 변화 발생###")   
            if( len(same_list_country) == 0):
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_country_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_country_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_country_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_country_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                                                                                 
            else:
                for i in range(0,len(same_list_country)):
                    print("#-----------------------------------------------------------#")
                    print("#관리 국가| 1차 조회-",(i+1),": ",same_list_country[i])
                    print("#관리 국가| 2차 조회-",(i+1),": ",same_list_country[i])                                                     
                print("#-----------------------------------------------------------#")                          
                i=0        
                while i < len(diff_list_country_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_country_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                              
                i=0            
                while i < len(diff_list_country_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_country_B[i])
                    i=i+1       
                print("#-----------------------------------------------------------#")
            FLAG_list[0] = 1        
    """####################################################################"""    
    
    
    """####################################################################"""
    ### 인터넷전화 ###
    for i in range(0,len(old_voip_list)):
        old_voip_set.add(old_voip_list[i].number)
    for i in range(0,len(new_voip_list)):        
        new_voip_set.add(new_voip_list[i].number)    
    same_list_voip = list(old_voip_set&new_voip_set)
    diff_list_voip_A = list(old_voip_set-new_voip_set)
    diff_list_voip_B = list(new_voip_set-old_voip_set)      
     
    
    if( len(old_voip_list) != len(new_voip_list)):
        print(Fore.RED+"###"+Fore.GREEN + "인터넷전화 List - "+ Fore.RED + " Count 변화 발생###")        
        if (len(old_voip_list) > len(new_voip_list)):            
            if( len(new_voip_list) == 0 ):
                print("#-----------------------------------------------------------#")                
                i=0                      
                while i<len(diff_list_voip_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_voip_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")
                print("#인터넷전화| 2차 조회- 없음")                                             
                print("#-----------------------------------------------------------#")                      
            elif( (len(new_voip_list) != 0) and (len(same_list_voip) != 0)):
                i=0
                while i<len(same_list_voip) :
                    print("#-----------------------------------------------------------#")
                    print("#인터넷전화| 1차 조회-",(i+1),": ",same_list_voip[i])
                    print("#인터넷전화| 2차 조회-",(i+1),": ",same_list_voip[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                    
                j=0
                while j<len(diff_list_voip_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_voip_A[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                            
                if (len(diff_list_voip_B) != 0):
                    j=0
                    while j < len(diff_list_voip_B):
                        print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_voip_B[j])
                        i=i+1                                   
                        j=j+1
                print("#-----------------------------------------------------------#")                          
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_voip_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_voip_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_voip_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_voip_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                
        else:                
            if( len(old_voip_list) == 0 ):            
                print("#-----------------------------------------------------------#")
                print("#인터넷전화| 1차 조회- 없음")                
                i=0
                print("#-----------------------------------------------------------#")
                while i<len(diff_list_voip_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_voip_B[i])             
                    i=i+1                
                print("#-----------------------------------------------------------#")                    
            elif( (len(old_voip_list) != 0) and (len(same_list_voip) != 0)):          
                i=0
                while i<len(same_list_voip) :
                    print("#-----------------------------------------------------------#")
                    print("#인터넷전화| 1차 조회-",(i+1),": ",same_list_voip[i])
                    print("#인터넷전화| 2차 조회-",(i+1),": ",same_list_voip[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                
             
                if(len(diff_list_voip_A) != 0):
                    j=0      
                    while j < len(diff_list_voip_A):
                        print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_voip_A[j])
                        i=i+1
                        j=j+1
                print("#-----------------------------------------------------------#")                
                j=0                      
                while j<len(diff_list_voip_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_voip_B[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                                
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_voip_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_voip_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_voip_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_voip_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                          
        print("Count :", len(new_voip_list) - len(old_voip_list))
        print("#-----------------------------------------------------------#")            
        FLAG_list[1] = 1        
    else:
        print(Fore.GREEN + "=====인터넷전화 List - Count 변화 없음=====")
        if( old_voip_set == new_voip_set) :
            if( len(old_voip_list) == 0):
                print(Fore.YELLOW + "=====인터넷전화 List - 등록데이터 없음 ====")                        
                print("#-----------------------------------------------------------#")
                print("#인터넷전화| 1차 조회- 없음")
                print("#인터넷전화| 2차 조회- 없음")                                
                print("#-----------------------------------------------------------#")                            
            else:            
                for i in range(0,len(same_list_voip)):            
                    print("#-----------------------------------------------------------#")
                    print("#인터넷전화| 1차 조회-",(i+1),": ",same_list_voip[i])
                    print("#인터넷전화| 2차 조회-",(i+1),": ",same_list_voip[i])
                print("#-----------------------------------------------------------#")                         
        else:
            print(Fore.RED+"###"+Fore.GREEN + "인터넷전화 List - "+ Fore.RED + "항목 변화 발생###")   
            if( len(same_list_voip) == 0):
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_voip_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_voip_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_voip_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_voip_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                                                                                 
            else:
                for i in range(0,len(same_list_voip)):
                    print("#-----------------------------------------------------------#")
                    print("#인터넷전화| 1차 조회-",(i+1),": ",same_list_voip[i])
                    print("#인터넷전화| 2차 조회-",(i+1),": ",same_list_voip[i])                                                     
                print("#-----------------------------------------------------------#")                          
                i=0        
                while i < len(diff_list_voip_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_voip_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                              
                i=0            
                while i < len(diff_list_voip_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_voip_B[i])
                    i=i+1       
                print("#-----------------------------------------------------------#")
            FLAG_list[1] = 1      
    """####################################################################"""
    
    
    """####################################################################"""                
    ### 유선 상접 ###
    for i in range(0,len(old_wire_list)):
        old_wire_set.add(old_wire_list[i].number)
    for i in range(0,len(new_wire_list)):        
        new_wire_set.add(new_wire_list[i].number)    
    same_list_wire = list(old_wire_set&new_wire_set)
    diff_list_wire_A = list(old_wire_set-new_wire_set)
    diff_list_wire_B = list(new_wire_set-old_wire_set)      
    
    if( len(old_wire_list) != len(new_wire_list)):
        print(Fore.RED+"###"+Fore.GREEN + "유선 상접 List - "+ Fore.RED + " Count 변화 발생###")        
        if (len(old_wire_list) > len(new_wire_list)):            
            if( len(new_wire_list) == 0 ):
                print("#-----------------------------------------------------------#")                
                i=0                      
                while i<len(diff_list_wire_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wire_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")
                print("#유선 상접| 2차 조회- 없음")                                             
                print("#-----------------------------------------------------------#")                      
            elif( (len(new_wire_list) != 0) and (len(same_list_wire) != 0)):
                i=0
                while i<len(same_list_wire) :
                    print("#-----------------------------------------------------------#")
                    print("#유선 상접| 1차 조회-",(i+1),": ",same_list_wire[i])
                    print("#유선 상접| 2차 조회-",(i+1),": ",same_list_wire[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                    
                j=0
                while j<len(diff_list_wire_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wire_A[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                            
                if (len(diff_list_wire_B) != 0):
                    j=0
                    while j < len(diff_list_wire_B):
                        print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wire_B[j])
                        i=i+1                                   
                        j=j+1
                print("#-----------------------------------------------------------#")                          
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wire_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_wire_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wire_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_wire_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                
        else:                
            if( len(old_wire_list) == 0 ):            
                print("#-----------------------------------------------------------#")
                print("#유선 상접| 1차 조회- 없음")                
                i=0
                print("#-----------------------------------------------------------#")
                while i<len(diff_list_wire_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wire_B[i])             
                    i=i+1                
                print("#-----------------------------------------------------------#")                    
            elif( (len(old_wire_list) != 0) and (len(same_list_wire) != 0)):          
                i=0
                while i<len(same_list_wire) :
                    print("#-----------------------------------------------------------#")
                    print("#유선 상접| 1차 조회-",(i+1),": ",same_list_wire[i])
                    print("#유선 상접| 2차 조회-",(i+1),": ",same_list_wire[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                
             
                if(len(diff_list_wire_A) != 0):
                    j=0      
                    while j < len(diff_list_wire_A):
                        print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wire_A[j])
                        i=i+1
                        j=j+1
                print("#-----------------------------------------------------------#")                
                j=0                      
                while j<len(diff_list_wire_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wire_B[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                                
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wire_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_wire_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wire_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_wire_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                          
        print("Count :", len(new_wire_list) - len(old_wire_list))
        print("#-----------------------------------------------------------#")            
        FLAG_list[2] = 1        
    else:
        print(Fore.GREEN + "=====유선 상접 List - Count 변화 없음=====")
        if( old_wire_set == new_wire_set) :
            if( len(old_wire_list) == 0):
                print(Fore.YELLOW + "=====유선 상접 List - 등록데이터 없음 ====")                        
                print("#-----------------------------------------------------------#")
                print("#유선 상접| 1차 조회- 없음")
                print("#유선 상접| 2차 조회- 없음")                                
                print("#-----------------------------------------------------------#")                            
            else:            
                for i in range(0,len(same_list_wire)):            
                    print("#-----------------------------------------------------------#")
                    print("#유선 상접| 1차 조회-",(i+1),": ",same_list_wire[i])
                    print("#유선 상접| 2차 조회-",(i+1),": ",same_list_wire[i])
                print("#-----------------------------------------------------------#")                         
        else:
            print(Fore.RED+"###"+Fore.GREEN + "유선 상접 List - "+ Fore.RED + "항목 변화 발생###")   
            if( len(same_list_wire) == 0):
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wire_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wire_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wire_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wire_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                                                                                 
            else:
                for i in range(0,len(same_list_wire)):
                    print("#-----------------------------------------------------------#")
                    print("#유선 상접| 1차 조회-",(i+1),": ",same_list_wire[i])
                    print("#유선 상접| 2차 조회-",(i+1),": ",same_list_wire[i])                                                     
                print("#-----------------------------------------------------------#")                          
                i=0        
                while i < len(diff_list_wire_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wire_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                              
                i=0            
                while i < len(diff_list_wire_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wire_B[i])
                    i=i+1       
                print("#-----------------------------------------------------------#")
            FLAG_list[2] = 1      
    """####################################################################"""


    """####################################################################"""    
    ### 무선 상접 ###
    for i in range(0,len(old_wireless_list)):
        old_wireless_set.add(old_wireless_list[i].number)
    for i in range(0,len(new_wireless_list)):        
        new_wireless_set.add(new_wireless_list[i].number)
    
    same_list_wireless = list(old_wireless_set&new_wireless_set)
    diff_list_wireless_A = list(old_wireless_set-new_wireless_set)
    diff_list_wireless_B = list(new_wireless_set-old_wireless_set)    
    
    if( len(old_wireless_list) != len(new_wireless_list)):
        print(Fore.RED+"###"+Fore.GREEN + "무선 상접 List - "+ Fore.RED + " Count 변화 발생###")        
        if (len(old_wireless_list) > len(new_wireless_list)):            
            if( len(new_wireless_list) == 0 ):
                print("#-----------------------------------------------------------#")                
                i=0                      
                while i<len(diff_list_wireless_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wireless_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")
                print("#무선 상접| 2차 조회- 없음")                                             
                print("#-----------------------------------------------------------#")                      
            elif( (len(new_wireless_list) != 0) and (len(same_list_wireless) != 0)):
                i=0
                while i<len(same_list_wireless) :
                    print("#-----------------------------------------------------------#")
                    print("#무선 상접| 1차 조회-",(i+1),": ",same_list_wireless[i])
                    print("#무선 상접| 2차 조회-",(i+1),": ",same_list_wireless[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                    
                j=0
                while j<len(diff_list_wireless_A) :
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wireless_A[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                            
                if (len(diff_list_wireless_B) != 0):
                    j=0
                    while j < len(diff_list_wireless_B):
                        print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wireless_B[j])
                        i=i+1                                   
                        j=j+1
                print("#-----------------------------------------------------------#")                          
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wireless_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_wireless_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wireless_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_wireless_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                
        else:                
            if( len(old_wireless_list) == 0 ):            
                print("#-----------------------------------------------------------#")
                print("#무선 상접| 1차 조회- 없음")                
                i=0
                print("#-----------------------------------------------------------#")
                while i<len(diff_list_wireless_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wireless_B[i])             
                    i=i+1                
                print("#-----------------------------------------------------------#")                    
            elif( (len(old_wireless_list) != 0) and (len(same_list_wireless) != 0)):          
                i=0
                while i<len(same_list_wireless) :
                    print("#-----------------------------------------------------------#")
                    print("#무선 상접| 1차 조회-",(i+1),": ",same_list_wireless[i])
                    print("#무선 상접| 2차 조회-",(i+1),": ",same_list_wireless[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                
             
                if(len(diff_list_wireless_A) != 0):
                    j=0      
                    while j < len(diff_list_wireless_A):
                        print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wireless_A[j])
                        i=i+1
                        j=j+1
                print("#-----------------------------------------------------------#")                
                j=0                      
                while j<len(diff_list_wireless_B) :
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wireless_B[j])
                    i=i+1
                    j=j+1
                print("#-----------------------------------------------------------#")                                                
            else:                      
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wireless_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ", diff_list_wireless_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wireless_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ", diff_list_wireless_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                          
        print("Count :", len(new_wireless_list) - len(old_wireless_list))
        print("#-----------------------------------------------------------#")            
        FLAG_list[3] = 1        
    else:
        print(Fore.GREEN + "=====무선 상접 List - Count 변화 없음=====")
        if( old_wireless_set == new_wireless_set) :
            if( len(old_wireless_list) == 0):
                print(Fore.YELLOW + "=====무선 상접 List - 등록데이터 없음 ====")                        
                print("#-----------------------------------------------------------#")
                print("#무선 상접| 1차 조회- 없음")
                print("#무선 상접| 2차 조회- 없음")                                
                print("#-----------------------------------------------------------#")                            
            else:            
                for i in range(0,len(same_list_wireless)):            
                    print("#-----------------------------------------------------------#")
                    print("#무선 상접| 1차 조회-",(i+1),": ",same_list_wireless[i])
                    print("#무선 상접| 2차 조회-",(i+1),": ",same_list_wireless[i])
                print("#-----------------------------------------------------------#")                         
        else:
            print(Fore.RED+"###"+Fore.GREEN + "무선 상접 List - "+ Fore.RED + "항목 변화 발생###")   
            if( len(same_list_wireless) == 0):
                print("#-----------------------------------------------------------#")                            
                i=0      
                while i < len(diff_list_wireless_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wireless_A[i])
                    i=i+1
                i=0
                print("#-----------------------------------------------------------#")                            
                while i < len(diff_list_wireless_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wireless_B[i])
                    i=i+1                                   
                print("#-----------------------------------------------------------#")                                                                                                 
            else:
                for i in range(0,len(same_list_wireless)):
                    print("#-----------------------------------------------------------#")
                    print("#무선 상접| 1차 조회-",(i+1),": ",same_list_wireless[i])
                    print("#무선 상접| 2차 조회-",(i+1),": ",same_list_wireless[i])                                                     
                print("#-----------------------------------------------------------#")                          
                i=0        
                while i < len(diff_list_wireless_A):
                    print(Fore.RED+"1차 조회| 삭제 항목-",(i+1),": ",diff_list_wireless_A[i])
                    i=i+1
                print("#-----------------------------------------------------------#")                                              
                i=0            
                while i < len(diff_list_wireless_B):
                    print(Fore.RED+"2차 조회| 신규 항목-",(i+1),": ",diff_list_wireless_B[i])
                    i=i+1       
                print("#-----------------------------------------------------------#")
            FLAG_list[3] = 1      
    """####################################################################"""

    
    return FLAG_list

### ----------------------------- ###
### ------------Cycle------------ ###
### ----------------------------- ###


# First Session Login & sh        
update_log()
update_log_2()

while True:
        cycle = cycle+1   
        print(Fore.RED + "\n\n======================================================================")
        print(Fore.CYAN + "현재 감시 Cycle Count : ",cycle)
        print(Fore.RED + "======================================================================")
        
        ###--------------------------------###      
        #1차 파일 - 1차 읽기 전
        # print(get_time(), " : 1차 파일 - 1차 읽기 전")
        #1차 파일 - 1차 읽기 완료
        old_log_1 = read_log(path1)
        print(Fore.YELLOW + str(get_time())+" : 등록 발번 - 1차 읽기 완료")
        ###--------------------------------###        
        #2차 파일 - 1차 읽기 전
        # print(get_time(), " : 2차 파일 - 1차 읽기 전")
        #2차 파일 - 1차 읽기 완료
        old_log_2 = read_log(path2)
        print(Fore.YELLOW + str(get_time())+" : 특별 관리 - 1차 읽기 완료")
        ###--------------------------------###

        
        ###-------수집 주기 200s(175s + 서버접속 및 메모리 해제 ~ 25s) ###--------###
        for i in range(1,176,1):
            sys.stdout.write("■")
            sys.stdout.flush()
            if(((i%35) == 0) ):
                print("")                        
            time.sleep(1)
#            time.sleep(0.01)
        print(Fore.RED + "======================================================================")        
        update_log()
        update_log_2()
        print(Fore.RED + "======================================================================")        
        ###--------------------------------###

        ###--------------------------------###        
        #1차 파일 - 2차 읽기 전
        # print(get_time(), " : 1차 파일 - 2차 읽기 전")
        #1차 파일 - 2차 읽기 완료
        new_log_1 = read_log(path1)
        print(Fore.YELLOW + str(get_time())+" : 등록 발번 - 2차 읽기 완료")
        ###--------------------------------###
        #2차 파일 - 2차 읽기 전
        # print(get_time(), " : 2차 파일 - 2차 읽기 전")       
        #2차 파일 - 2차 읽기 완료
        new_log_2 = read_log(path2)
        print(Fore.YELLOW + str(get_time())+" : 특별 관리 - 2차 읽기 완료")
        print(Fore.RED + "======================================================================")                        
        ###--------------------------------###

                        
        #비교    
        FLAG_c_num = is_diff_1(old_log_1, new_log_1)
        FLAG_list = is_diff_2(old_log_2, new_log_2)
        
        if FLAG_c_num == 1 :
            #알람 발생
            print(Fore.GREEN +"\n#===========================================================#")
            print(Fore.GREEN + str(get_time()) + " : 등록 발번 - "+ Fore.RED +"알람 발생")
            print(Fore.GREEN + "#===========================================================#")
            beepsound()            
            play_sound_c_num(FLAG_c_num,FLAG_list)
        else :
            #알람 미발생
            print("#-----------------------------------------------------------#")
            print(Fore.GREEN +"\n#===========================================================#")
            print(Fore.GREEN +str(get_time()) + " : 등록 발번 - 알람 미발생")
            print(Fore.GREEN +"#===========================================================#")
        print(Fore.BLUE + "================================================================")
                
        
        if (int(sum(FLAG_list)) > 0) :
            #알람 발생
            beepsound()
            
            if(FLAG_list[0] == 1):
                print(Fore.GREEN +"\n#===========================================================#")
                print(Fore.GREEN +str(get_time()) + " : 관리 국가 - "+ Fore.RED +"알람 발생")                
                
            if(FLAG_list[1] == 1):
                print(Fore.GREEN +"\n#===========================================================#")
                print(Fore.GREEN +str(get_time()) + " : 인터넷전화 - "+ Fore.RED +"알람 발생")                
                
            if(FLAG_list[2] == 1):
                print(Fore.GREEN +"\n#===========================================================#")
                print(Fore.GREEN +str(get_time()) + " : 유선 상접 - "+ Fore.RED +"알람 발생")
                
            if(FLAG_list[3] == 1):
                print(Fore.GREEN +"\n#===========================================================#")
                print(Fore.GREEN +str(get_time()) + " : 무선 상접 - "+ Fore.RED +"알람 발생")

            print(Fore.GREEN +"#===========================================================#")                            
            play_sound(FLAG_list)
        else :
            #알람 미발생
            print(Fore.GREEN +"\n#===========================================================#")
            print(Fore.GREEN +str(get_time()) + " : 특별 관리 - 알람 미발생")
            print(Fore.GREEN +"#===========================================================#")
        

#        break;
        ### Destroyer ###
        old_number_list.clear()
        new_number_list.clear()
        old_num_set.clear()
        new_num_set.clear()
        
        old_country_list.clear()
        new_country_list.clear()
        old_country_set.clear()
        new_country_set.clear()
        
        old_voip_list.clear()
        new_voip_list.clear()
        old_voip_set.clear()
        new_voip_set.clear()
        
        old_wire_list.clear()
        new_wire_list.clear()
        old_wire_set.clear()
        new_wire_set.clear()        
        
        old_wireless_list.clear()
        new_wireless_list.clear()
        old_wireless_set.clear()
        new_wireless_set.clear()
        
