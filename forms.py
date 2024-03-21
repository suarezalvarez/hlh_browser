from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Email, InputRequired, Length, ValidationError
from model import project_has_gene, gene_has_database,User,Role,Projects,Gene,Database


class SignUpForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired(), Length(min=1, max=80)],
                       render_kw={"placeholder": "Your name"})
    surname = StringField('Surname', validators=[InputRequired(), Length(min=1, max=80)],
                          render_kw={"placeholder": "Your surname"})
    email = StringField(validators=[Email(), InputRequired(), Length(min=1, max=80)],
                        render_kw={"placeholder": "name@example.com"})

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("This email address is already in use please choose different one.")

    password = PasswordField(validators=[InputRequired(), Length(min=1, max=80)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    email = StringField(validators=[Email(), InputRequired(), Length(min=1, max=80)],
                        render_kw={"placeholder": "name@example.com"})

    password = PasswordField(validators=[InputRequired(), Length(min=1, max=80)],
                             render_kw={"placeholder": "Password"})

    submit = SubmitField("Log in")


class SearchForm(FlaskForm):
    search = StringField(validators=[InputRequired(), Length(min=1, max=10)], render_kw={"placeholder": "ex: ASCL1"})

    submit = SubmitField("Add Sequence")

class ProjectForm(FlaskForm):
    project_name = StringField(validators=[InputRequired(), Length(min=1, max=80)],
                              render_kw={"placeholder": "Project name"})
    description = StringField(validators=[Length(min=1, max=2000)])

    submit = SubmitField("Create Project")