# This file is where data entry forms are created. Forms are placed on templates 
# and users fill them out.  Each form is an instance of a class. Forms are managed by the 
# Flask-WTForms library.

from flask_wtf import FlaskForm
import mongoengine.errors
from wtforms.validators import URL, Email, DataRequired, NumberRange
from wtforms.validators import URL, Email, DataRequired
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, SelectField, FileField, BooleanField, URLField

class ProfileForm(FlaskForm):
    fname = StringField('First Name', validators=[DataRequired()])
    lname = StringField('Last Name', validators=[DataRequired()]) 
    image = FileField("Image") 
    submit = SubmitField('Post')
    role = SelectField('Role',choices=[("Administrator","Administrator"),("User","User")])
    age = IntegerField('Age')

class BlogForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Blog', validators=[DataRequired()])
    tag = StringField('Tag', validators=[DataRequired()])
    submit = SubmitField('Blog')

class QuestionForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    content = TextAreaField('Question', validators=[DataRequired()])
    submit = SubmitField('Question')

class CommentForm(FlaskForm):
    content = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Comment')

class ClinicForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    streetAddress = StringField('Address', validators=[DataRequired()])
    city = StringField('City', validators=[DataRequired()])
    state = StringField('State', validators=[DataRequired()])
    zipcode = StringField('Zipcode',validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    submit = SubmitField('Submit')


class ReviewForm(FlaskForm):
    name = SelectField('Hospital Name',choices=[("Wilma Chan Highland Hospital","Wilma Chan Highland Hospital"),("Alta Bates Summit Medical Center","Alta Bates Summit Medical Center"), ("UCSF Benioff Children's Hospital", "UCSF Benioff Children's Hospital"), ("Kaiser Permanente", "Kaiser Permanente"), ("Fairmont Rehabilitation & Wellness", "Fairmont Rehabilitation & Wellness"), ("John George Psychiatric Pavilion", "John George Psychiatric Pavilion"), ("Alameda Hospital", "Alameda Hospital"), ("San Leandro Hospital","San Leandro Hospital")])
    text = TextAreaField('Write your Review', validators=[DataRequired()])
    subject = SelectField('Experiences',choices=[("Patient Care", "Patient Care"), ("Visitor","Visitor"),("Waiting Duration","Waiting Duration"), ("Internship/Leanring Programs", "Internship/Leanring Programs"), ("Volunteer", "Volunteer"), ("Patient", "Patient"), ("Hospitality", "Hospitality"), ("Other","Other")])
    rating = IntegerField('Rate your experience: 0 is terrible, 10 is amazing', validators=[NumberRange(min=0,max=10, message="Enter a number between 0 and 10.")])
    submit = SubmitField('Post Review')

class ReplyForm(FlaskForm):
    text = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Post')