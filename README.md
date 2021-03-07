# Student MCQ Exam API by Django

# how student can attend EXAM ?
### registered student can login via username and password to the endpoint ** /login/ ** by POST method <br>
### attend the exam by login by provinding token in Header (Authorization (key) Bearer token) , end point ** /test/ **

### submit the answer to end point ** /test/ ** with (Authorization (key) Bearer token). Provide the answers in body as (answers) key like an array of [ [ id, answer],[ id, answer],[ id, answer], . . .]

### student can get the answers by providing token to end point **/get-answers/ **

### student CRUD end point ** /student/ *
### standard CRUD end point ** /standard/ *


## step - 1
clone the project <br >
` git clone https://github.com/sangrampattnaik/student_examination.git`


## step - 2
create a virtual environment with name venv and activate <br >
`virtualenv venv` <br >
`source venv/bib/activate`


## step - 3
install depedancies <br >
`pip install -r requirements.txt`


## step - 4
create databasse <br >
`make migrate` <br >
or <br >

`python manage.py makemigrations`
`python manage.py migrate`

## step - 5
initial set up <br >
`make intial-setup` <br >
or <br >
`python manage.py initial_setup`

## step - 6
create admin <br >
`make admin` <br >
or <br >
`python manage.py createsuperuser`

## step - 7
runserver <br >
`make runserver` <br >
or <br >
`python manage.py runserver`

## step - 8
swagger documentaion <br >
`http://127.0.0.1:8000/swagger/` <br >
redoc documentaion <br>
`http://127.0.0.1:8000/redoc/`


