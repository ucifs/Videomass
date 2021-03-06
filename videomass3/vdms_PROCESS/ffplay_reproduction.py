# -*- coding: UTF-8 -*-

#########################################################
# Name: ffplay_reproduction.py 
# Porpose: simple media player with x-window-terminal-emulator
# Compatibility: Python3, wxPython Phoenix
# Author: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3
# Rev (10) December 27 2018
#########################################################

# This file is part of Videomass.

#    Videomass is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    Videomass is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with Videomass.  If not, see <http://www.gnu.org/licenses/>.

#########################################################
import wx
import subprocess
import shlex
import time
from threading import Thread

#########################################################################
not_exist_msg =  _('exist in your system?')
#########################################################################

def Messages(msg):
    """
    Receive error messages from Play(Thread) via wxCallafter
    """

    wx.MessageBox("[playback] ERROR:  %s" % (msg), 
                      "Videomass: FFplay", 
                      wx.ICON_ERROR
                      )
#########################################################################
class Play(Thread):
    """
    Run a separate process thread for media reproduction with a called 
    at ffplay witch need x-window-terminal-emulator for show files streaming.
    NOTE: the loglevel is set on 'error'. Do not use 'self.loglevel_type' 
          because -stats option do not work.
    """
    def __init__(self, filepath, param, ffplay_link, loglevel_type, OS):
        """
        costructor
        """
        Thread.__init__(self)
        """initialize"""
        self.filename = filepath # file name selected
        self.ffplay = ffplay_link # command process
        self.loglevel_type = loglevel_type # not used (used error)
        self.param = param # parametri aggiuntivi
        self.OS = OS # tipo di sistema operativo

        self.start() # start the thread (va in self.run())

    def run(self):
        #time.sleep(.5)
        loglevel_type = 'error'
        cmd = '%s -i "%s" %s -loglevel %s' % (self.ffplay,
                                              self.filename,
                                              self.param,
                                              loglevel_type,
                                              )
        try:
            if self.OS == 'Windows':
                command = cmd
            else:
                command = shlex.split(cmd)
            p = subprocess.Popen(command,
                                stderr=subprocess.PIPE,
                                )
            error =  p.communicate()
            
            if error[1]:
                wx.CallAfter(Messages, error[1])
                return
        
        except OSError as err_0:
            if err_0[1] == 'No such file or directory':
                pyerror = ("%s: \n'%s' %s") % (err_0, command[0], 
                                                not_exist_msg)
            else:
                pyerror = "%s: " % (err_0)
                
            wx.CallAfter(Messages, pyerror)
            return
