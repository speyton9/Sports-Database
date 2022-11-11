import default_values
from db import DB
import pandas as pd
import statistics as stat
from statistics import mean
import sqlite3 as sl

# Connects to DB
con = sl.connect(default_values.nba_db_connection)


class NbaDb(DB):
    def __init__(self, col='', tbl='', cons=None):
        super().__init__(
            col, tbl, cons
        )

    # Creates new Table if it doesn't exist
    def default(self, table='PLAYER'):
        with con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {table} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Day text,
                    Name text,
                    Team text,
                    Opp text,
                    Home text,
                    Dec text,
                    MP text,
                    FG int,
                    FGa int,
                    FGp float,
                    TPT int,
                    TPTa int,
                    TPTp float,
                    FT int,
                    FTa int,
                    FTp float,
                    oRbd int,
                    dRbd int,
                    Rbd int,
                    Assist int,
                    Steal int,
                    Block int,
                    Turn int,
                    PF int,
                    Pts int,
                    FP float,
                    DK float
                );
            """)
        print('Table ' + table + ' Ready')

    # Inputs values from NBA_scraper into DB
    def input_values(self, day, name, team, opp, home, dec, mp, fg, fgAtt, fgp, three, threeAtt, threep, ft, ftAtt,
                     ftp, oRbd, dRbd, rbd, ast, stl, blk, to, pf, pts, fp, dk, table):

        sql = f'INSERT INTO {table} (Day, Name, Team, Opp, Home, Dec, MP, FG, FGa, FGp, TPT, TPTa, TPTp, FT, ' \
              'FTa, FTp, oRbd, dRbd, Rbd, Assist, Steal, Block, Turn, PF, Pts, FP, DK) values(?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

        data = [(day, name, team, opp, home, dec, mp, int(fg), int(fgAtt), float(fgp), int(three), int(threeAtt),
                 float(threep), int(ft), int(ftAtt),
                 float(ftp), int(oRbd), int(dRbd), int(rbd), int(ast), int(stl), int(blk), int(to), int(pf), int(pts),
                 float(fp), float(dk))]

        try:
            with con:
                con.executemany(sql, data)
        except Exception as e:
            print(e)

    # Creates summary of stats to be exported to CSV
    def summary(self, table='PLAYERS', export=True, dest=default_values.nba_export):
        players = []
        statlist = []

        # Creates List of unique players to loop through for later
        with con:
            data = con.execute(f'SELECT name FROM {table}')
            for row in data:
                if row[0] not in players:
                    players.append(row[0])
        i = 0
        # Query to make list of scores an minutes from each game played for current player in previous unique list
        while i < len(players):
            box = []
            with con:
                data = con.execute(f'SELECT fp FROM {table} WHERE name = "{players[i]}"')
            for row in data:
                box.append(float(row[0]))
            minutes = []
            with con:
                data = con.execute(f'SELECT mp FROM {table} WHERE name = "{players[i]}"')
            for row in data:
                x = row[0].split(':')
                conv = ((int(x[0]) * 60) + int(x[1])) / 60
                minutes.append(float(conv))
            # Places values in dictionary then a list
            try:
                stat_dict = {'Name': players[i], 'AvgFP': mean(box), 'StdFP': stat.stdev(box), 'AvgMin': mean(minutes), 'StdMin': stat.stdev(minutes)}
                statlist.append(stat_dict)
            except:
                stat_dict = {'Name': players[i], 'AvgFP': box[0], 'StdFP': 0, 'AvgMin': minutes[0], 'StdMin': 0}
                statlist.append(stat_dict)
            i += 1
        # Finally exports values to CSV
        if export:
            df = pd.DataFrame(statlist)
            df.to_csv(dest)
            print('NBA DB Updated\nResults exported to ' + dest + '\n|=================================|')
