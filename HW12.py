from flask import Flask, render_template
import sqlite3

def open_db():
    """ Connect to the database """
    DB_FILE = '/Users/kybeth/Documents/SIT/SSW_810/HW12_YuanZhang/810_startup.db'
    db = sqlite3.connect(DB_FILE)
    return db

app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello world! This is Yuan's first flask!"

@app.route('/instructor_courses')
def instructors():
    db = open_db()
    query ='select ins.CWID, ins.Name, ins.Dept, gra.Course, count(gra.Student_CWID) from HW11_instructors ins join HW11_grades gra on ins.CWID=gra.Instructor_CWID group by gra.course order by ins.CWID'
    results = db.execute(query)
    data = [{'cwid':cwid, 'name':name, 'dept':dept, 'courses':courses, 'students':students} for cwid, name, dept, courses, students in results]
    db.close()

    return render_template('instructor_table.html',title="Stevens Repository", table_title="Number of students by course and instructor", instructors=data)

app.run(debug=True)