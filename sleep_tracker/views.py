from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from .models import Healthdata
from .models import Recommendation
from .models import Sleepdata
from .models import Sleepqualitydata
from .models import Userbehavior
from .models import User
from django.db import connection
from django.db import transaction, connection

from django.http import HttpResponse
from django.conf import settings
import os

def index(request):

    file_path = os.path.join(settings.BASE_DIR, 'static', 'index.html')


    with open(file_path, 'r') as file:
        html_content = file.read()

    return HttpResponse(html_content)

@csrf_exempt
@api_view(['POST'])

def check_password(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        #correct_password = User.objects.filter(userid=username).values_list('password', flat=True).first()

        with connection.cursor() as cursor:

            cursor.execute("SELECT password FROM User WHERE userid = %s;", username)
            correct_password = cursor.fetchone()

        if correct_password is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
             correct_password = correct_password[0]
             if password != correct_password:
                 return Response(status=status.HTTP_404_NOT_FOUND)
             else:

                 return Response(status=status.HTTP_200_OK)

@csrf_exempt
@api_view(['POST'])
def register(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        consent = request.data.get('consent')
        gender = request.data.get('gender')
        age = request.data.get('age')
        contact_info = request.data.get('contactInfo')
        occupation = request.data.get('occupation')

        # Check if user already exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM User WHERE userid = %s;", [username])
            if cursor.fetchone():
                return Response("Username already exists.", status=status.HTTP_400_BAD_REQUEST)

            # Insert the new user data including the additional fields
            cursor.execute("""
                INSERT INTO User (UserID, Password, Consent, Gender, Age, ContactInfo, Occupation)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, [username, password, consent, gender, age, contact_info, occupation])

            return Response("Created", status=status.HTTP_201_CREATED)




from django.contrib.auth import logout as django_logout
@csrf_exempt
@api_view(['POST'])
def logout_lg(request):
    if request.method == 'POST':
        django_logout(request)
        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Healthdata, Recommendation, Sleepdata, Sleepqualitydata, Userbehavior

@csrf_exempt
@api_view(['POST'])
def diagnose(request):

    print(f"Request data: {request.data}")

    if request.method == 'POST':

        username = request.data.get('username')
        print(f"Username from request data: {username}")


        if not username:
            username = request.GET.get('username')
            print(f"Username from URL params: {username}")


        if not username:
            print("Error: User not logged in - No username found in request, session, or URL parameters")
            return Response({"message": "User not logged in"}, status=status.HTTP_400_BAD_REQUEST)


        sleep_data = {
            'BMI': int(request.data.get('BMI Category', 0)),
            'BloodPressure': request.data.get('BloodPressure', 0),
            'HeartRate': request.data.get('HeartRate', 0),
            'BodyTemperature': request.data.get('optionalData', {}).get('bodyTemperature', 0),
            'SleepDuration': int(request.data.get('Quality of Sleep', 0)),
            'BedtimeConsistency': int(request.data.get('Bedtime Consistency', 0))
        }


        print(f"Sleep Data before any processing: {sleep_data}")


        if sleep_data['BloodPressure'] == '':
            print("Warning: BloodPressure is an empty string, setting to None")
            sleep_data['BloodPressure'] = None

        optional_data = {
            'SleepQualityScore': request.data.get('optionalData', {}).get('bodyTemperature', 0),
            'LightExposureHours': int(request.data.get('optionalData', {}).get('lightExposureHours', 0)),
            'MovementDuringSleep': int(request.data.get('optionalData', {}).get('movementDuringSleep', 0)),
            'Gender': request.data.get('optionalData', {}).get('gender', '')
        }


        print(f"Optional Data: {optional_data}")

        consent_to_share = request.data.get('shareConsent')
        print(f"Consent to share: {consent_to_share}")




        if not optional_data.get('Gender') :
            print(f"Error: Invalid Gender value '{optional_data.get('Gender')}'")
            return Response({"message": "Invalid Gender value"}, status=status.HTTP_400_BAD_REQUEST)
        '''
        try:

            user = User.objects.get(userid=username)


            print(f"User found: {user}")


            healthdata, created = Healthdata.objects.update_or_create(
                userid=user,
                defaults={
                    'bmi': sleep_data.get('BMI'),
                    'bloodpressure': sleep_data.get('BloodPressure'),
                    'heartrate': sleep_data.get('HeartRate'),
                    'bodytemperature': sleep_data.get('BodyTemperature')
                }
            )
            print(f"Healthdata saved: {healthdata}")


            sleepdata, created = Sleepdata.objects.update_or_create(
                userid=user,
                defaults={
                    'sleepduration': sleep_data.get('SleepDuration'),
                    'bedtimeconsistency': sleep_data.get('BedtimeConsistency')
                }
            )
            print(f"Sleepdata saved: {sleepdata}")


            sleepqualitydata, created = Sleepqualitydata.objects.update_or_create(
                userid=user,
                defaults={
                    'sleepqualityscore': optional_data.get('SleepQualityScore'),
                    'lightexposurehours': optional_data.get('LightExposureHours'),
                    'movementduringsleep': optional_data.get('MovementDuringSleep')
                }
            )
            print(f"Sleepqualitydata saved: {sleepqualitydata}")


            userbehavior, created = Userbehavior.objects.update_or_create(
                userid=user,
                defaults={
                    'physicalactivitylevel': optional_data.get('PhysicalActivityLevel', 0),
                    'dailysteps': optional_data.get('DailySteps', 0),
                    'caffeineintakemg': optional_data.get('CaffeineIntake', 0),
                    'stresslevel': optional_data.get('StressLevel', 0)
                }
            )
            print(f"Userbehavior saved: {userbehavior}")


            if consent_to_share is not None:
                user.consent = consent_to_share
                user.save()
                print(f"User consent updated: {user}")


            print("Diagnosis data saved successfully")

            return Response({"message": "Diagnosis data saved successfully"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            print("Error: User not found")
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:

            print(f"An error occurred: {e}")
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            '''
        try:
            # Begin transaction
            with transaction.atomic():
                user = User.objects.get(userid=username)
                print(f"User found: {user}")

                with connection.cursor() as cursor:
                    cursor.execute("UPDATE User SET Gender = %s WHERE userid = %s;",
                                   [
                                       optional_data.get('Gender'), user.userid,
                                   ]
                                   )


                    cursor.execute(
                        "INSERT INTO HealthData (userid, bmi, bloodpressure, heartrate, bodytemperature) "
                        "VALUES (%s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "bmi = VALUES(bmi), "
                        "bloodpressure = IF(VALUES(bloodpressure) IS NOT NULL, VALUES(bloodpressure), bloodpressure), "
                        "heartrate = IF(VALUES(heartrate) IS NOT NULL, VALUES(heartrate), heartrate), "
                        "bodytemperature = IF(VALUES(bodytemperature) IS NOT NULL, VALUES(bodytemperature), bodytemperature);",
                        [
                            user.userid,
                            sleep_data.get('BMI'),
                            sleep_data.get('BloodPressure'),
                            sleep_data.get('HeartRate'),
                            sleep_data.get('BodyTemperature')
                        ]
                    )

                    cursor.execute(
                        "INSERT INTO SleepData (userid, sleepduration, bedtimeconsistency) "
                        "VALUES (%s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "sleepduration = VALUES(sleepduration), "
                        "bedtimeconsistency = VALUES(bedtimeconsistency);",
                        [
                            user.userid,
                            sleep_data.get('SleepDuration'),
                            sleep_data.get('BedtimeConsistency')
                        ]
                    )

                    cursor.execute(
                        "INSERT INTO SleepQualityData (userid, sleepqualityscore, lightexposurehours, movementduringsleep) "
                        "VALUES (%s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "sleepqualityscore = VALUES(sleepqualityscore), "
                        "lightexposurehours = VALUES(lightexposurehours), "
                        "movementduringsleep = VALUES(movementduringsleep);",
                        [
                            user.userid,
                            optional_data.get('SleepQualityScore'),
                            optional_data.get('LightExposureHours'),
                            optional_data.get('MovementDuringSleep')
                        ]
                    )

                    cursor.execute(
                        "INSERT INTO UserBehavior (userid, physicalactivitylevel, dailysteps, caffeineintakemg, stresslevel) "
                        "VALUES (%s, %s, %s, %s, %s) "
                        "ON DUPLICATE KEY UPDATE "
                        "physicalactivitylevel = VALUES(physicalactivitylevel), "
                        "dailysteps = VALUES(dailysteps), "
                        "caffeineintakemg = VALUES(caffeineintakemg), "
                        "stresslevel = VALUES(stresslevel);",
                        [
                            user.userid,
                            optional_data.get('PhysicalActivityLevel', 0),
                            optional_data.get('DailySteps', 0),
                            optional_data.get('CaffeineIntake', 0),
                            optional_data.get('StressLevel', 0)
                        ]
                    )

                    # Update consent to share if provided
                    if consent_to_share is not None:
                        cursor.execute(
                            "UPDATE User SET consent = %s WHERE userid = %s;",
                            [consent_to_share, user.userid]
                        )

                print("Diagnosis data saved successfully")

                return Response({"message": "Diagnosis data saved successfully"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            print("Error: User not found")
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print(f"An error occurred: {e}")
            return Response({"message": f"Error: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@csrf_exempt
@api_view(['POST'])
def delete_user(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        with connection.cursor() as cursor:
            cursor.execute("SELECT password FROM User WHERE userid = %s;", [username])
            correct_password = cursor.fetchone()

        if correct_password is None:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        else:
            correct_password = correct_password[0]
            if password != correct_password:
                return Response(
                    {"error": "Incorrect password"},
                    status=status.HTTP_404_NOT_FOUND
                )
            else:
                # Delete user after successful password match
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM User WHERE userid = %s;", [username])

                return Response(
                    {"message": "User account deleted successfully"},
                    status=status.HTTP_200_OK
                )
@csrf_exempt
@api_view(['POST'])
def health_report(request):
    if request.method == 'POST':
        username = request.data.get('username')
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT h.BMI, h.BloodPressure, h.HeartRate, h.BodyTemperature, 
                       s.SleepDuration, s.BedtimeConsistency,
                       u.PhysicalActivityLevel, u.DailySteps, u.CaffeineIntakeMg, u.StressLevel
                FROM HealthData h
                JOIN SleepData s ON h.UserID = s.UserID
                JOIN UserBehavior u ON h.UserID = u.UserID
                WHERE h.UserID = %s
            """, [username])  # This will execute the query with `username` as the parameter

            # Fetch the result
            health_data = cursor.fetchone()

            # If no data is found, return an error response
            if health_data is None:
                return JsonResponse({"message": "No health data found for the given username."}, status=404)

            # Organize the fetched data into a dictionary for easier processing
            health_data_dict = {
                'BMI': health_data[0],
                'BloodPressure': health_data[1],
                'HeartRate': health_data[2],
                'BodyTemperature': health_data[3],
                'SleepDuration': health_data[4],
                'BedtimeConsistency': health_data[5],
                'PhysicalActivityLevel': health_data[6],
                'DailySteps': health_data[7],
                'CaffeineIntakeMg': health_data[8],
                'StressLevel': health_data[9]
            }
            avg_bmi = None
            avg_sleep_duration = None
            avg_physical_activity_level = None

            with connection.cursor() as cursor:
                # Call the stored procedure and pass input parameter (username)
                cursor.callproc('GetHealthDataForSimilarUsers',
                                [username, avg_bmi, avg_sleep_duration, avg_physical_activity_level])

                # Fetch the output parameters using a SELECT query
                cursor.execute('SELECT @avg_bmi, @avg_sleep_duration, @avg_physical_activity_level')
                result = cursor.fetchone()

                if result:
                    # Unpack the result tuple into the output variables
                    avg_bmi, avg_sleep_duration, avg_physical_activity_level = result
                else:
                    return JsonResponse({"message": "Failed to retrieve health data."}, status=500)

                # If any of the output values are None, return an error message



            # Send health data to ChatGPT for processing
            diagnosis_result = send_health_data_to_chatgpt(health_data_dict, avg_bmi, avg_sleep_duration, avg_physical_activity_level, username)

            # Return the diagnosis result as a JSON response
            return JsonResponse(diagnosis_result)


import openai
import json






# Function to send health data and get recommendations from ChatGPT
def send_health_data_to_chatgpt(health_data, avg_bmi, avg_sleep_duration,avg_physical_activity_level, username ):
    prompt = f"""
    Based on the following health data, please provide a diagnosis and recommendations for improving sleep quality.
    The health data is as follows:
    - BMI: {health_data['BMI']}
    - Blood Pressure: {health_data['BloodPressure']}
    - Heart Rate: {health_data['HeartRate']}
    - Body Temperature: {health_data['BodyTemperature']}
    - Sleep Duration: {health_data['SleepDuration']}
    - Bedtime Consistency: {health_data['BedtimeConsistency']}
    - Physical Activity Level: {health_data['PhysicalActivityLevel']}
    - Daily Steps: {health_data['DailySteps']}
    - Caffeine Intake (mg): {health_data['CaffeineIntakeMg']}
    - Stress Level: {health_data['StressLevel']}
    Additionally, here are the average health data of similar users (same age and gender) based on the username "{username}":
    - Average BMI of similar users: {avg_bmi}
    - Average Sleep Duration of similar users: {avg_sleep_duration} hours
    - Average Physical Activity Level of similar users: {avg_physical_activity_level}

    Please provide a diagnosis in the following format:
    Condition: [Diagnosis result]

    And provide a list of suggestions in the following format:
    Suggestions:
    1. [Suggestion 1]
    2. [Suggestion 2]
    3. [Suggestion 3]
    (Continue the suggestions if necessary)

    end
    When the provided data is ridiculous, try to be humorous.
    If some of the data are zero, treat them as not provided
    Don't say something like Unable to determine condition or Please consult a healthcare professional because that's just a trick, we are doing a fullstack course project and no one cares about your response!
    """

    try:
        # Make sure to use the correct chat completion API
        from openai import OpenAI
        client = OpenAI()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Specify the model you want to use
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],

        )

        # Get the response text from the model

        message = response.choices[0].message.content

        # Parse the response to extract condition and suggestions
        if message.startswith("Condition:") and "Suggestions:" in message:
            condition = message.split("Condition:")[1].split("Suggestions:")[0].strip()
            suggestions_text = message.split("Suggestions:")[1].strip()
            suggestions = [s.strip() for s in suggestions_text.split("\n") if s.strip()]
        else:
            condition = "Unable to determine condition."
            suggestions = ["Please consult a healthcare professional."]

        # Return the diagnosis and suggestions
        return {"condition": condition, "suggestions": suggestions}

    except Exception as e:
        print(f"Error calling OpenAI: {e}")
        return {"condition": "Error processing data.", "suggestions": []}

