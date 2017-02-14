# encoding=utf8 
from flask import Flask, render_template, json, request, jsonify
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import sys
from pandas_functions import *
import seaborn as sns
import numpy as np
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from flask import Flask, make_response
from flask import request
import json


### Fixing encoding problems
reload(sys)
sys.setdefaultencoding("utf-8")

mysql = MySQL()
app = Flask(__name__)

### MySQL 
app.config['MYSQL_DATABASE_USER'] = 'wally-user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ondeestou'
app.config['MYSQL_DATABASE_DB'] = 'Wally'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def main():

    ### Guarantee they're defined
    descriptive_dict = None
    descriptive_dict_hist = None
    filepath_aggregate = None
    filepath_each_serie = None
    filepath_graph3 = None

    
    option = 0
    ### Info to feed options
    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    categories_dropdown = get_categories_as_options(conn)

    how = "H"
    try:
        selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)
        option = request.form['time']
    except:
        selected_stores = stores_dropdown
    
    df = get_complete_table(conn)
    print(df.describe())
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    print(df.describe())
    df = realTimeFilters(df, option)
    print(df.describe())
    df_ori = df.copy()
    
    plt.clf()
    if len(df) > 1:
        valid = True
        filepath_each_serie, filepath_graph3, filepath_aggregate, descriptive_dict_hist = build_descriptive_graphs(df, how)
    else:
        valid = False
        descriptive_dict = {}
        filepath_aggregate = "static/images/wally.jpg"
        filepath_each_serie = "static/images/wally.jpg"

    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("templates/index.html")

    
    template_vars = {"descriptive_dict": descriptive_dict,
                     "descriptive_dict_hist": descriptive_dict,
                     "graph1": filepath_aggregate,
                     "graph2": filepath_each_serie,
                     "graph3": filepath_graph3,
                     "stores_dropdown": stores_dropdown,
                     "categories_dropdown": categories_dropdown,
                     "valid": valid}

    html_out = template.render(template_vars)
    return html_out
        


@app.route('/realtime', methods=['POST','GET'])
def getRealTime():


    descriptive_dict = None
    filepath_aggregate = None
    filepath_each_serie = None

    option = request.form['time']

    ### Info to feed options
    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    categories_dropdown = get_categories_as_options(conn)

    if option == "1":
        how = "10T"
    else:
        how = "H"

    selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    df = realTimeFilters(df, option)

    
    if len(df) > 1:
        valid = True
        filepath_each_serie, filepath_graph3, filepath_aggregate, descriptive_dict_hist = build_descriptive_graphs(df, how)
    else:
        ### When there's not data, we define place holders.
        valid = False
        descriptive_dict = {}
        filepath_aggregate = "static/images/wally.jpg"
        filepath_each_serie = "static/images/wally.jpg"
        filepath_graph3 = "static/images/wally.jpg"

    
    response = {"descriptive_dict": descriptive_dict,
                 "graph1": filepath_aggregate,
                 "graph2": filepath_each_serie,
                 "graph3": filepath_graph3,
                 "stores_dropdown": stores_dropdown,
                 "categories_dropdown": categories_dropdown,
                 "valid": valid}


    return jsonify(**response)

@app.route('/historical', methods=['POST','GET'])
def getHistorico():

    descriptive_dict_hist = None
    filepath_aggregate = None
    filepath_each_serie = None

    option  = 0

    start_date = request.form['start_date']
    start_date = start_date.split("/")[2] + "-" + start_date.split("/")[0] + "-" + start_date.split("/")[1]

    end_date = request.form['end_date']
    end_date = end_date.split("/")[2] + "-" + end_date.split("/")[0] + "-" + end_date.split("/")[1]

    days_between = (datetime.strptime(end_date, "%Y-%m-%d").date() - datetime.strptime(start_date, "%Y-%m-%d").date()).days
    
    if days_between > 90 and days_between < 270:
        how = "W"
    elif days_between >= 270:
        how = "M"
    else:
        how = "D"

        
    ### Info to feed options
    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    categories_dropdown = get_categories_as_options(conn)


    selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)

    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    df = histTimeFilters(df, start_date, end_date)

    if len(df) > 1:
        valid_hist = True
        filepath_each_serie, filepath_graph3, filepath_aggregate, descriptive_dict_hist = build_descriptive_graphs(df, how)
    else:

        ### When there's not data, we define place holders.
        valid_hist = False
        descriptive_dict = {}
        filepath_aggregate = "static/images/wally.jpg"
        filepath_each_serie = "static/images/wally.jpg"
        filepath_graph3 = "static/images/wally.jpg"
        descriptive_dict_hist = None

    valid_hist = True
    
    response = {"descriptive_dict_hist": descriptive_dict_hist,
                 "graph1_hist": filepath_aggregate,
                 "graph2_hist": filepath_each_serie,
                 "graph3_hist": filepath_graph3,
                 "stores_dropdown": stores_dropdown,
                 "categories_dropdown": categories_dropdown,
                 "valid_hist": valid_hist}


    return jsonify(**response)


@app.route('/heatmap', methods=['POST','GET'])
def getHeatMap():
    
    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    build_heat_map(df)

    response = {"heatmap_img": 2,
                "test": 3}

    return jsonify(**response)
    

@app.route('/similarstores', methods=['POST','GET'])
def getStoresCorr():
    
    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    corr_file = build_corr(df)

    response = {"heatmap_file": corr_file}

    return jsonify(**response)


@app.route('/recommender', methods=['POST','GET'])
def getRecommender():

    conn = mysql.connect()
    stores_dropdown = get_stores_as_options(conn)
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)
    recommended_stores = recommend(df, selected_stores)

    response = {"stores": recommended_stores}

    return jsonify(**response)
    
@app.route('/sobre')
def showSignUp():
    return render_template('sobre.html')


if __name__ == "__main__":
    app.run(port=5002)
