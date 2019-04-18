# SeniorDesign

http://senior-design.n7wvrh3jp8.us-east-1.elasticbeanstalk.com/

Application.py is the main Flask app that hosts the webapps' endpoints and handles all backend logic.
Models.py has the definition of the records that are used for storing information in the database and serializing records.
requirements.txt lists the python requirements of the project

templates/ This folder holds the Jinja2 templates that are used to generate the html of the frontend.
base.j2 is a wrapper template that brings in libraries static reources to be used
index.j2 defines the actual layout that is displayed to the user when they load the page

static/ This folder holds static resources for use by the front end
package.json describes the npm libraries that the project uses
main.css holds the styling information the frontend uses
main.js holds the javascript code that polls for data from the backend and updates the display
static/images holds some pictures that are or were previously used in the frontend

