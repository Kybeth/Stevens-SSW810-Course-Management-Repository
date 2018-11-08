"""
Author: Yuan Zhang
Course: SSW 810
Description of this script: Homework 09 - Stevens data repository
"""

from prettytable import PrettyTable
import os
from collections import defaultdict

def file_reader(path, fnum, sep = '\t', header = False):
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        print("Oops! Can't open file {}".format(path))
    else:
        with fp:
            counter = 0 
            for line in fp:  
                counter += 1
                if header == True and counter == 1:
                    continue
                fields = line.rstrip().split(sep)
                if len(fields) != fnum:
                    raise ValueError("ValueError: {} has {} fields on line {} but expected {}".format(path, len(fields), counter, fnum))
                else:
                    yield tuple(fields)

class Repository:
    """ holds all of the data for a specific organization """
    def __init__(self, path, print_tb=True):
        self.path = path
        self.majors = dict() # key: department(major) name; value: instance of Student
        self.students = dict() # key: cwid; value: instance of Student
        self.instructors = dict() # key: cwid; value: instance of Instructor

        self.get_majors(os.path.join(path, 'majors.txt'))
        self.get_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))

        
        #每个get_都和一个数据结构（自定义class）对应

        if print_tb:
            print('Majors Summary')
            self.major_table()####
            print("Student Summary")
            self.student_table()
            print("Instructor Summary")
            self.instructor_table()

    def get_majors(self, path):
        for dept, flag, course in file_reader(path, 3, sep='\t'):
            if dept not in self.majors:
                self.majors[dept] = Major(dept)
            self.majors[dept].add_course(flag, course)

    def get_students(self, path):
        for cwid, name, major in file_reader(path, 3, sep='\t'):
            #self.students[cwid] = Student(cwid, name, major)
            self.students[cwid] = Student(cwid, name, self.majors[major])

    def get_instructors(self, path):
        for cwid, name, department in file_reader(path, 3, sep='\t'):
            self.instructors[cwid] = Instructor(cwid, name, department)
    
    def get_grades(self, path):
        for student_cwid, course, grade, instructor_cwid in file_reader(path, 4, sep='\t'):
            if student_cwid in self.students:
                self.students[student_cwid].add_course(course, grade)
            else:
                print('Student {} is not in the file!'.format(student_cwid))
            if instructor_cwid in self.instructors:
                self.instructors[instructor_cwid].add_student(course)
            else:
                print('Instructor {} is not in the file!'.format(instructor_cwid))         
    
  

    def major_table(self):
        """ use PrettyTable to print major information """
        pt = PrettyTable(field_names=['Dept', 'Required', 'Electives'])
        for major in self.majors:
            pt.add_row(self.majors[major].pt_rows())
        print(pt)   

    def student_table(self):
        """ use PrettyTable to print students] information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 'Remaining Electives'])
        for cwid in self.students:
            pt.add_row(self.students[cwid].pt_rows())##
        print(pt)
    
    def instructor_table(self):
        """ use PrettyTable to print instructor information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Dept', 'Course', 'Students'])
        for cwid in self.instructors:
            for line in self.instructors[cwid].pt_rows():
                pt.add_row(line)
        print(pt)

     



class Major:
    """ the required courses and elective courses of a major """
    def __init__(self, dept):
        self.dept = dept
        self.courses = defaultdict(set) # key is R/E, value is set of courses

    def add_course(self, flag, course):
        self.courses[flag].add(course)
    
    def remaining_r(self, completed_courses):
        return self.courses['R'] - completed_courses
    
    def remaining_e(self, completed_courses):
        if self.courses['E'].intersection(completed_courses):
            return 'None'
        else:
            return self.courses['E']   

    def pt_rows(self):
        return [self.dept, sorted(self.courses['R']), sorted(self.courses['E'])]

class Student:
    """ a student's information """
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major ####
        self.courses = dict() # key is the course, value is the grade of the course
    
    def add_course(self, course, grade):
        self.courses[course] = grade 

    def completed_courses(self):
        com_courses = list()
        for course, grade in self.courses.items():
            if grade in {'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C'}:
                com_courses.append(course)
        return com_courses

    def pt_rows(self):
        return [self.cwid, self.name, self.major.dept, sorted(self.completed_courses()), self.major.remaining_r(set(self.completed_courses())), self.major.remaining_e(set(self.completed_courses()))]####
    

class Instructor:
    """ an instructor's information """
    def __init__(self, cwid, name, department):
        self.cwid = cwid
        self.name = name
        self.department = department
        self.courses = defaultdict(int)

    def add_student(self, course):
        #instructor's course should be a dict, key is the course, value is the students num
        self.courses[course] += 1

    def pt_rows(self):
        for k in self.courses:
            yield [self.cwid, self.name, self.department, k, self.courses[k]]


def main():
    path = '/Users/kybeth/Documents/SIT/SSW_810/Stevens'
    stevens = Repository(path) # read files and generate prettytables


if __name__ == '__main__':
    main()