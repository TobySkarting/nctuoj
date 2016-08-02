data = [
    {
        "name": "test_get_gorup_user_power",
        "url": "/api/groups/1/users/1/power/",
        "method": "get",
        "payload": {
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4, 5]
            }
        }
    },
    {
        "name": "test_post_group_user_power",
        "url": "/api/groups/1/users/1/power/",
        "method": "post",
        "payload": {
            "power": 6,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4, 5, 6]
            }
        }
    },
    {
        "name": "test_delete_user_power",
        "url": "/api/groups/1/users/1/power/",
        "method": "delete",
        "payload": {
            "power": 6,
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "power": [1, 2, 3, 4, 5]
            }
        }
    }
]
