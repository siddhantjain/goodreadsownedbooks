import os
import time
from rauth.service import OAuth1Service, OAuth1Session
import xml.etree.ElementTree as ET

url = 'http://www.goodreads.com'
request_token_url = '%s/oauth/request_token/' % url
authorize_url = '%s/oauth/authorize/' % url
access_token_url = '%s/oauth/access_token/' % url

#check if access tokens have been saved. If yes, generate session using access tokens
if(os.path.isfile('accesstokens.txt')):
    accesstokenFile = open('accesstokens.txt', 'r')
    access_token = accesstokenFile.readline().strip()
    access_token_secret = accesstokenFile.readline().strip()
    session = OAuth1Session(
        consumer_key = 'CHANGEME',
        consumer_secret = 'CHANGEME',
        access_token = access_token,
        access_token_secret = access_token_secret,
    )
else:
    goodreads = OAuth1Service(
        consumer_key='CHANGEME',
        consumer_secret='CHANGME',
        name='goodreads',
        request_token_url='http://www.goodreads.com/oauth/request_token',
        authorize_url='http://www.goodreads.com/oauth/authorize',
        access_token_url='http://www.goodreads.com/oauth/access_token',
        base_url='http://www.goodreads.com/'
    )
    # head_auth=True is important here; this doesn't work with oauth2 for some reason
    request_token, request_token_secret = goodreads.get_request_token(header_auth=True)
    authorize_url = goodreads.get_authorize_url(request_token)
    os.startfile(authorize_url)
    #webbrowser.open(authorize_url, new=0, autoraise=True)
    print ('Visit this URL in your browser: ' + authorize_url)
    accepted = 'n'
    while accepted.lower() == 'n':
        # you need to access the authorize_link via a browser,
        # and proceed to manually authorize the consumer
        accepted = input('Have you authorized me? (y/n) ')
    session = goodreads.get_auth_session(request_token, request_token_secret)

if(os.path.isfile('accesstokens.txt')==False):
    ACCESS_TOKEN = session.access_token
    ACCESS_TOKEN_SECRET = session.access_token_secret
    accesstokenFile = open('accesstokens.txt','w')
    accesstokenFile.write('%s\n%s'%(str(ACCESS_TOKEN),str(ACCESS_TOKEN_SECRET)))

useridxml = session.get('https://www.goodreads.com/api/auth_user')
root = ET.fromstring(useridxml.content)

for child in root:
        if str(child.tag)=='user':
            userid = (child.attrib['id'])
            break
#getting a list of friends of the user
userfriendsxml = session.get('https://www.goodreads.com/friend/user.xml',params={'id':userid,'page': '1'})
root = ET.fromstring(userfriendsxml.content)
#this variable is used to check if all friends have been listed
page_end = root.find('./friends').attrib['end']

#a dictionary to store book id as key and list of friends who own that book as value
friends_owned_books_dict = dict()
i = 2
while(int(page_end)!=0):
    nodelist = root.findall('./friends/user/id')
    for each in nodelist:
        ownedbooksxml = session.get('https://www.goodreads.com/owned_books/user.xml', params={'id':each.text, 'page':1})
        ownedbooks_root = ET.fromstring(ownedbooksxml.content)
        #again, this variable is used to check if all books owned by a user are listed
        paginateFlag = ownedbooks_root.find('./owned_books/owned_book')
        j=2;
        while(paginateFlag!=None):
            ownedbookslist = ownedbooks_root.findall('./owned_books/owned_book/book/id')
            for bookid in ownedbookslist:
                if bookid.text in friends_owned_books_dict:
                    friends_owned_books_dict[bookid.text].append(each.text)
                else:
                    friends_owned_books_dict[bookid.text]=[each.text]

            ownedbooksxml = session.get('https://www.goodreads.com/owned_books/user.xml', params={'id':each.text, 'page':j})        
            ownedbooks_root = ET.fromstring(ownedbooksxml.content)
            paginateFlag = ownedbooks_root.find('./owned_books/owned_book')
            j=j+1

    userfriendsxml = session.get('https://www.goodreads.com/friend/user.xml',params={'id':userid,'page': i})
    root = ET.fromstring(userfriendsxml.content)
    page_end = root.find('./friends').attrib['end']
    i=i+1



'''
code to search owners of a book
'''

bookid_input =  input("Enter id of book that you'd like to search")
if(bookid_input not in friends_owned_books_dict.keys()):
    print("none of your friends own this book")
else:
    print("Following users from your friend list own this book")
    for each in friends_owned_books_dict[bookid_input]:
        userinfoxml = session.get('https://www.goodreads.com/user/show/%s.xml'%each,params={'key':'CHANGEME','id':each})
        userinforoot = ET.fromstring(userinfoxml.content)
        username = userinforoot.find('./user/name')
        print(username.text)