Wayfare API
=============

The backend of Wayfare, an app for connecting drivers and passengers for long distance road trips.

## Getting Started
### Pre-requisites
- [Git](https://git-scm.com/downloads)
    - Hopefully you don't need help with this step.
- [Python 3.7](https://www.python.org/downloads/release/python-370/)
    - Or this one.
- [Pipenv](https://pipenv.readthedocs.io/en/latest/): Pipenv is a tool for managing your Python versions and installed application packages (it's a replacement for using a `requirements.txt` if you're familiar.) It's useful for keeping application-specific dependencies separate from global dependencies. For example, if you have `Flask 1.0.2` installed globally on your system but your project is a little older and requires `Flask 0.12.4`.
    Alternative Installation:
    - Once you have Python 3.7 installed, run 
        ```bash
        $ pip3 install pipenv
        ```
    - Then add the Python 3.7 installation directory to your `$PATH`. This works differently on every OS, but Google definitely knows how to do it.
- Knowledge of REST APIs:
    - [Wikipedia](https://en.wikipedia.org/wiki/Representational_state_transfer).
    - [Beginner-friendly intro video](https://www.youtube.com/watch?v=Q-BpqyOT3a8).

### Setup
This assumes you are on a Unix-based OS. If you are on Windows then IDK.
1. Clone the repo:
    ```bash
    $ pwd
    /path/to/workspace/
    $ git clone git@github.com:Joes-Minions/wayfare-api.git
    $ cd wayfare-api
    $ ls
    Pipfile  Pipfile.lock  README.md    # etc.
    ```
2. Install requirements:
    ```bash
    $ pwd
    /path/to/workspace/wayfare-api
    $ pipenv install
    ```
3. Run it:
    ```bash
    $ pwd 
    /path/to/workspace/wayfare-api
    $ pipenv shell # This will open a shell within virtualenv.
    (wayfare-api-xx) $ python app.py
    ```
4. Try it out. _(In another terminal)_:
- GET the index:
    ```bash
    $ curl localhost:5000  # or open `http://localhost:5000/` in your browser.
    ```
- GET test messages:
    ```bash
    $ curl localhost:5000/test  # or open `http://localhost:5000/test` in your browser.
    ```
- POST a new message:
    ```bash
    $ curl -v -X POST \
           localhost:5000/test \
           -H "Content-Type: application/json" \
           -d '{
             "id": 2,
             "msg": "Kari is thirsty."
           }'
    ```
- GET test messages again (now with your new message!):
    ```bash
    $ curl localhost:5000/test  # or open `http://localhost:5000/test` in your browser.
    ```
- POST an empty message, get an error:
    ```bash
    $ curl -v -X POST \
           localhost:5000/test \
           -H "Content-Type: application/json" \
           -d '{
             "id": 3
           }'
    ```
- POST a message with a duplicate ID, get an error:
    ```bash
    $ curl -v -X POST \
           localhost:5000/test \
           -H "Content-Type: application/json" \
           -d '{
             "id": 1,
             "msg": "Dude, this ID already exists."
           }'
    ```
    Note: If all of this `curl`ing seems tedious, look into [Postman](https://www.getpostman.com/).
5. ??????
6. PROFIT!!
