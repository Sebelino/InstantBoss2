#!/bin/python2

import sys,time,thread,os,argparse,select,csv,re,datetime

def beep(sound):
    os.system("mplayer %s &> /dev/null"% sound)

"""
Counts down from a number of seconds to zero, printing the remaining number of seconds
each second. Meanwhile, the user may enter some text and press enter, causing the
function to return the entered string immediately.
:param seconds: The number of seconds before the timer runs out.
:param callback: A function that is called each tick. It takes two arguments: the
                 passed and the total number of seconds.
:return: A string that was entered, or None if no string was entered before the timer
         ran out.
"""
def countdown(seconds,callback):
    appendix = ''
    for i in xrange(seconds):
        callback(i,seconds)
        (inp,o,e) = select.select([sys.stdin],[],[],1)
        if inp:
            return sys.stdin.readline().strip()
    return None

def tick(passed,total):
    appendix = ''
    if total < 100800:
        endtime = datetime.datetime.now()+datetime.timedelta(seconds=total)
        appendix = '\tends=%s'% str(endtime.strftime('%H:%M:%S'))
    print (str(total-passed)+appendix+'\t%d %%'% int(100.0*passed/total))

def currenttime():
    fmt = "%Y-%m-%dT%H:%M:%S"
    return time.strftime(fmt)

def writecsv(table,fname):
    with open(fname,'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(table)

def execute(subject,time,audio,output):
    if not re.match('\d*:\d*:\d*',time):
        print "Incorrectly formatted time. See --help."
        sys.exit()

    (hs,ms,ss) = time.split(':')
    interval_seconds = (int(hs) if hs else 0)*60*60+(int(ms) if ms else 0)*60+(int(ss) if ss else 0)

    intervals = []
    iteration = 0
    starttime = currenttime()
    response = countdown(interval_seconds,tick)
    stoptime = currenttime()
    intervals.append((starttime,stoptime,subject))
    thread.start_new_thread(beep,(audio,))

    print intervals
    writecsv(intervals,output)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("subject",type=str,help="The subject you are working on.")
    parser.add_argument("time",type=str,help="H:M:S, where H=hours, M=minutes and S=seconds.")
    parser.add_argument("audio",metavar='path',type=str,help="The name of the .wav file, including the extension.")
    parser.add_argument("output",type=str,metavar='path',
        help="The file to which the output should be written.")
    args = parser.parse_args()

    execute(args.subject,args.time,args.audio,args.output)
    sys.exit(0)

