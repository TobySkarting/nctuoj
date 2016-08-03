data = [
    {
        "name": "test_get_executes",
        "url": "/api/executes/",
        "method": "get",
        "payload": {
            "token": "ADMIN@TOKEN", 
        },
        "response_status": 200,
        "response_data": {
            "msg": [
                {
                    "description": "Basic C",
                    "file_name": "main.c",
                    "id": 1,
                    "language_id": 1,
                    "priority": 1,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic C++11",
                    "file_name": "main.cpp",
                    "id": 2,
                    "language_id": 2,
                    "priority": 2,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic C++14",
                    "file_name": "main.cpp",
                    "id": 3,
                    "language_id": 2,
                    "priority": 3,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Java",
                    "file_name": "Main.java",
                    "id": 4,
                    "language_id": 3,
                    "priority": 4,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Python2",
                    "file_name": "main.py",
                    "id": 5,
                    "language_id": 4,
                    "priority": 5,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Python3",
                    "file_name": "main.py",
                    "id": 6,
                    "language_id": 5,
                    "priority": 6,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Go",
                    "file_name": "main.go",
                    "id": 7,
                    "language_id": 6,
                    "priority": 7,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Perl",
                    "file_name": "main.pl",
                    "id": 8,
                    "language_id": 7,
                    "priority": 8,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Javascript",
                    "file_name": "main.js",
                    "id": 9,
                    "language_id": 8,
                    "priority": 9,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic Ruby",
                    "file_name": "main.rb",
                    "id": 10,
                    "language_id": 10,
                    "priority": 10,
                    "setter_user_id": 1,
                },
                {
                    "description": "Basic shell",
                    "file_name": "main.sh",
                    "id": 11,
                    "language_id": 11,
                    "priority": 11,
                    "setter_user_id": 1,
                }
            ]
        }
    },
    {
        "name": "test_post_executes",
        "url": "/api/executes/",
        "method": "post",
        "payload": {
            "token": "ADMIN@TOKEN", 
            "file_name": "test.cpp",
            "language_id": 3,
            "commands[]": [
                "g++ -O2 __FILE__",
                "./a.out",
            ],
            "description": "QQ",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "commands": [
                    {
                        "command": "g++ -O2 __FILE__"
                    },
                    {
                        "command": "./a.out"
                    }
                ],
                "description": "QQ",
                "file_name": "test.cpp",
                "id": 12,
                "language_id": 3,
                "priority": 999,
                "setter_user_id": 1,
            }
        }
    },
]
