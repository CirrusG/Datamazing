# TODO based on phase 3 requirement

- [x] revise phase 2

- [x] design of overall database/project structure

- [x] sql script (as external file to implement a single function)

  - [x] Create table
  - [x] insert sample sql for test table function
    - [x] 3-9 insertion of each table
    - [x] 2-5 queries of each table

  - [x] deploy to database
  - [x] grant permission

- [ ] application (interface based on requirement using sql function)

  For each user

  - [x] create new accounts (create sql)

    - [x] valid input
      - [x] if username exist in db: get the sql error message / check the db firstly
      - [x] if email has '@'
        - [Check if email address valid or not in Python](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/)
      - [x] password, first/last_name if empty

  - [x] Access via login

    - [x] valid username (if exist in db)
    - [x] valid password

  - [x] record date and time of both above activity (automatically added when insert into db)

  - [x] create collections of music (create)
  - [x] modify collection (alter, drop)
    - [x] change name
    - [x] delete the entire collection
  - [x] query/read list of collections (select)
  - [x] add/delete albums, songs from collection (insert, drop)

  - [ ] search song / show resulting list (select)
  - [ ] listen to song (select)

    - [x] add record to plays
    - [ ] maybe make a timer -- cli
    - type
      - [ ] individually
      - [ ] entire collection (list)
    - [ ] mark played and not played
    - show current play status

  - [x] follow/unfollow friend
    - [x] ~~check username at table account~~
    - [x] check following/follows at Follows table
    - [x] delete / insert
  - [x] search for new friends by email

- [ ] insert enough dataset for each table

  - [x] local
  - [ ] starbug
  - 10s - 100s rows/table
  - 200 - 500 rows/M:N table
  - source
    - spotify api
    - etc... (if has better choice)

- [ ] update phase 2 (report)

  - [ ] outline changes to EER diagram and reduction to tables
    - [ ] create tables
    - [ ] 2-5 queries for each table for populating the data
    - [ ] 5-10 insertion
      - [ ] explain how to load data
      - [ ] must loaded into the proper account area; not public postgres user area
  - [x] updated version of EER diagram and reduction to tables

- [ ] video demonstration (6 - 10 mins), show all required functions

- [ ] Phase3.zip (submission)
  - report.pdf
  - ERDiagram.pdf
  - Reduction.pdf
    > _above pdf must be in the root_
  - demo.mov (other movie files are fine)
  - src.zip
