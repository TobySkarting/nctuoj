data = [
    {
        "name": "test_get_execute",
        "url": "/api/executes/1/",
        "method": "get",
        "payload": {
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "commands": [
                    {
                        "command": "gcc __FILE__"
                    },
                    {
                        "command": "./a.out"
                    }
                ],
                "description": "Basic C",
                "file_name": "main.c",
                "id": 1,
                "language_id": 1,
                "priority": 1,
                "setter_user_id": 1,
            }
        }
    },
    {
        "name": "test_put_execute",
        "url": "/api/executes/1/",
        "method": "put",
        "payload": {
            "token": "ADMIN@TOKEN", 
            "id": 1,
            "description": "Basic Put C",
            "file_name": "main.c",
            "language_id": 1,
            "commands[]": [
                "gcc put __FILE__"
            ]
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "commands": [
                    {
                        "command": "gcc put __FILE__"
                    },
                ],
                "description": "Basic Put C",
                "file_name": "main.c",
                "id": 1,
                "language_id": 1,
                "priority": 1,
                "setter_user_id": 1,
            }
        }
    },
    {
        "name": "test_delete_executes",
        "url": "/api/executes/1/",
        "method": "delete",
        "payload": {
            "token": "ADMIN@TOKEN",
        },
        "response_status": 200,
        "response_data":{
            "msg": ""
        }
    }
]
