import sys
from tessera import db
from tessera.v1.models import *

testadmin = User(username="testadmin", 
                 email="test@example.com", 
                 password="test", 
                 full_name="Test Testerson II")
test = User(username="test", 
            email="test1@example.com", 
            password="test", 
            full_name="Test Testerson")
db.session.add(testadmin)
db.session.add(test)
db.session.commit()

a_team = Team(name="The A Team")
a_team.team_lead = test
db.session.add(a_team)
db.session.commit()

testp = Project(pkey="TEST", name="Test Project")
testp.project_lead = testadmin
a_team.projects.append(testp)

for i in range(100):
    t = Ticket(ticket_key=testp.pkey + "-" +
               str(Project.query.filter_by(pkey=testp.pkey).first().tickets.count() + 1),
               summary="This is test ticket #" + str(i + 1), 
               description="This isn't helplful")

    testp.tickets.append(t)

db.session.add(a_team)
db.session.add(testp)
db.session.commit()
