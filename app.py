from flask import Flask, render_template, url_for, redirect, request
from model import db
from forms import SignUpForm, LoginForm, SearchForm

import pymysql

app = Flask(__name__)

# Set the secret key
app.secret_key = 'your-secret-key'

# Set the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:1234@localhost:3306/hlh'

# Configure the SQLAlchemy instance with the Flask app
db.init_app(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        # add user registration logic here
        pass
    return render_template('signup.html', form=form)

@app.route('/search' , methods = ['POST','GET'])
def search():
    gene_input = request.form.get('gene_name')
    species = request.form.get('species')
    return render_template('search.html' , gene_input = gene_input, species = species)

@app.route('/sequence/<uniprot_accession_code>')
def get_sequence(uniprot_accession_code):
    url = f'https://rest.uniprot.org/uniprotkb/{uniprot_accession_code}.fasta'
    response = requests.get(url)
    if response.status_code == 200:
        sequence = response.text.strip()
        return render_template('sequence.html', sequence=sequence)
    else:
        return "Could not retrieve sequence information", 400

@app.route('/function/<uniprot_accession_code>')
def get_function(uniprot_accession_code):
    url = f'https://www.uniprot.org/uniprot/{uniprot_accession_code}.txt'
    response = requests.get(url)
    if response.status_code == 200:
        function_paragraph = ""
        hola = False
        for line in response.text.split('\n'):
            if '-!- FUNCTION' in line:
                hola = True
                line = line.replace('-!- FUNCTION:', '')
            elif '-!- SUBCELLULAR' in line:
                hola = False
            if hola:
                line = line.replace('CC   ', '')
                function_paragraph += line.strip() + " "
        return render_template('function.html', function=function_paragraph.strip())
    else:
        return "Could not retrieve function information", 400
    

@app.route('/network/<uniprot_accession_code>')
def get_network(uniprot_accession_code):
    string_api_url = "https://version-11-5.string-db.org/api"
    output_format1 = "tsv-no-header"
    output_format3 = "image"
    method1 = "get_string_ids"
    method2 = "network"

    params1 = {
        "identifiers": uniprot_accession_code,
        "limit": 1,
        "echo_query": 1,
    }

    params2 = {
        "identifiers": uniprot_accession_code,
        "add_white_nodes": 15,
        "network_flavor": "confidence",
        "caller_identity": "www.awesome_app.org"
    }

    request_url_id = "/".join([string_api_url, output_format1, method1])
    request_url_network = "/".join([string_api_url, output_format3, method2])

    results_id = requests.post(request_url_id, data=params1)
    results_network = requests.post(request_url_network, data=params2)

    string_identifier = None
    for line in results_id.text.strip().split("\n"):
        l = line.split("\t")
        input_identifier, string_identifier = l[0], l[2]

    file_name = f"{uniprot_accession_code}_network.png"
    with open(file_name, 'wb') as fh:
        fh.write(results_network.content)

    return send_file(file_name, mimetype='image/png')

@app.route('/nucleotide/<nucleotide_id>')
def fetch_nucleotide_sequence(nucleotide_id):
    api_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    params = {
        "db": "nuccore",
        "id": nucleotide_id,
        "rettype": "fasta",
        "retmode": "text"
    }
    
    response = requests.get(api_url, params=params)
    
    if response.status_code == 200:
        sequence = response.text
        return render_template('nucleotide.html', sequence=sequence)
    else:
        return "Failed to fetch nucleotide sequence from NCBI. Status code: " + str(response.status_code), 400


# Call the create_app function and run the app


if __name__ == "__main__":
    app.run(debug=True)