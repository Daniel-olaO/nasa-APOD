import os
import requests
import json
import datetime
import jwt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.exceptions import AuthenticationFailed
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException
from .serializers import UserSerializer
from .models import User


# Create your views here.
class RouteListView(APIView):
    def get(self, request):
        urlist = [
            'GET: /api',
            'POST: /api/register',
            'POST: /api/login',
            'GET: /api/users',
            'POST: /api/toggle-subscription/<int:id>/',
            'POST: /api/logout',
        ]
        return Response(urlist, status=200)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        sendWelcomeMessage(serializer.data['phone'], serializer.data['name'])
        return Response(serializer.data)


class LoginView(APIView):
    def post(self, request):
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


class UserView(APIView):

    def get(self, request):
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


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response
class SubscriptionView(APIView):
    def post(self, request, id):
        user = User.objects.filter(id=id).first()
        user.isSubscribed = not user.isSubscribed
        user.save()
        if user.isSubscribed:
            return Response({'name':user.email,
                            'isSubscribed':user.isSubscribed,
                            'message': 'You are now subscribed to NASA APOD Texting Service'
                            })
        else:
            return Response({'name':user.email,
                            'isSubscribed':user.isSubscribed,
                            'message': 'You are now unsubscribed from NASA APOD Texting Service'
                            })

def getNumbers():
    numbers = []
    for user in User.objects.all():
        if user.isSubscribed:
            numbers.append(user.phone)
    return numbers

def nasaAPOD():
    url="https://api.nasa.gov/planetary/apod"
    params = {'api_key':os.environ.get('NASA_API_KEY')}

    try:
        res = requests.get(url, params=params)
        if res.ok:
            response = json.loads(res.text)
            return response
    except requests.exceptions.RequestException as e:
        print(e)
        return None

def sendText(numbers):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    data = nasaAPOD()
    client = Client(account_sid, auth_token)
    for number in numbers:
        try:
            message = client.messages.create(
                to=number,
                from_=os.environ.get('TWILIO_PHONE_NUMBER'),
                body= f'\nToday\'s NASA Astronomy Picture of the Day is: {data["title"]}.\n\n{data["explanation"]}',
                media_url=data['hdurl']
            )
            print(message.sid)
        except TwilioRestException as e:
            print(e)

@api_view(['GET'])
def sendAPOD(request):
    numbers = getNumbers()
    sendText(numbers)
    return Response({'message':'success'})

def sendWelcomeMessage(name, number):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            to=number,
            from_=os.environ.get('TWILIO_PHONE_NUMBER'),
            body= f'Welcome to NASA APOD Texting Service, {name}! You will now receive a text message with today\'s NASA Astronomy Picture of the Day every day.'
        )
        print(message.sid)
    except TwilioRestException as e:
        print(e)