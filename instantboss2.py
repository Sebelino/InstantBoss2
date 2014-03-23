#!/bin/python2

# To pause the countdown, press enter.
# To resume from the pause, press enter again.
# To quit at any time, enter any string containing non-whitespace and press enter.

import sys,time,thread,os,argparse,select
from pprint import pprint

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

# @return A string that was entered, or None if no string was entered.
def countdown(seconds):
    for i in xrange(seconds):
        print (seconds-i)
        (inp,o,e) = select.select([sys.stdin],[],[],1)
        if inp:
            return sys.stdin.readline().strip()
    return None

def currenttime(topic=''):
    appendix = " - "+topic if topic else ""
    return time.strftime("%Y-%m-%d %H:%M:%S")+appendix

interval_seconds = 60*(args.minutes if args.minutes else 0)+(args.seconds if args.seconds else 0)
interval_seconds = interval_seconds if interval_seconds else sys.maxint

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

intervals = []
iteration = 0
starttime = currenttime(args.topic)
while True:
    if not args.repeat and iteration == 1:
        break
    iteration += 1
    if args.repeat:
        print("Iteration %s"% iteration)
    thread.start_new_thread(beep,("%s.wav"% args.audio,))
    response = countdown(interval_seconds)
    if response != None:
        stoptime = currenttime(args.topic)
        intervals.append([starttime,stoptime])
        if response:
            break
        else:
            response2 = sys.stdin.readline().strip()
            if response2:
                break
            starttime = currenttime(args.topic)

pprint(intervals)
