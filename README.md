# Zero Hunger API

The Zero Hunger API is a backend application built using Flask to help manage users, contacts, and donations in support of the Zero Hunger campaign.

## Features

- **User Management**: Register, log in, update, and delete users.
- **Contact Management**: Add, update, and delete contacts.
- **Donation Management**: Add, view, update, and delete donations.
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
git clone https://github.com/Gustitreshana/GROUP_E_Backend_RevoU.git
```

- Install dependencies using pip

```bash
pip install -r requirements.txt
```

- Create a `.env` file at the root of the project and configure the environment variables (DATABASE_URI, JWT_SECRET_KEY, etc.).

- Run the application.

```bash
python app.py
```

## Usage

### Registering a New User

```bash
POST /register
{
"username": "newuser",
"email": "newuser@example.com",
"password": "strongpassword",
"realname": "User Real Name",
"address": "User Address",
"occupation": "User Occupation"
}
```

### Login User

```bash
POST /login
{
"email": "newuser@example.com",
"password": "strongpassword"
}
```

### Adding Contact

```bash
POST /contacts
{
"name": "Contact Name",
"email": "contact@example.com",
"phone": "1234567890",
"user_id": 1
}
```

### Adding Donation

```bash
POST /donations
{
"nominal": 50000,
"from_id": 1
}
```

### Viewing All Donations

```bash
GET /donations
```

This update includes the addition of donation management and minor fixes to syntax and provided information. Ensure to update the `.env` and `requirements.txt` files according to the latest needs of your project.
