# TODO based on phase 3 requirement

- [x] revise phase 2

- [x] design of overall database/project structure

- [x] sql script (as external file to implement a single function)

  - [x] Create table
  - [x] insert sample sql for test table function
    - [x] 3-9 insertion of each table
    - [x] 2-5 queries of each table

  - [ ] deploy to database

- [ ] application (interface based on requirement using sql function)

  For each user

  - [ ] create new accounts (create sql)

    - [ ] valid input
      - [ ] if username exist in db: get the sql error message / check the db firstly
      - [ ] if email has '@'
        - [Check if email address valid or not in Python](https://www.geeksforgeeks.org/check-if-email-address-valid-or-not-in-python/)
      - [ ] password, first/last_name if empty

  - [ ] Access via login

    - [ ] valid username (if exist in db)
    - [ ] valid password

  - [x] record date and time of both above activity (automatically added when insert into db)

  - [ ] create collections of music (create)
  - [ ] modify collection (alter, drop)
    - [ ] change name
    - [ ] delete the entire collection
  - [ ] query/read list of collections (select)
  - [ ] add/delete albums, songs from collection (insert, drop)

  - [ ] search song / show resulting list (select)
  - [ ] listen to song (select)

    - [ ] maybe make a timer
    - type
      - [ ] individually
      - [ ] entire collection (list)
    - [ ] mark played and not played
    - show current play status

  - [ ] follow/unfollow friend
    - [ ] check username at table account
    - [ ] check following/follows at Follows table
    - [ ] drop / insert
  - [ ] search for new friends by email

- [ ] insert enough dataset for each table

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
