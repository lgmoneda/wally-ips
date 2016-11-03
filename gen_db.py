from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time
import pandas as pd 

### Corrigindo problemas de encoding
reload(sys)
sys.setdefaultencoding("utf-8")

mysql = MySQL()
app = Flask(__name__)

# MySQL 
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '___'
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
	msg = "insert into Registros values(\'\'," \
										  + str(userId) + ",\"" \
										  + str(date) + "\"," \
										  + str(placeId) + ")"
	return msg

def test_sql_to_pandas(conn):
	tabela = pd.read_sql("select * from Registros;", conn)
	print(tabela)

if __name__ == "__main__":

	d = date(2005, 7, 14)
	t = time(12, 30)
	date_ = datetime.combine(d, t)
	print(date_)
	print(build_insert_registro(10, date_, 1))

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(build_insert_registro(10, date_, 1))

	test_sql_to_pandas(conn)
	conn.commit()
	cursor.close() 
	conn.close()
