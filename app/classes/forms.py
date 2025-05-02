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

class ReplyForm(FlaskForm):
    text = TextAreaField('Reply', validators=[DataRequired()])
    submit = SubmitField('Post')