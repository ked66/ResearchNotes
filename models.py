from app import app, db

## table of projects
class Projects(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120), index = True, unique = False)
    summary = db.Column(db.String(500))
    sources = db.relationship('Source_Project')
    topics = db.relationship('Topics')
    sqlite_autoincrement = True

## tables relating to source information
## source id & description
class Sources(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    description = db.Column(db.String)
    source_type = db.Column(db.String)
    citation = db.Column(db.String)
    project = db.relationship('Source_Project')
    book = db.relationship('Books', cascade='all,delete-orphan')
    periodical = db.relationship('Periodicals', cascade='all,delete-orphan')
    people_source = db.relationship('People_Source', cascade='all,delete-orphan')
    source_project = db.relationship("Source_Project", cascade='all,delete-orphan')
    note = db.relationship('Notes', cascade='all,delete-orphan')
    sqlite_autoincrement = True

## source-project association
class Source_Project(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'),
                          primary_key = True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'),
                           primary_key = True)

## citation information
class Books(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'),
                          primary_key = True)
    title = db.Column(db.String(100))
    publisher = db.Column(db.String(100))
    year = db.Column(db.Integer)
    edition = db.Column(db.Integer)
    section = db.Column(db.String(100))
    volume = db.Column(db.Integer)

class Periodicals(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'),
                          primary_key = True)
    title = db.Column(db.String(100))
    journal = db.Column(db.String(100))
    volume = db.Column(db.Integer)
    issue = db.Column(db.Integer)
    month = db.Column(db.String(50))
    year = db.Column(db.Integer)

class People(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    first = db.Column(db.String(20))
    middle = db.Column(db.String(20))
    last = db.Column(db.String(20))
    people_source = db.relationship('People_Source')
    sqlite_autoincrement = True

    def __repr__(self):
        if self.middle:
            return "{first} {middle} {last}".format(first = self.first, middle = self.middle, last = self.last)
        else:
            return "{first} {last}".format(first = self.first, last = self.last)

class People_Source(db.Model):
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'),
                          primary_key = True)
    people_id = db.Column(db.Integer, db.ForeignKey('people.id'),
                          primary_key = True)
    type = db.Column(db.String(20), primary_key = True)
    ## e.g. author, editor, translator

## tables relating to notes
## table of subtopics
class Topics(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    topics_notes = db.relationship('Topics_Notes')
    sqlite_autoincrement = True

## table of notes
class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    source_id = db.Column(db.Integer, db.ForeignKey('sources.id'))
    first_page = db.Column(db.Integer)
    last_page = db.Column(db.Integer)
    note = db.Column(db.String)
    topics_notes = db.relationship('Topics_Notes')
    sqlite_autoincrement = True

    ## representation method - include page number(s) if given
    def __repr__(self):
        if self.first_page:
            if self.last_page and self.last_page != self.first_page:
                return "{note} ({first}-{last})".format(
                    note = self.note,
                    first = self.first_page,
                    last = self.last_page
                )
            else:
                return "{note} ({first})".format(
                    note = self.note,
                    first = self.first_page
                )
        else:
            return "{}".format(self.note)

## table connecting notes-topics
class Topics_Notes(db.Model):
    note_id = db.Column(db.Integer, db.ForeignKey('notes.id'),
                        primary_key = True)
    topic_id = db.Column(db.Integer, db.ForeignKey('topics.id'),
                         primary_key = True)

