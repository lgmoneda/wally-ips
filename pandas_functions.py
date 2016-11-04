from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time
import pandas as pd 

### Corrigindo problemas de encoding
reload(sys)
sys.setdefaultencoding("utf-8")

def get_registros_table(conn):
	table = pd.read_sql("select * from Registros;", conn)
	print(table)
	return table
