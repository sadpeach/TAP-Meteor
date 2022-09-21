# Install All Required Package
- pip install requirements.txt

# Run Application Locally
- python3 app.py

# Run Application with Docker locally
## Build Docker
- docker build --no-cache -t flask-backend .
## Run Docker
- docker run -it -d -p 5001:5001 flask-backend
## View logs
- docker ps: get container Id
- docker logs - f {container_id}

# Deployment Details
- The backend is deployed on google cloud run using container.
- Git hub workflow configuration file is set up to run the deployment when new code is pushed to the branch.
- The backend interacts with cloud database (planetscale) for data insertion and retrieval.

# Assumption
- Each household is identified by unique key (id)
- Every member in the household are eligible to multiple grants if they satisfy the critieria.

# Testing the APIs
1. Import the json file from /postman
2. Run the APIs under Dev/local enviornment
(Example Responses and included in the json)



