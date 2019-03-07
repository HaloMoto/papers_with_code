#!/usr/bin/env python
"""
This file shouldn't be in the develop branch but it is because I want to quickly move forward.
For the future, files in the repository should be in finalized (or on the way to finalized) state
and should be essential to running the app.

When adding files to the repo, think
Can the app run without this?
- If no, include it.
- If yes, but it provides a very standard way of testing (AKA unit tests), include it.
- Otherwise, nah. You can keep it locally to run, but it doesn't need to be tracked. I do this
  often with shell scripts like test.sh or a test_whatever.py type thing that I can run to check
  my code is working.
"""

from wayfare.models.location import Location
from wayfare.models.ride import Ride
from wayfare.models.time_range import TimeRange
from wayfare.models.user import User
from datetime import datetime
from wayfare.models.status import Status
from wayfare.models.passenger import Passenger



slo = Location(
    name='San Luis Obispo'
)
slo.create()
sf = Location(
    name='San Francisco'
)
sf.create()
r = Ride( 
    start_location_id=1,
    destination_id=2,
    departure_date = datetime(2015, 6, 5),
    capacity = 4,
    driver_id = 1,
    time_range_id = 1
)
r.create()
tr = TimeRange(
    description = 'Early Morning',
    start_time = '5',
    end_time='9'
)
tr.create()
u = User(
    first_name = 'ollie',
    last_name = 'wang',
    email = 'owang@calpoly.edu',
    password = 'password'
)
u.create()
u2 = User(
    first_name = 'quan',
    last_name = 'tran',
    email = 'qtran@calpoly.edu',
    password = 'password123'
)
u2.create()
u3 = User(
    first_name = 'phil',
    last_name = 'daniel',
    email = 'pdaniel@calpoly.edu',
    password = 'password321'
)
u3.create()
st = Status(
    description = 'Pending'
)
st.create()
st2 = Status(
    description = 'Confirmed'
)
st2.create()

print(User.query.all())
print(TimeRange.query.all())
print(Ride.query.all())


print("Append quan and phil to ride 1 ")
ps = Passenger(
    user_id = 1,
    ride_id = 1,
    status_id = 1,
    updated = datetime.utcnow()
)
ps.create()
print(Passenger.query.all()[0].updated)

ps.update({"updated": datetime.utcnow()})
print(Passenger.query.all()[0].updated)

ps2 = Passenger(
    user_id = 2,
    ride_id = 1,
    status_id = 1
)
ps2.create()

print("pre-updated timpstamp")
print(Passenger.query.all()[1].updated)
print("update second passenger ride status")
ps2.update({'status_id':2})
print("updated timpstamp")
print(Passenger.query.all()[1].updated)

print("find passengers by ride id(1): ")
print(Passenger.find_by_ride_id(1).all())

print("pre delete passenger")
print(Passenger.query.all())
print("delete passenger by id 1")
Passenger.find_by_id(1).delete()
print("post delete passenger")
print(Passenger.query.all())

print("find passengers by user id(1): ")
print(Passenger.find_by_user_id(1).all())

print("find passengers by Status id(1): ")
print(Passenger.find_by_status_id(1).all())

print("find passengers by Status id(2): ")
print(Passenger.find_by_status_id(2).all())

print("delete all")
Passenger.delete_all()
print(Passenger.query.all())
