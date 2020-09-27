url-tweets
==========

Connect4 Game built using Django.

:License: MIT

Live Demo
--------------
    :Demo: https://py-connect4.herokuapp.com/


Postman Collection
----------

    :Postman: https://www.getpostman.com/collections/ffcc8b9714874a496323


How To Use?
----------
    1. Go to postman collection, run start game api. It will return game_uuid, use that uuid for all other api call.
    2. Make Move Red: It can be used to make move of red, just change column to one you want to make move.
    3. Make Move Yellow: It can be used to make move of Yellow, just change column to one you want to make move.
    4. Show Game State: It will show visualization of game.
    5. Check turn: It tells which player turn it is.
    6. Check Game Result: Tells game result.

Basic Commands
--------------

Local Setup
----------

1. Clone the Repository in your Local Machine
    $ https://github.com/cipher098/Connect4.git
2. Create virtualenv
::
    $ virtualenv -p $(which python3) connect4
    $ source connect4/bin/activate
3. Go to project directory:
    $ cd connect4
4. Install requirements using command:
    $ pip install -r requirements.txt
5. Apply migrations to db using command:
    python manage.py migrate

6. Run server using command:
    python manage.py runserver
7. Import postman collection, and create environemnt with a variable: 'local_host' having value 'http://localhost:8000'
8. Choose the env created above and run postman as described in How to use.




