
import requests
from flask import Flask, request, send_file
import base64

def get_sequence(uniprot_accession_code):
    url = f'https://rest.uniprot.org/uniprotkb/{uniprot_accession_code}.fasta'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "Could not retrieve sequence information", 400


def get_function(uniprot_accession_code):
    url = f'https://rest.uniprot.org/uniprotkb/{uniprot_accession_code}.txt'
    response = requests.get(url)
    if response.status_code == 200:
        entry_text = response.text
        # Simple parsing for Function section - might need adjustment based on actual text structure
        start_marker = "CC   -!- FUNCTION:"
        end_marker = "CC   -!-"
        start_index = entry_text.find(start_marker)
        if start_index != -1:
            end_index = entry_text.find(end_marker, start_index + len(start_marker))
            function_text = entry_text[start_index:end_index].strip()
            return function_text.replace("CC       ", "").replace(start_marker, "").strip()
        else:
            return "Function information not found."
    else:
        return "Could not retrieve function information", 400
    


def get_network(uniprot_accession_code):
    string_api_url = "https://version-11-5.string-db.org/api"
    #output_format1 = "tsv-no-header"
    output_format3 = "image"
    #method1 = "get_string_ids"
    method2 = "network"

    # params1 = {
    #     "identifiers": uniprot_accession_code,
    #     "limit": 1,
    #     "echo_query": 1,
    # }

    params2 = {
        "identifiers": uniprot_accession_code,
        "add_white_nodes": 15,
        "network_flavor": "confidence",
        "caller_identity": "www.awesome_app.org"
    }

    #request_url_id = "/".join([string_api_url, output_format1, method1])
    request_url_network = "/".join([string_api_url, output_format3, method2])

    #results_id = requests.post(request_url_id, data=params1)
    results_network = requests.post(request_url_network, data=params2)

    string_identifier = None
    # for line in results_id.text.strip().split("\n"):
    #     l = line.split("\t")
    #     input_identifier, string_identifier = l[0], l[2]

    # file_name = f"{uniprot_accession_code}_network.png"
    # with open(file_name, 'wb') as fh:
    #     fh.write(results_network.content)

    # return send_file(file_name, mimetype='image/png')


    base64_image = base64.b64encode(results_network.content).decode('utf-8')
    return base64_image


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
        return response.text
    else:
        return "Failed to fetch nucleotide sequence from NCBI. Status code: " + str(response.status_code), 400
