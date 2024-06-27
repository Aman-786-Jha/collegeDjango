# myapps/management/commands/populate_data.py

import random
from django.core.management.base import BaseCommand
from faker import Faker
from myapps.models import University, College, Course

# class Command(BaseCommand):
#     help = 'Populate the database with fake data for testing'

#     def handle(self, *args, **kwargs):
#         fake = Faker()

#         # Populate University Model
#         for i in range(50):
#             university = University(
#                 name=fake.company(),
#                 location=fake.city(),
#                 established_year=random.randint(1800, 2023),
#                 website=fake.url(),
#                 contact_email=fake.email(),
#                 contact_phone=fake.phone_number(),
#                 description=fake.text(),
#                 student_population=random.randint(1000, 20000),
#                 faculty_count=random.randint(50, 500),
#                 annual_budget=round(random.uniform(100000, 1000000), 2),
#                 accreditation=fake.bs()
#             )
#             university.save()

#         # Populate College Model
#         for i in range(50):
#             college = College(
#                 name=fake.company(),
#                 location=fake.city(),
#                 university=University.objects.order_by('?').first(),
#                 dean=fake.name(),
#                 contact_email=fake.email(),
#                 contact_phone=fake.phone_number(),
#                 established_year=random.randint(1800, 2023),
#                 number_of_departments=random.randint(1, 10),
#                 student_population=random.randint(100, 5000),
#                 faculty_count=random.randint(10, 200),
#                 annual_budget=round(random.uniform(10000, 500000), 2)
#             )
#             college.save()

#         # Populate Course Model
#         course_choices = ['B.Tech', 'B.Sc', 'B.A', 'M.Tech', 'M.Sc', 'M.A']
#         semester_choices = ['Spring', 'Fall', 'Summer']

#         for i in range(50):
#             course = Course(
#                 name=random.choice(course_choices),
#                 description=fake.text(),
#                 duration=random.randint(2, 5),
#                 college=College.objects.order_by('?').first(),
#                 credits=random.randint(1, 5),
#                 syllabus=fake.text(),
#                 prerequisites=fake.text(),
#                 professor=fake.name(),
#                 max_enrollment=random.randint(20, 100),
#                 current_enrollment=random.randint(5, 50),
#                 offered_semester=random.choice(semester_choices)
#             )
#             course.save()

#         self.stdout.write(self.style.SUCCESS('Successfully populated the database with fake data'))



class Command(BaseCommand):
    help = 'Populate university_grade field with random values'

    def handle(self, *args, **kwargs):
        grades = ['A', 'B', 'C', 'D']
        universities = University.objects.all()

        for university in universities:
            university.university_grade = random.choice(grades)
            university.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated university_grade field for all universities'))


# from django.core.management.base import BaseCommand
# import uuid
# from myapps.models import College, Course

# class Command(BaseCommand):
#     help = 'Populate UUID field for College and Course models'

#     def handle(self, *args, **kwargs):
#         # Populate UUID for College Model
#         colleges = College.objects.all()
#         for college in colleges:
#             if not college.uuid:
#                 college.uuid = uuid.uuid4()
#                 college.save()

#         # Populate UUID for Course Model
#         courses = Course.objects.all()
#         for course in courses:
#             if not course.uuid:
#                 course.uuid = uuid.uuid4()
#                 course.save()

#         self.stdout.write(self.style.SUCCESS('Successfully populated UUID fields for College and Course models'))
