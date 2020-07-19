#Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import bs4
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import time
from selenium.common.exceptions import NoSuchElementException
import sys

#Gets the input and creates the url
#Twitter URL
twitter_start = 'https://twitter.com/search?f=users&vertical=default&q='
twitter_end='&src=typd'
first_name = input("Input the first name of the applicant: ")
last_name = input("Input the last name of the applicant: ")
while(first_name=="" or last_name==""):
    first_name = input("Input the first name of the applicant: ")
    last_name = input("Input the last name of the applicant: ")
limit=0
while(limit<=0 or limit>20):
    limit=int(input("Enter the maximum number of recent tweets you want from a student (min is 0 and max is 20): "))
twitter_url = twitter_start+first_name+"%20"+last_name+twitter_end

#Opens the browser and goes to the student's profile
browser=webdriver.Chrome()
browser.get(twitter_url)
try:
    elm=browser.find_element_by_css_selector('a.ProfileNameTruncated-link')
    elm.click()
except NoSuchElementException as exception:
    print("This person does not have a twitter account")
    sys.exit(1)
time.sleep(3)

#Extracts the tweets and displays them
uClient=uReq(browser.current_url)
page_html=uClient.read()
uClient.close()
page_soup=soup(page_html,"html.parser")

containers=page_soup.findAll("div",{"class":"js-tweet-text-container"})
catTweets=""
try:
    for i in range(0,limit):
        print(containers[i].text.strip()+"\n")
        catTweets+=(containers[i].text.strip()+"\n")
except IndexError:
    if len(containers)==0:
        print('There are no tweets by this person.')
    else:
        print("These are all the tweets available for " + first_name + " " + last_name + ".")

full_name=first_name+" "+last_name
#firebase = firebase.FirebaseApplication('https://university-admissions-insider.firebaseio.com/',None)
#result=firebase.post('/tweets',{full_name:"45446474\n32532532563623"})

import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate('./university-admissions-insider-firebase-admin.json')
default_app =  firebase_admin.initialize_app(cred)
db = firestore.client()

twit_ref=db.collection(u'applicants').document(full_name)
twit_ref.set({
    u'tweets': catTweets
})
