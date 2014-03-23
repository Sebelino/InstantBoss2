#!/bin/python2
import sys,time,thread,os,argparse

parser = argparse.ArgumentParser()
parser.add_argument("-x","--xmobar",action='store_true',
    help="Enable this if xmobar is installed and you want the timer in xmobar to be updated.")
parser.add_argument("-s","--seconds",type=int,help="S, where 60*M+S is the number of seconds between each interval.")
parser.add_argument("-m","--minutes",type=int,help="M, where 60*M+S is the number of seconds between each interval.")
parser.add_argument("-r","--repeat",action='store_true',help="Reset the timer when it reaches zero.")
parser.add_argument("-t","--topic",type=str,help="The subject you are working on.")
parser.add_argument("-a","--audio",default='1',metavar='file',type=str,
    help="The name of the .wav file, excluding the extension. \"1\" by default.")
args = parser.parse_args()

working_dir = os.path.dirname(os.path.realpath(__file__))

def beep(sound):
    os.system("mplayer %s &> /dev/null"% sound)

def countdown(message,seconds,file):
    print(message)
    thread.start_new_thread(beep,(file,))
    for i in range(seconds):
        print (seconds-i)
        time.sleep(1)

if not args.seconds and not args.minutes:
    print "Parameters missing. Rerun with --help for details."
    sys.exit()
interval_seconds = 60*(args.minutes if args.minutes else 0)+(args.seconds if args.seconds else 0)

if not interval_seconds:
    print("Don't be stupid.")
    sys.exit()

if args.xmobar:
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

iteration = 0
while True:
    if not args.repeat and iteration == 1:
        break
    iteration += 1
    countdown("Iteration %s."% iteration,
        interval_seconds,os.path.join(working_dir,"%s.wav"% args.audio))
    print time.strftime("%Y-%m-%d %H:%M:%S")+(" - "+args.topic if args.topic else "")
