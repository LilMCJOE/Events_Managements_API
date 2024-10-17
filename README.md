-------------------------------------
API URL: songa123.pythonanywhere.com
-------------------------------------

You can use tools like Postman or curl to test the endpoints:
1. User Registration:
    * POST /api/register/ with username, email, and password.
2. Obtain JWT Token:
    * POST /api/login/ with username and password to receive the access and refresh tokens.
3. Create Event:
    * POST /api/events/ with event data (must include JWT token in the Authorization header).
4. List Events:
    * GET /api/events/.
5. Retrieve, Update, or Delete Event:
    * GET/PUT/DELETE /api/events/<event_id>/.
6. Register for Attendance:
    * POST /api/attendances/ with the event ID in the request body({ "event": 1})
7. List My Attendances:
    * GET /api/my-attendances
    * 
List All Upcoming Events with Pagination:
* GET /api/events/?page=1 - Retrieves the first page of events.
Filter by Title:
* GET /api/events/?title=Birthday - Retrieves events with "conference" in the title.
Filter by Location:
* GET /api/events/?location=Kigali - Retrieves events located in "New York".
Filter by Date Range:
* GET /api/events/?date_time_after=2024-01-01T00:00:00Z&date_time_before=2024-12-31T23:59:59Z - Retrieves events happening within the specified date range.

my api will enforce a maximum capacity for events and prevent users from registering once that capacity is reached.
