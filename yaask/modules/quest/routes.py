from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
import json
from yaask.modules.quest.forms import  SubmitForm, SubmitForm2, FilterForm
import math
from yaask.models import *
from yaask import app



quest = Blueprint('quest',__name__)

secret_key='hello_bhai'


@quest.route('/submit', methods=['GET', 'POST'])
@login_required
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
                question_score=0,
                comment=form1.comment1.data,
                tags=tags,
            )
            x=questiondata.question
            x=x.replace("{tex}","\[")
            x=x.replace("{/tex}","\]")
            questiondata.question=x

            db.session.add(questiondata)
            db.session.commit()
            return render_template('display_int.html', question_to_display=questiondata)
            
        if form.validate_on_submit():
            tags=request.form.getlist('select_tag')
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
                question_score=0,
                comment=form.comment.data,
                tags=tags,
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
def display():
    form= FilterForm()
    questions_to_display = Questions.query.filter().all()
    return render_template('disp_questions.html', results=questions_to_display)
    

@quest.route('/display/<string:category>')
@login_required
def categorywise(category):
    categoryList = ['math',
        'chemistry',
        'physics',
        'biology',
        'other',]
    page=request.args.get('page')
    pg=page
    if category in categoryList:
        if(page is None):
            questions_to_display = Questions.query.filter().filter( Questions.category == category ).paginate(page=1).items
            limit= math.ceil(Questions.query.filter().count()/20)
            return render_template('display.html', questions_to_display=questions_to_display, cat=category, pg=1,limit=limit)
        else:
            questions_to_display = Questions.query.filter().filter( Questions.category == category ).all()
            limit= len(questions_to_display)/20
            questions_to_display=questions_to_display[0:20]
            return render_template('display.html', questions_to_display=questions_to_display, cat=category, pg=1,limit=limit)
            page=int(page)
            page-=1
            page*=20
            questions_to_display=questions_to_display[page:page+20]
            return render_template('display.html', questions_to_display=questions_to_display, cat=category, pg=pg,limit=limit)
            
    else:
        questions_to_display = Questions.query.filter().all()
        flash('Please enter a url where the category is any one of' + str(categoryList))
        return redirect(url_for('display', questions_to_display=questions_to_display))

@quest.route('/editquestions', methods=['GET', 'POST'])
@login_required
def editquestions():
    try:
        qid=request.args.get('qid')
        print (qid)
        delet=Questions.query.filter(Questions.questionid==qid).one()
        db.session.delete(delet)
        db.session.commit()
        questions_to_display = Questions.query.filter(Questions.creatorid == str(current_user.id)).all()
        return render_template('individual_questions.html', questions_to_display=questions_to_display)
    except:
        questions_to_display = Questions.query.filter(Questions.creatorid == str(current_user.id)).all()
        return render_template('individual_questions.html', questions_to_display=questions_to_display)


