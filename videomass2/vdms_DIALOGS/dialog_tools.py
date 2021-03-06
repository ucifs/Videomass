# -*- coding: UTF-8 -*-

#########################################################
# Name: dialog_tools.py
# Porpose: a module with multiple dialog tools
# Writer: Gianluca Pernigoto <jeanlucperni@gmail.com>
# Copyright: (c) 2015-2018/2019 Gianluca Pernigoto <jeanlucperni@gmail.com>
# license: GPL3

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

# Rev: 20/July/2014, 12/March/2015, 30/Apr/2015, 04/Aug/2018, 19/Oct/2018,
#      09/Nov/2018
#########################################################

import wx
import webbrowser
#import wx.lib.masked as masked # not work on macOSX

####################################################################
class Cut_Range(wx.Dialog):
    """
    This class show a simple dialog with a timer selection for
    cutting a time range of audio and video streams. 
    FIXME: replace spinctrl with a timer spin float ctrl if exist
    """
    def __init__(self, parent, hasSet):
        """
        FFmpeg use this format of a time range to specifier a media cutting
        range: "-ss 00:00:00 -t 00:00:00". The -ss flag is the initial
        start selection time; the -t flag is the duration time amount 
        starting from -ss. All this one is specified by hours, minutes and 
        seconds values.
        See FFmpeg documents for more details..
        When this dialog is called, the values previously set are returned 
        for a complete reading (if there are preconfigured values)
        """
        if hasSet == '':
            self.init_hour = '00'
            self.init_minute = '00'
            self.init_seconds = '00'
            self.cut_hour = '00'
            self.cut_minute = '00'
            self.cut_seconds = '00'
        else:#return a previus settings:
            self.init_hour = hasSet[4:6]
            self.init_minute = hasSet[7:9]
            self.init_seconds = hasSet[10:12]
            self.cut_hour = hasSet[16:18]
            self.cut_minute = hasSet[19:21]
            self.cut_seconds = hasSet[22:24]
        
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        """constructor """
        self.start_hour_ctrl = wx.SpinCtrl(self, wx.ID_ANY, "%s" % (
                  self.init_hour), min=0, max=23, style=wx.TE_PROCESS_ENTER)
        lab1 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD,0, ""))
        self.start_minute_ctrl = wx.SpinCtrl(self, wx.ID_ANY, "%s" % (
                self.init_minute), min=0, max=59, style=wx.TE_PROCESS_ENTER)
        lab2 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab2.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD,0, ""))
        self.start_second_ctrl = wx.SpinCtrl(self, wx.ID_ANY,"%s" % (
               self.init_seconds), min=0, max=59, style=wx.TE_PROCESS_ENTER)
        sizer_1_staticbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                        _(u"Seeking (start point) [hh,mm,ss]"))), wx.VERTICAL)
        self.stop_hour_ctrl = wx.SpinCtrl(self, wx.ID_ANY, "%s" % (
                   self.cut_hour), min=0, max=23, style=wx.TE_PROCESS_ENTER)
        lab3 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab3.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD,0, ""))
        self.stop_minute_ctrl = wx.SpinCtrl(self, wx.ID_ANY,"%s" % (
                 self.cut_minute), min=0, max=59, style=wx.TE_PROCESS_ENTER)
        lab4 = wx.StaticText(self, wx.ID_ANY, (":"))
        lab4.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD,0, ""))
        self.stop_second_ctrl = wx.SpinCtrl(self, wx.ID_ANY, "%s" % (
                self.cut_seconds), min=0, max=59, style=wx.TE_PROCESS_ENTER)
        sizer_2_staticbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                        _(u"Cut (end point) [hh,mm,ss]"))), wx.VERTICAL)
        btn_help = wx.Button(self, wx.ID_HELP, "", size=(-1, -1))
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")

        #----------------------Properties ----------------------#
        self.SetTitle('Videomass: duration')
        #self.start_hour_ctrl.SetMinSize((100,-1 ))
        #self.start_minute_ctrl.SetMinSize((100, -1))
        #self.start_second_ctrl.SetMinSize((100, -1))
        self.start_hour_ctrl.SetToolTipString(_(u"Hours time"))
        self.start_minute_ctrl.SetToolTipString(_(u"Minutes Time"))
        self.start_second_ctrl.SetToolTipString(_(u"Seconds time"))
        #self.stop_hour_ctrl.SetMinSize((100, -1))
        #self.stop_minute_ctrl.SetMinSize((100, -1))
        #self.stop_second_ctrl.SetMinSize((100, -1))
        self.stop_hour_ctrl.SetToolTipString(_(u"Hours amount duration"))
        self.stop_minute_ctrl.SetToolTipString(_(u"Minutes amount duration"))
        self.stop_second_ctrl.SetToolTipString(_(u"Seconds amount duration"))
        #----------------------Layout----------------------#
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(3, 1, 0, 0)
        gridFlex1 = wx.FlexGridSizer(1, 5, 0, 0)
        gridFlex2 = wx.FlexGridSizer(1, 5, 0, 0)
        
        grid_sizer_base.Add(sizer_1_staticbox,0,wx.ALL|wx.ALIGN_CENTRE, 5)
        sizer_1_staticbox.Add(gridFlex1,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex1.Add(self.start_hour_ctrl,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex1.Add(lab1,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex1.Add(self.start_minute_ctrl,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex1.Add(lab2,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex1.Add(self.start_second_ctrl,0, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        
        grid_sizer_base.Add(sizer_2_staticbox,0,wx.ALL|wx.ALIGN_CENTRE,5)
        sizer_2_staticbox.Add(gridFlex2, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        gridFlex2.Add(self.stop_hour_ctrl,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex2.Add(lab3,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex2.Add(self.stop_minute_ctrl,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex2.Add(lab4,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridFlex2.Add(self.stop_second_ctrl,0,wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
    
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridhelp.Add(btn_help, 1, wx.ALL,5)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridexit.Add(btn_close, 1, wx.ALL,5)
        gridexit.Add(btn_ok, 1, wx.ALL,5)
        gridexit.Add(btn_reset, 1, wx.ALL,5)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        #gridBtn = wx.BoxSizer()
        gridBtn.Add(gridhelp)
        gridBtn.Add(gridexit)
        #grid_sizer_base.Add(gridBtn)#, flag=wx.ALL|wx.ALIGN_RIGHT|wx.RIGHT, border=5)
        grid_sizer_base.Add(gridBtn, 1, wx.ALL,5)
        sizer_base.Add(grid_sizer_base)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()

        #----------------------Binding (EVT)----------------------#
        self.Bind(wx.EVT_SPINCTRL, self.start_hour, self.start_hour_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.start_minute, self.start_minute_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.start_second, self.start_second_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_hour, self.stop_hour_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_minute, self.stop_minute_ctrl)
        self.Bind(wx.EVT_SPINCTRL, self.stop_second, self.stop_second_ctrl)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, btn_ok)
        self.Bind(wx.EVT_BUTTON, self.resetValues, btn_reset)

    #----------------------Event handler (callback)----------------------#
    def start_hour(self, event):
        self.init_hour = '%s' % self.start_hour_ctrl.GetValue()
        if len(self.init_hour) == 1:
            self.init_hour = '0%s' % self.start_hour_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def start_minute(self, event):
        self.init_minute = '%s' % self.start_minute_ctrl.GetValue()
        if len(self.init_minute) == 1:
            self.init_minute = '0%s' % self.start_minute_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def start_second(self, event):
        self.init_seconds = '%s' % self.start_second_ctrl.GetValue()
        if len(self.init_seconds) == 1:
            self.init_seconds = '0%s' % self.start_second_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def stop_hour(self, event):
        self.cut_hour = '%s' % self.stop_hour_ctrl.GetValue()
        if len(self.cut_hour) == 1:
            self.cut_hour = '0%s' % self.stop_hour_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def stop_minute(self, event):
        self.cut_minute = '%s' % self.stop_minute_ctrl.GetValue()
        if len(self.cut_minute) == 1:
            self.cut_minute = '0%s' % self.stop_minute_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def stop_second(self, event):
        self.cut_seconds = '%s' % self.stop_second_ctrl.GetValue()
        if len(self.cut_seconds) == 1:
            self.cut_seconds = '0%s' % self.stop_second_ctrl.GetValue()
            
    #------------------------------------------------------------------#
    def resetValues(self, event):
        """
        Reset all values at initial state. Is need to confirm with
        ok Button for apply correctly.
        """
        self.start_hour_ctrl.SetValue(0), self.start_minute_ctrl.SetValue(0),
        self.start_second_ctrl.SetValue(0),self.stop_hour_ctrl.SetValue(0),
        self.stop_minute_ctrl.SetValue(0), self.stop_second_ctrl.SetValue(0)
        self.init_hour, self.init_minute, self.init_seconds = '00','00','00'
        self.cut_hour, self.cut_minute, self.cut_seconds = '00','00','00'
    #------------------------------------------------------------------#
    def on_help(self, event):
        """
        """
        page = 'https://jeanslack.github.io/Videomass/Pages/Toolbar/Duration.html'
        webbrowser.open(page)
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip() # need if destroy from parent

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        cut_range = "-ss %s:%s:%s -t %s:%s:%s" % (self.init_hour,
                                    self.init_minute, self.init_seconds,
                                    self.cut_hour, self.cut_minute, 
                                    self.cut_seconds)
        return cut_range
    

#############################################################################

class VideoRotate(wx.Dialog):
    """
    Show a dialog with buttons for movie image orientation.
    TODO: make rotate button with images 
    """
    
    def __init__(self, parent, orientation, msg):
        """
        Make sure you use the clear button when you finish the task.
        """
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)

        
        self.button_up = wx.Button(self, wx.ID_ANY, (_(u"Flip over"))) # capovolgi Sopra
        self.button_left = wx.Button(self, wx.ID_ANY, (_(u"Rotate Left"))) # ruota sx
        self.button_right = wx.Button(self, wx.ID_ANY, (_(u"Rotate Right"))) # ruota a destra
        self.button_down = wx.Button(self, wx.ID_ANY, (_(u"Flip below"))) # capovolgi sotto
        #self.button_reset = wx.Button(self, wx.ID_ANY, ("RESET"))
        self.text_rotate = wx.TextCtrl(self, wx.ID_ANY, "", 
                                    style=wx.TE_PROCESS_ENTER | wx.TE_READONLY
                                    )
        sizerLabel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Orientation points"))), wx.VERTICAL)
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")
        #----------------------Properties------------------------------------#

        self.SetTitle(_(u"Videomass: Set Video/Image Rotation"))
        #self.button_up.SetBackgroundColour(wx.Colour(122, 239, 255))
        self.button_up.SetToolTipString(_(u"Reverses visual movie from bottom to top"))
        #self.button_left.SetBackgroundColour(wx.Colour(122, 239, 255))
        self.button_left.SetToolTipString(_(u"Rotate view movie to left"))
        #self.button_right.SetBackgroundColour(wx.Colour(122, 239, 255))
        self.button_right.SetToolTipString(_(u"Rotate view movie to Right"))
        #self.button_down.SetBackgroundColour(wx.Colour(122, 239, 255))
        self.button_down.SetToolTipString(_(u"Reverses visual movie from top to bottom"))
        self.text_rotate.SetMinSize((200, 30))
        self.text_rotate.SetToolTipString(_(u"Display show settings"))

        #----------------------Handle layout---------------------------------#

        sizerBase = wx.BoxSizer(wx.VERTICAL)
        gridBase = wx.FlexGridSizer(2, 0, 0, 0)
        sizerBase.Add(gridBase, 0, wx.ALL, 0)
        gridBtnExit = wx.FlexGridSizer(1, 3, 0, 0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizerLabel = wx.GridSizer(1, 1, 0, 0)
        grid_sizerBase = wx.GridSizer(1, 2, 0, 0)

        sizer_3.Add(self.button_up, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL, 5)
        grid_sizerBase.Add(self.button_left, 0, wx.ALL 
                                                | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL, 5
                                                )
        grid_sizerBase.Add(self.button_right, 0, wx.ALL 
                                            | wx.ALIGN_CENTER_HORIZONTAL 
                                            | wx.ALIGN_CENTER_VERTICAL, 5
                                            )
        sizer_3.Add(grid_sizerBase, 1, wx.EXPAND, 0)
        sizer_3.Add(self.button_down, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL,5
                                                )
        #grid_sizerLabel.Add(self.button_reset, 0, wx.ALL 
                                            #| wx.ALIGN_CENTER_HORIZONTAL 
                                            #| wx.ALIGN_CENTER_VERTICAL,5
                                            #)
        grid_sizerLabel.Add(self.text_rotate, 0, wx.ALL 
                                        | wx.ALIGN_CENTER_HORIZONTAL 
                                        | wx.ALIGN_CENTER_VERTICAL,5
                                        )
        sizer_3.Add(grid_sizerLabel, 1, wx.EXPAND, 0)
        sizerLabel.Add(sizer_3, 1, wx.EXPAND, 0)
        gridBase.Add(sizerLabel, 1, wx.ALL | 
                                    wx.ALIGN_CENTER_HORIZONTAL | 
                                    wx.ALIGN_CENTER_VERTICAL,5)
        gridBase.Add(gridBtnExit, 1, wx.ALL,5)
        
        gridBtnExit.Add(btn_close, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                              | wx.ALIGN_CENTER_VERTICAL,5
                                               )
        gridBtnExit.Add(self.btn_ok, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL,5
                                                )
        gridBtnExit.Add(btn_reset, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL,5
                                                )
        self.SetSizer(sizerBase)
        sizerBase.Fit(self)
        self.Layout()

        #----------------------Binding (EVT)---------------------------------#
        self.Bind(wx.EVT_BUTTON, self.on_up, self.button_up)
        self.Bind(wx.EVT_BUTTON, self.on_left, self.button_left)
        self.Bind(wx.EVT_BUTTON, self.on_right, self.button_right)
        self.Bind(wx.EVT_BUTTON, self.on_down, self.button_down)
        #self.Bind(wx.EVT_BUTTON, self.on_reset, self.button_reset)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        
        if orientation == '':
            self.orientation = ''
        else:
            self.orientation = orientation
            self.text_rotate.SetValue(msg)

    #----------------------Event handler (callback)--------------------------#
    def on_up(self, event):
        self.orientation = "transpose=2,transpose=2"
        self.text_rotate.SetValue(_(u"180° from bottom to top"))
        
    #------------------------------------------------------------------#
    def on_left(self, event):
        opt = "transpose=2"
        self.orientation = opt
        self.text_rotate.SetValue(_(u"Rotate 90° Left"))
        
    #------------------------------------------------------------------#
    def on_right(self, event):
        self.orientation = "transpose=1"
        self.text_rotate.SetValue(_(u"Rotate 90° Right"))
        
    #------------------------------------------------------------------#
    def on_down(self, event):
        self.orientation = "transpose=2,transpose=2"
        self.text_rotate.SetValue(_(u"180° from top to bottom"))
        
    #------------------------------------------------------------------#
    def on_reset(self, event):
        self.orientation = ""
        self.text_rotate.SetValue("")
        
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip()

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        msg = self.text_rotate.GetValue()
        return (self.orientation, msg)
###########################################################################
class VideoCrop(wx.Dialog):
    """
    Show a dialog with buttons for movie image orientation.
    TODO: make rotate button with images 
    """
    
    def __init__(self, parent, fcrop):
        """
        Make sure you use the clear button when you finish the task.
        """
        self.w = '' # set -1 = disable
        self.h = '' # set -1 = disable
        self.y = '' # set -1 = disable
        self.x = '' # set -1 = disable
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        """ 
        """
        self.label_width = wx.StaticText(self, wx.ID_ANY, (_(u"Width")))
        self.crop_width = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1,  max=10000,
                               size=(-1,-1), style=wx.TE_PROCESS_ENTER
                                )
        self.label_height = wx.StaticText(self, wx.ID_ANY, (_(u"Height")))
        self.crop_height = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=10000, 
                                 size=(-1,-1), style=wx.TE_PROCESS_ENTER
                                 )
        self.label_X = wx.StaticText(self, wx.ID_ANY, ("X"))
        self.crop_X = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=10000, 
                                 size=(-1,-1), style=wx.TE_PROCESS_ENTER
                                 )
        self.label_Y = wx.StaticText(self, wx.ID_ANY, ("Y"))
        self.crop_Y = wx.SpinCtrl(self, wx.ID_ANY, "-1", min=-1, max=10000, 
                                 size=(-1,-1), style=wx.TE_PROCESS_ENTER
                                 )
        sizerLabel = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Crop Dimensions"))), wx.VERTICAL)
        btn_help = wx.Button(self, wx.ID_HELP, "")
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")
        
        #----------------------Handle layout---------------------------------#
        sizerBase = wx.BoxSizer(wx.VERTICAL)
        gridBase = wx.FlexGridSizer(2, 1, 0, 0)
        sizerBase.Add(gridBase, 0, wx.ALL, 0)
        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        grid_sizerBase = wx.FlexGridSizer(1, 5, 0, 0)

        sizer_3.Add(self.label_height, 0, wx.ALL | 
                                         wx.ALIGN_CENTER_HORIZONTAL, 5
                                         )
        sizer_3.Add(self.crop_height, 0, wx.ALL | 
                                        wx.ALIGN_CENTER_HORIZONTAL, 5
                                        )
        
        grid_sizerBase.Add(self.label_Y, 0, wx.ALL 
                                                | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL, 5
                                                )
        grid_sizerBase.Add(self.crop_Y, 0, wx.ALL 
                                                | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL, 5
                                                )
        grid_sizerBase.Add((50, 50), 0, wx.ALL 
                                            | wx.ALIGN_CENTER_HORIZONTAL 
                                            | wx.ALIGN_CENTER_VERTICAL, 5
                                            )
        grid_sizerBase.Add(self.crop_width, 0, wx.ALL 
                                            | wx.ALIGN_CENTER_HORIZONTAL 
                                            | wx.ALIGN_CENTER_VERTICAL, 5
                                            )
        grid_sizerBase.Add(self.label_width, 0, wx.ALL 
                                                | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL, 5
                                                )
        
        sizer_3.Add(grid_sizerBase, 1, wx.EXPAND, 0)
        sizer_3.Add(self.crop_X, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL,5
                                                )
        sizer_3.Add(self.label_X, 0, wx.ALL | wx.ALIGN_CENTER_HORIZONTAL 
                                                | wx.ALIGN_CENTER_VERTICAL,5
                                                )
        sizerLabel.Add(sizer_3, 1, wx.EXPAND, 0)
        gridBase.Add(sizerLabel, 1, wx.ALL |
                                    wx.ALIGN_CENTER_HORIZONTAL | 
                                    wx.ALIGN_CENTER_VERTICAL,10)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridBase.Add(gridBtn)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridBtn.Add(gridhelp, 0, wx.ALL ,5)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridBtn.Add(gridexit, 0, wx.ALL ,5)
        gridhelp.Add(btn_help, 1, wx.ALL ,5)
        gridexit.Add(btn_close, 1, wx.ALL, 5)
        gridexit.Add(self.btn_ok, 1, wx.ALL ,5)
        gridexit.Add(btn_reset, 1, wx.ALL ,5)
        self.SetSizer(sizerBase)
        sizerBase.Fit(self)
        self.Layout()
        
        #----------------------Properties------------------------------------#
        self.SetTitle("Videomass: Video/Image Crop")
        #self.crop_width.SetBackgroundColour(wx.Colour(122, 239, 255))
        #self.crop_height.SetBackgroundColour(wx.Colour(122, 239, 255))
        #self.crop_X.SetBackgroundColour(wx.Colour(122, 239, 255))
        #self.crop_Y.SetBackgroundColour(wx.Colour(122, 239, 255))
        height = (_(u'The height of the output video.\nSet to -1 for disabling.'))
        width = (_(u'The width of the output video.\nSet to -1 for disabling.'))
        x = (_(u'The horizontal position of the left edge.'))
        y = (_(u'The vertical position of the top edge of the left corner.'))
        self.crop_width.SetToolTipString(_(u'Width:\n%s') % width)
        self.crop_Y.SetToolTipString('Y:\n%s' % y)
        self.crop_X.SetToolTipString('X:\n%s' % x)
        self.crop_height.SetToolTipString(_(u'Height:\n%s') % height)
        
        #----------------------Binding (EVT)---------------------------------#
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        
        if fcrop: # set the previusly values
            s = fcrop.split(':')
            item1 = s[0][5:] # remove `crop=` word
            s[0] = item1 # replace first item
            for i in s:
                if i.startswith('w'):
                    self.w = i[2:]
                    self.crop_width.SetValue(int(self.w))
                if i.startswith('h'):
                    self.h = i[2:]
                    self.crop_height.SetValue(int(self.h))
                if i.startswith('x'):
                    self.x = i[2:]
                    self.crop_X.SetValue(int(self.x))
                if i.startswith('y'):
                    self.y = i[2:]
                    self.crop_Y.SetValue(int(self.y))
    #------------------------------------------------------------------#
    def on_help(self, event):
        """
        """
        page = ('https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/'
                'VideoConv_Panel/Filters/FilterCrop.html')
        webbrowser.open(page)
    #------------------------------------------------------------------#

    def on_reset(self, event):
        self.h, self.y, self.x, self.w = "", "", "", ""
        self.crop_width.SetValue(-1), self.crop_X.SetValue(-1)
        self.crop_height.SetValue(-1), self.crop_Y.SetValue(-1)
        
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip()

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        #print self.crop_Y.GetValue(),self.crop_width.GetValue(),self.crop_X.GetValue(),self.crop_height.GetValue()
        #print type(self.crop_Y.GetValue())
        if self.crop_width.GetValue() == -1:
            self.w = ''
        else:
            self.w = 'w=%s:' % self.crop_width.GetValue()
            
        if self.crop_height.GetValue() == -1:
            self.h = ''
        else:
            self.h = 'h=%s:' % self.crop_height.GetValue()
            
        if self.crop_X.GetValue() == -1:
            self.x = ''
        else:
            self.x = 'x=%s:' % self.crop_X.GetValue()
        
        if self.crop_Y.GetValue() == -1:
            self.y = ''
        else:
            self.y = 'y=%s:' % self.crop_Y.GetValue()

        s = '%s%s%s%s' % (self.w, self.h, self.x, self.y)
        if s:
            l = len(s)
            val = '%s' % s[:l - 1]
        else:
            val = ''
        return (val)

###########################################################################
class VideoResolution(wx.Dialog):
    """
    This class show parameters for set custom video resizing. 
    Include a video size, video scaling with setdar and 
    setsar options.
    """
    def __init__(self, parent, scale, dar, sar):
        """
        See FFmpeg documents for more details..
        When this dialog is called, the values previously set are returned 
        for a complete reading (if there are preconfigured values)
        """
        self.width = "0"
        self.height = "0"
        self.darNum = "0"
        self.darDen = "0"
        self.sarNum = "0"
        self.sarDen = "0"

        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        """constructor """
        ####----scaling static box section
        
        v_scalingbox = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Scale (resize)"))), wx.VERTICAL)
        
        label_width = wx.StaticText(self, wx.ID_ANY, (_(u"Width"))
                                          )
        
        self.spin_scale_width = wx.SpinCtrl(self, wx.ID_ANY, "0", min=-2, 
                                            max=9000, style=wx.TE_PROCESS_ENTER
                                            )
        label_x1 = wx.StaticText(self, wx.ID_ANY, ("X")
                                      )
        label_x1.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.BOLD,0, "")
                              )
        self.spin_scale_height = wx.SpinCtrl(self, wx.ID_ANY, "0", min=-2, 
                                             max=9000, style=wx.TE_PROCESS_ENTER
                                             )
        label_height = wx.StaticText(self, wx.ID_ANY, (_(u"Height")))
        #-------
        
        v_setdar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Setdar (display aspect ratio):"))), wx.VERTICAL)
        label_num = wx.StaticText(self, wx.ID_ANY, (_(u"Numerator"))
                                  )
        self.spin_setdarNum = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, 
                                      max=99, style=wx.TE_PROCESS_ENTER,
                                      size=(-1,-1))
        label_sepdar = wx.StaticText(self, wx.ID_ANY, ("/")
                                          )
        label_sepdar.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, 
                                          wx.BOLD,0, "")
                                          )
        self.spin_setdarDen = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, 
                                      max=99, style=wx.TE_PROCESS_ENTER,
                                      size=(-1,-1)
                                      )##
        label_den = wx.StaticText(self, wx.ID_ANY, (_(u"Denominator"))
                                          )
        #----------
        v_setsar = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"SetSar (sample aspect ratio):"))), wx.VERTICAL)
        label_num1 = wx.StaticText(self, wx.ID_ANY, (_(u"Numerator"))
                                          )
        self.spin_setsarNum = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, 
                                      max=10000, style=wx.TE_PROCESS_ENTER,
                                      size=(-1,-1))
        label_sepsar = wx.StaticText(self, wx.ID_ANY, ("/")
                                          )
        label_sepsar.SetFont(wx.Font(10, wx.DEFAULT, wx.NORMAL, 
                                          wx.BOLD,0, "")
                                          )
        self.spin_setsarDen = wx.SpinCtrl(self, wx.ID_ANY, "0", min=0, 
                                      max=10000, style=wx.TE_PROCESS_ENTER,
                                      size=(-1,-1))##
        label_den1 = wx.StaticText(self, wx.ID_ANY, (_(u"Denominator"))
                                          )
        ####----- confirm buttons section
        btn_help = wx.Button(self, wx.ID_HELP, "")
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")

        ####------Layout
        sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(4, 1, 0, 0)
        
        # scaling section:
        grid_sizer_base.Add(v_scalingbox, 1, wx.ALL | wx.EXPAND, 15)
        grid_sizer_base.Add(v_setdar, 1, wx.ALL | wx.EXPAND, 15)
        grid_sizer_base.Add(v_setsar, 1, wx.ALL | wx.EXPAND, 15)
        #Flex_scale_base = wx.GridSizer(3, 1, 0, 0)
        
        
       # Flex_scale_base.Add(Flex_scale)
        Flex_scale = wx.FlexGridSizer(1, 5, 0, 0)
        v_scalingbox.Add(Flex_scale, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        Flex_scale.Add(label_width, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(self.spin_scale_width, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(label_x1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(self.spin_scale_height, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_scale.Add(label_height, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        Flex_dar = wx.FlexGridSizer(1, 5, 0, 0)
        v_setdar.Add(Flex_dar, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        Flex_dar.Add(label_num, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(self.spin_setdarNum, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(label_sepdar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(self.spin_setdarDen, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_dar.Add(label_den, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        Flex_sar = wx.FlexGridSizer(1, 5, 0, 0)
        v_setsar.Add(Flex_sar, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        Flex_sar.Add(label_num1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(self.spin_setsarNum, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(label_sepsar, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(self.spin_setsarDen, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        Flex_sar.Add(label_den1, 0, wx.ALL|wx.ALIGN_CENTER_VERTICAL, 5)
        
        # confirm btn section:
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridexit.Add(btn_close,1, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridexit.Add(self.btn_ok,1, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridexit.Add(btn_reset,1, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridhelp.Add(btn_help,1, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        
        gridBtn.Add(gridhelp, 1, wx.ALL, 10)
        gridBtn.Add(gridexit, 1, wx.ALL, 10)
        
        
        grid_sizer_base.Add(gridBtn)#, flag=wx.ALL|wx.ALIGN_RIGHT|wx.RIGHT, border=5)
        # final settings:
        sizer_base.Add(grid_sizer_base, 1, wx.ALL | wx.EXPAND, 5)
        self.SetSizer(sizer_base)
        sizer_base.Fit(self)
        self.Layout()
        
        # Properties
        self.SetTitle(_(u"Videomass: Resize (change resolution)"))

        scale_str = (_(u'Scale (resize) the input video or image.'))
        self.spin_scale_width.SetToolTipString(_(u'WIDTH:\n%s') % scale_str)
        self.spin_scale_height.SetToolTipString(_(u'HEIGHT:\n%s') % scale_str)
        setdar_str = (_(u'Sets the Display Aspect '
                      u'Ratio.\nSet to 0 to disabling.'))
        self.spin_setdarNum.SetToolTipString(_(u'-NUMERATOR-\n%s') % setdar_str)
        self.spin_setdarDen.SetToolTipString(_(u'-DENOMINATOR-\n%s') % setdar_str)
        setsar_str = (_(u'The setsar filter sets the Sample (aka Pixel) '
                      u'Aspect Ratio.\nSet to 0 to disabling.'))
        self.spin_setsarNum.SetToolTipString(_(u'-NUMERATOR-\n%s') % setsar_str)
        self.spin_setsarDen.SetToolTipString(_(u'-DENOMINATOR-\n%s') % setsar_str)
        
        #----------------------Binding (EVT)---------------------------------#
        #self.Bind(wx.EVT_SPINCTRL, self.on_width, self.spin_scale_width)
        #self.Bind(wx.EVT_SPINCTRL, self.on_height, self.spin_scale_height)
        #self.Bind(wx.EVT_SPINCTRL, self.on_darNum, self.spin_setdarNum)
        #self.Bind(wx.EVT_SPINCTRL, self.on_darDen, self.spin_setdarDen)
        #self.Bind(wx.EVT_SPINCTRL, self.on_sarNum, self.spin_setsarNum)
        #self.Bind(wx.EVT_SPINCTRL, self.on_sarDen, self.spin_setsarDen)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)

        if scale:
            self.width = scale.split(':')[0][8:]
            self.height = scale.split(':')[1][2:]
            self.spin_scale_width.SetValue(int(self.width))
            self.spin_scale_height.SetValue(int(self.height))
        if dar:
            self.darNum = dar.split('/')[0][7:]
            self.darDen = dar.split('/')[1]
            self.spin_setdarNum.SetValue(int(self.darNum))
            self.spin_setdarDen.SetValue(int(self.darDen))
        if sar:
            self.sarNum = sar.split('/')[0][7:]
            self.sarDen = sar.split('/')[1]
            self.spin_setsarNum.SetValue(int(self.sarNum))
            self.spin_setsarDen.SetValue(int(self.sarDen))
        
    #----------------------Event handler (callback)--------------------------#
    ##------------------------------------------------------------------#
    def on_help(self, event):
        """
        """
        page = ('https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/'
                'VideoConv_Panel/Filters/FilterScaling.html')
        webbrowser.open(page)
    #------------------------------------------------------------------#
    def on_reset(self, event):
        self.width, self.height = "0", "0"
        self.darNum, self.darDen = "0", "0"
        self.sarNum, self.sarDen = "0", "0"
        self.spin_scale_width.SetValue(0), self.spin_scale_height.SetValue(0)
        self.spin_setdarNum.SetValue(0), self.spin_setdarDen.SetValue(0)
        self.spin_setsarNum.SetValue(0), self.spin_setsarDen.SetValue(0)
        
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip()

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        diction = {}
        self.width = '%s' % self.spin_scale_width.GetValue()
        self.height = '%s' % self.spin_scale_height.GetValue()
        self.darNum = '%s' % self.spin_setdarNum.GetValue()
        self.darDen = '%s' % self.spin_setdarDen.GetValue()
        self.sarNum = '%s' % self.spin_setsarNum.GetValue()
        self.sarDen = '%s' % self.spin_setsarDen.GetValue()

        if self.width == '0' or self.height == '0':
            size = ''
        else:
            size = 'scale=w=%s:h=%s' % (self.width,self.height)
            diction['scale'] = size
        
        if self.darNum == '0' or self.darDen == '0':
            setdar = ''
        else:
            setdar = 'setdar=%s/%s' % (self.darNum,self.darDen)
            diction['setdar'] = setdar
        
        if self.sarNum == '0' or self.sarDen == '0':
            setsar = ''
        else:
            setsar = 'setsar=%s/%s' % (self.sarNum,self.sarDen)
            diction['setsar'] = setsar

        return (diction)

#############################################################################

class Lacing(wx.Dialog):
    """
    Show a dialog for image deinterlace/interlace functions 
    with advanced option for each filter.
    """
    
    def __init__(self, parent, deinterlace, interlace):
        """
        Make sure you use the clear button when you finish the task.
        """
        self.cmd_opt = {}
        if deinterlace:
            self.cmd_opt["deinterlace"] = deinterlace
        elif interlace:
            self.cmd_opt["interlace"] = interlace
        else:
            pass
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        
        zone1 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Deinterlace"))), wx.VERTICAL)
        zone2 = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Interlace"))), wx.VERTICAL)
        
        self.ckbx_deintW3fdif = wx.CheckBox(self, wx.ID_ANY, 
                                (_(u"Deinterlaces (Using the 'w3fdif' filter)"))
                                            )
        self.rdbx_W3fdif_filter = wx.RadioBox(self, wx.ID_ANY, 
                                              (u"Filter"), choices=[(u"simple"),
                                              (u"complex")],
                                            majorDimension=0, 
                                            style=wx.RA_SPECIFY_ROWS
                                            )
        self.rdbx_W3fdif_deint = wx.RadioBox(self, wx.ID_ANY, 
                                            (u"Deint"), 
                                            choices=[("all"),
                                            ("interlaced")], majorDimension=0, 
                                            style=wx.RA_SPECIFY_ROWS
                                            )
        self.ckbx_deintYadif = wx.CheckBox(self, wx.ID_ANY, 
                                (_(u"Deinterlaces (Using the 'yadif' filter)"))
                                            )
        self.rdbx_Yadif_mode = wx.RadioBox(self, wx.ID_ANY, 
                                            (u"Mode"), choices=[("0, send_frame"),
                                            ("1, send_field"),
                                            ("2, send_frame_nospatial"),
                                            ("3, send_field_nospatial")], 
                                            majorDimension=0, 
                                            style=wx.RA_SPECIFY_ROWS
                                            )
        self.rdbx_Yadif_parity = wx.RadioBox(self, wx.ID_ANY, 
                                            (u"Parity"), choices=[("0, tff"),
                                            ("1, bff"), ("-1, auto")], 
                                            majorDimension=0, 
                                            style=wx.RA_SPECIFY_ROWS
                                            )
        self.rdbx_Yadif_deint = wx.RadioBox(self, wx.ID_ANY, 
                                            (u"Deint"), choices=[("0, all"),
                                            ("1, interlaced")], majorDimension=0, 
                                            style=wx.RA_SPECIFY_ROWS
                                            )
        self.ckbx_interlace = wx.CheckBox(self, wx.ID_ANY,
                            (_(u"Interlaces (Using the 'interlace' filter)"))
                                          )
        self.rdbx_inter_scan = wx.RadioBox(self, wx.ID_ANY, 
                                          ("Scanning mode"), 
                                          choices=[("scan=tff"), 
                                                   ("scan=bff")], 
                                    majorDimension=0, style=wx.RA_SPECIFY_ROWS
                                          )
        self.rdbx_inter_lowpass = wx.RadioBox(self, wx.ID_ANY, 
                                          ("Set vertical low-pass filter"), 
                                          choices=[("lowpass=0"),
                                                   ("lowpass=1")], 
                                    majorDimension=0, style=wx.RA_SPECIFY_ROWS
                                          )
        self.enable_opt = wx.wx.ToggleButton(self, wx.ID_ANY, 
                                            _(u"Advanced Options"))
        ####----- confirm buttons section
        btn_help = wx.Button(self, wx.ID_HELP, "")
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")
        
        # set Properties
        self.SetTitle(_(u"Videomass: Deinterlace/Interlace"))
        self.rdbx_W3fdif_filter.Hide()
        self.rdbx_W3fdif_deint.Hide()
        self.rdbx_Yadif_mode.Hide()
        self.rdbx_Yadif_parity.Hide()
        self.rdbx_Yadif_deint.Hide()
        self.rdbx_inter_scan.Hide()
        self.rdbx_inter_lowpass.Hide()
        self.ckbx_deintW3fdif.SetValue(False)
        self.ckbx_deintYadif.SetValue(False)
        self.ckbx_interlace.SetValue(False)
        self.rdbx_W3fdif_filter.SetSelection(1)
        self.rdbx_W3fdif_deint.SetSelection(0)
        self.rdbx_Yadif_mode.SetSelection(1)
        self.rdbx_Yadif_parity.SetSelection(2)
        self.rdbx_Yadif_deint.SetSelection(0)
        self.rdbx_inter_scan.SetSelection(0)
        self.rdbx_inter_lowpass.SetSelection(1)
        self.rdbx_W3fdif_filter.Disable(),self.rdbx_W3fdif_deint.Disable(),
        self.rdbx_Yadif_mode.Disable(),
        self.rdbx_Yadif_parity.Disable(), self.rdbx_Yadif_deint.Disable(),
        self.rdbx_inter_scan.Disable(), self.rdbx_inter_lowpass.Disable()

        ####------ set Layout
        self.sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(4, 1, 0, 0)
        grid_sizer_base.Add(zone1, 1, wx.ALL | wx.EXPAND, 5)
        deint_grid = wx.FlexGridSizer(2, 4, 0, 0)
        zone1.Add(deint_grid)
        deint_grid.Add(self.ckbx_deintW3fdif, 0, wx.ALL , 15)
        deint_grid.Add(self.rdbx_W3fdif_filter, 0, wx.ALL,15)
        deint_grid.Add(self.rdbx_W3fdif_deint, 0, wx.ALL, 15)
        deint_grid.Add((20, 20), 0, wx.ALL, 15)
        deint_grid.Add(self.ckbx_deintYadif, 0, wx.ALL, 15)
        deint_grid.Add(self.rdbx_Yadif_mode, 0, wx.ALL, 15)
        deint_grid.Add(self.rdbx_Yadif_parity, 0, wx.ALL, 15)
        deint_grid.Add(self.rdbx_Yadif_deint, 0, wx.ALL, 15)
        grid_sizer_base.Add(zone2, 1, wx.ALL | wx.EXPAND, 5)
        inter_grid = wx.FlexGridSizer(1, 3, 0, 0)
        zone2.Add(inter_grid)
        inter_grid.Add(self.ckbx_interlace, 0, wx.ALL, 15)
        inter_grid.Add(self.rdbx_inter_scan, 0, wx.ALL, 15)
        inter_grid.Add(self.rdbx_inter_lowpass, 0, wx.ALL, 15)
        grid_sizer_base.Add(self.enable_opt,1, wx.ALL|wx.ALIGN_CENTER_VERTICAL,5)
        # confirm btn section:
            
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        grid_sizer_base.Add(gridBtn,1, wx.ALL|wx.ALIGN_CENTRE, 0)#
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridBtn.Add(gridhelp)
        gridBtn.Add(gridexit)
        
        gridhelp.Add(btn_help,1, wx.ALL,5)
        gridexit.Add(btn_close,1, wx.ALL,5)
        gridexit.Add(self.btn_ok,1, wx.ALL,5)
        gridexit.Add(btn_reset,1, wx.ALL,5)
        # final settings:
        self.sizer_base.Add(grid_sizer_base, 1, wx.ALL, 5)
        self.SetSizer(self.sizer_base)
        self.sizer_base.Fit(self)
        self.Layout()
        
        self.ckbx_deintW3fdif.SetToolTipString(_(u'Deinterlace the input video '
                                               u'with `w3fdif` filter'))
                
        self.rdbx_W3fdif_filter.SetToolTipString(_(u'Set the interlacing filter '
                                                 u'coefficients.')
                                                 )
        self.rdbx_W3fdif_deint.SetToolTipString(_(u'Specify which frames to '
                                                u'deinterlace.')
                                                  )
        self.ckbx_deintYadif.SetToolTipString(_(u'Deinterlace the input video '
            u'with `yadif` filter. For FFmpeg is the best and fastest choice ')
                                              )
        self.rdbx_Yadif_mode.SetToolTipString(_(u'mode\n'
           u'The interlacing mode to adopt.'))
        self.rdbx_Yadif_parity.SetToolTipString(_(u'parity\n'
            u'The picture field parity assumed for the input interlaced video.'))
        self.rdbx_Yadif_deint.SetToolTipString(_(u'Specify which frames to '
                                               u'deinterlace.'))
        self.ckbx_interlace.SetToolTipString(_(u'Simple interlacing filter from '
                u'progressive contents.'))
        self.rdbx_inter_scan.SetToolTipString(_(u'scan:\n'
            u'determines whether the interlaced frame is taken from the '
            u'even (tff - default) or odd (bff) lines of the progressive frame.')
                                              )
        self.rdbx_inter_lowpass.SetToolTipString(_(u'lowpas:\n'
            u'Enable (default) or disable the vertical lowpass filter to '
            u'avoid twitter interlacing and reduce moire patterns.\n'
            u'Default is no setting.'))
        
        #----------------------Binding (EVT)---------------------------------#
        self.Bind(wx.EVT_CHECKBOX, self.on_DeintW3fdif, self.ckbx_deintW3fdif)
        self.Bind(wx.EVT_RADIOBOX, self.on_W3fdif_filter, self.rdbx_W3fdif_filter)
        self.Bind(wx.EVT_RADIOBOX, self.on_W3fdif_deint, self.rdbx_W3fdif_deint)
        self.Bind(wx.EVT_CHECKBOX, self.on_DeintYadif, self.ckbx_deintYadif)
        self.Bind(wx.EVT_RADIOBOX, self.on_modeYadif, self.rdbx_Yadif_mode)
        self.Bind(wx.EVT_RADIOBOX, self.on_parityYadif, self.rdbx_Yadif_parity)
        self.Bind(wx.EVT_RADIOBOX, self.on_deintYadif, self.rdbx_Yadif_deint)
        self.Bind(wx.EVT_CHECKBOX, self.on_Interlace, self.ckbx_interlace)
        self.Bind(wx.EVT_RADIOBOX, self.on_intScan, self.rdbx_inter_scan)
        self.Bind(wx.EVT_RADIOBOX, self.on_intLowpass, self.rdbx_inter_lowpass)
        self.Bind(wx.EVT_TOGGLEBUTTON, self.Advanced_Opt, self.enable_opt)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        
        self.settings()
        
    def settings(self):
        """
        set default or set in according with previusly activated option
        """
        if 'deinterlace' in self.cmd_opt:
            if self.cmd_opt["deinterlace"].startswith('yadif'):
                self.ckbx_deintYadif.SetValue(True)
                self.ckbx_deintW3fdif.Disable()
                self.ckbx_interlace.Disable()
                self.rdbx_Yadif_mode.Enable()
                self.rdbx_Yadif_parity.Enable() 
                self.rdbx_Yadif_deint.Enable()
                indx = self.cmd_opt["deinterlace"].split('=')[1].split(':')
                if indx[1] == '-1':
                    parity = 2
                self.rdbx_Yadif_mode.SetSelection(int(indx[0]))
                self.rdbx_Yadif_parity.SetSelection(parity)
                self.rdbx_Yadif_deint.SetSelection(int(indx[2]))
                
            elif self.cmd_opt["deinterlace"].startswith('w3fdif'):
                self.ckbx_deintW3fdif.SetValue(True)
                self.ckbx_deintYadif.Disable()
                self.ckbx_interlace.Disable()
                self.rdbx_W3fdif_filter.Enable()
                self.rdbx_W3fdif_deint.Enable()
                indx = self.cmd_opt["deinterlace"].split('=')[1].split(':')
                if indx[0] == 'complex':
                    filt = 1
                elif indx[0] == 'simple':
                    filt = 0
                self.rdbx_W3fdif_filter.SetSelection(filt)
                if indx[1] == 'all':
                    deint = 0
                elif indx[1] == 'interlaced':
                    deint = 1
                self.rdbx_W3fdif_deint.SetSelection(deint)
                
        elif 'interlace' in self.cmd_opt:
            self.ckbx_interlace.SetValue(True)
            self.ckbx_deintW3fdif.Disable(), self.ckbx_deintYadif.Disable(),
            self.rdbx_inter_scan.Enable(), self.rdbx_inter_lowpass.Enable(),
            
            scan = self.cmd_opt["interlace"].split('=')[2].split(':')
            if 'tff' in scan[0]:
                scan = 0
            elif 'bff' in scan[0]:
                scan = 1
            self.rdbx_inter_scan.SetSelection(scan)
            
            lowpass = self.cmd_opt["interlace"].split(':')
            if 'lowpass=0' in lowpass[1]:
                lowpass = 0
            elif 'lowpass=1' in lowpass[1]:
                lowpass = 1
            self.rdbx_inter_lowpass.SetSelection(lowpass)
        else:
            pass

    #----------------------Event handler (callback)--------------------------#
    #------------------------------------------------------------------------#
    def on_DeintW3fdif(self, event):
        """
        """
        if self.ckbx_deintW3fdif.IsChecked():
            self.rdbx_W3fdif_filter.Enable(), self.rdbx_W3fdif_deint.Enable(),
            self.ckbx_deintYadif.Disable(), self.ckbx_interlace.Disable()
            self.cmd_opt["deinterlace"] = "w3fdif=complex:all"
            
        elif not self.ckbx_deintW3fdif.IsChecked():
            self.rdbx_W3fdif_filter.Disable(),self.rdbx_W3fdif_deint.Disable(),
            self.ckbx_deintYadif.Enable(), self.ckbx_interlace.Enable(),
            self.cmd_opt.clear()
    #------------------------------------------------------------------#
    def on_W3fdif_filter(self, event):
        """
        """
        self.cmd_opt["deinterlace"] = "w3fdif=%s:%s" % (
                                self.rdbx_W3fdif_filter.GetStringSelection(),
                                self.rdbx_W3fdif_deint.GetStringSelection()
                                                    )
    #------------------------------------------------------------------#
    def on_W3fdif_deint(self, event):
        """
        """
        self.cmd_opt["deinterlace"] = "w3fdif=%s:%s" % (
                                self.rdbx_W3fdif_filter.GetStringSelection(),
                                self.rdbx_W3fdif_deint.GetStringSelection()
                                                    )
    #------------------------------------------------------------------#
    def on_DeintYadif(self, event):
        """
        """
        if self.ckbx_deintYadif.IsChecked():
            self.ckbx_deintW3fdif.Disable(), self.rdbx_Yadif_mode.Enable(),
            self.rdbx_Yadif_parity.Enable(), self.rdbx_Yadif_deint.Enable(),
            self.ckbx_interlace.Disable(),
            self.cmd_opt["deinterlace"] = "yadif=1:-1:0"
            
        elif not self.ckbx_deintYadif.IsChecked():
            self.ckbx_deintW3fdif.Enable(), self.rdbx_Yadif_mode.Disable(),
            self.rdbx_Yadif_parity.Disable(), self.rdbx_Yadif_deint.Disable(),
            self.ckbx_interlace.Enable(),
            self.cmd_opt.clear()
    #------------------------------------------------------------------#        
    def on_modeYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt["deinterlace"] = "yadif=%s:%s:%s" % (
                                self.rdbx_Yadif_mode.GetStringSelection()[0],
                                parity[0],
                                self.rdbx_Yadif_deint.GetStringSelection()[0]
                                                    )
    #------------------------------------------------------------------#
    def on_parityYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt["deinterlace"] = "yadif=%s:%s:%s" % (
                                self.rdbx_Yadif_mode.GetStringSelection()[0],
                                parity[0],
                                self.rdbx_Yadif_deint.GetStringSelection()[0]
                                                    )
    #------------------------------------------------------------------#
    def on_deintYadif(self, event):
        """
        """
        parity = self.rdbx_Yadif_parity.GetStringSelection().split(',')
        self.cmd_opt["deinterlace"] = "yadif=%s:%s:%s" % (
                                self.rdbx_Yadif_mode.GetStringSelection()[0],
                                parity[0],
                                self.rdbx_Yadif_deint.GetStringSelection()[0]
                                                    )
    #------------------------------------------------------------------#
    def on_Interlace(self, event):
        """
        """
        if self.ckbx_interlace.IsChecked():
            self.ckbx_deintW3fdif.Disable(), self.ckbx_deintYadif.Disable(),
            self.rdbx_inter_scan.Enable(), self.rdbx_inter_lowpass.Enable(),
            self.cmd_opt["interlace"] = "interlace=scan=tff:lowpass=1"
            
        elif not self.ckbx_interlace.IsChecked():
            self.ckbx_deintW3fdif.Enable(), self.ckbx_deintYadif.Enable(),
            self.rdbx_inter_scan.Disable(), self.rdbx_inter_lowpass.Disable(),
            self.cmd_opt.clear()
    #------------------------------------------------------------------#
    def on_intScan(self, event):
        """
        """
        self.cmd_opt["interlace"] = "interlace=%s:%s" % (
                                self.rdbx_inter_scan.GetStringSelection(),
                                self.rdbx_inter_lowpass.GetStringSelection(),
                                                     )
    #------------------------------------------------------------------#
    def on_intLowpass(self, event):
        """
        """
        self.cmd_opt["interlace"] = "interlace=%s:%s" % (
                                self.rdbx_inter_scan.GetStringSelection(),
                                self.rdbx_inter_lowpass.GetStringSelection(),
                                                     )
    #------------------------------------------------------------------#
    def Advanced_Opt(self, event):
        """
        Show or Hide advanved option for all filters
        """
        if self.enable_opt.GetValue():
            #self.enable_opt.SetBackgroundColour(wx.Colour(240, 161, 125))
            self.rdbx_W3fdif_filter.Show()
            self.rdbx_W3fdif_deint.Show()
            self.rdbx_Yadif_mode.Show()
            self.rdbx_Yadif_parity.Show()
            self.rdbx_Yadif_deint.Show()
            self.rdbx_inter_scan.Show()
            self.rdbx_inter_lowpass.Show()
        else:
            #self.enable_opt.SetBackgroundColour(wx.NullColour)
            self.rdbx_W3fdif_filter.Hide()
            self.rdbx_W3fdif_deint.Hide()
            self.rdbx_Yadif_mode.Hide()
            self.rdbx_Yadif_parity.Hide()
            self.rdbx_Yadif_deint.Hide()
            self.rdbx_inter_scan.Hide()
            self.rdbx_inter_lowpass.Hide()
            
        self.SetSizer(self.sizer_base)
        self.sizer_base.Fit(self)
        self.Layout()
    #------------------------------------------------------------------#
    def on_reset(self, event):
        """
        Reset all option and values
        """
        self.cmd_opt.clear()# deleting dictionary keys+values
        self.ckbx_deintW3fdif.SetValue(False)
        self.ckbx_deintYadif.SetValue(False)
        self.ckbx_interlace.SetValue(False)
        self.ckbx_deintW3fdif.Enable()
        self.ckbx_deintYadif.Enable()
        self.ckbx_interlace.Enable()
        self.rdbx_W3fdif_filter.SetSelection(1)
        self.rdbx_W3fdif_deint.SetSelection(0)
        self.rdbx_Yadif_mode.SetSelection(1)
        self.rdbx_Yadif_parity.SetSelection(2)
        self.rdbx_Yadif_deint.SetSelection(0)
        self.rdbx_inter_scan.SetSelection(0)
        self.rdbx_inter_lowpass.SetSelection(1)
        self.rdbx_W3fdif_filter.Disable(),self.rdbx_W3fdif_deint.Disable(),
        self.rdbx_Yadif_mode.Disable(), self.rdbx_Yadif_parity.Disable(), 
        self.rdbx_Yadif_deint.Disable(), self.rdbx_inter_scan.Disable(), 
        self.rdbx_inter_lowpass.Disable()
    #------------------------------------------------------------------#
    def on_help(self, event):
        """
        """
        page = ('https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/'
                'VideoConv_Panel/Filters/Deint_Inter.html')
        webbrowser.open(page)
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip()

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        return self.cmd_opt
    
#############################################################################

class Denoisers(wx.Dialog):
    """
    Show a dialog for set denoiser filter
    """
    def __init__(self, parent, denoiser):
        """
        Make sure you use the clear button when you finish the task.
        Enable filters denoiser useful in some case, example when apply
        a deinterlace filter
        <https://askubuntu.com/questions/866186/how-to-get-good-quality-when-
        converting-digital-video>
        """
        if denoiser:
            self.denoiser = denoiser
        else:
            self.denoiser = ''
        wx.Dialog.__init__(self, parent, -1, style=wx.DEFAULT_DIALOG_STYLE)
        
        
        zone = wx.StaticBoxSizer(wx.StaticBox(self, wx.ID_ANY, (
                                    _(u"Apply Denoisers Filters"))), wx.VERTICAL)
        
        self.ckbx_nlmeans = wx.CheckBox(self, wx.ID_ANY, 
                                (_(u"Enable nlmeans denoiser"))
                                            )
        self.rdb_nlmeans = wx.RadioBox(self, wx.ID_ANY, (
               _(u"nlmeans options")), choices=[
               ("Default"),
               ("Old VHS tapes - good starting point restoration"), 
               ("Heavy - really noisy inputs"), 
               ("Light - good quality inputs")], 
               majorDimension=0, style=wx.RA_SPECIFY_ROWS
                                        )
        self.ckbx_hqdn3d = wx.CheckBox(self, wx.ID_ANY, 
                                (_(u"Enable hqdn3d denoiser"))
                                            )
        self.rdb_hqdn3d = wx.RadioBox(self, wx.ID_ANY, (
               _(u"hqdn3d options")), choices=[
                ("Default"),
                ("Conservative [4.0:4.0:3.0:3.0]"),
                ("Old VHS tapes restoration [9.0:5.0:3.0:3.0]")],
                 majorDimension=0, 
                 style=wx.RA_SPECIFY_ROWS
                                        )
        ###----- confirm buttons section
        btn_help = wx.Button(self, wx.ID_HELP, "")
        btn_close = wx.Button(self, wx.ID_CANCEL, "")
        self.btn_ok = wx.Button(self, wx.ID_OK, "")
        btn_reset = wx.Button(self, wx.ID_CLEAR, "")
        
        ####------ set Layout
        self.sizer_base = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_base = wx.FlexGridSizer(2, 1, 0, 0)
        grid_sizer_base.Add(zone, 1, wx.ALL | wx.EXPAND, 5)
        grid_den = wx.FlexGridSizer(2, 2, 0, 0)
        zone.Add(grid_den)

        grid_den.Add(self.ckbx_nlmeans, 0, 
                    wx.ALL |
                    wx.ALIGN_CENTER_VERTICAL | 
                    wx.ALIGN_CENTER_HORIZONTAL,
                    15)
        grid_den.Add(self.rdb_nlmeans, 0, 
                    wx.ALL |
                    wx.ALIGN_CENTER_VERTICAL | 
                    wx.ALIGN_CENTER_HORIZONTAL,
                    15)
        grid_den.Add(self.ckbx_hqdn3d, 0, 
                    wx.ALL |
                    wx.ALIGN_CENTER_VERTICAL | 
                    wx.ALIGN_CENTER_HORIZONTAL,
                    15)
        grid_den.Add(self.rdb_hqdn3d, 0, 
                    wx.ALL |
                    wx.ALIGN_CENTER_VERTICAL | 
                    wx.ALIGN_CENTER_HORIZONTAL,
                    15)
        # confirm btn section:
        #gridBtn = wx.FlexGridSizer(1, 3, 0, 0)
        
        gridhelp = wx.GridSizer(1, 1, 0, 0)
        gridexit = wx.GridSizer(1, 3, 0, 0)
        gridBtn = wx.GridSizer(1, 2, 0, 0)
        gridBtn.Add(gridhelp)
        gridBtn.Add(gridexit)
        
        grid_sizer_base.Add(gridBtn)#, flag=wx.ALL|wx.ALIGN_RIGHT|wx.RIGHT, border=10)
        
        gridhelp.Add(btn_help,1, 
                    wx.ALL | 
                    wx.ALIGN_CENTER_VERTICAL,5)
        gridexit.Add(btn_close,1, 
                    wx.ALL | 
                    wx.ALIGN_CENTER_VERTICAL,5)
        gridexit.Add(self.btn_ok,1, 
                    wx.ALL | 
                    wx.ALIGN_CENTER_VERTICAL,5)
        gridexit.Add(btn_reset,1, 
                    wx.ALL | 
                    wx.ALIGN_CENTER_VERTICAL,5)
        # final settings:
        self.sizer_base.Add(grid_sizer_base, 1, 
                            wx.ALL | 
                            wx.EXPAND, 5)
        self.SetSizer(self.sizer_base)
        self.sizer_base.Fit(self)
        self.Layout()
        
        # set Properties
        self.SetTitle(_(u"Videomass: Denoisers filters"))
        self.ckbx_nlmeans.SetToolTipString(_(u'nlmeans:\n '
            u'(Denoise frames using Non-Local Means algorithm '
            u'is capable of restoring video sequences with even strong '
            u'noise. It is ideal for enhancing the quality of old VHS tapes.'))
        self.ckbx_hqdn3d.SetToolTipString(_(u'hqdn3d:\n '
            u'This is a high precision/quality 3d denoise filter. It aims '
            u'to reduce image noise, producing smooth images and making '
            u'still images really still. It should enhance compressibility.'))
        
        #----------------------Binding (EVT)---------------------------------#
        self.Bind(wx.EVT_CHECKBOX, self.on_nlmeans, self.ckbx_nlmeans)
        self.Bind(wx.EVT_CHECKBOX, self.on_hqdn3d, self.ckbx_hqdn3d)
        self.Bind(wx.EVT_RADIOBOX, self.on_nlmeans_opt, self.rdb_nlmeans)
        self.Bind(wx.EVT_RADIOBOX, self.on_hqdn3d_opt, self.rdb_hqdn3d)
        self.Bind(wx.EVT_BUTTON, self.on_help, btn_help)
        self.Bind(wx.EVT_BUTTON, self.on_close, btn_close)
        self.Bind(wx.EVT_BUTTON, self.on_ok, self.btn_ok)
        self.Bind(wx.EVT_BUTTON, self.on_reset, btn_reset)
        
        self.settings()
        
    def settings(self):
        """
        Set default or set in according with previusly activated option 
        """
        if self.denoiser:
            if self.denoiser.startswith('nlmeans'):
                spl = self.denoiser.split('=')
                if len(spl) == 1:
                    self.rdb_nlmeans.SetSelection(0) 
                else:
                    if spl[1] == '8:3:2':
                        self.rdb_nlmeans.SetSelection(1)
                    if spl[1] == '10:5:3':
                        self.rdb_nlmeans.SetSelection(2)
                    if spl[1] == '6:3:1':
                        self.rdb_nlmeans.SetSelection(3)
                self.ckbx_nlmeans.SetValue(True)
                self.ckbx_hqdn3d.SetValue(False)
                self.ckbx_nlmeans.Enable()
                self.ckbx_hqdn3d.Disable()
                self.rdb_nlmeans.Enable()
                self.rdb_hqdn3d.Disable()
                    
            elif self.denoiser.startswith('hqdn3d'):
                spl = self.denoiser.split('=')
                print spl
                if len(spl) == 1:
                    self.rdb_hqdn3d.SetSelection(0) 
                else:
                    if spl[1] == '4.0:4.0:3.0:3.0':
                        self.rdb_hqdn3d.SetSelection(1)
                    if spl[1] == '9.0:5.0:3.0:3.0':
                        self.rdb_hqdn3d.SetSelection(2)
                
                self.ckbx_nlmeans.SetValue(False)
                self.ckbx_hqdn3d.SetValue(True)
                self.ckbx_nlmeans.Disable()
                self.ckbx_hqdn3d.Enable()
                self.rdb_nlmeans.Disable()
                self.rdb_hqdn3d.Enable()
        else:
            self.ckbx_nlmeans.SetValue(False)
            self.ckbx_hqdn3d.SetValue(False)
            self.ckbx_nlmeans.Enable()
            self.ckbx_hqdn3d.Enable()
            self.rdb_nlmeans.SetSelection(0)
            self.rdb_nlmeans.Disable()
            self.rdb_hqdn3d.Disable()
    
    #----------------------Event handler (callback)--------------------------#
    #------------------------------------------------------------------------#
    def on_nlmeans(self, event):
        """
        """
        if self.ckbx_nlmeans.IsChecked():
            self.rdb_nlmeans.Enable()
            self.rdb_hqdn3d.Disable()
            self.ckbx_hqdn3d.Disable()
            self.denoiser = "nlmeans"
            
        elif not self.ckbx_nlmeans.IsChecked():
            self.rdb_nlmeans.Disable()
            self.ckbx_hqdn3d.Enable()
            self.denoiser = ""
    #------------------------------------------------------------------#
    def on_nlmeans_opt(self, event):
        """
        """
        opt = self.rdb_nlmeans.GetStringSelection()
        if opt == "Default":
            self.denoiser = "nlmeans"
        elif opt == "Old VHS tapes - good starting point restoration":
            self.denoiser = "nlmeans=8:3:2"
        elif opt == "Heavy - really noisy inputs":
            self.denoiser = "nlmeans=10:5:3"
        elif opt == "Light - good quality inputs":
            self.denoiser = "nlmeans=6:3:1"
    #------------------------------------------------------------------#
    def on_hqdn3d(self, event):
        """
        """
        if self.ckbx_hqdn3d.IsChecked():
            self.ckbx_nlmeans.Disable()
            self.rdb_hqdn3d.Enable()
            self.denoiser = "hqdn3d"
            
        elif not self.ckbx_hqdn3d.IsChecked():
            self.ckbx_nlmeans.Enable()
            self.rdb_hqdn3d.Disable()
            self.denoiser = ""
    #------------------------------------------------------------------# 
    def on_hqdn3d_opt(self, event):
        """
        """
        opt = self.rdb_hqdn3d.GetStringSelection()
        if opt == "Default":
            self.denoiser = "hqdn3d"
            
        elif opt == "Conservative [4.0:4.0:3.0:3.0]":
            self.denoiser = "hqdn3d=4.0:4.0:3.0:3.0"
            
        elif opt == "Old VHS tapes restoration [9.0:5.0:3.0:3.0]":
            self.denoiser = "hqdn3d=9.0:5.0:3.0:3.0"
    #------------------------------------------------------------------#
    def on_help(self, event):
        """
        """
        page = ('https://jeanslack.github.io/Videomass/Pages/Main_Toolbar/'
                'VideoConv_Panel/Filters/Denoisers.html')
        webbrowser.open(page)
    #------------------------------------------------------------------#  
    def on_reset(self, event):
        """
        Reset all option and values
        """
        self.denoiser = ""# deleting dictionary keys+values
        self.ckbx_nlmeans.SetValue(False)
        self.ckbx_hqdn3d.SetValue(False)
        self.ckbx_nlmeans.Enable()
        self.ckbx_hqdn3d.Enable()
        self.rdb_nlmeans.SetSelection(0)
        self.rdb_nlmeans.Disable()
        self.rdb_hqdn3d.SetSelection(0)
        self.rdb_hqdn3d.Disable()
    #------------------------------------------------------------------#
    def on_close(self, event):

        event.Skip()

    #------------------------------------------------------------------#
    def on_ok(self, event):
        """
        if you enable self.Destroy(), it delete from memory all data event and
        no return correctly. It has the right behavior if not used here, because 
        it is called in the main frame. 
        
        Event.Skip(), work correctly here. Sometimes needs to disable it for
        needs to maintain the view of the window (for exemple).
        """
        self.GetValue()
        #self.Destroy()
        event.Skip()
    #------------------------------------------------------------------#
    def GetValue(self):
        """
        This method return values via the interface GetValue()
        """
        return self.denoiser

