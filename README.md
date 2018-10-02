# Fast-Food-Fast-persistent [![Build Status](https://travis-ci.org/katunold/Fast-Food-Fast-persistent.svg?branch=feature7-post-order)](https://travis-ci.org/katunold/Fast-Food-Fast-persistent) [![Coverage Status](https://coveralls.io/repos/github/katunold/Fast-Food-Fast-persistent/badge.svg?branch=feature7-post-order)](https://coveralls.io/github/katunold/Fast-Food-Fast-persistent?branch=feature7-post-order) [![Maintainability](https://api.codeclimate.com/v1/badges/d545bdbca13a9bd80124/maintainability)](https://codeclimate.com/github/katunold/Fast-Food-Fast-persistent/maintainability)
## About
Fast-Food-Fast is a food delivery service app for a restaurant.
This project is part of the [Andela Fellowship](https://andela.com/) Bootcamp 12 Challenge.
## Motivation
This is driven by the need to improve service delivery, using technology has proven to be more effective in time saving.
This project is mean't to help users to easily make orders of food online and Admins to manage the system.
### Useful Links
| gh-Pages | Heroku | Pivotal Tracker |
|----------|--------|-----------------|
|[gh-pages Link](https://katunold.github.io/Fast-food-Fast/)|`Not available currently`|[Pivotaltracker Link](https://www.pivotaltracker.com/n/projects/2200063)                 |

***Features***
 * User can register with the system
 * User can login to his account
 * User(Admin) can fetch all orders.
 * User(Admin) can fetch a specific order.
 * User can post an order. 
 * User(Admin) can update an order status.
 * User can fetch all menu items.
 * User(Admin) can add a menu item
 * User can view his/her order history
 * User can logout
 
## Getting Started
These instructions will get you a copy of the project up and running on your local machine for development
and testing purposes.
### Prerequisites
What you need to install the software and get started.
```bash
- git : to update and clone the repository
- python3.6: The base language used to develop the api
- pip: a python package used to install project requirements
- postgesSQL: is an object-relational database management system `ORDBMS` with an emphasis on extensibility and standards compliance.
- pgAdmin4: is a tool for creating databases in postgres

```
### Installation
```bash
Type: "https://github.com/katunold/Fast-Food-Fast-persistent" in terminal
```
The api folder contains the system backend services.
- To install the requirements, run:
- [Python](https://www.python.org/) A general purpose programming language
- [Pip](https://pypi.org/project/pip/) A tool for installing python packages
- [Virtualenv](https://virtualenv.pypa.io/en/stable/)  A tool to create isolated Python environments
#### Development setup
- Create a virtual environment and activate it
    ```bash
     virtualenv venv
     source /venv/bin/activate
    ```
- Install dependencies 
    ```bash
    pip3 install -r requirements.txt
    ```
- Install postgres
    ```bash
    sudo apt-get install postgresql postgresql-contrib
    ```
- Create database
    ```bash
    cd Fast-food-Fast-Persistent
    psql -U postgres -f Fast-food.sql
    ```
- Run the application
    ```bash
    cd Fast-food-Fast-Persistent
    python run.py
    ```
- Now you can access the system api Endpoints:

| End Point                                           | Verb |Use                                       |
| ----------------------------------------------------|------|------------------------------------------|
|`/api/v1/auth/signup/`                               |POST  |Registers new user with the system |
|`/api/v1/auth/login/`                                |POST  |Logs in the user to the system |
|`/api/v1/menu`                                       |POST  |Admin can add a menu item |
|`/api/v1/menu`                                       |GET   |User can get all menu items |
|`/api/v1/orders/`                                    |GET   |Admin gets a list of all orders |
|`/api/v1/orders/<int:order_id>/`                     |GET   |Admin gets a specific order  |
|`/api/v1/users/orders`                               |GET   |User can view his/her order history |
|`/api/v1/orders/`                                    |POST  |Posting an order |
|`/api/v1/orders/<int:order_id>/`                     |PUT   |Updates the status of an order |
|`/api/v1/auth/logout`                                |POST  |User can logout|

## Running the tests

- To run the tests, run the following commands

```bash
pytest --cov=api
```

## Built With

* [Flask](http://flask.pocoo.org/docs/1.0/) - The web framework used
* [Python](https://www.python.org/) - Framework language
* HTML
* CSS

## Authors

* **Katumba Arnold** - *Initial work* - [katunold](https://github.com/katunold)

## Acknowledgments

* Andela Software Development Community
