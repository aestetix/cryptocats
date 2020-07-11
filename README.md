# Cryptocats
This code comprises the source code for https://www.cryptocats.me. What follows is a step by step guide to get your own setup running. All instructions assume an Ubuntu 20.04 system.

### Prerequisites
Ensure that git, sqlite3, gnupg, and python virtualenv are all installed.
Next, create a virtualenv directory. Then go into the directory and run "source bin/activate". Next, run the command "pip install -r requirements.txt", which will install the needed python libraries.

### Set up the key generator
Once you have checked out the repo, determine what massive file you want to upload to the keyservers, and set line 10 of create_db.py to point to that file. Then run create_db.py, which will create a database in sqlite, and begin the potentially long process of creating keys based on the file. Do not be surprised to see hundreds or thousands of keys result from this script.

### Set up the website
Now that you have a key generation in progress, you need to enable the website part. This is handled through python Flask, but I recommend using a reverse proxy like nginx that points to the flask backend. If you want to make it even more stable, wrap the flask in gunicorn.
