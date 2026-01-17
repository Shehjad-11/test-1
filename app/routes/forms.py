from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, DateTimeField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, NumberRange, URL, Optional
from datetime import datetime, timedelta

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Project Description', validators=[DataRequired()])
    required_skills = TextAreaField('Required Skills (comma-separated)', validators=[DataRequired()])
    deadline = DateTimeField('Deadline', validators=[DataRequired()], format='%Y-%m-%dT%H:%M')
    winner_reward = FloatField('Winner Reward ($)', validators=[DataRequired(), NumberRange(min=0)])
    participation_reward = FloatField('Participation Reward ($)', validators=[NumberRange(min=0)], default=0)
    max_shortlist = IntegerField('Maximum Shortlisted Candidates', validators=[DataRequired(), NumberRange(min=1, max=50)], default=10)
    submit = SubmitField('Post Project')

class ApplicationForm(FlaskForm):
    cover_letter = TextAreaField('Cover Letter', validators=[DataRequired(), Length(max=1000)])
    submit = SubmitField('Apply to Project')

class SubmissionForm(FlaskForm):
    github_url = StringField('GitHub Repository URL', validators=[Optional(), URL()])
    demo_url = StringField('Live Demo URL', validators=[Optional(), URL()])
    figma_url = StringField('Figma/Design URL', validators=[Optional(), URL()])
    description = TextAreaField('Submission Description', validators=[DataRequired()])
    submit = SubmitField('Submit Work')

class MessageForm(FlaskForm):
    content = TextAreaField('Message', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Send Message')

class FeedbackForm(FlaskForm):
    score = IntegerField('Score (1-10)', validators=[DataRequired(), NumberRange(min=1, max=10)])
    feedback = TextAreaField('Feedback', validators=[DataRequired()])
    submit = SubmitField('Submit Feedback')