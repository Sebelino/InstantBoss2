import winsound,sys,time
import os
import thread

def beep(sound):
    winsound.PlaySound(sound,winsound.SND_FILENAME|winsound.SND_NOWAIT)

def countdown(message,seconds,file):
    print(message)
    thread.start_new_thread(beep,(file,))
    for i in range(seconds):
        os.system("title %d - %s"% (seconds-i,message))
        time.sleep(1)

# The number of arguments has to be 2.
if not len(sys.argv) == 3:
    print("Please apply 2 parameters: the number of work minutes and the number of break "\
            "minutes.")
    sys.exit()

work_secs = 60*int(sys.argv[1])
break_secs = 60*int(sys.argv[2])
while True:
    countdown("Get to work!",work_secs,"work")
    countdown("Chill out.",break_secs,"break")
