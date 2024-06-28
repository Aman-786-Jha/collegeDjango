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






from rest_framework.permissions import AllowAny, AllowAny

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import get_object_or_404
from .models import University, College, Course
from .serializers import UniversitySerializer, CollegeSerializer, CourseSerializer
from rest_framework.permissions import AllowAny, AllowAny
from rest_framework.pagination import PageNumberPagination









page_param = openapi.Parameter(
    'page',
    openapi.IN_QUERY,
    description="Page number",
    type=openapi.TYPE_INTEGER
)

page_size_param = openapi.Parameter(
    'page_size',
    openapi.IN_QUERY,
    description="Number of items per page",
    type=openapi.TYPE_INTEGER
)

# Common manual parameter for authorization
authorization_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Bearer Token',
    type=openapi.TYPE_STRING
)

class UniversityCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        request_body=UniversitySerializer,
        responses={
            201: openapi.Response(description='Created', schema=UniversitySerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        try:
            serializer = UniversitySerializer(data=request.data)
            if serializer.is_valid():
                university = serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'University created successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UniversityListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK', schema=UniversitySerializer(many=True)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request):
        try:
            universities = University.objects.all()
            serializer = UniversitySerializer(universities, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'List of universities.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UniversityDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK', schema=UniversitySerializer),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request, uuid):
        try:
            university = get_object_or_404(University, uuid=uuid)
            serializer = UniversitySerializer(university)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'University details.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UniversityUpdateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        request_body=UniversitySerializer,
        responses={
            200: openapi.Response(description='OK', schema=UniversitySerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def put(self, request, uuid):
        try:
            university = get_object_or_404(University, uuid=uuid)
            serializer = UniversitySerializer(university, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'University updated successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class UniversityDeleteView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK'),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def delete(self, request, uuid):
        try:
            university = get_object_or_404(University, uuid=uuid)
            university.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'University deleted successfully.',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )




authorization_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description='Bearer Token',
    type=openapi.TYPE_STRING
)

class CollegeCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        # manual_parameters=[authorization_param],
        request_body=CollegeSerializer,
        responses={
            201: openapi.Response(description='Created', schema=CollegeSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        try:
            serializer = CollegeSerializer(data=request.data, context={'request': request})
            if serializer.is_valid():
                college = serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'College created successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

from rest_framework.pagination import PageNumberPagination

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class CollegeListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        manual_parameters=[page_param, page_size_param],
        responses={
            200: openapi.Response(description='OK', schema=CollegeSerializer(many=True)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request):
        try:
            colleges = College.objects.all()
            paginator = StandardResultsSetPagination()
            paginated_colleges = paginator.paginate_queryset(colleges, request, view=self)
            serializer = CollegeSerializer(paginated_colleges, many=True)
            return paginator.get_paginated_response(serializer.data)
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CollegeDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        # manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK', schema=CollegeSerializer),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request, uuid):
        try:
            college = get_object_or_404(College, uuid=uuid)
            serializer = CollegeSerializer(college)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'College details.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CollegeUpdateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        # manual_parameters=[authorization_param],
        request_body=CollegeSerializer,
        responses={
            200: openapi.Response(description='OK', schema=CollegeSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def put(self, request, uuid):
        try:
            college = get_object_or_404(College, uuid=uuid)
            serializer = CollegeSerializer(college, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'College updated successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CollegeDeleteView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        # manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK'),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def delete(self, request, uuid):
        try:
            college = get_object_or_404(College, uuid=uuid)
            college.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'College deleted successfully.',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import CourseSerializer
from .models import Course, College

class CourseCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=CourseSerializer,
        responses={
            201: openapi.Response(description='Created', schema=CourseSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        try:
            serializer = CourseSerializer(data=request.data)
            if serializer.is_valid():
                course = serializer.save()
                response_data = serializer.data
                response_data['college'] = course.college.name  # Display college name instead of UUID
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'Course created successfully.',
                        'responseData': response_data,
                    },
                    status=status.HTTP_201_CREATED
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseListView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK', schema=CourseSerializer(many=True)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request):
        try:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'List of courses.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

   


class CourseDetailView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK', schema=CourseSerializer),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def get(self, request, uuid):
        try:
            course = get_object_or_404(Course, uuid=uuid)
            serializer = CourseSerializer(course)
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Course details.',
                    'responseData': serializer.data,
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseUpdateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        request_body=CourseSerializer,
        responses={
            200: openapi.Response(description='OK', schema=CourseSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def put(self, request, uuid):
        try:
            course = get_object_or_404(Course, uuid=uuid)
            serializer = CourseSerializer(course, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        'responseCode': status.HTTP_200_OK,
                        'responseMessage': 'Course updated successfully.',
                        'responseData': serializer.data,
                    },
                    status=status.HTTP_200_OK
                )
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class CourseDeleteView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        #manual_parameters=[authorization_param],
        responses={
            200: openapi.Response(description='OK'),
            404: openapi.Response(description='Not Found', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def delete(self, request, uuid):
        try:
            course = get_object_or_404(Course, uuid=uuid)
            course.delete()
            return Response(
                {
                    'responseCode': status.HTTP_200_OK,
                    'responseMessage': 'Course deleted successfully.',
                },
                status=status.HTTP_200_OK
            )
        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .serializers import UniversityNestedSerializer
from .models import University, College, Course




class UniversityCollegeCourseCreateView(APIView):
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        request_body=UniversityNestedSerializer,
        responses={
            201: openapi.Response(description='Created', schema=UniversityNestedSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )
    def post(self, request):
        try:
            serializer = UniversityNestedSerializer(data=request.data)
            if serializer.is_valid():
                university_data = serializer.validated_data
                colleges_data = university_data.pop('colleges', [])

                # Create University
                university = University.objects.create(**university_data)

                # Create Colleges and associated Courses
                for college_data in colleges_data:
                    courses_data = college_data.pop('courses', [])

                    # Assign University instance to College
                    college_data['university'] = university  # Assigning the actual University instance

                    # Create College
                    college = College.objects.create(**college_data)

                    # Create Courses for the College
                    for course_data in courses_data:
                        course_data['college'] = college  # Assigning the actual College instance
                        Course.objects.create(**course_data)

                # Serialize and return response data
                response_data = UniversityNestedSerializer(university).data
                return Response(
                    {
                        'responseCode': status.HTTP_201_CREATED,
                        'responseMessage': 'University, College, and Courses created successfully.',
                        'responseData': response_data,
                    },
                    status=status.HTTP_201_CREATED
                )
            
            # Return bad request response if serializer is not valid
            return Response(
                {
                    'responseCode': status.HTTP_400_BAD_REQUEST,
                    'responseMessage': 'Invalid data provided.',
                    'responseData': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        except Exception as e:
            # Handle any exceptions and return internal server error response
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        






from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UniversityNestedSerializer

class UniversityCollegeCourseBatchCreateView(APIView):
    permission_classes = [AllowAny]
    @swagger_auto_schema(
        request_body=UniversityNestedSerializer,
        responses={
            201: openapi.Response(description='Created', schema=UniversityNestedSerializer),
            400: openapi.Response(description='Bad Request', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
            500: openapi.Response(description='Internal Server Error', schema=openapi.Schema(type=openapi.TYPE_OBJECT)),
        }
    )

    def post(self, request):
        try:
            universities_data = request.data
            created_universities = []

            for university_data in universities_data:
                serializer = UniversityNestedSerializer(data=university_data)
                if serializer.is_valid():
                    # Save University and related Colleges and Courses
                    university = serializer.save()
                    created_universities.append(university)
                else:
                    return Response(
                        {
                            'responseCode': status.HTTP_400_BAD_REQUEST,
                            'responseMessage': 'Invalid data provided.',
                            'responseData': serializer.errors,
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

            return Response(
                {
                    'responseCode': status.HTTP_201_CREATED,
                    'responseMessage': 'Universities, Colleges, and Courses created successfully.',
                    'responseData': UniversityNestedSerializer(created_universities, many=True).data,
                },
                status=status.HTTP_201_CREATED
            )

        except Exception as e:
            return Response(
                {
                    'responseCode': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'responseMessage': 'Something went wrong! Please try again.',
                    'responseData': {'error': str(e)},
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )







################################ MULTIPLE UNIVERSITY COLLEGE ASYNS #################################


from django.http import JsonResponse
from django.shortcuts import render
import asyncio
import aiohttp
import json

async def create_data(session, url, data):
    async with session.post(url, json=data) as response:
        return await response.json()

async def process_data(base_url, data):
    url = f'{base_url}/api/create-university-college-course/' 
    headers = {'Content-Type': 'application/json'}
    
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for item in data:
            task = create_data(session, url, item)
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        return responses

def create_universities_view(request):
    if request.method == 'POST':
        json_data = request.POST.get('json_data')
        base_url = f'http://{request.get_host()}'
        try:
            data = json.loads(json_data)
            responses = asyncio.run(process_data(base_url, data))
            return JsonResponse({'responses': responses})
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON provided'}, status=400)
    return render(request, 'myapps/create_universities.html')