import os
import requests
import json
import datetime
import jwt
import random
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .serializers import UserSerializer
from .models import User, RandomAPODText


# Twilo Environment Variables: do not change here
ACCOUNT_SID = os.environ.get('TWILIO_ACCOUNT_SID')
AUTH_TOKEN = os.environ.get('TWILIO_AUTH_TOKEN')
TWILIO_CLIENT = Client(ACCOUNT_SID, AUTH_TOKEN)

# Create your views here.
@api_view(['GET'])
def index(request):
    urlist = [
        'GET: /api',
        'POST: /api/register',
        'POST: /api/login',
        'GET: /api/users',
        'PUT: /api/toggle-subscription/<int:id>/',
        'POST: /api/logout',
    ]
    return Response(urlist, status=200)

@api_view(['POST'])
def register_user(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    send_welcome_message(serializer.data['name'], serializer.data['phone'])
    return Response(serializer.data)


@api_view(['POST'])
def check_user(request):
    email = request.data['email']
    password = request.data['password']

    user = User.objects.filter(email=email).first()

    if user is None:
        raise AuthenticationFailed('User not found!')

    if not user.check_password(password):
        raise AuthenticationFailed('Incorrect password!')

    payload = {
        'id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
        'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, os.environ.get(
        'JWT_SECRET'), algorithm='HS256')

    response = Response()

    response.set_cookie(key='jwt', value=token, httponly=True)
    response.data = {
        'user': UserSerializer(user).data,
        'jwt': token,
    }
    return response


@api_view(['GET'])
def get_users(request):
    token = request.COOKIES.get('jwt')

    if not token:
        raise AuthenticationFailed('Unauthenticated!')

    try:
        payload = jwt.decode(token, 'secret', algorithm=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed('Unauthenticated!')

    user = User.objects.filter(id=payload['id']).first()
    serializer = UserSerializer(user)
    return Response(serializer.data)


@api_view(['POST'])
def logOut(request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {
        'message': 'success'
    }
    return response

@api_view(['PUT', 'PATCH'])
def toggle_subscriptions(request, id):
    user = User.objects.filter(id=id).first()
    user.isSubscribed = not user.isSubscribed
    user.save()
    if user.isSubscribed:
        return Response({'id':user.id,
                        'name':user.name,
                        'isSubscribed':user.isSubscribed,
                        'message': 'You are now subscribed to NASA APOD Texting Service'
                        })
    else:
        return Response({'id':user.id,
                        'name':user.name,
                        'isSubscribed':user.isSubscribed,
                        'message': 'You are now unsubscribed from NASA APOD Texting Service'
                        })


#main function
def send_NASA_APOD():
    print("sending message........", datetime.datetime.now())
    phone_numbers = get_phone_numbers()
    
    for phone_number in phone_numbers:
        did_send = send_text(phone_number)
        if did_send:
            print("sent to ", phone_number)
        else:
            print("failed to send to ", phone_number)
    
    print("done sending messages", datetime.datetime.now())

def get_phone_numbers():
    phone_numbers = []
    for user in User.objects.all():
        if user.isSubscribed:
            phone_numbers.append(user.phone)
    return phone_numbers

def get_nasaAPOD():
    url="https://api.nasa.gov/planetary/apod"
    params = {'api_key':os.environ.get('NASA_API_KEY')}

    try:
        res = requests.get(url, params=params)
        if res.ok:
            response = json.loads(res.text)
            print("Retrieved data from NASA API")
            return response
    except requests.exceptions.RequestException as requestException:
        print("RequestException: ", requestException)

def send_apod_text(apod_data: dict, phone_number: str):
    try:
        if apod_data['media_type'] == 'image':
            message = TWILIO_CLIENT.messages.create(
                to=phone_number,
                from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                body= f'\nToday\'s NASA Astronomy Picture of the Day is: {apod_data["title"]}.\n\n{apod_data["explanation"]}',
                media_url=apod_data['url']
            )
            print(message.sid)
        elif apod_data['media_type'] == 'video':
            message = TWILIO_CLIENT.messages.create(
            to=phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            body= f'\nToday\'s NASA Astronomy Picture of the Day is: {apod_data["title"]}.\n\n{apod_data["explanation"]} \n\n Video URL: {apod_data["url"]}'
            )
            print(message.sid)
        else:
            message = TWILIO_CLIENT.messages.create(
            to=phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            body= f'\nToday\'s NASA Astronomy Picture of the Day is: {apod_data["title"]}.\n\n{apod_data["explanation"]}'
            )
            print(message.sid)
        return True
    except TwilioRestException as twilioRestException:
        print("TwilioRestException: ", twilioRestException)
        return False
    
def send_text(phone_number: str):
    apod_data = get_nasaAPOD()
    if apod_data is None:
        print("Sending back-up notification ..")
        send_backUp_message(phone_number)
        return True # return true because we still want to send the backup message
    return send_apod_text(apod_data, phone_number)

def send_welcome_message(user_name: str, phone_number: str):
    try:
        message = TWILIO_CLIENT.messages.create(
            to=phone_number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            body= f'\nWelcome to NASA APOD Texting Service\nHey {user_name}!\nYou will now receive a text message with today\'s NASA Astronomy Picture of the Day every day.'
        )
        print(message.sid)
    except TwilioRestException as twilioRestException:
        print("TwilioRestException: ", twilioRestException)

#store text message in database for future use to be called weekly
def store_message_weekly():
    apod_data = get_nasaAPOD()
    if apod_data is None:
        return
    try:
        random_message = RandomAPODText.objects.create(title=apod_data['title'],
                                                       media_type=apod_data['media_type'], 
                                                       link=apod_data['url'], 
                                                       message=apod_data['explanation']
                                                       )

        random_message.save()
        print("Stored message in database")
    except Exception as exception:
        print("Exception: ", exception)     
  
#get random message from database
def get_random_message():
    try:
        count = RandomAPODText.objects.count()
        random_index = random.randint(0, count - 1)
        random_message = RandomAPODText.objects.all()[random_index]
        return random_message
    except Exception as exception:
        print("Exception: ", exception)

def send_backUp_message(phone_number: str):
    apod_data = get_random_message()
    if apod_data is None:
        return
    return send_apod_text(apod_data, phone_number)