# Car Analysis

### Steps for running this project
* Clone this repo to local
  `git clone https://github.com/palakkayare/car_analysis`
* Install Python ['3.8.0'](https://www.python.org/downloads/release/python-380/)
  - You must have Python version 3.8.0 installed to run this project
* Create a virtual environment - To create virtual env in windows refer [How to create venv in widows](https://medium.com/co-learning-lounge/create-virtual-environment-python-windows-2021-d947c3a3ca78)
  `python -m venv ~/car_analysis`
* Activate the environment
  `source ~/car_analysis/bin/activate`
* Install required python libraries for this project
  `pip install -r requirements.txt`
* Create migrations
  `python manage.py makemigrations`
* Apply migrations to DB
  `python manage.py migrate`
* Run the project
  `python manage.py runserver` after running this command the website will be hosted to localserver http://127.0.0.1:8000/
* Use below creds for login
  ```
  username - imjarvis
  password - letmelogin@2022
  ```
* Bingo! now you can explore the web