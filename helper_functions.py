from app import db
from models import *
from sqlalchemy import func

# function to retrieve list of tuples of people from form
def get_form_people(form):
    people = [(form.person_first.data, form.person_middle, form.person_last.data, form.person_type.data),
              (form.second_person_first.data, form.second_person_middle.data, form.second_person_last.data,
               form.second_person_type.data),
              (form.third_person_first.data, form.third_person_middle.data, form.third_person_last.data,
               form.third_person_type.data),
              (form.fourth_person_first.data, form.fourth_person_middle.data, form.fourth_person_last.data,
               form.fourth_person_type.data),
              (form.fifth_person_first.data, form.fifth_person_middle.data, form.fifth_person_last.data,
               form.fifth_person_type.data)]

    return people

# function to loop through people in form, add to database, and return lists of
    # authors, editors, translators
def sort_new_people(form, new_source_id):
    # list of people from form
    people = get_form_people(form)

    # empty lists of authors/editors/translators
    authors = []
    editors = []
    translators = []

    # loop through people
    for person in people:
        # if any name field is not blank
        if (person[0] or person[1] or person[2]):
            # blank fields coerced to empty string instead of stringfield object
            new_person = People(first=person[0] if isinstance(person[0], str) else "",
                                middle=person[1] if isinstance(person[1], str) else "",
                                last=person[2] if isinstance(person[2], str) else "")
            db.session.add(new_person)
            db.session.commit()
            if person[3] == 'author': authors.append(new_person.__repr__())
            if person[3] == 'editor': editors.append(new_person.__repr__())
            if person[3] == 'translator': translators.append(new_person.__repr__())

            new_person_id = db.session.query(func.max(People.id)).scalar()
            new_people_source = People_Source(source_id=new_source_id,
                                              people_id=new_person_id,
                                              type=person[3])

            db.session.add(new_people_source)
            db.session.commit()

    # return lists of authors, editors, translators
    return authors, editors, translators

# function to query all people with source_id, assign as defaults for form
def set_people_defaults(form, source_id):
    # query people names & people_source types
    people_with_id = db.session.query(People.id, People.first, People.middle, People.last, People_Source.type).\
        join(People_Source).filter(People_Source.source_id == source_id).all()
    people_id = [person[0] for person in people_with_id]
    people = [person[1:] for person in people_with_id]

    if len(people) > 0:
        form.person_first.default = people[0][0]
        form.person_middle.default = people[0][1]
        form.person_last.default = people[0][2]
        form.person_type.default = people[0][3]

        if len(people) > 1:
            form.second_person_first.default = people[1][0]
            form.second_person_middle.default = people[1][1]
            form.second_person_last.default = people[1][2]
            form.second_person_type.default = people[1][3]

            if len(people) > 2:
                form.third_person_first.default = people[2][0]
                form.third_person_middle.default = people[2][1]
                form.third_person_last.default = people[2][2]
                form.third_person_type.default = people[2][3]

                if len(people) > 3:
                    form.fourth_person_first.default = people[3][0]
                    form.fourth_person_middle.default = people[3][1]
                    form.fourth_person_last.default = people[3][2]
                    form.fourth_person_type.default = people[3][3]

                    if len(people) > 4:
                        form.fifth_person_first.default = people[4][0]
                        form.fifth_person_middle.default = people[4][1]
                        form.fifth_person_last.default = people[4][2]
                        form.fifth_person_type.default = people[4][3]

    return people, people_id

# function to update people records from edit form
def update_people(form, people, people_id, source_id):
    # list of people from form
    new_people = get_form_people(form)

    # empty lists of authors, editors, translators
    authors = []
    editors = []
    translators = []

    # loop through new people
    for person in new_people:
        if person not in people and (person[0] or person[1] or person[2]):
            # if new person didn't already exist, add People instance
            add_person = People(first=person[0] if isinstance(person[0], str) else "",
                                middle=person[1] if isinstance(person[1], str) else "",
                                last=person[2] if isinstance(person[2], str) else "")
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
            People_Source.query.filter(People_Source.people_id == people_id[i]). \
                filter(People_Source.source_id == source_id).delete()
            db.session.commit()

    return authors, editors, translators