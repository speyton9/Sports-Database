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
