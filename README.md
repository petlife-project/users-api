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

4 - Fill the .env file with the environment variables and theirs values; the variables you'll need are in the .env-example file; Export them using:

```
$ export $(cat .env | xargs)
```

5 - Finally, start the application:

```
$ python3.7 -m users.app
```

# Use cases and endpoints #

## Login ##
`POST /auth` 

*Request body:*
Form data
```
username: "user"
password: "pass"
type: "client" | "shop"
```

*Responses*

`200 OK`

Returns whole user object (except password)

```JSON
{
    "username": "allandlo",
    "name": "Allan",
    "email": "allan@gmail.com",
    "address": "12345-022",
    "cpf": "000.000.000-00",
    "phone_number": "11988884444",
    "pets": {
        "pet_name1": {
            "species": "dog",
            "breed": "labrador",
            "age_years": "10",
            "weight_kilos": "12"
        },
        "pet_name2": {
            "species": "cat",
            "breed": "persa",
            "age_years": "5",
            "weight_kilos": "7"
        }
    }
}
```

`401 Unauthorized`

Returns unauthorized code if username and password don't match

```JSON
Invalid user information
```

## Client Registration ##
`POST /clients`

*Request body:*
Form data
```
username: "user"
password: "pass"
name: "Jonh Doe"
email: "user@server.com"
address: "12345-022"
phone_number: "99999999999"
cpf: "12345678900"
```

*Responses*

`200 OK`

Returns newly created user object (containing password)

```JSON
{
    "username": "allandlo",
    "password": "created_password",
    "name": "Allan",
    "email": "allan@gmail.com",
    "address": "12345-022",
    "cpf": "000.000.000-00",
    "phone_number": "11988884444"
}
```

`409 Conflict`

Returns conflict code if user already exists

```JSON
User allandlo already exists in clients
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Invalid CPF
```

## Client Update ##
`PUT /clients`

*Request body:*
Form data
```
username: "user"
password: "pass"
name: "Jonh Doe"
email: "user@server.com"
address: "12345-022"
phone_number: "99999999999"
pets: (stringified JSON) `{"pet_name1":{"species":"dog","breed":"labrador","age_years":"10","weight_kilos":"12"}}`
```

*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "allandlo",
    "name": "Allan",
    "email": "allan@gmail.com",
    "address": "12345-022",
    "cpf": "000.000.000-00",
    "phone_number": "11988884444",
    "pets": {
        "pet_name1": {
            "species": "dog",
            "breed": "labrador",
            "age_years": "10",
            "weight_kilos": "12"
        }
    }
}
```

`400 Bad Request`

Returns a bad request code if any of the fields fail upon validation

```JSON
Invalid email address
Incorrect username or password
```

## Shop Registration ##
`POST /shops`

*Request body:*
Form data
```
username: "user"
password: "pass"
name: "PetX"
email: "petx@corpemail.com"
address: "12345-022"
phone_number: "99999999999"
cnpj: "12345678901234"
```

*Responses*

`200 OK`

Returns newly created user object (containing password)

```JSON
{
    "username": "petx",
    "password": "created_password",
    "name": "PetX",
    "email": "petx@corpemail.com",
    "address": "12345-022",
    "cnpj": "12345678901234",
    "phone_number": "11988884444"
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
`PUT /shops`

*Request body:*
Form data
```
username: "user"
password: "pass"
name: "PetX"
email: "user@server.com"
address: "12345-022"
phone_number: "99999999999"
services: (stringified JSON) `[{"service_name":"some name","service_id":"service id on services collection","price":"R$19,99"}]`
description: "Melhor petshop da regiao!"
hours: "08h00 - 20h00"
profile_pic: [File]
banner_pic: [File]
```

*Responses*

`200 OK`

Returns updated user object (except password)

```JSON
{
    "username": "user",
    "name": "PetX",
    "pics": {
        "profile": "file id on cos",
        "banner": "file id on cos"
    },
    "email": "user@server.com",
    "address": "00000-000",
    "cnpj": "00.000.000/0001-00",
    "phone_number": "11 38965749",
    "description": "LOREM IPSUM",
    "hours": "08h00 - 20h00",
    "services": [
        {
            "service_name": "some name",
            "service_id": "service id on services collection",
            "price": "R$19,99"
        },
        {
            "service_name": "some other name",
            "service_id": "service id on services collection",
            "price": "R$39,99"
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
