# main application

from typing import List

import cmd2
from cmd2 import *
import re, sys, datetime
from datetime import datetime
import create, read, update, delete
from cmd2.table_creator import *



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

    def ansi_print(self, text):
        ansi.style_aware_write(sys.stdout, text + '\n\n')


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
            info = []
            info.append(user_f_info)
            print("User " + user_f + " was found!")
            columns: List[Column] = list()
            columns.append(Column("First Name", width=20))
            columns.append(Column("Last Name", width=20))
            columns.append(Column("Username", width=30))
            columns.append(Column("Email", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(info)
            self.ansi_print(table)
        else:
            print("User " + arg + " was not found!")


    def do_list_friends(self, arg):
        'List users you follow: list_friends'

        friends = read.show_friend_list(self.username)
        columns: List[Column] = list()
        columns.append(Column("First Name", width=20))
        columns.append(Column("Last Name", width=20))
        columns.append(Column("Email", width=30))
        columns.append(Column("Username", width=20))
        st = SimpleTable(columns)
        table = st.generate_table(friends)
        self.ansi_print(table)

    def do_follow(self, arg):
        'Follow a user: follow userToFollow(username)'
        # if user exists is checked here so that a message is printed out
        friend = arg
        if not read.verify_username(friend):
            print(f"User {friend} not found!")
        else:
            info = create.follow_friend(self.username, friend)
            if info is not None:
                u_info = []
                u_info.append(info)
                print("Following\n")
                columns: List[Column] = list()
                columns.append(Column("First Name", width=20))
                columns.append(Column("Last Name", width=20))
                columns.append(Column("Username", width=30))
                columns.append(Column("Email", width=20))
                st = SimpleTable(columns)
                table = st.generate_table(u_info)
                self.ansi_print(table)
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
                u_info = []
                u_info.append(info)
                print("Unfollowing\n")
                columns: List[Column] = list()
                columns.append(Column("First Name", width=20))
                columns.append(Column("Last Name", width=20))
                columns.append(Column("Username", width=30))
                columns.append(Column("Email", width=20))
                st = SimpleTable(columns)
                table = st.generate_table(u_info)
                self.ansi_print(table)
            else:
                print("Fail to unfollow", not_friend)

    list_collec_parser = Cmd2ArgumentParser()
    list_collec_parser.add_argument('-a', '--asc', action='store_true', help='list collection in ascending order')
    list_collec_parser.add_argument('-d', '--desc', action='store_true', help='list collection in descending order')
    @with_argparser(list_collec_parser)
    def do_show_collecs(self, opts):
        """
        show_collecs --asc(-a)/--desc(-d)
        """
        if opts.desc:
            collecs = read.list_user_collec(self.username, False)
        elif opts.asc:
            collecs = read.list_user_collec(self.username, True)
        else:
            print("Please use --asc/-a or --desc/-d")
            return

        columns: List[Column] = list()
        columns.append(Column("Collection Name", width=20))
        columns.append(Column("Collection ID", width=20))
        columns.append(Column("Number of song", width=20))
        columns.append(Column("Total length", width=20))
        st = SimpleTable(columns)
        table = st.generate_table(collecs)
        self.ansi_print(table)


    def do_create_collec(self, arg):
        'create_collec collectionName'
        name = arg
        info = []
        info.append(create.create_collec(self.username, name))
        print("New collection created!\n")
        columns: List[Column] = list()
        columns.append(Column("Collection Name", width=20))
        columns.append(Column("Collection ID", width=20))
        st = SimpleTable(columns)
        table = st.generate_table(info)
        self.ansi_print(table)

    def do_delete_collec(self, arg):
        'Delete an existing collection: delete_collection collectionName'
        collectionid = arg
        info = []
        collec_info = read.get_collec_info(self.username, collectionid)
        if len(collec_info) == 0:
            print("Collection was not found!")
        else:
            info.append([collec_info[0], collec_info[2]])
            delete.delete_collec(self.username, collectionid)
            print("Deleted collection")
            columns: List[Column] = list()
            columns.append(Column("Collection ID", width=20))
            columns.append(Column("Collection Name", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(info)
            self.ansi_print(table)


    rename_collec_parser = Cmd2ArgumentParser()
    rename_collec_parser.add_argument('collectionid', nargs='?', help='collection ID')
    rename_collec_parser.add_argument('new_name', nargs='?', help='new collection name')
    @with_argparser(rename_collec_parser)
    def do_rename_collec(self, args):
        """
        rename_collec <collectionid> <new_name>
        list collection -> get collectionid -> rename the collection with new name
        """
        'Rename an existing collection: rename_collec collectiondid new_name'
        collectionid = args.collectionid
        collection_info = read.get_collec_info(self.username, collectionid)
        new_name = args.new_name
        if len(collection_info) == 0:
            print(f"User {self.username} does not own this collection!")
        else:
            modified = update.rename_collec(self.username, collectionid, new_name)
            print(f"sucessfully rename collection \"{collection_info[2]}\" to \"{modified[2]}\"")


    add_collec_album_parser = Cmd2ArgumentParser()
    add_collec_album_parser.add_argument('collectionid', nargs='?', help='collection ID')
    add_collec_album_parser.add_argument('albumid', nargs='?', help='album ID')
    @with_argparser(add_collec_album_parser)
    def do_add_collec_album(self, args):
        """
        add_collec_album collectionid albumid
        list collections -> get collectionid
        search album -> get albumid
        add song with albumid and collectionid
        """
        'Adds all songs in an album to a collection: add_collec_album collectionID albumID'
        collection_info = read.get_collec_info(self.username, args.collectionid)
        album_info = read.get_album_info(args.albumid)
        if len(album_info) == 0:
            print(f"The album {args.albumid} does not exist")
        elif len(collection_info) == 0:
            print(f"The collection {args.collectionid} does not belong to user {self.username}")
        else:
            print(f"adding all song from album \"{album_info[1]}\" to collection {collection_info[2]}")

            create.album_to_collec(self.username, args.collectionid, args.albumid)

    add_collec_song_parser = Cmd2ArgumentParser()
    add_collec_song_parser.add_argument('collectionid', nargs='?', help='collection ID')
    add_collec_song_parser.add_argument('songid', nargs='?', help='song ID')
    @with_argparser(add_collec_song_parser)
    def do_add_collec_song(self, args):
        'Adds a song to a collection: add_collec_song collectionID songID'
        collection_info = read.get_collec_info(self.username, args.collectionid)
        if len(collection_info) == 0:
            print("Collection was not found!")
        else:
            song_info = read.get_song_info(args.songid)
            if len(song_info) == 0:
                print("Song was not found!")
            else:
                local_number = create.add_song_collec(self.username, args.collectionid, args.songid)[0][0]
                print(f"Song `{song_info[1]}` has added into collection `{collection_info[2]}` at local number `{local_number}`")


    def do_play_song(self, arg):
        'Play a song: play_song songID'
        songid = arg
        if read.verify_item('song', 'songid', songid):
            info = []
            info.append(create.play_song(user, songid))
            print("playing")
            columns: List[Column] = list()
            columns.append(Column("Song ID", width=20))
            columns.append(Column("Song name", width=20))
            columns.append(Column("Artist", width=20))
            columns.append(Column("Length", width=20))
            columns.append(Column("Genre", width=20))
            columns.append(Column("Released Date", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(info)
            self.ansi_print(table)
        else:
            print("song entered does not exist")

    def do_profile(self, arg):
        """list user profile"""
        collecs_info = read.get_profile(self.username)
        print(f"======{self.username}'s profile=======")
        print(f"# of collections {collecs_info[0]}")
        print(f"# of followers {collecs_info[1]}")
        print(f"# of following {collecs_info[2]}")
        print(f"\n ===Top 10 artist {self.username} most plays===")
        columns: List[Column] = list()
        columns.append(Column("ArtistName", width=20))
        columns.append(Column("# of Play", width=20))
        st = SimpleTable(columns)
        table = st.generate_table(collecs_info[3])
        self.ansi_print(table)

    recommend_parser = Cmd2ArgumentParser()
    recommend_parser.add_argument('-a', action='store_true', help='list top 50 most popular songs in the last 30 days')
    recommend_parser.add_argument('-b', action='store_true', help='list top 50 most popular songs among friend')
    recommend_parser.add_argument('-c', action='store_true', help='list top 5 most popular genres of the month')
    recommend_parser.add_argument('-r', action='store_true', help='list recommend songs (for you)')
    @with_argparser(recommend_parser)
    def do_recommend(self, opts):
        """
        recommend system
        recommend -a: show top 50 most popular songs in the last 30 days
        recommend -b: show top 50 most popular songs among my friends
        recommend -c: show top 5 most popular genres of the month (calendar month)
        recommend -r: show recommend song based on top 3 genres and artists (each 3 songs)
        """
        if not (opts.c or opts.b or opts.a or opts.r):
            print("Wrong argument!")
            return

        if not opts.c:
            songs = None
            if opts.a:
                songs = read.get_recommend(self.username, 'a')
                print("===The top 50 most popular songs in the last 30 days===\n")
            elif opts.b:
                songs = read.get_recommend(self.username, 'b')
                print("===The top 50 most popular songs among my friends===\n")
            elif opts.r:
                songs = read.get_recommend(self.username, 'r')
                print("===Recommend songs based on genre, artist===")
            columns: List[Column] = list()
            columns.append(Column("Song ID", width=20))
            columns.append(Column("Song Title", width=20))
            columns.append(Column("Artist", width=20))
            columns.append(Column("Play Count", width=20))
            columns.append(Column("Length", width=20))
            columns.append(Column("Genre", width=20))
            columns.append(Column("Create Date", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(songs)
            self.ansi_print(table)
        else:
            genres = read.get_recommend(self.username, 'c')
            print("===The top 5 most popular genres of the month (calendar month)===")
            columns: List[Column] = list()
            columns.append(Column("Genre Name", width=20))
            columns.append(Column("Play Count", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(genres)
            self.ansi_print(table)

    search_parser = Cmd2ArgumentParser()
    search_parser.add_argument('-s', '--song', action='store_true', help='list song by song name')
    search_parser.add_argument('-a', '--artist', action='store_true', help='list song by artist name')
    search_parser.add_argument('-al', '--album', action='store_true', help='list song by album name')
    search_parser.add_argument('-g', '--genre', action='store_true', help='list song by genre')
    search_parser.add_argument('criteria', nargs='+', help='word to say')
    @with_argparser(search_parser)
    def do_search_song(self, opts):
        """
        search_song -s/--song [criteria]: search for a song by song name
        search_song -a/--artist [criteria]: search for a song by artist name
        search_song -al/--album [criteria]: search for a song by album name
        search_song -g/--genre [criteria]: search for a song by genre
        """
        arg = opts.criteria
        args = ''
        for i in range(len(arg) - 1):
            args += arg[i]
            args += " "
        args += arg[-1]
        if not (opts.song or opts.artist or opts.album or opts.genre):
            print("Invalid Criteria!!!")
            return
        elif opts.criteria is None:
            print("No criteria entered")
            return
        songs = []
        if opts.song:
            songs = read.list_songs_song(args)
        elif opts.artist:
            songs = read.list_songs_artist(args)
        elif opts.album:
            songs = read.list_songs_album(args)
        elif opts.genre:
            songs = read.list_songs_genre(args)

        if len(songs) != 0:
            columns: List[Column] = list()
            columns.append(Column("Song ID", width=20))
            columns.append(Column("Album ID", width=20))
            columns.append(Column("Song Title", width=20))
            columns.append(Column("Artist", width=20))
            columns.append(Column("Genre", width=20))
            columns.append(Column("Album", width=20))
            columns.append(Column("Length", width=20))
            st = SimpleTable(columns)
            table = st.generate_table(songs)
            self.ansi_print(table)
        else:
            print("No result!")


if __name__ == '__main__':
    user = entrance()
    if user is not None:
        app = DatamazingShell(user)
        app.debug = True
        if app.cmdloop() == 0:
            sys.exit('bye!')

