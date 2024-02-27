from model import Gene, Database, gene_has_database, project_has_gene, User,Role, db
from sqlalchemy import create_engine, MetaData, insert, select
from sqlalchemy.orm import Session
from flask import Flask # needs an active application context
from app import app
import pandas as pd




# Read the Excel file
excel_genes = pd.read_excel('data/gene_ids.xlsx', sheet_name='Sheet1' , header=0)

# Set the first column as the DataFrame index
excel_genes.set_index(excel_genes.columns[0], inplace=True)

# Convert the DataFrame to a dictionary
dict_genes = excel_genes.to_dict('index')






with app.app_context():
# Create all tables in the database and load data

    db.create_all()

    # Delete existing rows in the Database table

    db.session.query(gene_has_database).delete()
    db.session.query(Database).delete()
    db.session.query(Gene).delete()
    db.session.commit()

        
    # Create instances of Database
    uniprot = Database(id=1, db_name="UNIPROT", url_prefix="http://www.uniprot.org/uniprotkb/")
    ncbi = Database(id=2, db_name="NCBI", url_prefix="https://www.ncbi.nlm.nih.gov/gene/")
    pdb = Database(id=3, db_name="PDB", url_prefix="https://www.rcsb.org/structure/")
    
    db.session.add_all([uniprot, ncbi, pdb])

    # Commit the session to persist the instances in the database
    db.session.commit()




    gene_numeric_id = 1

    for gene_species , ids_dict in dict_genes.items():



        # Create instances of Gene
        gene_species = Gene(id = gene_numeric_id, 
                    gene_name = ids_dict['gene_name'], 
                    species = ids_dict['species']) 
        
        db.session.add(gene_species)



        # Create instances of gene_has_database
        
        # Insert data into the gene_has_database table

        
        stmt = insert(gene_has_database).values(gene_id = gene_species.id,
                                                database_id = uniprot.id, 
                                                gene_in_db = ids_dict['uniprot'], 
                                                url = uniprot.url_prefix + ids_dict['uniprot'])
        db.session.execute(stmt)

        stmt = insert(gene_has_database).values(gene_id=gene_species.id,
                                                database_id=ncbi.id, 
                                                gene_in_db = ids_dict['ncbi'], 
                                                url = ncbi.url_prefix + str(ids_dict['ncbi']))
        db.session.execute(stmt)
        
        stmt = insert(gene_has_database).values(gene_id=gene_species.id,
                                                database_id=pdb.id, 
                                                gene_in_db = ids_dict['pdb'], 
                                                url = pdb.url_prefix + str(ids_dict['pdb']))
        db.session.execute(stmt)
        # Commit the session to persist the data in the gene_has_database table
        db.session.commit()

        gene_numeric_id += 1





