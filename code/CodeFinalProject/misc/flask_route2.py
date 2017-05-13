from flask import Flask, render_template
import json
import pandas as pd
import sqlite3 as db
from flask import Markup
app = Flask(__name__)

@app.route('/list')
def list():
   con = db.connect("project_data.db")
   con.row_factory = db.Row
   
   cur = con.execute("select * from Data")
   
   rows = cur.fetchall(); 
     
   return render_template('list2.html', rows = rows)

@app.route('/linegraph')
def graph():
   con = db.connect("project_data.db")
  
   df = pd.read_sql_query("select * from Data LIMIT 40",con)
   
   time = json.dumps(df['data_time'].values.tolist())
   soilTemp = json.dumps(df['temp1'].values.tolist())
   humidity = json.dumps(df['humidity'].values.tolist())
   airTemp = json.dumps(df['temp2'].values.tolist())
   moisture = json.dumps(df['moisture'].values.tolist())

  
   return render_template('test2.html', time = time,soilTemp=soilTemp,humidity = humidity, airTemp = airTemp, moisture = moisture)


if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8088, debug=True)
