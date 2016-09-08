import sys
from tessera import db
from tessera.v1.models import *

testadmin = User(username="testadmin",
                 email="test@example.com",
                 password="test",
                 full_name="Test Testerson II",
                 is_admin=True)
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

# make the default statuses
backlog     = Status(name="Backlog", status_type=0)
in_progress = Status(name="In Progress", status_type=1)
on_hold     = Status(name="On Hold", status_type=1)
closed      = Status(name="Closed", status_type=2)

backlog.next_statuses.append(in_progress)
backlog.next_statuses.append(on_hold)
in_progress.next_statuses.append(closed)
in_progress.next_statuses.append(on_hold)
on_hold.next_statuses.append(backlog)
on_hold.next_statuses.append(in_progress)
on_hold.next_statuses.append(closed)
closed.next_statuses.append(backlog)

db.session.add(backlog)
db.session.add(in_progress)
db.session.add(on_hold)
db.session.add(closed)
db.session.commit()

statuses = [ backlog, in_progress, on_hold, closed ]

testp = Project(pkey="TEST", name="Test Project")
testp.project_lead = testadmin
a_team.projects.append(testp)

s = 0
for i in range(100):
    t = Ticket(ticket_key=testp.pkey + "-" +
               str(len(Project.query.filter_by(pkey=testp.pkey).first().tickets) + 1),
               summary="This is test ticket #" + str(i + 1),
               description="This isn't helplful")
    t.assignee = test
    t.reporter = testadmin
    t.status   = statuses[s]
    s += 1
    if s == len(statuses):
        s = 0
    for i in range(5):
        cmt = Comment(body="Hi I'm a comment. #" + str(i),
                      author=test)
        t.comments.append(cmt)
    testp.tickets.append(t)

db.session.add(a_team)
db.session.add(testp)
db.session.commit()
