import re

def is_phrase_in(phrase, text):
    return re.search(r"\b{}\b".format(phrase), text, re.IGNORECASE) is not None


def normalize(date):
    year = date.replace(" ", "")
    year = year[-4:]
    if is_phrase_in("January", date)  or is_phrase_in("Ιανουαρίου", date):
        month = 1
    elif is_phrase_in("February", date)  or is_phrase_in("Φεβρουαρίου", date):
        month = 2
    elif is_phrase_in("March", date)  or is_phrase_in("Μαρτίου", date):
        month = 3
    elif is_phrase_in("April", date)  or is_phrase_in("Απριλίου", date):
        month = 4
    elif is_phrase_in("May", date)  or is_phrase_in("Μαΐου", date):
        month = 5
    elif is_phrase_in("June", date)  or is_phrase_in("Ιουνίου", date):
        month = 6
    elif is_phrase_in("July", date)  or is_phrase_in("Ιουλίου", date):
        month = 7
    elif is_phrase_in("August", date)  or is_phrase_in("Αυγούστου", date):
        month = 8
    elif is_phrase_in("September", date)  or is_phrase_in("Σεπτεβρίου", date):
        month = 9
    elif is_phrase_in("October", date)  or is_phrase_in("Οκτωβρίου", date):
        month = 10
    elif is_phrase_in("November", date)  or is_phrase_in("Νοεμβρίου", date):
        month = 11
    elif is_phrase_in("December", date)  or is_phrase_in("Δεκεμβρίου", date):
        month = 12
    elif "/" in date:
        month = date.split("/", 1)[0]
    else:
        month = 1
    return  month,year

