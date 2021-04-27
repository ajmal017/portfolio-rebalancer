import asyncio
# import util


import os
os.environ["DJANGO_SETTINGS_MODULE"] = "pv-rebalance.settings"
import django
django.setup()

from django.shortcuts import render
# from portfoliovisualizer.models import Target
from scraping_events.models import Target

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver import ActionChains
import time
import requests
import pickle
import pandas as pd
import json
import os
import logging
import re
import calendar
import datetime
from datetime import timedelta
import pandas_market_calendars as mcal
# from rebal.db import rowInsert, db_session
# from rebal.models import Targets
# from .data_utils import sendEmail, sendText


# strats = {
# "1" : "MovingAvg-A",
# "2" : "MovingAvg-B", 
# "3" : "Adaptive-C", 
# "4" : "Adaptive-D", 
# "5" : "Adaptive-E"
# }
##change 20210127
strats = {
"1" : ["MovingAvg-A", "AmthUPRO100"],
"2" : ["MovingAvg-B", "BmthSSOUBT5050"], 
"3" : ["Adaptive-C", "CwkTQQQTMF"],
"4" : ["Adaptive-D", "DwkQLDUBT"],
"5" : ["Adaptive-E", "EwkUPROTMF"]
}

log = logging.getLogger(__name__)



today = datetime.datetime.today()
nyse = mcal.get_calendar('NYSE')
days = nyse.valid_days(start_date=today, end_date=today + timedelta(days=60))

targets = []

class webDriver:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("enable-automation")
        self.options.add_argument("--disable-infobars")
        self.options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Firefox(executable_path=r'/home/abc/Downloads/geckodriver-v0.29.1-linux64/geckodriver')
        # self.driver = webdriver.Firefox(options=self.options)
        # self.driver = webdriver.Firefox(capabilities=firefox_capabilities)

class pvScraper(webDriver):
    def __init__(self):
        super().__init__()

    def getReports(self):
        log.info('PV signin')
        self.driver.get("https://www.portfoliovisualizer.com/login")
        elem=self.driver.find_element_by_css_selector('#username')
        elem.send_keys("burklindahl@yahoo.com")
        elem=self.driver.find_element_by_css_selector('#password')
        elem.send_keys("upwork1")
        elem.send_keys(Keys.RETURN)
        time.sleep(4)
        
        for i in range(1,6):
            report = str(i)

            # self.driver.get(f"https://www.portfoliovisualizer.com/manage-timing-models?action=open&type=timing&actionIndex={report}")
            self.driver.get(f"https://www.portfoliovisualizer.com/manage-timing-models?action=open&type=timing&name={strats[report][1]}") 

            time.sleep(3)   

            runTest = self.driver.find_element_by_css_selector('#submitButton').click()
            time.sleep(5)
            ##timing tab
            elems = self.driver.find_elements_by_css_selector('#tabs > li')
            for e in elems:
                if 'Periods' in e.text:
                    e.click()
            time.sleep(3)
            cells = self.driver.find_elements_by_css_selector('html body div.container-fluid div#result-content.tab-content div#timingPeriods.tab-pane.active table.table.table-striped.table-condensed.stickyHeaders tbody tr')

            rows = []
            # dfrows = []
            # for cell in cells:
            #     dfrows.append(cell.text.split())

            for cell in cells:
                rows.append(cell.text)    

            tickers = re.findall('\(([a-zA-Z]{3,4})\)', rows[0])
            tgts = re.findall('(\d{1,3}\.\d{1,2}%)', rows[0])   
            datesWeekly = re.findall(r'(\d{2}\/\d{2}\/\d{4})', rows[0])    
            datesMonthly = re.findall(r'([a-zA-z]{3}\s\d{4})', rows[0])    ##rows[-1])
            strategy = [ strats[report][0] for i in tickers] 

            if 'Moving' in strats[report][0]:
                date = datetime.datetime.strptime(datesMonthly[1], "%b %Y")
                tradeDate = getTradeDate(date, 'monthly')
                # print(date)

            if 'Adaptive' in strats[report][0]:
                date = datetime.datetime.strptime(datesWeekly[1], "%m/%d/%Y")
                tradeDate = getTradeDate(date, 'weekly')
                # print(periods)
                # print(date)


            tradeDates = [ tradeDate for i in tickers]

            zipper = list(zip(tickers,tgts,strategy,tradeDates)) 
            targets.append(zipper)

            # df = pd.DataFrame(dfrows)
            # df.to_csv(f'testweights_{report}.csv')      

        flat_list = [item for sublist in targets for item in sublist]

        df=pd.DataFrame(flat_list, columns = ['ticker', 'target', 'strategy', 'date'])
        # df.to_csv('weights.csv')
        # df.to_pickle("scrape.pkl")

        targetArray = []
        # deleted_objects = Targets.__table__.delete()
        # db_session.execute(deleted_objects)
        # db_session.commit()
        for row in df.itertuples():
            targetArray.append({'ticker': row.ticker, #datetime.strptime(row.startDate, '%m/%d/%Y %H:%M:%S'),
                                'target': row.target,
                                'strategy': row.strategy,
                                'date': row.date
                                })
        # rowInsert(Targets, targetArray, 'scraper')
        for target in targetArray:
        	Target.objects.create(**target)

        # sendEmail("Target weights", True, df.to_html(), "Target Scrape")
        # sendText("Scraper successfull.")


        self.driver.quit()


def getTradeDate(date, strategy):

    if strategy == 'monthly':
        lastTradingDay = datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month)[1])
        while lastTradingDay.weekday() > 4:
            lastTradingDay = lastTradingDay - timedelta(days=1)
    
    if strategy == 'weekly':
        lastTradingDay = date
        while lastTradingDay.weekday() > 4:
            lastTradingDay = lastTradingDay + timedelta(days=1)        

    dt = datetime.datetime(
        year=lastTradingDay.year, 
        month=lastTradingDay.month,
        day=lastTradingDay.day,
        )

    while dt not in days:
        if strategy =='weekly':
            dt = dt + timedelta(days=1)
        else:
            dt = dt - timedelta(days=1)
    return dt


pv = pvScraper()
pv.getReports()