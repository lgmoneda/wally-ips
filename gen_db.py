from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time
import pandas as pd 
from datetime import timedelta
from random import randint
import numpy as np

### Corrigindo problemas de encoding
reload(sys)
sys.setdefaultencoding("utf-8")

mysql = MySQL()
app = Flask(__name__)

# MySQL 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '____'
app.config['MYSQL_DATABASE_DB'] = 'Wally'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

"""
CREATE TABLE Registros(
 registroId INT NOT NULL AUTO_INCREMENT,
 userId INT NOT NULL,
 date datetime NOT NULL,
 placeId INT NOT NULL,
 PRIMARY KEY(registroId)
 );
"""

def build_insert_registro(userId, date, placeId, registroId=""):
	msg = "insert into Registros values(0," \
										  + str(userId) + ",\"" \
										  + str(date) + "\"," \
										  + str(placeId) + ")"
	return msg

def test_sql_to_pandas(conn):
	tabela = pd.read_sql("select * from Registros;", conn)
	print(tabela)


def random_date(start, end, hour_mean=12):
	year = randint(start.year, end.year)
	month = randint(1, 12)
	day = randint(1, 30)
	hour = int(np.random.normal(loc=hour_mean, scale=4))
	minute = randint(0, 59)

	try:
		date_ = datetime(year=year,month=month,day=day,hour=hour, minute=minute)
	except:
		day = randint(1, 28)
		hour = randint(8, 21)
		date_ = datetime(year=year,month=month,day=day,hour=hour, minute=minute)
	return date_

def random_date2(start, end):
	while(True):
		new_date = start + timedelta(
	        seconds=randint(0, int((end - start).total_seconds())))
		if new_date.hour >= 8 and new_date.hour <= 21:
			break 
	print(new_date)
	return new_date

### Gerando dados para o grupo familia
def gen_data(startDate, endDate, placeIDs, n_registers, groupRange):

	for i in range(n_registers):
		userId = randint(groupRange[0], groupRange[1])
		place = placeIDs[randint(0, len(placeIDs) - 1)]
		
		date_ = random_date(startDate, endDate)
		conn = mysql.connect()
		cursor = conn.cursor()
		msg = build_insert_registro(userId, date_, place)
		print(msg)
		cursor.execute(msg)
		conn.commit()





if __name__ == "__main__":

	### Lista com os IDs de lojas para familias
	family_stores = [2, 11, 13, 18]
	family_range = (1, 10000)

	housewife_stores = [14, 8]
	housewife_range = (10000, 13000)

	young_stores = [5, 12]
	young_range = (13000, 20000)

	couple_stores = [11, 4, 6]
	couple_range = (20000, 23000)

	friends_stores = [2, 9]
	friends_range = (23000, 24000)

	bourgeois_stores = [1, 3, 4, 6]
	bourgeois_range = (24000, 25000)


	d = date(2016, 2, 11)
	t = time(14, 45)
	date_ = datetime.combine(d, t)
	print(date_)
	print(build_insert_registro(10, date_, 1))

	conn = mysql.connect()
	cursor = conn.cursor()
	#cursor.execute(build_insert_registro(14, date_, 3))

	test_sql_to_pandas(conn)


	### Criado os limites de data para gerar os dados
	d = date(2012, 1, 1)
	t = time(8, 0)
	start = datetime.combine(d, t)
	d = date(2016, 10, 11)
	t = time(8, 0)
	end = datetime.combine(d, t)
	date_ = random_date(start, end)

	gen_data(start, end, family_stores, 10, family_range)

	gen_data(start, end, housewife_stores, 10, housewife_range)

	gen_data(start, end, friends_stores, 30, friends_range)

	gen_data(start, end, couple_stores, 20, couple_range)

	gen_data(start, end, young_stores, 80, young_range)

	gen_data(start, end, bourgeois_stores, 30, bourgeois_range)
	#conn.commit()
	cursor.close() 
	conn.close()
	
