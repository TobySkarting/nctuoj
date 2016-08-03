data = [
    {
        "name": "post_bulletin",
        "url": "/api/bulletins/",
        "method": "post",
        "payload": {
            "token": "ADMIN@TOKEN", 
            "title": "test bulletin",
            "content": "content",
            "group_id": 1,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "id": 1,
                "title": "test bulletin",
                "content": "content",
                "group_id": 1,
                "setter_user_id": 1,
            }
        }
    },
    {
        "name": "test_get_bulletin",
        "url": "/api/bulletins/1/",
        "method": "get",
        "payload": {
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "id": 1,
                "title": "test bulletin",
                "content": "content",
                "group_id": 1,
                "setter_user_id": 1,
            }
        }
    },
    {
        "name": "test_put_bulletin",
        "url": "/api/bulletins/1/",
        "method": "put",
        "payload": {
            "token": "ADMIN@TOKEN", 
            "title": "test bulletin modify",
            "content": "content",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "id": 1,
                "title": "test bulletin modify",
                "content": "content",
                "group_id": 1,
                "setter_user_id": 1,
            }
        }
    },
    {
        "name": "test_delete_bulletin",
        "url": "/api/bulletins/1/",
        "method": "delete",
        "payload": {
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": ""
        }
    },
]

