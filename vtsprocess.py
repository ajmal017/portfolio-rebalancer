import pandas as pd
import os
import smtplib
import imaplib
import email
import re
import sys
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import datetime
import logging
import time
import re
# from rebal.eoauth import OauthSession
# from rebal.orders import getPositions, getPrices, getPreviewIDs, sendOrders, getOrderDetails
# from rebal.models import vtsTarget, SecurityXref, vtsStrategy
#from rebal.db import rowInsert, init_db, db_session
# from scraper.data_utils import sendEmail, sendText
# from dotenv import load_dotenv, find_dotenv
# import math


# logging.basicConfig(filename='vtsprocess.log',format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', level=logging.INFO)

# ##etrade auth
# etradeAuth = OauthSession()
# etradeAuth.account_key='oyGfgHdr_IAh2Rt8XFgZOA'

# if etradeAuth.refresh():
#     etradeAuth.renew_auth_session()
# else:
#     etradeAuth.create_session()


# init_db()

# desktopPath = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# from io import StringIO
# from html.parser import HTMLParser

# load_dotenv(find_dotenv())


# try:
#     debug = sys.argv[1]
# except:
#     debug = 0

# debug=1

# today = datetime.date.today()


# def getTargets():
#     orders = []
#     tickers = []
#     try:
#         vtstrades = pd.read_sql(db_session.query(vtsTarget).statement,db_session.bind, index_col='id')

#         if len(vtstrades) > 0:
#             date = vtstrades['date'].values[0]
#             if date == today:
#                 for index, row in vtstrades.iterrows():
#                     orders.append({"ticker": row.ticker, "transactionType": row.transactionType})
#                     tickers.append(row.ticker)
#             else:
#                 orders, tickers = getEmailOrders()
#         else:
#             orders, tickers = getEmailOrders()
#     except Exception as e:
#         sendText("VTS Target failure - getTargets()")
#         logging.exception("error in getTargets()")

#     return orders, tickers

# class MLStripper(HTMLParser):
#     def __init__(self):
#         super().__init__()
#         self.reset()
#         self.strict = False
#         self.convert_charrefs= True
#         self.text = StringIO()
#     def handle_data(self, d):
#         self.text.write(d)
#     def get_data(self):
#         return self.text.getvalue()

# def strip_tags(html):
#     s = MLStripper()
#     s.feed(html)
#     return s.get_data()

def getEmailOrders():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('brlind999@gmail.com', 'WatermelonSugar999')
    mail.select("inbox") 
    # result, data = mail.search(None, '(FROM "volatilitytradingstrategies@hotmail.com" UNSEEN)' )
    result, data = mail.search(None, '(FROM "volatilitytradingstrategies@hotmail.com" SUBJECT "Backup - Daily Trade" UNSEEN)' )

    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string
    latest_email_id = id_list[-1] # get the latest
    result, data = mail.fetch(latest_email_id, "(RFC822)") 
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    msg = msg.get_payload(decode=True)
    msg = msg.decode()
    msg = strip_tags(msg)
    # print(msg.is_multipart())

    pattern = re.compile(r'\s\s+')
    msg = re.sub(pattern, '', msg)

    ##are there any trades today?
    trades = re.search(r'Section 3:.*(Total Portfolio Solution trades:\d)',msg).group(1)
    trades = int(trades.split(':')[1])
    orders = []
    tickers = []
    orderArray = []
    if trades > 0:

        try:
            matches = ['Balanced', 'strategy page']

            link = re.search(r'Section 3:.*trades:\d(.*)Section 4',msg).group(1)
            link = link.split('20%')

            for item in link:
                if all(x in item for x in matches):
                    if 'Required' in item:
                        instruction = item.split('Required')[1]
                        orders = instruction.split('/')
                    else:
                        logging.info("No VTS orders")

            if len(orders) > 0:
                for order in orders:
                    instructions = order.split(' ')
                    # tickers.append(instructions[1])
                    orderArray.append({"ticker": instructions[1], "transactionType": instructions[0]})

                ##security xref
                df = pd.DataFrame(orderArray)
                securityxref = pd.read_sql(db_session.query(SecurityXref).statement,db_session.bind, index_col='id')
                df = pd.merge(df, securityxref, how='left', on='ticker')
                df.loc[df.rebalTicker.isnull(), 'rebalTicker'] = df['ticker']
                df['ticker'] = df['rebalTicker']
                del df['rebalTicker']

                orderArray = df.to_dict('records') 
                tickers = df['ticker'].tolist()

        except:
            logging.exception("VTS Email Scrape Failed - orders exist but not captured.")
            sendEmail("VTS Email Scrape Failed - orders exist but not captured.", False)
            sendText("VTS Scrape Failed, please check email and rerun.")

    mail.close()
    return orderArray, tickers


# active = db_session.query(vtsStrategy).filter(vtsStrategy.strategy=='Daily-A').first()

# if active.strategy:
#     if debug == 1:
#         orderArray, tickers = getEmailOrders()    
#         if len(orderArray) > 0:
#             db_session.query(vtsTarget).delete()
#             db_session.commit()    
#             for array in orderArray:
#                 array['date'] = datetime.date.today()
#             rowInsert(vtsTarget, orderArray, 'vts')
#             df = pd.DataFrame(orderArray)
#             sendEmail("VTS Targets", True, df.to_html(), "VTS")
#             sendText("VTS targets successfully scraped - Please Authorize")
#         else:
#             db_session.query(vtsTarget).delete()
#             db_session.commit()
#             db_session.close()
#             sendEmail("VTS - No Targets Today.", True, subjectText="VTS")
#             sendText("No VTS targets today.")

#     else:
#         try:
#             orderArray, tickers = getTargets()
#             if len(orderArray)>0:
#                 # print(orderArray, tickers)
#                 tickers = ','.join(tickers)
#                 positions = getPositions(etradeAuth)
#                 prices = getPrices(tickers, etradeAuth)
#                 SLticker = None
#                 cashAmountBY = None
#                 Loop = True
#                 ##get SL order
#                 indexSL = next(index for index, dictionary in enumerate(orderArray)
#                     if dictionary['transactionType'] == 'Sell')
#                 symbolSL = orderArray[indexSL]['ticker']
#                 symbolBY = orderArray[1-indexSL]['ticker']

#                 orderArray[indexSL]['quantity'] = positions[symbolSL]
#                 orderArray[indexSL]['symbol'] = symbolSL
#                 orderArray[indexSL]['transactionType'] = 'SL'
#                 cashAmountBY = (positions[symbolSL] * prices[symbolSL])

#                 prevIds = getPreviewIDs([orderArray[indexSL]], etradeAuth, process='vts')
#                 orderIds = sendOrders(prevIds, 'vts', etradeAuth)   
#                 sendText("VTS SL order submitted.")
#                 orderIdSL = orderIds[0]
#                 logging.info(f"SL orderId: {orderIds[0]}")
                
#                 ##check open orders
#                 status = getOrderDetails(etradeAuth, orderID=orderIdSL)
#                 openTry = 0
#                 while status[0]['filledQuantity'] < status[0]['orderedQuantity'] or status[0]['status']=="No Response":
#                     time.sleep(3)
#                     status = getOrderDetails(etradeAuth, orderID=orderIdSL)
#                     logging.info(status)
#                     if status[0]['status']=='No Response':
#                         openTry += 1
#                     if openTry > 4:
#                         break
#                     print("checking status-open")

#                 ##check executed orders
#                 status = getOrderDetails(etradeAuth, orderID=orderIdSL, query={"status": "EXECUTED"})
#                 while status[0]['filledQuantity'] < status[0]['orderedQuantity']:
#                     time.sleep(5)
#                     status = getOrderDetails(etradeAuth, orderID=orderIdSL, query={"status": "EXECUTED"})
#                     logging.info(status)
#                     print("checking status-executed")
#                 ##get shares of BY symbol
#                 try:
#                     sharesBY = math.trunc((status[0]['filledQuantity'] * status[0]['avgPX']) / prices[symbolBY])
#                 except:
#                     sharesBY = math.trunc(cashAmountBY / prices[symbolBY])
#                 orderArray[1-indexSL]['quantity'] = sharesBY
#                 orderArray[1-indexSL]['transactionType'] = 'BY'
#                 orderArray[1-indexSL]['symbol'] = symbolBY
#                 prevIds = getPreviewIDs([orderArray[1-indexSL]], etradeAuth, process='vts')
#                 BYorderIds= sendOrders(prevIds, 'vts', etradeAuth)        
#                 sendText("VTS BY order submitted.")
#                 logging.info(f"BY orderId:{BYorderIds[0]}")


#             else:
#                 db_session.query(vtsTarget).delete()
#                 db_session.commit()
#                 db_session.close()
#                 sendEmail("No trades today.", True)
#                 sendText("No VTS targets today.")


#         except Exception as e:
#             logging.exception("vts order gen")
#             sendEmail(f"VTS Failed during order generation: {e}", False)
#             sendText("VTS Failure during order generation.")
#             db_session.close()
#             print('fail')
#             sys.exit(1)
# else:
#     sendText("VTS Strategy is inactive")
#     logging.info("VTS inactive")
#     db_session.close()

# print('success')
# sys.exit(0)




z = getEmailOrders()
print(z)