from forms import ProjectForm, BookForm, PeriodicalForm, SubtopicForm, NoteForm
from models import *
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from sqlalchemy import func
from citation_programs import mla_book, mla_journal_citation
from helper_functions import get_form_people, sort_new_people, set_people_defaults

# Display list of current projects, add projects
@app.route("/projects", methods=["GET", "POST"])
def projects():
    # form to add projects
    form=ProjectForm()
    if request.method=='POST' and form.validate():
        new_project=Projects(name=form.name.data,
                               summary=form.summary.data)
        db.session.add(new_project)
        db.session.commit()

    # query all current projects
    current_projects = Projects.query.all()

    return render_template('projects_list.html',
                           current_projects = current_projects,
                           form = form)

# Display summary of given project
@app.route('/project/<project_id>', methods = ["GET", "POST"])
def project(project_id):
    # query current project from Projects
    current_project = Projects.query.filter_by(id=project_id).first()

    # query current project from Source_Project (to get source ids)
    project_sources = db.session.query(Source_Project.source_id).filter(Source_Project.project_id==project_id).all()
    # format source ids as a list
    project_source_ids = [id[0] for id in project_sources]
    # query source info
    sources = db.session.query(Sources).filter(Sources.id.in_(project_source_ids)).all()

    form = SubtopicForm()
    # form to add subtopic
    if request.method == "POST" and form.validate():
        new_subtopic = Topics(name = form.name.data,
                            project_id = project_id)
        db.session.add(new_subtopic)
        db.session.commit()

    # query subtopics
    subtopics = db.session.query(Topics).filter(Topics.project_id==project_id).all()

    return render_template('project_summary.html',
                           project_name = current_project.name,
                           project_summary = current_project.summary,
                           sources = sources,
                           subtopics = subtopics,
                           form = form)

# Add source type book
@app.route('/project/add_source/book', methods=["GET", "POST"])
def add_book():
    form = BookForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).all()
    if request.method == 'POST':
        new_source = Sources(description = form.description.data,
                             source_type = 'book')
        db.session.add(new_source)
        db.session.commit()

        new_source_id = db.session.query(func.max(Sources.id)).scalar()

        new_book = Books(source_id = new_source_id,
                         title = form.title.data,
                         publisher = form.publisher.data,
                         year = form.year.data,
                         edition = form.edition.data,
                         section = form.section.data,
                         volume = form.volume.data)

        new_source_project = Source_Project(source_id = int(new_source_id),
                                            project_id = form.project.data)

        db.session.add(new_book)
        db.session.add(new_source_project)
        db.session.commit()

        # Add people, get lists of people by contribution type
        authors, editors, translators = sort_new_people(form, new_source_id)

        # Generate citation
        citation = mla_book(authors = authors,
                            title = form.title.data,
                            publisher = form.publisher.data,
                            year = form.year.data,
                            editor= editors,
                            translator= translators,
                            author_type="person",
                            edition= form.edition.data,
                            volume= form.volume.data)

        db.session.query(Sources).filter(Sources.id == new_source_id).update({Sources.citation: citation})
        db.session.commit()

        return redirect(url_for('project', project_id = form.project.data))

    return render_template('add_book.html', form = form, action = "add")

# Add source type periodical
@app.route('/project/add_source/periodical', methods=["GET", "POST"])
def add_periodical():
    form = PeriodicalForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).all()
    if request.method == "POST":
        new_source = Sources(description=form.description.data,
                             source_type='periodical')
        db.session.add(new_source)
        db.session.commit()

        new_source_id = db.session.query(func.max(Sources.id)).scalar()

        new_periodical = Periodicals(source_id = new_source_id,
                                     title = form.title.data,
                                     journal = form.journal.data,
                                     volume = form.volume.data,
                                     issue = form.issue.data,
                                     month = form.month.data,
                                     year = form.year.data)

        new_source_project = Source_Project(source_id=int(new_source_id),
                                            project_id=form.project.data)

        db.session.add(new_periodical)
        db.session.add(new_source_project)
        db.session.commit()

        authors, editors, translators = sort_new_people(form, new_source_id)

        citation = mla_journal_citation(authors = authors,
                                        title = form.title.data,
                                        journal = form.journal.data,
                                        volume = form.volume.data,
                                        issue = form.issue.data,
                                        month = form.month.data,
                                        year = form.year.data)

        db.session.query(Sources).filter(Sources.id == new_source_id).update({Sources.citation: citation})
        db.session.commit()

        return redirect(url_for('project', project_id = form.project.data))

    return render_template('add_periodical.html', form = form)

# View Source and Add Notes
@app.route('/source/<source_id>', methods = ["GET", "POST"])
def source(source_id):
    # Query basic source info
    source = Sources.query.get(source_id)

    # Query citation info
    if source.source_type == "book":
        citation_info = Books.query.get(source_id)
    elif source.source_type == "periodical":
        citation_info = Periodicals.query.get(source_id)

    # Query author info
    authors = db.session.query(People).join(People_Source).filter(People_Source.source_id == source_id).\
        filter(People_Source.type=='author').all()

    # Qury editor info
    editors = db.session.query(People).join(People_Source).filter(People_Source.source_id == source_id).\
        filter(People_Source.type=='editor').all()

    # Query translator info
    translators = db.session.query(People).join(People_Source).filter(People_Source.source_id == source_id).\
        filter(People_Source.type=='translator').all()

    # Form to add Notes
    project_id = db.session.query(Source_Project.project_id).filter(Source_Project.source_id == source.id).scalar()
    form = NoteForm()
    form.topic.choices = [(None, "None")] + db.session.query(Topics.id, Topics.name).\
        filter(Topics.project_id == project_id).all()
    if request.method == "POST":
        new_note = Notes(source_id = source.id,
                         first_page = form.first_page.data,
                         last_page = form.last_page.data,
                         note = form.note.data)
        db.session.add(new_note)
        db.session.commit()

        if form.topic.data:
            for topic in form.topic.data:
                new_note_id = db.session.query(func.max(Notes.id)).scalar()

                new_topic_note = Topics_Notes(note_id = new_note_id,
                                      topic_id = topic)
                db.session.add(new_topic_note)
                db.session.commit()

    # Query Notes - order by first page
    notes = db.session.query(Notes, Notes.id).filter(Notes.source_id == source_id).order_by(Notes.first_page)

    return render_template('source_summary.html',
                           source = source,
                           info = citation_info,
                           authors = authors,
                           editors = editors,
                           translators = translators,
                           notes = notes,
                           form = form)
# View subtopic summary
@app.route('/subtopic/<subtopic_id>')
def subtopic(subtopic_id):
    subtopic = Topics.query.get(subtopic_id)
    note_ids = db.session.query(Topics_Notes.note_id).filter(Topics_Notes.topic_id == subtopic_id).all()
    note_ids = [id[0] for id in note_ids]
    notes = db.session.query(Notes, Notes.source_id, Notes.id).filter(Notes.id.in_(note_ids)).all()
    source_ids = [id[1] for id in notes]
    sources = db.session.query(Sources).filter(Sources.id.in_(source_ids)).all()

    return render_template('subtopic_summary.html',
                           subtopic = subtopic,
                           notes = notes,
                           sources = sources)

# Delete subtopic
@app.route('/delete/subtopic/<id>', methods = ["POST"])
def delete_subtopic(id):
    project_id = db.session.query(Topics.project_id).filter(Topics.id == id).scalar()
    topic = db.session.query(Topics).filter(Topics.id == id).first()
    db.session.delete(topic)
    db.session.commit()

    flash("Subtopic Deleted!")

    return redirect(url_for('project', project_id = project_id))

# Delete note
@app.route('/delete/note/<id>', methods = ["POST"])
def delete_note(id):
    source_id = db.session.query(Notes.source_id).filter(Notes.id == id).scalar()
    note = db.session.query(Notes).filter(Notes.id == id).first()
    db.session.delete(note)
    db.session.commit()

    flash("Note Deleted!")

    return redirect(url_for('source', source_id = source_id))

# Remove Note from Subtopic
@app.route('/delete/subtopic_note/<subtopic_id>/<note_id>', methods = ["POST"])
def delete_subtopic_note(subtopic_id, note_id):
    topic_note = db.session.query(Topics_Notes).filter(Topics_Notes.topic_id == subtopic_id).\
        filter(Topics_Notes.note_id == note_id).first()
    db.session.delete(topic_note)
    db.session.commit()

    flash("Note removed from Subtopic!")

    return redirect(url_for('subtopic', subtopic_id = subtopic_id))

# delete source
@app.route('/delete/source/<source_id>', methods = ["POST"])
def delete_source(source_id):
    project_id = db.session.query(Source_Project.project_id).filter(Source_Project.source_id == source_id).scalar()
    # note to self: must be deleted in 2 lines like this or cascade won't work
    source = db.session.query(Sources).filter(Sources.id == source_id).first()
    db.session.delete(source)
    db.session.commit()

    flash("Source deleted!")

    return redirect(url_for('project', project_id = project_id))

# edit book source information
@app.route('/edit_source/book/<source_id>', methods = ["GET", "POST"])
def edit_source_book(source_id):
    book = Books.query.get(source_id)
    source = Sources.query.get(source_id)
    project = db.session.query(Source_Project.project_id).filter(Source_Project.source_id == source_id).scalar()

    # initialize form
    form = BookForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).all()

    # default form to existing information
    form.project.default = project
    form.title.default = book.title
    form.publisher.default = book.publisher
    form.year.default = book.year
    form.edition.default = book.edition
    form.section.default = book.section
    form.description.default = source.description

    # change submit button label
    form.submit.label.text = "Save Changes"

    # get lists of people, people_ids & set people defaults
    people, people_id = set_people_defaults(form, source_id)

    # save defaults
    form.process()

    if request.method == "POST":
        # Initialize form with new inputs
        form = BookForm()

        # Update Book instance
        db.session.query(Books).filter(Books.source_id == source_id).update(
            {Books.title: form.title.data,
             Books.publisher: form.publisher.data,
             Books.edition: form.edition.data,
             Books.section: form.section.data})
        db.session.commit()

        # Update People instances
        # list of people from form
        new_people = get_form_people(form)
        authors = []
        editors = []
        translators = []

        for person in new_people:
            if person not in people and (person[0] or person[1] or person[2]):
                # if new person didn't already exist, add People instance
                add_person = People(first = person[0] if isinstance(person[0], str) else "",
                                    middle = person[1] if isinstance(person[1], str) else "",
                                    last = person[2] if isinstance(person[2], str) else "")
                db.session.add(add_person)
                db.session.commit()

                if person[3] == 'author': authors.append(add_person.__repr__())
                if person[3] == 'editor': editors.append(add_person.__repr__())
                if person[3] == 'translator': translators.append(add_person.__repr__())

                # and People_Source instance
                add_person_id = db.session.query(func.max(People.id)).scalar()
                add_people_source = People_Source(source_id=source_id,
                                                  people_id=add_person_id,
                                                  type=person[3])

                db.session.add(add_people_source)
                db.session.commit()

        for i in range(len(people)):
            if people[i] in new_people:
                person = str(People.query.filter(People.id == people_id[i]).first())
                if people[i][3] == 'author': authors.append(person)
                if people[i][3] == 'editor': editors.append(person)
                if people[i][3] == 'translator': translators.append(person)
            # if person is no longer in citation, remove from People_Source from db
            else:
                People_Source.query.filter(People_Source.people_id == people_id[i]).\
                    filter(People_Source.source_id == source_id).delete()
                db.session.commit()

        # Generate citation & update Source instance
        citation = mla_book(authors = authors,
                            title = form.title.data,
                            publisher = form.publisher.data,
                            year = form.year.data,
                            editor= editors,
                            translator= translators,
                            author_type="person",
                            edition= form.edition.data,
                            volume= form.volume.data)

        db.session.query(Sources).filter(Sources.id == source_id).update({Sources.citation: citation})

        db.session.commit()
        
        return redirect(url_for('project', project_id = project))
        

    return render_template('add_book.html', form = form)

# TODO: add edit periodical source information
