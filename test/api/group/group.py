data = [
    {
        "name": "test_post_groups",
        "url": "/api/groups/",
        "method": "post",
        "payload": {
            "token": "ADMIN@TOKEN", 
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
            "token": "ADMIN@TOKEN", 
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
            "token": "ADMIN@TOKEN", 
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
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": ""
        }
    }
]
