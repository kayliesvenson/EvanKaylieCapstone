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

@app.route('/question/<questionID>')
@login_required
def question(questionID):
    thisQuestion = Question.objects.get(id=questionID)
    theseComments = Comment.objects(question=thisQuestion)
    return render_template('question.html',question=thisQuestion,comments=theseComments)

@app.route('/question/list')
@app.route('/questions')
@login_required
def questionList():
    questions = Question.objects()
    return render_template('questions.html',questions=questions)

@app.route('/question/edit/<questionID>', methods=['GET', 'POST'])
@login_required
def questionEdit(questionID):
    editQuestion = Question.objects.get(id=questionID)
    if current_user != editQuestion.author:
        flash("You can't edit a question you don't own.")
        return redirect(url_for('question',questionID=questionID))
    form = QuestionForm()
    if form.validate_on_submit():
        editQuestion.update(
            subject = form.subject.data,
            content = form.content.data,
            tag = form.tag.data,
            modify_date = dt.datetime.utcnow
        )
        return redirect(url_for('question',questionID=questionID))
    
    form.subject.data = editQuestion.subject
    form.content.data = editQuestion.content
    form.tag.data = editQuestion.tag
    return render_template('questionform.html',form=form)

@app.route('/question/delete/<questionID>')
@login_required
def questionDelete(questionID):
    deleteQuestion = Question.objects.get(id=questionID)
    if current_user == deleteQuestion.author:
        deleteQuestion.delete()
        flash('The question was deleted.')
    else:
        flash("You can't delete a question you don't own.")
    questions = Question.objects()  
    return render_template('questions.html',questions=questions)