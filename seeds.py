import random
from tessera import db
from tessera.models.v1 import *

db.create_all()

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

b_team = Team(name="The B Team")
b_team.team_lead = testadmin

db.session.add(a_team)
db.session.add(b_team)
db.session.commit()

# make the default statuses
backlog     = Status(name="Backlog", status_type="TODO")
in_progress = Status(name="In Progress", status_type="IN_PROGRESS")
on_hold     = Status(name="On Hold", status_type="IN_PROGRESS")
closed      = Status(name="Closed", status_type="DONE")

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

# Make default fields
story_points    = Field(name="Story Points", data_type="INTEGER")
estimated_hours = Field(name="Estimated Hours", data_type="INTEGER")
logged_hours    = Field(name="Logged Hours", data_type="INTEGER")
test_field1     = Field(name="Test String Field", data_type="STRING")
test_field2     = Field(name="Test Text Field", data_type="TEXT")
test_field3     = Field(name="Test Integer Field", data_type="INTEGER")
test_field4     = Field(name="Test Float Field", data_type="FLOAT")

db.session.add(story_points)
db.session.add(estimated_hours)
db.session.add(logged_hours)
db.session.add(test_field1)
db.session.add(test_field2)
db.session.add(test_field3)
db.session.add(test_field4)
db.session.commit()

testp = Project(pkey="TEST", name="Test Project")
testp.project_lead = testadmin

testp2 = Project(pkey="TEST2", name="Test Project 2")
testp2.project_lead = test

a_team.projects.append(testp)
a_team.projects.append(testp2)

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

    hours_estimated = FieldValue(field_id=estimated_hours.id,
                                 integer_value=random.randint(0, 100))

    hours_worked = FieldValue(field_id=logged_hours.id,
                              integer_value=random.randint(0, 100))
    points = FieldValue(field_id=story_points.id,
                        integer_value=random.randint(0, 100))
    t.fields.append(points)
    t.fields.append(hours_worked)
    t.fields.append(hours_estimated)
    testp.tickets.append(t)

db.session.add(a_team)
db.session.add(testp)
db.session.commit()
