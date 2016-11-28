#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import wx
import wx.lib.buttons
import cPickle


class PaintWindow(wx.Window):
    def __init__(self, parent):
        super(PaintWindow, self).__init__(parent, -1)

        self.window_init()
        self.event_init()

    def window_init(self):
        self.SetBackgroundColour("White")

        self.color = 'Green'
        self.thickness = 10

        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

        self.lines = []
        self.cur_lines = []
        self.pos = (0, 0)

        self.buffer_init()

    def buffer_init(self):
        # 创建缓存的设备上下文
        self.buffer = wx.EmptyBitmap(self.GetClientSize().width, self.GetClientSize().height)
        dc = wx.BufferedDC(None, self.buffer)

        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))  # 使用设备上下文
        dc.Clear()

        self.draw_lines(dc)
        self.buffer_reinit_flag = False

    def draw_lines(self, dc):
        for colour, thickness, line in self.lines:
            pen = wx.Pen(colour, thickness, wx.SOLID)
            dc.SetPen(pen)
            for coords in line:
                dc.DrawLine(*coords)

    def color_set(self, color):
        self.color = color
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def thickness_set(self, thickness):
        self.thickness = thickness
        self.pen = wx.Pen(self.color, self.thickness, wx.SOLID)

    def lines_get(self):
        return self.lines[:]

    def lines_set(self, lines):
        self.lines = lines[:]
        self.buffer_init()
        self.Refresh()

    def event_init(self):
        self.Bind(wx.EVT_LEFT_DOWN, self.left_down)
        self.Bind(wx.EVT_LEFT_UP, self.left_up)
        self.Bind(wx.EVT_MOTION, self.move)
        self.Bind(wx.EVT_SIZE, self.size)
        self.Bind(wx.EVT_IDLE, self.idle)
        self.Bind(wx.EVT_PAINT, self.paint)

    def left_down(self, event):
        self.cur_lines = []

        self.pos = event.GetPositionTuple()
        self.CaptureMouse()

    def left_up(self, event):
        if self.HasCapture():  # 该窗口有捕获到鼠标
            self.lines.append((self.color,
                               self.thickness,
                               self.cur_lines))
            self.cur_lines = []
            self.ReleaseMouse()

    def move(self, event):
        if event.Dragging() and event.LeftIsDown():
            dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
            self.draw(dc, event)
        event.Skip()

    def draw(self, dc, event):
        dc.SetPen(self.pen)
        new_pos = event.GetPositionTuple()
        coords = self.pos + new_pos
        self.cur_lines.append(coords)
        dc.DrawLine(*coords)
        self.pos = new_pos

    def size(self, event):
        self.buffer_reinit_flag = True

    def idle(self, event):
        if self.buffer_reinit_flag:
            self.buffer_init()
            self.Refresh(False)

    def paint(self, event):
        dc = wx.BufferedPaintDC(self, self.buffer)


class ControlPanel(wx.Panel):
    def __init__(self, parent, paint):
        super(ControlPanel, self).__init__(parent, -1, style = wx.RAISED_BORDER)

        self.max_thickness = 16
        self.color_list = ('Black', 'Yellow', 'Red', 'Green', 'Blue', 'Purple',
                           'Brown', 'Aquamarine', 'Forest Green', 'Light Blue',
                           'Goldenrod', 'Cyan', 'Orange', 'Navy', 'Dark Grey',
                           'Light Grey')

        self.paint = paint
        self.parent = parent
        self.bt_size = (22, 22)

        self.window_init()
        self.event_init()

    def window_init(self):
        self.vbox = wx.BoxSizer(wx.VERTICAL)  # 使用垂直的box szier放置grid sizer

        self.color_grid_create()  # 创建颜色grid sizer
        self.thickness_grid_create()  # 创建线条grid sizer

        self.vbox.Add(self.color_grid, 0, wx.ALL, 4)  # 参数0表示在垂直方向伸展时不改变尺寸
        self.vbox.Add(self.thickness_grid, 0, wx.ALL, 4)
        self.SetSizer(self.vbox)
        self.vbox.Fit(self)

    def event_init(self):
        self.Bind(wx.EVT_MOTION, self.move)

    def move(self, event):
        event.Skip()

    def color_grid_create(self):
        self.color_map = {}
        self.color_button = {}
        self.color_grid = wx.GridSizer(cols = 4, hgap = 2, vgap = 2)
        for each_color in self.color_list:
            bmp = self.bit_map_make(each_color)
            bt = wx.lib.buttons.GenBitmapToggleButton(self, -1, bmp, size = self.bt_size)
            bt.SetBezelWidth(1)
            bt.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.__color_set, bt)
            self.color_grid.Add(bt, 0)
            self.color_map[bt.GetId()] = each_color
            self.color_button[each_color] = bt

        self.color_set(self.color_list[0])

    def bit_map_make(self, color):
        bmp = wx.EmptyBitmap(16, 15)
        dc = wx.MemoryDC(bmp)
        dc.SetBackground(wx.Brush(color))
        dc.Clear()
        dc.SelectObject(wx.NullBitmap)
        return bmp

    def thickness_grid_create(self):
        self.thickness_map = {}
        self.thickness_button = {}
        self.thickness_grid = wx.GridSizer(cols = 4, hgap = 2, vgap = 2)
        for x in range(1, self.max_thickness + 1):
            bt = wx.lib.buttons.GenToggleButton(self, -1, str(x), size = self.bt_size)
            bt.SetBezelWidth(1)
            bt.SetUseFocusIndicator(False)
            self.Bind(wx.EVT_BUTTON, self.__thickness_set, bt)
            self.thickness_grid.Add(bt, 0)
            self.thickness_map[bt.GetId()] = x
            self.thickness_button[x] = bt

        self.thickness_set(1)

    def __color_set(self, event):
        self.color_set(self.color_map[event.GetId()])

    def color_set(self, color):
        if color == self.paint.color:
            return

        if self.color_button.has_key(self.paint.color):
            self.color_button[self.paint.color].SetToggle(False)  # 设置按钮为弹起状态

        if self.color_button.has_key(color):
            self.color_button[color].SetToggle(True)  # 设置按钮为按下状态

        self.paint.color_set(color)

    def __thickness_set(self, event):
        self.thickness_set(self.thickness_map[event.GetId()])

    def thickness_set(self, thickness):
        if thickness != self.paint.thickness:
            self.thickness_button[self.paint.thickness].SetToggle(False)
        self.thickness_button[thickness].SetToggle(True)
        self.paint.thickness_set(thickness)


class DrawWindow(wx.Frame):
    def __init__(self, parent, title):
        super(DrawWindow, self).__init__(parent, -1, title = title, size = (800, 600))

        self.title = title
        self.file_name = ''
        self.paint = PaintWindow(self)  # 创建画图面板

        self.window_init()
        self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        self.menu_bar_init()
        self.status_bar_init()
        self.panel_init()
        self.tool_bar_init()

    def menu_bar_init(self):
        self.menu = [
            (unicode('&文件', 'utf-8'), (  # 一级菜单项
                (unicode('&新建\tAlt+N', 'utf-8'), "New paint file", wx.ITEM_NORMAL, self.new),  # 二级菜单项
                (unicode('&打开\tAlt+O', 'utf-8'), "Open paint file", wx.ITEM_NORMAL, self.open),
                (unicode('&保存\tCtrl+S', 'utf-8'), "Save paint file", wx.ITEM_NORMAL, self.save),
                (unicode('&另存为...', 'utf-8'), "Save paint file", wx.ITEM_NORMAL, self.save_as),
                ("", "", ""),  # 分隔线
                (unicode('&颜色', 'utf-8'), (
                    ("&Black", "black", wx.ITEM_RADIO, self.color_select),  # 三级菜单项，单选
                    ("&Red", "red", wx.ITEM_RADIO, self.color_select),
                    ("&Green", "green", wx.ITEM_RADIO, self.color_select),
                    ("&Blue", "blue", wx.ITEM_RADIO, self.color_select),
                    ("&Other", "other", wx.ITEM_RADIO, self.other_color_select))),
                ("", "", ""),
                (unicode('&退出', 'utf-8'), "Quit", wx.ITEM_NORMAL, self.quit))),
            (unicode('&视图', 'utf-8'), (
                (unicode('&工具栏', 'utf-8'),
                 "show or hide the tool_bar",
                 wx.ITEM_CHECK,
                 self.tool_show_hide),
                (unicode('&状态栏', 'utf-8'),
                 "show or hide the menu_stat",
                 wx.ITEM_CHECK,
                 self.status_show_hide)
            )),
            (unicode('&帮助', 'utf-8'), (
                (unicode('&关于', 'utf-8'), "About this soft", wx.ITEM_NORMAL, self.about),
            ))
        ]

        self.menu_bar = wx.MenuBar()
        for each_menu in self.menu:
            self.menu_bar.Append(self.menu_create(each_menu[1]), each_menu[0])
        self.SetMenuBar(self.menu_bar)

    def menu_create(self, menu):
        top_menu = wx.Menu()  # 一级菜单

        # print menu

        for each_menu in menu:
            if len(each_menu) == 2:  # 三级菜单
                sub_menu = self.menu_create(each_menu[1])
                top_menu.AppendMenu(wx.NewId(), each_menu[0], sub_menu)
            else:  # 二级菜单
                if each_menu[0]:
                    menu = top_menu.Append(wx.NewId(), each_menu[0], each_menu[1], kind = each_menu[2])
                    self.Bind(wx.EVT_MENU, each_menu[3], menu)

                    if each_menu[2] == wx.ITEM_CHECK:
                        menu.Check(True)
                        #top_menu.Check(menu.GetId(), True)
                else:
                    top_menu.AppendSeparator()

        return top_menu

    def tool_bar_init(self):
        self.tool_bar = self.CreateToolBar()
        self.tool_new = self.tool_bar.AddSimpleTool(wx.NewId(),
                                                    # wx.Bitmap("1.png"),
                                                    #wx.Image('1.png', wx.BITMAP_TYPE_PNG).ConvertToBitmap(),
                                                    self.panel.bit_map_make('Red'),
                                                    'new',
                                                    'New paint file')

        self.tool_open = self.tool_bar.AddSimpleTool(wx.NewId(),
                                                     self.panel.bit_map_make('Blue'),
                                                     'open',
                                                     'Open paint file')

        self.tool_save = self.tool_bar.AddSimpleTool(wx.NewId(),
                                                     self.panel.bit_map_make('Yellow'),
                                                     'save',
                                                     'Save paint file')

        self.tool_bar.AddSeparator()

        # 添加工具栏到窗体
        self.tool_bar.Realize()

        self.tool_bar.EnableTool(self.tool_new.GetId(), False)

    def status_bar_init(self):
        self.status_bar = self.CreateStatusBar()
        self.status_bar.SetFieldsCount(4)
        self.status_bar.SetStatusWidths([-3, -2, -2, -1])

        self.status_bar.SetStatusText(unicode('鼠标位置: 0,0', 'utf-8'), 1)
        self.status_bar.SetStatusText(unicode('当前线条长度: 0', 'utf-8'), 2)
        self.status_bar.SetStatusText(unicode('线条数目: 0', 'utf-8'), 3)

    def panel_init(self):
        self.panel = ControlPanel(self, self.paint)  # 创建画笔选择框
        self.vbox = wx.BoxSizer(wx.HORIZONTAL)  # 放置水平的box sizer
        self.vbox.Add(self.panel, 0, wx.EXPAND)  # 水平方向伸展时不改变尺寸
        self.vbox.Add(self.paint, 1, wx.EXPAND)
        self.SetSizer(self.vbox)

        #self.vbox.Hide(self.panel)

    def event_init(self):
        self.Bind(wx.EVT_CLOSE, self.quit)
        self.paint.Bind(wx.EVT_MOTION, self.move)
        self.panel.Bind(wx.EVT_MOTION, self.move)

        self.Bind(wx.EVT_TOOL, self.new, self.tool_new)
        self.Bind(wx.EVT_TOOL, self.open, self.tool_open)
        self.Bind(wx.EVT_TOOL, self.save, self.tool_save)

    def move(self, event):
        self.status_bar.SetStatusText(unicode('鼠标位置: ', 'utf-8') + str(event.GetPositionTuple()), 1)
        self.status_bar.SetStatusText(unicode('当前线条长度: %s' % len(self.paint.cur_lines), 'utf-8'), 2)
        self.status_bar.SetStatusText(unicode('线条数目: %s' % len(self.paint.lines), 'utf-8'), 3)

        event.Skip()

    def new(self, event):
        pass

        '''
        wx.ColourDialog
        wx.DirDialog
        wx.MultiChoiceDialog
        wx.SingleChoiceDialog
        wx.TextEntryDialog
        wx.PasswordEntryDialog
        wx.NumberEntryDialog
        wx.FontDialog
        wx.MessageDialog
        wx.GenericProgressDialog
        wx.ProgressDialog
        wx.FindReplaceDialog
        '''

    def open(self, event):
        # 文件类型说明|文件格式|文件类型说明|文件格式...
        file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"
        dlg = wx.FileDialog(self, "Open paint file...",
                            os.getcwd(),
                            style = wx.OPEN,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            self.file_name = dlg.GetPath()
            self.file_read()
            self.SetTitle(self.title + ' ' + self.file_name)
        dlg.Destroy()

    def save(self, event):
        if not self.file_name:
            self.save_as(event)
        else:
            self.file_save()

    def save_as(self, event):
        file_wildcard = "Paint files(*.paint)|*.paint|All files(*.*)|*.*"
        dlg = wx.FileDialog(self,
                            "Save paint as ...",
                            os.getcwd(),
                            style = wx.SAVE | wx.OVERWRITE_PROMPT,
                            wildcard = file_wildcard)
        if dlg.ShowModal() == wx.ID_OK:
            if not os.path.splitext(dlg.GetPath())[1]:  # 如果没有文件名后缀
                self.file_name = dlg.GetPath() + '.paint'
            else:
                self.file_name = dlg.GetPath()

            self.file_save()
            self.SetTitle(self.title + ' ' + self.file_name)
        dlg.Destroy()

    def quit(self, event):
        self.Destroy()

    def tool_show_hide(self, event):
        if self.FindItemInMenuBar(event.GetId()).IsChecked():
            self.tool_bar.Show()
            print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' show'
        else:
            self.tool_bar.Hide()
            print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' hide'

        self.Refresh()

    def status_show_hide(self, event):
        print type(self.FindItemInMenuBar(event.GetId()))
        if self.FindItemInMenuBar(event.GetId()).IsChecked():
            self.status_bar.Show()
            print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' show'
        else:
            self.status_bar.Hide()
            print self.FindItemInMenuBar(event.GetId()).GetItemLabelText() + ' hide'

        self.Refresh()

    def about(self, event):
        description = '''wxpython实现的简单画图程序'''.decode('utf-8')

        licence = """File Hunter is free software; you can redistribute
                it and/or modify it under the terms of the GNU General Public License as
                published by the Free Software Foundation"""

        info = wx.AboutDialogInfo()
        # info.SetIcon(wx.Icon('iboxpay.png', wx.BITMAP_TYPE_PNG))
        info.SetVersion('2.0')
        info.SetDescription(description)
        info.SetCopyright('(C) 2007 - 2016 liujie@iboxpay.com')
        info.SetWebSite('http://www.iboxpay.com/')
        info.SetLicence(licence)
        info.AddDeveloper('liujie@iboxpay.com')
        info.AddDocWriter('liujie@iboxpay.com')
        info.AddArtist('liujie@iboxpay.com')
        info.AddTranslator('liujie@iboxpay.com')

        wx.AboutBox(info)

    def color_select(self, event):
        self.panel.color_set(self.menu_bar.FindItemById(event.GetId()).GetLabel())

    def other_color_select(self, event):
        dlg = wx.ColourDialog(self)  # 创建颜色对话框
        dlg.GetColourData().SetChooseFull(True)  # 创建颜色对象数据
        if dlg.ShowModal() == wx.ID_OK:
            self.panel.color_set(dlg.GetColourData().GetColour())
        dlg.Destroy()

    def file_read(self):
        if not self.file_name:
            return

        try:
            with open(self.file_name, 'r') as fp:
                self.paint.lines_set(cPickle.load(fp))
        except Exception as e:
            wx.MessageBox('%s is not a paint file(%s)' % (self.file_name, str(e)),
                          unicode('警告', 'utf-8'),
                          style = wx.OK | wx.ICON_EXCLAMATION)

    def file_save(self):
        if not self.file_name:
            return

        with open(self.file_name, 'w') as fp:
            cPickle.dump(self.paint.lines_get(), fp)


if __name__ == '__main__':
    app = wx.PySimpleApp()
    DrawWindow(None, unicode('画图', 'utf-8'))
    app.MainLoop()
