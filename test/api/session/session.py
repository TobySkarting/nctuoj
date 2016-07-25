data = [
    {
        "name": "test_create_session_by_password",
        "url": "/api/users/session/",
        "method": "post",
        "payload": {
            "account": "admin",
            "password": "admin",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "email": "admin@gmail.com", 
                "account": "admin", 
                "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
                "id": 1,
                "school_id": 1,
                "name": "",
                "student_id": "0000000",
            }
        }
    },
    {
        "name": "test_create_session_by_password_again",
        "url": "/api/users/session/",
        "method": "post",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
        },
        "response_status": 401,
        "response_data": {
            "msg": "You have already signined."
        }
    },
]
