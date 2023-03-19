# Podcast API

This podcast app aims to provide a centralized and user-friendly platform for managing, discovering, and organizing podcast content. It addresses the needs of podcast creators and listeners, making it easier for them to share, discover, and enjoy podcast content in a more organized and efficient way.


<br>


## Installation Guide

<br>

### Prerequisites ###

<br>

Python 3.6 or higher

pip

virtualenv (optional but recommended)

<br>

### Steps

<br>

1. Clone the repository:

git clone https://github.com/Daniel-Piciocchi/podcast_api

<br>

2. Change to the project directory:

cd podcast_api

<br>

3. Create a virtual environment (optional but recommended):

python -m venv venv

<br>

4. Activate the virtual environment:

On macOS and Linux:

source venv/bin/activate


<br>

On Windows:

.\venv\Scripts\activate

<br>

5. Install the required packages:

pip install -r requirements.txt

<br>


6. Set the FLASK_APP environment variable:

On macOS and Linux:

export FLASK_APP=app

<br>

On Windows:

set FLASK_APP=app

<br>

7. Initialize the database and migrations:

flask db init

<br>

8. Generate the initial migration:

flask db migrate -m "Initial migration"

<br>

9. Apply the migration to create the database tables:

flask db upgrade

<br>

10. Run the application:

The app should now be running on http://127.0.0.1:5000

<br>

## Requirements

<br>

### 1. Identification of the problem you are trying to solve by building this particular app.

<br>

The podcast app is designed to address the challenges of managing and organizing podcast-related content through a centralized and user-friendly platform. It solves the issues of discoverability by providing search and browse functionalities based on criteria such as genre, podcast, and episodes. The app also aims to improve accessibility by simplifying the interface to search, browse, and consume podcasts and their episodes. Users can categorize and track their podcasts while rating them, promoting high-quality content discovery and community building. Additionally, the app offers administrative capabilities for efficient and streamlined content management.

<br>

### 2. Why is it a problem that needs solving?

<br>

A podcast API can provide users with a comprehensive platform that not only lists podcasts, but also provides access to detailed information about each podcast, including its title, description, author, genre, and more. Additionally, it can provide a rating and review system that enables users to rate and provide feedback on podcasts they have listened to, which can assist other listeners in determining which podcast to listen to next.

Moreover, a podcast API can help podcast creators by providing them with tools to promote their content, manage their podcasts, and track their analytics. It can also offer user management features that allow podcast creators to manage their subscribers and listener data.

<br>

### 3. Why have you chosen this database system. What are the drawbacks compared to others?

<br>

I chose Flask-SQLAlchemy for building web applications with Flask due to its seamless integration with the framework and powerful query API. SQLAlchemy provides a high-level, Pythonic interface for interacting with databases, allowing developers to focus on application logic instead of writing raw SQL queries. Furthermore, it supports multiple database management systems, making it flexible and scalable. 

However, there are some potential drawbacks to using SQLAlchemy. It can have a steeper learning curve compared to simpler ORMs, and its abstraction and feature richness may introduce performance overhead compared to using raw SQL queries or more lightweight ORMs. Additionally, the flexibility and features provided by SQLAlchemy may introduce unnecessary complexity for small-scale projects or applications with simple database requirements.

<br>

### 4. Identify and discuss the key functionalities and benefits of an ORM.

<br>

By offering a high-level, object-oriented interface, an object relational mapper (ORM) is a programming tool that makes it easier to communicate with databases. The underlying SQL queries and database management responsibilities are abstracted, allowing developers to manipulate database entries as if they were Python objects. Instead of writing raw SQL queries, this abstraction layer enables developers to deal with databases using the well-known ideas of classes and objects from object-oriented programming.

Portability is one of the main advantages of utilising an ORM. Developers can switch between many databases with little to no code change thanks to ORMs, which typically support multiple database management systems. This facilitates the migration of an application to a new database system or between several settings.

Code maintainability is an additional advantage. Developers may write clear, understandable, and maintainable code by utilising an ORM that concentrates on application logic rather than database-specific concerns. There is less boilerplate code for developers to create because the ORM handles the underlying SQL queries.

Moreover, ORMs contribute to increased security by thwarting SQL injection threats by automatically escaping user inputs and managing SQL queries in the background. This lessens the chance of introducing security flaws into the application.

Furthermore, ORMs can boost productivity by streamlining database operations and giving users access to tools for controlling database schema migrations. Rather than wasting time on database operations, this enables developers to concentrate on building application features.

Finally, ORMs make it simple to construct one-to-many, many-to-one, and many-to-many relationships as well as deal with related records. 

<br>

### 5. Doucment all endpoints for your API.

<br>

#### User Routes:

1. Register a new user
• Method: POST
• Route: /api/users/register
• Description: Registers a new user with the provided username, email, and password.

2. Log in an existing user
• Method: POST
• Route: /api/users/login
• Description: Logs in an existing user with the provided username and password, returning an access token.

3. Get all users
• Method: GET
• Route: /api/users
• Description: Retrieves a list of all registered users. Requires admin privileges.

4. Get a specific user
• Method: GET
• Route: /api/users/int:user_id
• Description: Retrieves the details of a specific user by their user ID. Requires admin privileges.

5. Get the current user's profile
• Method: GET
• Route: /api/users/profile
• Description: Retrieves the profile information of the currently authenticated user.

6. Update the current user's profile
• Method: PUT
• Route: /api/users/profile
• Description: Updates the profile information of the currently authenticated user.

7. Delete the current user
• Method: DELETE
• Route: /api/users/delete
• Description: Deletes the currently authenticated user's account.

#### Podcast Routes:

1.  Create a new podcast
• Method: POST
• Route: /api/podcasts
• Description: Creates a new podcast with the provided title, description, and genre_id.

2. Get all podcasts
• Method: GET
• Route: /api/podcasts
• Description: Retrieves a list of all podcasts.

3. Get a specific podcast
• Method: GET
• Route: /api/podcasts/int:podcast_id
• Description: Retrieves the details of a specific podcast by its podcast ID.

4. Update a podcast
• Method: PUT
• Route: /api/podcasts/int:podcast_id
• Description: Updates the title, description, and genre_id of a specific podcast by its podcast ID.

5. Delete a podcast
• Method: DELETE
• Route: /api/podcasts/int:podcast_id
• Description: Deletes a specific podcast by its podcast ID.

#### Episode Routes:

1. Create a new episode
• Method: POST
• Route: /api/episodes
• Description: Creates a new episode with the provided title, podcast_id, and description.

2. Get all episodes
• Method: GET
• Route: /api/episodes
• Description: Retrieves a list of all episodes.

3. Get a specific episode
• Method: GET
• Route: /api/episodes/int:episode_id
• Description: Retrieves the details of a specific episode by its episode ID.

4. Update an episode
• Method: PUT
• Route: /api/episodes/int:episode_id
• Description: Updates the title, podcast_id, and description of a specific episode by its episode ID.

5. Delete an episode
• Method: DELETE
• Route: /api/episodes/int:episode_id
• Description: Deletes a specific episode by its episode ID.

#### Rating Routes
1. Create a new rating
• Method: POST
• Route: /api/ratings
• Description: Creates a new rating with the provided user_id, episode_id, and score.

2. Get all ratings
• Method: GET
• Route: /api/ratings
• Description: Retrieves a list of all ratings.
3. Get all ratings for an episode
• Method: GET
• Route: /api/episodes/int:episode_id/ratings
• Description: Retrieves a list of all ratings for a specific episode by its episode ID.

4. Update a rating
• Method: PUT
• Route: /api/ratings/int:rating_id
• Description: Updates the score of a specific rating by its rating ID.
5. Delete a rating
• Method: DELETE
• Route: /api/ratings/int:rating_id
• Description: Deletes a specific rating by its rating ID.

#### Search Routes

1. Search for podcasts and episodes
• Method: GET
• Route: /api/search?keyword=<search_keyword>
• Description: Searches for podcasts and episodes based on a keyword provided in the query parameter. Returns both podcast and episode results that match the keyword in their title, author (for podcasts), or description (for episodes).

### 6. An ERD for your api:

<img src="/Users/Dan/podcast_api/docs/API diagram.jpeg" alt="ERD">

#### 7. Detail any third party services that your app will use.

1. Flask: A web framework for Python that provides tools, libraries, and extensions for building web applications, extensively used throughout the routes, models, controllers,configs and tests.

2. Flask-SQLAlchemy: A Flask extension that simplifies the integration of SQLAlchemy ORM with a Flask application. It's used in the controller, config, and models files.

3. Flask-Marshmallow: An object serialization/deserialization library that provides integration with the Flask web framework and SQLAlchemy. It is used in the __init__.py file.

4. Flask-JWT-Extended: A Flask extension for handling JSON Web Tokens (JWT). It's used for authentication and authorization purposes in the route, controller, and util files where endpoints require authentication or admin privileges.

5. Flask-Migrate: A Flask extension for handling Alembic database migrations. It's useful for managing database schema changes over time. It is used in the _init__.py file.

6. Werkzeug: A utility library that comes with Flask and provides various utilities, including password hashing and checking. It's used in the controller, model, and hash_password.py files.

7. Secrets: A Python built-in module used to generate secure random numbers. It's used to generate secure tokens for authentication purposes in the __init__.py file.

8. datetime: A Python built-in module used for handling date and time objects. It's used to set token expiration times. It is used in the _init_.py file and the model files.

9. functools: A Python built-in module that provides higher-order functions and operations on callable objects. It's used to create a custom decorator, admin_required, which is applied to routes that require admin access. It can be found in the utils.py file.

10. JSON: A Python built-in module for working with JSON data. It provides methods for encoding and decoding JSON data. it is used in the test_podcast_api.py file, to parse JSON responses from your API calls, and in the controllers and _init_.py file.

11. Unittest: A built-in Python library for creating and running test cases. It provides a framework to define test cases, test suites, and test runners. It is being used to in the test_podcast_api file.

#### 8. Describe your projects models in terms of the relationships they have with each other.

1.	User:
- One-to-many relationship with Podcast: A user can create multiple podcasts, but each podcast can be created by only one user (author). This relationship is established using the author field in the Podcast model and the podcasts backref in the User model.
- One-to-many relationship with Rating: A user can rate multiple podcasts, but each rating is associated with only one user. This relationship is established using the user field in the Rating model and the ratings backref in the User model.

2.	Podcast:
- Many-to-one relationship with User: A podcast is created by one user (author), but a user can create multiple podcasts. This relationship is established using the author_id foreign key and the author field in the Podcast model.
- One-to-many relationship with Episode: A podcast can have multiple episodes, but each episode belongs to only one podcast. This relationship is established using the podcast field in the Episode model and the episodes backref in the Podcast model.
- Many-to-one relationship with Genre: A podcast belongs to one genre, but a genre can have multiple podcasts. This relationship is established using the genre_id foreign key and the genre field in the Podcast model.
- One-to-many relationship with Rating: A podcast can have multiple ratings, but each rating is associated with only one podcast. This relationship is established using the podcast field in the Rating model and the ratings backref in the Podcast model.

3. Episode:
- Many-to-one relationship with Podcast: An episode belongs to one podcast, but a podcast can have multiple episodes. This relationship is established using the podcast_id foreign key and the podcast field in the Episode model.

4. Rating:
- Many-to-one relationship with User: A rating is associated with one user, but a user can rate multiple podcasts. This relationship is established using the user_id foreign key and the user field in the Rating model.
- Many-to-one relationship with Podcast: A rating is associated with one podcast, but a podcast can have multiple ratings. This relationship is established using the podcast_id foreign key and the podcast field in the Rating model.

5. Genre:
- One-to-many relationship with Podcast: A genre can have multiple podcasts, but each podcast belongs to only one genre. This relationship is established using the genre field in the Podcast model and the podcasts backref in the Genre model.

#### 9. Discuss the database relations to be implemented in your application.

1. One-to-Many relationship between User and Podcast:
- A User can create multiple Podcasts, but each Podcast has only one author (User).
- This is represented by the author_id foreign key in the Podcast model and the backref='podcasts' in the User model.

2. One-to-Many relationship between Genre and Podcast:
- A Genre can be associated with multiple Podcasts, but each Podcast belongs to only one Genre.
- This is represented by the genre_id foreign key in the Podcast model and the backref='podcasts' in the Genre model.

3. One-to-Many relationship between Podcast and Episode:
- A Podcast can have multiple Episodes, but each Episode belongs to only one Podcast.
- This is represented by the podcast_id foreign key in the Episode model and the backref='episodes' in the Podcast model.

4. Many-to-One relationship between User and Rating:
- A User can give multiple Ratings, but each Rating is given by only one User.
- This is represented by the user_id foreign key in the Rating model and the backref='ratings' in the User model.

5. Many-to-One relationship between Podcast and Rating:
- A Podcast can have multiple Ratings, but each Rating is associated with only one Podcast.
- This is represented by the podcast_id foreign key in the Rating model and the backref='ratings' in the Podcast model.

#### 10. Describe the way tasks are allocated and tracked in your project

Tasks have been allocated through Trello in terms of their priority and necessity. 

1. Initial Setup:





