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
    def summary(self, table='PLAYER', export=True, dest=default_values.nba_export):
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
            fppm = []
            with con:
                data = con.execute(f'SELECT mp, fp FROM {table} WHERE name = "{players[i]}"')
            for row in data:
                x = row[0].split(':')
                conv = ((int(x[0]) * 60) + int(x[1])) / 60
                y = [conv, float(row[1])]
                fppm.append(y)
            try:
                mn = mean(minutes)
            except:
                mn = minutes[0]
            try:
                dev = stat.stdev(minutes)
            except:
                dev = 0
            below = []
            above = []
            avg = []
            aboveMin = []
            for row in fppm:
                avg.append(row[1])
                if row[0] < mn - dev:
                    below.append(row[1])
                elif row[0] > mn + dev:
                    above.append(row[1])
                    aboveMin.append(row[0])
                # elif mn - dev < row[0] < mn + dev:
                # avg.append(row[1])
            try:
                avgFP = mean(avg)
            except:
                avgFP = 0
            try:
                stdFp = stat.stdev(avg)
            except:
                stdFp = 0
            try:
                avgMin = mean(minutes)
            except:
                avgMin = minutes[0]
            try:
                stdMin = stat.stdev(minutes)
            except:
                stdMin = 0
            try:
                blw = mean(below)
            except:
                blw = 0
            try:
                stdBlw = stat.stdev(below)
            except:
                stdBlw = 0
            try:
                abv = mean(above)
            except:
                abv = 0
            try:
                stdAbv = stat.stdev(above)
            except:
                stdAbv = 0
            try:
                abvMin = mean(aboveMin)
            except:
                abvMin = 0

            # Places values in dictionary then a list
            stat_dict = {'Name': players[i], 'AvgFP': avgFP, 'StdFP': stdFp, 'AvgMin': avgMin, 'StdMin': stdMin,
                         'BelowFP': blw, 'StdBlw': stdBlw, 'AboveFP': abv, 'StdAbv': stdAbv, 'AbvMin': abvMin}
            statlist.append(stat_dict)
            i += 1
        # Finally exports values to CSV
        if export:
            df = pd.DataFrame(statlist)
            df.to_csv(dest)
            print('NBA DB Updated\nResults exported to ' + dest + '\n|=================================|')

    # Correlation
    def correlation(self, table='PLAYER'):
        tms = []
        statlist = []
        with con:
            data = con.execute(f"SELECT DISTINCT team FROM PLAYER")
        for row in data:
            if row[0] not in tms:
                tms.append(row[0])
        for tm in tms:
            players = []
            days = []
            with con:
                data = con.execute(f"SELECT day FROM PLAYER WHERE (team = '{tm}' AND name IN (SELECT name FROM perGame WHERE (mp > 14)))")
            for row in data:
                if row[0] not in days:
                    days.append(row[0])
            with con:
                data = con.execute(f"SELECT name FROM PLAYER WHERE (team = '{tm}' AND name IN (SELECT name FROM perGame WHERE (mp > 14)))")
            for row in data:
                if row[0] not in players:
                    players.append(row[0])
            df = pd.DataFrame(index=days, columns=players)
            # SQL to get player list > 30mpg ---- SELECT name, fp FROM PLAYER WHERE name IN (SELECT name FROM perGame WHERE (mp > 30))
            i = 0
            while i < len(days):
                j = 0
                while j < len(players):
                    box = []
                    with con:
                        data = con.execute(f'SELECT fp FROM PLAYER WHERE (name = "{players[j]}" AND day = "{days[i]}")')
                    for row in data:
                        box.append(row[0])
                    try:
                        df.iloc[i, j] = float(box[0])
                    except:
                        pass
                    j += 1
                i += 1
            i = 0
            while i < (len(players)):
                j = i + 1
                while j < len(players):
                    if i == j:
                        pass
                    else:
                        pA = []
                        pB = []
                        daysBoth = []
                        with con:
                            data = con.execute(f'SELECT day FROM PLAYER WHERE name = "{players[i]}"')
                        for row in data:
                            pA.append(row[0])
                        with con:
                            data = con.execute(f'SELECT day FROM PLAYER WHERE name = "{players[j]}"')
                        for row in data:
                            pB.append(row[0])
                        count = 0
                        k = 0
                        while k < len(pA):
                            if pA[k] in pB:
                                count += 1
                                daysBoth.append(pA[k])
                            k += 1
                        mpA = 0
                        mpB = 0
                        with con:
                            k = 0
                            while k < len(daysBoth):
                                data = con.execute(
                                    f'SELECT mp FROM PLAYER WHERE (name = "{players[i]}" AND day = "{daysBoth[k]}")')
                                for row in data:
                                    x = row[0].split(':')
                                    y = (int(x[0] * 60) + int(x[1])) / 60
                                    mpA += y
                                k += 1
                        with con:
                            k = 0
                            while k < len(daysBoth):
                                data = con.execute(
                                    f'SELECT mp FROM PLAYER WHERE (name = "{players[j]}" AND day = "{daysBoth[k]}")')
                                for row in data:
                                    x = row[0].split(':')
                                    y = (int(x[0] * 60) + int(x[1])) / 60
                                    mpB += y
                                k += 1
                        if count > 8:
                            x = df[players[i]].astype(float).corr(df[players[j]].astype(float))
                            if x <= -.3:
                                player_corr = {'Combo': players[i] + "&" + players[j], 'Correlation': x}
                                statlist.append(player_corr)
                    j += 1
                i += 1
        df2 = pd.DataFrame(statlist)
        df2.to_csv(f'C:\\Users\\Steven\\Desktop\\NBAcorrelation.csv')
        print('Done')

    def pbp(self, tbl='PBP'):

        with con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {tbl} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Name text,
                    Pos text,
                    Age int,
                    Team text,
                    GP int,
                    MP float,
                    PG float,
                    SG float,
                    SF float,
                    PF float,
                    C float
                );
            """)
        print('Table ' + tbl + ' Ready')

    def input_pbp(self, name, pos, age, tm, games, mp, pg, sg, sf, pf, c, tbl):
        sql = 'INSERT INTO PBP (Name, Pos, Age, Team, GP, MP, PG, SG, SF, PF, C) values(?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?, ?)'

        data = [(name, pos, int(age), tm, int(games), float(mp), float(pg), float(sg), float(sf), float(pf), float(c))]
        try:
            with con:
                con.executemany(sql, data)
        except Exception as e:
            print(e)

    def dvp(self):
        teams = []
        with con:
            data = con.execute('SELECT DISTINCT team FROM PLAYER')
        for row in data:
            teams.append(row[0])
        with con:
            dat = con.execute('SELECT PLAYER.name, PLAYER.fp, PBP.pos, PLAYER.opp FROM PLAYER JOIN PBP ON '
                              'PLAYER.name=PBP.name;')
        pg = []
        sg = []
        sf = []
        pf = []
        c = []
        for row in dat:
            if row[2] == 'PG':
                pg.append((row[1], row[3]))
            elif row[2] == 'SG':
                sg.append((row[1], row[3]))
            elif row[2] == 'SF':
                sf.append((row[1], row[3]))
            elif row[2] == 'PF':
                pf.append((row[1], row[3]))
            elif row[2] == 'C':
                c.append((row[1], row[3]))

        positions = ['PG', 'SG', 'SF', 'PF', 'C']

        df = pd.DataFrame(index=teams, columns=positions)
        i = 0
        while i < len(teams):
            tpg = []
            tsg = []
            tsf = []
            tpf = []
            tc = []
            j = 0
            while j < len(pg):
                if pg[j][1] == teams[i]:
                    tpg.append((pg[j][0]))
                j += 1
            j = 0
            while j < len(sg):
                if sg[j][1] == teams[i]:
                    tsg.append(float(sg[j][0]))
                j += 1
            j = 0
            while j < len(sf):
                if sf[j][1] == teams[i]:
                    tsf.append(float(sf[j][0]))
                j += 1
            j = 0
            while j < len(pf):
                if pf[j][1] == teams[i]:
                    tpf.append(float(pf[j][0]))
                j += 1
            j = 0
            while j < len(c):
                if c[j][1] == teams[i]:
                    tc.append(float(c[j][0]))
                j += 1
            df.iloc[i, 0] = float(sum(tpg))
            df.iloc[i, 1] = float(sum(tsg))
            df.iloc[i, 2] = float(sum(tsf))
            df.iloc[i, 3] = float(sum(tpf))
            df.iloc[i, 4] = float(sum(tc))
            i += 1
        print(df)

    def perGame(self, tbl='perGame'):

        with con:
            con.execute(f"""
                CREATE TABLE IF NOT EXISTS {tbl} (
                    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                    Name text,
                    MP float,
                    FG float,
                    Three float,
                    Two float,
                    FT float,
                    RBD float,
                    Assists float,
                    Steals float,
                    Blocks float,
                    GA float,
                    PF float
                );
            """)
        print('Table ' + tbl + ' Ready')

    def input_perGame(self, name, mp, fg, three, two, ft, rbd, ast, stl, blk, to, pf):

        sql = 'INSERT INTO perGame (Name, MP, FG, Three, Two, FT, RBD, Assists, Steals, Blocks, GA, PF) values(?, ?, ?, ?, ' \
              '?, ?, ?, ?, ?, ?, ?, ?)'

        data = [(name, float(mp), float(fg), float(three), float(two), float(ft), float(rbd), float(ast), float(stl), float(blk), float(to), float(pf))]
        try:
            with con:
                con.executemany(sql, data)
        except Exception as e:
            print(e)
