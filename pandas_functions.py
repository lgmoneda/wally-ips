# encoding=utf8  
from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
import sys
from datetime import datetime, date, time, timedelta
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import dates
import numpy as np


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
	print("HOW NA DESCREPTIVE ")
	print(how)
	if how != "M" and how != "W" and how != "D":
		descriptive_dict["max_time"] = df["pessoas"].idxmax().strftime("%H:%M")
	else:
		descriptive_dict["max_time"] = df["pessoas"].idxmax().strftime("%d, %b %Y")


	

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


def one_hot_encoding(df, columns, keep=False):
    """ 
    Transform categorical data to the one hot encoding representation. 
    Parameters
    ----------
    df: pandas.DataFrame
        The entire dataframe in which the categorical data is present. 
    columns: string list
        A list containing all categorical data columns names.
    keep: boolean
        Chooses if the categorical columns will be kept or dropped.
    Returns
    -------
    df: pandas.DataFrame
        The new dataframe with the categorical columns.
    ohe_columns: string list
        A list with the new columns names.
    Example
    -------
    data = pd.DataFrame({"Product Category": ["cellphone", "TV", "refrigerator", "notebook"], 
                      "Year": ["2008", "2009", "2013", "2016"]})
    data, categorical_features = onehot_encoding(data, ["Product Category","Year"])
    """
    ohe_data = pd.get_dummies(df[columns])
    ohe_columns = ohe_data.columns
    
    if not keep:
        df = df.drop(columns, axis=1)
    df = df.join(ohe_data)
    return df, list(ohe_columns.values)


def build_corr(df):
	df, stores = one_hot_encoding(df, ["nome"], keep = False)
	df = df.groupby(df["userId"]).sum()
	#df = df.apply(lambda x : 1 if x > 1 else x)
	print("Quantidade de users: ")
	print(len(df))
	df = df[stores]
	#df = pd.get_dummies(df["nome"]).set_index(df.index)
	print(df.head())
	#sns.set_palette("Blues")
	#coocc = df.T.dot(df)
	coocc = df.corr()
	plt.figure(figsize=(16,16))
	stores_names = [store[5:] for store in stores]
	sns.heatmap(coocc, square=True, annot=True, xticklabels=stores_names, yticklabels=stores_names, fmt=".2f", cbar=False, cmap="Blues")
	#sns.set_palette("Blues")
	plt.xticks(rotation=90, size=16)	
	plt.yticks(rotation=0, size=16) 

	plt.savefig("static/images/plots/teste.png", bbox_inches='tight')
	plt.clf()

	print(df.values)
	print(coocc)
	return "static/images/plots/teste.png"

def set_diag(self, values): 
    n = min(len(self.index), len(self.columns))
    self.values[[np.arange(n)] * 2] = values
pd.DataFrame.set_diag = set_diag

def recommend(df, based_on):
	df, stores = one_hot_encoding(df, ["nome"], keep = False)
	df = df.groupby(df["userId"]).sum()
	df = df[stores]
	coocc = df.T.dot(df)
	coocc.set_diag(0)

	stores_names = [store[5:] for store in stores]
	print(stores_names)
	print(based_on)
	based_array = np.array([1 if str(store) in based_on else 0 for store in stores_names])
	print("array da massa")
	print(based_array)

	print(coocc.index)

	print(np.dot(coocc.as_matrix(), based_array))

	scores = np.dot(coocc.as_matrix(), based_array)



	recommends = [(x, y) for (y,x) in sorted(zip(stores_names, scores), reverse=False)]
	recommends = [(x, y) for (x, y) in recommends if x != 0]
	recommends = sorted(recommends, reverse=True)
	recommends = ["static/images/logos/"+str(y)+".png" for (x, y) in recommends]
	print(recommends)
	return recommends

