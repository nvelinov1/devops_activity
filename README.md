# DevOps Activity - Nikola Velinov
*Note: Unable to complete SMTP functionality*

## How to Setup
1. Clone the repository using: `git clone https://github.com/nvelinov1/devops_activity`
2. Change into the repository directory: `cd ./devops_activity`
3. In the main repository directory, rename the `.env.example` file to `.env`and change any values if needed
4. Change into the monitoring service directory using `cd ./monitoring`
5. Rename the `.env.example` file to `.env`and change any values if needed (make sure SMTP configuration values match the `.env` file in the main repository directory
6. Change back into the main repository directory, and run docker-compose in detached mode using: `docker-compose up -d`

## How to Test Monitoring Service
1. After running `docker-compose up -d`, check the list of containers using `docker ps` and take note of the ID of the `devops_activity-web` container
2. To check for a connection error, stop the web server container using: `docker container stop (id)` 
3. Check the logs of the monitoring service container using `docker container logs -f (id)` and verify that a `"connection error"`  message is printed in the logs (may need to wait one minute for the job to occur)
4. Shut down the compose stack using: `docker-compose down`
5. To check for a wrong status code, first remove the web server docker image using `docker rmi -f devops_activity-web`
6. Navigate to `./web/app.py` add a syntax error in the `hello()` function
7. Build the compose stack using `docker compose up -d`
8. Repeat step 3, verify that a `"status code error"` message is printed in the monitoring service container logs.
9. Repeat steps 4-8. Instead, of adding a syntax error, add `time.sleep(10)`in the `hello()` function to check for a timeout. Verify that a `"connection error"` message is printed in the monitoring service container logs.

## Implementation Explanation
I decided to implement a Flask application using APScheduler to monitor for errors in the application. APScheduler allows background tasks to run at an interval through Flask, which fits the requirements for this implementation. I implemented the SMTP integration using smtplib, but was not able to make it functional due to a `[Errno 111] Connection refused` error message. I used console logging to implement similar functionality.

## Assumptions
- The user's underlying Linux environment is able to run docker compose, the monitoring service did not include any checks to verify the user's Linux environment
- Only the / endpoint was tested using the monitoring service, additional code would need to be implemented to check for more endpoints (if aplicable)
- Only 200 status codes are accepted using the monitoring service, additional checks would need to be added if more status codes were to be included

## Pros/Cons
### Pros
- The implementation is able to monitor errors at the required interval and output an error message to the console
- The Monitoring Service uses Flask + Docker, same as the web application service
- The Monitoring Service includes .env configurations for SMTP and other application settings (interval, timeout), allowing for the application to be configured easily

### Cons
- The Code for the SMTP functionality is implemented, but it is not functional (returns `[Errno 111] Connection refused`)
- The .env configuration is not implemented for the application ports
- The monitoring service only checks one web service endpoint (/)
- The monitoring service only considers status code 200 as valid, any other status code (e.g.: 201), would still be considered an error


## Test Feedback
Overall, the test was fair and tested DevOps skills (Linux, Docker) and Python programming skills in a fair way. The difficulty of the application to implement was fair, I did not find the web service difficult to understand. Only difficulty I had was with the SMTP service, I had not worked with beforehand.
