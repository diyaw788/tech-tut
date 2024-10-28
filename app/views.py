# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

# Flask modules
from flask   import jsonify, render_template, request, redirect, url_for, flash, session
from jinja2  import TemplateNotFound
from datetime import datetime
import os
import pandas as pd
import json

# App modules
from app import app, dbConn, cursor
UPLOAD_FOLDER = 'uploads'  # Create this folder in the same directory as app.py
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         first_name = request.form['first_name']
#         last_name = request.form['last_name']
#         role = request.form['role']
#         sql = "INSERT INTO Tech_Tut (First_Name, Last_Name, Role) VALUES (%s, %s, %s)"
#         cursor.execute(sql, [first_name, last_name, role])
#         dbConn.commit()

#         return redirect(url_for('all_individuals'))
    
#     return render_template('index.html')

# @app.route('/all_individuals')
# def all_individuals():
#     search_term = request.args.get('search')  # Get the search term

#     if search_term:
#         sql = "SELECT First_Name, Last_Name, Role FROM Tech_Tut WHERE First_Name LIKE %s"
#         cursor.execute(sql, (search_term,))

#     else:
#         sql = "SELECT First_Name, Last_Name, Role FROM Tech_Tut"
#         cursor.execute(sql)

#     rows = cursor.fetchall()
#     return render_template('all_individuals.html', rows=rows)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('sign_up.html')

@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        print(name)
        sql = '''
                INSERT INTO Tech_Tut_Users (Name, Email, Password, Role)
                VALUES (%s, %s, %s, %s)
            '''
        cursor.execute(sql, (name, email, password, role))
        dbConn.commit()

        return render_template('sign_in.html')
    else:
        return render_template('sign_up.html')
    
@app.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        try:
            # Query the database for the user with the provided email and password
            sql = "SELECT * FROM Tech_Tut_Users WHERE Email = %s AND Password = %s"
            cursor.execute(sql, (email, password))
            user = cursor.fetchone()
            if user:
                # Convert the Row object to a dictionary
                user_dict = {
                    'ID': user['ID'],
                    'Name': user['Name'],
                    'Email': user['Email'],
                    'Password': user['Password'],
                    'Role': user['Role']
                }
                # Store user information in session
                session['user'] = user_dict

                user_role = session['user'].get('Role')
                if user_role == 'teacher':
                    return render_template('teacher_home.html', user=user)
                elif user_role == 'student':
                    return render_template('student_home.html', user=user)
            else:
                flash('Incorrect email or password. Please try again.', 'error')
                return redirect(url_for('sign_in'))
        except Exception as e:
            print(f"Error: {e}")
            flash('An error occurred: {}'.format(str(e)), 'error')
            return redirect(url_for('sign_in'))
    else:
        return render_template('sign_in.html')

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        sql = '''
                sql = "UPDATE Tech_Tut_Users SET Password = %s WHERE Email = %s"
            '''
        cursor.execute(sql, (password, email))
        dbConn.commit()

        return render_template('sign_in.html')
    else:
        return render_template('forgot_password.html')
    
@app.route('/teacher_home', methods=['GET', 'POST'])
def teacher_home():
    return render_template('teacher_home.html')
    
@app.route('/student_home', methods=['GET', 'POST'])
def student_home():
    return render_template('student_home.html')

@app.route('/get_evaluations', methods = ['GET']) 
def get_evaluations():
    try:
        evaluatorName = request.args.get("evaluatorName")
        print(evaluatorName)
        sql = "select Student_Being_Evaluated_Name, Student_Evaluating_Name, Status, Due_Date from Scheduled_Eval where Student_Evaluating_Name = %s"
        cursor.execute(sql, (evaluatorName,))
        evaluations = cursor.fetchall()
        print(evaluations)
        evaluations = [
            {
                "Student_Being_Evaluated_Name": row["Student_Being_Evaluated_Name"],
                "Student_Evaluating_Name": row["Student_Evaluating_Name"],
                "Status": row["Status"],
                "Due_Date": row["Due_Date"]
            }
            for row in evaluations
        ]
        print("i reach here")
        return jsonify(evaluations)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    
@app.route('/form/<string:beingEval>/<string:evaluatorName>')
def form(beingEval, evaluatorName):
    try:
        print("diya reached form")
        return render_template('form.html', student_name=beingEval, evaluator_name=evaluatorName)

    except Exception as e:
        print(f"Error: {e}")
        return "An error occurred", 500
    
@app.route('/submit_evaluation/<evaluator_name>', methods=['POST'])
def submit_evaluation(evaluator_name):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            Team_Member_Name = request.form.get('Team_Member_Name')
            Group_Effort_Peer = int(request.form.get('topic1', 0))
            Completes_Tasks_On_Time_Peer = int(request.form.get('topic2', 0))
            Provides_Useful_Feedback_Peer = int(request.form.get('topic3', 0))
            Communicates_Effectively_Peer = int(request.form.get('topic4', 0))
            Accepts_Contribution_Peer = int(request.form.get('topic5', 0))
            Builds_Contributions_Peer = int(request.form.get('topic6', 0))
            Group_Role_Peer = int(request.form.get('topic7', 0))
            Clarifies_Goals_Peer = int(request.form.get('topic8', 0))
            Reports_To_Team_Peer = int(request.form.get('topic9', 0))
            Ensures_Consistency_Peer = int(request.form.get('topic10', 0))
            Positivity_Peer = int(request.form.get('topic11', 0))
            Appropriate_Assertiveness_Peer = int(request.form.get('topic12', 0))
            Appropriate_Contibution_Peer = int(request.form.get('topic13', 0)) 
            Manages_Conflict_Peer = int(request.form.get('topic14', 0))
            Overall_Score_Peer = int(request.form.get('topic15', 0))

            # Insert data into the Evaluation table
            sql = '''
                INSERT INTO Evaluation (
                    Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, 
                    Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, 
                    Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, 
                    Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, 
                    Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contribution_Peer, 
                    Manages_Conflict_Peer, Overall_Score_Peer
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            '''
            # Update status in Scheduled_Eval table
            sql1 = '''
                UPDATE Scheduled_Eval
                SET Status = 'Complete'
                WHERE Student_Being_Evaluated_Name = %s
                AND Student_Evaluating_Name = %s;
            '''
            cursor.execute(sql1, (Team_Member_Name, evaluator_name))
            cursor.execute(sql, (Team_Member_Name, Group_Effort_Peer, Completes_Tasks_On_Time_Peer, Provides_Useful_Feedback_Peer, Communicates_Effectively_Peer, Accepts_Contribution_Peer, Builds_Contributions_Peer, Group_Role_Peer, Clarifies_Goals_Peer, Reports_To_Team_Peer, Ensures_Consistency_Peer, Positivity_Peer, Appropriate_Assertiveness_Peer, Appropriate_Contibution_Peer, Manages_Conflict_Peer, Overall_Score_Peer))
            dbConn.commit()
            return render_template('student_home.html')
        except Exception as e:
            dbConn.rollback()
            print(f"Error: {e}")
            flash(f"An error occurred: {e}", 'error')
            return f"An error occurred: {e}", 500

@app.route('/get_courses', methods = ['GET']) 
def get_courses():
    try:
        professorName = request.args.get("professorName")
        searchValue = request.args.get("searchValue", "")
        print(professorName)

        if searchValue == "":
            sql = "select Course_Name, CourseID from Courses where Professor = %s"
            cursor.execute(sql, (professorName,))
        else:
            sql = "SELECT Course_Name, CourseID FROM Courses WHERE Professor = %s AND CourseID LIKE %s"
            cursor.execute(sql, (professorName, f"%{searchValue}%"))
        courses = cursor.fetchall()
        print(courses)
        courses = [
            {
                "Course_Name": row["Course_Name"],
                "CourseID": row["CourseID"]
            }
            for row in courses
        ]
        print("i reach here")
        return jsonify(courses)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
    

@app.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            try:
                data = pd.read_csv(filepath) # Read the CSV file using pandas
                for index, row in data.iterrows():
                    try:
                        cursor.execute("""
                            INSERT INTO Courses (CourseID, Course_Name, Professor) 
                            VALUES (%s, %s, %s);
                            """, 
                            (row['CourseID'], row['Course_Name'], row['Professor'])
                        )
                        dbConn.commit()
                    except Exception as e:
                        print(f"Error inserting row {index}: {e}")
            except Exception as e:
                flash(f'Error processing file: {e}')
            return redirect(url_for('index'))
        flash('File type is not allowed.')
        return redirect(request.url)
    else:
        return render_template('upload.html')

@app.route('/sorted_evaluations', methods=['GET'])
def sorted_evaluations():
    try:
        evaluatorName = request.args.get("evaluatorName")
        sql = """
            SELECT Student_Being_Evaluated_Name, Status, Due_Date 
            FROM Scheduled_Eval 
            WHERE Student_Evaluating_Name = %s 
            ORDER BY Due_Date ASC
        """
        cursor.execute(sql, (evaluatorName,))
        evaluations = cursor.fetchall()

        # Convert results to JSON-friendly format
        evaluations = [
            {
                "Student_Being_Evaluated_Name": row["Student_Being_Evaluated_Name"],
                "Status": row["Status"],
                "Due_Date": row["Due_Date"].strftime("%Y-%m-%d")
            }
            for row in evaluations
        ]

        return jsonify(evaluations)
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500
