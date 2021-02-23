
import smtplib
import requests
import json
import time
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup


# global variables
printStats = False
sendEmailNot = False
user = ""
email = ""
pswd = ""

######################## Email Functions #######################
def craftMessage(date, emailparam):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = 'DANVERS Vaccine Opening'
    msg['From'] = emailparam
    msg['To'] = emailparam

    text = """
    Dear """+user+""",

    https://vaxfinder.mass.gov/locations/doubletree-hotel-danvers/

    It appears a vaccine opening has occurred on """ + date + """. Please visit the site quickly to book an appointment.

    Love,
    Vicky
    """

    html = """

    <p>Dear """ + user+""",<br><br>

    <a href="https://vaxfinder.mass.gov/locations/doubletree-hotel-danvers/">
    MAImmunizations Search Results
    </a><br><br>

    It appears a vaccine opening has occurred on """ + date + """. Please visit the site quickly to book an appointment.<br><br>

    Love,<br>
    Vicky</p>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    return msg


def sendEmail(msg, msg2):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    #use gmail app password for added security
    s.login(user, pswd)
    s.send_message(msg)
    s.send_message(msg2)
    s.quit()

def getHTML():
    baseURL = 'https://vaxfinder.mass.gov/locations/doubletree-hotel-danvers/'

    resp = requests.get(baseURL)

    html = resp.text

    return html

# get number of available appointments each day listed
def parseResp(html, apptsDict={}):
    parsed_html = BeautifulSoup(html, features='html.parser')
    table = parsed_html.find(lambda tag: tag.name=='table')
    rows = table.findAll(lambda tag: tag.name=='tr')

    for day in rows[1:]:
        td_list = []
        for td in day:
            if td != '\n':
                td_list.append(td)
        dayHeader = td_list[0].string
        available = td_list[2].strong.string
        apptsDict[dayHeader] = available

    return apptsDict

def run():
    # set request interval to 5 seconds so as to not overload the site
    sleepy = 5
    prevAppt = {}
    stats = {"minutes":0, "appts":0}
    emailsent = False
    appts = {}

    while True:
        try:
            appts.clear()
            htmlPage1 = getHTML()
            appts = parseResp(htmlPage1)

        # catch either web connection error or website is overloaded error
        except Exception:
            print("Request failed, trying again.")
            time.sleep(sleepy)
            continue

        print(appts)
        if printStats:
            print(stats)

        stats['minutes'] += 1/12

        # when an appointment becomes available, only send one email
        if appts == prevAppt and emailsent:
            time.sleep(sleepy)
            continue
        prevAppt = appts

        for d in appts:
            print(d, appts[d])
            if int(appts[d]) > 20 and sendEmailNot:

                try:
                    msg = craftMessage(d, email)
                    msg2 = craftMessage(d, email2)
                    sendEmail(msg, msg2)
                    #sendEmail(msg2)
                    emailsent = True
                    print("Sent an email!")
                    break
                except Exception:
                    print("Failed to send email. Please check config.json")
                    time.sleep(sleepy)
                    continue

                print("Found appointment!!")
                stats['appts'] += 1

        if emailsent:
            break
        time.sleep(sleepy)


if __name__ == "__main__":

    # load parameters
    params = {}
    with open('config.json') as json_file:
        params = json.load(json_file)

        sendEmailNot = params["send_email_notification"]
        printStats = params["print_statistics"]
        email = params['your_email']
        email2 = params['second_email']
        user = params['your_gmail_username']
        pswd = params['your_google_app_password']

    run()
