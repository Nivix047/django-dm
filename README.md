# Direct Messaging App

## Overview

Direct Messaging App is a comprehensive backend solution for a Direct Messaging (DM) application built with Django. It provides a robust platform for users to engage in private and group messaging. Its design centers on high modularity, allowing for seamless integration with various front-end frameworks and platforms. This flexibility makes it an ideal choice for developers looking to incorporate direct messaging capabilites into their existing systems or to build upon a robust and scalable foundation.

## Features

- **User Management:** Register, login, logout, and update user profiles.
- **Friend Management:** Add, delete, and list friends. Manage friend requests.
- **Direct Messaging:** Send and receive private messages.
- **Group Chat:** Create groups, add/remove friends to/from groups, and send/receive group messages.
- **Security:**: Token-based authentication for secure access.

## Technology Stack

- Django
- Django REST Framework
- PostgreSQL
- Token Authentication

## Installation

1. Create and activate a Virtual Environment (optional but recommended).

- python3 -m venv venv
- source venv/bin/activate

2. Install dependencies.

- pip install -r requirements.txt

3. Create a PostgreSQL database.

4. Environment Variables:
   SECRET_KEY=your_secret_key
   DEBUG=True
   DATABASE_NAME=your_database_name
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_HOST=your_database_host
   DATABASE_PORT=your_database_port

## Testing

For testing the API endpoints of Direct Messaging App, manual testing can be performed using tools like Insomnia or Postman. These tools allow for a detailed examination of API responses and are essential for ensuring the correct functioning of your application's endpoints.

### Steps for Manual Testing

1. **Install a Testing Tool:** Download and install Insomnia or Postman.
2. **Configure and Send Requests:** Set up your testing environment to target your local server (usually `http://localhost:8000`).
3. **Create and Send Requests:** Manually create requests for various API endpoints. Include necessary headers and authentication tokens.
4. **Analyze Responses:** Check the responses for correctness in terms of status codes and returned data.
5. **Debugging:** Use insights from these tests to identify and fix issues in your API.

## Usage

To use the Direct Messaging App, follow these steps:

1. **Configure Enviornment Variables:** Ensure that the `.env` file is correctly filled out with all necessary settings like `SECRET_KEY`, database configurations, and other environment-specific variables.

2. **Install Dependencies:** Run `pip3 install -r requirements.txt` to install all required dependencies.

3. **Start the Server:** Execute `python3 manage.py runserver` to start the Django development server.

Once the server is running, the API endpoints are accessible and ready for interaction.
