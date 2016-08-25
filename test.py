from tessera import db
db.create_all()
from tessera.lib.models import *

m = User("test", "test@example.com", "Test Testerson", "test")

print(m)
