#!/usr/bin/python
# coding:utf-8

import wx
import wx.grid


class GridTable(wx.grid.PyGridTableBase):
    def __init__(self, data = {}, rows = 10, cols = 10, max_rows = 50, max_cols = 50):
        # wx.grid.PyGridTableBase.__init__(self)
        super(GridTable, self).__init__()

        self.rows = rows
        self.cols = cols
        self.data = data

        self.max_rows = max_rows
        self.max_cols = max_cols

        self.odd = wx.grid.GridCellAttr()
        self.odd.SetOverflow(False)
        self.odd.SetBackgroundColour("sea green")
        self.odd.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

        self.even = wx.grid.GridCellAttr()
        self.odd.SetOverflow(False)
        self.even.SetBackgroundColour("green")
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
        if self.data.get((row, col)):
            return self.data.get((row, col))
        else:
            return ''

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr

    def AppendRows(self, rows = 1):
        print 111
        if (self.rows + rows) <= self.max_rows:
            self.rows += rows
            print self.rows
            return True
        else:
            return False

    def AppendCols(self, cols = 1):
        print 111
        if (self.cols + cols) <= self.max_cols:
            self.cols += cols
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
    def __init__(self, parent, title):
        super(SelfFrame, self).__init__(parent = parent,
                                        title = "Grid Table",
                                        size = (640, 480))

        self.data = {(1, 1): "Here",
                     (2, 2): "is",
                     (3, 3): "some",
                     (4, 4): "data",
                     }

        self.grid = wx.grid.Grid(self)
        self.grid.ClearGrid()

        self.table = GridTable(self.data)

        self.grid.SetTable(self.table, True)

        self.grid.BeginBatch()

        self.grid.AppendRows(5)

        self.grid.EndBatch()

        self.grid.ForceRefresh()

        self.grid.EnableEditing(True)
        print self.grid.IsReadOnly(1, 2)

        self.grid.SetColLabelAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER)

        print self.grid.GetCellValue(1, 1)

    def grid_event(self, evt):
        pass


if __name__ == '__main__':
    app = wx.App()
    frame = SelfFrame(None, title = unicode('表格', 'utf-8'))
    frame.Show()
    app.MainLoop()
