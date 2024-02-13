from model import Gene, Database, gene_has_database, project_has_gene, User,Role, db
from sqlalchemy import create_engine, MetaData, insert, select
from sqlalchemy.orm import Session
from flask import Flask # needs an active application context
from app import create_app

app = create_app()

# Create all tables in the database and load data
with app.app_context():
    db.create_all()

    # Delete existing rows in the Database table
    db.session.query(gene_has_database).delete()
    db.session.query(Database).delete()
    db.session.query(Gene).delete()
    db.session.commit()

    
    # Create instances of Gene
    MYOD1_human = Gene(id=1, gene_name="myod1", species="human")
    db.session.add(MYOD1_human)

    MYOD1_mouse = Gene(id=2, gene_name="myod1", species="mouse")
    db.session.add(MYOD1_mouse)
    
    # Create instances of Database
    UNIPROT = Database(id=1, db_name="UNIPROT", url_prefix="http://www.uniprot.org/uniprotkb/")
    NCBI = Database(id=2, db_name="NCBI", url_prefix="https://www.ncbi.nlm.nih.gov/gene/")
    db.session.add_all([UNIPROT, NCBI])



    # Commit the session to persist the instances in the database
    db.session.commit()

    # Create instances of gene_has_database
    
    # Insert data into the gene_has_database table
    stmt = insert(gene_has_database).values(gene_id=MYOD1_human.id, database_id=UNIPROT.id, gene_in_db="MYOD1", url="http://www.uniprot.org/uniprotkb/MYOD1")
    db.session.execute(stmt)

    stmt = insert(gene_has_database).values(gene_id=MYOD1_human.id, database_id=NCBI.id, gene_in_db="MYOD1", url="https://www.ncbi.nlm.nih.gov/gene/MYOD1")
    db.session.execute(stmt)

    stmt = insert(gene_has_database).values(gene_id=MYOD1_mouse.id, database_id=UNIPROT.id, gene_in_db="MYOD1", url="http://www.uniprot.org/uniprotkb/MYOD1")
    db.session.execute(stmt)
    
    stmt = insert(gene_has_database).values(gene_id=MYOD1_mouse.id, database_id=NCBI.id, gene_in_db="MYOD1", url="https://www.ncbi.nlm.nih.gov/gene/MYOD1")
    db.session.execute(stmt)

    # Commit the session to persist the data in the gene_has_database table
    db.session.commit()






