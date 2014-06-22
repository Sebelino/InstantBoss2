#!/bin/python2

import sys,time,thread,os,argparse,select,csv,datetime,re

""" :returns A processed representation of the csv file. """
def readcsv(path):
    with open(path,'r') as csvfile:
        reader = csv.reader(csvfile)
        fmt = "%Y-%m-%dT%H:%M:%S"
        totime = lambda t: datetime.datetime.fromtimestamp(time.mktime(time.strptime(t,fmt)))
        return [(totime(a),totime(b),s) for (a,b,s) in reader]

parser = argparse.ArgumentParser()
parser.add_argument("-i","--input",type=str,metavar='file',default='schedule.csv',
    help="The file which is to be read. If not specified, the output will\
    be written to ./dat/schedule.csv.")
parser.add_argument("-t","--topic",type=str,metavar='topic',
    help="The topic to filter on.")
parser.add_argument("-p","--period",type=str,metavar='period',
    help="The time interval. Format: \" A:B\", where the first day is today+A and the last\
    day is today+B. By default A=-Inf, B=+Inf")
parser.add_argument("-s","--sum",action='store_true',
    help="Sum the results.")
args = parser.parse_args()

working_dir = os.path.dirname(os.path.realpath(__file__))
data_dir = "dat"
path = os.path.join(data_dir,args.input)

intervals = readcsv(path)
if args.period:
    if args.period:
        m = re.match('(-?\d*):(-?\d*)',args.period.strip())
        if not m:
            raise Exception("Incorrect format for argument \"period\".")
        forever = 36500
        first = int(m.group(1)) if m.group(1) else -forever
        last = int(m.group(2)) if m.group(2) else forever
        intervals = [(a,t,s) for (a,t,s) in intervals
                if datetime.datetime.now().date()+datetime.timedelta(days=first) <= a.date()
                and t.date() <= datetime.datetime.now().date()+datetime.timedelta(days=last)
        ]
intervals = [(a.ctime(),b-a,s) for (a,b,s) in intervals]
if args.topic:
    intervals = [(a,t,s) for (a,t,s) in intervals if s == args.topic]
datesum = datetime.timedelta(0)
for (a,t,s) in intervals:
    datesum += t
output = [[datesum]] if args.sum else intervals
for row in output:
    print ' | '.join([str(cell) for cell in row])

