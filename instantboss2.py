#!/bin/python2

import sys,time,thread,os,argparse,select,csv,re,datetime

parser = argparse.ArgumentParser()
#parser.add_argument("-x","--xmobar",action='store_true',
#    help="Enable this if xmobar is installed and you want the timer in xmobar to be updated.")
parser.add_argument("-t","--time",type=str,help="H:M:S, where H=hours, M=minutes and S=seconds.")
#parser.add_argument("-r","--repeat",action='store_true',help="Reset the timer when it reaches zero.")
parser.add_argument("subject",type=str,help="The subject you are working on.")
parser.add_argument("-a","--audio",default='sound/1',metavar='file',type=str,
    help="The name of the .wav file, excluding the extension. \"1\" by default.")
parser.add_argument("-o","--output",type=str,metavar='file',default='schedule.csv',
    help="The file to which the output should be written. If not specified, the output will\
    be written to ./dat/schedule.csv.")
args = parser.parse_args()

working_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = "dat"

def beep(sound):
    os.system("mplayer %s &> /dev/null"% sound)

# @return A string that was entered, or None if no string was entered.
def countdown(seconds):
    appendix = ''
    if seconds < 100800:
        endtime = datetime.datetime.now()+datetime.timedelta(seconds=seconds)
        appendix = '\tends=%s'% str(endtime.strftime('%H:%M:%S'))
    for i in xrange(seconds):
        print (str(seconds-i)+appendix+'\t%d %%'% int(100.0*i/seconds))
        (inp,o,e) = select.select([sys.stdin],[],[],1)
        if inp:
            return sys.stdin.readline().strip()
    return None

def currenttime():
    fmt = "%Y-%m-%dT%H:%M:%S"
    return time.strftime(fmt)

def writecsv(table,fname):
    with open(os.path.join(data_dir,fname),'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)

if args.time and not re.match('\d*:\d*:\d*',args.time):
    print "Incorrectly formatted time. See --help."
    sys.exit()
(hs,ms,ss) = args.time.split(':') if args.time else ('','','')
interval_seconds = (int(hs) if hs else 0)*60*60+(int(ms) if ms else 0)*60+(int(ss) if ss else 0)
interval_seconds = interval_seconds if interval_seconds else sys.maxint

#if args.xmobar:
#    f = open(os.path.join(working_dir,data_dir,"current_time"),"r+")
#    sounds = [os.path.join(working_dir,"%s.wav"% i) for i in range(1,len(intervals)+1)]
#    while True:
#        for (interval_time,sound) in zip([str(time_factor*int(m)) for m in intervals],sounds):
#            beep(sound)
#            f.write(interval_time)
#            f.seek(0)
#            for i in reversed(range(0,int(interval_time))):
#                f.write("<fc=#9988FF>%s</fc>"% i)
#                f.truncate()
#                f.seek(0)
#                time.sleep(1)

intervals = []
iteration = 0
starttime = currenttime()
response = countdown(interval_seconds)
stoptime = currenttime()
intervals.append((starttime,stoptime,args.subject))
thread.start_new_thread(beep,("%s.wav"% args.audio,))

print intervals
writecsv(intervals,args.output)

