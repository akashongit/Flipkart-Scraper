import requests
from lxml import html
from urls import phones, test
from mailer import sendErrorReport, sendMail

def main():
    for phone, url in test.items():
        page = requests.get(url)
        if(page.ok != True):
            sendErrorReport()
            break
        
        tree = html.fromstring(page.content)
        notifyMeEle = tree.xpath("/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/button")
        if(len(notifyMeEle) != 0):
            value = str(notifyMeEle[0].text).lower()
            if value != "notify me":
                continue
        else:
            buyNowEle = tree.xpath("/html/body/div[1]/div/div[3]/div[2]/div[1]/div[1]/div[2]/div/ul/li[2]/form/button")
            if(len(buyNowEle) != 0):
                value = str(buyNowEle[0].text).lower()
                if "buy now" in value:
                    sendMail()
            else:
                sendErrorReport()
                continue

if __name__ == "__main__":
    main()
