
"""
Author: Yuan Zhang
Course: SSW 810
Description of this script: Homework 09 - Stevens data repository
"""

from prettytable import PrettyTable
import os
from collections import defaultdict


def file_reader(path, fnum, sep = '\t'):
    try:
        fp = open(path, 'r')
    except FileNotFoundError:
        print("Oops! Can't open", path)
    else:
        with fp:
            for line in fp:  
                fields = line.strip().split(sep)
                if len(fields) != fnum:
                    raise ValueError("ValueError: {} has {} fields on line {} but expected {}".format(path, len(fields), counter, fnum))
                else:
                    yield tuple(fields)


class Repository:
    """ holds all of the data for a specific organization """
    def __init__(self, path, print_tb=True):
        self.path = path
        self.students = defaultdict(Student) # key: cwid; value: instance of Student
        self.instructors = defaultdict(Instructor) # key: cwid; value: instance of Instructor

        self.get_students(os.path.join(path, 'students.txt'))
        self.get_instructors(os.path.join(path, 'instructors.txt'))
        self.get_grades(os.path.join(path, 'grades.txt'))

        if print_tb:
            print("---Student Summary---")
            self.student_table()
            print("---Instructor Summary---")
            self.instructor_table()

    def get_students(self, path):
        for cwid, name, major in file_reader(path, 3, sep='\t'):
            self.students[cwid] = Student(cwid, name, major)

    def get_instructors(self, path):
        for cwid, name, department in file_reader(path, 3, sep='\t'):
            self.instructors[cwid] = Instructor(cwid, name, department)
    
    def get_grades(self, path):
        for student, course, grade, instructor in file_reader(path, 4, sep='\t'):
            if student in self.students:
                self.students[student].add_course(course, grade)
            else:
                print('Student {} is not in the file!'.format(student))
            if instructor in self.instructors:
                self.instructors[instructor].add_student(course)
            else:
                print('Instructor {} is not in the file!'.format(instructor))         
    
    def student_table(self):
        """ use PrettyTable to print students information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        for cwid in self.students:
            pt.add_row(self.students[cwid].pt_rows())
    
    def instructor_table(self):
        """ use PrettyTable to print instructors information """
        pt = PrettyTable(field_names=['CWID', 'Name', 'Depart', 'Course', 'Students'])
        for cwid in self.instructors:
            pt.add_row(self.instructors[cwid].pt_rows())


class Student:
    """ a student's information """
    def __init__(self, cwid, name, major):
        self.cwid = cwid
        self.name = name
        self.major = major
        self.courses = defaultdict(int) # key is the course, value is the grade of the course
    
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
        for course, students in self.courses.items():
            return [self. cwid, self.name, self.department, course, students]


def main():
    path = '/Users/kybeth/Documents/SIT/SSW_810/Stevens'
    stevens = Repository(path) # read files and generate prettytables


if __name__ == '__main__':
    main()