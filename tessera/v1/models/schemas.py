from copy import deepcopy

user_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'password': { 'type': 'string' },
        'username': { 'type': 'string' },
        'email': { 'type': 'string' },
        'fullName': { 'type': 'string' },
        'isAdmin': { 'type': 'boolean' },
    },
    'required': ['username'],
}

user_signup_schema = deepcopy(user_schema)
user_signup_schema['required'] += ['fullName', 'email', 'password']

team_schema = {
    'type': 'object',
    'properties': {  
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'icon': { 'type': 'string' },
        'team_lead': user_schema,
    },
    'required': [ 'name' ],
}

team_create_schema = deepcopy(team_schema)
team_create_schema['required'] += ['team_lead']

project_schema = {
    'type': 'object',
    'properties': {  
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'pkey': { 'type': 'string' },
        'repo': { 'type': 'string' },
        'homepage': { 'type': 'string' },
        'team': team_schema,
        'project_lead': user_schema,
    },
    'required': [ 'pkey', 'name', 'project_lead' ],
}

status_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'statusType': { 'type': 'integer' },
    },
    'required': [ 'id', 'name', 'statusType' ],
}

field_schema = {
    'type': 'object',
    'properties': {
        'id': { 'type': 'integer' },
        'name': { 'type': 'string' },
        'value': { 'type': ['string', 'integer', 'float'] },
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
