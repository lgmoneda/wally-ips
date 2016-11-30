# encoding=utf8  
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time, timedelta
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import dates


### Corrigindo problemas de encoding
reload(sys)  
sys.setdefaultencoding('utf8')

def get_registros_table(conn):
	table = pd.read_sql("select * from Registros;", conn)
	return table

def get_table(conn, table):
	table = pd.read_sql("select * from "+ table +";", conn)
	return table


def get_complete_table(conn):
	table = pd.read_sql("SELECT Registros.registroId, Registros.userId, Registros.date, Lojas.nome, Lojas.categoria \
						FROM Registros \
						LEFT JOIN Lojas ON Registros.placeId = Lojas.placeId;", conn)
	return table

def get_stores_as_options(conn):
	table = pd.read_sql("SELECT * FROM Lojas;", conn)
	#print(list(table["nome"].values))
	return list(table["nome"].values)

def get_categories_as_options(conn):
	table = pd.read_sql("SELECT distinct(Lojas.categoria) FROM Lojas;", conn)
	#print(list(table["nome"].values))
	return list(table["categoria"].values)
	#return list(table["categoria"].unique().values)

def build_aggregate_serie(df):
	pass

def build_each_store_serie(df, filename, title=" ", legend=False, how='M'):
	stores = df["nome"].unique()
	print(df.head())

	max_value = 0
	final_xticks_labels = []
	fig, ax = plt.subplots()
	for store in stores:
		df2 = pd.DataFrame()
		df2["date"] = df[df["nome"] == store]["date"]
		df2["pessoas"] = 1

		df2 = df2.set_index('date')
		df2 = df2.resample(how).sum()
		df2 = df2.fillna(0)

		if df2["pessoas"].max() > max_value:
			max_value = df2["pessoas"].max()

	
		plt.plot(df2, label=store)
	print(df2.head())

	### WIN
	import matplotlib.dates as mdates
	if how == "H":
		print("\n\n\n\nFORMATAO")
		timeFmt = mdates.DateFormatter('%H:%M')
		ax.xaxis.set_major_formatter(timeFmt)

	plt.title(title)
	plt.xlabel("Horário")
	plt.ylabel("Quantidade de visitantes")
	plt.xticks(rotation=45, size=14)	
	plt.ylim(0, max_value*1.1)
	filepath = "static/images/plots/" + filename
	if legend:
		lgd = plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))	
		plt.savefig(filepath, bbox_extra_artists=(lgd,), bbox_inches='tight')
	else:
		plt.savefig(filepath, bbox_inches='tight')
	plt.clf()

	return filepath

def realTimeFilters(df, option=0):

	option = int(option)
	todays_data = [True if x.date() == datetime.today().date() else False for x in df["date"]]
	df = df[todays_data]


	if option == 1:
		hour_data = [True if ( x.time() <= datetime.today().time() and
							   x.time() >= (datetime.today() - timedelta(minutes=60)).time()) else False for x in df["date"]]

		df = df[hour_data]
	

	return df

def histTimeFilters(df, start, end):

	#todays_data = [True if x.date() == datetime.today().date() else False for x in df["date"]]
	df = df[(df["date"] > start) & (df["date"] < end)]
	

	# if option == 1:
	# 	hour_data = [True if ( x.time() <= datetime.today().time() and
	# 						   x.time() >= (datetime.today() - timedelta(minutes=60)).time()) else False for x in df["date"]]

	# 	df = df[hour_data]
	

	return df

def build_descriptive_dict(df, how='M'):

	descriptive_dict = dict()
	descriptive_dict["unique_guests"] = len(df["userId"].unique())

	df = df.set_index('date')
	df = df.resample(how).sum()
	descriptive_dict["max"] = int(df["pessoas"].max())
	if how != "M":
		descriptive_dict["max_time"] = df["pessoas"].idxmax().strftime("%H:%M")
	else:
		descriptive_dict["max_time"] = df["pessoas"].idxmax()
	

	return descriptive_dict

def build_unique_bar(df, filename, title, legend):

	df["pessoas"] = 1
	df = df.set_index('date')
	df = df.fillna(0)
	df = df.drop_duplicates(["nome", "userId"])
	plt.figure(figsize=(16, 8))
	ax = sns.countplot(x="nome", data=df, palette="muted")
	for item in ax.get_xticklabels(): item.set_rotation(90)
	plt.title(title)
	plt.ylabel("Quantidade de visitantes")
	plt.xlabel("Lojas")
	ymin, ymax = ax.get_ylim()
	plt.ylim(0, ymax*1.1)
	filepath = "static/images/plots/" + filename
	plt.savefig(filepath, bbox_inches='tight')
	plt.clf()

	return filepath

def return_selected_stores(query_string, all_stores, conn):

	if  "cat_" not in query_string > 1:
		print(query_string)
		print("," in query_string)
		if "," in query_string:
			selected_stores = query_string.split(",")
		else:
			selected_stores = []
			selected_stores.append(query_string)
		return selected_stores

			
	else:
		selected_stores = query_string[4:]
		if selected_stores == "Todas":
			table = pd.read_sql("SELECT Lojas.nome FROM Lojas;", conn)
			return list(table["nome"].values)
		else: 
			table = pd.read_sql("SELECT Lojas.nome, Lojas.categoria FROM Lojas WHERE categoria = \"" + selected_stores + "\";", conn)
			return list(table["nome"].values)
