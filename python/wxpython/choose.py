#!/usr/bin/python
# coding:utf-8

import wx
import random
from form import *
from list import *
from calculator import *
from draw_pictrue import *


class ChooseWindow(wx.Frame):
    def __init__(self, parent, title):
        super(ChooseWindow, self).__init__(parent = parent,
                                     title = title,
                                     size = (350, 250),
                                     style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                     name = os.path.basename(sys.argv[0]).split('.')[0])

        self.font_init()
        self.window_init()
        self.event_init()
        self.Centre()
        self.Show()

    def font_init(self):
        '''
        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        wx.Font(pointsize,
            family,
            style,
            weight,
            underline = false,
            face = emptystring,
            encoding = FONTENCODING_DEFAULT)
        pointsize:字体大小
        family:字体类型
            wx.DECORATIVE：一个正式的老的英文样式字体。
            wx.DEFAULT   ：系统默认字体。
            wx.MODERN    ：一个单间隔（固定字符间距）字体。
            wx.ROMAN     ：serif字体，通常类似于Times New Roman。
            wx.SCRIPT    ：手写体或草写体。
            wx.SWISS     ：sans-serif字体，通常类似于Helvetica或Arial。
        style:字体样式
            wx.NORMAL
            wx.SLANT
            wx.ITALIC
        weight:字体醒目程度
            wx.NORMAL
            wx.LIGHT
            wx.BOLD
        face:字体名
        encoding:字体编码
        '''
        self.font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD, face = unicode('自定义', 'utf-8'))

    def window_init(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.panel_init()

        self.gridsizer_init()

        self.vbox.Add((-1, 10))
        self.vbox.Add(self.gridsizer,
                      flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP | wx.BOTTOM,
                      border = 5,
                      proportion = 1)

        self.SetSizer(self.vbox)

        self.status_bar_init()

    def panel_init(self):
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(random.choice(
            ['Green', 'Yellow', 'Grey', 'Red', 'White', 'Black']))
        self.panel.SetBackgroundColour(
            (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        self.panel.Refresh()

    def gridsizer_init(self):
        self.button = [
            (unicode('表格', 'utf-8'), self.button_event, FormWindow),
            (unicode('列表', 'utf-8'), self.button_event, ListWindow),
            (unicode('计算器', 'utf-8'), self.button_event, CalcWindow),
            (unicode('画图', 'utf-8'), self.button_event, DrawWindow),
            (unicode('暂未使用', 'utf-8'), self.button_event, None),
            (unicode('暂未使用', 'utf-8'), self.button_event, None)
        ]

        self.gridsizer = wx.GridSizer(2, 3, 5, 5)

        for each_bt in self.button:
            bt = wx.Button(self, wx.NewId(), label = each_bt[0], size = (30, 30))
            bt.SetFont(self.font)
            bt.Bind(wx.EVT_BUTTON, each_bt[1])
            bt.Bind(wx.EVT_ENTER_WINDOW, each_bt[1])
            bt.Bind(wx.EVT_LEAVE_WINDOW, each_bt[1])
            bt.Bind(wx.EVT_LEFT_UP, each_bt[1])
            bt.Bind(wx.EVT_LEFT_DOWN, each_bt[1])
            bt.Bind(wx.EVT_RIGHT_UP, each_bt[1])
            bt.Bind(wx.EVT_RIGHT_DOWN, each_bt[1])
            bt.Bind(wx.EVT_MOTION, self.mouse_move)
            self.gridsizer.AddMany([(bt, 0, wx.EXPAND)])

    def status_bar_init(self):
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(3)
        self.status_bar.SetStatusWidths([-1, -2, -2])

        self.status_bar.SetStatusText(unicode('Ready', 'utf-8'), 0)
        self.status_bar.SetStatusText(unicode('鼠标位置: 0,0', 'utf-8'), 1)
        self.status_bar.SetStatusText(unicode('窗口位置: 0,0', 'utf-8'), 2)

    def event_init(self):
        # 窗口坐标
        self.Bind(wx.EVT_MOVE, self.mouse_move)
        # 鼠标坐标
        self.Bind(wx.EVT_MOTION, self.mouse_move)
        self.Bind(wx.EVT_PAINT, self.repaint)
        self.Bind(wx.EVT_CLOSE, self.window_close)

    def button_event(self, event):
        '''
        FindWindowById   : 根据控件id获取控件
        FindWindowByLabel: 根据控件标签获取控件
        FindWindowByName : 根据控件名称获取控件
        '''
        if event.EventType in [wx.EVT_BUTTON.typeId, wx.EVT_LEFT_DOWN.typeId]:
            lable_name = self.FindWindowById(event.GetId()).GetLabel()

            for each_bt in self.button:
                if each_bt[0] == lable_name and each_bt[2]:
                    each_bt[2](None, lable_name)
                    #self.Destroy()

        elif event.EventType == wx.EVT_ENTER_WINDOW.typeId:
            self.status_bar.SetStatusText('enter', 0)
            self.FindWindowById(event.GetId()).SetBackgroundColour('green')
        elif event.EventType == wx.EVT_LEAVE_WINDOW.typeId:
            self.status_bar.SetStatusText('leave', 0)
            self.FindWindowById(event.GetId()).SetBackgroundColour('default')
        elif event.EventType == wx.EVT_LEFT_UP.typeId:
            self.status_bar.SetStatusText('left up', 0)
        elif event.EventType == wx.EVT_RIGHT_UP.typeId:
            self.status_bar.SetStatusText('right up', 0)
        elif event.EventType == wx.EVT_RIGHT_DOWN.typeId:
            self.status_bar.SetStatusText('right down', 0)

    def mouse_move(self, event):
        if wx.EVT_MOVE.typeId == event.EventType:
            self.status_bar.SetStatusText(
                unicode('窗口位置: %s, %d' % (event.GetPosition()[0], event.GetPosition()[1]), 'utf-8'), 2)
        elif wx.EVT_MOTION.typeId == event.EventType:
            self.status_bar.SetStatusText(unicode('鼠标位置: %s, %d' % (event.GetPosition()[0], event.GetPosition()[1]), 'utf-8'), 1)
        else:
            pass

    def repaint(self, event):
        self.Refresh()

    def window_close(self, event):
        '''
        wx.OK              : show Ok button
        wx.CANCEL          : show Cancel button
        wx.YES_NO          : show Yes, No buttons
        wx.YES_DEFAULT     : make Yes button the default
        wx.NO_DEFAULT      : make No button the default
        wx.ICON_EXCLAMATION: show an alert icon
        wx.ICON_ERROR      : show an error icon
        wx.ICON_HAND       : same as wx.ICON_ERROR
        wx.ICON_INFORMATION: show an info icon
        wx.ICON_QUESTION   : show a question icon
        '''

        dlg = wx.MessageDialog(self,
                               unicode('确定退出？', 'utf-8'),
                               unicode('选择', 'utf-8'),
                               wx.YES_NO | wx.YES_DEFAULT | wx.ICON_QUESTION)

        if dlg.ShowModal() == wx.ID_YES:
            self.Destroy()
        else:
            event.Veto()

if __name__ == '__main__':
    app = wx.App()
    ChooseWindow(None, title = unicode('选择', 'utf-8'))
    app.MainLoop()
