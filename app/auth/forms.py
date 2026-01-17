from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
from app.models import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('developer', 'Developer/Designer'), ('company', 'Company')], validators=[DataRequired()])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class CompanyProfileForm(FlaskForm):
    company_name = StringField('Company Name', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Company Description')
    website = StringField('Website URL', validators=[Length(max=200)])
    industry = StringField('Industry', validators=[Length(max=100)])
    size = SelectField('Company Size', choices=[
        ('1-10', '1-10 employees'),
        ('11-50', '11-50 employees'),
        ('51-200', '51-200 employees'),
        ('201-1000', '201-1000 employees'),
        ('1000+', '1000+ employees')
    ])
    location = StringField('Location', validators=[Length(max=200)])
    submit = SubmitField('Save Profile')

class DeveloperProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(max=200)])
    bio = TextAreaField('Bio')
    skills = TextAreaField('Skills (comma-separated)', validators=[DataRequired()])
    experience_level = SelectField('Experience Level', choices=[
        ('beginner', 'Beginner (0-1 years)'),
        ('intermediate', 'Intermediate (1-3 years)'),
        ('advanced', 'Advanced (3-5 years)'),
        ('expert', 'Expert (5+ years)')
    ])
    portfolio_url = StringField('Portfolio URL', validators=[Length(max=200)])
    github_url = StringField('GitHub URL', validators=[Length(max=200)])
    linkedin_url = StringField('LinkedIn URL', validators=[Length(max=200)])
    submit = SubmitField('Save Profile')