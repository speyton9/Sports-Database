import sqlite3 as sl
import default_values


class DB:

    def __init__(self, col='', tbl='', cons=None):
        if cons is None:
            cons = []
        self.col = col
        self.tbl = tbl
        self.cons = cons

    # Experimental - if conds (conditions) param in helper is present, attempts to split and add to function
    def __craft(self, lst):
        print(len(lst))
        if len(lst) > 1:
            x = 'WHERE ' + ' AND '.join(lst)
            print(x)
            return x
        else:
            x = 'WHERE ' + lst[0]
            return x

    # Experimental - Attempts to get parameters from user input to create queries
    def helper(self, sport, col, tbl, conds):
        if sport == 'NBA':
            con = sl.connect(default_values.nba_db_connection)
        elif sport == 'NHL':
            con = sl.connect(default_values.nhl_db_connection)

        if conds is None:
            with con:
                data = con.execute(f"SELECT {col} FROM {tbl}")
                for row in data:
                    print(row)
        else:
            with con:
                data = con.execute(f"SELECT {col} FROM {tbl} {self.__craft(conds)}")
                for row in data:
                    print(row)

    # Allows user to enter queries manually
    def manual(self, sport, statement):
        if sport == 'NBA':
            con = sl.connect(default_values.nba_db_connection)
        elif sport == 'NHL':
            con = sl.connect(default_values.nhl_db_connection)

        with con:
            data = con.execute(statement)
            for row in data:
                print(row)

    # Experimental - Lists unique days entered into DB. Helps identify missing values or where user last ran
    def list_days(self, sport, tbl):
        if sport == 'NBA':
            con = sl.connect(default_values.nba_db_connection)
        elif sport == 'NHL':
            con = sl.connect(default_values.nhl_db_connection)

        with con:
            data = con.execute(f'SELECT DISTINCT day FROM {tbl}')
            for row in data:
                print(row[0])
