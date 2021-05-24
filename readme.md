# Vessel and Equipments Management API

This project creates a backend to manage different equipment of an FPSO (Floating Production, Storage and Offloading). This system will be used for other applications in the organization and is extremely important creating this in a reusable way.

## Getting Started
___

### Pre-requisites and Local Development

### Database - PostgreSQL

PostgreSQL is a relational object database management system, developed as an open source project. Due to the relational nature of the problem, considering the relationship between vessels and equipments, this manager was chosen among other things for being robust, supporting working with a large volume of data in addition to having an extremely strong development community, which makes it my own point of view one of the best if not the best option to model the application database.
To install PostgreSQL visit this [website](https://www.postgresql.org/) and select the best option depending on your operating system. In this project was used the `version 13.0` 

### Database configuration

After install PostgreSQL, it's necessary to create the databases needed to run the tests and the application.

__Creating environment - Tests__

1) Download the project, navigate to root directory.
2) Run the following commands on the terminal:

```psql
createbd -U postgres modec_test
psql -U postgres modec_test < modec_test.sql
```

__Creating environment - Application__

In this case, it's necessary just to create an application database in order to connect, store and get data.

1. Run the following command on the terminal:

```pqsl
createdb -U postgres modec
```

In this case -U defines the user used to create the databases. Although the default postgres user has been used, any other user can be used as long as he has the creation permissions in the environment used.

### Python 3 

It's necessary to have python3 and pip installed. The version used was `3.7.2 32 bits` and it is highly recommended to create a virtual environment to create an isolated development environment. All required packages are included in the requirements.txt file. To run the application follow instructions bellow:

1. Using the terminal, navigate to app folder inside the root project directory.
2. Run the commands:

```
set FLASK_APP=app.py
set FLASK_ENV=development
flask run
```
*commands considering windows environment for unix use export instead of set*

These commands put the application in development and directs our application to use the app.py into the working directory. Working in development mode shows an interactive debugger in the console and restarts the server whenever changes are made.
The application is run on `http://127.0.0.1:5000/` by default.

## Tests  

To run the tests, navigate to `test` folder inside root project directory and run the commands: 

```
python3 test_app.py
```

After run tests the following message will appear in the terminal:

```
Ran 6 tests

OK
```

With "OK" meaning that all tests were passed with success.


## API Rerefence
___

### Getting Started

- Base URL: Running locally the base url is `https://127.0.0.1:5000/`

### Error Handling

Errors are returned as JSON objects in the following format:

```
{
    "success": False,
    "error": 400,
    "message": "bad request"
}
```

The API will return three errors types when requests fail:
- 400: bad request
- 404: not found
- 403: code already exists

### Endpoints

#### POST /vessels

- General:
    - Insert and persist a new vessel into the database.
- Sample: `curl https://127.0.0.1:5000/vessels -H POST -H "Content-Type: application/json" -d "{\"code\": \"MV102\"}"`

Using windows put \ before double quotes is necessary to avoid errors.

Request:
```json
{
    "code": "MV102",
}
```

Response:
```json
{
    "id": 1,
    "code": "MV102",
    "success": true
}
```

#### POST /equipments

- General:
    - Insert and persist a new equipment associated with a existing vessel into the database. 
- Sample: `curl https://127.0.0.1:5000/equipments -H POST -H "Content-Type: application/json" -d "{\"code\": \"MV111\"}"`

Request:
```json
{
    "name": "compressor",
    "code": "5310B9D7",
    "location": "Brazil",
    "vessel_code": "MV102"
}
```

Response:
```json
{
    "success": true,
    "id": 1, 
    "code": "5310B9D7", 
    "name": "compressor", 
    "location": "Brazil",
    "activation_status": true, 
    "vessel_code": "MV102"
}
```

#### PATCH /equipments

- General:
    - Update activation_status of a list containing one or more equipments, setting it to False, what means that these equipments are deactivate.
- Sample: `https://127.0.0.1:5000/equipments`

request:
```json
{
    "equipments": [
        {"code": "5310B9D7"},
        {"code": "5310B9D8"},
        {"code": "No Exist In Database"}
    ]
}
```
Response:
```json
{
    "success": true,
    "non_processed_equipments": [
        {"code": "No Exist In Database"}
    ] 
}
```

#### GET /equipments/< vessel_code >

- General:
    - Returns all active equipments associated with a specific vessel.
- Sample: `https://127.0.0.1:5000/equipments/mv102`

Response:
```json
{
    "vessel_code": "MV102",
    "success": true,
    "equipments": [
        {
            "id": 1, 
            "name": "compressor",
            "code": "5310B9D7",
            "location": "Brazil",
            "activation_status": true,
            "vessel_code": "MV102"
        },
        {
            "id": 1, 
            "name": "compressor",
            "code": "5310B9D8",
            "location": "Brazil",
            "activation_status": true,
            "vessel_code": "MV102"
        },
        {
            "id": 1, 
            "name": "compressor",
            "code": "5310B9D9",
            "location": "Brazil",
            "activation_status": true,
            "vessel_code": "MV102"
        }
    ]
}
```


## Authors

Rodrigo Bernardo Medeiros