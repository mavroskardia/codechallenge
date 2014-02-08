Code Challenge
==============

Django-based website powering daily coding challenges.

Getting Started
---------------
```
# grab the project from github
git clone https://github.com/mavroskardia/codechallenge.git

# change to the new codechallenge directory
cd codechallenge

# make a virtual environment
virtualenv ve

# activate the virtual environment
source ve/bin/activate

# install the prerequisites
pip install -r requirements.txt

# setup migrations
cd cc
./manage.py schemamigration --init landing
./manage.py schemamigration --init coder
./manage.py schemamigration --init ccauth
./manage.py schemamigration --init challenge

# setup database
./manage.py syncdb

# migrate tables set up for migration
./manage.py migrate

# make sure everything is working by starting up the development server
./manage.py runserver
```

Roadmap
-------
* [ ] ~~Allow people to log in using OAuth2~~
    * Decided not to use OAuth.

* [ ] Creating challenges:
    * [ ] Specify challenge name, duration, rules
    * [ ] Other things to specify?
    * [ ] Challenge owners can modify their own challenges
    * [ ] Challenge owners can assign judges (non-participants)

* [ ] Participating in challenges:
    * [ ] Reputation-based challenges?
    * [ ] Time-based challenges (months, days, hours?)
    * [ ] Collaborative challenges

* [ ] Reputation-based system (a la Stack Exchange) that gives users graduated capabilities:
    * [ ] Vote for challenges
    * [ ] Create challenges
    * [ ] Judge challenge results