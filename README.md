# MA Vaccine Appointment Checker

## Description

This is a simple Python program that checks the Massachusetts' COVID vaccine appointment website every so often for availablities.

## Installation

This program requires the following dependencies:

- Python 3
  - To install, go to [Python's website](https://www.python.org/downloads/) and download the most recent version of Python
  - During the install process, make sure *Add Python 3.x to PATH* is checked
  - you should be able to open a command line and run ```python --version```
- Beautiful Soup 4
  - Once Python is installed, run ```pip install beautifulsoup4```
  - This library makes it easier to parse the html from web pages
- Git
  - Check to see if Git is already installed by running ```git --version```
  - If it's not installed, head to [Git's website](https://git-scm.com/download/win) to install

In addition to those dependencies, you need to edit the config file **config.json** to include your corresponding information, such as email addresss and Google App credentials. It also allows for adding a secondary email address so you can be notified in 2 places.

### Google App Setup

By setting up Gmail App credentials, you are allowing this program to send you mail, notifying you when an appointment becomes available.

To create your gmail app credentials, follow these steps:

1. Go to your Google Account settings at [My Google Account](https://myaccount.google.com/)
2. On the left sidebar, select **Security**
3. Under the *Signing in to Google Section*, select **App Passwords**
4. Enter your Google Password if necessary
5. Click **Select App**, and select **Mail**
6. Click **Select Device**, and choose the corresponding device
7. Click **Generate**
8. Copy and paste the generated password into *config.json*

**Note**: Google creates these passwords for you as an added layer of security, so that you don't have to type in your own Google password.

## Usage

Once you've filled out the *config.json* file to your satisfaction, simply run the following commands to search for appointments at Gillette:

```
git clone https://github.com/alecdean/check-covid-appointments.git
cd check-covid-vaccines
python vaccines.py
```

Similarly, to search for appointments at the Danvers site, you can run:

```
python danversvaccine.py
```

After running the last command, you should begin to see the results of each search printed every few seconds.
