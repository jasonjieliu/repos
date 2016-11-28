#!/usr/bin/python
# coding:utf-8

import wx


class Calculator(wx.Frame):
    def __init__(self, parent, title):
        super(Calculator, self).__init__(parent = parent,
                                         title = title,
                                         size = (280, 200),
                                         style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                         name = 'calculator window')

        self.window_init()
        # self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.display = wx.TextCtrl(self, style = wx.TE_RIGHT)

        self.vbox.Add(self.display, flag = wx.EXPAND | wx.TOP | wx.BOTTOM, border = 5)

        # 行 列 行间隔 列间隔
        self.grid = wx.GridSizer(5, 4, 5, 5)
        self.grid.AddMany([(wx.Button(self, label = 'clear'), 0, wx.EXPAND),
                           (wx.Button(self, label = 'back'), 0, wx.EXPAND),
                           (wx.StaticText(self), wx.EXPAND),
                           (wx.Button(self, label = 'close'), 0, wx.EXPAND),
                           (wx.Button(self, label = '7'), 0, wx.EXPAND),
                           (wx.Button(self, label = '8'), 0, wx.EXPAND),
                           (wx.Button(self, label = '9'), 0, wx.EXPAND),
                           (wx.Button(self, label = '/'), 0, wx.EXPAND)])
        self.grid.AddMany([(wx.Button(self, label = '4'), 0, wx.EXPAND),
                           (wx.Button(self, label = '5'), 0, wx.EXPAND),
                           (wx.Button(self, label = '6'), 0, wx.EXPAND),
                           (wx.Button(self, label = '*'), 0, wx.EXPAND),
                           (wx.Button(self, label = '1'), 0, wx.EXPAND),
                           (wx.Button(self, label = '2'), 0, wx.EXPAND),
                           (wx.Button(self, label = '3'), 0, wx.EXPAND),
                           (wx.Button(self, label = '-'), 0, wx.EXPAND),
                           (wx.Button(self, label = '0'), 0, wx.EXPAND),
                           (wx.Button(self, label = '.'), 0, wx.EXPAND),
                           (wx.Button(self, label = '='), 0, wx.EXPAND),
                           (wx.Button(self, label = '+'), 0, wx.EXPAND)])

        self.vbox.Add(self.grid, flag = wx.EXPAND, proportion = 1)
        self.SetSizer(self.vbox)


if __name__ == '__main__':
    app = wx.App()
    Calculator(None, title = 'GridSizer')
    app.MainLoop()
