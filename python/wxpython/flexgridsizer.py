#!/usr/bin/python
# coding:utf-8

import wx


class Flexgrid(wx.Frame):
    def __init__(self, parent, title):
        super(Flexgrid, self).__init__(parent = parent,
                                       title = title,
                                       size = (280, 400),
                                       style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                       name = 'calculator window')

        self.window_init()
        # self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        self.panel = wx.Panel(self)

        self.vbox = wx.BoxSizer(wx.HORIZONTAL)

        self.flexgrid = wx.FlexGridSizer(3, 2, 9, 25)

        self.title = wx.StaticText(self.panel, label = 'Title:')
        self.author = wx.StaticText(self.panel, label = 'Author:')
        self.review = wx.StaticText(self.panel, label = 'Review:')

        self.text_title = wx.TextCtrl(self.panel)
        self.text_author = wx.TextCtrl(self.panel)
        self.text_review = wx.TextCtrl(self.panel, style = wx.TE_MULTILINE)

        self.flexgrid.AddMany([(self.title),
                               (self.text_title, 1, wx.EXPAND),
                               (self.author),
                               (self.text_author, 2, wx.EXPAND),
                               (self.review),
                               (self.text_review, 3, wx.EXPAND)])

        '''
        AddGrowableRow(idx, proportion = 0): 索引为idx的行为扩展行, 占用列比例为proportion
        AddGrowableCol(idx, proportion = 0): 索引为idx的列为扩展列, 占用行比例为proportion
            行和列都从0开始
        '''
        self.flexgrid.AddGrowableCol(1, 1)
        self.flexgrid.AddGrowableRow(2, 1)

        self.vbox.Add(self.flexgrid, flag = wx.ALL | wx.EXPAND, proportion = 1, border = 15)
        self.panel.SetSizer(self.vbox)


if __name__ == '__main__':
    app = wx.App()
    Flexgrid(None, title = 'FlexGridSizer')
    app.MainLoop()
