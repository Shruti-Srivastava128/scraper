# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 16:06:25 2020

@author: Lenovo
"""

from bs4 import BeautifulSoup
import requests
from pymongo import MongoClient
#from itertools import cycle 
client=MongoClient("mongodb://localhost:27017")
db=client["weddingzvenueData-database"]
scrappedvenues=db.scrappedvenues
urlsToScraps= db.urlsToScraps
urls=[
 {
    "_id": "5bbf61964b500d0ef32462ed",
    "name": "Park Inn By Radisson",
    "vm_id": "park-inn-by-radisson-bilaspur",
    "city": "gurgaon",
    "onboarded": "TRUE",
    "isOnboarded": "FALSE",
    "VenueLook": "",
    "Weddingz": "https://weddingz.in/gurugram/park-inn-by-radisson-bilaspur-nh-8/"
  }
]

readData=urlsToScraps.find({"Weddingz":{"$exists": True}})
def repalceAllBadCharacter(testString):
            badChars=["\n","\t","\r"]
            testString = ''.join(i for i in testString if not i in badChars) 
            testString=str(testString)
            return testString

def scrapeUrl(lists=[],*args):
    for venue in lists:
        source=requests.get(venue["Weddingz"]).text
        soup=BeautifulSoup(source,"lxml")
        soup.prettify()
        venueTitleHeading=soup.find(class_="text-content")
        if(venueTitleHeading!=None):
            venueTitle = venueTitleHeading.h1
            if (venueTitle!=None):
                venueTitle=venueTitle.text
                venueTitle=repalceAllBadCharacter(venueTitle)
            else:
                venueTitle= None
        else:
            venueTitle = None
        print(venueTitle)  
        venueTypes = soup.find(class_="venue-type")
        venueTypeList=[]
        if(venueTypes!=None):
            for listItem in venueTypes.find_all("li"):
               cocktailVenue=listItem.h2.text
               cocktailVenue=repalceAllBadCharacter(cocktailVenue)
               venueTypeList.append(cocktailVenue)
        else:
            venueTypeList=None
        print(venueTypeList)
        likes=soup.find(class_="liked")
        if(likes!=None):
            likes=likes.text
            likes=repalceAllBadCharacter(likes)
        else:
            likes=None
        print(likes)
        bookings=soup.find(class_="booking")
        if(bookings!=None):
            bookings=bookings.text
            bookings=bookings.split(":")
            bookings=bookings[1].split(" ")
            pastBookings=bookings[1]
            pastBookings=repalceAllBadCharacter(pastBookings)
        else:
            pastBookings=None
        print(pastBookings)
        views=soup.find(class_="views")
        if(views!=None):
            views=views.text.lstrip()
            views=repalceAllBadCharacter(views)
        else:
            views=None
        print(views)
        pastShortlist=soup.find(class_="shortlist")
        if(pastShortlist!=None):
            pastShortlist=pastShortlist.text.lstrip()
            pastShortlist=repalceAllBadCharacter(pastShortlist)
        else:
            pastShortlist=None
        print(pastShortlist)
        venueDescriptionSpan=soup.find(class_="white-wrapper about-venue-desc less-more")
        if(venueDescriptionSpan!=None):
            venueDescription = venueDescriptionSpan.span
            if(venueDescription!=None):
                venueDescription=venueDescription.text
                venueDescription=repalceAllBadCharacter(venueDescription)
            else:
                venueDescription=None
        else:
            venueDescription = None
        print(venueDescription)
        veg=soup.find(class_="veg")
        if(veg!=None):
            vegAmount=veg.find(class_="amount").text
            vegAmount=repalceAllBadCharacter(vegAmount)
        else:
            vegAmount=None
        print(vegAmount)
        nonVeg=soup.find(class_="non-veg")
        if(nonVeg!=None):
            nonVegAmount=nonVeg.find(class_="amount").text
            nonVegAmount=repalceAllBadCharacter(nonVegAmount)
        else:
            nonVegAmount=None
        print(nonVegAmount)
        liquior=soup.find(class_="liquior")
        if(liquior!=None):
            liquiorAmount=liquior.find(class_="amount").text
            liquiorAmount=repalceAllBadCharacter(liquiorAmount)
        else:
            liquiorAmount=0
        print(liquiorAmount)
        venueContact=soup.find(class_="number")
        if(venueContact!=None):
            venueContact=venueContact.text.lstrip()
            venueContact=repalceAllBadCharacter(venueContact)
        else:
            venueContact=None
        print(venueContact)
        venueAddress=soup.find(class_="tab-data address")
        if(venueAddress!=None):
            venueAddress=venueAddress.text.lstrip()
            venueAddress=repalceAllBadCharacter(venueAddress)
        else:
            venueAddress=None
        print(venueAddress)
        timings=[]
        timing=soup.find_all("slot")
        if (timing!=None):
            for timing in soup.find_all(class_="slot"):
                mornevenTiming=timing.text.lstrip()
                mornevenTiming=repalceAllBadCharacter(mornevenTiming)
                timings.append(mornevenTiming)
        else:
            timings=None
        print(timings)
        venueCloseTiming=soup.find(class_="venue-close")
        if (venueCloseTiming!=None):
            venueCloseTiming=venueCloseTiming.text
            venueCloseTiming=repalceAllBadCharacter(venueCloseTiming)
        else:
           venueCloseTiming=None
        print(venueCloseTiming)
        venueLandmark=soup.find(class_="tab-data landmark")
        if (venueLandmark!=None):
            venueLandmark=venueLandmark.text
            venueLandmark=repalceAllBadCharacter(venueLandmark)
        else:
            venueLandmark=None
        print(venueLandmark)
        uspDetail=soup.find(class_="usp-detail")
        if (uspDetail!=None):
            uspDetail=uspDetail.text.lstrip().rstrip()
            usps=[]
            usps=uspDetail.split("\n")
        else:
           usps=None
        print(usps)         
        #print(tableDataValues)
        venueExpertNotes=soup.find(class_="tab-data target")
        if(venueExpertNotes!=None):
            venueExpertNotes=venueExpertNotes.text.lstrip()
            venueExpertNotes=repalceAllBadCharacter(venueExpertNotes)
        else:
            venueExpertNotes=None
        print(venueExpertNotes)
        summary=soup.find(class_="summary__div")
        if(summary!=None):
            summary=summary.text.lstrip()
            summary=repalceAllBadCharacter(summary)
        else:
            summary=None
        print(summary)
        decorPolicies=soup.find(class_="decorators")
        if(decorPolicies!=None):
            decorators = []
            for listItem in decorPolicies.find_all("li"):
                isRed = False
                isGreen = False
                span = listItem.find('span')
                if(span != None):
                    classes = span.get('class');
                    if('color-green' in classes):
                        isGreen = True
                    elif('color-red' in classes):
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
                decorators.append({
                            "isAvailable": isAvailable,
                             "isApplicable": isApplicable,
                            "value": text
                        })
        else:
            decorators=None
        print(decorators)
        foodPolicies=soup.find(class_="caterers")
        if(foodPolicies!=None):
            foods=[]
            for listItem in foodPolicies.find_all("li"):
                isRed = False
                isGreen = False
                span = listItem.find('span')
                if(span != None):
                    classes = span.get('class');
                    if('color-green' in classes):
                        isGreen = True
                    elif('color-red' in classes):
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
                foods.append({
                            "isAvailable": isAvailable,
                             "isApplicable": isApplicable,
                            "value": text
                        })
        else:
            foods=None
        print(foods)
        alcoholPolicies=soup.find(class_="policies-col alcohol")
        if(alcoholPolicies!=None):
            alcohols=[]
            for listItem in alcoholPolicies.find_all("li"):
                isRed = False
                isGreen = False
                span = listItem.find('span')
                if(span != None):
                    classes = span.get('class');
                    if('color-green' in classes):
                        isGreen = True
                    elif('color-red' in classes):
                        isRed = True  
                text = listItem.text
                text=repalceAllBadCharacter(text)
                print(text)
                isAvailable = False
                isApplicable = True
                if(isRed == False and  isGreen == False):
                    isApplicable = False
                elif(isRed == True):   
                    isApplicable = True
                elif(isGreen == True):
                    isAvailable = True
                    isApplicable = True 
                alcohols.append({
                            "isAvailable": isAvailable,
                             "isApplicable": isApplicable,
                            "value": text
                        })
        else:
            alcohols=None
        print(alcohols)
        taxes=soup.find(class_="policies-col taxes")
        if (taxes!=None):
            taxes=taxes.find(class_="tab-data").text
            taxes=repalceAllBadCharacter(taxes)
        else:
            taxes=None
        print(taxes)
        cancellationPolicies=soup.find(class_="policies-col cancellation")
        if(cancellationPolicies!=None):
            cancellationPolicies=cancellationPolicies.find(class_="tab-data").text
            cancellationPolicies=repalceAllBadCharacter(cancellationPolicies)
        else:
            cancellationPolicies=None
        print(cancellationPolicies)
        advancePolicies=soup.find(class_="policies-col advance")
        if(advancePolicies!=None):
            advancePolicies=advancePolicies.find(class_="tab-data").text
            advancePolicies=repalceAllBadCharacter(advancePolicies)
        else:
            advancePolicies=None
        print(advancePolicies)
        parkings=[]
        lodgings=[]
        changingRooms=[]
        venuePoliciesParking = soup.find_all(class_="policies-col parking")
        
        if(len(venuePoliciesParking) > 0 and  venuePoliciesParking[0]!=None):
                for listItem in venuePoliciesParking[0].find_all("li"):
                    isRed = False
                    isGreen = False
                    span = listItem.find('span')
                    if(span != None):
                        classes = span.get('class');
                        if('color-green' in classes):
                            isGreen = True
                        elif('color-red' in classes):
                            isRed = True  
                    text = listItem.text
                    text=repalceAllBadCharacter(text)
                    print(text)
                    isAvailable = False
                    isApplicable = True
                    if(isRed == False and  isGreen == False):
                        isApplicable = False
                    elif(isRed == True):   
                        isApplicable = True
                    elif(isGreen == True):
                        isAvailable = True
                        isApplicable = True 
                    parkings.append({
                                "isAvailable": isAvailable,
                                 "isApplicable": isApplicable,
                                "value": text
                            })
        else:
                parkings=None
        print(parkings)
            
        if(len(venuePoliciesParking) > 1 and  venuePoliciesParking[1]!=None):
                for listItem in venuePoliciesParking[1].find_all("li"):
                    isRed = False
                    isGreen = False
                    span = listItem.find('span')
                    if(span != None):
                        classes = span.get('class');
                        if('color-green' in classes):
                            isGreen = True
                        elif('color-red' in classes):
                            isRed = True  
                    text = listItem.text
                    text=repalceAllBadCharacter(text)
                    print(text)
                    isAvailable = False
                    isApplicable = True
                    if(isRed == False and  isGreen == False):
                        isApplicable = False
                    elif(isRed == True):   
                        isApplicable = True
                    elif(isGreen == True):
                        isAvailable = True
                        isApplicable = True 
                    lodgings.append({
                                "isAvailable": isAvailable,
                                 "isApplicable": isApplicable,
                                "value": text
                            })
        else:
                lodgings=None
        print(lodgings)
            
        if(len(venuePoliciesParking) > 2 and  venuePoliciesParking[2]!=None):
                for listItem in venuePoliciesParking[2].find_all("li"):
                    isRed = False
                    isGreen = False
                    span = listItem.find('span')
                    if(span != None):
                        classes = span.get('class');
                        if('color-green' in classes):
                            isGreen = True
                        elif('color-red' in classes):
                            isRed = True  
                    text = listItem.text
                    text=repalceAllBadCharacter(text)
                    print(text)
                    isAvailable = False
                    isApplicable = True
                    if(isRed == False and  isGreen == False):
                        isApplicable = False
                    elif(isRed == True):   
                        isApplicable = True
                    elif(isGreen == True):
                        isAvailable = True
                        isApplicable = True 
                    changingRooms.append({
                                "isAvailable": isAvailable,
                                 "isApplicable": isApplicable,
                                "value": text
                   })
        else:
                changingRooms=None
        print(changingRooms)
            
        otherPolicies=soup.find(class_="tab-data venue-highlights highlights")
        if(otherPolicies!=None):
            otherPoliciesList=[]
            for listItem in otherPolicies.find_all("li"):
                isRed = False
                isGreen = False
                span = listItem.find('span')
                if(span != None):
                    classes = span.get('class');
                    if('color-green' in classes):
                        isGreen = True
                    elif('color-red' in classes):
                        isRed = True  
                text = listItem.text
                text=repalceAllBadCharacter(text)
                print(text)
                isAvailable = False
                isApplicable = True
                if(isRed == False and  isGreen == False):
                    isApplicable = False
                elif(isRed == True):   
                    isApplicable = True
                elif(isGreen == True):
                    isAvailable = True
                    isApplicable = True 
                otherPoliciesList.append({
                            "isAvailable": isAvailable,
                             "isApplicable": isApplicable,
                            "value": text
                        })
        else:
            otherPoliciesList=None
        print(otherPoliciesList)
        
       
                
        
        scrappedvenue={
                "venueTitle":venueTitle,
                "venueTypes":venueTypeList,
                "metadata":{
                "likes":likes,
                "pastBookings":pastBookings,
                "views":views,
                "pastShortlist":pastShortlist
                },
                "venueDescription":venueDescription,
                "pricePerPlate":{
                "veg":vegAmount,
                "nonVeg":nonVegAmount,
                },
                "liquior":liquiorAmount,
                "venueContact":venueContact,
                "venueAddress":venueAddress,
                "timings":timings,
                "venueCloseTiming":venueCloseTiming,
                "venueLandmark":venueLandmark,
                "usp":usps,
                "venueExpertNotes":venueExpertNotes,
                "summary":summary,
                "decorationPolicies":decorators,
                "foodPolicies":foods,
                "alcoholPolicies":alcohols,
                "taxes":taxes,
                "cancellationPolicies":cancellationPolicies,
                "advancePolicies":advancePolicies,
                "parkingPolicies":parkings,
                "lodgingPolicies":lodgings,
                "changingRoomsPolicies":changingRooms,
                "otherPolicies":otherPoliciesList,
                "vm_venueid": venue["_id"],
                "vm_id": venue["vm_id"],
                "city": venue["city"],
                "vm_venue_name": venue["name"]
                }
     
        resultData=scrappedvenues.count({"vm_venueid":venue["_id"]})
        # resultData=resultData.count()
        #print(resultData)
        #resultData=resultData.count()
        
        if(resultData>0):
            result=scrappedvenues.update_one({"vm_venueid":venue["_id"]},{"$set":scrappedvenue})
            urlsToScraps.replace_one({"isDone":True},{"isDone":False})
    return result

scrapeUrl(readData)