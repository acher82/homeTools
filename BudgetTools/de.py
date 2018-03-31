# -*- coding: utf-8 -*-
class dataEntity(object):
    def __init__(self, date, place, summ, source):
        self.date = date
        self.place = place
        self.summ = summ
        self.source = source
    def __str__(self):
        return "{0},'{1}',{2},{3}".format(self.date, self.place.encode('utf-8'), self.summ, self.source)