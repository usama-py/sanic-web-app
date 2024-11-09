# Simple Survey App

This project is a full-stack web application that consists of a backend API built with Python (using the Sanic framework) and a frontend built with React. The backend interacts with a MongoDB database, while the frontend provides a user interface to submit surveys. Both components are containerized using Docker and orchestrated with Docker Compose.

## Table of Contents

- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Environment Variables](#environment-variables)
- [Endpoints](#endpoints)
- [Running Tests](#running-tests)
- [Technologies Used](#technologies-used)
- [Development Workflow](#development-workflow)
- [License](#license)
---

## Getting Started

### Prerequisites

Make sure you have the following installed:

- Docker
- Docker Compose

### Setup Instructions

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/simplesurveyapp.git
   cd sanic-web-app
   ```

2. **Start the application with Docker Compose:**
    ```bash
    docker-compose up --build
    ```
This will
- Build and run the backend API at http://localhost:5050.
- Build and serve the React frontend at http://localhost:3000.
- Run a MongoDB instance on mongodb://localhost:27017.

3. **Access the App:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:5050

## Project Structure

- backend/: Contains the Python backend API code.
    - app.py: Main entry point for the Sanic server.
    - controllers/: Defines survey processing and health check endpoints.
    - services/: Contains logic for data processing, validation, and storage.

- frontend/: Contains the React frontend code.

- docker-compose.yml: Defines services for backend, frontend, and MongoDB.

- requirements.txt: Lists Python dependencies for the backend.


## Environment Variables

### Create a .env file in the backend/ directory with the following variables:

- MONGO_URI: MongoDB connection string, default is mongodb://mongo:27017/mydatabase.
- PORT: Port for the Sanic server (optional, defaults to 5050).
- ENVIRONMENT: Set to local for local development.
- GEMINI_API_KEY: Gemini api key REQUIRED for the app to work!

## Endpoints

- POST /process_survey: Processes a survey submission.

### Request Body:
 ```bash
        {
            "user_id": "test_user",
            "survey_results": [
                {"question_number": 1, "question_value": 7},
                {"question_number": 2, "question_value": 7},
                {"question_number": 3, "question_value": 4},
                {"question_number": 4, "question_value": 1},
                {"question_number": 5, "question_value": 6},
                {"question_number": 6, "question_value": 6},
                {"question_number": 7, "question_value": 2},
                {"question_number": 8, "question_value": 7},
                {"question_number": 9, "question_value": 6},
                {"question_number": 10, "question_value": 6}
            ]
        }

 ```
### Response:
```bash
{
  "message": "Survey data saved!",
  "insights": { ... }  // Processed insights from survey data
}
```

## Running Tests
### To run backend tests in docker, use:

```bash
    cd backend
    pytest
```

## Testing Coverage
### To generate a coverage report:

```bash
    Copy code
    pytest --cov=.
```

## Technologies Used
- Backend: Sanic, MongoDB, Pymongo, Sanic CORS, Docker
- Frontend: React, Docker
- Testing: Pytest, Sanic Testing

4. **Install Dependencies (Optional):**

   If you'd like to run the backend or frontend locally without Docker, you can install the required dependencies manually:

   - **Backend**:
     ```bash
     cd backend
     pip install -r requirements.txt
     ```

   - **Frontend**:
     ```bash
     cd frontend
     npm install
     ```

5. **Running Locally (without Docker)**:

   - **Backend**: Start the Sanic server
     ```bash
     cd backend
     python app.py
     ```

     By default, the backend will run on `http://localhost:5050`. If the `PORT` environment variable is set, the backend will use the specified port.

   - **Frontend**: Start the React development server
     ```bash
     cd frontend
     npm start
     ```

     This will serve the frontend on `http://localhost:3000`, and it will automatically proxy API requests to `http://localhost:5050`.

---

## Development Workflow

This project uses **Chokidar** to enable automatic reloading in both the frontend and backend services. Code changes in the `backend/` and `frontend/` directories will be reflected in real-time when running through Docker Compose.

### Common Development Commands

- **Rebuild the Docker containers** (after making configuration changes):
  ```bash
  docker-compose up --build
  ```
- **Stop all containers:**
   ```bash
    docker-compose down
    ```
- **Remove all containers, networks, and volumes:**
    ```bash
    docker-compose down -v
    ```

## License

- This project is open-source and available under the MIT License.
