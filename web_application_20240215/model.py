from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask

#### define model ####

db = SQLAlchemy()


project_has_gene = db.Table("project_has_gene", 
                            db.Column("project_id", db.Integer, db.ForeignKey("projects.id")),
                            db.Column("gene_id", db.Integer, db.ForeignKey("gene.id"))
                            )

gene_has_database = db.Table("gene_has_database",
                             db.Column("gene_id", db.Integer, db.ForeignKey("gene.id")),
                             db.Column("database_id", db.Integer, db.ForeignKey("database.id")),
                             db.Column("gene_in_db", db.String(255), nullable=False),
                             db.Column("url", db.String(255), nullable=False)
                             )

class User(db.Model, UserMixin): #no entiendo el user mixin
    id = db.Column(db.Integer, primary_key=True, unique=True)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable=False)

    user_projects= db.relationship("Projects", backref="User")
    
class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    name = db.Column(db.String(40), nullable=False)
    privileges = db.Column(db.String(255), nullable=False)
    
    user = db.relationship("User", backref="Role")

class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    project_name = db.Column(db.String(255),nullable=False, unique=False)
    description = db.Column(db.String(255), nullable=True)
    user = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    genes_projects = db.relationship("Gene", secondary=project_has_gene, backref="Projects")

class Gene(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    gene_name = db.Column(db.String(40), nullable=False)
    species = db.Column(db.String(40), nullable=False)

    gene_database = db.relationship("Database", secondary=gene_has_database, backref="Gene")
    
class Database(db.Model):
    id = db.Column(db.Integer, primary_key=True, unique=True)
    db_name = db.Column(db.String(255), nullable=False)
    url_prefix = db.Column(db.String(255), nullable=False)


