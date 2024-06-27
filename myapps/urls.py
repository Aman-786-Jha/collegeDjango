
from myapps.views import *   
from django.urls import path
from graphene_django.views import GraphQLView
from myapps.schema import schema
from django.views.decorators.csrf import csrf_exempt
from . import views 
urlpatterns = [
    # ...
    path('', views.dashboard, name='dashboard'), 
    path('demo/', views.demo, name='demo'), 
    path('charts/', views.charts, name='charts'), 
    path('university-count/', views.university_count_view, name='university_count'),
    path('user-profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('graphql/', (GraphQLView.as_view(graphiql=True, schema=schema))), 



    ########################################## REST APIs  ###############################
   path('university/create/', UniversityCreateView.as_view(), name='university-create'),
    path('university/list/', UniversityListView.as_view(), name='university-list'),
    path('university/detail/<uuid>/', UniversityDetailView.as_view(), name='university-detail'),
    path('university/update/<uuid>/', UniversityUpdateView.as_view(), name='university-update'),
    path('university/delete/<uuid>/', UniversityDeleteView.as_view(), name='university-delete'),

    path('college/create/', CollegeCreateView.as_view(), name='college-create'),
    path('college/list/', CollegeListView.as_view(), name='college-list'),
    path('college/detail/<uuid>/', CollegeDetailView.as_view(), name='college-detail'),
    path('college/update/<uuid>/', CollegeUpdateView.as_view(), name='college-update'),
    path('college/delete/<uuid>/', CollegeDeleteView.as_view(), name='college-delete'),

    path('course/create/', CourseCreateView.as_view(), name='course-create'),
    path('course/list/', CourseListView.as_view(), name='course-list'),
    path('course/detail/<uuid>/', CourseDetailView.as_view(), name='course-detail'),
    path('course/update/<uuid>/', CourseUpdateView.as_view(), name='course-update'),
    path('course/delete/<uuid>/', CourseDeleteView.as_view(), name='course-delete'),



    path('api/create-university-college-course/', UniversityCollegeCourseCreateView.as_view(), name='create-university-college-course'),
    # path('api/create-university-college-course-multiple/', UniversityCollegeCourseBatchCreateView.as_view(), name='multi-create-university-college-course'),
    
    
]
