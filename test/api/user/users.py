data = [
    {
        "name": "test_post_user",
        "url": "/api/users/",
        "method": "post",
        "payload": {
            "email": "test@gmail.com",
            "account": "test",
            "name": "NAMEISTEST",
            "password": "test",
            "repassword": "test",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "email": "test@gmail.com",
                "account": "test",
                "name": "NAMEISTEST",
                "school_id": 1,
                "id": 2,
                "student_id": "",
            }
        }
    },
    {
        "name": "test_post_user",
        "url": "/api/users/",
        "method": "post",
        "payload": {
            "email": "test@gmail.com",
            "account": "test",
            "name": "NAMEISTEST",
            "password": "test",
            "repassword": "test",
        },
        "response_status": 400,
        "response_data": {
            "msg": "Email Exist",
        }
    },
]
