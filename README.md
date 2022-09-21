# TAP-Meteor

# Run Application with Docker
## Build and Run Docker Compose
- docker-compose up --build -d   
## Stop Docker Compose
- docker-compose down

## View logs
- docker ps: get container Id
- docker logs - f {container_id}

# Database Overview
<img width="452" alt="image" src="https://user-images.githubusercontent.com/28836136/191396531-6de3f9d9-1643-4e00-8557-c27ba7f52833.png">

# Assumptions
1. Each household is identified by the unique key (housingUnit)
2. Member must be associated to a household 
3. Member can be added without spouse
4. Member can be eligible for multiple grant scheme if they meet the requirments specified

# Testing APIs
1. Naviagate to /postman
2. Import Meteor.postman_collection.json into Postman 
3. Test the APIs!

(Example response are included in the json file)
