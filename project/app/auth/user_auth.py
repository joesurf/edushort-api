# create a fake db
FAKE_DB = {"hey@joesurf.io": {"name": "Joseph"}}


def valid_email_from_db(email):
    return email in FAKE_DB
