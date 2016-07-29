data = [
    {
        "name": "test_post_groups",
        "url": "/api/groups/",
        "method": "post",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
            "name": "name",
            "description": "description",
            "type": 1,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "id": 2,
                "name": "name",
                "type": 1,
            }
        }
    },
    {
        "name": "test_get_group",
        "url": "/api/groups/2/",
        "method": "get",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "id": 2,
                "name": "name",
                "type": 1,
            }
        }
    },
    {
        "name": "test_put_group",
        "url": "/api/groups/2/",
        "method": "put",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
            "name": "Test put name",
            "description": "description",
            "type": 1,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "id": 2,
                "name": "Test put name",
                "type": 1,
            }
        }
    },
    {
        "name": "test_delete_group",
        "url": "/api/groups/2/",
        "method": "delete",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
        },
        "response_status": 200,
        "response_data": {
            "msg": ""
        }
    }
]
