# ResearchNotes
Flask Web App to organize research notes by project, source, and subject. Based on the "note card system" of research organization (see the
[Gallaudet University English Center's](https://www.gallaudet.edu/tutorial-and-instructional-programs/english-center/the-process-and-type-of-writing/pre-writing-writing-and-revising/the-note-card-system) explanation), but paperless!

## Demo
<b>Demo currently offline for improvements to data structure</b>

Very rough demo available [here](https://research-note-organizer.herokuapp.com/)!

Hosted by herokuapp

## Site
### Homepage
Sign in with username and password

### Projects List
List of current projects, option to add more

![User homepage for "Katie", with linked list of current projects - "History of Cats" and "Models of Deafness", form to add new projects, and simple text search](https://github.com/ked66/ResearchNotes/blob/master/img/projects_list.jpeg)

### Project Homepage
Lists of project sources and subtopics

![Homepage for project "History of Cats", with linked lists of sources and subtopics](https://github.com/ked66/ResearchNotes/blob/master/img/project_homepage.jpeg)

### Add/Edit Sources
Web form to add and/or edit source citation information -- MLA 8 citation is automatically generated

Currently supports (print) Book and Periodical source types

![Form to add book source "Cats in Ancient Egypt"](https://github.com/ked66/ResearchNotes/blob/master/img/add_book.jpeg)

![Form to add periodical source "Cats! Cats! Cats!](https://github.com/ked66/ResearchNotes/blob/master/img/add_periodical.jpeg)

### Source Homepage
Displays citation information and notes associated with source

![Source hompage for "Cats in Ancient Egypt" with bibliographic information and option to edit](https://github.com/ked66/ResearchNotes/blob/master/img/source_homepage.jpeg)
![Bottom of source homepage, with notes"](https://github.com/ked66/ResearchNotes/blob/master/img/subtopic_homepage(2).jpeg)

### Subtopic Homepage
Displays notes associated with subtopic, sorted by source

![Subtopic homepage for "Pest Control" with list of notes](https://github.com/ked66/ResearchNotes/blob/master/img/subtopic_homepage.jpeg)

### Note Search
Allows user to search notes by note text, source title, contributors, source type, year of publication, project, and subtopic

![Advanced search form](https://github.com/ked66/ResearchNotes/blob/master/img/advanced_search.jpeg)

When a project is selected, associated subtopics appear

![Advanced search form with "History of Cats" project selected; subtopic options appear](https://github.com/ked66/ResearchNotes/blob/master/img/advanced_search_subtopic.jpeg)

## To-Do:
- Add user sign-in :white_check_mark:
    - 2 Dec. 2020: All pages besides homepage require login, and users can only edit their own projects/sources/notes, etc. 
- Add note search functionality
    - 7 Dec. 2020: Simple Note search available on "Projects List" page, and Advanced Search available
    - Still to do: improve search by contributer option (currently can only search last name)
- Expand supported source types
    - This will be done by changing bibliographic data structure to BibTex (in progress)
- Add CSS formatting
    - 3 Dec. 2020: Added top Navigation Bar, added font styles "Sniglet" and "Roboto"
    - 9 Dec. 2020: Added extensive styling of notes and topic labels (including option to choose color of label)

## Built Using
- [Flask](https://flask.palletsprojects.com/en/1.1.x/#): web framework that wraps [Werkzeug](https://werkzeug.palletsprojects.com/), a unicode web application library, and [Jinja](http://jinja.pocoo.org/docs), a web templating language for python
- [WTForms](https://wtforms.readthedocs.io/en/2.3.x/): web library to support form validation and rendering
- [SQLAlchemy](https://docs.sqlalchemy.org/en/13/): ORM to connect python and SQL databases (SQLite in early development, PostgreSQL in app)
- [Werkzeug.security](https://werkzeug.palletsprojects.com/en/1.0.x/utils/#module-werkzeug.security): Werkzeug utility functions to easily hash user passwords

## Creator
[Katie Dillon](https://github.com/ked66)
