from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,TextAreaField,FieldList
from wtforms.validators import data_required,EqualTo

class Register_form(FlaskForm):
    email=StringField('Email',validators=[data_required()])
    password=PasswordField('Password',validators=[data_required()])
    confirm_password=PasswordField('Confirm Password',validators=[data_required(),EqualTo('password')])
    submit=SubmitField()


class Login_form(FlaskForm):
    email = StringField('Email', validators=[data_required()])
    password = PasswordField('Password', validators=[data_required()])
    submit = SubmitField('Login ')


class Resume_details(FlaskForm):
    name=StringField('Name',validators=[data_required()])
    phone_no=StringField('Phone Number',validators=[data_required()])
    work_email=StringField('Email',validators=[data_required()])
    linkedIn=StringField('LinkedIn',validators=[data_required()])
    education=TextAreaField('Education',validators=[data_required()])
    skills=TextAreaField('Skills',validators=[data_required()])
    project_1=TextAreaField('Project Title-1',validators=[data_required()])
    project_2 = TextAreaField('Project Title-2', validators=[data_required()])
    submit = SubmitField('Login ')