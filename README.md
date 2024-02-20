# noteslink-api

Efficient note-taking API for seamless management of thoughts and tasks

![Python version](https://img.shields.io/badge/Python-3.10.8-4c566a?logo=python&&longCache=true&logoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django version](https://img.shields.io/badge/Django-4.2.8-4c566a?logo=django&&longCache=truelogoColor=white&colorB=pink&style=flat-square&colorA=4c566a) ![Django-RestFramework version](https://img.shields.io/badge/Django_Rest_Framework-3.14.0-red.svg?longCache=true&style=flat-square&logo=django&logoColor=white&colorA=4c566a&colorB=pink)  ![Last Commit](https://img.shields.io/github/last-commit/bhaveshdev09/noteslink/master?&&longCache=true&logoColor=white&colorB=green&style=flat-square&colorA=4c566a) [![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://opensource.org/licenses/MIT)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

## Features

* User authentication: Users can register, log in, and log out.
* CRUD operations: Users can create, read and update their notes.
* Share notes: Users can share notes with other users.
* Version history: Users can view the version history of notes and track changes made over time.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/bhaveshdev09/noteslink.git
   ```
2. Install Poetry (if not already installed):

   ```bash
   curl -sSL https://install.python-poetry.org | python -
   ```
3. Install dependencies using Poetry:

   ```bash
   poetry install
   ```
4. Apply database migrations:

   ```bash
   poetry run python manage.py migrate
   ```
5. Run the development server:

   ```bash
   poetry run python manage.py runserver
   ```
6. Set the environment variables

   > Please refer **.env.example** for must have variables
   >
7. Access the application at http://localhost:8000.

> Note: By default, this project uses **SQLite3** as the database. If you wish to use a different database, please follow the database settings in the [Django documentation](https://docs.djangoproject.com/en/4.2/ref/settings/).


## API Endpoints

Below is a summary of the available API endpoints:

**User Authentication & SignUp**

| Endpoint    | Method | Description             |
| :---------- | ------ | ----------------------- |
| `/login`  | POST   | signin into an account. |
| `/signup` | POST   | signup a new user.     |

**Operations on Notes**

| Endpoint                        | Method      | Description                                |
| ------------------------------- | ----------- | ------------------------------------------ |
| `/notes/create`               | POST        | Create a note.                             |
| `/notes/{id}`                 | GET         | View a particular note.                    |
| `/notes/{id}`                 | PUT / PATCH | Update a particular note.                 |
| `/notes/share`                | POST        | Share a particular note to other users. |
| `/notes/version-history/{id}` | GET         | GET all the changes associated with note.  |

**Additional Docs**

| Endpoint           | Method | Description                                                   |
| ------------------ | ------ | ------------------------------------------------------------- |
| `/schema/doc/`   | GET    | List all the apis in Open API3 documentation format.          |
| `/schema/redoc/` | GET    | List all the apis in Open API3 detailed documentation format. |

## Testing

Run the tests using the following command:

```bash
python manage.py test
```

To check coverage report of the entire codebases try this command:

```bash
coverage run manage.py test

# to get the coverage report on command line
coverage report -m

# To get the html report of code coverage try this
coverage html
```

## Contributing

Inputs and contributions to this project are appreciated. To make them as transparent and easy as possible, please follow this steps:

- ### How to contribute:


  1. Fork the repository and create your branch from master with different name.
  2. Clone the project to your own machine
  3. Commit changes to your own branch
  4. Push your work back up to your fork
  5. Submit a Pull request

  ### Don't:

  - Don't include any license information when submitting your code as this repository is MIT licensed, and so your submissions are understood to be under the same MIT License as well.
- ### How to report a bug:


  1. Open a new Issue.
  2. Write a bug report with details, background, and when possible sample code. That's it!

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).
