#!/usr/bin/python
# coding:utf-8

import wx
import wx.grid

class CustomForm(wx.grid.PyGridTableBase):
    def __init__(self, data = {}, rows = 10, cols = 10):
        #wx.grid.PyGridTableBase.__init__(self)
        super(CustomForm, self).__init__()

        self.rows = rows
        self.cols = cols
        self.data = data

        self.max_rows = 50
        self.max_cols = 50

        self.odd = wx.grid.GridCellAttr()
        self.odd.SetBackgroundColour("sea green")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.even = wx.grid.GridCellAttr()
        self.even.SetBackgroundColour("Green")
        self.even.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

    def SetFont(self, font):
        self.odd.SetFont(font)
        self.even.SetFont(font)

    '''
    自定义表格需要覆盖以下函数
    初始化时内部set方法都会调用get方法, 因此此处的set方法是给外部调用的
    '''
    def GetNumberRows(self):
        return self.rows

    def GetNumberCols(self):
        return self.cols

    def IsEmptyCell(self, row, col):
        return self.data.get((row, col)) is not None

    def GetValue(self, row, col):
        value = self.data.get((row, col))
        if value:
            return value
        else:
            return ''

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr

    def AppendRows(self, numRows = 1):
        if (self.rows + numRows) <= self.max_rows:
            self.rows += numRows
            return True
        else:
            return False

    def AppendCols(self, numCols = 1):
        if (self.cols + numCols) <= self.max_cols:
            self.cols += numCols
            return True
        else:
            return False

    def GetRowLabelValue(self, row):  # 行标签
        return unicode('第%d行', 'utf-8') % (row + 1)

    def GetColLabelValue(self, col):  # 列标签
        '''
        ord(char) char -> int
        chr(int)  int -> char
        '''
        return unicode('第%s列', 'utf-8') % chr(col + 65)

    '''
        外部调用时生效
        '''
    def SetValue(self, row, col, value):
        self.data[(row, col)] = value


class SelfFrame(wx.Frame):
    def __init__(self):
        super(SelfFrame, self).__init__(None, title = "Grid Table", size = (640, 480))

        self.data = {(1, 1): "Here",
                     (2, 2): "is",
                     (3, 3): "some",
                     (4, 4): "data",
                     }

        self.grid = wx.grid.Grid(self)
        self.table = CustomForm(self.data)

        self.grid.SetTable(self.table, True)

        self.grid.BeginBatch()

        self.table.AppendRows(1)

        self.table.AppendCols(2)

        self.grid.EndBatch()

        self.grid.ForceRefresh()

        self.grid.EnableEditing(True)
        print self.grid.IsEditable()
        self.grid.SetReadOnly(1, 1, isReadOnly = True)
        print self.grid.IsReadOnly(3, 2)

        self.grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        print self.grid.GetCellValue(1,1)

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
        wx.grid.EVT_GRID_Select_CELL：       当用户将焦点移到一个新的单元格，并选择它时触发该事件。
        '''
        # self.grid.Bind(wx.grid.EVT_GRID_CELL_CHANGE, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_CLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_CLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_CELL_RIGHT_DCLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_EDITOR_HIDDEN, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_EDITOR_SHOWN, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_CLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_LABEL_LEFT_DCLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_CLICK, self.grid_event)
        # self.grid.Bind(wx.grid.EVT_GRID_LABEL_RIGHT_DCLICK, self.grid_event)
        #self.grid.Bind(wx.grid.EVT_GRID_Select_CELL, self.grid_event)

    def grid_event(self, evt):
        '''
        evt.AltDown()：        当事件被触发时，如果alt键被按下了，则返回True。
        evt.ControlDown()：    当事件被触发时，如果control键被按下了，则返回True。
        evt.GetCol()：         返回发生事件的单元格所在的列的索引。
        evt.GetPosition()：    返回返回一个wx.Point。它代表事件发生点的逻辑坐标（以像素为单位）。
        evt.GetRow()：         返回发生事件的单元格所在的行的索引。
        evt.MetaDown()：       当事件被触发时，如果met键被按下了，则返回True。
        evt.Selecting()：      如果事件是一个被选事件，则返回True，如果事件是取消选择事件，则返回False。
        evt.evt.ShiftDown()：  当事件被触发时，如果shift键被按下了，则返回True。
        '''
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = SelfFrame()
    frame.Show()
    app.MainLoop()

