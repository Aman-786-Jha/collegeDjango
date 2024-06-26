
from . import views  # Ensure you import views correctly
from django.urls import path
from graphene_django.views import GraphQLView
from myapps.schema import schema
from django.views.decorators.csrf import csrf_exempt
urlpatterns = [
    # ...
    path('', views.dashboard, name='dashboard'), 
    path('demo/', views.demo, name='demo'), 
    path('charts/', views.charts, name='charts'), 
    path('university-count/', views.university_count_view, name='university_count'),
    path('user-profile/<int:user_id>/', views.user_profile_view, name='user_profile'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True, schema=schema))), # Given that schema path is defined in GRAPHENE['SCHEMA'] in your settings.py

]
