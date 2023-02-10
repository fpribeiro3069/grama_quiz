# Grama Quiz

Application for registering quiz answers during Grama's quiz events. Built in Django, offers a chance to answer either multiple choice questions or text answers. Has backoffice functionality for inputing the questions.
 >At the moment it only supports one quiz at a time.

# Installation & Running
To install and run this project you need to clone this repository and create a virtual environment for the project and activate it:
`python3 -m venv venv` (for Linux users)
`source venv/bin/activate`
or
`py -m venv venv` (for Windows users)
`venv\Scripts\activate`

After that you need to install dependencies:
`pip install -r requirements.txt` (same for both systems)

Now you need to apply the database migrations for the project by doing:
`cd grama_quiz`
`python3 manage.py migrate` (for Linux users)
or
`py manage.py migrate` (for Windows users)

And finally to run the development server just:
`<your_python_os> manage-py runserver`