# https://pymotw.com/2/cmd/
# https://docs.python.org/3/library/cmd.html#module-cmd

import cmd
import re
import query


def login():
    choice = int(input(
        "What would you like to do?\n\t1. log in\n\t2. sign up\nPlease enter 1 or 2: "))
    if choice == 1:
        uname = input("\nPlease enter your username.\nUsername: ")
        if not query.user_exists(uname):
            print("User does not exist.\n")
            login()
        else:
            pw = input("\nPlease enter your password.\nPassword: ")
            while not query.pass_correct(uname, pw):
                print("Incorrect password.")
                pw = input("\nPlease enter your password.\nPassword: ")
            print("Logging in.")
    elif choice == 2:
        poss_uname = input("\nPlease choose a username: ")
        while query.user_exists(poss_uname):
            print("That username is already taken.")
            poss_uname = input("\nPlease choose your username: ")
        new_pw = input("\nPlease choose a password: ")
        confirm_pw = input("Please retype the password: ")
        while new_pw != confirm_pw:
            print("Passwords do not match")
            new_pw = input("\nPlease choose a password: ")
            confirm_pw = input("Please retype the password: ")
        new_first_name = input("\nPlease enter your first name: ")
        new_last_name = input("Please enter your last name: ")
        new_email_address = input("Please enter your email address: ")
        while not valid_email(new_email_address):
            print("Invalid email")
            new_email_address = input("\nPlease enter valid email address: ")
        query.register_user(poss_uname, new_pw, new_first_name,
                            new_last_name, new_email_address)
        login()


def valid_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.fullmatch(regex, email):
        # TODO CHECK IF EMAIL IS IN DATABASE ALREADY
        return query.email_exists(email)
    return False


class DatamazingShell(cmd.Cmd):
    intro = 'Welcome to Datamazing! Type help or ? to list commands. \n'
    prompt = '(Datamazing)'
    file = None

    def do_create_collec(self, arg):
        'Create a new collection: create_collec collectionName'
        # TODO CHECK IF COLLECTION NAME ALREADY IN DATABASE
        # QUESTION: not sure if it is necessary, since there is a collectionID and username to control the uniqueness of the collection.
        # If it is useful to make it unique in the database, I need to modify the table to make the name column to be unique
        return

    def do_list_collec(self, arg):
        'List the collections: list_collec asc/des'
        return

    def do_search_song(self, arg):
        # QUESTION: how to
        """Search for songs by song by various criteria: search song criteria searchTerm\nCriteria:
        \tsong\n\tartist\n\talbum\n\tgenre"""
        return

    def do_sort_search(self, arg):
        """Sort previous search results by various criteria: sort_search sortBy asc/des\nsortBy:
        \tsong\n\tartist\n\tgenre\n\treleased"""
        return

    def do_add_collec_album(self, arg):
        'Adds all songs in an album to a collection: add_collec_album collectionName albumID'
        return

    def do_add_collec_song(self, arg):
        'Adds a song to a collection: add_collec_song collectionName songID'
        return

    def do_rename_collec(self, arg):
        'Rename an existing collection: rename_collection collectionName newName'
        return

    def do_delete_collec(self, arg):
        'Delete an existing collection: delete_collection collectionName'
        return

    def do_play_song(self, arg):
        'Play a song: play_song songName'
        return

    def do_play_collec(self, arg):
        'Play a collection: play_collec collectionName'
        return

    def do_search_user(self, arg):
        'Search for a user by name or email: search_user userName/userEmail'
        return

    def do_list_friends(self):
        'List users you follow: list_friends'
        return

    def do_follow(self, arg):
        'Follow a user: follow userToFollow'
        return

    def do_unfollow(self, arg):
        'Unfollow a user: unfollow userToUnfollow'
        return

    # this will probably be changed but it is a start for logging out
    def do_logout(self, arg):
        'User would like to logout.'
        response = input('Are you sure? (y/n)')
        if response == "y":
            print('Okay, bye!')
            self.close()
            quit()
        else:
            print("Not logging out.")

    def close(self):
        if self.file:
            self.file.close()
            self.file = None


def parse(arg):
    return tuple(arg.split())


if __name__ == '__main__':
    login()
    DatamazingShell().cmdloop()
