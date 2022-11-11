from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import default_values
import scraper
from nhl_db import NhlDb
from scraper import Scraper


class NHLScraper(Scraper):
    def __init__(self, to=25):
        super().__init__(
            to
        )

    def scrape(self, days: list, skate='SKATERS', goal='GOALIES', export=True, dest=default_values.nhl_export):

        timeout = self.time()

        driver = webdriver.Chrome()

        nhlDb = NhlDb()
        print('Preparing Table ' + skate)
        nhlDb.default_skaters(skate)
        print('Preparing Table ' + goal)
        nhlDb.default_goalies(goal)

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
            url = f"https://www.hockey-reference.com/friv/dailyleaders.fcgi?month={data[1]}&day={data[2]}&year={data[0]}&type=all"
            driver.get(url)
            element_present = EC.presence_of_element_located((By.XPATH, f'//*[@id="content"]/h1'))
            WebDriverWait(driver, timeout).until(element_present)
            # total skaters for day
            try:
                total = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters_sh"]/h2').text
                pull = total.split()
                print(total + ' for ' + day[i])
                j = int(pull[0])
            except:
                j = 0
                print('No Games Today')
            k = 0
            # get info for each skater
            while k < j:
                try:
                    name = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[1]/a').text
                    pos = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[2]').text
                    tm = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[3]').text
                    opp = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[5]').text
                    if driver.find_element(by=By.XPATH,
                                           value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[4]').text == '@':
                        home = opp
                    else:
                        home = tm
                    dec = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[6]').text
                    g = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[8]').text
                    a = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[9]').text
                    pts = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[10]').text
                    pm = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[11]').text
                    pim = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[12]').text
                    eG = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[13]').text
                    ppG = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[14]').text
                    shG = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[15]').text
                    gwg = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[16]').text
                    eA = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[17]').text
                    ppA = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[18]').text
                    shA = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[19]').text
                    shot = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[20]').text
                    shift = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[22]').text
                    toi = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[23]').text
                    hits = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[24]').text
                    blk = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[25]').text
                    fow = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[26]').text
                    fol = driver.find_element(by=By.XPATH, value=f'//*[@id="skaters"]/tbody/tr[{k + 1}]/td[27]').text
                    fp = (int(g) * 12) + (int(a) * 8) + (int(ppG) * .5) + (int(shG) * 2) + (int(ppA) * .5) + (
                            int(shA) * 2) + (int(shot) * 1.6) + (int(blk) * 1.6)
                    dkG = 0
                    dkS = 0
                    dkB = 0
                    dkP = 0
                    if int(g) > 2:
                        dkG = 3
                    if int(shot) > 4:
                        dkS = 3
                    if int(blk) > 2:
                        dkB = 3
                    if (int(g) + int(a)) > 2:
                        dkP = 3
                    dk = ((int(g) * 8.5) + (int(a) * 5) + (int(shG) * 2) + (int(shA) * 2) + (int(shot) * 1.5) +
                          (int(blk) * 1.3) + dkP + dkB + dkS + dkG)

                    # Sends data for specific skater on this date to be entered into DB
                    nhlDb.input_skaters(day[i], name, pos, tm, opp, home, dec, g, a, pts, pm, pim, eG, ppG, shG, gwg,
                                       eA, ppA, shA, shot, shift, toi, hits, blk, fow, fol, fp, dk, skate)
                    k += 1
                except:
                    # Site has sub headers every 15 or 20 rows, skips these and adds one to the loop total
                    j += 1
                    k += 1

            try:
                total = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies_sh"]/h2').text
                pull = total.split()
                p = int(pull[0])
                print(total + ' for ' + day[i])
            except:
                p = 0
            g = 0
            # get info for each goalie
            while g < p:
                try:
                    name = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[1]/a').text
                    pos = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[2]').text
                    tm = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[3]').text
                    opp = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[5]').text
                    if driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[4]').text == "@":
                        home = opp
                    else:
                        home = tm
                    dec = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[8]').text
                    ga = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[9]').text
                    sa = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[10]').text
                    sv = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[11]').text
                    svp = int(sv) / int(sa)
                    so = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[13]').text
                    toi = driver.find_element(by=By.XPATH, value=f'//*[@id="goalies"]/tbody/tr[{g + 1}]/td[17]').text
                    win = 0
                    if dec == 'W':
                        win = 12
                    fp = ((int(sv) * .8) - (int(ga) * 4) + (int(so) * 8) + win)
                    dkSV = 0
                    if int(sv) > 34:
                        dkSV = 3
                    dk = ((int(sv) * .7) - (int(ga) * 3.5) + (int(so) * 4) + (win / 2) + dkSV)

                    # Sends data for specific goalie on this date to be entered into DB
                    nhlDb.input_goalies(day[i], name, pos, tm, opp, home, dec, ga, sa, sv, svp, so, toi, fp, dk, goal)
                    g += 1
                except:
                    p += 1
                    g += 1
            i += 1

        # Exports summary of Fanduel Points to CSV
        if export:
            nhlDb.summary(skate, goal, export, dest)
        else:
            print('NHL DB Updated\n|=================================|')
