from tessera import db

class Base(db.Model):
    """Base class that all models are derived from.
    
    It defines the id, created_at, and updated_at fields for all models.
    """
    __abstract__ = True

    id         = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), 
                           onupdate=db.func.current_timestamp())

    def to_json(self):
        """This drops the internal sqlalchemy field which won't JSONify"""
        s = self.__dict__
        s.pop('_sa_instance_state', None)
        return s
