import pygame,sys,time
import thread

pygame.init()

def beep(sound):
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play()

def countdown(message,seconds,file):
    print(message)
    thread.start_new_thread(beep,(file,))
    for i in range(seconds):
        print (seconds-i)
        time.sleep(1)

if len(sys.argv) <= 1:
    print("Please apply 1 or more arguments.")
    sys.exit()

argument_count = len(sys.argv)-1
while True:
    for i in range(1,argument_count+1):
        countdown("Initiate phase %s."% i ,60*int(sys.argv[i]),"%s.wav"% i)
