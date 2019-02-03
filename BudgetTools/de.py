# -*- coding: utf-8 -*-
class dataEntity(object):
    def __init__(self, date, month, place, summ, source, target):
        self.date = date
        self.month = month
        self.place = place
        self.summ = summ
        self.source = source
        self.target = target
    def __str__(self):
        return "{0},{1},{2},{3},{4},{5}".format(self.date, self.month, self.summ, self.source, self.target, self.place.encode('utf-8'))