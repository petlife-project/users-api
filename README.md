# users-api

The REST API responsible for registering and updating users information

## Running locally ##

1 - To run this API locally you should first create a python virtual environment with:

```
$ python3.7 -m venv venv
```

2 - And then enter it:

```
$ source venv/bin/activate
```

3 - Now you can install the project's dependencies:

```
$ pip install -r requirements.txt
```

4 - Fill the .env file with the environment variables and theirs values; <br/>The variables you'll need are in the .env-example file; <br/>Export them using:

```
$ export $(cat .env | xargs)
```

5 - Finally, start the application:

```
$ python -m users.app
```

# Data models #
## Client user ##
```json
{
    "username": "string",
    "password": "string",
    "type": "client",
    "name": "string",
    "email": "string",
    "address": "string",
    "cpf": "string",
    "phone_number": "string",
    "pets": [
        {
            "name": "string",
            "species": "string",
            "breed": "string",
            "age_years": "integer",
            "weight_kilos": "float"
        }
    ]
}
```

## Shop user ##
```json
{
    "username": "string",
    "password": "string",
    "type": "shop",
    "name": "string",
    "pics": {
        "profile": "bytes",
        "banner": "bytes"
    },
    "email": "string",
    "address": "string",
    "cnpj": "string",
    "phone_number": "string",
    "description": "string",
    "hours": "string",
    "services": [
        {
            "service_name": "string",
            "service_id": "string",
            "price": "string"
        }
    ]
}
```

# Use cases and endpoints #

## Login ##
`POST /auth` 

*Request body:*
JSON
```json
{
    "username": "string",
    "password": "string",
    "type": "client" | "shop"
}

```

*Responses*

`200 OK`

Returns JWT

```json
eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE2MTk0Njk1NTUsIm5iZiI6MTYxOTQ2OTU1NSwianRpIjoiMmNjM2U1OGItMjQwMi00MWRiLWFiMDEtZWYxNzg5Yzk0NDc4IiwiZXhwIjoxNjE5NDcxMzU1LCJpZGVudGl0eSI6eyJfaWQiOiI2MDg3MjRkM2ZkZTNlNzgyY2M4NTE0YWQiLCJ1c2VybmFtZSI6InVsdGltYXRlX3Rlc3QxMjMiLCJuYW1lIjoic3RyaW5nIiwiZW1haWwiOiJzdHJpbmdAc2VydmVyLmNvbSIsImFkZHJlc3MiOiJzdHJpbmciLCJwaG9uZV9udW1iZXIiOiJzdHJpbmciLCJjcGYiOiIzNjI2MjEyOTA0OSIsInBldHMiOltdLCJ0eXBlIjoiY2xpZW50In0sImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.bjcBOKnZntefUeOyBd7K-1RfktCXl008LVEtt_bGrNA
```

`401 Unauthorized`

Returns unauthorized code if username and password don't match

```JSON
Invalid user information
```

## Client Registration ##
`POST /clients`

*Request body:*
JSON
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "phone_number": "string",
    "cpf": "string"
}
```

*Responses*

`200 OK`

Returns newly created user object (except password)

```JSON
{
    "username": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "cpf": "string",
    "pets": [],
    "phone_number": "string"
}
```

`409 Conflict`

Returns conflict code if user already exists

```JSON
User string already exists in clients
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Invalid CPF
```

## Client Update ##

*protected*

`PUT /clients`

*Request header*

Authorization
Bearer token

*Request body:*
JSON
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "phone_number": "string",
    "pets": { // Only one per request
        "name": "string",
        "species": "string",
        "breed": "string",
        "age_years": "integer",
        "weight_kilos": "float"
    }
}
```    

*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "cpf": "string",
    "phone_number": "string",
    "pets": [
        {
            "name": "string",
            "species": "string",
            "breed": "string",
            "age_years": "integer",
            "weight_kilos": "float"
        }
    ]
}
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Incorrect username or password
```

## Pet removal ##

*protected*

`DELETE /clients?pet_name=<exact-match>`

*Request header*

Authorization
Bearer token


*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "cpf": "string",
    "phone_number": "string",
    "pets": [
        {
            "name": "string",
            "species": "string",
            "breed": "string",
            "age_years": "integer",
            "weight_kilos": "float"
        }
    ]
}
```

`404 Not Found`

Returns a bad request code if the pet name sent is not found on the user

## Shop Registration ##
`POST /shops`

*Request body:*
JSON
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "phone_number": "string",
    "cnpj": "string"
}
```

*Responses*

`200 OK`

Returns newly created user object (except password)

```JSON
{
    "username": "string",
    "name": "string",
    "email": "string",
    "address": "string",
    "cnpj": "string",
    "phone_number": "string"
}
```

`409 Conflict`

Returns conflict code if user already exists

```JSON
User petx already exists in shops
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Invalid CNPJ
```

## Shop Update ##

*protected*

`PUT /shops`

*Request header*

Authorization
Bearer token

*Request body:*
JSON
```json
{
    "username": "string",
    "password": "string",
    "name": "string",
    "profile_pic": "base64 encoded file",
    "banner_pic": "base64 encoded file",
    "email": "string",
    "address": "string",
    "cnpj": "string",
    "phone_number": "string",
    "description": "string",
    "hours": "string",
    "services": { // Only one per request
        "service_name": "string",
        "service_id": "string",
        "price": "string"
    }
}

```

*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "string",
    "password": "string",
    "name": "string",
    "pics": {
        "profile": "bytes",
        "banner": "bytes"
    },
    "email": "string",
    "address": "string",
    "cnpj": "string",
    "phone_number": "string",
    "description": "string",
    "hours": "string",
    "services": [
        {
            "service_name": "string",
            "service_id": "string",
            "price": "string"
        }
    ]
}
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Incorrect username or password
```

## Service removal ##

*protected*

`DELETE /shops?service_id=<exact-match>`

*Request header*

Authorization
Bearer token

*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "string",
    "name": "string",
    "pics": {
        "profile": "bytes",
        "banner": "bytes"
    },
    "email": "string",
    "address": "string",
    "cnpj": "string",
    "phone_number": "string",
    "description": "string",
    "hours": "string",
    "services": [
        {
            "service_name": "string",
            "service_id": "string",
            "price": "string"
        }
    ]
}
```

`404 Not Found`

Returns a bad request code if the service id sent is not found on the user
