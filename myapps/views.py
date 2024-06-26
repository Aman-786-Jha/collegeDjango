from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.shortcuts import render
from .models import University

def dashboard(request):
    universities = University.objects.all()

    context = {
        'universities': universities,
    }

    return render(request, 'myapps/index.html', context)




def demo(request):
    return render(request, 'myapps/demo.html')


# import requests

# def get_universities_count():
#     endpoint_url = 'http://localhost:8000/graphql/'
#     query = '''
#     query {
#         universities {
#             id
#         }
#     }
#     '''
#     try:
#         response = requests.post(endpoint_url, json={'query': query})
#         response.raise_for_status()  # Check for HTTP errors
#         data = response.json()  # Parse JSON response
#         universities = data.get('data', {}).get('universities', [])
#         return len(universities)
#     except requests.exceptions.RequestException as e:
#         print(f"HTTP Request failed: {e}")
#         return 0  # Return 0 or handle error appropriately
#     except ValueError as e:
#         print(f"JSON Decode Error: {e}")
#         print("Response content:", response.content)  # Print response for debugging
#         return 0  # Return 0 or handle error appropriately


# from django.core.cache import cache
# from django.shortcuts import get_object_or_404, render
# from myapps.models import University

# def user_profile_view(request, user_id):
#     # Example: Assume 'user_id' is used to fetch a university's details
#     cache_key = f'university_profile_{user_id}'
#     university = cache.get(cache_key)
#     print('cache_key-------->',cache_key)
#     print('university-------->',university)

#     if university is not None:
#         print("University data fetched from cache")
#     else:
#         print("University data fetched from database")
#         # Assuming 'user_id' corresponds to a specific university ID
#         university = get_object_or_404(University, pk=user_id)
#         print('univsersity----------->',university)
#         cache.set(cache_key, university, timeout=60 * 15)  # Cache for 15 minutes
#         print('cache_key-------->',cache_key)
#         print('university-------->',university)

#     return render(request, 'myapps/university_profile.html', {'university': university})



from django.core.cache import cache
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from myapps.models import University
import json

def user_profile_view(request, user_id):
    cache_key = f'university_profile_{user_id}'
    university = cache.get(cache_key)
    print('cache_key-------->', cache_key)
    print('university-------->', university)

    if university is not None:
        print("University data fetched from cache")
    else:
        print("University data fetched from database")
        university = get_object_or_404(University, pk=user_id)
        print('university fetched from DB----------->', university)
        cache.set(cache_key, university, timeout=60 * 15)  # Cache for 15 minutes
        print('cache_key-------->', cache_key)
        print('university-------->', university)

    # Convert university object to JSON serializable format (optional, if needed)
    university_data = {
        'name': university.name,
        'location': university.location,
        'established_year': university.established_year,
        # Add more fields as needed
    }

    # Return JSON response
    return JsonResponse(university_data)



import requests
from django.shortcuts import render
from django.middleware.csrf import get_token

def university_count_view(request):
    query = """
    query {
        universitiesCount
        collegeCount
    }
    """
    try:
        # Get the CSRF token
        csrf_token = get_token(request)
        
        response = requests.post(
            f"http://{request.get_host()}/graphql/",  # Note the trailing slash
            json={'query': query},
            headers={'X-CSRFToken': csrf_token}
        )
        print("Response content:", response.content)  # Log the response content
        response.raise_for_status()  # Raises an error for HTTP status codes 4xx/5xx
        data = response.json()
        if 'errors' in data:
            raise Exception(data['errors'])
        total_universities = data['data']['universitiesCount']
        total_colleges = data['data']['collegeCount']
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        total_universities = None
    except Exception as e:
        print(f"GraphQL error: {e}")
        total_universities = None

    return render(request, 'myapps/index.html', {'total_universities': total_universities, 'total_colleges' : total_colleges})



def charts(request):
    return render(request, 'myapps/charts.html')



import json
import redis
from django.shortcuts import render
from django.conf import settings
from django.middleware.csrf import get_token
from myapps.models import University, College

# Initialize Redis connection
# redis_instance = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=1)

# def university_colleges_view(request):
#     cache_key = 'naac_a_universities'
#     cached_data = redis_instance.get(cache_key)
#     print('cached_data------------>', cached_data)

#     if cached_data:
#         data = json.loads(cached_data)
#         print('data------------>', data)
#     else:
#         print('fetching data from database')
#         universities = University.objects.filter(university_grade='A').prefetch_related('college_set')
#         data = {
#             'universities': [
#                 {
#                     'id': university.id,
#                     'name': university.name,
#                     'colleges': [{'id': college.id, 'name': college.name} for college in university.college_set.all()]
#                 }
#                 for university in universities
#             ]
#         }
#         redis_instance.set(cache_key, json.dumps(data))

#     csrf_token = get_token(request)
#     return render(request, 'myapps/index.html', {'csrf_token': csrf_token, 'data': data})



