# from rest_framework import serializers
# from .models import University, College, Course

# class CourseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = '__all__'

# class CollegeSerializer(serializers.ModelSerializer):
#     courses = CourseSerializer(many=True)

#     class Meta:
#         model = College
#         fields = '__all__'

# class UniversitySerializer(serializers.ModelSerializer):
#     colleges = CollegeSerializer(many=True)

#     class Meta:
#         model = University
#         fields = '__all__'

#     def create(self, validated_data):
#         colleges_data = validated_data.pop('colleges')
#         university = University.objects.create(**validated_data)
#         for college_data in colleges_data:
#             courses_data = college_data.pop('courses')
#             college = College.objects.create(university=university, **college_data)
#             for course_data in courses_data:
#                 Course.objects.create(college=college, **course_data)
#         return university

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.location = validated_data.get('location', instance.location)
#         instance.established_year = validated_data.get('established_year', instance.established_year)
#         instance.website = validated_data.get('website', instance.website)
#         instance.contact_email = validated_data.get('contact_email', instance.contact_email)
#         instance.contact_phone = validated_data.get('contact_phone', instance.contact_phone)
#         instance.description = validated_data.get('description', instance.description)
#         instance.student_population = validated_data.get('student_population', instance.student_population)
#         instance.faculty_count = validated_data.get('faculty_count', instance.faculty_count)
#         instance.annual_budget = validated_data.get('annual_budget', instance.annual_budget)
#         instance.accreditation = validated_data.get('accreditation', instance.accreditation)
#         instance.university_grade = validated_data.get('university_grade', instance.university_grade)
#         instance.save()

#         # Handle colleges and courses update
#         self._update_colleges(instance, validated_data.get('colleges', []))

#         return instance

#     def _update_colleges(self, university, colleges_data):
#         existing_college_ids = set(university.colleges.values_list('uuid', flat=True))
#         new_college_ids = []

#         for college_data in colleges_data:
#             college_uuid = college_data.pop('uuid', None)
#             if college_uuid:
#                 college, created = College.objects.update_or_create(
#                     uuid=college_uuid,
#                     university=university,
#                     defaults={
#                         'name': college_data.get('name'),
#                         'location': college_data.get('location'),
#                         'dean': college_data.get('dean'),
#                         'contact_email': college_data.get('contact_email'),
#                         'contact_phone': college_data.get('contact_phone'),
#                         'established_year': college_data.get('established_year'),
#                         'number_of_departments': college_data.get('number_of_departments'),
#                         'student_population': college_data.get('student_population'),
#                         'faculty_count': college_data.get('faculty_count'),
#                         'annual_budget': college_data.get('annual_budget')
#                     }
#                 )
#                 new_college_ids.append(college.uuid)
#                 self._update_courses(college, college_data.get('courses', []))
#             else:
#                 college = College.objects.create(university=university, **college_data)
#                 new_college_ids.append(college.uuid)
#                 self._update_courses(college, college_data.get('courses', []))

#         # Delete colleges not in the updated list
#         university.colleges.exclude(uuid__in=new_college_ids).delete()

#     def _update_courses(self, college, courses_data):
#         existing_course_ids = set(college.courses.values_list('uuid', flat=True))
#         new_course_ids = []

#         for course_data in courses_data:
#             course_uuid = course_data.pop('uuid', None)
#             if course_uuid:
#                 course, created = Course.objects.update_or_create(
#                     uuid=course_uuid,
#                     college=college,
#                     defaults={
#                         'name': course_data.get('name'),
#                         'description': course_data.get('description'),
#                         'duration': course_data.get('duration'),
#                         'credits': course_data.get('credits'),
#                         'syllabus': course_data.get('syllabus'),
#                         'prerequisites': course_data.get('prerequisites'),
#                         'professor': course_data.get('professor'),
#                         'max_enrollment': course_data.get('max_enrollment'),
#                         'current_enrollment': course_data.get('current_enrollment'),
#                         'offered_semester': course_data.get('offered_semester')
#                     }
#                 )
#                 new_course_ids.append(course.uuid)
#             else:
#                 course = Course.objects.create(college=college, **course_data)
#                 new_course_ids.append(course.uuid)

#         # Delete courses not in the updated list
#         college.courses.exclude(uuid__in=new_course_ids).delete()




# serializers.py
from rest_framework import serializers
from .models import University, College, Course

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'

from rest_framework import serializers
from .models import College, University

class CollegeSerializer(serializers.ModelSerializer):
    university = serializers.UUIDField(source='university.uuid')
    

    class Meta:
        model = College
        fields = [
            'uuid',
            'name',
            'location',
            'dean',
            'contact_email',
            'contact_phone',
            'established_year',
            'number_of_departments',
            'student_population',
            'faculty_count',
            'annual_budget',
            'university',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['university'] = instance.university.name
        return representation

    def create(self, validated_data):
        university_data = validated_data.pop('university')
        university = University.objects.get(uuid=university_data['uuid'])
        college = College.objects.create(university=university, **validated_data)
        return college

    def update(self, instance, validated_data):
        university_data = validated_data.pop('university')
        university = University.objects.get(uuid=university_data['uuid'])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.university = university
        instance.save()
        return instance
    


from rest_framework import serializers
from .models import Course, College

class CourseSerializer(serializers.ModelSerializer):
    college = serializers.UUIDField(source='college.uuid')

    class Meta:
        model = Course
        fields = [
            'uuid',
            'name',
            'description',
            'duration',
            'credits',
            'syllabus',
            'prerequisites',
            'professor',
            'max_enrollment',
            'current_enrollment',
            'offered_semester',
            'college',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['college'] = instance.college.name  
        return representation

    def create(self, validated_data):
        college_data = validated_data.pop('college')
        college = College.objects.get(uuid=college_data['uuid'])
        course = Course.objects.create(college=college, **validated_data)
        return course

    def update(self, instance, validated_data):
        college_data = validated_data.pop('college')
        college = College.objects.get(uuid=college_data['uuid'])
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.college = college
        instance.save()
        return instance




from rest_framework import serializers
from .models import University, College, Course

class CourseNestedSerializer(serializers.ModelSerializer):
    college = serializers.UUIDField()

    class Meta:
        model = Course
        fields = [
            'uuid',
            'name',
            'description',
            'duration',
            'credits',
            'syllabus',
            'prerequisites',
            'professor',
            'max_enrollment',
            'current_enrollment',
            'offered_semester',
            'college',
        ]

class CollegeNestedSerializer(serializers.ModelSerializer):
    university = serializers.UUIDField()
    courses = CourseNestedSerializer(many=True)

    class Meta:
        model = College
        fields = [
            'uuid',
            'name',
            'location',
            'dean',
            'contact_email',
            'contact_phone',
            'established_year',
            'number_of_departments',
            'student_population',
            'faculty_count',
            'annual_budget',
            'university',
            'courses',
        ]

class UniversityNestedSerializer(serializers.ModelSerializer):
    colleges = CollegeNestedSerializer(many=True)

    class Meta:
        model = University
        fields = [
            'uuid',
            'name',
            'location',
            'established_year',
            'website',
            'contact_email',
            'contact_phone',
            'description',
            'student_population',
            'faculty_count',
            'annual_budget',
            'accreditation',
            'university_grade',
            'colleges',
        ]



# from rest_framework import serializers
# from .models import University, College, Course

# class CourseNestedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Course
#         fields = '__all__'

# class CollegeNestedSerializer(serializers.ModelSerializer):
#     courses = CourseNestedSerializer(many=True)

#     class Meta:
#         model = College
#         fields = '__all__'

# class UniversityNestedSerializer(serializers.ModelSerializer):
#     colleges = CollegeNestedSerializer(many=True)

#     class Meta:
#         model = University
#         fields = '__all__'
