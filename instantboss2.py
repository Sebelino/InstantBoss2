#!/bin/python2
import sys,time,thread,os

working_dir = os.path.dirname(os.path.realpath(__file__))

def beep(sound):
    os.system("mplayer %s"% sound)

def countdown(message,seconds,file):
    print(message)
    thread.start_new_thread(beep,(file,))
    for i in range(seconds):
        print (seconds-i)
        time.sleep(1)

xmobar_yes = "xmobar" in sys.argv[1:]

is_seconds = "s" in "".join(sys.argv[1:])
time_factor = 1 if is_seconds else 60
filtered_input = [s.replace("s","") for s in sys.argv[1:]]
intervals = filter(lambda x: x.isdigit(),filtered_input)

if not intervals:
    print("Usage:")
    print("python2 %s [OPTION...] [xmobar]"% sys.argv[0])
    print("Example:")
    print("python2 %s 25 5"% sys.argv[0])
    print("toggles between a period of 25 minutes and a period of 5 minutes.")
    sys.exit()
if '0' in intervals:
    print("Don't be stupid.")
    sys.exit()

argument_count = len(intervals)

if xmobar_yes:
    f = open(os.path.join(working_dir,"dat","current_time"),"r+")
    sounds = [os.path.join(working_dir,"%s.wav"% i) for i in range(1,len(intervals)+1)]
    while True:
        for (interval_time,sound) in zip([str(time_factor*int(m)) for m in intervals],sounds):
            beep(sound)
            f.write(interval_time)
            f.seek(0)
            for i in reversed(range(0,int(interval_time))):
                f.write("<fc=#9988FF>%s</fc>"% i)
                f.truncate()
                f.seek(0)
                time.sleep(1)

while True:
    for i in range(0,argument_count):
        countdown("Initiate phase %s."% (i+1)
           ,time_factor*int(intervals[i]),os.path.join(working_dir,"%s.wav"% (i+1)))
