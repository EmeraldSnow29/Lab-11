
NUMBERS = "1234567890"

#Assignments in assignments have a name, identifier, and weight.
class Assignment:
    def __init__(self, name, idn, weight):
        self.name = name
        self.idn = idn
        self.weight = weight

    @classmethod
    def from_strings(cls, strings):
        """
        Strings must be a list of 3 strings
        """

        return cls(strings[0].strip(), strings[1].strip(), int(strings[2].strip()))

class Student:
    def __init__(self, idn, name):
        self.idn = idn
        self.name = name

    @classmethod
    def from_string(cls, string):
        """
        strings are ids followed by a name
        """

        idn = ""
        name = ""
        for i in range(len(string)):
            c = string[i]
            if c in NUMBERS:
                idn += c
            else:
                name = string[i:-1]
                break


        return cls(idn, name)

class Submission:
    def __init__(self, student, assignment, grade):
        """
        :param student: the student id
        :param assignment: the assignment id
        :param grade: the grade
        """
        self.student = student
        self.assignment = assignment
        self.grade = grade
    @classmethod
    def from_string(cls, string):
        """
        data is separated by |
        """

        strings = string.split(sep = "|")
        return cls(strings[0], strings[1], int(strings[2]))