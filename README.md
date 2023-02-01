# Reddit Clone

This is reddit clone backend. It is like reddit where users can join communities, create posts, and vote/comment on posts. They can also chat with other community members in real-time. This API will be consumed by flutter app.

Technology used:

- Django
- Django Rest Framework
- Django Channels
- Redis
- PostgreSQL

## Features

- JWT Authentication + Google Authentication
- Real-time chat
- Create communities/posts/comments
- Upvote/downvote posts/comments
- Get random username & profile pictures
- Post ranking algorithm

## Installation

1. Fork the repo

2. Clone the repo:
   `$ git clone`

3. Create a virtual environment:
   `$ python3 -m venv env`

4. Activate the virtual environment:
   `$ source env/bin/activate`

5. Install the dependencies:
   `$ pip install -r requirements.txt`

6. Create a .env file and using .env.example as a reference.

7. Make migrations:
   `$ python manage.py makemigrations`

8. Migrate:
   `$ python manage.py migrate`

9. Run the server:
   `$ python manage.py runserver`

## Future Scope

- [ ] Add more tests
- [ ] Handle image from microservice.

## API Documentation

Coming soon...

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Acknowledgements

- [Django](https://www.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [Django Channels](https://channels.readthedocs.io/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Redis](https://redis.io/)
- [Avatar Generator](https://avatars.dicebear.com/)
