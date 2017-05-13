from flask import Flask, render_template
# import datetime
import sqlite3 as db
from flask import Markup
app = Flask(__name__)

@app.route('/list')
def list():
   con = db.connect("project_data.db")
   con.row_factory = db.Row
   
   cur = con.execute("select * from Data")
   
   rows = cur.fetchall(); 
  
   
   return render_template('datalist.html', rows = rows)

if __name__ == "__main__":
 app.run(host='0.0.0.0', port=8088, debug=True)

