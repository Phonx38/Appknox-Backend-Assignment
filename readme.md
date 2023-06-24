# Appknox-Backend-Assignment

Make sure you have the following tools installed on your machine:

- Docker
- Docker Compose

# Getting Started

1. Clone the repository:

   ```bash
   git clone https://github.com/Phonx38/Appknox-Backend-Assignment.git
   ```

2. Navigate to the project directory:

   ```bash
   cd appknox-assignment
   ```

3. Build Docker Image and start detached containers:

   ```bash
   docker-compose up -d --build
   ```

Now you're ready to access API endpoints at http://localhost:8000/<endpoint_name>/

4. Shutting down containers:

   ```bash
   docker-compose down
   ```

# Accessing API endpoint docs

- You can access api docs by going to this url:

```bash
   http://localhost:8000/api/schema/swagger-ui/
```

# Testing

- To run tests you can use following commands:

  - Run all tests:

  ```bash
  docker-compose exec web  pytest
  ```

# Miscellanous

- I have not removed .env file from repo for your ease of use.
