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
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '***REMOVED***'
app.config['MYSQL_DATABASE_DB'] = 'Wally'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/', methods=['POST', 'GET'])
def main():

    descriptive_dict = None
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

        if len(request.form['selected_stores']) > 1:
    	   selected_stores = request.form['selected_stores'].split(",")
        else:
            selected_stores = request.form['selected_stores']
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

    if len(request.form['selected_stores']) > 1:
       selected_stores = request.form['selected_stores'].split(",")
    else:
        selected_stores = request.form['selected_stores']


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

    print(len(request.form))
    print(request.form)

    conn = mysql.connect()

    stores_dropdown = get_stores_as_options(conn)

    try:
        print("REQUEST STORES")
        print(request.form['selected_stores'])
        if len(request.form['selected_stores']) > 1:
           selected_stores = request.form['selected_stores'].split(",")
        else:
            selected_stores = request.form['selected_stores']
    except:
        selected_stores = stores_dropdown

    #df = get_registros_table(conn)
    
    df = get_complete_table(conn)
    df = df.drop("registroId", 1)
    df = df[df["nome"].isin(selected_stores)]
    filepath_each_serie = build_each_store_serie(df, "historicalGraph1")
    
    plt.clf()

    print("marcando")
    df2 = pd.DataFrame()
    #df2["datas"] = df["date"].apply(lambda x : x.date())
    df2["datas"] = df["date"]
    df2["userId"] = df["userId"]
    df2["pessoas"] = 1
    #df2.index = pd.to_datetime(df2.index)
    df2 = df2.set_index('datas')
    df2 = df2.resample('M').sum()
    #df2 = df2.groupby("datas")["pessoas"].sum()
    #df2 = df2.resample('M', how='sum')
    descriptive_dict = build_descriptive_dict(df2)
    #print(df2)

    #graph = sns.barplot(y="userId", x="date", data=df)
    #graph = sns.barplot(y=df2.values, x=df2.index)
    #graph = sns.tsplot(df2, time="datas", unit="pessoas")
    graph = plt.plot(df2["pessoas"])
    plt.title("Quantidade de pessoas")
    plt.ylim(0, max(df2["pessoas"].values)*1.1)
    filepath_aggregate = "static/images/plots/realTimeGraph1.png"
    plt.savefig(filepath_aggregate)
    plt.clf()

    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("templates/index.html")

    template_vars = {"analytics_hist1" : df.head(5).to_html(index=False),
                     "descriptive_dict": descriptive_dict,
                     "graph1_hist": filepath_aggregate,
                     "graph2": filepath_each_serie,
                     "stores_dropdown": stores_dropdown }

    html_out = template.render(template_vars)

    return html_out



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
