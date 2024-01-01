def init_blacklist_file():
    open("jwt_blacklist.txt", "a").close()
    return True


def add_blacklist_token(token):
    with open("jwt_blacklist.txt", "a") as file:
        file.write(f"{token},")
    return True


def is_token_blacklisted(token):
    with open("jwt_blacklist.txt") as file:
        content = file.read()
        array = content[:-1].split(",")
        for value in array:
            if value == token:
                return True

    return False
