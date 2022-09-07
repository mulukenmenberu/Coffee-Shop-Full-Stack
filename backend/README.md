# Coffee Shop Backend

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./src/database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

Each time you open a new terminal session, run:

```bash
export FLASK_APP=api.py;
export AUTH0_DOMAIN=dev--0iw-l86.us.auth0.com
export ALGORITHMS=['RS256']
export API_AUDIENCE=http://localhost:4200/

```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

### API Description 

### Endponints accessed by GET Method 
1.  /drinks
      - gets list of available drinks
      - Request Arguments: None
      - Permissions: Public
      - Returns JSON data like the following format 
      ```json
              {
                  "drinks": [
                     {
                           "id": 1,
                           "recipe": [
                              {
                                 "color": "blue",
                                 "name": "water",
                                 "parts": 1
                              }
                           ],
                           "title": "water"
                     }
                  ],
                  "success": true
                  }
      ```
2.  /drinks-detail
      - gets list of available drinks with details
      - Request Arguments: None
      - Permissions: Barista
      - Returns JSON data like the following format 
      ```json
            {
               "drinks": [
                  {
                        "id": 1,
                        "recipe": [
                           {
                              "color": "blue",
                              "name": "water",
                              "parts": 1
                           }
                        ],
                        "title": "water"
                  }
               ],
               "success": true
            }
      ```
### Endponints accessed by POST Method 
1.  /drinks
      - added a new drink to the DB
      - Request Arguments: 
      ```json
           {
            "title": "test", 
            "recipe": [{"name": "test", "color": "red","parts": 1}]
            }
       ```     
      - Permissions: Manager
      - Status code on Success: 200
      - Returns JSON data like the following format 
      ```json
           {
            "success": True, 
            "drinks":  [array of drink data]
            }
      ```
### Endponints accessed by PATCH Method 
1.  /drinks/<int:id>
      - this end point can be used to update drink details
      - Request Arguments: drink ID and ...
      ```json
           {
            "title": "test", 
            "recipe": [{"name": "test", "color": "red","parts": 1}]
            }
       ```     
      - Permissions: Manager
      - Returns JSON data like the following format 
      ```json
           {
            "success": True, 
            "drinks":  [array of drink data]
            }
      ```
      - status code on success: 200
### Endponints accessed by DELETE Method 
1.  /drinks/<int:id>
      - this end point can be used to delete a drink
      - Request Arguments: drink ID and ...
      - Permissions: Manager
      - Returns JSON data like the following format 
      ```json
           {
            "success": True, 
            "delete":  deleted drink id
            }
      ```
      - status code on success: 200