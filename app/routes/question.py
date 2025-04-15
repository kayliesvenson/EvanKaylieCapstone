from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Question, Comment
from app.classes.forms import QuestionForm, CommentForm
from flask_login import login_required
import datetime as dt

@app.route('/question/new', methods=['GET', 'POST'])
@login_required
def questionNew():
    form = QuestionForm()
    if form.validate_on_submit():
        newQuestion = Question(
            subject = form.subject.data,
            content = form.content.data,
            author = current_user.id,
            modify_date = dt.datetime.utcnow
        )
        newQuestion.save()

        return redirect(url_for('question',QuestionID=newQuestion.id))

    return render_template('questionform.html',form=form)