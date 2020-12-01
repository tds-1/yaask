from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
import json
from yaask.modules.quest.forms import  SubmitForm, SubmitForm2, FilterForm
import math
from yaask.models import *
from yaask import app
from yaask.modules.main.decorators import check_confirmed

quest = Blueprint('quest',__name__)

secret_key='hello_bhai'


@quest.route('/submit', methods=['GET', 'POST'])
@login_required
@check_confirmed
def submit():
    try:
        form = SubmitForm()
        form1= SubmitForm2()
        if form1.validate_on_submit():
            tags=request.form.getlist('select_tag')
            questiondata = Questions(
                question=form1.question1.data,
                a=-1,
                b=-1,
                c=-1,
                d=-1,
                answer=form1.answer1.data,
                creatorid=current_user.id,
                category=form1.category1.data,
                difficulty=form1.difficulty1.data,
                question_score=(int(form1.difficulty1.data))*20,
                comment=form1.comment1.data,
                tags=tags,
                attempts=50,
            )
            x=questiondata.question
            x=x.replace("{tex}","\[")
            x=x.replace("{/tex}","\]")
            questiondata.question=x

            db.session.add(questiondata)
            db.session.commit()
            return render_template('display_int.html', question_to_display=questiondata)
            
        if form.validate_on_submit():
            questiondata = Questions(
                question=form.question.data,
                a=form.a.data,
                b=form.b.data,
                c=form.c.data,
                d=form.d.data,
                answer=form.answer.data,
                creatorid=current_user.id,
                category=form.category.data,
                difficulty=form.difficulty.data,
                question_score=(int(form.difficulty.data))*20,
                comment=form.comment.data,
                tags=[form.tags.data],
                attempts=50,
            )

            x=questiondata.question
            x=x.replace("{tex}","\[")
            x=x.replace("{/tex}","\]")
            questiondata.question=x
            
            db.session.add(questiondata)
            db.session.commit()
            return render_template('display_mcq.html', question_to_display=questiondata)
        f = open("yaask/tag.txt", "r")
        x= (f.read())
        ini=0
        tag=[]
        for i in range (0,len(x)):
            if (x[i]=='\n'):
                tag.append(x[ini:i])
                ini=i+1
        tag.append(x[ini:len(x)])
        return render_template('submit.html', form=form, form1=form1, tag=tag)
    except:
        return redirect(url_for('users.login'))
    

@quest.route('/display', methods=['GET', 'POST'])
@login_required
@check_confirmed
def display():
    form= FilterForm(request.form)
    if request.method == 'GET':
        questions_to_display = Questions.query.filter().order_by(Questions.questionid.desc()).all()
        return render_template('disp_questions.html',form = form, results=questions_to_display)
    else:
        subject = form.subject.data
        topic = form.tags.data
        questions_to_display = Questions.query.filter()
        if( subject != "all"):
            questions_to_display = questions_to_display.filter(Questions.category == subject)
        if( topic != "all"):
            questions_to_display = questions_to_display.filter(Questions.tags == [topic])
        questions_to_display = questions_to_display.all()
        return render_template('disp_questions.html',form = form, results=questions_to_display)

@quest.route('/editquestion/<questionid>', methods=['GET', 'POST'])
@login_required
@check_confirmed
def editquestions(questionid):
    form = SubmitForm()
    if request.method == 'GET':
        query = Questions.query.filter(Questions.questionid == questionid).one()
        form.question.data = query.question
        form.a.data = query.a
        form.b.data = query.b
        form.c.data = query.c
        form.d.data = query.d
        form.answer.data = query.answer
        form.category.data = query.category
        form.difficulty.data = query.difficulty
        try:
            form.tags.data = query.tags[0]
        except:
            form.tags.data = ""
        
        form.comment.data = query.comment
        return render_template('editquestion.html', form = form)
    if request.method == 'POST':
        if form.validate_on_submit():
            query = Questions.query.filter(Questions.questionid == questionid).one()
            x=form.question.data
            x=x.replace("{tex}","\[")
            x=x.replace("{/tex}","\]")
            query.question = x            
            query.a = form.a.data
            query.b = form.b.data
            query.c = form.c.data
            query.d = form.d.data
            query.answer = form.answer.data
            query.comment=form.comment.data
            query.tags=[form.tags.data]
            db.session.commit()
            return redirect(url_for('main.home'))
        else:
            flash('incorrect submission')
            return render_template('editquestion.html', form = form)
