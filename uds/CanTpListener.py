#!/usr/bin/env python

__author__ = "Richard Clubb"
__copyrights__ = "Copyright 2018, the python-uds project"
__credits__ = ["Richard Clubb"]

__license__ = "MIT"
__maintainer__ = "Richard Clubb"
__email__ = "richard.clubb@embeduk.com"
__status__ = "Development"

from can import Listener


##
# @brief this may want to be a specialisation of the standard listener class
class CanTpListener(Listener):

    ##
    # @brief initialiser for CanTpListener
    def __init__(self):
        super().__init__()

    ##
    # @brief callback method
    def on_message_received(self, msg):
        raise NotImplementedError("Not implemented yet")

    ##
    # @brief method to stop the listener
    def stop(self):
        self.on_message_received = None
