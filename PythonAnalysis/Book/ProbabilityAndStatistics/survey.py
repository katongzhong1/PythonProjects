# coding=utf-8
from __future__ import print_function

"""This file contains code for use with "Think Stats",
by Allen B. Downey, available from greenteapress.com

Copyright 2010 Allen B. Downey
License: GNU GPLv3 http://www.gnu.org/licenses/gpl.html
"""



import sys
import gzip
import os
import thinkstats
import math
import matplotlib.pyplot as pyplot
import pmf


class Record(object):
    """Represents a record."""

# 被调查者
class Respondent(Record):
    """Represents a respondent."""

# 怀孕
class Pregnancy(Record):
    """Represents a pregnancy."""


class Table(object):
    """Represents a table as a list of objects"""

    def __init__(self):
        self.records = []

    def __len__(self):
        return len(self.records)

    def ReadFile(self, data_dir, filename, fields, constructor, n=None):
        """Reads a compressed data file builds one object per record.

        Args:
            data_dir: string directory name
            filename: string name of the file to read

            fields: sequence of (name, start, end, case) tuples specifying
            the fields to extract

            constructor: what kind of object to create
        """
        filename = os.path.join(data_dir, filename)

        if filename.endswith('gz'):
            fp = gzip.open(filename)
        else:
            fp = open(filename)

        for i, line in enumerate(fp):
            if i == n:
                break
            record = self.MakeRecord(line, fields, constructor)
            self.AddRecord(record)
        fp.close()

    @staticmethod
    def MakeRecord(line, fields, constructor):
        """Scans a line and returns an object with the appropriate fields.

        Args:
            line: string line from a data file

            fields: sequence of (name, start, end, cast) tuples specifying
            the fields to extract

            constructor: callable that makes an object for the record.

        Returns:
            Record with appropriate fields.
        """
        obj = constructor()
        for (field, start, end, cast) in fields:
            try:
                s = line[start - 1:end]
                val = cast(s)
            except ValueError:
                # If you are using Visual Studio, you might see an
                # "error" at this point, but it is not really an error;
                # I am just using try...except to handle not-available (NA)
                # data.  You should be able to tell Visual Studio to
                # ignore this non-error.
                val = 'NA'
            setattr(obj, field, val)
        return obj

    def AddRecord(self, record):
        """Adds a record to this table.

        Args:
            record: an object of one of the record types.
        """
        self.records.append(record)

    def ExtendRecords(self, records):
        """Adds records to this table.

        Args:
            records: a sequence of record object
        """
        self.records.extend(records)

    def Recode(self):
        """Child classes can override this to recode values."""
        pass


class Respondents(Table):
    """Represents the respondent table."""

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, self.GetFields(), Respondent, n)
        self.Recode()

    def GetFilename(self):
        return '2002FemResp.dat.gz'

    def GetFields(self):
        """Returns a tuple specifying the fields to extract.

        The elements of the tuple are field, start, end, case.

                field is the name of the variable
                start and end are the indices as specified in the NSFG docs
                cast is a callable that converts the result to int, float, etc.
        """
        return [
            ('caseid', 1, 12, int),
        ]


class Pregnancies(Table):
    """Contains survey data about a Pregnancy."""

    def ReadRecords(self, data_dir='.', n=None):
        filename = self.GetFilename()
        self.ReadFile(data_dir, filename, self.GetFields(), Pregnancy, n)
        self.Recode()

    def GetFilename(self):
        return '2002FemPreg.dat.gz'

    def GetFields(self):
        """Gets information about the fields to extract from the survey data.

        Documentation of the fields for Cycle 6 is at
        http://nsfg.icpsr.umich.edu/cocoon/WebDocs/NSFG/public/index.htm

        Returns:
            sequence of (name, start, end, type) tuples
        """
        return [
            ('caseid', 1, 12, int),         # 被调查者的 ID
            ('nbrnaliv', 22, 22, int),
            ('babysex', 56, 56, int),
            ('birthwgt_lb', 57, 58, int),
            ('birthwgt_oz', 59, 60, int),
            ('prglength', 275, 276, int),   # 怀孕周期
            ('outcome', 277, 277, int),     # 怀孕结果, 1代表活产
            ('birthord', 278, 279, int),    # 正常出生的婴儿的顺序, 如果没有出生, 则该字段为空
            ('agepreg', 284, 287, int),     #
            ('finalwgt', 423, 440, float),  # 被调查者的统计权重
        ]

    def Recode(self):
        for rec in self.records:

            # divide mother's age by 100
            try:
                if rec.agepreg != 'NA':
                    rec.agepreg /= 100.0
            except AttributeError:
                pass

            # convert weight at birth from lbs/oz to total ounces
            # note: there are some very low birthweights
            # that are almost certainly errors, but for now I am not
            # filtering
            try:
                if (rec.birthwgt_lb != 'NA' and rec.birthwgt_lb < 20 and
                            rec.birthwgt_oz != 'NA' and rec.birthwgt_oz <= 16):
                    rec.totalwgt_oz = rec.birthwgt_lb * 16 + rec.birthwgt_oz
                else:
                    rec.totalwgt_oz = 'NA'
            except AttributeError:
                pass


def main(name, data_dir='.'):
    resp = Respondents()
    resp.ReadRecords(data_dir)
    print('Number of respondents', len(resp.records))

    """习题一: 查询怀孕记录"""
    preg = Pregnancies()
    preg.ReadRecords(data_dir)
    print('习题一: 怀孕记录', len(preg.records))

    """习题二: 计算活婴量"""
    count = 0
    for record in preg.records:
        if record.outcome == 1:
            count += 1
    print('习题二: 计算活婴量', count)

    """习题三: 将活婴分为两组"""
    firArr = Pregnancies()
    secArr = Pregnancies()
    for record in preg.records:
        if record.outcome == 1:
            if record.birthord == 1:
                firArr.AddRecord(record)
            else :
                secArr.AddRecord(record)
    print('习题三:')
    print('活婴为第一胎的数量为', len(firArr.records))
    print('活婴不为第一胎的数量', len(secArr.records))

    """习题四: 分别计算第一胎和其他的平均怀孕周期"""
    firPreg = 0
    for record in firArr.records:
        firPreg += record.prglength
    averFirPreg = firPreg * 1.0 / len(firArr.records)
    print('习题四: ')
    print('第一胎的平均怀孕周期', averFirPreg)

    secPreg = 0
    for record in secArr.records:
        secPreg += record.prglength
    averSecPreg = secPreg * 1.0 / len(secArr.records)
    print('其他胎的平均怀孕周期', averSecPreg)

    """习题2-2-1: 计算标准差"""
    (lf, rf) = Prekin([rec.prglength for rec in firArr.records],
                      [rec.prglength for rec in secArr.records])
    print('习题2-2-1: 计算标准差')
    print('第一胎的怀孕周期的标准差', math.sqrt(lf[1]))
    print('其他胎的怀孕周期的标准差', math.sqrt(rf[1]))

    PyplotPre([rec.prglength for rec in firArr.records],
              [rec.prglength for rec in secArr.records])


def Prekin(lf, rf):
    return thinkstats.MeanVar(lf), thinkstats.MeanVar(rf)

def PyplotPre(lf, rf):
    Render(lf)
    Render(rf)
    pyplot.show()

def Render(list):
    hist = pmf.MakeHistFromList(list)
    vals, freqs = hist.Render()
    pyplot.bar(vals, freqs)

if __name__ == '__main__':
    main(*sys.argv)