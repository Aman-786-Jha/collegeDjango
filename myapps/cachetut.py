# import redis

# r = redis.Redis(host='127.0.0.1', port=6379, db=1)
# keys = r.keys('*')
# for key in keys:
#     print(key, r.get(key))


import asyncio
import aiohttp
import json

async def create_data(session, url, data):
    async with session.post(url, json=data) as response:
        print('response----------->', response.json())
        
        return await response.json()

async def main():
    url = 'http://127.0.0.1:8000/api/create-university-college-course/' 
    headers = {'Content-Type': 'application/json'}

    
    data = [
        {
            "name": "University kk",
            "location": "City A",
            "established_year": 2000,
            "website": "https://universitya.com",
            "contact_email": "info@canara.com",
            "contact_phone": "1234567890",
            "description": "University A description",
            "student_population": 5000,
            "faculty_count": 300,
            "annual_budget": "1000000.00",
            "accreditation": "Accreditation A",
            "university_grade": "A",
            "colleges": [
                {
                    "name": "College A1",
                    "location": "Location A1",
                    "dean": "Dean A1",
                    "contact_email": "dean@collegea1.com",
                    "contact_phone": "9876543210",
                    "established_year": 2010,
                    "number_of_departments": 10,
                    "student_population": 2000,
                    "faculty_count": 100,
                    "annual_budget": "500000.00",
                    "university": "384db528-f436-437a-92f3-9f61bab773eb",
                    "courses": [
                        {
                            "name": "B.Tech",
                            "description": "Course A1 description",
                            "duration": 4,
                            "credits": 120,
                            "syllabus": "Course A1 syllabus",
                            "prerequisites": "Course A1 prerequisites",
                            "professor": "Professor A1",
                            "max_enrollment": 200,
                            "current_enrollment": 150,
                            "offered_semester": "Spring",
                            "college": "259deac8-1a6a-4340-b699-13248749940a"
                        }
                    ]
                }
            ]
        },
        {
            "name": "University B",
            "location": "City B",
            "established_year": 1995,
            "website": "https://universityb.com",
            "contact_email": "info@universityb.com",
            "contact_phone": "9876543210",
            "description": "University B description",
            "student_population": 7000,
            "faculty_count": 500,
            "annual_budget": "1500000.00",
            "accreditation": "Accreditation B",
            "university_grade": "B",
            "colleges": [
                {
                    "name": "College B1",
                    "location": "Location B1",
                    "dean": "Dean B1",
                    "contact_email": "dean@collegeb1.com",
                    "contact_phone": "1234567890",
                    "established_year": 2005,
                    "number_of_departments": 8,
                    "student_population": 1500,
                    "faculty_count": 80,
                    "annual_budget": "400000.00",
                    "university": "384db528-f436-437a-92f3-9f61bab773eb",
                    "courses": [
                        {
                            "name": "B.Tech",
                            "description": "Course B1 description",
                            "duration": 3,
                            "credits": 90,
                            "syllabus": "Course B1 syllabus",
                            "prerequisites": "Course B1 prerequisites",
                            "professor": "Professor B1",
                            "max_enrollment": 150,
                            "current_enrollment": 120,
                            "offered_semester": "Fall",
                            "college": "259deac8-1a6a-4340-b699-13248749940a"
                        }
                    ]
                }
            ]
        }
    ]

    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = []
        for item in data:
            task = create_data(session, url, item)
            print('task----------------->', task)
            tasks.append(task)
        responses = await asyncio.gather(*tasks)
        for response in responses:
            print(response)

if __name__ == '__main__':
    asyncio.run(main())

