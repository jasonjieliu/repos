#!/usr/bin/python
# coding:utf-8

__Author__ = 'Liu'

'''
根据年份生成tbl_stlm_date对应的insert语句
'''

import os
import sys
import random
import datetime
import calendar
import collections


class WorkerDay(object):
    def __init__(self, year, tx_seq, legal_holiday_range = {}, legal_workday_list = []):
        self.year = year
        self.tx_seq = tx_seq
        self.total_days = 0
        self.legal_holiday_range = legal_holiday_range
        self.total_day_list = []
        self.work_day_list = []
        self.legal_holiday_list = []
        self.legal_workday_list = legal_workday_list
        self.record_list = collections.OrderedDict()

        self.info_print()

        self.total_day_gen()

        self.legal_holiday_gen()

        self.work_day_gen()

        self.total_day_list.sort()
        self.work_day_list.sort()
        self.legal_holiday_list.sort()
        self.legal_workday_list.sort()

        '''
        对list中元素先按第二个子元素再按第一个子元素逆序排序方法
        list.sort(key = lambda x: (x[1], x[0]), reverse = True)
        list.sort(key = operator.itemgetter(1,0), reverse = True)
        list.sort(lambda x,y: cmp(x[1],y[1]), reverse = True)
        '''

        self.record_gen()

        self.sql_insert_gen()

    def info_print(self):
        if calendar.isleap(int(self.year)):
            print 'leap year'
            self.total_days = 366
        else:
            print 'nonleap year'
            self.total_days = 365

    def total_day_gen(self):
        first_datetime = datetime.datetime.strptime(self.year + '0101', '%Y%m%d')

        for i in range(self.total_days):
            next_datetime = first_datetime + datetime.timedelta(days = i)
            self.total_day_list.append(next_datetime.strftime('%Y%m%d'))

            if next_datetime.isoweekday() in [1, 2, 3, 4, 5]:
                self.work_day_list.append(next_datetime.strftime('%Y%m%d'))

    def legal_holiday_gen(self):
        for (begin, end) in self.legal_holiday_range.items():
            while True:
                self.legal_holiday_list.append(begin)
                begin_datetime = datetime.datetime.strptime(begin, '%Y%m%d')
                begin = (begin_datetime + datetime.timedelta(days = 1)).strftime('%Y%m%d')
                if begin == end:
                    self.legal_holiday_list.append(begin)
                    break

    def work_day_gen(self):
        [self.work_day_list.remove(day) for day in self.legal_holiday_list if day in self.work_day_list]
        [self.work_day_list.append(day) for day in self.legal_workday_list if day not in self.work_day_list]

    def clear_day_get(self, tx_day):
        stlm_date = None

        for day in self.work_day_list:
            if day > tx_day:
                stlm_date = day
                break

        if stlm_date:
            self.record_list[stlm_date]['trans_date'].append(tx_day)

    def record_gen(self):
        for stlm_date in self.work_day_list:
            self.record_list[stlm_date] = {}
            self.record_list[stlm_date]['trans_date'] = []

        map(self.clear_day_get, self.total_day_list)

        for (stlm_date, value) in self.record_list.items():
            self.record_list[stlm_date]['resv1'] = self.tx_seq
            self.tx_seq += 1

    def sql_insert_gen(self):
        profit_flag = None

        for (stlm_date, value) in self.record_list.items():
            for tx_day in value['trans_date']:
                if tx_day[-2:] == '01':
                    profit_date = stlm_date

                if tx_day == profit_date:
                    batch_flag = 1
                elif tx_day in self.record_list.keys():
                    batch_flag = 2
                else:
                    batch_flag = 3
                print '''insert tbl_stlm_date(trans_date, stlm_date, stlm_flag, batch_flag, resv1)
                    values('%s', '%s', 0, %d, %d);''' % (tx_day, stlm_date, batch_flag, value['resv1'])


if __name__ == '__main__':
    WorkerDay('2017',
              503,
              {
                  '20170101': '20170102',
                  '20170127': '20170202',
                  '20170402': '20170404',
                  '20170429': '20170501',
                  '20170528': '20170530',
                  '20171001': '20171008',
              },
              ['20170122', '20170204', '20170401', '20170527', '20170930'])