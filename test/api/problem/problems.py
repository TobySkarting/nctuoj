data = [
    {
        "name": "test_post_problems",
        "url": "/api/problems/",
        "method": "post",
        "payload": {
            "token": "ADMIN@TOKEN", 
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
]
