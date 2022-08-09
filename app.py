from flask import Flask, render_template, url_for, request, redirect
from datetime import datetime
import sys
from sqlalchemy import create_engine

app = Flask(__name__)
db = create_engine('mysql://user:pass@localhost/flaskdata')

class dbsql():
    def insert_content(self, content):
        try:
            db.execute("insert into flaskdata.model (content) values (%s)", (content))
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
    def delete_content(self, id):
        try:
            db.execute("DELETE FROM flaskdata.model WHERE id = %s", (id))
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
    
    def update_content(self, id, content):
        try:
            db.execute("UPDATE flaskdata.model SET content = %s WHERE id = %s", (content,id))
        except BaseException as err:
            print(f"Unexpected {err=}, {type(err)=}")
            
    def get_data(self):
        result = db.execute("select * from model")
        return result.fetchall()
    
#index
@app.route('/', methods=['POST','GET'])
def index():
    dbs = dbsql()    
    if request.method =='POST':
        task_content = request.form['content']
        try:
            print('insert data', file=sys.stdout)
            dbs.insert_content(task_content)
            return redirect('/')
        except e: # work on python 2.x
            print(f"Unexpected {err=}, {type(err)=}")
    else:
        tasks = dbs.get_data()
        
        for i in range(len(tasks)):
            print(tasks[i][1]+str(tasks[i][2].date()), file=sys.stdout)
            
        return render_template('index.html', task=tasks, len=range(len(tasks)), str=str)
#delete    
@app.route('/delete/<int:id>')
def delete(id):
    dbs = dbsql()    
    try:
        print(f'Deleting {id}', file=sys.stdout)
        dbs.delete_content(id)
        return redirect('/')
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")
#update
@app.route('/update/<int:id>', methods = ['GET','POST'])
def update(id):
    dbs = dbsql()    
    if request.method =='POST':
        task_content = request.form['content']
        try:
            dbs.update_content(id, task_content)
            return redirect('/')
        except err: 
            print(f"Unexpected {err=}, {type(err)=}")
    else:
        return render_template('update.html', id=id)
        
if __name__ == "__main__":
    app.run()