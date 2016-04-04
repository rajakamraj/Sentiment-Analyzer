#!/usr/bin/python

import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
##===============================================

class DatabaseUtility: 
	def __init__(self, database, tableName):
		self.db = database
		self.tableName = tableName

		
		p = 'Ssdi@2015';
		self.cnx = mysql.connector.connect(user = 'root',
									password = p,
									host = '127.0.0.1')
		self.cursor = self.cnx.cursor()
		
		self.ConnectToDatabase()
		if(tableName in 'reviewDetails'):
			self.createReviewTable()
		elif(tableName in 'masterTable'):
			self.CreateTable()
	
		
	def ConnectToDatabase(self):
		try:
			self.cnx.database = self.db
		except mysql.connector.Error as err:
			if err.errno == errorcode.ER_BAD_DB_ERROR:
				self.CreateDatabase()
				self.cnx.database = self.db
			else:
				print(err.msg)

	def CreateDatabase(self):
		try:
			self.RunCommand("CREATE DATABASE %s DEFAULT CHARACTER SET 'utf8';" %self.db)
		except mysql.connector.Error as err:
			print("Failed creating database: {}".format(err))

	def CreateTable(self):
		cmd = (" CREATE TABLE IF NOT EXISTS " + self.tableName + " ("
			" `ID` int(5) NOT NULL AUTO_INCREMENT,"
			" `username` char(50) NOT NULL,"
			" `password` char(50) NOT NULL,"
			" PRIMARY KEY (`ID`)"
			") ENGINE=InnoDB;")
		self.RunCommand(cmd)
	def createReviewTable(self):
		cmd=(" CREATE TABLE IF NOT EXISTS " + self.tableName + " ("
			" `ID` int(5) NOT NULL AUTO_INCREMENT,"
			" `bookname` VARCHAR (200) NOT NULL,"
			" `reviewername` VARCHAR (200) NOT NULL,"
			" `review` VARCHAR (1000) NOT NULL,"
			" `sentiment` VARCHAR (50) NOT NULL,"
			" PRIMARY KEY (`ID`)"
			") ENGINE=InnoDB;")
		self.RunCommand(cmd)
		
	def GetTable(self):
		self.CreateTable()
		return self.RunCommand("SELECT * FROM %s;" % self.tableName)
	
	def GetTableReview(self):
		return self.RunCommand("SELECT * FROM %s;" % self.tableName)
	
	def GetTableReviewCount(self):
		return self.RunCommand("SELECT sentiment,count(*) FROM %s group by sentiment;" % self.tableName)

	def GetColumns(self):
		return self.RunCommand("SHOW COLUMNS FROM %s;" % self.tableName)

	def RunCommand(self, cmd):
		print ("RUNNING COMMAND: " + cmd)
		try:
			self.cursor.execute(cmd)
		except mysql.connector.Error as err:
			print ('ERROR MESSAGE: ' + str(err.msg))
			print ('WITH ' + cmd)
		try:
			msg = self.cursor.fetchall()
		except:
			msg = self.cursor.fetchone()
		return msg

	def AddEntryToTable(self, username, password):
		self.createReviewTable()
		cmd = " INSERT INTO " + self.tableName + " (username, password)"
		cmd += " VALUES ('%s', '%s');" % (username, password)
		self.RunCommand(cmd)
		
	def AddEntryToTableReview(self, bookName, reviewerName,review,sentiment):
		tempBookName=bookName.replace("'","")
		tempReviewerName=reviewerName.replace("'","")
		tempReview=review.replace("'","")
		
		cmd = " INSERT INTO " + self.tableName + " (bookname, reviewername,review,sentiment)"
		cmd += " VALUES ('%s', '%s','%s', '%s');" % (tempBookName, tempReviewerName,tempReview,sentiment)
		self.RunCommand(cmd)
		self.RunCommand("commit;")

	def __del__(self):
		self.cnx.commit()
		self.cursor.close()
		self.cnx.close()

##===============================================
##===============================================


if __name__ == '__main__':
	db = 'UsernamePassword_DB'
	tableName = 'masterTable'

	dbu = DatabaseUtility(db, tableName)
	
# 	tableName='reviewDetails'
# 	
# 	dbu = DatabaseUtility(db, tableName)
	# dbu.AddEntryToTable ('asdf', 'asdf')
	# print (dbu.GetColumns())
	# print (dbu.GetTable())
	
