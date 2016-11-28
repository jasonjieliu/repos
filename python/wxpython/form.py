#!/usr/bin/python
# coding:utf-8

import wx
import os
import sys
import wx.grid


class FormWindow(wx.Frame):
    def __init__(self, parent, title):
        '''
        wx.DEFAULT_FRAME_STYLE   : 这是每个窗口的缺省风格，包含标题、可调节大小的边框，最大最小化按钮、关闭按钮和系统菜单。
        wx.CAPTION               : 在框架上增加一个标题栏，它显示该框架的标题属性。
        wx.CLOSE_BOX             : 指示系统在框架的标题栏上显示一个关闭框，使用系统默认的位置和样式。
        Wx.FRAME_ON_TOP          : 置顶窗口。
        wx.FRAME_SHAP ED         : 用这个样式创建的框架可以使用SetShape()方法去创建一个非矩形的窗口。
        wx.FRAME_TOOL_WINDOW     : 通过给框架一个比正常更小的标题栏，使框架看起来像一个工具框窗口。在Windows下，使用这个样式创建的框架不会出现在显示所有打开窗口的任务栏上。
        wx.MAXIMIZE_BOX          : 指示系统在框架的标题栏上显示一个最大化框，使用系统默认的位置和样式。
        wx.MINIMIZE_BOX          : 指示系统在框架的标题栏上显示一个最小化框，使用系统默认的位置和样式。
        wx.RESIZE_BORDER         : 给框架增加一个可以改变尺寸的边框。
        wx.SIMPLE_BORDER         : 没有装饰的边框。不能工作在所有平台上。
        wx.SYSTEM_MENU           : 增加系统菜单（带有关闭、移动、改变尺寸等功能）和关闭框到这个窗口。在系统菜单中的改变尺寸和关闭功能的有效性依赖于wx.MAXIMIZE_BOX, wx.MINIMIZE_BOX和wx.CLOSE_BOX样式是否被应用。
        wx.FRAME_EX_META         : 如果时在 MacOS 中，这个属性用于是否显示“金属风格”
        wx.FRAME_EX_CONTEXTHELP  : 是否有联机帮助按钮。
        wx.FRAME_FLOAT_ON_PARENT : 窗口是否显示在最上层，与 wx.STAY_ON_TOP 不同，它必须有一个父窗口。
        '''
        super(FormWindow, self).__init__(parent = parent,
                                         title = title,
                                         size = (350, 250),
                                         style = wx.MINIMIZE_BOX | wx.SYSTEM_MENU | wx.CAPTION | wx.CLOSE_BOX,
                                         name = os.path.basename(sys.argv[0]).split('.')[0])

        self.window_init()
        self.event_init()
        self.Centre()
        self.Show()

    def window_init(self):
        '''
        wx.VERTICAL  : 垂直方向
        wx.HORIZONTAL: 水平方向
        '''
        self.vbox = wx.BoxSizer(wx.VERTICAL)

        self.form_init()

        self.vbox.Add((-1, 10))
        self.vbox.Add(self.box_form,
                      flag = wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP,
                      border = 5,
                      proportion = 1)

        self.SetSizer(self.vbox)

    def form_init(self):
        self.box_form = wx.BoxSizer(wx.VERTICAL)

        grid_data = [
            "liu 20 157171169890 shenzhen".split(),
            "li 30 11111122222 guangdong ".split(),
            "zhang 25 33333344444 huizhou".split(),
            "wang 33 55555566666 shaoguan".split(),
        ]

        self.grid = wx.grid.Grid(self, size = (4, 4))
        self.grid.CreateGrid(5, 4)

        self.grid.SetLabelBackgroundColour('White')
        self.grid.SetCellHighlightColour('Blue')
        self.grid.SetGridLineColour('Red')

        for row in range(4):
            self.grid.SetRowSize(row, 20)  # 设置行高度
            self.grid.SetRowLabelValue(row, unicode('第%d行', 'utf-8') % (row))
            for col in range(4):
                self.grid.SetColSize(col, 80)  # 设置列宽度
                self.grid.SetColLabelValue(col, unicode('第%d列', 'utf-8') % (col))
                self.grid.SetCellValue(row, col, grid_data[row][col])
                self.grid.SetReadOnly(row, col)
                self.grid.SetCellTextColour(row, col, 'Red')  # 设置文本颜色
                self.grid.SetCellBackgroundColour(row, col, 'Green')  # 设置背景颜色
                self.grid.SetCellAlignment(row, col, 5, 5)

                # print self.grid.GetCellValue(row, col)
                # print self.grid.GetRowLabelValue(row)

        '''
        0:默认选中一格
        1:默认选中一行
        2:默认选中一列
        '''
        self.grid.SetSelectionMode(0)

        self.grid.HideCol(0)

        self.grid.SelectRow(1) # 初始化选中第一行
        print self.grid.GetSelectedRows() # 获取当前选中行
        self.grid.SelectCol(1) # 初始化选中第一列
        self.grid.ClearSelection() # 清除选中

        self.grid.AppendRows(1)  # 末尾新增一行
        self.grid.AppendCols(1)  # 末尾新增一列
        self.grid.InsertRows(2, 1)  # 第二行后新增一行

        self.box_form.Add(self.grid, flag = wx.EXPAND, proportion = 1)

    def event_init(self):
        '''
        wx.grid.EVT_GRID_CELL_CHANGE：       当用户通过编辑器改变单元格中的数据时触发该事件。
        wx.grid.EVT_GRID_CELL_LEFT_CLICK：   当用户在一个单元格中敲击鼠标左键时触发该事件。
        wx.grid.EVT_GRID_CELL_LEFT_DCLICK：  当用户在一个单元格中双击鼠标左键时触发该事件。
        wx.grid.EVT_GRID_CELL_RIGHT_CLICK：  当用户在一个单元格中敲击鼠标右键时触发该事件。
        wx.grid.EVT_GRID_CELL_RIGHT_DCLICK： 当用户在一个单元格中双击鼠标右键时触发该事件。
        wx.grid.EVT_GRID_EDITOR_HIDDEN：     当在编辑会话结束时隐藏一个单元格编辑器则触发该事件。
        wx.grid.EVT_GRID_EDITOR_SHOWN：      当在编辑会话结束时显示一个单元格编辑器则触发该事件。
        wx.grid.EVT_GRID_LABEL_LEFT_CLICK：  当用户在行或列的标签区域敲击鼠标左键时触发该事件。
        wx.grid.EVT_GRID_LABEL_LEFT_DCLICK： 当用户在行或列的标签区域双击鼠标左键时触发该事件。
        wx.grid.EVT_GRID_LABEL_RIGHT_CLICK： 当用户在行或列的标签区域敲击鼠标右键时触发该事件。
        wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK：当用户在行或列的标签区域双击鼠标右键时触发该事件。
        wx.grid.EVT_GRID_SELECT_CELL：       当用户将焦点移到一个新的单元格，并选择它时触发该事件。
        '''
        self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.grid_event)
        self.grid.Bind(wx.grid.EVT_GRID_SELECT_CELL, self.grid_event)

    def grid_event(self, event):
        #print event.GetId(), event.EventType
        if wx.grid.EVT_GRID_CELL_CHANGE.typeId == event.EventType:
            self.event_info(event, 'cell change')
        elif wx.grid.EVT_GRID_CELL_LEFT_CLICK.typeId == event.EventType:
            self.event_info(event, 'left down')
        elif wx.grid.EVT_GRID_CELL_LEFT_DCLICK.typeId == event.EventType:
            self.event_info(event, 'left double down')
        elif wx.grid.EVT_GRID_CELL_RIGHT_CLICK.typeId == event.EventType:
            self.event_info(event, 'right down')
        elif wx.grid.EVT_GRID_CELL_RIGHT_DCLICK.typeId == event.EventType:
            self.event_info(event, 'right double down')
        elif wx.grid.EVT_GRID_EDITOR_HIDDEN.typeId == event.EventType:
            self.event_info(event, 'hide')
        elif wx.grid.EVT_GRID_EDITOR_SHOWN.typeId == event.EventType:
            self.event_info(event, 'show')
        elif wx.grid.EVT_GRID_LABEL_LEFT_CLICK.typeId == event.EventType:
            self.event_info(event, 'lable left down')
        elif wx.grid.EVT_GRID_LABEL_LEFT_DCLICK.typeId == event.EventType:
            self.event_info(event, 'lable left double down')
        elif wx.grid.EVT_GRID_LABEL_RIGHT_CLICK.typeId == event.EventType:
            self.event_info(event, 'lable right down')
        elif wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK.typeId == event.EventType:
            self.event_info(event, 'lable right double down')
        elif wx.grid.EVT_GRID_SELECT_CELL.typeId == event.EventType:
            self.event_info(event, 'new cell')
        event.Skip()

    def event_info(self, event, msg):
        print event.GetRow(), event.GetCol(), self.grid.GetNumberRows(), self.grid.GetNumberCols()
        print self.grid.GetSelectedCells(), self.grid.GetSelectedRows(), self.grid.GetSelectedCols()
        #print self.grid.GetCellValue(event.GetRow(), event.GetCol()), msg

        # event.AltDown()
        # event.ControlDown()
        # event.GetCol()
        # event.GetPosition()
        # event.GetRow()
        # event.MetaDown()
        # event.Selecting()
        # event.ShiftDown()

if __name__ == '__main__':
    app = wx.App()
    FormWindow(None, title = 'form')
    app.MainLoop()
