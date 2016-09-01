from tessera import db
from sqlalchemy import or_
from jsonschema import validate
from tessera.v1.models.base import Base

class Team(Base):
    """Team is a container for projects.
    
    When changing the name for a team use set_name as this properly updates
    dependent fields for Team. YOU WILL HAVE A BAD TIME IF YOU DO team.name =
    SOME_NAME.
    """
    name     = db.Column(db.String(120), nullable=False, unique=True)
    url_slug = db.Column(db.String(150), nullable=False, unique=True)
    icon     = db.Column(db.String(150))    

    team_lead_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    projects = db.relationship('Project', backref='team', lazy='dynamic')
    members  = db.relationship('Membership', backref='team', lazy='dynamic')
    
    def __init__(self, *, name, icon=""):
        self.name     = name
        self.url_slug = name.lower().replace(" ", "-")
        self.icon          = icon

    def set_name(self, name):
        self.name = name
        self.url_slug = name.lower().replace(" ", "-")

    def from_json(json):
        validate(json, team_schema)
        t = Team(name=json["name"],
                 icone=json.get("icon", ""))
        un = json.get("project_lead",{}).get("username", "")
        lead =  User.query.filter_by(username=un).first()
        t.team_lead = lead
        return t

    def get_by_name_or_stub(name):
        t = Team.query.filter(or_(Team.name == name, 
                                  Team.url_stub == name)).first()
        if t == None:
            raise AppError(status_code=404,
                           message="That team does not exist")
        return t

    def from_json(json):
        validate(json, team_schema)
        t = Team(name=json["name"],
                 icone=json.get("icon", ""))
        un = json.get("project_lead",{}).get("username", "")
        lead =  User.query.filter_by(username=un).first()
        t.team_lead = lead
        return t

    def __repr__(self):
        return "<Team %r>" % (self.name)

team_schema = {
    "type": "object",
    "properties": {  
        "name": { "type": "string" },
        "icon": { "type": "string" },
        "team_lead": { 
            "type": "object",
            "properties": {
                "id": { "type": "integer" },
                "username": { "type": "string" },
                "email": { "type": "string" },
                "fullName": { "type": "string" },
            },
            "required": [ "username" ],
        },
    },
    "required": [ "team_lead", "name" ],
}
