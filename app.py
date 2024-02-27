from flask import Flask, render_template, url_for, redirect, request 
from model import *
from forms import SignUpForm, LoginForm, SearchForm
import pymysql
from apis import *
from sqlalchemy import select, and_ 
from flask import flash, redirect, url_for
from flask_bcrypt import bcrypt
from flask_login import login_user, current_user, LoginManager, login_required

app = Flask(__name__)


# Set the secret key
app.secret_key = 'your-secret-key'

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/hlh'

# Configure the SQLAlchemy instance with the Flask app
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, (int(user_id)))

@app.route('/')
def index():
    
    # Get a list of all gene names from the Gene table
    
    gene_names = [gene.gene_name for gene in Gene.query.all()]
    
    return render_template('index.html', gene_names=gene_names)



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # add user registration logic here
        pass
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginerror = None
    form = LoginForm()  # Create the form instance before the conditional statement
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if (form_password := form.password.data):
                if bcrypt.checkpw(form_password.encode('utf8'), user.password):
                    login_user(user)
                    return redirect(url_for('userspace'))
        loginerror = 'Invalid email or password'
    return render_template('login.html', form=form, loginerror=loginerror)
                                    


@app.route('/search' , methods = ['POST','GET'])
def search():


    gene_input = request.form.get('gene_name')
    species = request.form.get('species')

    # Query the Gene table for a gene with the given name and species
    gene = Gene.query.filter_by(gene_name=gene_input, species=species).first()

    # Get the Database instance for Uniprot
    uniprot = Database.query.filter_by(db_name='Uniprot').first()

 
        
    if gene and uniprot:
        
        # Create a select statement for the gene_has_database table
        stmt = select(gene_has_database.c.gene_in_db).where(and_(gene_has_database.c.gene_id == gene.id, gene_has_database.c.database_id == uniprot.id))

        # Execute the select statement and fetch the results
        results = db.session.execute(stmt).fetchall()

        # Print the gene_in_db values
        for result in results:
            uniprot_accession_code = result[0]
        

        sequence = get_sequence(uniprot_accession_code=uniprot_accession_code)
        

        return render_template('search.html', gene_input=gene.gene_name, uniprot_accession_code=uniprot_accession_code , species = gene.species, sequence = sequence)


    else:
        
        return render_template(index.html)


# Call the create_app function and run the app


if __name__ == "__main__":
    app.run(debug=True)