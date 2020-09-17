import sqlite3
from flask import g
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
#首页
@app.route('/')
def index():
   return render_template('main.html')
'''
@app.route('/main/<list_name>/<timeline>')
def index():
   return render_template('main.html')
'''
# 初始化数据库连接:
#数据库链接与绘图
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///time.sqlite3'
app.config['SECRET_KEY'] = "random string"
db = SQLAlchemy(app)
##时间模型list1
class list1_time(db.Model):
   __tablename__ = "list1"
   timeline = db.Column('timeline', db.Integer, primary_key = True)
   value = db.Column(db.REAL)
   iswrong = db.Column(db.Integer)
def __init__(self, timeline, value, iswrong):
   self.timeline = timeline
   self.value = value
   self.iswrong = iswrong
#查询
##时间模型list2
class list2_time(db.Model):
   __tablename__ = "list2"
   timeline = db.Column('timeline', db.Integer, primary_key = True)
   value = db.Column('value',db.REAL)
   iswrong = db.Column('iswrong',db.Integer)
def __init__(self, timeline, value, iswrong):
   self.timeline = timeline
   self.value = value
   self.iswrong = iswrong
##查询
@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      if request.form['chose']=="list1" :
         times=( list1_time.query.filter_by(timeline = request.form['time']).all())
      else:
         times=( list2_time.query.filter_by(timeline= request.form['time']).all())
   return render_template("result.html",result = times)

##绘图

@app.route('/plot',methods = ['POST', 'GET'])
def plot():
   if request.method == 'POST':
      if request.form['chose']=="list1" :
         times=( list1_time.query.filter( list1_time.timeline >=request.form['start'] , list1_time.timeline <= request.form['end'] ).all())
      else:
         times=( list2_time.query.filter( list2_time.timeline >=request.form['start'] , list2_time.timeline <= request.form['end'] ).all())
   result = []
   for x in times:
      result.append(x.value)
   return render_template("plot.html",result=result,length=len(result))


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)

