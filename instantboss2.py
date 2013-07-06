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

xmobar_yes = "xmobar" in sys.argv[1:]

intervals = filter(lambda x: x.isdigit(),sys.argv[1:])

if not intervals:
    print("Usage:")
    print("python2 %s [OPTION...] [xmobar]"% sys.argv[0])
    print("Example:")
    print("python2 %s 25 5"% sys.argv[0])
    print("toggles between a period of 25 minutes and a period of 5 minutes.")
    sys.exit()

argument_count = len(intervals)

if xmobar_yes:
    f = open("/home/sebelino/repos/InstantBoss2/dat/current_time","r+")
    sounds = ["%s.wav"% i for i in range(1,len(intervals)+1)]
    while True:
        for (interval_time,sound) in zip([str(60*int(m)) for m in intervals],sounds):
            beep(sound)
            f.write(interval_time)
            f.seek(0)
            for i in reversed(range(0,int(interval_time))):
                f.write(str(i))
                f.truncate()
                f.seek(0)
                time.sleep(1)

while True:
    for i in range(0,argument_count):
        countdown("Initiate phase %s."% i ,60*int(intervals[i]),"%s.wav"% i)
