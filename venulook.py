# -*- coding: utf-8 -*-
"""
Created on Thu Feb 13 12:16:44 2020

@author: Lenovo
"""

from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
client=MongoClient("mongodb://localhost:27017")
db=client["venuelookvenue-database"]
scrappedVenues=db.scrappedVenues
def repalceAllBadCharacter(testString):
            badChars=["\n","\t","\r","\xa0"]
            testString = ''.join(i for i in testString if not i in badChars) 
            testString=str(testString)
            return testString 
urls=[{
    "_id": "5e3bd58e3912a0416863d119",
    "name": "The Courtyard House",
    "vm_id": "the-courtyard-house-sarjapur-road",
    "city": "bangalore",
    "onboarded": "TRUE",
    "isOnboarded": "FALSE",
    "VenueLook": "https://www.venuelook.com/Bangalore/The-Courtyard-House-in-Sarjapur-Road",
    "Weddingz": "https://weddingz.in/bangalore/the-courtyard-house-sarjapur-road/"
  },
    {
    "_id": "5e3a831384c3a41e05c943cd",
    "name": "Days Inn",
    "vm_id": "days-inn-neemrana",
    "city": "gurgaon",
    "onboarded": "TRUE",
    "isOnboarded": "FALSE",
    "VenueLook": "https://www.venuelook.com/Alwar/Bar-of-Days-Hotel-in-Neemrana",
    "Weddingz": "https://weddingz.in/jaipur/days-hotel-neemrana/"
  }
  ]
def scrapeUrl(lists=[],*args):
    for venue in lists:
        source=requests.get(venue["VenueLook"]).text
        soup=BeautifulSoup(source,"lxml")
        soup.prettify()
        venueTitle=soup.find(class_="vendor-details h4 text-bold")
        if(venueTitle!=None):
            venueTitle=venueTitle.text
            venueTitle=repalceAllBadCharacter(venueTitle)
        else:
            venueTitle=None
        print(venueTitle)
        
        venueAddress=soup.find(class_="addr-right")
        venueSubArea=soup.find(class_="text-secondary h6 frow v-center")
        if(venueSubArea!=None):
            venueSubArea=venueSubArea.text
            venueSubArea=repalceAllBadCharacter(venueSubArea)
        else:
            venueSubArea=None
        print(venueSubArea)
        if(venueAddress!=None):
            venueLocation=venueAddress.find("p",class_="text-tertiary")
            if(venueLocation!=None):
                venueLocation=venueLocation.text
                venueLocation=repalceAllBadCharacter(venueLocation)
            else:
                venueLocation=None
            print(venueLocation)
        else:
            venueAddress=None
        totalViews=soup.find(class_="views")
        if(totalViews!=None):
            totalViews=totalViews.text
            totalViews=repalceAllBadCharacter(totalViews)
        else:
            totalViews=None
        print(totalViews)
        venueEnquiries=soup.find(class_="Enquiries")
        if(venueEnquiries!=None):
            venueEnquiries=venueEnquiries.text
            venueEnquiries=repalceAllBadCharacter(venueEnquiries)
        else:
            venueEnquiries=None
        print(venueEnquiries)
        pricePerPlate=soup.find(class_="col-md-6 price_sec")
        if(pricePerPlate!=None):
            vegAmount=pricePerPlate.find(class_="text").text
            vegAmount=repalceAllBadCharacter(vegAmount)
            if("Veg Price" in vegAmount):
                veg=pricePerPlate.find("div",class_="rate")
                strike=veg.find("strike")
                if(strike != None):
                    veg=veg.text
                    veg=repalceAllBadCharacter(veg)
                    veg=veg.split(" ")
                    veg=veg[2]+veg[3]+veg[4]+veg[5]
                    print(veg)
                else:
                    veg=veg.text
                    veg=repalceAllBadCharacter(veg)
                    print(veg)
            else:
                veg=None
                print(veg)
            nonVegAmount=pricePerPlate.find(class_="text").text
            nonVegAmount=repalceAllBadCharacter(nonVegAmount)
            if("NonVeg Price" in vegAmount):
                nonVeg=pricePerPlate.find("div",class_="rate")
                strike=nonVeg.find("strike")
                if(strike != None):
                    nonVeg=nonVeg.text
                    nonVeg=repalceAllBadCharacter(nonVeg)
                    nonVeg=nonVeg.split(" ")
                    nonVeg=nonVeg[2]+nonVeg[3]+nonVeg[4]+nonVeg[5]
                    print(nonVeg)
                else:
                    nonVeg=nonVeg.text
                    nonVeg=repalceAllBadCharacter(nonVeg)
                    print(nonVeg)
            else:
                nonVeg=None
                print(nonVeg)
        else:
            pricePerPlate = None
        capacity=soup.find(class_="col-md-6 cap_sec")
        if(capacity!=None):
            capacity=capacity.find(class_="rate").text
            capacity=repalceAllBadCharacter(capacity)
        else:
            capacity=None
        print(capacity)
        
        #data=soup.find("ul",class_="list-unstyled theam-list")

       # availableRooms=soup.find("i",class_="fa fa-university")
        #if(availableRooms!=None):
           # availableRooms=availableRooms.find("span",class_="pull-right")
            #availableRooms=repalceAllBadCharacter(availableRooms)
        #else:
            #availableRooms=None
       # print(availableRooms)
        FAQS=soup.find(class_="panel-group")
        if(FAQS!=None):
            FAQList=[]
            for listItem in FAQS.find_all(class_="panel panel-warning"):
                ques=listItem.find("div",class_="panel-heading").text
                ques=repalceAllBadCharacter(ques)
                ans=listItem.find("div",itemtype="https://schema.org/Answer").text
                ans=repalceAllBadCharacter(ans)
                FAQList.append({
                        
                        "Question":ques,
                        "Answer":ans
                         }) 
        else:
            FAQList=None
        print(FAQList)
        about=soup.find(class_="panel-body about-space")
        if(about!=None):
            about=about.text
            about=repalceAllBadCharacter(about)
        else:
            about=None
        print(about)
        
        timing=soup.find(class_="fa fa-clock-o mr5 yes")
        if(timing!=None):
            timing=timing.next_sibling
            timings = timing.next_sibling.next_sibling
            operatingTime=timings.next_element
            operatingTime=repalceAllBadCharacter(operatingTime)
        else:
            operatingTime=None
        print(operatingTime)
        cuisinesServed=soup.find("ul",class_="list-inline space-gdfroccasion")
        if(cuisinesServed!=None):
            cuisinesServes=[]
            for listItem in cuisinesServed.find_all("li"):
                value=listItem.text
                value=repalceAllBadCharacter(value)
                cuisinesServes.append(value)
        else:
            cuisinesServes=None
        print(cuisinesServes)
        occasionTypes=[]
        occasionType=soup.find("div",id="occa_good")
        if (occasionType!=None):
            for listItem in occasionType.find_all("li"):
                    isRed = False
                    isGreen = False
                    iTag = listItem.find("i")
                    if(iTag != None):
                        classes = iTag.get('class');
                        if('fa fa-check yes mr5' in classes):
                            isGreen = True
                        elif('fa fa-close close_no mr5' in classes):
                            isRed = True  
                    text = listItem.text
                    text=repalceAllBadCharacter(text)
                    isAvailable = False
                    isApplicable = True
                    if(isRed == False and  isGreen == False):
                        isApplicable = False
                    elif(isRed == True):   
                        isApplicable = True
                    elif(isGreen == True):
                        isAvailable = True
                        isApplicable = True 
                    occasionTypes.append({
                                "isAvailable": isAvailable,
                                "isApplicable": isApplicable,
                                "value": text
                            })
        else:
            occasionTypes=None
        print(occasionTypes)
        modesOfPayments=[]
        modesOfPayment=soup.find(class_="info_desc")
        if(modesOfPayment!=None):
            for modesOfPayment in soup.find_all("li",class_="info_desc"):
                isRed = False
                isGreen = False
                iTag = modesOfPayment.find("i")
                if(iTag != None):
                    classes = iTag.get('class');
                    if('fa fa-check yes mr5' in classes):
                        print("hi")
                        isGreen = True
                    elif('fa fa-close close_no mr5' in classes):
                        isRed = True  
                    text = modesOfPayment.text
                    text=repalceAllBadCharacter(text)
                    isAvailable = False
                    isApplicable = True
                    if(isRed == False and  isGreen == False):
                        isApplicable = False
                    elif(isRed == True):   
                        isApplicable = True
                    elif(isGreen == True):
                        isAvailable = True
                        isApplicable = True 
                    modesOfPayments.append({
                                    "isAvailable": isAvailable,
                                     "isApplicable": isApplicable,
                                    "value": text
                                })
                       
        else:
            modesOfPayments=None
        print(modesOfPayments) 
        
           
        scrappedvenue={
                "venueTitle": venueTitle,
                "venueSubArea":venueSubArea,
                "venueLocation":venueLocation,
                "totalViews":totalViews,
                "venueEnquiries":venueEnquiries,
                "pricePerPlate":{
                "veg":veg,
                },
                "maxCapacity":capacity,
               # "availableRooms":availableRooms,
                "FAQList": FAQList,
                "about": about,
                "operatingTime":operatingTime,
                "cuisinesServes": cuisinesServes,
                "occasionTypes": occasionTypes,
                "modesOfPayments": modesOfPayments,
                "vm_venueid": venue["_id"],
                "vm_id": venue["vm_id"],
                "city": venue["city"],
                "vm_venue_name": venue["name"],
            } 
        resultData=scrappedVenues.count({"vm_venueid":venue["_id"]})
        print(resultData)
       
        if(resultData==0):
            result=scrappedVenues.insert_one(scrappedvenue)
        else:
            result=scrappedVenues.update_one({"vm_venueid":venue["_id"]},{"$set":scrappedvenue})
    return result               
         
                
                
        
        
scrapeUrl(urls)



