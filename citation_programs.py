## Define author section
def mla_book_author(authors, publisher, author_type):
    ## if author is unknown, enter as authors = ["unknown"]
    if "unknown" in authors or "Unknown" in authors or "UNKNOWN" in authors:
        author_section = ""

    ## Corporate/Organization Authors
    elif author_type == "Corporation" or author_type == "Organization":
        if authors[0] == publisher:
            author_section = ""

        else:
            author_section = "{author}. ".format(
                author=authors[0])

    ## 1 normal author
    elif len(authors) == 1:
        author_split = authors[0].split()
        author_first = author_split[0]
        author_last = author_split[1]

        author_section = "{last}, {first}. ".format(
            last=author_last,
            first=author_first)

    ## 2 normal authors
    elif len(authors) == 2:
        author_1_split = authors[0].split()
        author_1_first = author_1_split[0]
        author_1_last = author_1_split[1]

        author_2_split = authors[1].split()
        author_2_first = author_2_split[0]
        author_2_last = author_2_split[1]

        author_section = "{last_1}, {first_1}, and {first_2} {last_2}. ".format(
            last_1=author_1_last,
            first_1=author_1_first,
            first_2=author_2_first,
            last_2=author_2_last)

    ## 3+ normal authors
    elif len(authors) > 2:
        author_1_split = authors[0].split()
        author_1_first = author_1_split[0]
        author_1_last = author_1_split[1]

        author_section = "{last_1}, {first_1}, et al. ".format(
            last_1=author_1_last,
            first_1=author_1_first)

    return author_section


def mla_book_editor(editor, author_section):
    ## Editor & author
    if len(editor) != 0 and author_section != "":
        if len(editor) == 1:
            editor_section = "Edited by {editor}, ".format(
                editor=editor[0])

        elif len(editor) == 2:
            editor_section = "Edited by {editor1} and {editor2}, ".format(
                editor1=editor[0],
                editor2=editor[1])

        else:
            editor_section = "Edited by {editor1}, et al.,  ".format(
                editor1=editor[0])

    ## Editor, no author
    elif len(editor) != 0 and author_section == "":
        if len(editor) == 1:
            editor_split = editor[0].split()
            editor_first = editor_split[0]
            editor_last = editor_split[1]

            author_section = "{last}, {first}, editor. ".format(
                last=editor_last,
                first=editor_first)

            editor_section = ""

        elif len(editor) == 2:
            editor_1_split = editor[0].split()
            editor_1_first = editor_1_split[0]
            editor_1_last = editor_1_split[1]

            editor_2_split = editor[1].split()
            editor_2_first = editor_2_split[0]
            editor_2_last = editor_2_split[1]

            author_section = "{last_1}, {first_1}, and {first_2} {last_2}, editors. ".format(
                last_1=editor_1_last,
                first_1=editor_1_first,
                first_2=editor_2_first,
                last_2=editor_2_last)

            editor_section = ""

        else:
            editor_split = editor[0].split()
            editor_first = editor_split[0]
            editor_last = editor_split[1]

            author_section = "{last}, {first}, et al., editors. ".format(
                first=editor_first,
                last=editor_first)

            editor_section = ""

    ## No editor
    else:
        editor_section = ""

    return editor_section, author_section


def mla_book(authors, title, publisher, year, editor="",
             translator="", author_type="person", edition=1,
             section="", volume="", pages="",
             website="", url="", access=""):
    author_section = mla_book_author(authors, publisher, author_type)

    editor_section, author_section = mla_book_editor(editor, author_section)

    ## translator section
    if len(translator) != 0:
        if len(translator) == 1:
            translator_section = "Translated by {translator}, ".format(
                translator=translator[0])

        if len(translator) == 2:
            translator_section = "Translated by {translator1} and {translator2}, ".format(
                translator1=translator[0],
                translator2=translator[1])

        else:
            translator_section = "Translated by {translator1}, et al., ".format(
                translator1=translator[0])
    else:
        translator_section = ""

    ## edition section
    if edition != None and edition != 1:
        if edition in [11, 12, 13]:
            label = "th"
        elif str(edition)[-1] == "1":
            label = "st"
        elif str(edition)[-1] == "2":
            label = "nd"
        elif str(edition)[-1] == "3":
            label = "rd"
        else:
            label = "th"

        edition_section = "{edition}{label} ed., ".format(
            edition=str(edition),
            label=label)
    else:
        edition_section = ""

    ## volume section
    if volume != "" and volume != None:
        volume_section = "vol. {volume}, ".format(volume=volume)
    else:
        volume_section = ""

    ## website/database section
    if len(website) != 0:
        website_section = " <em>{website}</em>".format(
            website=website)
    else:
        website_section = ""

    ## url section
    if len(url) != 0:
        if url.startswith("https://"):
            cleaned_url = url[len("https://"):]

        elif url.startswith("http://"):
            cleaned_url = url[len("http://"):]

        else:
            cleaned_url = url

        url_section = "{url}".format(
            url=cleaned_url)
    else:
        url_section = ""

    ## Date of Access
    if len(access) != 0:
        accessed = date(access[0], access[1], access[2]).strftime('%d %b %Y')
        access_section = ", Accessed {date}".format(date=accessed)
    else:
        access_section = ""

    ## Section
    if len(section) != 0:
        section_section = "\"{section}.\" ".format(section=section)
    else:
        section_section = ""

    ## Pages
    if len(pages) != 0:
        if len(pages) == 1:
            pages_section = ", p. {page}".format(page=pages[0])
        else:
            pages_section = ", pp. {first}-{last}".format(
                first=pages[0],
                last=pages[1])
    else:
        pages_section = ""

    citation = "{author}{section}<em>{title}</em>. {editor}{translator}{edition}{volume}{publisher}, {year}{pages}.{website}{url}{access}".format(
        author=author_section,
        section=section_section,
        title=title,
        editor=editor_section,
        edition=edition_section,
        volume=volume_section,
        translator=translator_section,
        publisher=publisher,
        year=year,
        pages=pages_section,
        website=website_section,
        url=url_section,
        access=access_section)

    return citation

# Periodical Citation
def mla_journal_citation(authors="", title="", journal="",
                         volume="", issue="", month="",
                         year="", pages="", database="",
                         doi="", link="", access="",
                         author_type="person"):
    ## Author section; publisher is NA for journals
    author_section = mla_book_author(authors, "", author_type)

    ## volume
    if len(str(volume)) > 0:
        volume_section = ", vol. {volume}".format(volume=str(volume))
    else:
        volume_section = ""

    ## issue
    if len(str(issue)) > 0:
        issue_section = ", no. {issue}".format(issue=str(issue))
    else:
        issue_section = ""

    ## month
    if len(month) == 0:
        month_section = ""
    elif len(month) > 4:
        if month.lower() == "september":
            month_section = ", Sept."
        else:
            month_section = ", " + month.title()[:3] + "."
    else:
        month_section = ", " + month.title()

    ## Pages
    if len(pages) != 0:
        if len(pages) == 1:
            pages_section = ", p. {page}".format(page=pages[0])
        else:
            pages_section = ", pp. {first}-{last}".format(
                first=pages[0],
                last=pages[1])
    else:
        pages_section = ""

    ## Database
    if len(database) != 0:
        database_section = ". <em>{database}</em>".format(database=database)
    else:
        database_section = ""

    ## DOI
    if len(doi) != 0:
        doi_section = ", doi: {doi}".format(doi=doi)
    else:
        doi_section = ""

    ## Link - only used if no doi
    if len(doi) == 0 and len(link) != 0:
        link_section = ", {link}".format(link=link)
    else:
        link_section = ""

    ## Access Date
    if len(access) != 0:
        accessed = date(access[0], access[1], access[2]).strftime('%d %b %Y')
        access_section = " Accessed {date}".format(date=accessed)
    else:
        access_section = ""

    citation = '''{author}\"{title}.\" <em>{journal}</em>{volume}{issue}{month}, {year}{pages}{database}{doi}{link}{access}.'''.format(
        author=author_section,
        title=title,
        journal=journal,
        volume=volume_section,
        issue=issue_section,
        month=month_section,
        year=year,
        pages=pages_section,
        database=database_section,
        doi=doi_section,
        link=link_section,
        access=access_section
    )

    return citation