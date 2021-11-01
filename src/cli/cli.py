# https://pymotw.com/2/cmd/
# https://docs.python.org/3/library/cmd.html#module-cmd

import cmd
import re
import query

user = None
last_search = None

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
            user = uname # never use
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
    else:
        print("Invalid choice.\n")
        login()


def valid_email(email):
    regex = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if re.fullmatch(regex, email):
        return query.email_exists(email)
    return False


class DatamazingShell(cmd.Cmd):
    intro = 'Welcome to Datamazing! Type help or ? to list commands. \n'
    prompt = '(Datamazing) '
    file = None

    def do_create_collec(self, arg):
        'Create a new collection: create_collec collectionName'
        'please enter collection name'
        # check length of arg to get collection name
        # TODO
        name = None
        query.add_collec(user, name)
        return

    # TOTEST
    def do_list_collec(self, arg):
        'List the users collections: list_collec asc/des'
        collecs = query.list_collec(user)
        if(not collecs):
            print("No collections found")
        else:
            if arg == "asc":
                collecs.sort()
            else:
                collecs.sort(reverse=True)
            i = 1
            for collec in collecs:
                print(i, ": ", collec)
                i += 1

    # TODO
    def do_search_song(self, arg):
        # """Search for songs by song by various criteria: search_song criteria searchTerm\nCriteria:
        # \tsong\n\tartist\n\talbum\n\tgenre"""
        # args = parse(arg)
        # last_search = query.song_list(args[0], args[1], user)
        # DatamazingShell.print_songs()
        return

    # TODO
    def do_sort_search(self, arg):
        """Sort previous search results by various criteria: sort_search sortBy asc/desc\nsortBy:
        \tsong\n\tartist\n\tgenre\n\treleased"""
        # if (last_search is None):
        #     print("Please preform song search before sorting")
        # else:
        #     args = parse(arg)
        #     last_search = query.song_list_sort(args[0],args[1])
        #     DatamazingShell.print_songs()
        return

    # TODO
    def print_songs(self, last_search):
        # print("{:<3}{:<15}{:<15}{:<15}{:<15}".format("#","Song","Artist","Album","Length","Plays"))
        # i = 1
        # for s,a,al,l,c in last_search:
        #     print("{:<3}{:<15}{:<15}{:<15}{:<15}".format(i,s,a,al,l,c))
        #     i+=1
        return

    def do_add_collec_album(self, arg):
        # TODO may show a list of exist collection with ID, then let user to choose
        'Adds all songs in an album to a collection: add_collec_album collectionName albumID'
        #query.album_to_add(collectionName, albumID)
        return

    def do_add_collec_song(self, args):
        'Adds a song to a collection: add_collec_song collectionName songID'
        arg_names = parse(args)
        if not query.collec_exists(user, arg_names[0]):
            print("Collection was not found!")
        elif not query.if_exist('Song', 'name', arg_names[1]):
            print("Song was not found!")
        else:
            list_songs = query.songs_to_add(arg_names[1])
            print("{:<3}{:<15}{:<15}".format("#","Artist","Album","Release Date"))
            i = 1
            for a,al,d in list_songs:
                print("{:<3}{:<15}{:<15}".format(i,a,al,d))
                i+=1
            print("Please select which song you would like to add: ")
            # TODO ADD SONG TO COLLECTION
            
        return

    def do_rename_collec(self, args):
        'Rename an existing collection: rename_collec collectionName newName'
        c_names = parse(args)
        c_exist = query.collec_exists(user, c_names[0])
        c_new_exist = query.collec_exists(user, c_names[1])
        if not c_exist:
            print("Collection was not found!")
        elif c_new_exist:
            print("There is already another collection with that name.")
        else:
            query.rename_collec(user, *parse(args))

    def do_delete_collec(self, arg):
        'Delete an existing collection: delete_collection collectionName'
        if not query.collec_exists(user, arg):
            print("Collection was not found!")
        else:
            query.delete_collec(user, arg)

    def do_play_song(self, arg):
        'Play a song: play_song songName'
        return
    
    def do_show_collec(self, arg):
        'List out all of the songs within a collection: show_collec collectionName'
        return
        
    def do_play_collec(self, arg):
        'Play a collection: play_collec collectionName'
        return

    def do_search_user(self, arg):
        'Search for a user by name or email: search_user userName/userEmail'
        # if email not valid
        if not valid_email(arg):
            # if user doesn't exist
            if not query.user_exists(arg):
                print("User not found!")
            # if user does exist
            else:
                query.find_friend_u(arg)
        # if email is valid
        else:
            query.find_friend_e(arg)
        return

    def do_list_friends(self):
        'List users you follow: list_friends'
        query.show_friend_list(user)

    def do_follow(self, arg):
        'Follow a user: follow userToFollow'
        # if friend exists is checked in follow_friend so no need to here
        query.follow_friend(arg, user)

    def do_unfollow(self, arg):
        'Unfollow a user: unfollow userToUnfollow'
        # if friend exists is checked in unfollow_friend so no need to here
        if not query.user_exists(arg):
            print("User not found!")
        else:
            query.unfollow_friend(arg, user)

    # this will probably be changed but it is a start for logging out
    def do_logout(self, arg):
        'User would like to logout.'
        response = input('Are you sure? (y/n) ')
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
    return list(arg.split())


if __name__ == '__main__':
    login()
    DatamazingShell().cmdloop()
