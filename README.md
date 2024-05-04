# Zero Hunger API 

The Zero Hunger API is a backend application built using Flask to help manage users and contacts in support of the Zero Hunger campaign.

## Features

- **User Management**: Register, log in, update, and delete users.
- **Contact Management**: Add, update, and delete contacts.
- **Authentication**: Uses JWT for user authentication.

## Technologies Used

- Flask as the web application framework.
- Flask-SQLAlchemy as the ORM.
- Flask-JWT-Extended for JWT-based authentication.
- MySQL as the database management system.

## Environment Setup

Ensure you have Python and pip installed. You also need to have MySQL set up and running.

## Installation

- Clone this repository.

```bash
   git https://github.com/Gustitreshana/GROUP_E_Backend_RevoU.git
```

- Install dependencies using pip

```bash
   pip install -r requirements.txtl
```

- Create a `.env` file at the root of the project and configure the environment variables (DB_URI, JWT_SECRET_KEY, etc.).

- Run the application.

```bash
   python main.py
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
