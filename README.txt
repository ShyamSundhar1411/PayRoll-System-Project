Django Project Setup Guide
This README provides step-by-step instructions on how to set up and run this Django project from GitHub on your local machine using Poetry as the dependency management tool.

Prerequisites
Before you get started, make sure you have the following installed:

Python (version 3.6 or higher)
Make sure ADD TO PATH is checked while installation.


Installation and Setup
1.Download and Extract the ZIP File: 

Download the ZIP file to your local machine and extract its contents to a directory of your choice and copy the folder path


2.Move into the project directory through command prompt or terminal:

cd <folder-path>


3.Install all project dependencies:

i) pip install -r requirements.txt
ii) pip install django-filter
iii) pip install pandas
iv) pip install numpy
v) pip install openpyxl


4.Apply the initial database migrations:

python manage.py migrate


5.Create a superuser account to access the Django admin panel:

python manage.py createsuperuser
Follow the prompts to set up the superuser account.


Running the Development Server
Now that you have set up the project, you can run the development server to see your Django application in action.

1.Start the Django development server:

python manage.py runserver
The development server should start, and you'll see output indicating the local address where your application is accessible (usually http://127.0.0.1:8000/).

Open a web browser and navigate to the local server address to view your Django application.

Access the Django admin panel (database view) by appending /admin/ to the server address and log in using the superuser credentials you created earlier.


URLS:
home page :- http://127.0.0.1:8000/
add employee page :- http://127.0.0.1:8000/addemployee
upload excel page :- http://127.0.0.1:8000/uploadexcel
payroll page :- http://127.0.0.1:8000/payslip
employee list page :- http://127.0.0.1:8000/emlist
