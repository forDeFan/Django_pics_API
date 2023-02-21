<h1>Django pic API example</h1>

## Explanation

The idea here is to treat users equal on some level - to enable admin to change user tier plan while the app is operated by the user 
and enable user to receive various responses accordingly to current plan even if theimages were uploaded in higher or lower tier previously.


## Table of contents

* [Setup](#setup)
* [Interaction with the API](#interaction)
* [Tests](#tests)
* [TODO](#todo)

## Setup

### Prerequisites

* python 3.X
* Docker and docker-compose

### Install

Install codebase and run the app:

```
$ git clone https://github.com/forDeFan/Django_pics_API.git
$ cd Django_pics_API
```
<strong>IMPORTANT</strong> Create .env (or rename .env_example to .env) and then

```
$ docker-compose up -d --build
```
<br>

## Interaction

For reviewer convenience admin and regular user are created at app start (thru command).
<br>
New users can be added thru admin panel. 
<br>
Tiers/ plans - can be managed and pin-up to the user thru admin panel as well.
<br>

1. Admin credentials:

admin@example.com : password

2. User credentials

user@example.com : password

<br>
Endpoints available:

1. To get all images of the user (GET)

http://localhost:8000/api/images/getall

2. To upload image (POST)

http://localhost:8000/api/images/upload

3. Swagger docs available at 

http://localhost:8000/api/docs

4. Django Admin panel

http://localhost:8000/admin

<br>The user can interact with the docs after authorization.
<br><br>
POST request thru Postman:

a) prepare POST request to /upload endpoint<br>
b) Auth tab - select auth type: 'Basic Auth' and provide user credentials<br>
c) Body tab - in KEY field select "File"<br>
d) provide KEY field name "image_link" and in VALUE field click 'select files' to attach image to the request<br>
e) send the request towards API<br>
f) files will land in path: media/images/{user.id}/{filename}

Depending on current user Tier plan - different JSON response will appear.

## Tests
Fired thru docker

```
$ docker-compose run --rm app sh -c "python manage.py test"
```

## Todo

1. At this point expiring link functionality do not work with time expire - link is generated without time span, however
seconds field avaliable in POST as an option from the user (when user have Custom or Enterprise tier attached), along with seconds validation.

2. Higher test coverage for sure
