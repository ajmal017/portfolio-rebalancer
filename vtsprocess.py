import asyncio
# import util


import os
os.environ["DJANGO_SETTINGS_MODULE"] = "pv-rebalance.settings"
import django
django.setup()
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
from scraping_events.models import VTSEmail
from email.mime.multipart import MIMEMultipart
from html.parser import HTMLParser
from django.conf import settings
from io import StringIO
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

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

import pdb
import base64, pytesseract
from six.moves import urllib
from bs4 import BeautifulSoup
from pytesseract import Output
from PIL import Image
import cv2
import os
import tempfile
import subprocess
from fuzzywuzzy import fuzz
import boto3
import urllib.request
def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()
def ocr(path):
    temp = tempfile.NamedTemporaryFile(delete=False)

    process = subprocess.Popen(['tesseract', path, temp.name], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    process.communicate()

    with open(temp.name + '.txt', 'r') as handle:
        contents = handle.read()

    os.remove(temp.name + '.txt')
    os.remove(temp.name)

    return contents

def detect_text(path):
    """Detects text in the file."""
    from google.cloud import vision
    import io
    client = vision.ImageAnnotatorClient()

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)

    response = client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')

    for text in texts:
        print('\n"{}"'.format(text.description))

        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        print('bounds: {}'.format(','.join(vertices)))

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))

def getEmailOrders():
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login(settings.SCRAPY_EMAIL, settings.SCRAPY_EMAIL_PASSWORD)
    mail.select("inbox") 
    # result, data = mail.search(None, '(FROM "volatilitytradingstrategies@hotmail.com" UNSEEN)' )
    # result, data = mail.search(None, '(FROM "puneetmakhija4@gmail.com" SUBJECT "Fwd: Backup - Daily Trade Signals (Apr 20, 2021)" SEEN)')

    result, data = mail.search(None, '(FROM "er.mohittambi@gmail.com" SUBJECT "Fwd: Backup - Daily Trade Signals (Apr 20, 2021)" SEEN)' )
    # result, data = mail.search(None, '(FROM "er.mohittambi@gmail.com" SUBJECT "Fwd: Backup - Daily Trade Signals (Mar 8, 2021)" SEEN)' )

    ids = data[0] # data is a list.
    id_list = ids.split() # ids is a space separated string
    latest_email_id = id_list[-1] # get the latest
    
    result, data = mail.fetch(latest_email_id, "(RFC822)") 
    raw_email = data[0][1]
    msg = email.message_from_bytes(raw_email)
    # msg = msg.get_payload(decode=True)
    # while msg.is_multipart():
    #     msg = msg.get_payload(0)
    content = msg.get_payload(1)
    content = content.get_payload(decode=True)
    content = content.decode()
    # print('content', content)

    # html = urlopen(content)
    bs = BeautifulSoup(content, 'html.parser')
    # table = bs.find(text="Total Portfolio Solution").find_parent("table")
    table = bs.find_all('table')[3]
    # table1 = table.find_all('table')[0]
    # table2 = table1.find_all('table')
    # print(table)
    print('*************************')
    trade_portfolio_path = ''
    p = 0
    found = False
    for row in table.find_all("tr")[1:]:
        # i += 1
        if found:
            if p >= 1:
                print("congrats")
                for img in row.findAll('img'):
                    print(img.get('src'))
                    trade_portfolio_path = img.get('src')
                    found = False
            else:
                p+=1
        # print('row' + str(i))
        # print(row)
        for subtable in row.find_all('table'):
            # if found:
            # print([cell.get_text() for cell in subtable.find_all("td")])
            for cell in subtable.find_all("td"):
                print(cell.get_text())
                match = fuzz.ratio(cell.get_text(), 'Total Portfolio Solution trades') 
                if match > 90:
                    # if i == 1:
                    found = True
                    # else:
                        # i += 1
        # for q in row.find_all("td"):
        #     print(q)
        # print(row)
        # row.find_all("table")
        # get_table = row.find_all('table')
        # if get_table:
        #     for tab in get_table:
        #         pass
        # print(row)
    print('*************************')
    urllib.request.urlretrieve(trade_portfolio_path, "local-filename.png")

    documentName = "unnamed.png"

    # Read document content
    with open(documentName, 'rb') as document:
        imageBytes = bytearray(document.read())

    # Amazon Textract client
    textract = boto3.client('textract')

    # Call Amazon Textract
    response = textract.detect_document_text(Document={'Bytes': imageBytes})

    print(response)
    # phone battery down but this solution works sir Great Great
    # please type here
    # Print detected text
    found = False
    search = False
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            if search:
                try:
                    ticker = item["Text"].split(':')[1]
                    VTSEmail.objects.create(ticker=ticker.strip(), target='100', strategy='VTSEmail')
                except:
                    pass
            else:    
                print ('\033[94m' +  item["Text"] + '\033[0m')
                if found:
                    if item["Text"].isupper():
                        VTSEmail.objects.create(ticker=item["Text"], target='100', strategy='VTSEmail')
                    else:
                        search = True
                if item["Text"] == 'Position':
                    found = True

            
    # bototextract.py
    # images = bs.find_all('img')
    # all_images = []
    # for img in images:
    #     if img.has_attr('src'):
    #         # print(img['src'])
    #         all_images.append(img['src'])
    # print(all_images[10])
    # # img = Image.open(all_images[10])
    # urllib.request.urlretrieve(all_images[10], "sample.png")
    # detect_text(all_images[10])

    #####

    


    ##### 
    # im = Image.open("sample.png")

    # text = pytesseract.image_to_string(im, lang = 'eng')

    # print(text)
    # from asprise_ocr_api import *

    # ocr = Ocr()
    # ocr.start_engine("eng")  # deu, fra, por, spa - more than 30 languages are supported
    # text = ocr.recognize(
    #     "sample.png",  # gif, jpg, pdf, png, tif, etc.
    #     OCR_PAGES_ALL,  # the index of the selected page
    #     -1, -1, -1, -1,  # you may optionally specify a region on the page instead of the whole page
    #     OCR_RECOGNIZE_TYPE_TEXT,  # recognize type: TEXT, BARCODES or ALL
    #     OCR_OUTPUT_FORMAT_PLAINTEXT  # output format: TEXT, XML, or PDF
    # )
    # print("Result: ",text)

    # # ocr.recognize(more_images...)

    # ocr.stop_engine()

    # image = cv2.imread('sample.png')
    # gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # threshold_img = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # # custom_config = r'--oem 3 --psm 6'
    # details = pytesseract.image_to_data(threshold_img, output_type=Output.DICT, lang='eng')
    # print(details.keys())
    # total_boxes = len(details['text'])
    # for sequence_number in range(total_boxes):
    #     if int(details['conf'][sequence_number]) >30:
    #         print("kush", details['text'])

    # t = pytesseract.image_to_string(Image.open('sample.png'))
    # m = re.findall(r"Position: [\d—-]+", t)
    # if m:
    #     print(m[0])
    # print("t", t)
    # ste = detect_text('sample.png')
    # ste = ocr('sample.png')
    # print("ste", ste)





    import cv2
    import numpy as np
    # import numpy as np
    # import matplotlib.pyplot as plt
    # file = r'sample.png'
    # im1 = cv2.imread(file, 0)
    # im = cv2.imread(file)
    # ret,thresh_value = cv2.threshold(im1,180,255,cv2.THRESH_BINARY_INV)
    # kernel = np.ones((5,5),np.uint8)
    # dilated_value = cv2.dilate(thresh_value,kernel,iterations = 1)
    # contours, hierarchy = cv2.findContours(dilated_value,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # print('---------------------------')
    # print(contours, hierarchy)
    # print('--------------------------')
    # cordinates = []
    # for cnt in contours:
    #     x,y,w,h = cv2.boundingRect(cnt)
    #     cordinates.append((x,y,w,h))
    #     #bounding the images
    #     if y< 50:
         
    #         cv2.rectangle(im,(x,y),(x+w,y+h),(0,0,255),1)
    # plt.imshow(im)
    # cv2.namedWindow('detecttable', cv2.WINDOW_NORMAL)
    # cv2.imwrite('detecttable.jpg',im)
    # # img = Image.open(image_path) 



    # img = cv2.imread('sample.png')
    # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    # lines = cv2.HoughLines(edges, 1, np.pi / 180, 200)

    # for line in lines:
    #     rho, theta = line[0]
    #     a = np.cos(theta)
    #     b = np.sin(theta)
    #     x0 = a * rho
    #     y0 = b * rho
    #     x1 = int(x0 + 1000 * (-b))
    #     y1 = int(y0 + 1000 *(a))
    #     x2 = int(x0 - 1000 * (-b))
    #     y2 = int(y0 - 1000 * (a))
    #     print(cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 2))


    # content = strip_tags(content)
    # print(msg.is_multipart())
    # with open("imageToSave.png", "wb") aroundcubes fh:
        # fh.write(base64.decodebytes(content))

    # print('content', content)



    # pattern = re.compile(r'\s\s+')
    # content = re.sub(pattern, '', content)

    # ##are there any trades today?
    # trades = re.search(r'Section 3:.*(Total Portfolio Solution trades:\d)',content).group(1)

    # trades = int(trades.split(':')[1])
    # orders = []
    # tickers = []
    # orderArray = []
    # print("orders", orders)
    # if trades > 0:

    #     try:
            
    #         matches = ['Balanced', 'strategy page']
    #         print('matches', matches)
    #         link = re.search(r'Section 3:.*trades:\d(.*)Section 4',content).group(1)
    #         print('link', link)
    #         link = link.split('20%')
    #         for item in link:
    #             if all(x in item for x in matches):
    #                 if 'Required' in item:
    #                     instruction = item.split('Required')[1]
    #                     orders = instruction.split('/')
    #                 else:
    #                     logging.info("No VTS orders")

    #         if len(orders) > 0:
    #             for order in orders:
    #                 instructions = order.split(' ')
    #                 # tickers.append(instructions[1])
    #                 orderArray.append({"ticker": instructions[1], "transactionType": instructions[0]})

    #             ##security xref
    #             df = pd.DataFrame(orderArray)
    #             securityxref = pd.read_sql(db_session.query(SecurityXref).statement,db_session.bind, index_col='id')
    #             df = pd.merge(df, securityxref, how='left', on='ticker')
    #             df.loc[df.rebalTicker.isnull(), 'rebalTicker'] = df['ticker']
    #             df['ticker'] = df['rebalTicker']
    #             del df['rebalTicker']

    #             orderArray = df.to_dict('records') 
    #             tickers = df['ticker'].tolist()

    #     except Exception as ex:
    #         print(str(ex))
    #         # logging.exception("VTS Email Scrape Failed - orders exist but not captured.")
    #         # sendEmail("VTS Email Scrape Failed - orders exist but not captured.", False)
    #         # sendText("VTS Scrape Failed, please check email and rerun.")

    # mail.close()
    # return orderArray, tickers


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