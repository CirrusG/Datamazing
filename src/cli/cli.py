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

global username

def valid_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.fullmatch(regex, email):
       return True
    return False

def login_in():
    while True:
        username = input("Username: ")
        if not read.verify_username(username):
            again = input(f"User {username} does not exist. Try again (y/n)? ")
            if again.lower()[0] == 'n':
                return False
        else:
            break

    attempt = 3
    while attempt > 0:
        password = input("Password: ")
        if read.verify_password(username, password):
            create.login_user(username)
            print(f"User {username} logins at {datetime.now()}")
            return True
        attempt -= 1
        print(f"Incorrect password! Remaining attempt(s) {count}.")
    print("Passwords entered more than three times.")
    return False

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
        if not login_in():
            entrance()
    elif choice == 2:
        if sign_up():
            if not login_in():
                entrance()
        else:
            entrance()
    elif choice == 3:
        sys.exit("bye!")
    else:
        print("Invalid choice.\n")
        entrance()

class DatamazingShell(cmd2.Cmd):
    def __init__(self):
        super().__init__()
        self.hidden_unneed_commands()
        self.intro = style('Welcome to Datamazing! Type help or ? to list commands!')
        self.prompt = "(Datamazing) "

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
            # if user doesn't exist
            user_f_info = read.get_user_info(user_f, True)
       # if email is valid
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
        friends = read.show_friend_list(user)
        print("{:<3}{:<15}{:<15}{:<15}".format("#", "First name", "Last name", "Username"))
        i = 1
        for fn, ln, un in friends:
            print("{:<3}{:<15}{:<15}{:<15}".format(i, fn, ln, un))
            i += 1

    def do_follow(self, arg):
        'Follow a user: follow userToFollow(username)'
        # if user exists is checked here so that a message is printed out
        friend = arg
        if not read.verify_username(friend):
            print(f"User {friend} not found!")
        else:
            create.follow_friend(username, friend)

    # TOFIX
    def do_unfollow(self, arg):
        # passed test
        'Unfollow a user: unfollow userToUnfollow'
        # if user exists is checked here so that a message is printed out
        if not query.user_exists(arg):
            print("User not found!")
        else:
            query.unfollow_friend(arg, user)
        print("done!")

    # def do_articulate(self, statement):
    #     # demo for get args
    #     # 1st option
    #     # statement.argv contains the command
    #     # and the arguments, which have had quotes
    #     # stripped
    #     for arg in statement.argv:
    #         self.poutput(arg)



if __name__ == '__main__':
    entrance()
    c = DatamazingShell()
    if c.cmdloop() == 0:
        sys.exit('bye!')

