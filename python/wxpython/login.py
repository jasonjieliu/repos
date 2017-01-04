#!/usr/bin/python
# coding:utf-8

import wx
import os
import sys
from choose import *

class LoginWindow(wx.Frame):
    def __init__(self, parent, title):
        super(LoginWindow, self).__init__(parent = parent,
                                    title = title,
                                    size = (280, 200),
                                    style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                    name = os.path.basename(sys.argv[0]).split('.')[0])

        self.window_init()
        self.font_init()
        self.event_init()
        self.Centre()
        self.Show()

        for list in self.GetChildren()[0].GetChildren():
            print list

        print type(self.GetChildren())

    def window_init(self):
        self.panel = wx.Panel(self)

        '''
        wx.VERTICAL  : 垂直方向
        wx.HORIZONTAL: 水平方向
        '''
        self.vbox = wx.BoxSizer(wx.VERTICAL)
        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box3 = wx.BoxSizer(wx.HORIZONTAL)
        box4 = wx.BoxSizer(wx.HORIZONTAL)

        '''
        wx.ALIGN_CENTER    : 文本在控件中心
        wx.ALIGN_LEFT      : 文本在控件左对齐, 默认方式
        wx.ALIGN_RIGHT     : 文本在控件右对齐
        wx.ST_NO_AUTORESIZE: 文件自动适应
        '''
        self.label_user = wx.StaticText(self.panel,
                                        label = unicode('用户名:', 'utf-8'),
                                        style = wx.ALIGN_LEFT)
        '''
        wx.TE_CENTER       : 文本在控件中心
        wx.TE_LEFT         : 文件在控件左对齐, 默认方式
        wx.TE_RIGHT        : 文本在控件右对齐
        wx.TE_NOHIDESEL    : 文件高亮
        wx.TE_PASSWORD     : 文件以星号代替
        wx.TE_PROCESS_ENTER: 回车触发文件输入事件
        wx.TE_PROCESS_TAB  : TAB当作字符输入文本, 否则进行控件间的切换
        wx.TE_READONLY     : 文本只读
        '''
        self.text_user = wx.TextCtrl(self.panel, style = wx.TE_NOHIDESEL | wx.TE_PROCESS_ENTER)

        '''
        flag        : 设置和周围的间隔方式。
        border      : 设置和周围的间隔像素。
        proportion  : 设置所占用Sizer的比例。
        '''
        box1.Add(self.label_user, flag = wx.LEFT, border = 10)
        box1.Add(self.text_user, flag = wx.RIGHT, border = 10, proportion = 1)

        self.label_passwd = wx.StaticText(self.panel, label = unicode('密    码:', 'utf-8'))

        self.text_passwd = wx.TextCtrl(self.panel, style = wx.TE_PASSWORD | wx.TE_PROCESS_ENTER)

        box2.Add(self.label_passwd, flag = wx.LEFT, border = 10)
        box2.Add(self.text_passwd, flag = wx.RIGHT, border = 10, proportion = 1)

        self.text_user.SetValue('username')

        self.bt_ok = wx.Button(self.panel, label = unicode('登陆', 'utf-8'), size = (70, 30))
        self.bt_exit = wx.Button(self.panel, label = unicode('取消', 'utf-8'), size = (70, 30))

        box3.Add(self.bt_ok, flag = wx.LEFT | wx.RIGHT, border = 30)
        box3.Add(self.bt_exit, flag = wx.LEFT | wx.RIGHT, border = 30)

        # CheckBox
        self.normal = wx.RadioButton(self.panel,
                                    label = unicode('正常登录', 'utf-8'),
                                    style = wx.RB_GROUP)
        self.anonymity = wx.RadioButton(self.panel,
                                    label = unicode('匿名登录', 'utf-8'))

        box4.Add(self.normal, flag = wx.LEFT | wx.RIGHT, border = 25)
        box4.Add(self.anonymity, flag = wx.LEFT | wx.RIGHT, border = 25)

        self.vbox.Add((-1, 10))
        self.vbox.Add(box1, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 1)
        self.vbox.Add((-1, 10))
        self.vbox.Add(box2, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 1)
        self.vbox.Add((-1, 10))
        self.vbox.Add(box3, flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border = 1)
        self.vbox.Add((-1, 10))
        self.vbox.Add(box4, flag = wx.ALIGN_RIGHT | wx.RIGHT, border = 10)
        self.vbox.Add((-1, 10))

        self.panel.SetSizer(self.vbox)

    def font_init(self):
        self.font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        self.font.SetPointSize(10)

        self.label_user.SetFont(self.font)
        self.label_passwd.SetFont(self.font)
        self.normal.SetFont(self.font)
        self.anonymity.SetFont(self.font)

    def event_init(self):
        '''
        事件描述
        EVT_SIZE                 : 由于用户干预或由程序实现，当一个窗口大小发生改变时发送给窗口。
        EVT_MOVE                 : 由于用户干预或由程序实现，当一个窗口被移动时发送给窗口。
        EVT_CLOSE                : 当一个框架被要求关闭时发送给框架。除非关闭是强制性的，否则可以调用event.Veto(true)来取消关闭。
        EVT_PAINT                : 无论何时当窗口的一部分需要重绘时发送给窗口。
        EVT_CHAR                 : 当窗口拥有输入焦点时，每产生非修改性（Shift键等等）按键时发送。
        EVT_IDLE                 : 这个事件会当系统没有处理其它事件时定期的发送。
        EVT_LEFT_DOWN            : 鼠标左键按下。
        EVT_LEFT_UP              : 鼠标左键抬起。
        EVT_LEFT_DCLICK          : 鼠标左键双击。
        EVT_MOTION               : 鼠标在移动。
        EVT_SCROLL               : 滚动条被操作。这个事件其实是一组事件的集合，如果需要可以被单独捕捉。
        EVT_BUTTON               : 按钮被点击。
        EVT_MENU                 : 菜单被选中。
        '''
        self.Bind(wx.EVT_PAINT, self.repaint_event)
        self.bt_ok.Bind(wx.EVT_BUTTON, self.login_event)
        self.bt_exit.Bind(wx.EVT_BUTTON, self.exit_event)
        self.normal.Bind(wx.EVT_RADIOBUTTON, self.choice_event)
        self.anonymity.Bind(wx.EVT_RADIOBUTTON, self.choice_event)
        self.Bind(wx.EVT_TEXT_ENTER, self.login_event, self.text_user)
        self.Bind(wx.EVT_TEXT_ENTER, self.login_event, self.text_passwd)

    def repaint_event(self, event):
        self.Refresh()

    def choice_event(self, event):
        pass

    def login_event(self, event):
        if self.user_check(self.text_user.GetValue(), self.text_passwd.GetValue()) or self.anonymity.GetValue():
            self.exit_event(event)
            ChooseWindow(None, unicode('应用选择', 'utf-8'))
        else:

            dlg = wx.MessageDialog(self,
                                   unicode('用户名或者密码有误', 'utf-8'),
                                   unicode('登陆', 'utf-8'),
                                   wx.OK)
            dlg.ShowModal()
            dlg.Destroy()

    def user_check(self, username, password):
        if username == 'root' and password == '111111':
            return True
        else:
            return False

    def exit_event(self, event):
        self.Destroy()

    def keyboard_down_event(self, event):
        print event.GetKeyCode()

if __name__ == '__main__':
    app = wx.App()
    LoginWindow(None, title = unicode('登陆', 'utf-8'))
    app.MainLoop()
