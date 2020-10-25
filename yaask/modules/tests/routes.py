from flask import Blueprint
from flask import Flask, render_template, url_for, request, session, redirect, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, user_logged_in
from flask_session import Session
from flask_weasyprint import HTML, render_pdf
import json
from yaask.modules.tests.forms import  QuizForm, GenerateForm, RandomTest, UploadForm, TestForm
import operator
import math
from collections import OrderedDict 
from yaask.models import *
from yaask import app
from coolname import generate_slug
import random
from yaask.modules.tests.utils import choosequestions
from datetime import timedelta, datetime
from sqlalchemy.orm.attributes import QueryableAttribute

tests = Blueprint('tests',__name__)

secret_key='hello_bhai'


@app.route('/test', methods=['GET','POST'])
@login_required
def test():
    categoryList = ['math',
        'chemistry',
        'physics',
        'biology',
        'other',]
    #To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
    form=RandomTest()
    
    if request.method == 'GET':
        db.session.commit()
        questions_to_display = Questions.query.filter().all()
        return render_template('test.html',form=form, questions_to_display=questions_to_display, categoryList=categoryList)

    if request.method == 'POST':		
        questions_to_display = Questions.query.filter().all()
        selected=[]
        for question in questions_to_display:
            check=request.form.get(str(question.questionid))
            if check=="checked":
                selected.append(question.questionid)
        
        category=form.subject.data
        avg=form.avg_difficulty.data
        n=form.number_of_questions.data
        
        temp=Questions.query.filter( ~Questions.questionid.in_(selected)).filter(Questions.category==category).all()
        arr=[]
        for x in temp:
            arr.append((int(x.difficulty), x.question_score, x.questionid))
    
        random_questions=choosequestions(arr, avg, n)
        for question in random_questions:
            selected.append(question[2])
        #update score
        questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
        for x in questions_to_display:
            x.question_score=x.question_score+1
            db.session.commit()

        testdata = Test(
            creatorid=current_user.id,
            selected=selected,
        )
        db.session.add(testdata)
        db.session.commit()
        session['selected']=selected
        session['testid']=testdata.testid
        
        return redirect(url_for('generated_test'))



@app.route('/preview-test', methods=['GET','POST'])
@login_required
def preview_test():
    if request.method=='GET':
        id=current_user.id
        test= Test.query.filter(Test.creatorid==id).all()
        return render_template ("preview-test.html",test=test)

    if request.method=='POST':
        try:
            x=request.form['button']
            session['testid']=x
            return redirect(url_for('generated_test'))

        except:
            x=request.form['delete']
            delet=Test.query.filter(Test.testid==x).one()
            db.session.delete(delet)
            db.session.commit()
            return redirect(url_for('preview_test'))
        


@app.route('/generated_test', methods=['GET','POST'])
@login_required
def generated_test():
    testid=session.get('testid')
    z=Test.query.filter(Test.testid==testid).one()
    selected=z.selected
    form = GenerateForm()
    return render_template('chose_test.html',testid=testid,form=form)


@app.route('/online_test', methods=['GET','POST'])
@login_required
def online_test():
    if request.method=='GET':
        id=request.args.get('id')
        selected=Test.query.filter(Test.testid==id).one()
        selected=selected.selected
        questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
        return render_template("online_test.html",questions_to_display=questions_to_display,id=id)
    if request.method=='POST':
        id=request.args.get('id')
        selected=Test.query.filter(Test.testid==id).one()
        selected=selected.selected
        score=0
        questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
        quest={}
        for x in selected:
            x=str(x)
            z=request.form[x]

            answer=Questions.query.filter(Questions.questionid==x).one()
            ans=answer.answer
            
            if ((answer.a=='-1') and (answer.b=='-1') and (answer.c=='-1') and (answer.d=='-1')):
                try:
                    z=str(int(float(z)))
                except:
                    z=""
                ans=str(int(float(ans)))
                if(len(z)==0):
                    quest[answer]='N'
                    pass
                elif (z==ans):
                    quest[answer]='C'
                    score=score+4
                else:
                    quest[answer]='W'
                    score=score-1
        
            else:
                if(z=='N'):
                    quest[answer]='N'
                    pass
                elif (z==ans):
                    quest[answer]='C'
                    score=score+4
                else:
                    quest[answer]='W'
                    score=score-1
        
        return  render_template('result.html',score=score,questions_to_display=quest)

@app.route('/print_test', methods=['GET','POST'])
@login_required
def print_test():
    selected=session.get('selected')
    questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
    form= GenerateForm()
    name=form.name.data.upper()
    time=form.time.data
    institution=form.institution.data.upper()
    html= render_template("generate.html",questions_to_display=questions_to_display,name=name, time=time, institution=institution)
    return render_pdf(HTML(string=html))



@app.route('/<username>/create-test', methods = ['GET', 'POST'])
@login_required
def create_test_info(username):
    if username == current_user.username and current_user.role == 'teacher':
        form = UploadForm()
        if request.method == 'POST':
            try:
                start = str(form.start_date.data) + " " + str(form.start_time.data)
                end = str(form.end_date.data) + " " + str(form.end_time.data)
                start = datetime.strptime(start , "%Y-%m-%d %H:%M:%S")- timedelta(hours=5, minutes=30)
                start = str(start)
                end = datetime.strptime(end , "%Y-%m-%d %H:%M:%S")-  timedelta(hours=5, minutes=30)
                end = str(end)
                
                test_info =  Test_info(
                    creatorid = current_user.id,
                    subject = form.subject.data,
                    topic = form.topic.data,
                    start_time = start,
                    end_time = end,
                    show_result = form.show_result.data,
                    neg_mark = form.neg_mark.data,
                    duration = int(form.duration.data)*60,
                    password = form.password.data,
                    type = 0,
                )
                
                db.session.add(test_info)
                db.session.commit()
                test_id = test_info.testid
                flash(f'Test ID: {test_id}', 'success')       
                return redirect(url_for('create_test', username=current_user.username, testid=test_id))
            except:
                flash("all fields are required", 'danger')
                return render_template('create_test.html' , form = form)
        return render_template('create_test.html' , form = form)
    else:
        return ("you are not authorized to access this page")


@app.route('/quest', methods = ['POST'])
def all_quest():
    if request.method == "POST":
        questions_to_display = Questions.query.filter().order_by(Questions.created_date.desc()).all()
        ques = []
        for question_to_display in questions_to_display:
            q={}
            q['question']=question_to_display.question
            q['question_id']=question_to_display.questionid
            q['a']=question_to_display.a
            q['b']=question_to_display.b
            q['c']=question_to_display.c
            q['d']=question_to_display.d
            q['subject']=question_to_display.category
            q['explaination']=question_to_display.comment
            q['answer']=question_to_display.answer
            try:
                q['topic']=question_to_display.tags[0]
            except:
                q['topic']=""
            ques.append(q) 
        return json.dumps(ques)
    return ('', 204)


@app.route('/<username>/create-test/<testid>', methods = ['GET', 'POST'])
@login_required
def create_test(username, testid):
    if username == current_user.username and current_user.role == 'teacher':
        categoryList = [
            'biology',]
        #To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
        form=RandomTest(request.form)

        if request.method == 'GET':
            data = {'question':'' , 'questionid': '', 'a': "", 'b': "",'c': "",'d': "" ,'comment':''}
            return render_template('test.html' ,**data, form =form)

        if request.method == 'POST':
            selected = []
            try:
                subject = form.subject.data
                number = form.number_of_questions.data
                tag = form.topic.data
                tag = [tag]
                questions_to_display = Questions.query.filter(Questions.category== subject).order_by(Questions.questionid.asc())
                c=0
                for x in questions_to_display:
                    if x.tags==tag:
                        selected.append(x.questionid)
                        c+=1
                        if (c==number):
                            break
            except:            
                questions_to_display = Questions.query.filter().all()
                for question in questions_to_display:
                    check=request.form.get(str(question.questionid))
                    if check=="checked":
                        selected.append(question.questionid)
            questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
            for x in questions_to_display:
                x.question_score=x.question_score+1
                db.session.commit()
            testdata = Test(
                testid = testid,
                selected=selected
            )
            db.session.add(testdata)
            db.session.commit()
            return redirect(url_for('dashboard'))
    else:
        return ("you are not authorized to access this page")

    
@app.route('/<username>/tests-created/<testid>/questions', methods = ['POST','GET'])
@login_required
def questions(username, testid):
    if username == current_user.username:
        try:
            results = Test.query.filter(Test.testid == testid).one()
            results = results.selected
            questions_to_display = Questions.query.filter( Questions.questionid.in_(results) ).all()
        except:
            questions_to_display={}
        return render_template('disp_questions.html', results=questions_to_display)
    else:
        return redirect(url_for('dashboard'))
     

@app.route('/<username>/tests-created')
@login_required
def tests_created(username):
    if username == current_user.username :
        results = Test_info.query.filter(Test_info.creatorid == str(current_user.id)).all()
        return render_template('tests_created.html', tests=results)
    else:
        return redirect(url_for('dashboard'))


@app.route("/give-test", methods = ['GET', 'POST'])
@login_required
def give_test_auth():
    global duration, marked_ans	
    marked_ans = "{}"
    form = TestForm(request.form)
    if request.method == 'POST' and form.validate():
        test_id = form.test_id.data
        password_candidate = form.password.data
        results = Test_info.query.filter(Test_info.testid == test_id).all()
        if len(results) > 0:
            data = results[0]
            password = data.password
            duration = int(data.duration)
            start = str(data.start_time)
            end = str(data.end_time)
            if password == password_candidate:
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
                if (datetime.strptime(start,"%Y-%m-%d %H:%M:%S") < now) and (datetime.strptime(end,"%Y-%m-%d %H:%M:%S") > now):
                    results = Student_test_info.query.filter(Student_test_info.username == current_user.username).filter(Student_test_info.testid == test_id).all()
                    if len(results)>0 :
                        results = results[0]
                        is_completed = results.completed
                        if is_completed == False:
                            time_left = max(0, duration - (now-datetime.strptime(results.time_started,"%Y-%m-%d %H:%M:%S")).total_seconds())
                            if time_left <= duration:
                                duration = time_left
                                results = Students.query.filter(Students.userid == str(current_user.id)).filter(Students.testid == test_id).all()
                                marked_ans = {}
                                if len(results) > 0:
                                    for row in results:
                                        marked_ans[row.quid] = row.ans
                                marked_ans = json.dumps(marked_ans)
                        else:
                            flash('Test already given', 'success')
                            return redirect(url_for('give_test_auth'))
                    else:
                        student_test_info_data = Student_test_info(
                            username= current_user.username,
                            testid = test_id,
                            time_started = now,
                            completed = False,
                            time_taken = [],
                        )
                        db.session.add(student_test_info_data)
                        db.session.commit()
                        
                        results = Student_test_info.query.filter(Student_test_info.username == current_user.username).filter(Student_test_info.testid == test_id).all()
                        if len(results)>0 :
                            results = results[0]
                            is_completed = results.completed
                            if is_completed == False:
                                time_left = max(0,duration -( now-datetime.strptime(results.time_started,"%Y-%m-%d %H:%M:%S")).total_seconds())

                                if time_left <= duration:
                                    duration = time_left
                                    results = Students.query.filter(Students.userid == str(current_user.id)).filter(Students.testid == test_id).all()
                                    marked_ans = {}
                                    if len(results) > 0:
                                        for row in results:
                                            marked_ans[row['qid']] = row.ans
                                    marked_ans = json.dumps(marked_ans)
                        
                else:
                    if datetime.strptime(start,"%Y-%m-%d %H:%M:%S") > now:
                        flash(f'Test start time is {start}', 'danger')
                    else:
                        flash(f'Test has ended', 'danger')
                    return redirect(url_for('give_test_auth'))
                return redirect(url_for('test_portal' , testid = test_id))
            else:
                flash('Invalid password', 'danger')
                return redirect(url_for('give_test_auth'))
        flash('Invalid testid', 'danger')
        return redirect(url_for('give_test_auth'))
        cur.close()
    return render_template('give_test.html', form = form)

@app.route('/give-test/<testid>', methods=['GET','POST'])
@login_required
def test_portal(testid):
    global duration,marked_ans
    if request.method == 'GET':
        try:
            now = datetime.now()
            now = now.strftime("%Y-%m-%d %H:%M:%S")
            now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
            info = Student_test_info.query.filter(Student_test_info.testid == testid).filter(Student_test_info.username == current_user.username).one()
            time_left = max(0,duration - ( now-datetime.strptime(info.time_started,"%Y-%m-%d %H:%M:%S")).total_seconds())
            data = {'duration': time_left, 'marks': '', 'q': '', 'a': "", 'b':"",'c':"",'d':"" }
            return render_template('quiz.html' ,**data, answers=marked_ans)
        except:
            return redirect(url_for('give_test_auth'))
    else:
        flag = request.form['flag']
        if flag=='mark':
            qid = request.form['qid']
            ans = request.form['ans']
            try:
                marked_ans = eval (marked_ans)
            except:
                marked_ans = "{}"
                marked_ans = eval (marked_ans)
            marked_ans[qid]=ans
            marked_ans = json.dumps(marked_ans)
            results = Students.query.filter(Students.testid== testid).filter(Students.quid== qid).filter(Students.userid== str(current_user.id)).all()
            if len(results) == 0:
                studentdata = Students(
                    ans= ans,
                    testid=testid,
                    quid = qid,
                    userid = current_user.id,
                )
                db.session.add(studentdata)
                db.session.commit()
            else:
                studentdata=Students.query.filter(Students.userid== str(current_user.id)).filter(Students.testid== testid).filter(Students.quid== qid).one()
                studentdata.ans=ans
                db.session.commit()
        elif flag=='close':
            time_taken = request.form.getlist('time_taken[]')
            if(len(time_taken)!=0):
                info = Student_test_info.query.filter(Student_test_info.username==current_user.username).filter(Student_test_info.testid == testid).one()
                info.time_taken= time_taken
                db.session.commit()
        else:
            time_taken = request.form.getlist('time_taken[]')
            info = Student_test_info.query.filter(Student_test_info.username==current_user.username).filter(Student_test_info.testid == testid).one()
            info.time_left=0
            info.completed= True
            info.time_taken= time_taken
            db.session.commit()
            randid = Test_info.query.filter(Test_info.testid == testid).one()
            if randid.type == 1:
                temp = Random_test_id.query.filter(Random_test_id.student_id == current_user.id).filter(Random_test_id.subject == randid.subject).filter(Random_test_id.topic == randid.topic).one()
                tid = temp.id
                qlist = Test.query.filter(Test.testid == testid).one()
                qlist = qlist.selected
                for i in range(0,len(qlist)):
                    quest = qlist[i]
                    rst = Random_test_question.query.filter(Random_test_question.question_id == quest).filter(Random_test_question.random_test_id == tid).one()
                    time = time_taken[i]
                    speed = 1
                    diff = 1
                    if(int(time)<=20):
                        speed = 1
                    elif(int(time)>=35):
                        speed = 3
                    else:
                        speed = 2

                    try:                    
                        s = Students.query.filter(Students.testid == testid).filter(Students.userid == current_user.id).filter(Students.quid == quest).one()
                        t = Questions.query.filter(Questions.questionid == quest).one()
                        if (s.ans == t.answer):
                            diff = 1
                        else:
                            diff = 3
                    except:
                        diff = 2
                        
                    db.session.commit()
                    score = 1
                    if(speed == 1 and diff == 1):
                        score = 1
                    elif(speed == 1 and diff == 2):
                        score = 3
                    elif(speed == 1 and diff == 3):
                        score = 5
                    elif(speed == 2 and diff == 1):
                        score = 2
                    elif(speed == 2 and diff == 2):
                        score = 3
                    elif(speed == 2 and diff == 3):
                        score = 4
                    elif(speed == 3 and diff == 1):
                        score = 3
                    elif(speed == 3 and diff == 2):
                        score = 4
                    else:
                        score = 5

                    
                    if(score == 1):
                        rst.score += random.randint(150, 300)
                    elif(score == 2):
                        rst.score += random.randint(120, 150)
                    elif(score == 3):
                        rst.score += random.randint(80, 120)
                    elif(score == 4):
                        rst.score += random.randint(60, 90)
                    else:
                        rst.score += random.randint(40, 60)

                    db.session.commit()

            flash("Test submitted successfully", 'info')
            return json.dumps({'sql':'fired'})
    return ('', 204)

@app.route('/randomize', methods = ['POST'])
def random_gen():
    if request.method == "POST":
        id = request.form['id']
        results = Test.query.filter(Test.testid== id).one()
        results = results.selected
        if len(results) > 0:
            nos = results
            data = {}
            time_taken = Student_test_info.query.filter(Student_test_info.username == current_user.username).filter(Student_test_info.testid == id).one()
            time_taken = time_taken.time_taken
            if(len(time_taken) == 0 ):
                time_taken = [0]*len(nos) 
            for i in range(0,len(nos)):
                id = nos[i]
                question = Questions.query.filter(Questions.questionid == id).one()
                data[i]=(question.question,question.a,question.b,question.c,question.d,time_taken[i],question.questionid)
            return json.dumps(data, sort_keys=False)

def marks_obtained(testid, username):
    reports = Students.query.filter(Students.testid == testid).filter(Students.userid== str(current_user.id)).all()
    marks = 0
    for report in reports:
        correct = Questions.query.filter(Questions.questionid == report.quid).one()
        if(correct.answer == report.ans.upper()):
            marks += 4
        elif (report.ans == '#'):
            marks += 0
        else:
            marks -= 1
    return marks

@app.route('/<username>/tests-given')
@login_required
def tests_given(username):
    if username == current_user.username:
        test_given = Student_test_info.query.with_entities(Student_test_info.testid).filter(Student_test_info.username==str(current_user.username)).order_by(Student_test_info.testid.desc()).distinct()
        results=[]
        for testid in test_given:
            result={}
            testid=testid[0]
            result['test_id'] = testid
            subject, topic = Test_info.query.with_entities(Test_info.subject,Test_info.topic).filter(Test_info.testid==testid).one()
            result['subject'] = subject
            result['topic'] = topic
            result['marks'] = marks_obtained(testid, username)
            results.append(result)
        return render_template('tests_given.html', tests=results)
    else:
        flash('You are not authorized', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/<username>/tests-given/result/<testid>')
@login_required
def tests_result(username, testid):
    completed = Student_test_info.query.filter(Student_test_info.username == username).filter(Student_test_info.testid== testid).one()
    if username == current_user.username and completed.completed==True :
        time_taken = completed.time_taken
        result = Test.query.filter(Test.testid== testid).one()
        results = []
        for qid in result.selected:
            l = []
            quer = Questions.query.filter(Questions.questionid == qid).one()
            l.append(quer)
            results.append(l)
        

        for result in results:
            qid= result[0].questionid
            try:
                marked = Students.query.filter(Students.testid== str(testid)).filter(Students.userid == str(current_user.id)).filter(Students.quid == str(qid)).one()
                marked= marked.ans               
            except:
                marked = '#'
            result.append(marked)

        for i in range(0,len(results)):
            results[i].append(time_taken[i])


        return render_template('tests_result.html', results= results, time_taken=time_taken)
    else:
        flash('You are not authorized', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/<username>/tests-created/<testid>', methods = ['POST','GET'])
@login_required
def student_results(username, testid):
    if username == current_user.username and current_user.role == 'teacher':
        results = Student_test_info.query.filter(Student_test_info.testid== testid).filter(Student_test_info.completed== True).all()
        final = []
        count=1
        data = []

        for user in results:
            score = marks_obtained(testid,user.username)
            name = User.query.filter(User.username == user.username)
            dic = {}
            dic['srno'] = count
            dic['username'] = user.username
            dic['name'] = user.username
            dic['marks'] = score
            data.append(dic)
            final.append([count, user.username, score])
            count+=1
            
        if request.method =='GET':
            results = sorted(data, key=operator.itemgetter('marks'))
            return render_template('student_results.html', data=data)
        else:
            fields = ['Sr No', 'Name', 'Marks']
            with open('static/' + testid + '.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
                writer.writerows(final)
