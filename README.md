# AfriExplore
![AfriExplore Logo](website/templates/images/logo.png "AfriExplore Logo")


AfriExplore is a web application built with Flask for sharing and exploring adventures in Africa.

## Features

- **User Authentication**: Users can sign up, log in, and log out securely.
- **Adventure Posting**: Users can post their adventures, including photos and descriptions.
- **Explore Adventures**: Browse through adventures posted by other users.
- **Responsive Design**: The application is designed to work seamlessly on desktop and mobile devices.

## Technologies Used

- **Flask**: Python web framework used for backend development.
- **SQLAlchemy**: Object-relational mapping (ORM) library for database management.
- **Bootstrap**: Frontend framework for responsive design and UI components.
- **HTML/CSS**: Frontend markup and styling.
- **JavaScript**: Client-side scripting for enhanced interactivity.

## Setup

To run AfriExplore locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <repository_url>
   cd AfriExplore
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up the database:**

   - Modify `config.py` to specify your database configuration (e.g., PostgreSQL, MySQL).
   - Initialize the database:

     ```bash
     flask db init
     flask db migrate
     flask db upgrade
     ```

4. **Run the application:**

   ```bash
   flask run
   ```

   The application will be available at `http://localhost:5000`.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or improvements, please open an issue or a pull request on GitHub.

##  Authors

-NSANZIMANA RUGWIRO Dominique Parfait

## Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)
```

Feel free to customize this template further based on additional features, specific setup instructions, or any other information relevant to your project.