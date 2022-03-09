install:
	RUN python3 -m pip install --upgrade pip

	pip install --upgrade pip &&\
		pip install -r requirements.txt
	
format:
	black *.py

all: install lint test