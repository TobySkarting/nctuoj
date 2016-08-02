data = [
    {
        "name": "post_bulletin",
        "url": "/api/bulletins/",
        "method": "post",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
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
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
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
