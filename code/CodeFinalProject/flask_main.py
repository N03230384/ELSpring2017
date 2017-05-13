from flask import Flask, render_template
import json
import pandas as pd
import sqlite3 as db
from flask import Markup
app = Flask(__name__)

@app.route('/')
def main():
   con = db.connect("project_data.db")
   con.row_factory = db.Row

   cur = con.execute("select * from Data")

   rows = cur.fetchall();

  ## chart
   df = pd.read_sql_query("select * from Data",con)

   time = json.dumps(df['data_time'].values.tolist())
   soilTemp = json.dumps(df['temp1'].values.tolist())
   humidity = json.dumps(df['humidity'].values.tolist())
   airTemp = json.dumps(df['temp2'].values.tolist())
   moisture = json.dumps(df['moisture'].values.tolist())


   return render_template('index.html', rows = rows,time = time,soilTemp=soilTemp,humidity = humidity, airTemp = airTemp, moisture = moisture)



if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8088, debug=True)
