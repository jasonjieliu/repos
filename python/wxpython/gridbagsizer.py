#!/usr/bin/python
# coding:utf-8

import wx

class Gridbag(wx.Frame):
    def __init__(self, parent, title):
        super(Gridbag, self).__init__(parent = parent,
                                      title = title,
                                      size = (320, 150),
                                      style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                      name = 'calculator window')

        self.window_init()
        # self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        self.panel = wx.Panel(self)

        self.gridbag = wx.GridBagSizer(4, 4)

        self.gridbag.Add(wx.StaticText(self.panel, label = 'Rename to'),
                         pos = (0, 0),
                         flag = wx.TOP | wx.LEFT | wx.BOTTOM,
                         border = 5)

        self.gridbag.Add(wx.TextCtrl(self.panel),
                         pos = (1, 0),
                         span = (1, 3),
                         flag = wx.LEFT | wx.RIGHT,
                         border = 5)

        self.gridbag.Add(wx.Button(self.panel, label = 'OK', size = (90, 28)),
                         pos = (3, 3))
        self.gridbag.Add(wx.Button(self.panel, label = 'EXIT', size = (90, 28)),
                         pos = (3, 4),
                         flag = wx.RIGHT | wx.BOTTOM,
                         border = 5)

        self.gridbag.AddGrowableRow(2)
        self.gridbag.AddGrowableCol(1)

        self.panel.SetSizerAndFit(self.gridbag)

if __name__ == '__main__':
    app = wx.App()
    Gridbag(None, title = 'GridBagSizer')
    app.MainLoop()
