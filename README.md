# Zero Hunger API (- **still under development by Iman**)

The Zero Hunger API is a backend application built using Flask to help manage users, contacts, and donations in support of the Zero Hunger campaign.

## Features

- **User**: Register, log in, update, and delete users.
- **Program Donasi**: Add, update, and delete contacts.
- **Donatur**: Add, view, update, and delete donature.
- **Donasi**: Add, view, update, and delete donasi.
- **Authentication**: Uses JWT for user authentication.

- **still under development by Iman**

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

- Install dependencies using "poetry add"

```bash
poetry add ...
```

- Create a `.env` file at the root of the project and configure the environment variables (DATABASE_URI, JWT_SECRET_KEY, etc.).

- Run the application.

```bash
poetry run flask --app app run
```

## Usage

## API Documentation

For more detailed information on API endpoints and their usage, please refer to our [API Documentation](https://documenter.getpostman.com/view/29213022/2sA3JDhQs8).

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
"email": "newuser@example.com",
"password": "strongpassword"
}
```

### Adding Contact

```bash
POST /contacts
{
# "name": "Contact Name",
# "email": "contact@example.com",
# "phone": "1234567890",
# "user_id": 1
- **still under development by Iman**
}
```

### Adding Program, Donatur and Donasi

```bash
POST /programs
{
# "nominal": 50000,
# "from_id": 1
- **still under development by Iman**
}
```
```bash
POST /donatur
{
# "nominal": 50000,
# "from_id": 1
- **still under development by Iman**
}
```
```bash
POST /donasi
{
# "nominal": 50000,
# "from_id": 1
- **still under development by Iman**
}
```
### Viewing All Program by Customer log in

```bash
# GET /all_programs
- **still under development by Iman**
```

### Viewing All Donatur and Donasi

```bash
# GET /donations
- **still under development by Iman**
```

<!-- This update includes the addition of donation management and minor fixes to syntax and provided information. Ensure to update the `.env` and `requirements.txt` files according to the latest needs of your project. -->
