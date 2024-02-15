import requests

def get_unipro_info_tuple(uniprot_accession_code):
    sequence = get_sequence(uniprot_accession_code)
    return uniprot_accession_code, sequence


def get_sequence(uniprot_accession_code):
    url = f'https://rest.uniprot.org/uniprotkb/stream?compressed=false&format=json&query=accession={uniprot_accession_code}&fields=sequence'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results')
        if results:
            first_result = results[0]
            sequence = first_result.get('sequence')
            if sequence:
                return sequence.get('value')

    return None

def get_organism_id(uniprot_accession_code):
    url = f'https://rest.uniprot.org/uniprotkb/stream?compressed=false&format=json&query=accession={uniprot_accession_code}&fields=organism_id'
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        results = data.get('results')
        if results:
            first_result = results[0]
            organism_id = first_result.get('organism_id')
            if organism_id:
                return organism_id.get('value')

    return None