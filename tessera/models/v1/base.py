from tessera.lib import to_camel_case
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
    def to_json(self, ignoreFields=[]):
        """This method will convert a class to a JSON serializable dict while
        ignoring any fields passed into it via ignoreFields"""
        s = self.__dict__

        jsn = {}
        for k, v in s.items():
            # If the key starts with _ assume it's private and skip it
            # or if it has _id we don't want to see it
            # or if it's in the ignoreFields we were passed skip it.
            if k.startswith("_") or "_id" in k or k in ignoreFields:
                continue
            if isinstance(v, Base):
                jsn[to_camel_case(k)] = v.to_json()
            else:
                jsn[to_camel_case(k)] = v
        return jsn

