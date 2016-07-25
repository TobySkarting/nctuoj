data = [
    {
        "name": "test_get_user_power",
        "url": "/api/users/1/power/",
        "method": "get",
        "payload": {
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4]
            }
        }
    },
    {
        "name": "test_post_user_power",
        "url": "/api/users/1/power/",
        "method": "post",
        "payload": {
            "power": 5,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4, 5]
            }
        }
    },
    {
        "name": "test_delete_user_power",
        "url": "/api/users/1/power/",
        "method": "delete",
        "payload": {
            "power": 5,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4]
            }
        }
    }
]
