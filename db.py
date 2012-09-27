# -*- coding: utf-8 -*-
import numpy as np
import math as math
import matplotlib.pylab as plt
import kcorrect as KC
from kcorrect.sdss import SDSSKCorrect, SDSSPhotoZ, SDSS
from scipy import integrate
import matplotlib.cm as cm
import matplotlib.mlab as mlab
import sqlite3
import csv

class dbUtils:
	def makeArray(self,a):
	  print np.array(a[1:]).dtype
	  return np.array(a[1:])
	@staticmethod  
	def getValueCount(csvReader):
	  valueCount = 0
	  for row in csvReader:
	      if row[0].startswith('#'):
		continue
	      valueCount = len(row)
	      return valueCount
	   
	@staticmethod	  
	def createPlaceHolderString(valueCount):
	  print valueCount, 'valueCount'
	  placeHolderString = ''
	  for i in range(0, valueCount):
	    placeHolderString = placeHolderString + '?, '
	  placeHolderString = " values(" + placeHolderString[:-2] + ")"
	  return placeHolderString

	@staticmethod
	def deleteOldTable(c, tableName):
	  try:
	   	c.execute('drop table ' + tableName)
	  except sqlite3.OperationalError:
	  	pass
	  try:
	  	c.execute('drop view ' + tableName)		  
	  except sqlite3.OperationalError:
	  	pass	
	@staticmethod  
	def createDBFromFile(dbName, dataFile, schema):
	  conn = sqlite3.connect(dbName)
	  c = conn.cursor()
	  dbUtils.deleteOldTable(c, dbName)	
	  c.execute('create table ' + dbName + schema)
	#  print 'create table ' + dbName + schema
	  csvReader = csv.reader(open(dataFile), delimiter=',')
	  placeHolderString = dbUtils.createPlaceHolderString(dbUtils.getValueCount(csvReader))
	  #print 'insert into ' + dbName + schema + placeHolderString, row
	  for row in csvReader:
	     
	     if row[0].startswith('#'):
		continue
		print 'comment!'
	     #conn.execute('insert into ' + dbName + schema + valueString, row)
	     conn.execute('insert into ' + dbName + placeHolderString, row);
	  conn.commit()
	  
	@staticmethod  
	def createDBFromArray(dbName, data, schema):
	  conn = sqlite3.connect(dbName)
	  c = conn.cursor()
	  
	  dbUtils.deleteOldTable(c, dbName)
	  c.execute('create table ' + dbName + schema)
	  print 'len[data]', len(data)
	  #data = np.array(data)
	  #np.savetxt('data.csv', data)
	  placeHolderString = dbUtils.createPlaceHolderString(data.shape[1])
	  for i in range(0, data.shape[0]):
	    c.execute('insert into ' + dbName + placeHolderString, data[i, :])
	    print data[i, :], 'ith', i
	    #c.execute('insert into ' + dbName + placeHolderString, t)
	  conn.commit()
	
	@staticmethod
	def getFromDB(columns, table, view, *whereClause): 
	  print 'connected'
	  conn = sqlite3.connect(table)
	  
	  c = conn.cursor()
	  print 'about to select'
	  print 'select ' + columns + ' from ' + view + ''.join(whereClause) +' order by rowid asc'
	  c.execute('select ' + columns + ' from ' + view + ''.join(whereClause)+' order by rowid asc')
	  conn.commit()
	  return c.fetchall()
	'''
	@staticmethod
	def selectWithJoin(dbname, viewName, table1, table2, columns1, key,  *where):
	  conn = sqlite3.connect(table1, table2)
	  c = conn.cursor()
	  print 'create view '+dbname+'.'+viewName+' AS  select ' + table1 +'.'+key1+','+columns1+' from '+table1+' LEFT JOIN '+table2+' USING '+ key
	  conn.commit()
	'''
	
	@staticmethod
	def createViewbyIds(table, view, idColumn, columns, ids):
	  conn = sqlite3.connect(table)
	  c = conn.cursor()
	  dbUtils.deleteOldTable(c, view)
	  c.execute('create view ' + view + ' as select '+columns+' from '+table+' where '+idColumn+' in (%s)' % (", ".join(ids)), ())  
	  conn.commit()
	   
	@staticmethod
	def addColumn(table, column):
	  conn = sqlite3.connect(table)
	  c = conn.cursor()
	  c.execute('alter table '+ table+' add column '+column)
	  conn.commit()

	@staticmethod
	def updateColumn(table1, column1, table2, column2, id1, id2): #table1, column1 -- destination, table2, col2 -- source 
	  conn = sqlite3.connect(table1)
	  c = conn.cursor()
	  c.execute('attach '+table2+' as '+table2)
	  #morphId = dbUtils.getFromDB('califaid', 'morphData', 'morphData')
	  #c.execute('select califa_id from mothersample, morphData where morphData.califaid = mothersample.CALIFA_id')
	  #c.execute('select '+column2+' from '+ table1+', '+table2+' where '+table1+'.'+id1+' = '+table2+'.'+id2)
	  print 'select '+column2+' from '+ table2+', '+table1+' where '+table1+'.'+id1+' = '+table2+'.'+id2
	  #c.execute('update '+ table1+' set '+column1+' = (select '+column2+' from '+ table2+', '+table1+' where '+table1+'.'+id1+' = '+table2+'.'+id2+')')
	  #c.execute('select '+column2+' from '+ table2+', '+table1+' where '+table1+'.'+id1+' = '+table2+'.'+id2)
	  for i in range(0, 938):
	    #c.execute('insert into ' + dbName + placeHolderString, data[i, :])
	    print 'ith', i
	    #var = c.execute('select '+column2+' from '+ table2+', '+table1+' where '+table1+'.'+id1+' = '+table2+'.'+id2)
	    c.execute('select '+column2+' from '+ table2+', '+table1+' where '+table1+'.'+id1+' = '+str(i))
	    c.fetchall()
	    c.execute('update '+ table1+' set '+column1+' =  '+var)

	  conn.commit()
	  #return c.fetchall()
	  
	@staticmethod
	def createView(table, view, columns, *whereClause):
	  conn = sqlite3.connect(table)
	  c = conn.cursor()
	  dbUtils.deleteOldTable(c, view)
	  sql = 'create view ' + view + ' as (select '+ ''.join(columns) + ' from ' + table + ' where ' + ''.join(whereClause[0])+')'			
	  print sql 
	  c.execute(sql)
	  conn.commit()
	  
	@staticmethod
	def count(table, view, *args):
	  conn = sqlite3.connect(table)
	  c = conn.cursor()
	  print 'count (*) from ' + view + ''.join(args)
	  c.execute('select count (*) from ' + view + ''.join(args))
	  conn.commit()
	  return c.fetchall()
	
