from flask import Flask,jsonify,request
from flask_mysqldb import MySQL
import json

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'CRBT'
mysql = MySQL(app)

@app.route('/')
def index():
   
   title = request.args.get('title')
   
   """
    Finding all the score 
   """
   cur = mysql.connection.cursor()
   q = """SELECT title,max(score) as c from( select title,MATCH (title)
    AGAINST ('{title}' IN NATURAL LANGUAGE MODE) AS score
FROM songs) as correct_song group by title""".format(title=title)
   
   cur.execute(q)
   row_headers=[x[0] for x in cur.description] #this will extract row headers
   rv = cur.fetchall()
   json_data=[]
   for result in rv:
        json_data.append(dict(zip(row_headers,result)))
   for data in json_data:
      if(data['c']>0):
         song_name = data['title']
   # return song_name

   """
     Taking the title with highest score to retrive the important information
   """
   outcome = mysql.connection.cursor()
   query = "SELECT * FROM songs WHERE title  = '{song_name}'".format(song_name=song_name)
   outcome.execute(query)
   row_headers=[x[0] for x in outcome.description] #this will extract row headers
   rs = outcome.fetchall()
   json_data=[]
   for result in rs:
        json_data.append(dict(zip(row_headers,result)))
   return jsonify(json_data)

if __name__=='__main__':
   app.run(host='0.0.0.0')