from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time

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
	msg = "insert into Registros values(\"" + str(registroId) + "\"," \
										  + str(userId) + ",\"" \
										  + str(date) + "\"," \
										  + str(placeId) + ")"
	return msg




"""
insert into User values('','Admin','admin');
"""

if __name__ == "__main__":
	#date = datetime("20/02/2016")
	d = date(2005, 7, 14)
	t = time(12, 30)
	date_ = datetime.combine(d, t)
	print(date_)
	print(build_insert_registro(10, date_, 1))

	conn = mysql.connect()
	cursor = conn.cursor()
	cursor.execute(build_insert_registro(10, date_, 1, 2))
	conn.commit()
	cursor.close() 
	conn.close()
