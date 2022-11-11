import pandas as pd
import statistics as stat
from statistics import mean
import default_values
from db import DB
import sqlite3 as sl

# Connects to DB
con = sl.connect(default_values.nhl_db_connection)


class NhlDb(DB):
    def __init__(self, col='', tbl='', cons=None):
        super().__init__(
            col, tbl, cons
        )

    # Creates new Table if it doesn't exist
    def default_skaters(self, name='SKATERS'):
        with con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Day text,
                    Name text,
                    Pos text,
                    Team text,
                    Opp text,
                    Home text,
                    Dec text,
                    Goals text,
                    Assists int,
                    Pts int,
                    Plus int,
                    PIM int,
                    evG int,
                    ppG int,
                    shG int,
                    gwg int,
                    evA int,
                    ppA int,
                    shA int,
                    Shots int,
                    Shifts int,
                    TOI TEXT,
                    Hits int,
                    Blocks int,
                    FOW int,
                    FOL int,
                    FP float,
                    DK float
                );
            """)
        print('Table ' + name + ' Ready')

    # Inputs values from NHL_scraper into DB
    def input_skaters(self, day, name, pos, tm, opp, home, dec, g, a, pts, pm, pim, eG, ppG, shG, gwg,
                                       eA, ppA, shA, shot, shift, toi, hits, blk, fow, fol, fp, dk, table):

        sql = f'INSERT INTO {table} (Day, Name, Pos, Team, Opp, Home, Dec, Goals, Assists, Pts, Plus, PIM, evG, ppG, ' \
              'shG, gwg, evA, ppA, shA, Shots, Shifts, TOI, Hits, Blocks, FOW, FOL, FP, DK) values(?, ?, ?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        data = [(day, name, pos, tm, opp, home, dec, int(g), int(a), int(pts), int(pm), int(pim), int(eG), int(ppG),
                 int(shG), int(gwg), int(eA), int(ppA), int(shA), int(shot), int(shift), toi, int(hits), int(blk),
                 int(fow), int(fol), float(fp), float(dk))]
        val = 1
        try:
            with con:
                con.executemany(sql, data)
                val += 1
        except Exception as e:
            print(e)

    # Creates new Table if it doesn't exist
    def default_goalies(self, name='GOALIES'):
        with con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {name} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Day text,
                    Name text,
                    Pos text,
                    Team text,
                    Opp text,
                    Home text,
                    Dec text,
                    GA int,
                    Shots int,
                    Saves int,
                    SaveP float,
                    SO int,
                    TOI text,
                    FP float,
                    DK float
                );
            """)
        print('Table ' + name + ' Ready')

    # Inputs values from NHL_scraper into DB
    def input_goalies(self, day, name, pos, tm, opp, home, dec, ga, sa, sv, svp, so, toi, fp, dk, table):

        sql = f'INSERT INTO {table} (Day, Name, Pos, Team, Opp, Home, Dec, GA, Shots, Saves, SaveP, SO, TOI, ' \
              'FP, DK) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        data = [(day, name, pos, tm, opp, home, dec, int(ga), int(sa), int(sv), float(svp), int(so), toi, float(fp),
                 float(dk))]

        try:
            with con:
                con.executemany(sql, data)
        except Exception as e:
            print(e)

    # Creates summary of stats to be exported to CSV
    def summary(self, Stbl='SKATERS', Gtbl='GOALIES', export=True, dest=default_values.nhl_export):
        skaters = []
        statlist = []
        # Creates List of unique skaters and team to loop through for later
        with con:
            data = con.execute(f'SELECT name, team FROM {Stbl}')
            for row in data:
                if row not in skaters:
                    skaters.append(row)
        i = 0
        # Query to make list of scores from each game played for current player in previous unique list
        while i < len(skaters):
            box = []
            with con:
                data = con.execute(f'SELECT fp FROM {Stbl} WHERE (name = "{skaters[i][0]}" AND team = "{skaters[i][1]}")')
            for row in data:
                box.append(float(row[0]))
            # Places values in dictionary then a list
            try:
                stat_dict = {'Name': skaters[i][0], 'Team': skaters[i][1], 'Avg': mean(box), 'StD': stat.stdev(box)}
                statlist.append(stat_dict)
            except:
                stat_dict = {'Name': skaters[i][0], 'Team': skaters[i][1], 'Avg': box[0], 'StD': 0}
                statlist.append(stat_dict)
            i += 1
        goalies = []
        # Creates List of unique goalies to loop through for later
        with con:
            data = con.execute(f'SELECT name, team FROM {Gtbl}')
            for row in data:
                if row not in goalies:
                    goalies.append(row)
        i = 0
        # Query to make list of scores from each game played for current player in previous unique list
        while i < len(goalies):
            box = []
            with con:
                data = con.execute(f'SELECT fp FROM {Gtbl} WHERE (name = "{goalies[i][0]}" AND team = "{goalies[i][1]}")')
            for row in data:
                box.append(float(row[0]))
            # Places values in dictionary then a list
            try:
                stat_dict = {'Name': goalies[i][0], 'Team': goalies[i][1], 'Avg': mean(box), 'StD': stat.stdev(box)}
                statlist.append(stat_dict)
            except:
                stat_dict = {'Name': goalies[i][0], 'Team': goalies[i][1], 'Avg': box[0], 'StD': 0}
                statlist.append(stat_dict)
            i += 1
        # Finally exports values to CSV
        if export:
            df = pd.DataFrame(statlist)
            df.to_csv(dest)
            print('NHL DB Updated\nResults exported to ' + dest + '\n|=================================|')



