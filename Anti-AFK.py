import time
import math
import wx
import pyautogui
from pynput.mouse import Controller
from _thread import *

def getCurTime():
    return int(time.time())

mouseController = Controller()#mouse movement controller
lastMoveTime = getCurTime()#current time
lastMousePos = mouseController.position#current mouse position
akfEnabled = False

def listenAFK():
    global mouseController
    global lastMoveTime
    global lastMousePos
    global akfEnabled
    while True:
        time.sleep(30)#check or move at most once every second
        if akfEnabled:
            if (lastMousePos != Controller().position):#check if mouse moved
                lastMoveTime = getCurTime()#set last moved time to now
                lastMousePos = Controller().position #update mouse position

            elif ((getCurTime() - lastMoveTime) > 30):
                # Radius
                R = 30
                #Location of current mouse pos
                (X,Y) = lastMousePos
                # offsetting by radius
                pyautogui.moveTo(X+R,Y)

                for i in range(360):
                    # setting pace with a modulus
                    if i%6==0:
                        pyautogui.moveTo(X+R*math.cos(math.radians(i)),Y+R*math.sin(math.radians(i)))

                pyautogui.moveTo(X,Y)

start_new_thread(listenAFK, ())

class GUIFrame(wx.Frame):

    def __init__(self, parent, title):
        super(GUIFrame, self).__init__(parent, title=title)

        self.InitUI()
        self.Centre()
        self.SetMaxSize(wx.Size(width=301, height=151))
        self.SetMinSize(wx.Size(width=300, height=150))
        self.SetSize(wx.Size(300, 150))

    def InitUI(self):

        vbox = wx.BoxSizer(wx.VERTICAL)
        gs = wx.GridSizer(3, 1, 0, 0)

        self.SetBackgroundColour("WHITE")
        self.statusLbl = wx.StaticText(self, label="Status: off")
        self.toggleBtn = wx.Button(self, label='Toggle')
        self.toggleBtn.Bind(wx.EVT_BUTTON, self.toggleOn)

        gs.AddMany([
            (wx.StaticText(self, label="Anti-AFK mouse mover"), wx.ALIGN_CENTER , wx.ALIGN_CENTER),
            (self.statusLbl, wx.ALIGN_CENTER , wx.ALIGN_CENTER),
            (self.toggleBtn, wx.ALIGN_CENTER , wx.ALIGN_CENTER)
            ])

        vbox.Add(gs, proportion=1, flag=wx.EXPAND)
        self.SetSizer(vbox)

    def toggleOn(self, e):
        global akfEnabled
        akfEnabled = not akfEnabled
        if (akfEnabled):
            self.statusLbl.SetLabel("Status: on")
        else:
            self.statusLbl.SetLabel("Status: off")

def Main():
    app = wx.App()
    global frm
    frm = GUIFrame(None, title='Anti-AFK')
    frm.Show()
    app.MainLoop()

if __name__ == '__main__':
    Main()