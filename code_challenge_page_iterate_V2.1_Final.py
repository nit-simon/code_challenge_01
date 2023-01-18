#!/usr/bin/env python
# coding: utf-8


import pandas as pd
import requests
from bs4 import BeautifulSoup #as soup
import time
import json

from pathlib import Path  
import os


# versions of the core libraries used
# - pandas version: 1.0.1
# 
# - BeautifulSoup version: 4.8.2
# 
# - requests version: 2.22.0
# 
# - python version: 3.7.3



# tested only on windows, fetch the username folder, assist in saving location
# first = len("c:\\users\\")
# print(os.path.abspath(os.getcwd()))
# pwd = os.path.abspath(os.getcwd())
# second = pwd[first:len(pwd)]
# third = second.find("\\")
# pc_username_folder = second[0:third]
# print("username: "+ pc_username_folder)

# save_loc =fr'C:\Users\{pc_username_folder}\Desktop\pharma_ida.csv'




#manually type save location
save_loc =fr'C:\Users\rsimon\Desktop\pharma_ida.csv'





#This URL is the page you actually want to pull down with requests.
initial_page = 'https://idbop.mylicense.com/verification/Search.aspx'
searchPage = initial_page



# format the fetch list into  columns.
def list_format(list_name, step):
    return [list_name[i::step] for i in range(step)]
#print(list_format(data,4))



def fetch_next_page(page):
    payload_next_page = {
    "CurrentPageIndex":page,
    "__EVENTTARGET":"datagrid_results$_ctl44$_ctl1",
    "__EVENTARGUMENT":"",
    "__VIEWSTATEGENERATOR":viewStateGenerator,
    "__VIEWSTATE":viewState,
    "__EVENTVALIDATION":eventValidation}
    nextpage="https://idbop.mylicense.com/verification/SearchResults.aspx"
    result_np=req_sess.post(nextpage,headers=headers1,data=payload_next_page)
    soup1=BeautifulSoup(result_np.content, 'html.parser')
    td_as_base1 = soup1.find_all('td') 
    data2 = []
    for cell in td_as_base1:
            if cell.text=="":
                #print("empty string skipped")
                continue
            #if cell.text.startswith('\n'):
            if '\\' in  r"%r" % cell.text:
                #print("slash skipped")
                continue
            insertdata = cell.text.strip()
            data2.append(insertdata)
    return data2 ,soup1




def count_pages():
    pagination=BeautifulSoup(result.content, 'html.parser')
    paginationtags = pagination.find_all('a') # all trs
    pages = [tag.text.strip() for tag in paginationtags if tag.text.isnumeric()]
    return pages




def remove_these(thisList):
    try:
        thisList.remove("Search")
        thisList.remove("Search Results")
        print("Removed exess texts")
    except:
        print("keywords removed/not present")


############# SEQUENCE 1 - the initial page needs to be loaded first to acquire the viewstate to be used in the search page, then the pagination


print("Loading the initial page")
req_sess=requests.Session()
r=req_sess.get(initial_page)
time.sleep(5)
soup=BeautifulSoup(r.content, 'html.parser')



# eventTarget=soup.find(id="__EVENTTARGET")['value']
#eventArguement=soup.find(id="__EVENTARGUMENT")['value']
viewState=soup.find(id="__VIEWSTATE")['value']
viewStateGenerator=soup.find(id="__VIEWSTATEGENERATOR")['value']
eventValidation=soup.find(id="__EVENTVALIDATION")['value']


# # for testing
# license_type_name = "Pharmacist"
# lastName ="L*"


### search fields , Please uncomment after testing
lastName = input("Enter Last Name")
first_name  = input('Enter First Name')
license_type_name =input("Enter License Type")
last_name  = input('Enter Last Name')
addr_city  = input('Enter City')
license_no  = input('Enter license no')
addr_state  = input('Enter State')
license_status_name  = input('Enter license status')
addr_county  = input('Enter Country')
addr_zipcode  = input('Enter Zip')



payload = {
    "__EVENTTARGET":"",
    "__EVENTARGUMENT":"",
    "__LASTFOCUS":"",
    "__VIEWSTATEGENERATOR":viewStateGenerator,
    "__VIEWSTATE":viewState,
    "__EVENTVALIDATION":eventValidation,
    "t_web_lookup__first_name":"",
    "t_web_lookup__license_type_name":license_type_name,
    "t_web_lookup__last_name":lastName,
    "t_web_lookup__addr_city":"",
    "t_web_lookup__license_no":"",
    "t_web_lookup__addr_state":"",
    "t_web_lookup__license_status_name":"",
    "t_web_lookup__addr_county":"",
    "t_web_lookup__addr_zipcode":"",
    "sch_button":"Search"
}




headers1 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Content-Length': '2853',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'idbop.mylicense.com',
    'Origin':'https://idbop.mylicense.com',
    'Referer': 'https://idbop.mylicense.com/verification/Search.aspx',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'X-Requested-With':'XMLHttpRequest'
}





headers2 = {
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding':'gzip, deflate, br',
    'Connection':'keep-alive',
    'Cache-Control':'max-age=0',
    'Content-Length': '2853',
    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
    'Host':'idbop.mylicense.com',
    'Origin':'https://idbop.mylicense.com',
    'Referer': 'https://idbop.mylicense.com/verification/SearchResults.aspx',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 Edg/108.0.1462.54',
    'X-Requested-With':'XMLHttpRequest'
}



print("submitting inital requet to page")
result=req_sess.post(searchPage,headers=headers1,data=payload)



# searchPage


# for fetching the page count
soup=BeautifulSoup(result.text, 'html.parser')


# fetch all the Links(href) of the persons on the list

def get_all_links(soup):
    #soup=BeautifulSoup(result.text, 'html.parser')
    tds = soup.find_all('td')
    atagList=[]
    for atags in tds:
        atag = atags.find('a')
        if atag==[]:
            continue
        if atag==None:
            continue
        if not atag.has_attr('target'):    #add this line
            continue
        if not atag['target']=='_blank':   #add this line
            continue
        if len(atag['href'])<43:           #add this line
            continue
        atagList.append(atag)    
    ##list of names only
    
    #atagList_reduce=atagList[6:86:1] # remove this line  ##########################
    
    ##remove the duplicates
    #reduced_atag = atagList_reduce[::2] -- change variable name as below ##################
    reduced_atag = atagList[::2] 
    print("hrefs fethed: "+ str(len(reduced_atag)))
    #href = reduced_atag[0].find_all('id')
    href_tags = []
    for hr in reduced_atag:
        hreftag =hr.get('href')
        href_tags.append(hreftag)
        #print(href_tags)
    return href_tags


# Load the individual page of each person in the list

def get_person_data(href_tag):
    resultOnly = href_tag[20::] 
    person_req_link = "https://idbop.mylicense.com/verification/"
    person_req_get_request_link = person_req_link+href_tag
    person=req_sess.get(person_req_get_request_link,headers=headers2,data=resultOnly)
    time.sleep(1)

    #working code v1
    person_page=BeautifulSoup(person.content, 'html.parser')
    table  =person_page.find_all('table')


    person_data = []
    for td in table[4]:
        try:
            row = td.find('td').text.strip()
            #print(row)
            person_data.append(row)
        except:
            continue

    person_data1 = []
    tds2 = table[4].find_all('td')
    for td in tds2:
        for tr in td:
            try:
                trdata= tr.text.strip()
                person_data1.append(trdata)
            except:
                continue

    dataSet2 = []
    for td in table[8]:
        for tr in td:
            try:
                trdata= tr.text.strip()
                dataSet2.append(trdata)
            except:
                continue

    dataSet1 = person_data1[9:15:]

    person_data1 = []
    tds2 = table[4].find_all('td')
    for td in tds2:
        for tr in td:
            try:
                trdata= tr.text.strip()
                person_data1.append(trdata)
            except:
                continue

    final_dataset = dataSet1+dataSet2

    person_info = list_format(final_dataset, 2)

    df1 = pd.DataFrame(person_info)
    header_row = df1.iloc[0]
    df2 = pd.DataFrame(df1.values[1:], columns=header_row)

    return df2


#query model (sample of the get request of each of the Person )
#https://idbop.mylicense.com/verification/Details.aspx?result=7fabb069-2284-4244-ac9f-115002f9da12




# For page 1
persons_on_this_page = get_all_links(soup)


#fetch page 1
all_person =[]
for person in persons_on_this_page:
    print(person)
    each_person = get_person_data(person)
    time.sleep(3)
    all_person.append(each_person)




# test output of "get_all_links" function and check if we can use "contains" to filter every href




############################################################################################################################


pageCount =count_pages()
pageCount

#iterate fetching the res the  pages
all_person =[]
for page in range(len(pageCount)+1):
    print("fetching page "+str(page))
    fetchedData,soup = fetch_next_page(page)
    persons_on_this_page = get_all_links(soup)
    for person in persons_on_this_page:
        print(person)
        each_person = get_person_data(person)
        time.sleep(3)
        all_person.append(each_person)


final_data = pd.concat(all_person)



final_data



final_data.drop(['DBA:', 'Effective:','Status Reason:','Status Date:','Method:'], axis=1)



print("saving file")
filepath = Path(save_loc)  
filepath.parent.mkdir(parents=True, exist_ok=True)  
final_list.to_csv(filepath)



print("scrape completed")

