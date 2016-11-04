from flask import Flask, render_template, json, request
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash
import sys
from pandas_functions import *
import seaborn as sns
import numpy as np
from jinja2 import Environment, FileSystemLoader
import matplotlib.pyplot as plt
from flask import Flask, make_response

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


@app.route('/')
def main():
	conn = mysql.connect()
	df = get_registros_table(conn)
	df = df.drop("registroId", 1)
	df2 = pd.DataFrame()
	df2["datas"] = df["date"].apply(lambda x : x.date())
	df2["pessoas"] = 1
	df2 = df2.groupby("datas")["pessoas"].sum()
	print(df2)

	#graph = sns.barplot(y="userId", x="date", data=df)
	graph = sns.barplot(y=df2.values, x=df2.index)
	plt.title("Quantidade de pessoas")
	plt.ylim(0, max(df2.values)*1.1)
	filepath = "static/images/plots/exemplo.png"
	plt.savefig(filepath)

	env = Environment(loader=FileSystemLoader('.'))
	template = env.get_template("templates/index.html")

	template_vars = {"analytics" : df.to_html(index=False),
	            	 "graph1": filepath }

	html_out = template.render(template_vars)
	return html_out
	#return render_template('index.html')

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
