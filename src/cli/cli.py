# Reference
# cmd.select: Presents a numbered menu to the user;
# https://cmd2.readthedocs.io/en/latest/features/misc.html?highlight=menu#select
# PRI of refactoring this application
# 1. realize basic functions (CRUD)
# 2. realize requirement functions (recommend system)
# 3. improve overall code design
# 4. improve user experience

import cmd2
from cmd2 import *
import re, sys, datetime
from datetime import datetime
import starbug, create, read, update, delete


def valid_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.fullmatch(regex, email):
       return True
    return False

def login_in():
    while True:
        login_username = input("Username: ")
        if not read.verify_username(login_username):
            again = input(f"User {login_username} does not exist. Try again (y/n)? ")
            if again.lower()[0] == 'n':
                return False
        else:
            break

    attempt = 3
    while attempt > 0:
        password = input("Password: ")
        if read.verify_password(login_username, password):
            create.login_user(login_username)
            print(f"User {login_username} logins at {datetime.now()}")
            return login_username
        attempt -= 1
        print(f"Incorrect password! Remaining attempt(s) {attempt}.")
    print("Passwords entered more than three times.")
    return None

def sign_up():
    while True:
        new_username = input("\nNew username: ")
        if read.verify_username(new_username):
            again = input(f"Username {new_username} is already taken! Try again (y/n)? ")
            if again.lower()[0] == 'n':
                return False
        else:
            break

    while True:
        new_password = input("\nNew password: ")
        confirm_password = input("Retype new password to confirm: ")
        if new_password != confirm_password:
            again = input(f"Passwords do not match! Try again (y/n)? ")
            if again.lower()[0] == 'n':
                return False
        else:
            break
    new_first_name = input("\nPlease enter your first name: ")
    new_last_name = input("Please enter your last name: ")
    while True:
        new_email_address = input("Please enter your email address: ")
        if valid_email(new_email_address):
            if read.verify_email(new_email_address):
                again = input(f"Email {new_email_address} has been used! Try again (y/n)? ")
                if again.lower()[0] == 'n':
                    return False
            else:
                break
        else:
            again = input(f"Invalid email format! Try again (y/n)? ")
            if again.lower()[0] == 'n':
                return False
    create.register_user(new_username, new_password, new_first_name,
                         new_last_name, new_email_address)
    print(f"Successfully create user {new_username}! Back to login.")
    return True

def entrance():
    choice = int(input(
        "What would you like to do?\n\t1. log in\n\t2. sign up\n\t3. quit\nPlease enter (1-3): "))
    if choice == 1:
        return_username = login_in()
        if return_username is None:
            entrance()
        else:
            return return_username
    elif choice == 2:
        if sign_up():
            # Duplication with the previous if, may need to be simplified
            return_username = login_in()
            if return_username is None:
                entrance()
            else:
                return return_username
        else:
            entrance()
    elif choice == 3:
        sys.exit("bye!")
    else:
        print("Invalid choice.\n")
        entrance()

class DatamazingShell(cmd2.Cmd):
    def __init__(self, username):
        super().__init__()
        self.hidden_unneed_commands()
        self.intro = style('Welcome to Datamazing! Type help or ? to list commands!')
        self.prompt = "(Datamazing) "
        self.username = username

    def hidden_unneed_commands(self):
        # hide unnecessary builtin Commands
        self.hidden_commands.append('alias')
        self.hidden_commands.append('edit')
        self.hidden_commands.append('run_script')
        self.hidden_commands.append('shell')
        self.hidden_commands.append('macro')
        self.hidden_commands.append('run_pyscript')
        self.hidden_commands.append('set')
        self.hidden_commands.append('shortcuts')

    def do_search_user(self, arg):
        'Search for a user by name or email: search_user userName/userEmail'
        user_f = arg
        if valid_email(user_f):
            user_f_info = read.get_user_info(user_f, True)
        else:
            user_f_info = read.get_user_info(user_f, False)
        if user_f_info is not None:
            print("User " + user_f + " was found!")
            # TODO format
            print(user_f_info)
        else:
            print("User " + arg + " was not found!")

    def do_list_friends(self, arg):
        'List users you follow: list_friends'
        # gets list of friends and outputs first name, last name, username
        # passed test (if everyone is okay with this format)
        friends = read.show_friend_list(self.username)
        print(friends)

        #print("{:<3}{:<15}{:<15}{:<15}".format("#", "First name", "Last name", "Username"))
        #i = 1
        #for fn, ln, un in friends:
        #    print("{:<3}{:<15}{:<15}{:<15}".format(i, fn, ln, un))
        #    i += 1

    def do_follow(self, arg):
        'Follow a user: follow userToFollow(username)'
        # if user exists is checked here so that a message is printed out
        friend = arg
        if not read.verify_username(friend):
            print(f"User {friend} not found!")
        else:
            info = create.follow_friend(self.username, friend)
            if info is not None:
                print("Following", info)
            else:
                print("fail to follow", friend)

    def do_unfollow(self, arg):
        'Unfollow a user: unfollow userToUnfollow'
        # if user exists is checked here so that a message is printed out
        not_friend = arg
        if not read.verify_username(not_friend):
            print(f"User {not_friend} not found!")
        else:
            info = delete.unfollow_friend(self.username, not_friend)
            if info is not None:
                print("Unfollowing", info)
            else:
                print("Fail to unfollow", not_friend)

    list_collec_parser = cmd2.Cmd2ArgumentParser()
    list_collec_parser.add_argument('-a', '--asc', action='store_true', help='list collection in ascending order')
    list_collec_parser.add_argument('-d', '--desc', action='store_true', help='list collection in descending order')
    @with_argparser(list_collec_parser)
    def do_list_collec(self, opts):
        # TODO
        # Users will be to see the list of all their collections by name in ascending order. The list
        # must show the following information per collection:
        # – Collection’s name
        # – Number of songs in the collection
        # – Total duration in minutes
        'List the users collections: list_collec asc(default)/desc'
        # collection {id, username, collection_name}

        collecs = None
        if opts.desc:
            collecs = read.list_collec(self.username, False)
        else:
            collecs = read.list_collec(self.username, True)

        print(collecs)
            # i = 1
            # for collec in collecs:
            #     # removes parenthesis and commas
            #     c = str(collec)[1:-2]
            #     print(i, ": ", c)
            #     i += 1

    def do_create_collec(self, arg):
        'Create a new collection: create_collec collectionName'
        name = arg
        info = create.add_collec(self.username, name)
        print(f"New collection created:\n {info}")


    # def do_articulate(self, statement):
    #     # demo for get args
    #     # 1st option
    #     # statement.argv contains the command
    #     # and the arguments, which have had quotes
    #     # stripped
    #     for arg in statement.argv:
    #         self.poutput(arg)

#     # 🎈test
    def do_delete_collec(self, arg):
        # pass test
        'Delete an existing collection: delete_collection collectionName'
        collectionid = arg
        if not read.verify_collec(self.username, collectionid):
            print("Collection was not found!")
        else:
            info = delete.delete_collec(self.username, collectionid)
            print(f"Deleted collection {info}")
#     # 🎈test
#     def do_play_song(self, arg):
#
#         'Play a song: play_song songID'
#         songid = arg
#         if query.if_exist('song', 'songid', songid):
#             print("playing", query.play_song(user, songid))
#         else:
#             print("song entered does not exist"
#
if __name__ == '__main__':
    user = entrance()
    if user is not None:
        app = DatamazingShell(user)
        app.debug = True
        if app.cmdloop() == 0:
            sys.exit('bye!')

