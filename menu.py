from db import DB
from NHL_scraper import NHLScraper
from NBA_scraper import NBAScraper
from NFL_scraper import NFLScraper
from nba_db import NbaDb


def start_up(run=True):
    if run:
        print('Welcome! What would you like to do? \n1: update stats \n2: search stats\n3: Quit\n5: NBA Correlations\n6: '
              'Player Usage Stats\n7: DvP Report\n8: Per Game Stats')
        task = int(input())
        main_task(task)


def main_task(task):
    if task == 1:
        print('What Database Would You Like to Update?\n1: NBA\n2: NHL\n3: Back\n4: Quit')
        choice = int(input())
        if choice == 3:
            start_up()
        elif choice == 4:
            start_up(False)
        else:
            sport_select(choice)
    elif task == 2:
        print('Would You Like to Use the Helper?\n1: Query Helper\n2: Manual\n3: Back\n4: Quit')
        select = int(input())
        if select == 3:
            start_up()
        elif select == 4:
            start_up(False)
        else:
            print('1: NBA\n2: NHL\n3: Back')
            x = int(input())
            if x == 3:
                main_task(2)
            elif x == 1 or x == 2:
                query(select, x)
    elif task == 3:
        start_up(False)
    elif task == 4:
        nhlPA = DB()
        nhlPA.match()
    elif task == 5:
        nbaCorr = NbaDb()
        nbaCorr.correlation()
    elif task == 6:
        nbaScrape = NBAScraper()
        nbaScrape.scrape_pbp('PBP')
    elif task == 7:
        nbadvp = NbaDb()
        nbadvp.dvp()
    elif task == 8:
        nbaScrape = NBAScraper()
        nbaScrape.scrape_perGame('perGame')


def sport_select(sport):
    if sport == 1:
        nbaScrape = NBAScraper()
        print('What Day(s) Would You Like Stats From? Ex: 2022-12-3')
        days = input()
        d = days.split()
        print("Default Table Name is PLAYER. If Would You Like to Rename This, Please Enter New Name. Otherwise "
              "Leave Blank.")
        tbl = input()
        if len(tbl) > 0:
            name = tbl.upper()
        else:
            name = 'PLAYER'
        print("Would You Like to Export a Summary of DFS Points to CSV? Y/N")
        export = input().upper()
        if export == 'N':
            exp = False
        else:
            exp = True
        nbaScrape.scrape(d, name, exp)
    elif sport == 2:
        nhlScrape = NHLScraper()
        print('What Day(s) Would You Like Stats From? Ex: 2022-12-3')
        days = input()
        d = days.split()
        print("Default Table Name is SKATERS. If Would You Like to Rename This, Please Enter New Name. Otherwise "
              "Leave Blank.")
        tblS = input()
        if len(tblS) > 0:
            Sname = tblS.upper()
        else:
            Sname = 'SKATERS'
        print("Default Table Name is GOALIES. If Would You Like to Rename This, Please Enter New Name. Otherwise "
              "Leave Blank.")
        tblG = input()
        if len(tblG) > 0:
            Gname = tblG.upper()
        else:
            Gname = 'GOALIES'
        print("Would You Like to Export a Summary of DFS Points to CSV? Y/N")
        export = input().upper()
        if export == 'N':
            exp = False
        else:
            exp = True
        nhlScrape.scrape(d, Sname, Gname, exp)
    start_up()


def query(choice, sport):
    nba = DB()
    nhl = DB()
    if choice == 1:
        print('What Column Would you Like?')
        y = input()
        print('From Which Table?')
        z = input()
        print('Any Conditions? If none, enter None\nEx: team=\'PHI\', pts > 5')
        cond = input()
        if cond == 'None' or cond == 'none':
            cond = None
        else:
            cond = cond.split(",")
        if sport == 1:
            nba.helper('NBA', y, z.upper(), cond)
        elif sport == 2:
            nhl.helper('NHL', y, z.upper(), cond)
        elif sport == 3:
            pass
        elif sport == 4:
            pass
    elif choice == 2:
        print('Enter SQL Query')
        manual_query = input()
        if sport == 1:
            nba.manual('NBA', manual_query)
        elif sport == 2:
            nhl.manual('NHL', manual_query)
    elif choice == 3:
        main_task(1)
    elif choice == 4:
        start_up(False)
