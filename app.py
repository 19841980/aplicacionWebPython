#import
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from werkzeug.security import check_password_hash

#create the SQLAlchemy instance
db = SQLAlchemy()
def create_app():
#create the flask aplicacion
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.config['SECRET_KEY'] = 'password'

#inicializa SQLAlchemy with this Flask application
    db.init_app(app)

    with app.app_context():
        db.create_all()
    return app

app = create_app()

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



#database tablas
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Product{self.title}>'
    
class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))

#login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

#url
#http://127.0.0.1:5000

#routes
@app.route('/')
def home():
    products = products.query.all()
    return render_template('home.html', products=products)

@app.route('/login')
def login():
    return render_template('login.html')

#products routes
@app.route('/products', methods=['GET','POST'])
def create_product():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        price = request.form.get('price')
        product = product(title=title, descripcion=description, price=price)
        db.session.add(product)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('create_product.html')

@app.route('/products/delete/<int:id', methods=['GET','POST'])
@login_required
def delete_product(id):
    product = Product.query.get(id)
    if product:
        db.session.delete(product)
        db.session.commit()
    return redirect(url_for('home'))
        
   
       

#run aplicacion
if __name__ == '__main__':
    app.run(debug=True)
