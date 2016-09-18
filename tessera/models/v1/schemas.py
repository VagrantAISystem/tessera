from copy import deepcopy

user_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'username': { 'type': 'string' },
        'email': { 'type': 'string', 'format': 'email' },
        'fullName': { 'type': 'string' },
        'isAdmin': { 'type': 'boolean' },
    },
    'required': ['username'],
}

user_signup_schema = deepcopy(user_schema)
user_signup_schema['properties']['password'] = { 'type': 'string' }
user_signup_schema['required'] += ['fullName', 'email', 'password']

team_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'description': { 'type': 'string' },
        'icon': { 'type': 'string' },
        'teamLead': user_schema,
    },
    'required': [ 'name', 'teamLead' ],
}

project_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'pkey': { 'type': 'string' },
        'repo': { 'type': 'string' },
        'homepage': { 'type': 'string' },
        'team': team_schema,
        'projectLead': user_schema,
    },
    'required': [ 'pkey', 'name', 'projectLead' ],
}

status_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'statusType': { 'enum': [ 'TODO', 'IN_PROGRESS', 'DONE']},
    },
    'required': [ 'id', 'name', 'statusType' ],
}

field_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'value': {
            'oneOf': [
                {
                    "type": "string",
                },
                {
                    "type": "number",
                }
                ]
        },
    },
    'required': ['id', 'name', 'value']
}

ticket_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'ticketKey': { 'type': 'string' },
        'summary': { 'type': 'string' },
        'description': { 'type': 'string' },
        'updatedAt': { 'type': 'string', 'format': 'date-time' },
        'createdAt': { 'type': 'string', 'format': 'date-time' },
        'assignee': user_schema,
        'reporter': user_schema,
        'project': project_schema,
        'status': status_schema,
        'fields': {
            'type': 'array',
            'items': field_schema,
        },
    },
    'required': [ 'summary', 'description', 'reporter' ],
}

ticket_test_schema = deepcopy(ticket_schema)
ticket_test_schema['required'] += ['assignee', 'ticketKey']

comment_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'body': { 'type': 'string' },
        'author': user_schema,
    },
    'required': [ 'body', 'author' ],
}

role_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'members': {
            'type': 'array',
            'items': user_schema,
        },
    },
    'required': [ 'id', 'name' ],
}
