import imp
from logging import warning
import re
from flask import Flask, redirect,render_template,request,flash
from flask_sqlalchemy import SQLAlchemy
from flask_login  import LoginManager,UserMixin,login_user,logout_user
import os

 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= 'sqlite:///mydatabase.db'
app.config['SECRET_KEY'] = 'you-will-never-guess'
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)



@login_manager.user_loader
def load_user(id):
    return Register.query.get(int(id))


class Register(UserMixin,db.Model):

    __tablename__ = 'register'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80),nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Contact(db.Model):

    __tablename__ = 'contact'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(100),unique=True, nullable=False)
    phone = db.Column(db.String(100), nullable=False)
    messege = db.Column(db.String(500), nullable=False)
    

# db.create_all()


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/base")
def base():
    return render_template('base.html')



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method=='POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # print(first_name,last_name,username,email,password)
        user = Register.query.filter_by(username=username).first()
        if user is None:
            register = Register(first_name=first_name,last_name=last_name,username=username,email=email,password=password)
            db.session.add(register)
            db.session.commit()
            flash('You were successfully Registered','success')
            return redirect('/login')
        else:
            flash('Username already exist','danger')
            return redirect('/register')
    return render_template('register.html')


    # Add data into register table 

        # register = Register(first_name='hiren',last_name='popat',username='hirenpopat',email='hiren@123',password='hiren')
        # db.session.add(register)
        # db.session.commit()


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method=='POST':
        username = request.form['username']
        password = request.form['password']
        user = Register.query.filter_by(username=username).first()
        if user is None:
            flash("User Is Not Registered",'danger')
            return redirect('/register')
        elif user  and (password == user.password):
            login_user(user)

            flash('You were successfully Login','success')
            return redirect('/')
        
        else:
            flash('Invalid Username','danger')
            return redirect('/login')

        
    return render_template('login.html')


@app.route("/logout")
def logout():
    logout_user()
    flash('You were successfully Logout','warning')
    return redirect('/')


@app.route("/free_courses")
def courses():
   return render_template('free_courses.html')

@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method=='POST':
        full_name = request.form['full_name']
        email = request.form['email']
        phone = request.form['phone']
        messege = request.form['messege']
        contact = Contact(full_name=full_name,email=email,phone=phone,messege=messege)
        db.session.add(contact)
        db.session.commit()
        flash('Thank you for getting in touch! We appreciate you contacting us','success')
        return redirect('/')
    return render_template('contact.html')
    

@app.route("/blog")
def blog():
    return render_template('blog.html')



if __name__ == "__main__":
    app.run(debug=True)