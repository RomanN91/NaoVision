# -*- encoding: UTF-8 -*-
""" Say `My {Body_part} is touched` when receiving a touch event
"""

import sys
import time

sys.path.append('./naoqi/')
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule
import argparse

# Global variable to store the ReactToTouch module instance
ReactToTouch = None
is_skip_touched = False
memory = None

class ReactToTouch(ALModule):
    """ A simple module able to react
        to touch events.
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        # No need for IP and port here because
        # we have our Python broker connected to NAOqi broker

        # Create a proxy to ALTextToSpeech for later use
        self.tts = ALProxy("ALTextToSpeech")

        # Subscribe to TouchChanged event:
        global memory
        memory = ALProxy("ALMemory")
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

        # Initialize bahaviours
        #self.behaviours = _behaviours
        # if len(self.behaviours) != 3:


    def onTouched(self, strVarName, value):
        """ This will be called each time a touch
        is detected.

        """
        # Unsubscribe to the event when talking,
        # to avoid repetitions
        memory.unsubscribeToEvent("TouchChanged",
            "ReactToTouch")

        touched_bodies = []
        for p in value:
            if p[1]:
                touched_bodies.append(p[0])

        global is_skip_touched
        print touched_bodies
        if len(touched_bodies) > 1:
            if touched_bodies[-1] == 'Head/Touch/Front':
                print 0
            elif touched_bodies[-1] == 'Head/Touch/Middle':
                print 1
            elif touched_bodies[-1] == 'Head/Touch/Rear':
                print 2
                is_skip_touched = True

        # self.say(touched_bodies)

        # Subscribe again to the event
        memory.subscribeToEvent("TouchChanged",
            "ReactToTouch",
            "onTouched")

    def say(self, bodies):
        if (bodies == []):
            return

        sentence = bodies[0]

        self.tts.say(sentence)


def main(ip, port):
    """ Main entry point
    """
    # We need this broker to be able to construct
    # NAOqi modules and subscribe to other modules
    # The broker must stay alive until the program exists
    myBroker = ALBroker("myBroker",
       "0.0.0.0",   # listen to anyone
       0,           # find a free port and use it
       ip,          # parent broker IP
       port)        # parent broker port


    global ReactToTouch
    ReactToTouch = ReactToTouch("ReactToTouch")

    try:
        while True and not is_skip_touched:
            time.sleep(1)
        print "the skip's has been toched"
    except KeyboardInterrupt:
        print
        print "Interrupted by user, shutting down"
        myBroker.shutdown()

if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("--ip", type=str, default="127.0.0.1",
    #                    help="Robot ip address")
    # parser.add_argument("--port", type=int, default=9559,
    #                    help="Robot port number")
    # args = parser.parse_args()
    main("192.168.1.33", 9559)
