from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time
import pandas as pd 
import matplotlib.pyplot as plt

### Corrigindo problemas de encoding
reload(sys)
sys.setdefaultencoding("utf-8")

def get_registros_table(conn):
	table = pd.read_sql("select * from Registros;", conn)
	print(table)
	return table

def get_table(conn, table):
	table = pd.read_sql("select * from "+ table +";", conn)
	return table


def get_complete_table(conn):
	table = pd.read_sql("SELECT Registros.registroId, Registros.userId, Registros.date, Lojas.nome \
						FROM Registros \
						LEFT JOIN Lojas ON Registros.placeId = Lojas.placeId;", conn)
	return table

def get_stores_as_options(conn):
	table = pd.read_sql("SELECT * FROM Lojas;", conn)
	print(list(table["nome"].values))
	return list(table["nome"].values)

def build_each_store_serie(df):
	stores = df["nome"].unique()

	for store in stores:
		df2 = pd.DataFrame()
		df2["datas"] = df[df["nome"] == store]["date"]
		df2["pessoas"] = 1
		df2 = df2.set_index('datas')
		df2 = df2.resample('M', how='sum')
		plt.plot(df2, label=store)


	plt.title("Cada loja selecionada")
	plt.ylim(0, max(df2.values)*1.1)
	plt.legend()
	filepath = "static/images/plots/build_each_store_serie.png"
	plt.savefig(filepath)
	plt.clf()

	return filepath
