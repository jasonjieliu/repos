#!/usr/bin/python
# coding:utf-8

import wx
import os
import sys
import collections

class CalcWindow(wx.Frame):
    def __init__(self, parent, title):
        super(CalcWindow, self).__init__(parent = parent,
                                         title = title,
                                         size = (280, 250),
                                         style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                         name = os.path.basename(sys.argv[0]).split('.')[0])

        self.list = []

        self.window_init()
        self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        box_calculator = wx.BoxSizer(wx.VERTICAL)

        self.display = wx.TextCtrl(self, style = wx.TE_RIGHT | wx.TE_READONLY)

        self.display.SetValue('0')

        box_calculator.Add(self.display, flag = wx.EXPAND | wx.TOP | wx.BOTTOM, border = 5)

        self.gridsizer_init()

        box_calculator.Add(self.gridsizer, flag = wx.EXPAND, proportion = 1)

        self.vbox.Add((-1, 10))
        self.vbox.Add(box_calculator,
                      flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                      border = 5,
                      proportion = 1)

        self.SetSizer(self.vbox)

    def gridsizer_init(self):
        self.button_dict = collections.OrderedDict()

        self.button_dict[102] = ('clear', self.button_event)
        self.button_dict[8] = ('back', self.button_event)
        self.button_dict[101] = ('', None)
        self.button_dict[27] = ('close', self.button_event)
        self.button_dict[55] = ('7', self.button_event)
        self.button_dict[56] = ('8', self.button_event)
        self.button_dict[57] = ('9', self.button_event)
        self.button_dict[47] = ('/', self.button_event)
        self.button_dict[52] = ('4', self.button_event)
        self.button_dict[53] = ('5', self.button_event)
        self.button_dict[54] = ('6', self.button_event)
        self.button_dict[42] = ('*', self.button_event)
        self.button_dict[49] = ('1', self.button_event)
        self.button_dict[50] = ('2', self.button_event)
        self.button_dict[51] = ('3', self.button_event)
        self.button_dict[45] = ('-', self.button_event)
        self.button_dict[48] = ('0', self.button_event)
        self.button_dict[46] = ('.', self.button_event)
        self.button_dict[13] = ('=', self.button_event)
        self.button_dict[43] = ('+', self.button_event)

        self.gridsizer = wx.GridSizer(5, 4, 5, 5)

        for (each_key, each_bt) in self.button_dict.items():
            if len(each_bt[0]):
                bt = wx.Button(self, wx.NewId(), label = each_bt[0])
                bt.Bind(wx.EVT_BUTTON, each_bt[1])
                bt.Bind(wx.EVT_CHAR, self.keyboard_down)
            else:
                bt = wx.StaticText(self)
            self.gridsizer.AddMany([(bt, 0, wx.EXPAND)])

    def event_init(self):
        # self.Bind(wx.EVT_KEY_DOWN, self.keyboard_down) # 键盘事件不区分大小写，全部按大写来
        # self.Bind(wx.EVT_KEY_UP, self.keyboard_down) # 键盘事件不区分大小写，全部按大写来

        self.Bind(wx.EVT_CHAR, self.keyboard_down) # 键盘事件区分大小写

    def button_event(self, event):
        self.input_event(self.FindWindowById(event.GetId()).GetLabel())

    def keyboard_down(self, event):
        if self.button_dict.has_key(event.GetKeyCode()) and self.button_dict[event.GetKeyCode()][1]:
            self.input_event(self.button_dict[event.GetKeyCode()][0])

    def input_event(self, lable_name):
        if lable_name == 'close':
            self.Destroy()
            return

        if lable_name == 'clear':
            self.display.SetValue('0')
            self.list = []
            return

        if lable_name == 'back':
            if 1 == len(self.display.GetValue()):
                self.display.SetValue('0')
            else:
                self.display.SetValue(self.display.GetValue()[0:-1])
            return

        if '0' == self.display.GetValue() and lable_name == '0':
            return

        if lable_name in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']:
            if '0' == self.display.GetValue() and lable_name != '.':
                self.display.SetValue(lable_name)
            else:
                self.display.SetValue(self.display.GetValue() + lable_name)
            return

        if lable_name in ['+', '-', '*', '/']:
            if '0' == self.display.GetValue():
                return

            self.list.append(self.display.GetValue())
            if len(self.list) and self.list[-1] not in ['+', '-', '*', '/']:
                self.list.append(lable_name)
            self.display.SetValue('0')
            return

        if lable_name == '=':
            self.list.append(self.display.GetValue())
            self.display.SetValue('')
            for i in range(0, len(self.list)):
                self.display.SetValue(self.display.GetValue() + ' ' + self.list[i])
            self.list = []

if __name__ == '__main__':
    app = wx.App()
    CalcWindow(None, title = unicode('计算器', 'utf-8'))
    app.MainLoop()
