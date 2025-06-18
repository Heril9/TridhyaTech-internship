# Flask Project Documentation

## Project Overview
This project is a Flask application that includes user and role management functionalities. It consists of two main files:

1. **mini_project.py**: This file contains a Flask application with user and role management functionalities. It defines models for `User` and `Role`, and provides routes for creating, retrieving, updating, and deleting users and roles.

2. **flaskex.py**: This file contains a simple Flask application with basic routes for handling GET and POST requests. It includes a home route and a submit route that processes JSON data.

## Installation
To set up the project, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   ```

2. Navigate to the project directory:
   ```
   cd Flask_project_2
   ```

3. (Optional) Create a virtual environment:
   ```
   python -m venv venv
   ```

4. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

5. Install the required packages:
   ```
   pip install Flask Flask-SQLAlchemy
   ```

## Usage
To run the applications, execute the following commands in the terminal:

- For `mini_project.py`:
  ```
  python mini_project.py
  ```

- For `flaskex.py`:
  ```
  python flaskex.py
  ```

Visit `http://127.0.0.1:5000` in your web browser to access the applications.

## API Endpoints
### mini_project.py
- **Users**
  - `POST /users`: Create a new user.
  - `GET /users`: Retrieve all users.
  - `GET /users/<user_id>`: Retrieve a specific user by ID.
  - `PUT /users/<user_id>`: Update a specific user by ID.
  - `DELETE /users/<user_id>`: Delete a specific user by ID.

- **Roles**
  - `POST /roles`: Create a new role.
  - `GET /roles`: Retrieve all roles.
  - `GET /roles/<role_id>`: Retrieve a specific role by ID.
  - `PUT /roles/<role_id>`: Update a specific role by ID.
  - `DELETE /roles/<role_id>`: Delete a specific role by ID.

### flaskex.py
- `GET /`: Home route.
- `POST /submit`: Submit JSON data.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.