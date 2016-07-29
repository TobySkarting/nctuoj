data = [
    {
        "name": "post_problems",
        "url": "/api/problems/",
        "method": "post",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
            "group_id": 1,
            "title": "test problem",
            "description": "description",
            "input": "input",
            "output": "output",
            "sample_input": "sample_input",
            "sample_output": "sample_output",
            "hint": "hint",
            "source": "source",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "group_id": 1,
                "hint": "hint",
                "id": 10001,
                "input": "input",
                "interactive": 0,
                "output": "output",
                "pdf": False,
                "sample_input": "sample_input",
                "sample_output": "sample_output",
                "score_type_id": 1,
                "setter_user_id": 1,
                "source": "source",
                "title": "test problem",
                "verdict_id": 1,
                "visible": 0
            }
        }
    },
    {
        "name": "test_get_problem",
        "url": "/api/problems/10001/",
        "method": "get",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "group_id": 1,
                "hint": "hint",
                "id": 10001,
                "input": "input",
                "interactive": 0,
                "output": "output",
                "pdf": False,
                "sample_input": "sample_input",
                "sample_output": "sample_output",
                "score_type_id": 1,
                "setter_user_id": 1,
                "source": "source",
                "title": "test problem",
                "verdict_id": 1,
                "visible": 0
            }
        }
    },
    {
        "name": "test_put_problem",
        "url": "/api/problems/10001/",
        "method": "put",
        "payload": {
            "token": "P8AWkMjJFcEjsc7rpVfBk9XkBt99H4KjyHSHBwPtzXtyl3LtUeA6CQl8EVcdZrhr", 
            "title": "Hello PUT",
        },
        "response_status": 200,
        "response_data": {
            "msg": {
                "description": "description",
                "group_id": 1,
                "hint": "hint",
                "id": 10001,
                "input": "input",
                "interactive": 0,
                "output": "output",
                "pdf": False,
                "sample_input": "sample_input",
                "sample_output": "sample_output",
                "score_type_id": 1,
                "setter_user_id": 1,
                "source": "source",
                "title": "Hello PUT",
                "verdict_id": 1,
                "visible": 0
            }
        }
    },
    {
        "name": "test_delete_problem",
        "url": "/api/problems/10001/",
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
