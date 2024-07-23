# AfriExplore

![AfriExplore Logo](website/templates/images/logo.png "AfriExplore Logo")

AfriExplore is a web application built with Flask for sharing and exploring adventures in Africa.

## Introduction

AfriExplore is designed to connect adventurers and explorers with the beauty and diversity of Africa. Users can post their adventures, explore others' experiences, and interact through comments and likes.

- **Deployed Site:** [AfriExplore](#) <!-- Add your deployed site link here -->
- **Project Blog Article:** [Final Project Blog](#) <!-- Add your blog article link here -->
- **Author's LinkedIn:** [NSANZIMANA RUGWIRO Dominique Parfait](https://www.linkedin.com/in/nsanzimana-rugwiro-dominique-parfait/)

## Features

- **User Authentication:** Users can sign up, log in, and log out securely.
- **Adventure Posting:** Users can post their adventures, including photos and descriptions.
- **Explore Adventures:** Browse through adventures posted by other users.
- **Responsive Design:** The application is designed to work seamlessly on desktop and mobile devices.

## Technologies Used

- **Flask:** Python web framework used for backend development.
- **SQLAlchemy:** Object-relational mapping (ORM) library for database management.
- **Bootstrap:** Frontend framework for responsive design and UI components.
- **HTML/CSS:** Frontend markup and styling.
- **JavaScript:** Client-side scripting for enhanced interactivity.

## Setup

To run AfriExplore locally, follow these steps:

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/Rugwiroparfait/Afri-explore-web-app>
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

## Usage

1. **Sign Up:** Create an account to start sharing your adventures.
2. **Log In:** Access your account and explore other users' posts.
3. **Create Posts:** Share your adventures by creating new posts with descriptions and photos.
4. **Interact:** Comment on and like other users' posts.

## Contributing

Contributions are welcome! If you have any suggestions, bug reports, or improvements, please open an issue or a pull request on GitHub.

## Related Projects

- [Flask](https://flask.palletsprojects.com/)
- [SQLAlchemy](https://docs.sqlalchemy.org/)
- [Bootstrap](https://getbootstrap.com/)

## Licensing

This Project is owned by ALX Africe
## Authors

- **NSANZIMANA RUGWIRO Dominique Parfait**

## Acknowledgements

- [Flask Documentation](https://flask.palletsprojects.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Bootstrap Documentation](https://getbootstrap.com/)
