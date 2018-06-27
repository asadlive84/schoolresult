


class SubjectGrade:

    def __init__(self, subject_number):
        self.subject_number=subject_number



    def subgrade(self):
        if self.subject_number>=80 and self.subject_number<=100:
            return 'A+'
        elif self.subject_number >= 70 and self.subject_number <= 79:
            return 'A'

        elif self.subject_number >= 60 and self.subject_number <= 69:
            return 'A-'

        elif self.subject_number >= 50 and self.subject_number <= 59:
            return 'B'

        elif self.subject_number >= 40 and self.subject_number <= 49:
            return 'C'

        elif self.subject_number >= 33 and self.subject_number <= 39:
            return 'D'

        elif self.subject_number >= 0 and self.subject_number <= 32:
            return 'F'
        

class SubjectGradePoint:

    def __init__(self, subject_number):
        self.subject_number = subject_number

    def subgrade(self):
        if self.subject_number >= 80 and self.subject_number <= 100:
            return 5
        elif self.subject_number >= 70 and self.subject_number <= 79:
            return 4

        elif self.subject_number >= 60 and self.subject_number <= 69:
            return 3.5

        elif self.subject_number >= 50 and self.subject_number <= 59:
            return 3

        elif self.subject_number >= 40 and self.subject_number <= 49:
            return 2

        elif self.subject_number >= 33 and self.subject_number <= 39:
            return 1

        elif self.subject_number >= 0 and self.subject_number <= 32:
            return 0
