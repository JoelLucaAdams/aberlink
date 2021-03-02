# Attendance API endpoint

Currently waiting for the API to be setup for sending a request to update a students attendance. Will leave for a few weeks and then contact Leslie Johns [lej] if there is no response.

Below is an example of the JSON objects which will be sent and recieved from the API endpoint:

Request:

```json
{
    "username": "joa38"
}
```

Response:

```json
{
    "status_updated": "true",
    "request": "200", 
    "module_code": "CS32120"
 }
```

<https://integration.aber.ac.uk/joa38/good.php> will always return `{"status_updated":"true","request":"200","module_code":"CS32120"}`

<https://integration.aber.ac.uk/joa38/bad.php> will always return `{"status_updated":"false","request":"400","error_message":"Unknown user or no event"}`

<https://integration.aber.ac.uk/joa38/submit.php> will return either of the above (with correct module code if successful) depending on the timetable and user submitted.

I can’t see anything on discord for semester 2 so submit.php will not return successfully hence the first two url’s.


Thank you to Leslie Jones [lej] for setting this up.
