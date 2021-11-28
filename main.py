from re import sub
from flask import Flask,request
from flask.templating import render_template
import os
import shutil

app = Flask(__name__)
ALLOWED_EXTS = {"csv"}

def check_file(file):
    return '.' in file and file.rsplit('.',1)[1].lower() in ALLOWED_EXTS

def refresh_server():
    output_path = ".\\outputs"
    uploads_path = ".\\uploads"
    try:
        if os.path.exists(output_path):
            shutil.rmtree(output_path)
        if os.path.exists(uploads_path):
            shutil.rmtree(uploads_path)
        
        return True

    except Exception:
        return False

def check_range(range1, range2):

    if len(range1)!=8 or len(range2)!=8:
        return False

    year1 = range1[0:2]
    course1 = range1[2:4]
    branch1  = range1[4:6]
    roll1 = range1[6:8]

    year2 = range2[0:2]
    course2= range2[2:4]
    branch2  = range2[4:6]
    roll2 = range2[6:8]

    if (year1.isnumeric()
     and course1.isnumeric()
     and branch1.lower().isalpha() 
     and roll1.isnumeric() 
     and year2.isnumeric() 
     and course2.isnumeric() 
     and branch2.lower().isalpha() 
     and roll2.isnumeric()
     and year1.lower()==year2.lower()
     and branch1.lower()==branch2.lower()
     and course1.lower()==course2.lower()
     and (int(roll1) < int(roll2))):
        return True
    return False




@app.route("/", methods = ["GET", "POST"])
def build():

    error = None
    success = None
    if request.method == "POST":
        if 'submit_files' in request.form:
            if 'grades' not in request.files or 'namesroll' not in request.files or 'subjectmaster' not in request.files:
                error = "Please upload all files together!"
                return render_template("index.html", error = error)

            grade_file = request.files["grades"]
            grade_filename = grade_file.filename

            namesroll_file = request.files["namesroll"]
            namesroll_filename = namesroll_file.filename

            subjectmaster_file = request.files["subjectmaster"]
            subjectmaster_filename = subjectmaster_file.filename

            if grade_filename=='' or namesroll_filename=='' or subjectmaster_filename == '':
                error = "Please upload all files!"
                return render_template("index.html", error = error)
            if not (check_file(grade_filename) and check_file(namesroll_filename) and check_file(subjectmaster_filename)):
                error = "Please upload csv type files!"
                return render_template('index.html', error = error)

            upload_path = "./uploads"
            if os.path.exists(upload_path):
                shutil.rmtree(upload_path)
                os.mkdir(upload_path)
            else:
                os.mkdir(upload_path)
            
            grade_file.save(os.path.join(upload_path,"grades.csv"))
            namesroll_file.save(os.path.join(upload_path,"names-roll.csv"))
            subjectmaster_file.save(os.path.join(upload_path,"subjects_master.csv"))
            
            return render_template("index.html", error=error, success = "Upload success" )

        if 'generate_range' in request.form:
            
            if not (check_range(range1 = request.form['range1'], range2 = request.form['range2'])):
                error_range = "Please enter a valid range"
                return render_template('index.html', error_range = error_range)

            return render_template("index.html")
        
        if 'refresh' in request.form:
            if refresh_server():
                return render_template('index.html',success_refresh = '1')
            return render_template('index.html',error_refresh = "There was some error in refreshing, please restart the server!")

    return render_template("index.html")

app.run(debug=True)