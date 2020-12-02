# ResearchNotes
Flask Web App to organize research notes by project, source, and subject. Based on the "note card system" of research organization (see the
[Gallaudet University English Center's](https://www.gallaudet.edu/tutorial-and-instructional-programs/english-center/the-process-and-type-of-writing/pre-writing-writing-and-revising/the-note-card-system) explanation), but paperless!

## Demo
Very rough demo available [here](https://research-note-organizer.herokuapp.com/)!

Hosted by herokuapp

## Site
### Homepage
Sign in with username and password

*under construction*

### Projects List
List of current projects, option to add more

### Project Homepage
Lists of project sources and subtopics

### Add/Edit Sources
Web form to add and/or edit source citation information -- MLA 8 citation is automatically generated

Currently supports (print) Book and Periodical source types

### Source Homepage
Displays citation information and notes associated with source

### Subtopic Homepage
Displays notes associated with subtopic, sorted by source

### Note Search
Allows user to search & sort notes

*under construction*

## To-Do:
- Add user sign-in
- Add note search functionality
- Expand supported source types
- Add CSS formatting

## Built Using
- [Flask](https://flask.palletsprojects.com/en/1.1.x/#): web framework that wraps [Werkzeug](https://werkzeug.palletsprojects.com/), a unicode web application library, and [Jinja](http://jinja.pocoo.org/docs), a web templating language for python
- [WTForms](https://wtforms.readthedocs.io/en/2.3.x/): web library to support form validation and rendering
- [SQLAlchemy](https://docs.sqlalchemy.org/en/13/): ORM to connect python and SQL databases (SQLite in early development, PostgreSQL in app)

## Creator
[Katie Dillon](https://github.com/ked66)