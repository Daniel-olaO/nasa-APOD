# Nasa Astronomical Picture of the Day Texting Service(server)

This is a Django API that sends the NASA Astronomy Picture of the Day to a user's phone number via text message. This service gets the daily picture and description from the Nasa-APOD API and sends it to the user's phone number via text message using the Twilio API.

## Table of Contents

- [Motivation](#motivation)
- [requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Demo](#demo)
- [LINK](#link)
- [Tools](#tools)
- [Author](#author)
- [references](#references)

# Motivation

I created this app to share my love of space and astronomy with others. I also wanted to create a fun and easy way to learn about the universe.

# requirements

Nasa-APOD Texting Service requires the following to run:

- Nasa API key
- Twilo Account

# Installation

## Virtual Environment

Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

## Create .env file

```bash
touch .env
```

## Add the following to the .env file

- [Database](#database)
- [Nasa API](#nasa-api)
- [Twilio API](#twilio-api)
- [Secret Key](#secret-key)
- [JWT](#jwt)

### Database

```bash
DB_NAME=your_database_name
DB_USER=your_database_user
DB_PASSWORD=your_database_password
DB_HOST=your_database_host
DB_PORT=your_database_port
```

### Nasa API

```bash
NASA_API_KEY=your_nasa_api_key
```

### Twilio API

```bash
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
TWILIO_PHONE_NUMBER=your_twilio_phone_number
```

### Secret Key

```bash
SECRET_KEY=your_secret_key
```

### JWT

```bash
JWT_SECRET_KEY=your_jwt_secret_key
```

## Migrate Database

```bash
python manage.py makemigration api
python manage.py migrate
```

# Usage

use the following command to start the server:

```bash
python manage.py runserver
```

users must sign up with a name, a phone number, an email address and a password. The phone number must have the country code of the country in which the phone number originated: Canada -> +16574832074. The email address must be valid. The user will receive a welcome text message. The user will also receive a text message every day with the NASA Astronomy Picture of the Day.

# Demo

https://nasa-client-production.up.railway.app/

# LINK

This app is deployed on AWS EC2 and can be accessed at:
http://3.85.54.30:8000/api/

# Tools

This app was created using the following tools:
Django, Django Rest Framework, docker, PostgreSQL, Nasa-APOD API, Twilio API

# Author

Nasa-APOD Texting Service was created by:

### Daniel Adedeji

- [Github](https://github.com/Daniel-olaO)
- [LinkedIn](https://www.linkedin.com/in/daniel-adedeji-1a996220a/)

with the mentorship of:

### Russell Pollari

- [Github](https://github.com/Russell-Pollari)
- CEO of [SharpestMinds](https://www.sharpestminds.com/)
- [LinkedIn](https://www.linkedin.com/in/russell-pollari/)

# references

- [Material-UI](https://material-ui.com/)
- [Daniel-olaO/student-app](https://github.com/Daniel-olaO/student-app)
