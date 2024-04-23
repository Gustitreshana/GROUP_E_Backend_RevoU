# Zero Hunger API

Zero Hunger API is a backend application built using Flask to help manage users and contacts in support of the Zero Hunger campaign.

## Features

- **User Management**: Register, login, update, and delete users.
- **Contact Management**: Add, update, and delete contacts.
- **Authentication**: Using JWT for user authentication.

## Technologies Used

- Flask as a web application framework.
- Flask-SQLAlchemy as the ORM.
- Flask-JWT-Extended for JWT-based authentication.
- MySQL as a database management system.

## Environment Setup

Make sure you have Python and poetry installed. You also need to have MySQL set up and running.

## Installation

- Clone this repository.

```bash
   git clone https://github.com/yourusername/Zero_Hunger_API.git
   cd Zero_Hunger_API
```

- Install dependencies using poetry

```bash
   poetry install
```

- Create a `.env` file in the root of the project and configure the environment variables (DB_URI, JWT_SECRET_KEY, etc.).

- Run the application.

```bash
   poetry run flask --app app run
```

## Usage

### Registering a New User

```bash
POST /register
{
"username": "newuser",
"email": "newuser@example.com",
"password": "strongpassword"
}
```

### Login User

```bash
POST /login
{
"username": "newuser",
"password": "strongpassword"
}
```

### Adding Contact

```bash
POST /contacts
{
"name": "Contact Name",
"email": "contactemail@example.com",
"phone": "1234567890"
}
```
