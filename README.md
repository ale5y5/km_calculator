## General considerations
The code focuses on a reduced complexity rather than grouping logic into smaller functions.  
This can be achieved, and logic can be split out, e.g. a separate function for parsing digits into a multi digit integer value.  
However, I wanted to avoid iterating over those digits in a separate function for a second time (considering that most of the chars in an expression are digits, it would increase complexity).


## Commands
To run without a webapp (as described in Parts 1 & 2):  
-create a virtual env  
-activate it  
-install everything from requirements.txt  
`pip install -r requirements.txt`  


## Tests
To run tests, from the root of the project:  
`pytest tests/`  


## Implementation  
###Part 1: to start the prefix calculator, run  
`python prefix_calculator.py`  


###Part 2: to start the infix calculator, run  
`python infix_calculator.py`  


### Bonus: to run as a webservice, build the docker container  
From the root of the project:  
`docker build . -t km_calculator`  
`docker-compose up -d`  
This will start a webserver on localhost:3456 where you can reach the two calculators on these 2 endpoints: `/calculator/infix` and `/calculator/prefix`.  
I decided to go with Flask which is lightweight compared to Django.

These endpoints accept POST with a payload like:  
`{"expression": "+ 2 3"}` or `{"expression": "( + 2 3 )"}`

Example calls:  
GET @ `http://localhost:3456/status/`  
POST @ `http://localhost:3456/calculator/prefix/` with payload `{"expression": "+ 5000 / 1000000 + 1000 0"}`  
POST @ `http://localhost:3456/calculator/infix/` with payload `{"expression": "( + 2 3 )"}`  

