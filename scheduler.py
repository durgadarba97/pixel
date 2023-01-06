import os
import threading
import time
from collections import deque
from pixel import *
from configs import gifpath
import subprocess
import sys


class Scheduler():
    def __init__(self):
        self.isplaying = False
        self.states = [GameOfLife(), Stardust()]
        self.displayqueue = deque()
        self.current_index = 0
        self.test = 0

    def logger(self, pids):
        pass

    def main(self):
            # buffer the next state
            self.event = threading.Event()
            self.animationsthread = threading.Thread(target=self.animationsThread)
            self.spotifythread = threading.Thread(target=self.spotifyThread)

            self.spotifythread.start()
            self.animationsthread.start()
            self.displayThread()


    def displayThread(self):
        print("hello from the display thread")
        end_time = time.time()
        start_time = time.time()
        oldpid = None
        while True:
            # if(self.isplaying and self.event.is_set()):
            # print(time.time() >= end_time)

            if((not self.isplaying and len(self.displayqueue) > 0 and time.time() >= end_time) or (self.event.is_set())):
                state_info = self.displayqueue.popleft()
                
                print("elapse time: " + str(time.time() - start_time))

                start_time = self.display(state_info[1])
                end_time = (state_info[0] / 1000) + start_time
                self.event.clear() 
            
    def spotifyThread(self):
        spotify = Spotify()
        lastimage = None
        print("hello from the spotify thread")

        while(True):
            time.sleep(4)

            self.isplaying = spotify.isPlaying()

            if(not self.isplaying):
                continue
            
            currentimage = spotify.getTrackImage()

            if(not spotify.compareimages(currentimage, lastimage)):
                lastimage = currentimage
                self.buffer(spotify, 1)
                self.event.set()

    def animationsThread(self):
        print("hello from the animations thread")
        while True:
            if(len(self.displayqueue) < len(self.states)):
                self.buffer(self.nextState(), 0)

    def buffer(self, next_state, priority):

        print("now buffering : " + next_state.toString())

        state_info = next_state.generateFrames(numframes = 1000)
        print(state_info)

        if(not priority):
            self.displayqueue.append(state_info)
        else:
            self.displayqueue.appendleft(state_info)

        # preprocess the gif to stream file
        self.preprocess(state_info[1])



    def nextState(self):
        # get the next state
        self.current_index = (self.current_index + 1) % len(self.states)
        return self.states[self.current_index]

    def kill(self, pid):
        os.system("./bin/kill.sh "+ pid)

    def preprocess(self, name):
        scr = "./bin/to_stream.sh"
        if(self.test):
            print(scr + " " + name)
            return 
        
        subprocess.run([scr + " " + name], shell=True)
        
        

    def display(self, name):
        scr = "./bin/display.sh"
        if(self.test):
            print(scr + " " + name)
            subprocess.run(["code " + gifpath + name], shell=True)
            return time.time()
        
        subprocess.run([scr + " " + name], shell=True)
        return time.time()

    


if(__name__ == "__main__"):
    print(os.getcwd())
    scheduler = Scheduler()
    if(len(sys.argv) > 1 and sys.argv[1] == "test"):
        scheduler.test = 1
    
    scheduler.main()






