# blog-project

BlogProject

-----------------------------------------------------------------------------------------

Installation

Requirements
Ensure Python and Django are installed. Use requirements.txt to install dependencies:

pip install -r requirements.txt

-----------------------------------------------------------------------------------------

Running the Development Server

To run the Django development server:

python manage.py runserver

-----------------------------------------------------------------------------------------

Using Docker

If using Docker, build and run the containers:

docker-compose up --build

-----------------------------------------------------------------------------------------

Redis Configuration
When Using Docker
In settings.py, configure Redis as follows:

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://redis:6379/1', 
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}


Without Docker
Comment out the Docker configuration and uncomment the local Redis configuration in settings.py:

# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': 'redis://127.0.0.1:6379/1',  
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#         }
#     }
# }


Note: I didn't gitignore any files.
