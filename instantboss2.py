import winsound,sys,time
from os import system

def beep(sound):
    winsound.PlaySound('%s.wav' % sound, winsound.SND_FILENAME)

def countdown(message,seconds,file):
    print(message)
    beep(file)
    for i in range(seconds):
        system("title %d - %s"% (seconds-i,message))
        time.sleep(1)

# The number of arguments has to be 2.
if not len(sys.argv) == 3:
    print("Please apply 2 parameters: the number of work minutes and the number of break"\
            "minutes.")
    sys.exit()

work_secs = 60*int(sys.argv[1])
break_secs = 60*int(sys.argv[2])
while True:
    countdown("Get to work!",work_secs,"work")
    countdown("Chill out.",break_secs,"break")
