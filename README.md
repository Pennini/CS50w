# People Management System

The People Management System is a web-based application designed to facilitate efficient management of personnel, events, projects, meetings, and availability within an organization. Developed using the Django framework, this system provides a comprehensive solution for organizing and overseeing various aspects of people management in a professional setting.

## Distinctiveness and Complexity
    
Unlike other projects such as network, Wikipedia clone, and e-commerce clones that cater to specific functionalities, this system provides a comprehensive solution for organizing and overseeing various aspects of people management in a professional setting.

### Key Distinctive Features:

#### Custom User Model:

* The project incorporates a customized user model derived from Django's `AbstractUser`. This allows for the inclusion of additional attributes such as `position, group, area, and biography` to better represent the roles and profiles of users within the system.

#### Flexible Organization Structure:

* The system accommodates dynamic organizational structures with models like `Group` and `Area`, allowing users to be associated with specific groups and areas. This provides flexibility for organizations with diverse departments and teams.

#### Event and Project Management:

* Events and projects are crucial components of organizational activities. The system provides dedicated models (`Event` and `Project`) with features such as start and end dates, descriptions, and responsible users. This supports efficient planning and tracking of events and projects.

#### Meeting and Availability Tracking:

* The inclusion of a `Meeting` model facilitates the recording of meetings associated with groups or areas. Additionally, the `Availability` model helps in tracking user availability on specific days and times, enhancing coordination and scheduling within the organization.

#### Distinct Categories:

* Events and projects can be categorized, adding an extra layer of organization and making it easier to filter and search for specific types of activities. This feature supports a more granular approach to managing different types of events and projects.


## File Contents

* **models:**

    * Defines the data models for the application, including Group, Area, Position, User, Event, Project, Meeting, and Availability.

* **views:**

    * Contains the view functions that handle HTTP requests and define the application's behavior, including functionalities such as user authentication, project creation, event management, availability tracking, and more.

* **urls:**

    * Specifies the URL patterns for the application, mapping them to the corresponding views.

* **admin:**

    * customizes the Django admin interface for efficient management of People Management System data. It streamlines many-to-many relationships, optimizing member associations in Project, Event, and Meeting models.

* **templatetags**
    |_ **custom_tags**:
    
    * introduces custom Django template filters and a simple tag. These succinct additions empower concise dictionary operations, facilitate conditional rendering, and streamline many-to-many relationship access within templates.

* **templates**
    |_**system**:
    * **layout.html:**  serves as the foundational layout for the project, providing a consistent structure across various pages.
    * **index.html:** renders the main dashboard, displaying projects and events
    * **meeting.html:** responsible for rendering the meeting page, handling permissions based on the user's position.
    * **search.html:** displays search results for projects, events, and users
    * **profile.html:** presents the user's profile with a score calculated from their involvement in projects, events, and meetings
    * **display.html:** shows detailed information and allows updating descriptions for projects and events
    * **availability.html:** manages user availability settings
    * **calendar.html:** visualizes a calendar with scheduled projects, events, areas, and groups for the given month

## How to Run the Application

#### Clone the repository to your local machine.

```
git clone https://github.com/me50/Pennini/tree/web50/projects/2020/x/capstone
```

#### Navigate to the project directory.

```
cd system
```

#### Install the required dependencies.

```
pip install -r requirements.txt
```

#### Apply database migrations.

```
python manage.py makemigrations sistema
python manage.py migrate
```

#### Run the development server.

```
python manage.py runserver
```

Open a web browser and visit http://localhost:8000 to access the application.

## Additional Information

The project is built using Django, a high-level Python web framework, providing a robust and scalable foundation for web development.

Ensure that you have Python and Django installed on your system before running the application.

For administrative purposes, superuser credentials can be created using the following command:

```python manage.py createsuperuser
```

The application emphasizes user-friendly interfaces, ensuring that individuals at all levels within the organization can navigate and utilize its features effectively.

Contributions and feedback are welcome. Feel free to submit issues or pull requests on the project's GitHub repository.