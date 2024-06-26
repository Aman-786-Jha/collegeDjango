import graphene
from graphene_django.types import DjangoObjectType
from .models import University, College, Course
from django.core.cache import cache

# Define a GraphQL type for University
class UniversityType(DjangoObjectType):
    class Meta:
        model = University
        fields = '__all__'

# Define a GraphQL type for College
class CollegeType(DjangoObjectType):
    class Meta:
        model = College
        fields = '__all__'

# Define a GraphQL type for Course
class CourseType(DjangoObjectType):
    class Meta:
        model = Course
        fields = '__all__'

class Query(graphene.ObjectType):
    universities = graphene.List(UniversityType)
    universities_list = graphene.List(UniversityType)
    universities_by_grade = graphene.List(UniversityType, grade=graphene.String())

    colleges = graphene.List(CollegeType)
    courses = graphene.List(CourseType)
    universities_count = graphene.Int(description="Total number of universities")
    course_name = graphene.String(description="Total number of courses")
    college_count = graphene.Int(description="Total number of colleges")

    def resolve_universities_list(self, info, **kwargs):
        return University.objects.all()
    
    def resolve_universities(self, info, **kwargs):
        return University.objects.all()
    
    def resolve_universities_by_grade(self, info, grade=None, **kwargs):
        query = University.objects.all()
        if grade:
            query = query.filter(university_grade=grade)
        return query

    def resolve_colleges(self, info, **kwargs):
        return College.objects.all()

    def resolve_courses(self, info, **kwargs):
        return Course.objects.all()
    
    def resolve_course_name(self, info, **kwargs):
        return Course.objects.filter(name="B.Tech")

    def resolve_universities_count(self, info, **kwargs):
        universities_count = cache.get('universities_count')
        print('universities_count_cache----->', universities_count)
        if universities_count is not None:
            print("University count data fetched from cache")
        else:
            print("University data fetched from database")
            universities_count = University.objects.all().count()
            cache.set('universities_count', universities_count, timeout=60)  # Cache for 1 minute
        return universities_count

    def resolve_college_count(self, info, **kwargs):
        college_count = cache.get('college_count')
        print('college_count----->', college_count)
        if college_count is not None:
            print("College count data fetched from cache")
        else:
            print("College data fetched from database")
            college_count = College.objects.all().count()
            cache.set('college_count', college_count, timeout=60)  # Cache for 1 minute
        return college_count

schema = graphene.Schema(query=Query)
