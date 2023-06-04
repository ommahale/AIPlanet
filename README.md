## AI Planet Assignment
This is a submission for AI Planet Assignment
## How to run
1. Clone the repository
2. Install and run docker daemon
3. Run the following command
```bash
docker-compose up --scale app= $NO_OF_INSTANCES
deocker-compose run app python manage.py migrate
```
4. Open the browser and go to http://localhost:8000
5. You can see the result of the assignment

## Go to API docs:
1. Go to http://localhost:8000/api/v1/swagger/ or http://localhost:8000/api/v1/redoc/
2. You can see the API docs

Note: If you get operational error in first run please retry the command in step 3 again. This happens because the database sometimes is not ready yet to connect to application. Or the databasse hasn't been initialized yet.
