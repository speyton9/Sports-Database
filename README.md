# Sports-Database
Make your own basic sports database using python, selenium, and sqlite3

Currently supports NBA and NHL.

I made this as a project to learn more about OOP, python, selenium, and SQL. While I made this with the novices in mind, it wouldn't hurt to learn more 
about SQL queries to get the most out of it.

To get started you need to install a few things:
  
  pip install selenium
  pip install statistics
  pip install pandas
  
Run the program from main.py and it will prompt the user for inputs.

Update stats:
  User chooses which sport, NBA or NHL, to update the database.
  User then enters what day or days in YYYY-MM-DD, no quotes needed. For specific days separate with a space (ie 2022-10-8 2022-11-2)
      You can also specify a range separated by ':' (ie 2022-10-7:2022-11-3). If there are no games for that date, they will be skipped.
      
Search stats currently has two options, Query Helper and Manual.
  Manual allows the user to enter full SQL queries and view the results.
  Helper is currently experimental. It works but is a little sensitive at the moment. I plan on working on this more to make it user friendly and add
  some pre-programmed queries that should be helpful.
