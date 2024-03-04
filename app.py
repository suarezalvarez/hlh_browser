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
        if (form_password := form.password.data):
            hashed_password = bcrypt.hashpw(form_password.encode('utf8'), bcrypt.gensalt())
            default_role = Role.query.filter_by(name='user').first()
            new_user = User(email=form.email.data, password=hashed_password, role_id=default_role.id)
            db.session.add(new_user)
            
            db.session.commit()
            return redirect(url_for('userspace'))
      
    return render_template('signup.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    loginerror = None
    form = LoginForm()  # Create the form instance before the conditional statement
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            if (form_password := form.password.data):
                if bcrypt.checkpw(form_password.encode('utf8'), user.password.encode('utf8')):
                    login_user(user)
                    return redirect(url_for('userspace'))
        loginerror = 'Invalid email or password'
    return render_template('login.html', form=form, loginerror=loginerror)
                                    
@app.route('/userspace', methods=['GET', 'POST'])
@login_required
def userspace():
    user = User.query.get(int(current_user.id))
    form = SearchForm()
    #falta un trozo, cuando queramos meter cosas lo ponemos
    return render_template('userspace.html', form=form, user_email=user.email)



@app.route('/search' , methods = ['POST','GET'])
def search():


    gene_input = request.form.get('gene_name')

    species = request.form.get('species')


    
    # Query the Gene table for a gene with the given name and species
    gene = Gene.query.filter_by(gene_name=gene_input, species=species).first()

    # Get the Database instance for NCBI

    ncbi = Database.query.filter_by(db_name='NCBI').first()

    # Get the Database instance for Uniprot
    uniprot = Database.query.filter_by(db_name='Uniprot').first()

    # Get the Database instance for PDB
    pdb = Database.query.filter_by(db_name='PDB').first()


    if gene and uniprot:


        #######################################
        #### NUCLEOTIDE SEQUENCE FROM NCBI ####
        #######################################

        stmt = select(gene_has_database.c.gene_in_db).where(and_(gene_has_database.c.gene_id == gene.id, gene_has_database.c.database_id == ncbi.id))

        # Execute the select statement and fetch the results

        results = db.session.execute(stmt).fetchall()

        # fetch info 

        for result in results:
            nuc_seq = result[0]

        nuc_seq = fetch_nucleotide_sequence(nuc_seq)


        #######################################
        #### PROTEIN SEQUENCE FROM UNIPROT ####
        #######################################
        # Create a select statement for the gene_has_database table
        stmt = select(gene_has_database.c.gene_in_db).where(and_(gene_has_database.c.gene_id == gene.id, gene_has_database.c.database_id == uniprot.id))

        # Execute the select statement and fetch the results
        results = db.session.execute(stmt).fetchall()

        # fetch sequence from uniprot_accession_code
        for result in results:
            uniprot_accession_code = result[0]
        

        sequence = get_sequence(uniprot_accession_code=uniprot_accession_code)
        

        ####################################
        #### PROTEIN STRUCTURE FROM PDB ####
        ####################################

        # Create a select statement for the gene_has_database table
        stmt = select(gene_has_database.c.gene_in_db).where(and_(gene_has_database.c.gene_id == gene.id, gene_has_database.c.database_id == pdb.id))

        # Execute the select statement and fetch the results
        results = db.session.execute(stmt).fetchall()

        # Print the gene_in_db values
        for result in results:
            pdb_accession_code = result[0]

        
        

        ####################################
        ####      FUNCTION UNIPROT      ####  
        ####################################
       
        function = get_function(uniprot_accession_code)


        ##################################
        ####     NETWORK STRING      #####
        ##################################


        network = get_network(uniprot_accession_code)


        return render_template('search.html', 
                               gene_input=gene.gene_name, 
                               uniprot_accession_code=uniprot_accession_code , 
                               species = gene.species, 
                               nuc_seq = nuc_seq,
                               sequence = sequence,
                               pdb = pdb_accession_code,
                               function = function,
                               network_image = network)


    else:
        
        return render_template(index.html)


# Call the create_app function and run the app


if __name__ == "__main__":
    app.run(debug=True)