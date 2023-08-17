from flask import Flask, render_template, request, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__,template_folder='templates')
app.config["SECRET_KEY"]="hhfjksjf"
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///User.db'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///Data.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=True

db=SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False,unique=True)
    password = db.Column(db.String(80),nullable=False)

class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(10),nullable=False)
    lastname = db.Column(db.String(10),nullable=False)
    age=db.Column(db.String(100),nullable=False)
    roomno=db.Column(db.String(100),nullable=False,unique=True)


@app.route('/')
def Main():
    return render_template('Main.html')

@app.route('/Login',methods=["POST","GET"])
def Login():
    if request.method =="POST":
        ema=request.form["em"]
        pa=request.form["pas"]
        user=User.query.filter_by(username=ema).first()
        if user:
            if user.password==pa:
                return render_template('Rooms.html')
            else:
                return render_template('Login.html')
        else:
            return render_template('Login.html')
    else: 
        return render_template('Login.html')   

@app.route('/Home')
def Home():
    return render_template('Main.html')

@app.route('/Signup',methods=["POST","GET"])
def Signup():
    if request.method =="POST":
        em=request.form["ema"]
        pas=request.form["pass"]
        fill=User(username=em,password=pas)
        db.session.add(fill)
        db.session.commit()
        return redirect(url_for('Login'))
    else:
        return render_template('Signup.html')

@app.route('/Rooms')
def Rooms():
    return render_template('Rooms.html')

@app.route('/Tables')
def Tables():
    return render_template('Tables.html',query=Data.query.all())

@app.route('/Checkin',methods=["POST","GET"])
def Checkin():
    if request.method=="POST":
        fin=request.form["fn"]
        lan=request.form["ln"]
        age=request.form["ag"]
        ron=request.form["rn"]

        fill=Data(firstname=fin,lastname=lan,age=age,roomno=ron)
        db.session.add(fill)
        db.session.commit()
        return redirect(url_for('Tables'))
    else:
        return render_template('checkin.html')

@app.route('/Checkout')
def Checkout():
    return render_template('checkout.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=8000)