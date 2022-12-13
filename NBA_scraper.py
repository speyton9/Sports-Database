from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import default_values
import scraper
from nba_db import NbaDb
from scraper import Scraper


class NBAScraper(Scraper):
    def __init__(self, to=25):
        super().__init__(
            to
        )

    def scrape(self, days: list, table='PLAYER', export=True, dest=default_values.nba_export):

        timeout = self.time()

        driver = webdriver.Chrome()
        print('Preparing Table ' + table)
        nbaDb = NbaDb()
        nbaDb.default(table)

        # Determines if days given are individual dates or a range
        if days[0].find(':') > 0:
            day = scraper.date_range(days)
        else:
            day = days

        print('Retrieving Stats for day(s)')
        print(day)

        i = 0
        while i < len(day):
            data = day[i].split("-")
            # Open URL with current date in list
            url = f"https://www.basketball-reference.com/friv/dailyleaders.fcgi?month={data[1]}&day={data[2]}&" \
                  f"year={data[0]}&type=all"
            driver.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/h1'))
            WebDriverWait(driver, timeout).until(element_present)
            # total players for day
            try:
                total = driver.find_element(by=By.XPATH, value=f'//*[@id="stats_sh"]/h2').text
                pull = total.split()
                print(total + ' for ' + day[i])
                j = int(pull[0])
            except:
                j = 0
                print('No Games Today')
            k = 0
            # get info for each player
            while k < j:
                try:
                    name = driver.find_element(by=By.XPATH,
                                               value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[1]/a').text
                    team = driver.find_element(by=By.XPATH,
                                               value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[2]').text
                    opp = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[4]').text
                    if driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[3]').text == '@':
                        home = opp
                    else:
                        home = team
                    dec = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[5]').text
                    mp = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[6]').text
                    fg = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[7]').text
                    fgAtt = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[8]').text
                    try:
                        fgp = int(fg) / int(fgAtt)
                    except:
                        fgp = 0.0
                    three = driver.find_element(by=By.XPATH,
                                                value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[10]').text
                    threeAtt = driver.find_element(by=By.XPATH,
                                                   value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[11]').text
                    try:
                        threep = int(three) / int(threeAtt)
                    except:
                        threep = 0.0
                    ft = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[13]').text
                    ftAtt = driver.find_element(by=By.XPATH,
                                                value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[14]').text
                    try:
                        ftp = int(ft) / int(ftAtt)
                    except:
                        ftp = 0.0
                    oRbd = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[16]').text
                    dRbd = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[17]').text
                    ast = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[19]').text
                    stl = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[20]').text
                    blk = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[21]').text
                    to = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[22]').text
                    pf = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[23]').text
                    pts = driver.find_element(by=By.XPATH, value=f'//*[@id="stats"]/tbody/tr[{k + 1}]/td[24]').text
                    rbd = int(oRbd) + int(dRbd)
                    doubles = 0
                    if int(pts) > 9:
                        doubles += 1
                    if int(rbd) > 9:
                        doubles += 1
                    if int(ast) > 9:
                        doubles += 1
                    if int(blk) > 9:
                        doubles += 1
                    if int(stl) > 9:
                        doubles += 1
                    fp = (int(three) + (int(ast) * 1.5) + (int(blk) * 3) + (int(fg) * 2) + (int(rbd) * 1.2) + int(
                        ft) +
                          (int(stl) * 3) - int(to))
                    if doubles > 2:
                        bonus = 3
                    elif doubles == 2:
                        bonus = 1.5
                    else:
                        bonus = 0
                    dk = (int(pts) + (int(three) * .5) + (int(rbd) * 1.25) + (int(ast) * 1.5) + (int(stl) * 2) +
                          (int(blk) * 2) - (int(to) * .5) + bonus)

                    # Sends data for specific player on this date to be entered into DB
                    nbaDb.input_values(day[i], name, team, opp, home, dec, mp, fg, fgAtt, fgp, three, threeAtt,
                                       threep, ft, ftAtt, ftp, oRbd, dRbd, rbd, ast, stl, blk, to, pf, pts, fp, dk, table)
                    k += 1
                except:
                    # Site has sub headers every 15 or 20 rows, skips these and adds one to the loop total
                    j += 1
                    k += 1
            i += 1

        # Exports summary of Fanduel Points to CSV
        if export:
            nbaDb.summary(table, export, dest)
        else:
            print('NBA DB Updated\n|=================================|')

    def scrape_pbp(self, tbl='PBP'):

        timeout = self.time()

        driver = webdriver.Chrome()
        print('Preparing Table ' + tbl)
        nbaDb1 = NbaDb()
        nbaDb1.pbp(tbl)
        url = f"https://www.basketball-reference.com/leagues/NBA_2023_play-by-play.html"
        driver.get(url)
        element_present = EC.presence_of_element_located((By.XPATH, f'//*[@id="pbp_stats_sh"]/h2'))
        WebDriverWait(driver, timeout).until(element_present)
        table = driver.find_element(by=By.XPATH, value='//*[@id="pbp_stats"]/tbody')
        rows = table.find_elements(by=By.XPATH, value='//*[@id="pbp_stats"]/tbody/tr')
        players = len(rows)

        i = 0
        while i < players:
            try:
                name = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="pbp_stats"]/tbody/tr[{i+1}]/td[1]/a').text
                pos = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="pbp_stats"]/tbody/tr[{i+1}]/td[2]').text
                age = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="pbp_stats"]/tbody/tr[{i+1}]/td[3]').text
                tm = driver.find_element(by=By.XPATH,
                                          value=f'//*[@id="pbp_stats"]/tbody/tr[{i+1}]/td[4]/a').text
                games = driver.find_element(by=By.XPATH,
                                          value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[5]').text
                mp = driver.find_element(by=By.XPATH,
                                            value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[6]').text
                pg = driver.find_element(by=By.XPATH,
                                            value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[7]').text
                sg = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[8]').text
                sf = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[9]').text
                pf = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[10]').text
                c = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="pbp_stats"]/tbody/tr[{i + 1}]/td[11]').text
                if pg == '':
                    pg = 0.0
                else:
                    pg = float(pg.replace('%', '')) / 100
                if sg == '':
                    sg = 0.0
                else:
                    sg = float(sg.replace('%', '')) / 100
                if sf == '':
                    sf = 0.0
                else:
                    sf = float(sf.replace('%', '')) / 100
                if pf == '':
                    pf = 0.0
                else:
                    pf = float(pf.replace('%', '')) / 100
                if c == '':
                    c = 0.0
                else:
                    c = float(c.replace('%', '')) / 100

                nbaDb1.input_pbp(name, pos, age, tm, games, mp, pg, sg, sf, pf, c, table)

            except:
                pass
            i += 1

        print("PBP Updated")

    def scrape_perGame(self, tbl='perGame'):

        timeout = self.time()

        driver = webdriver.Chrome()
        print('Preparing Table ' + tbl)
        nbaDb1 = NbaDb()
        nbaDb1.perGame(tbl)
        url = f"https://www.basketball-reference.com/leagues/NBA_2023_per_game.html"
        driver.get(url)
        element_present = EC.presence_of_element_located((By.XPATH, f'//*[@id="meta"]/div[2]/h1/span[3]'))
        WebDriverWait(driver, timeout).until(element_present)
        table = driver.find_element(by=By.XPATH, value='//*[@id="per_game_stats"]/tbody')
        rows = table.find_elements(by=By.XPATH, value='//*[@id="per_game_stats"]/tbody/tr')
        players = len(rows)

        i = 0
        while i < players:
            try:
                name = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[1]/a').text
                mp = driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[7]').text
                fg = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[8]').text
                three = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[11]').text
                two = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[14]').text
                ft = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[18]').text
                rbd = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[23]').text
                ast = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[24]').text
                stl = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[25]').text
                blk = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[26]').text
                to = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[27]').text
                pf = driver.find_element(by=By.XPATH,
                                         value=f'//*[@id="per_game_stats"]/tbody/tr[{i + 1}]/td[28]').text
                if mp == "":
                    mp = 0
                if fg == "":
                    fg = 0
                if three == "":
                    three = 0
                if two == "":
                    two = 0
                if ft == "":
                    ft = 0
                if rbd == "":
                    rbd = 0
                if ast == "":
                    ast = 0
                if stl == "":
                    stl = 0
                if blk == "":
                    blk = 0
                if to == "":
                    to = 0
                if pf == "":
                    pf = 0

                nbaDb1.input_perGame(name, mp, fg, three, two, ft, rbd, ast, stl, blk, to, pf)
            except:
                pass
                print('pass' + str(i))
            i += 1

        print("perGame Updated")
