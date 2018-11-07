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
        self.students = dict() # key: cwid; value: instance of Student
        self.instructors = dict() # key: cwid; value: instance of Instructor

        self.get_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))

        if print_tb:
            print("Student Summary")
            self.student_table()
            print("Instructor Summary")
            self.instructor_table()

    def get_students(self, path):
        for cwid, name, major in file_reader(path, 3, sep='\t'):
            self.students[cwid] = Student(cwid, name, major)

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
    
    def student_table(self):
        """ use PrettyTable to print students information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        for cwid in self.students:
            pt.add_row(self.students[cwid].pt_rows())
        print(pt)
    
    def instructor_table(self):
        """ use PrettyTable to print instructors information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Depart', 'Course', 'Students'])
        for cwid in self.instructors:
            for line in self.instructors[cwid].pt_rows():
                pt.add_row(line)
        print(pt)


class Student:
    """ a student's information """
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = dict() # key is the course, value is the grade of the course
    
    def add_course(self, course, grade):
        self.courses[course] = grade

    def pt_rows(self):
        return [self.cwid, self.name, sorted(self.courses.keys())]
    

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