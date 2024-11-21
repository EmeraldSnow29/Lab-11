import matplotlib.pyplot as plt
import os
from course_info import *

#calculated at runtime
max_weight = 0

Students = []
Assignments = []
Submissions = []
def readfiles():
    """
    Reads all files and puts them into lists
    """
    with open(os.path.join("data", "students.txt")) as f:
        #all student data is stored in a single line.
        for l in f:
            Students.append(Student.from_string(l))
    #read the data in assignments
    with open(os.path.join("data", "assignments.txt")) as f:
        lines = f.readlines()
        leng = len(lines)//3
        #assignment data is in sets of 3 lines.
        for i in range(leng):
            ind1 = i*3
            ind2 = i*3 + 3
            Assignments.append(Assignment.from_strings(lines[ind1:ind2]))
    #Find all the files in the submissions directory.
    for name, subdirs, files in os.walk(os.path.join("data", "submissions")):
        for file in files:
            #load each file.
            with open(os.path.join("data", "submissions", file)) as f:
                for l in f:
                    Submissions.append(Submission.from_string(l))


def student_by_name(name):
    """
    Gets the data for a student by name.
    """
    for student in Students:
        if student.name == name:
            return student
    return None

def assignment_by_name(name):
    """
    Gets the data for an assignment by name.
    """
    for assignment in Assignments:
        if assignment.name == name:
            return assignment
    return None

def get_all_grades(assignment):
    """
    Gets all the grades on a particular assignment.
    """
    res = []
    for submission in Submissions:
        if submission.assignment == assignment:
            res.append(submission.grade)
    return res


def get_assignment_grade(student, assignment):
    """
    Gets the student's grade on the assignment
    """
    std2 = student.idn
    asn2 = assignment.idn
    global max_weight
    res = 0
    for submission in Submissions:
        #find the submission matching the assignment and student.
        if std2 == submission.student and asn2 == submission.assignment:
            res += submission.grade * (assignment.weight / max_weight)
    return res

def calc_max_weight():
    """
    Calculates the "maximum weight", the total of the weights of all assignments.
    :return:
    """
    global max_weight
    res = 0
    for assignment in Assignments:
        res += int(assignment.weight)
    max_weight = res

def generate_bins(grades, segments):
    """
    Calculates an appropriate width for the bars on the bar graph.
    """

    #grades should be evenly divided between segments.
    #bins shouldn't go below 0 or above 100.
    #otherwise, bins should have one empty section on either end of the graph.

    #we need 3 or more segments for this method to work.
    assert segments > 3, "Cannot use less than 3 segments!"
    min_grade = min(grades)
    max_grade = max(grades)

    #calculate the segment width, ignoring borders.
    #using integer division ensures the graph uses nice round numbers.
    segment_width = (max_grade - min_grade) // (segments - 1)

    #with that info, calculate the new segment width with borders
    cut_beginning = False

    if min_grade - segment_width < 0 and max_grade + segment_width > 100:
        cut_beginning = True
        segment_width = 100 / segments

    elif min_grade - segment_width < 0:
        cut_beginning = True
        segment_width = max_grade // (segments-1)

    elif max_grade + segment_width > 100:
        segment_width = 100 - min_grade // (segments-1)

    #This adds empty segments at the beginning and end of the graph.
    res = []
    for i in range(segments + 3):
        #make sure to start from 0
        start = segment_width if cut_beginning else min_grade
        bin = start + (segment_width * (i-1))

        #caps the bin pos at 100
        add = bin if bin < 100 else 100

        res.append(add)

        #if we have a bin at 100, we are done.
        if add == 100:
            break

    return res


def main():
    readfiles()
    calc_max_weight()

    print("1. Student grade",
          "2. Assignment statistics",
          "3. Assignment graph \n", sep = "\n")

    inp = 0
    try:
        inp = int(input("Enter your selection: "))
    finally:
        pass


    if inp == 1:
        name = input("What is the student's name: ")

        student = student_by_name(name)
        if student:
            total = 0
            for assignment in Assignments:
                total += get_assignment_grade(student, assignment)

            print(f"{total:.1f}%")
        else:
            print("Student not found")

    if inp == 2:
        name = input("What is the assignment name: ")

        assignment = assignment_by_name(name)
        if assignment:
            grades = get_all_grades(assignment.idn)

            print(f"Min: {min(grades)}%")
            print(f"Avg: {(sum(grades)//len(grades))}%")
            print(f"Max: {max(grades)}%")
        else:
            print("assignment not found")

    if inp == 3:
        name = input("What is the assignment name: ")

        assignment = assignment_by_name(name)
        if assignment:
            grades = get_all_grades(assignment.idn)

            bins = generate_bins(grades, 10)

            plt.hist(sorted(grades), bins = bins, label=name)
            plt.show()

        else:
            print("assignment not found")





if __name__ == '__main__':
    main()
