from app import app
import mongoengine.errors
from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from app.classes.data import Question, Reply
from app.classes.forms import QuestionForm, ReplyForm
from flask_login import login_required
import datetime as dt
from mongoengine.queryset.visitor import Q

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

        return redirect(url_for('question',questionID=newQuestion.id))

    return render_template('questionsform.html',form=form)

@app.route('/question/list')
@app.route('/questions')
@login_required
def questionList():
    questions = Question.objects()
    return render_template('questions.html',questions=questions)





@app.route('/question/<questionID>')
@login_required
def question(questionID):
    thisQuestion = Question.objects.get(id=questionID)
    theseReplies = Reply.objects(Q(question=thisQuestion) & Q(outer=True) & Q(dFromOuter=0))
    return render_template('question.html',question=thisQuestion, replies=theseReplies)

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
            modify_date = dt.datetime.utcnow
        )
        theseReplies = Reply.objects(Q(question=editQuestion) & Q(outer=True) & Q(dFromOuter=0))
        return redirect(url_for('question',questionID=questionID, replies=theseReplies))
    
    form.subject.data = editQuestion.subject
    form.content.data = editQuestion.text

    return render_template('questionsform.html',form=form)

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

@app.route('/reply/newQuestion/<questionID>', methods=['GET', 'POST'])
@login_required
def replyNewQuestion(questionID):
    question = Question.objects.get(id=questionID)
    form = ReplyForm()
    if form.validate_on_submit():
        newReply = Reply(
            author = current_user.id,
            question = questionID,
            text = form.text.data,
            dFromOuter = 0,
            outer = True
        )
        newReply.save()
        theseReplies = Reply.objects(Q(question=question) & Q(outer=True) & Q(dFromOuter=0))
        return redirect(url_for('question',questionID=question.id, replies=theseReplies))
    return render_template('replyform.html',form=form,question=question)

@app.route('/reply/newRep/<questionID>/<replyID>', methods=['GET', 'POST'])
@login_required
def replyNewRep(questionID, replyID):
    question = Question.objects.get(id=questionID)
    reply = Reply.objects.get(id=replyID)
    form = ReplyForm()
    if form.validate_on_submit():
        newReply = Reply(
            author = current_user.id,
            question = questionID,
            text = form.text.data,
            dFromOuter = reply.dFromOuter+1,
            outer = False
        )
        newReply.save()
        reply.replies.append(newReply)
        reply.save()
        return redirect(url_for('question',questionID=question.id))
    return render_template('replyform.html',form=form,question=reply)


@app.route('/reply/edit/<replyID>', methods=['GET', 'POST'])
@login_required
def replyEdit(replyID):
    editReply = Reply.objects.get(id=replyID)
    if current_user != editReply.author:
        flash("You can't edit a reply you didn't write.")
        return redirect(url_for('question',questionID=editReply.question.id))
    question = Question.objects.get(id=editReply.question.id)
    form = ReplyForm()
    if form.validate_on_submit():
        editReply.update(
            text = form.text.data,
            modify_date = dt.datetime.utcnow
        )
        theseReplies = Reply.objects(Q(question=question) & Q(outer=True) & Q(dFromOuter=0))
        return redirect(url_for('question',questionID=editReply.question.id, replies=theseReplies))

    form.text.data = editReply.text

    return render_template('replyform.html',form=form,question=question)   

@app.route('/reply/delete/<replyID>')
@login_required
def replyDelete(replyID): 
    deleteReply = Reply.objects.get(id=replyID)
    for reply in Reply.objects(Q(question=deleteReply.question) & Q(dFromOuter=(deleteReply.dFromOuter-1))):
        if reply.replies is not None and deleteReply in reply.replies:
                replyReplies = reply.replies
                reply.replies = replyReplies.remove(deleteReply)
                reply.save()
    deleteReply.delete()
    flash('The reply was deleted.')
    theseReplies = Reply.objects(Q(question=deleteReply.question) & Q(outer=True) & Q(dFromOuter=0))
    return redirect(url_for('question',questionID=deleteReply.question.id, replies=theseReplies)) 