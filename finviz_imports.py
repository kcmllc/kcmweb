#!/usr/bin/python
import urllib2
import mysql.connector
from csv import reader
cnx = mysql.connector.connect(host="68.169.60.221",user="root",passwd="702186263d7cda80856652cbe8a431d4",port=3306,database='financial_intel')
cursor = cnx.cursor()

def importoverview():
    response = urllib2.urlopen('http://finviz.com/export.ashx?v=111')
    data = response.readlines()[2:]
    cursor.execute('TRUNCATE TABLE finviz_overview')
    for line in reader(data):
        param = '%s ' * len(line)
        sqlparam = ','.join(param.split(' '))
        columns = sqlparam[:-1]
        print columns
        print line
        cursor.execute('INSERT INTO finviz_overview VALUES (' + columns + ')', line)
        #del linelength
    try:
        cnx.commit()
    except Exception, e:
        print enumerate
    else:
        cnx.close


def importvaluation():
    response = urllib2.urlopen('http://finviz.com/export.ashx?v=121')
    data = response.readlines()[2:]
    cursor.execute('TRUNCATE TABLE finviz_valuation')
    for line in reader(data):
        param = '%s ' * len(line)
        sqlparam = ','.join(param.split(' '))
        columns = sqlparam[:-1]
        print columns
        print line
        cursor.execute('INSERT INTO finviz_valuation VALUES (' + columns + ')', line)
        #del linelength
    try:
        cnx.commit()
    except Exception, e:
        print enumerate
    else:
        cnx.close


def importfinancial():
    response = urllib2.urlopen('http://finviz.com/export.ashx?v=161')
    data = response.readlines()[2:]
    cursor.execute('TRUNCATE TABLE finviz_financial')
    for line in reader(data):
        param = '%s ' * len(line)
        sqlparam = ','.join(param.split(' '))
        columns = sqlparam[:-1]
        print columns
        print line
        cursor.execute('INSERT INTO finviz_financial VALUES (' + columns + ')', line)
        #del linelength
    try:
        cnx.commit()
    except Exception, e:
        print enumerate
    else:
        cnx.close


def main():
    importoverview()
    importvaluation()
    importfinancial()

if __name__ == '__main__':
    main()

__author__ = 'kyle'
