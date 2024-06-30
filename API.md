API Documentation

User Registration
    URL: /api/register/
    Method: POST
    Permissions: AllowAny

    Request Body:
        {
            "username": "string",
            "email": "string",
            "password": "string",
            "confirm_password": "string"
        }

    Response:
        Status Code: 201 CREATED
        {
            "user": {
                "id": 1,
                "first_name": "",
                "last_name": "",
                "username": "string",
                "email": "string"
            },x
            "token": "token_string"
        }


User Login
    URL: /api/login/
    Method: POST
    Permissions: AllowAny

    Request Body:
        {
            "username": "string",
            "password": "string"
        }
    
    Response
        Status Code: 200 OK
            {
                "user": {
                    "id": 1,
                    "first_name": "",
                    "last_name": "",
                    "username": "string",
                    "email": "string"
                },
                "token": "token_string"
            }

        Status Code: 400 BAD REQUEST
        {
            "details": "Error message"
        }

User Logout
    URL: /api/logout/
    Method: POST
    Permissions: IsAuthenticated

    Response:
        Status Code: 200 OK
        {
            "details": "Logged out successfully."
        }

        Status Code: 400 BAD REQUEST
        {
            "details": "Error message"
        }

Blog Post List
    URL: /api/blogposts/
    Method: GET
    Permissions: AllowAny

    Response:
        Status Code: 200 OK
        {
            "count": 10,
            "next": "link_to_next_page",
            "previous": null,
            "results": [
                {
                "id": 1,
                "title": "string",
                "content": "string",
                "publication_date": "2024-07-01T12:00:00Z",
                "author": {
                    "id": 1,
                    "first_name": "string",
                    "last_name": "string",
                    "username": "string",
                    "email": "string"
                }
                },
                {
                "id": 2,
                "title": "string",
                "content": "string",
                "publication_date": "2024-07-01T12:00:00Z",
                "author": {
                    "id": 2,
                    "first_name": "string",
                    "last_name": "string",
                    "username": "string",
                    "email": "string"
                }
                }
            ]
        }


Create Blog Post
    URL: /api/blogposts/create/
    Method: POST
    Permissions: IsAuthenticated

    Request Body:
        {
            "title": "string",
            "content": "string"
        }

    Response
        {
            "id": 1,
            "title": "string",
            "content": "string",
            "publication_date": "2024-07-01T12:00:00Z",
            "author": {
                "id": 1,
                "first_name": "string",
                "last_name": "string",
                "username": "string",
                "email": "string"
            }
        }

        Status Code: 400 BAD REQUEST
        {
            "details": "Error message"
        }

Retrieve Blog Post
    URL: /api/blogposts/{id}/
    Method: GET
    Permissions: IsAuthenticated

    Response:
        Status Code: 200 OK
        {
            "id": 1,
            "title": "string",
            "content": "string",
            "publication_date": "2024-07-01T12:00:00Z",
            "author": {
                "id": 1,
                "first_name": "string",
                "last_name": "string",
                "username": "string",
                "email": "string"
            }
        }

        Status Code: 404 NOT FOUND
        {
            "detail": "Not found."
        }

Update Blog Post
    URL: /api/blogposts/{id}/update/
    Method: PUT or PATCH
    Permissions: IsAuthenticated

    Request Body:
    {
        "title": "string",
        "content": "string"
    }

    Response:
        Status Code: 200 OK
        {
            "id": 1,
            "title": "string",
            "content": "string",
            "publication_date": "2024-07-01T12:00:00Z",
            "author": {
                "id": 1,
                "first_name": "string",
                "last_name": "string",
                "username": "string",
                "email": "string"
            }
        }

        Status Code: 400 BAD REQUEST
        {
            "details": "Error message"
        }

Delete Blog Post
    URL: /api/blogposts/{id}/delete/
    Method: DELETE
    Permissions: IsAuthenticated

    Response:
        Status Code: 204 NO CONTENT
        {}


    Status Code: 404 NOT FOUND
        {
            "detail": "Not found."
        }
        

Authentication and Authorization

Authentication: Token-based authentication (TokenAuthentication) or session-based authentication (SessionAuthentication).
Authorization: Certain endpoints require IsAuthenticated permission.