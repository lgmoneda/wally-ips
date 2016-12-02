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
from PIL import Image


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


	### WIN
	import matplotlib.dates as mdates
	if how == "H":
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

	df = df[stores]
	#df = pd.get_dummies(df["nome"]).set_index(df.index)

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

	based_array = np.array([1 if str(store) in based_on else 0 for store in stores_names])


	scores = np.dot(coocc.as_matrix(), based_array)



	recommends = [(x, y) for (y,x) in sorted(zip(stores_names, scores), reverse=False)]
	recommends = [(x, y) for (x, y) in recommends if x != 0]
	recommends = sorted(recommends, reverse=True)
	recommends = ["static/images/logos/"+str(y)+".png" for (x, y) in recommends]

	return recommends

def build_heat_map(df):
	

	ten_min_data = [True if ( x.time() <= datetime.today().time() and
							   x.time() >= (datetime.today() - timedelta(minutes=30)).time()) else False for x in df["date"]]
	df = df[ten_min_data]

	print(df["nome"].value_counts())
	stores = df["nome"].value_counts().index.values 
	people = df["nome"].value_counts().values

	color_level_step = 9

	color = dict()
	color["Americanas"] = (255, 255, 255, 255)
	color["Rascal"] = (255, 255, 255, 255)
	color["Viena"] = (255, 255, 255, 255)
	color["Centauro"] = (255, 255, 255, 255)
	color["Bodytech"] = (255, 255, 255, 255)

	color["Calvin Klein"] = (255, 255, 255, 255)
	color["Lacoste"] = (255, 255, 255, 255)
	color["Hering"] = (255, 255, 255, 255)
	color["Arezzo"] = (255, 255, 255, 255)
	color["Carrefour"] = (255, 255, 255, 255)


	### Floor 2
	color["Cinemark"] = (255, 255, 255, 255)
	color["Lilica & Tigor"] = (255, 255, 255, 255)
	color["Havaianas"] = (255, 255, 255, 255)
	color["Bayard"] = (255, 255, 255, 255)
	color["Ralph Lauren"] = (255, 255, 255, 255)

	color["Saraiva"] = (255, 255, 255, 255)
	color["C&A"] = (255, 255, 255, 255)
	color["City Lar Eletrodomésticos"] = (255, 255, 255, 255)
	color["Drogasil"] = (255, 255, 255, 255)
	color["Hot Zone"] = (255, 255, 255, 255)

	for i in range(len(stores)):
		if 255 - people[i] < 0:
			replace = 0
		else:
			replace = 255 - people[i]*color_level_step
		color[stores[i]] = (255, replace, replace, 255)


	shift_x = 145
	shift_y = 110
	locations = dict()
	locations["Americanas"] = (0, 0)
	locations["Rascal"] = (0, 1)
	locations["Viena"] = (0, 2)
	locations["Centauro"] = (0, 3)
	locations["Bodytech"] = (0, 4)

	locations["Calvin Klein"] = (1, 0)
	locations["Lacoste"] = (1, 1)
	locations["Hering"] = (1, 2)
	locations["Arezzo"] = (1, 3)
	locations["Carrefour"] = (1, 4)

	base_pixel = np.array((80, 65, 230, 175))
	pixels = dict()
	for key, value in locations.items():
	    j = value[0]
	    i = value[1]
	    pixels[key] = base_pixel + (shift_x * i, shift_y * j, shift_x * i, shift_y * j)

	image = Image.open("static/images/floor_1_clean.png")
	image.convert("RGBA") # Convert this to RGBA if possible

	pixel_data = image.load()

	if image.mode == "RGBA":
	  # If the image has an alpha channel, convert it to white
	  # Otherwise we'll get weird pixels
	  for y in xrange(image.size[1]): # For each row ...
	    for x in xrange(image.size[0]): # Iterate through each column ...
	      # Check if it's opaque
	      if pixel_data[x, y][3] < 255:
	        # Replace the pixel data with the colour white
	        for key, value in pixels.items():
	            if x > pixels[key][0] and x < pixels[key][2] and y > pixels[key][1] and y < pixels[key][3]:
	                pixel_data[x, y] = color[key]

	filename = "static/images/floor_1.png"
	# Resize the image thumbnail
	#image.thumbnail([resolution.width, resolution.height], Image.ANTIALIAS)
	image.save(filename) 


	locations["Cinemark"] = (0, 0)
	locations["Lilica & Tigor"] = (0, 1)
	locations["Havaianas"] = (0, 2)
	locations["Bayard"] = (0, 3)
	locations["Ralph Lauren"] = (0, 4)

	locations["Saraiva"] = (1, 0)
	locations["C&A"] = (1, 1)
	locations["City Lar Eletrodomésticos"] = (1, 2)
	locations["Drogasil"] = (1, 3)
	locations["Hot Zone"] = (1, 4)

	base_pixel = np.array((105, 85, 255, 195))
	pixels = dict()
	for key, value in locations.items():
	    j = value[0]
	    i = value[1]
	    pixels[key] = base_pixel + (shift_x * i, shift_y * j, shift_x * i, shift_y * j)

	image = Image.open("static/images/floor_2_clean.png")
	image.convert("RGBA") # Convert this to RGBA if possible

	pixel_data = image.load()

	if image.mode == "RGBA":
	  # If the image has an alpha channel, convert it to white
	  # Otherwise we'll get weird pixels
	  for y in xrange(image.size[1]): # For each row ...
	    for x in xrange(image.size[0]): # Iterate through each column ...
	      # Check if it's opaque
	      if pixel_data[x, y][3] < 255:
	        # Replace the pixel data with the colour white
	        for key, value in pixels.items():
	            if x > pixels[key][0] and x < pixels[key][2] and y > pixels[key][1] and y < pixels[key][3]:
	                pixel_data[x, y] = color[key]

	filename = "static/images/floor_2.png"
	# Resize the image thumbnail
	#image.thumbnail([resolution.width, resolution.height], Image.ANTIALIAS)
	image.save(filename) 
