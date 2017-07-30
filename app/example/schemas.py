POST_TEST = {
    "type": "object",
    "additionalProperties": False,
    "required": ["name"],
    "properties": {
        "name": {"type": "string"},
    }
}

GET_TEST = {
    "type": "object",
    "additionalProperties": False,
    "properties": {}
}
