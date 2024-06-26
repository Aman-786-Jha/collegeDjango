from django.db import models

import string
import random
from django.db import models
from django.utils.text import slugify

class University(models.Model):
    GRADE_CHOICES = [
        ('A', 'NAAC A'),
        ('B', 'NAAC B'),
        ('C', 'NAAC C'),
        ('D', 'NAAC D'),
    ]

    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    established_year = models.PositiveIntegerField()
    website = models.URLField(max_length=255, blank=True, null=True, default='')
    contact_email = models.EmailField(max_length=255, blank=True, null=True, default='')
    contact_phone = models.CharField(max_length=255, blank=True, null=True, default='')
    description = models.TextField(blank=True, null=True, default='')
    student_population = models.PositiveIntegerField(blank=True, null=True, default=0)
    faculty_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    annual_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0.00)
    accreditation = models.CharField(max_length=255, blank=True, null=True, default='')
    university_grade = models.CharField(max_length=1, choices=GRADE_CHOICES, blank=True, null=True, default='')

    def __str__(self):
        return self.name

class College(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    university = models.ForeignKey(University, related_name='colleges', on_delete=models.CASCADE)
    dean = models.CharField(max_length=255, blank=True, null=True, default='')
    contact_email = models.EmailField(max_length=255, blank=True, null=True, default='')
    contact_phone = models.CharField(max_length=255, blank=True, null=True, default='')
    established_year = models.PositiveIntegerField(blank=True, null=True, default=0)
    number_of_departments = models.PositiveIntegerField(blank=True, null=True, default=0)
    student_population = models.PositiveIntegerField(blank=True, null=True, default=0)
    faculty_count = models.PositiveIntegerField(blank=True, null=True, default=0)
    annual_budget = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True, default=0.00)
    
    def __str__(self):
        return self.name



class Course(models.Model):
    # Choices for course names
    COURSE_CHOICES = [
        ('B.Tech', 'Bachelor of Technology'),
        ('B.Sc', 'Bachelor of Science'),
        ('B.A', 'Bachelor of Arts'),
        ('M.Tech', 'Master of Technology'),
        ('M.Sc', 'Master of Science'),
        ('M.A', 'Master of Arts'),
    ]

    name = models.CharField(max_length=255, choices=COURSE_CHOICES)
    description = models.TextField()
    duration = models.PositiveIntegerField(help_text="Duration in years")
    college = models.ForeignKey(College, related_name='courses', on_delete=models.CASCADE)
    credits = models.PositiveIntegerField(default=0)
    syllabus = models.TextField(blank=True, null=True, default='')
    prerequisites = models.TextField(blank=True, null=True, default='')
    professor = models.CharField(max_length=255, blank=True, null=True, default='')
    course_code = models.CharField(max_length=50, unique=True, editable=False)  # editable=False to prevent direct editing
    max_enrollment = models.PositiveIntegerField(default=0)
    current_enrollment = models.PositiveIntegerField(default=0)
    offered_semester = models.CharField(
        max_length=50, 
        choices=[('Spring', 'Spring'), ('Fall', 'Fall'), ('Summer', 'Summer')], 
        default='Fall'
    )

    def __str__(self):
        return f"{self.name} at {self.college.name}"

    def save(self, *args, **kwargs):
        if not self.course_code:
            # Generate course code based on name and college
            college_code_part = self.college.name[:6].upper()  # Take first 6 characters of college name
            name_slug = slugify(self.name)  # Slugify course name

            # Ensure course_code is unique
            while True:
                random_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
                proposed_course_code = f"{name_slug[:6].upper()}-{college_code_part}-{random_code}"

                if not Course.objects.filter(course_code=proposed_course_code).exists():
                    self.course_code = proposed_course_code
                    break

        super().save(*args, **kwargs)

