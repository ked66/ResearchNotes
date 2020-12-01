from forms import ProjectForm, BookForm, PeriodicalForm, SubtopicForm, NoteForm, \
    RegistrationForm, SignInForm
from models import *
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from sqlalchemy import func
from citation_programs import mla_book, mla_journal_citation
from helper_functions import get_form_people, sort_new_people, set_people_defaults, update_people

# Define user_loader
@login_manager.user_loader
def load_user(user_id):
  return Users.query.get(int(user_id))

# Display registration form
@app.route("/new_user", methods = ["GET", "POST"])
def new_user():
    form=RegistrationForm()

    if request.method == "POST":
        user = Users(name = form.name.data,
                     email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('projects', user_id = user.id))

    return render_template('user_registration.html', form=form)

# Display Sign In form
@app.route("/sign_in", methods = ["GET", "POST"])
def sign_in():
    form = SignInForm()

    if request.method == "POST":
        user = Users.query.filter_by(email=form.email.data).first()

        if user and user.check_password(form.password.data):
            login_user(user, remember = True)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('projects', user_id = user.id))

        else:
            flash("Oops! Email or password incorrect!")
            return redirect(url_for("sign_in"))

    return render_template("sign_in.html", form=form)

# Logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Okay, logged out!")
    return redirect(url_for('welcome'))

# Display list of current projects, add projects
@app.route("/<user_id>/projects", methods=["GET", "POST"])
@login_required
def projects(user_id):
    # form to add projects
    if current_user.get_id() == user_id:
        form=ProjectForm()
        if request.method=='POST' and form.validate():
            new_project=Projects(name=form.name.data,
                             summary=form.summary.data,
                             user_id = user_id)
            db.session.add(new_project)
            db.session.commit()

        # query all current projects
        current_projects = Projects.query.filter(Projects.user_id == user_id).all()

        return render_template('projects_list.html',
                               current_projects=current_projects,
                               form=form,
                               user=load_user(user_id))

    else:
        flash("Oops! You aren't authorized to view that page!")
        return redirect(url_for("welcome"))

# Display summary of given project
@app.route('/<user_id>/project/<project_id>', methods = ["GET", "POST"])
@login_required
def project(user_id, project_id):
    if current_user.get_id() == user_id:
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
    else:
        flash("Oops! You aren't authorized to view that page!")
        return redirect(url_for("welcome"))

# Add source type book
@app.route('/project/add_source/book', methods=["GET", "POST"])
@login_required
def add_book():
    form = BookForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).\
        filter(Projects.user_id == current_user.get_id()).all()

    if request.method == 'POST':
        new_source = Sources(description = form.description.data,
                             source_type = 'book',
                             user_id = current_user.get_id())
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

        return redirect(url_for('project', project_id = form.project.data, user_id = current_user.get_id()))

    return render_template('add_book.html', form = form, action = "add")

# Add source type periodical
@app.route('/project/add_source/periodical', methods=["GET", "POST"])
@login_required
def add_periodical():
    form = PeriodicalForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).\
        filter(Projects.user_id == current_user.get_id()).all()
    if request.method == "POST":
        new_source = Sources(description=form.description.data,
                             source_type='periodical',
                             user_id = current_user.get_id())
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

        return redirect(url_for('project', project_id = form.project.data, user_id = current_user.get_id()))

    return render_template('add_periodical.html', form = form)

# View Source and Add Notes
@app.route('/source/<source_id>', methods = ["GET", "POST"])
def source(source_id):
    # Query basic source info
    source = Sources.query.get(source_id)

    if int(current_user.get_id()) == source.user_id:
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
    else:
        flash("Oops! You aren't authorized to view that page.")
        return redirect(url_for('projects', user_id = current_user.get_id()))

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
        authors, editors, translators = update_people(form, people, people_id, source_id)

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

# edit periodical source information
@app.route('/edit_source/periodical/<source_id>', methods = ["GET", "POST"])
def edit_source_periodical(source_id):
    periodical = Periodicals.query.get(source_id)
    source = Sources.query.get(source_id)
    project = db.session.query(Source_Project.project_id).filter(Source_Project.source_id == source_id).scalar()

    # initialize form
    form = PeriodicalForm()
    form.project.choices = db.session.query(Projects.id, Projects.name).all()

    # default form to existing information
    form.project.default = project
    form.title.default = periodical.title
    form.journal.default = periodical.journal
    form.volume.default = periodical.volume
    form.issue.default = periodical.issue
    form.month.default = periodical.month
    form.year.default = periodical.year
    form.description.default = source.description

    # change submit button label
    form.submit.label.text = "Save Changes"

    # get lists of people, people_ids & set people defaults
    people, people_id = set_people_defaults(form, source_id)

    # save defaults
    form.process()

    if request.method == "POST":
        # Initialize form with new inputs
        form = PeriodicalForm()

        # Update Book instance
        db.session.query(Periodicals).filter(Periodicals.source_id == source_id).update(
            {Periodicals.title: form.title.data,
             Periodicals.journal: form.journal.data,
             Periodicals.volume: form.volume.data,
             Periodicals.issue: form.issue.data,
             Periodicals.month: form.month.data,
             Periodicals.year: form.year.data})
        db.session.commit()

        # Update People instances
        authors, editors, translators = update_people(form, people, people_id, source_id)

        # Generate citation & update Source instance
        citation = mla_journal_citation(authors=authors,
                                        title=form.title.data,
                                        journal=form.journal.data,
                                        volume=form.volume.data,
                                        issue=form.issue.data,
                                        month=form.month.data,
                                        year=form.year.data)

        db.session.query(Sources).filter(Sources.id == source_id).update({Sources.citation: citation})

        db.session.commit()

        return redirect(url_for('project', project_id=project))

    return render_template('add_periodical.html', form=form)