# UniLife
This repo is an REST API for  "UniLife" mobile app. UniLife mobile app is a blog app where users can share about their memories at university.
## Overview
The main features that have currently been implemented are:

* Read posts(no need to login)
* Create / Update / Delete the post.
* Like / Save / Comment the post
* Authentication and Authorization(oject-level)
* Token Authentication
* User Profile
* Follow / Unfollow
* Search posts

## Tech Stack

**Backend** - Django REST Framework   
**Database** - Postgres  
**Hosting** - AWS Lambda, AWS S3 Bucket, AWS RDS  


## Demo
The endpoint used in production is priavate. However, you can test on this [mock server](https://pyaephyokyaw.pythonanywhere.com/swagger/)



## Entity–relationship Diagram
> **Note:** Click and download the image to see details.
![Entity–relationship model](https://github.com/pyaephyokyaw15/Whale/blob/main/ERD.png)


## Quick Start

To get this project up and running locally on your computer:

1. Clone the project.

   ```bash
   git clone https://github.com/pyaephyokyaw15/Whale.git
   ```
1. Set up the Python development environment.
   > **Note:** I want to recommend using a Python virtual environment.
   
1. Create .env file in the project root directory and create variables used in settings.py.

1. Assuming you have Python setup, run the following commands (if you're on Windows you may use `py` or `py -3` instead of `python` to start Python):
   ```
   pip3 install -r requirements.txt
   python3 manage.py makemigrations
   python3 manage.py migrate
   python3 manage.py collectstatic
   python3 manage.py test # Run the standard tests. These should all pass.
   python3 manage.py createsuperuser # Create a superuser
   python3 manage.py runserver
   ```
1. Open a browser to `http://127.0.0.1:8000.`
 
1. Admin Site: `http://127.0.0.1:8000/admin`

## References

* [Django Documentation](https://docs.djangoproject.com/en/4.1/)
* [mdn web docs](https://developer.mozilla.org/en-US/docs/Learn)

## Author

- [@pyaephyokyaw15](https://github.com/pyaephyokyaw15/)
