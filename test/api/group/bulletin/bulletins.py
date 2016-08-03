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
        "name": "test_get_group_bulletin",
        "url": "/api/groups/1/bulletins/",
        "method": "get",
        "payload": {
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": [{
                "id": 1,
                "title": "test bulletin",
                "content": "content",
                "group_id": 1,
                "setter_user_id": 1,
            },]
        }
    },
]
