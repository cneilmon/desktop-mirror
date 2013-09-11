#!/usr/bin/env python
import wx


class MyFrame(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title,
                          style=wx.RESIZE_BORDER | wx.STAY_ON_TOP |
                          wx.FRAME_NO_TASKBAR | wx.CLIP_CHILDREN)

        self.rootPanel = wx.Panel(self)
        self.rootPanel.SetBackgroundColour(wx.Colour(128, 0, 0))

        centerPanel = wx.Panel(self.rootPanel)
        centerPanel.SetBackgroundColour(wx.Colour(0, 128, 0))

        innerPanel = wx.Panel(centerPanel)
        innerPanel.SetBackgroundColour(wx.Colour(0, 0, 128))

        rootBox = wx.BoxSizer(wx.HORIZONTAL)
        centerBox = wx.BoxSizer(wx.HORIZONTAL)
        innerBox = wx.BoxSizer(wx.VERTICAL)

        # I want this line visible in the CENTRE of the inner panel
        self.txt = wx.StaticText(innerPanel,
                                 label="Start Live!")
        self.txt.SetFont(wx.Font(20, wx.MODERN, wx.NORMAL, wx.BOLD))
        innerBox.Add(self.txt, 0, wx.ALL | wx.ALIGN_CENTER, border=0)
        innerPanel.SetSizer(innerBox)

        centerBox.Add(innerPanel, 1, wx.ALL | wx.ALIGN_CENTER, border=0)
        centerPanel.SetSizer(centerBox)

        rootBox.Add(centerPanel, 1, wx.ALL | wx.ALIGN_CENTER | wx.EXPAND, border=5)
        self.rootPanel.SetSizer(rootBox)

        rootBox.Fit(self)

        centerPanel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseEvents)
        innerPanel.Bind(wx.EVT_LEFT_DOWN, self.OnMouseEvents)
        self.txt.Bind(wx.EVT_LEFT_DOWN, self.OnMouseEvents)

        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_title)
        self.timer.Start(60)  # in miliseconds
        self.background_colour = 0
        self.mouse_start_pos = None
        self.mouse_end_pos = None
        self.step = 0
        self.count_to_next_step = 0

    def update_title(self, event):
        # border colorize
        if self.step >= 1:
            self.background_colour = (self.background_colour + 8) % 512
            if self.background_colour >= 256:
                colour = 511 - self.background_colour
            else:
                colour = self.background_colour
            self.rootPanel.SetBackgroundColour(wx.Colour(colour,
                                                         colour,
                                                         colour))
        # move window
        if self.step == 0:
            pos = wx.GetMousePosition()
            self.SetPosition((pos.x, pos.y))
            self.SetSize((1, 1))
            self.mouse_start_pos = pos
        if self.step == 1:
            pos = wx.GetMousePosition()
            x = pos.x if pos.x < self.mouse_start_pos.x else self.mouse_start_pos.x
            y = pos.y if pos.y < self.mouse_start_pos.y else self.mouse_start_pos.y
            w = pos.x if pos.x > self.mouse_start_pos.x else self.mouse_start_pos.x
            h = pos.y if pos.y > self.mouse_start_pos.y else self.mouse_start_pos.y
            if (w - x) >= 10 or (h - y) >= 10:
                self.step = 2
        if self.step >= 2 and self.step <= 3:
            pos = wx.GetMousePosition()
            x = pos.x if pos.x < self.mouse_start_pos.x else self.mouse_start_pos.x
            y = pos.y if pos.y < self.mouse_start_pos.y else self.mouse_start_pos.y
            w = pos.x if pos.x > self.mouse_start_pos.x else self.mouse_start_pos.x
            h = pos.y if pos.y > self.mouse_start_pos.y else self.mouse_start_pos.y
            if (w - x) <= 10:
                w = x + 10
            if (h - y) <= 10:
                h = y + 10
            w += 1
            h += 1
            self.SetPosition((x, y))
            self.SetSize((w - x, h - y))
            self.mouse_end_pos = pos

        # start point
        if self.step == 0 and wx.GetMouseState().LeftDown():
            self.txt.SetLabel('')

        # end point
        if self.step == 3 and not wx.GetMouseState().LeftDown():
            self.txt.SetLabel('Start Live!')

        # confirm
        if self.step == 5 and not wx.GetMouseState().LeftDown():
            self.Close(True)

        # increment
        odd = (self.step % 2) == 1
        if not odd and wx.GetMouseState().LeftDown():
            self.step += 1
        if odd and not wx.GetMouseState().LeftDown():
            self.step += 1

    def OnMouseEvents(self, e):
        self.step = 7
        self.Close(True)

    def OnClose(self, event):
        if self.step == 7:
            pos = self.mouse_end_pos
            x = pos.x if pos.x < self.mouse_start_pos.x else self.mouse_start_pos.x
            y = pos.y if pos.y < self.mouse_start_pos.y else self.mouse_start_pos.y
            w = pos.x if pos.x > self.mouse_start_pos.x else self.mouse_start_pos.x
            h = pos.y if pos.y > self.mouse_start_pos.y else self.mouse_start_pos.y
            print '{}x{}+{}+{}'.format(x, y, w, h)
        self.Destroy()

class MyApp(wx.App):
    def OnInit(self):
        frame = MyFrame(None, -1, 'Live Area')
        frame.Show(True)
        frame.Center()
        frame.SetTransparent(100)
        return True

app = MyApp(0)
app.MainLoop()
