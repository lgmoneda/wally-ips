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


### Corrigindo problemas de encoding
reload(sys)
sys.setdefaultencoding("utf-8")

mysql = MySQL()
app = Flask(__name__)

# MySQL 
app.config['MYSQL_DATABASE_USER'] = 'wally-user'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ondeestou'
app.config['MYSQL_DATABASE_DB'] = 'Wally'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def main():

    descriptive_dict = None
    descriptive_dict_hist = None
    filepath_aggregate = None
    filepath_each_serie = None


    option = 0
    conn = mysql.connect()

    stores_dropdown = get_stores_as_options(conn)
    categories_dropdown = get_categories_as_options(conn)

    if option == "1":
        how = "10T"
    else:
        how = "H"

    try:
        selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)
        option = request.form['time']

        # if len(request.form['selected_stores']) > 1:
    	   # selected_stores = request.form['selected_stores'].split(",")
        # else:
        #     selected_stores = request.form['selected_stores']
    except:
		selected_stores = stores_dropdown


    
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    df = realTimeFilters(df, option)
    df_ori = df.copy()

    filepath_graph3 = build_unique_bar(df, 
                                       "realTimeGraph3.png", 
                                       "Total de visitantes únicos no período", 
                                       True)
    plt.clf()
    if len(df) > 1:
        valid = True
        filepath_each_serie = build_each_store_serie(df, 
                                                     "realTimeGraph2.png", 
                                                     "Visitantes ao longo do tempo para cada loja",
                                                     True,
                                                     how)
        plt.clf()

        filepath_graph3 = build_unique_bar(df_ori, 
                                           "realTimeGraph3.png", 
                                           "Total de visitantes únicos no período", 
                                           True)

        df["nome"] = "Todas as lojas selecioandas"
        filepath_aggregate = build_each_store_serie(df, 
                                                    "realTimeGraph1.png", 
                                                    "Visitantes ao longo do tempo em todas as lojas selecionadas", 
                                                    False,
                                                    how)
        

        descriptive_dict = build_descriptive_dict(df, 'H')


        plt.clf()
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
    #return render_template('index.html')



@app.route('/realtime', methods=['POST','GET'])
def getRealTime():


    descriptive_dict = None
    filepath_aggregate = None
    filepath_each_serie = None


    option = request.form['time']
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
        filepath_each_serie = build_each_store_serie(df, 
                                                     "realTimeGraph2.png", 
                                                     "Visitantes ao longo do tempo para cada loja",
                                                     True,
                                                     how)
        plt.clf()

        filepath_graph3 = build_unique_bar(df, "realTimeGraph3.png", "Total de visitantes únicos no período", True)
        
        df["nome"] = "Todas as lojas selecioandas"
        filepath_aggregate = build_each_store_serie(df, 
                                                    "realTimeGraph1.png", 
                                                    "Visitantes ao longo do tempo em todas as lojas selecionadas", 
                                                    False,
                                                    how)
        
        


        descriptive_dict = build_descriptive_dict(df, 'H')

        plt.clf()

    else:

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
    print("ENTREI NO HISTORICO")



    descriptive_dict_hist = None
    filepath_aggregate = None
    filepath_each_serie = None

    option  = 0

    start_date = request.form['start_date']
    start_date = start_date.split("/")[2] + "-" + start_date.split("/")[0] + "-" + start_date.split("/")[1]

    end_date = request.form['end_date']
    end_date = end_date.split("/")[2] + "-" + end_date.split("/")[0] + "-" + end_date.split("/")[1]

    print("Dates requestadas: {0} e {1}".format(start_date, end_date))

    conn = mysql.connect()

    stores_dropdown = get_stores_as_options(conn)
    categories_dropdown = get_categories_as_options(conn)


    how = "D"

    selected_stores = return_selected_stores(request.form['selected_stores'], stores_dropdown, conn)

    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    #df = realTimeFilters(df, option)

    df = histTimeFilters(df, start_date, end_date)

    if len(df) > 1:
        valid_hist = True
        filepath_each_serie = build_each_store_serie(df, 
                                                     "histTimeGraph2.png", 
                                                     "Visitantes ao longo do tempo para cada loja",
                                                     True,
                                                     how)
        plt.clf()

        filepath_graph3 = build_unique_bar(df, "histTimeGraph3.png", "Total de visitantes únicos no período", True)
        
        df["nome"] = "Todas as lojas selecioandas"
        filepath_aggregate = build_each_store_serie(df, 
                                                    "histTimeGraph1.png", 
                                                    "Visitantes ao longo do tempo em todas as lojas selecionadas", 
                                                    False,
                                                    how)
        
        


        descriptive_dict_hist = build_descriptive_dict(df, 'M')

        plt.clf()

    else:

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



@app.route('/sobre')
def showSignUp():
    return render_template('sobre.html')


@app.route('/signUp',methods=['POST','GET'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:
            
            # All Good, let's call MySQL
            
            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close() 
        conn.close()


if __name__ == "__main__":
    app.run(port=5002)
