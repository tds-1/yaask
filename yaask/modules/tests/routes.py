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
from yaask.models import *
from yaask import app
from coolname import generate_slug
import random
from yaask.modules.tests.utils import choosequestions
from datetime import timedelta, datetime

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
                print (form.data)
                test_info =  Test_info(
                    creatorid = current_user.id,
                    subject = form.subject.data,
                    topic = form.topic.data,
                    start_date = form.start_date.data,
                    end_date = form.end_date.data,
                    start_time = form.start_time.data,
                    end_time = form.end_time.data,
                    show_result = form.show_result.data,
                    neg_mark = form.neg_mark.data,
                    duration = int(form.duration.data)*60,
                    password = form.password.data
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

        
@app.route('/<username>/create-test/<testid>', methods = ['GET', 'POST'])
@login_required
def create_test(username, testid):
    if username == current_user.username and current_user.role == 'teacher':
        categoryList = [
            'biology',]
        #To allow sorting by username just do an ajax request back to score board with argument (like /score/#username then /score/#score)
        form=RandomTest(request.form)
        if request.method == 'GET':
            db.session.commit()
            questions_to_display = Questions.query.filter().all()
            return render_template('test.html',form=form, questions_to_display=questions_to_display, categoryList=categoryList)

        if request.method == 'POST':
            selected = []
            try:
                subject = form.subject.data
                number = form.number_of_questions.data
                tag = form.topic.data
                tag = [tag]
                print (subject, number, tag)
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
                # category=form.subject.data
                # avg=form.avg_difficulty.data
                # n=form.number_of_questions.data
                # print (category, avg, n)
                # temp=Questions.query.filter( ~Questions.questionid.in_(selected)).filter(Questions.category==category).all()
                # arr=[]
                # for x in temp:
                #     arr.append((int(x.difficulty), x.question_score, x.questionid))
            
                # random_questions=choosequestions(arr, avg, n)
                # print (random_questions)
                # for question in random_questions:
                #     selected.append(question[2])
                #update score
            questions_to_display = Questions.query.filter( Questions.questionid.in_(selected) ).all()
            for x in questions_to_display:
                x.question_score=x.question_score+1
                db.session.commit()
            print (selected)
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
        results = Test_info.query.filter(Test_info.creatorid == current_user.id).all()
        return render_template('tests_created.html', tests=results)
    else:
        # flash('You are not authorized', 'danger')
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
            start_date = data.start_date
            start_time = data.start_time
            end_date = data.end_date
            end_time = data.end_time
            start = str(start_date) + " " + str(start_time)
            end = str(end_date) + " " + str(end_time)
            if password == password_candidate:
                now = datetime.now()
                now = now.strftime("%Y-%m-%d %H:%M:%S")
                now = datetime.strptime(now,"%Y-%m-%d %H:%M:%S")
                if datetime.strptime(start,"%Y-%m-%d %H:%M:%S") < now and datetime.strptime(end,"%Y-%m-%d %H:%M:%S") > now:
                    results = Student_test_info.query.filter(Student_test_info.username == current_user.username).filter(Student_test_info.testid == test_id).all()
                    if len(results)>0 :
                        results = results[0]
                        is_completed = results.completed
                        if is_completed == False:
                            time_left = max(0, duration - (now-datetime.strptime(results.time_started,"%Y-%m-%d %H:%M:%S")).total_seconds())
                            if time_left <= duration:
                                duration = time_left
                                results = Students.query.filter(Students.username == current_user.username).filter(Students.testid == test_id).all()
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
                            completed = False
                        )
                        db.session.add(student_test_info_data)
                        db.session.commit()
                        
                        results = Student_test_info.query.filter(Student_test_info.username == current_user.username).filter(Student_test_info.testid == test_id).all()
                        if len(results)>0 :
                            results = results[0]
                            is_completed = results.completed
                            if is_completed == False:
                                time_left = max(0,duration -  ( now-datetime.strptime(results.time_started,"%Y-%m-%d %H:%M:%S")).total_seconds())

                                if time_left <= duration:
                                    duration = time_left
                                    results = Students.query.filter(Students.username == current_user.username).filter(Students.testid == test_id).all()
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

from flask_marshmallow import Marshmallow

ma = Marshmallow(app)

class PhotoShareSchema(ma.Schema):
    class Meta:
        fields = ('a','b','c','d','question','questionid')

photo_share_schema = PhotoShareSchema()
photos_share_schema = PhotoShareSchema(many=True)


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
        if flag == 'get':
            num = request.form['no']
            results = Questions.query.filter(Questions.questionid== num).one()
            data = photo_share_schema.dump(results)
            data['marked']= eval(marked_ans)
            return json.dumps(data)
        elif flag=='mark':
            qid = request.form['qid']
            ans = request.form['ans']
            print (qid, ans)
            marked_ans = eval (marked_ans)
            marked_ans[qid]=ans
            marked_ans = json.dumps(marked_ans)
            results = Students.query.filter(Students.testid== testid).filter(Students.quid== qid).filter(Students.username== current_user.username).all()
            if len(results) == 0:
                studentdata = Students(
                    ans= ans,
                    testid=testid,
                    username= current_user.username,
                    quid = qid
                )
                db.session.add(studentdata)
                db.session.commit()
            else:
                studentdata=Students.query.filter(Students.username== current_user.username).filter(Students.testid== testid).filter(Students.quid== qid).one()
                studentdata.ans=ans
                db.session.commit()
        else:
            info = Student_test_info.query.filter(Student_test_info.username==current_user.username).filter(Student_test_info.testid == testid).one()
            info.time_left=0
            info.completed= True
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
            random.Random(id).shuffle(nos)
            data = {}
            for id in nos:
                question = Questions.query.filter(Questions.questionid == id).one()
                data[question.questionid]=(question.question,question.a,question.b,question.c,question.d)
            return json.dumps(data)

def marks_obtained(testid, username):
    reports = Students.query.filter(Students.testid == testid).filter(Students.username== username).all()
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
        test_given = Students.query.with_entities(Students.testid).filter(Students.username==username).distinct()
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
        # add a condition if test is given 
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
                marked = Students.query.filter(Students.testid== str(testid)).filter(Students.username == username).filter(Students.quid == str(qid)).one()
                marked= marked.ans               
            except:
                marked = '#'
            result.append(marked)
        return render_template('tests_result.html', results= results)
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
            #return send_file('/static/' + testid + '.csv', as_attachment=True)
