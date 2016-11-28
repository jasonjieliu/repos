#!/usr/bin/python
# coding:utf-8

import wx
import os
import sys
import wx.grid

class ListWindow(wx.Frame):
    def __init__(self, parent, title):
        super(ListWindow, self).__init__(parent = parent,
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
            self.grid.SetRowSize(row, 20)
            self.grid.SetRowLabelValue(row, unicode('第%d行', 'utf-8') % (row + 1))
            for col in range(4):
                self.grid.SetColSize(col, 50)
                self.grid.SetColLabelValue(col, unicode('第%d列', 'utf-8') % (col + 1))
                self.grid.SetCellValue(row, col,
                                       grid_data[row][col])
                self.grid.SetCellTextColour(row, col, 'Red')
                self.grid.SetCellBackgroundColour(row, col, 'Green')

                # print self.grid.GetCellValue(row, col)
                # print self.grid.GetRowLabelValue(row)

        self.grid.AppendRows(1)
        self.grid.AppendCols(1)
        self.grid.InsertRows(2, 1)

        self.box_form.Add(self.grid, flag = wx.EXPAND, proportion = 1)

    def event_init(self):
        pass

if __name__ == '__main__':
    app = wx.App()
    ListWindow(None, title = 'form')
    app.MainLoop()
