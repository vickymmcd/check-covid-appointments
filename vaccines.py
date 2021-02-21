
import smtplib
import requests
import time
from email.message import EmailMessage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from bs4 import BeautifulSoup


######################## Email Functions #######################
def craftMessage(date):

    msg = MIMEMultipart('alternative')

    msg['Subject'] = 'Vaccine Opening'
    msg['From'] = 'ald01845@gmail.com'
    msg['To'] = 'aldean303@gmail.com'

    text = """
    Dear Alec,

    https://www.maimmunizations.org/clinic/search?q%5Bservices_name_in%5D%5B%5D=Vaccination&location=&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont%5D=Gillette&q%5Bvaccinations_name_i_cont%5D=&commit=Search#search_results

    It appears a vaccine opening has occurred on """ + date + """. Please visit the site quickly to book an appointment.

    Love,
    Alec
    """

    html = """

    <p>Dear Alec,<br><br>
    
    <a href="https://www.maimmunizations.org/clinic/search?q%5Bservices_name_in%5D%5B%5D=Vaccination&location=&search_radius=All&q%5Bvenue_search_name_or_venue_name_i_cont%5D=Gillette&q%5Bvaccinations_name_i_cont%5D=&commit=Search#search_results">
    MAImmunizations Search Results
    </a><br><br>

    It appears a vaccine opening has occurred on """ + date + """. Please visit the site quickly to book an appointment.<br><br>

    Love,<br>
    Alec</p>
    """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    msg.attach(part1)
    msg.attach(part2)

    return msg


def sendEmail(msg):
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    #use gmail app password for added security
    s.login('ald01845','prcgdbsgxfohxmoy')
    s.send_message(msg)
    s.quit()


###################### Web Parsing Functions ############################

# make get request and return html of the search results
def getHTML():
    baseURL = 'https://www.maimmunizations.org/clinic/search?'

    params = {
        'q[services_name_in][]': 'Vaccination',
        'search_radius': 'All',
        'q[venue_search_name_or_venue_name_i_cont]': 'Gillette',
        'commit': 'Search'
    }

    resp = requests.get(baseURL, params=params)

    html = resp.text

    return html

# get number of available appointments each day listed
def parseResp(html):
    parsed_html = BeautifulSoup(html, features='html.parser')
    
    gilletteList = parsed_html.body.div.find_all('div',
     attrs={'class':'md:flex justify-between -mx-2 md:mx-0 px-2 md:px-4 pt-4 pb-4 border-b border-gray-200'})


    apptsDict = {}
    for day in gilletteList:
        dayHeader = day.div.find('p', attrs={'class':'text-xl font-black'})
        dayList = dayHeader.text.split()
        date = dayList[-1]

        # find available appointments
        allP = day.div.find_all('p')
        for p in allP:

            if "Available" in p.text:
                col = p.text.find(":")
                appts = int(p.text[col+1:])
        
                if date in apptsDict:
                    apptsDict[date] += appts
                else:
                    apptsDict[date] = appts
    return apptsDict

######################################################################

def run():
    # set request interval to 5 seconds so as to not overload the site
    sleepy = 5
    prevAppt = {}
    stats = {"minutes":0, "appts":0}
    while True:
        try:
            html = getHTML()
            appts = parseResp(html)
        # catch either web connection error or website is overloaded error
        except Exception:
            print("Request failed, trying again.")
            time.sleep(sleepy)
            continue

        print(appts)
        print(stats)

        stats['minutes'] += 1/12

        # when an appointment becomes available, only send one email
        if appts == prevAppt:
            time.sleep(sleepy)
            continue
        prevAppt = appts

        for d in appts:
            if appts[d] > 0:
                # msg = craftMessage(d)
                # sendEmail(msg)
                print("Found appointment!!")
                stats['appts'] += 1

        time.sleep(sleepy)

if __name__ == "__main__":
    run()