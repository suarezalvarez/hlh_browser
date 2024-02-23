from flask import Flask, render_template, url_for, redirect, request
from model import db
import pymysql

app = Flask(__name__)

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/hlh'

# Configure the SQLAlchemy instance with the Flask app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/search' , methods = ['POST','GET'])
def search():
    gene_input = request.form.get('gene_name')
    species = request.form.get('species')
    return render_template('search.html' , gene_input = gene_input)

    


# Call the create_app function and run the app



if __name__ == "__main__":
    app.run()