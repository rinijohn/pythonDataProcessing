"""
Program: finalProject_rjohn_07.py
Author:  Rini Lilly John
Purpose: Program that dynamically plots a graph based on data from csv files and inputs from user.
Revisions:
    00: Reading from a CSV File.
    01: Reading as rows from the File.
    02: Modifying the data.
    03: Filtering required data.
    04: Logic to calculate average.
    05: Logic to form <select>.
    06: Plotting the plotly graph.
    07: Fine tuning the graph.
"""

import csv #module to handle csv files
from datetime import datetime #module to handle date & time converions
import plotly.graph_objs as go #module to handle graphs
import plotly.offline as py #module to plot and visualize graphs

#STEP 0
announcement = "Analysis of Commodity Data"
print('='*len(announcement)+'\n'+announcement+'\n'+'='*len(announcement)+'\n')

#STEP 1
with open('produce_csv.csv','r') as csvfile: #opening the produce_csv file
    reader = csv.reader(csvfile)    #reader function to read the file
    data = [row for row in reader]  #reading each row from the reader object
print(f'{data[:5]=}') #for testing purposes only

#STEP 2
locations = data.pop(0)[2:] #Extracting only the locations as a list
print(f'{locations=}') #for testing purposes only

#STEP 3
modifiedData = []   #New list that will contain the modified data
for row in data:    #traversing each row in data
    newRow = list() #creating the new row that will be appened into modifiedData
    for item in row:    #traversing each item in the row
        if '$' in item: #checking if the item is a price value
            newRow.append(float(item.replace('$', ''))) #removing '$'and converting to float & appending it to the new row
        elif '/'in item:#checkingif the item is a date
            newRow.append(datetime.strptime(item, '%m/%d/%Y')) #converting date string to a date format & appending it to the new row
        else: #when item is neither a date nor a price
            newRow.append(item)
    modifiedData.append(newRow) #Appending newly formatted row to modifiedData
    
#STEP 4
print(f'{modifiedData[:5]=}') #for testing purposes only

#STEP 5
records = list()    #list to store each record
for row in modifiedData:    #traversing through each row in modifiedData
    newRow = row[:2]    #extracting name and date for a particular item
    for location, price in zip(locations, row[2:]):   #traversing through the item and its corresponding price
        records.append(newRow+[location, price])    #Adding the list to the records
        
#STEP 6
print(f'{records[:5]=}') #for testing purposes only

#STEP 7
products = sorted(list(set([x[0] for x in records])))
print(f'{products[:5]=}') #for testing purposes only
print('SELECT PRODUCTS BY NUMBER ...')
for itemNo,product in enumerate(products):
    print(f"{f'<{itemNo:>2}> {product}':<25}",end=' ')  #formatting output
    if (itemNo + 1)% 3 == 0:
        print()
print()

#STEP 8
userInput = input('Enter product number seperated by spaces: ').strip().split()
productList = [products[int(i)] for i in userInput]
print('Selected product: '+', '.join(productList)+'\n')

#STEP 9
dates = sorted(list(set([datetime.strftime(x[1],'%Y-%m-%d') for x in records])))
for itemNo,x in enumerate(dates):
    print(f"<{itemNo:>2}> {x}",end=' ') #formatting output
    if (itemNo + 1)% 5 == 0:
        print()
print('\nEarliest available date is: ',dates[0])
print('Latest available date is: ',dates[-1])

#STEP 10
startDate, endDate = input('Enter start/end date numbers separated by a space:').strip().split()
startDate, endDate = dates[int(startDate)], dates[int(endDate)]
print(f'Dates from {startDate} to {endDate}\n')

#STEP 11
print('SELECT LOCATIONS BY NUMBER ...')
locations.sort()
for itemNo,location in enumerate(locations):
    print(f'<{itemNo}> {location}')
    
#STEP 12
userInput = input("Enter location numbers separated by spaces: ").strip().split()
locationList = [locations[int(i)] for i in userInput]
print('Selected locations: '+', '.join(locationList))

#STEP 13
select = [x for x in records if x[0] in productList and datetime.strftime(x[1],'%Y-%m-%d')>=startDate and datetime.strftime(x[1],'%Y-%m-%d')<=endDate and x[2] in locationList]
print(f'{select[:5]=}') #for testing purposes only
print(f'{len(select)} records have been selected.')

#STEP 14
recordDict = {} #Creating a dictionary
for x in productList:   #Adding product,location as keys to the dictionary
    for y in locationList:
        recordDict.update({(x,y):[]})
print(recordDict) #for testing purposes only
for row in select:
    recordDict[(row[0],row[2])].append(row[3]) #Aggregating prices for the given product,location 
print(recordDict) #for testing purposes only

#STEP 15
for row in recordDict:
    if (len(recordDict[row])>0): #Checking if price list is empty
        recordDict[row]=round(sum(recordDict[row])/len(recordDict[row]),2) # calculating the avergae of price list
    else:
        recordDict[row]=0
print(recordDict) #for testing purposes only

#STEP 16
titleString = f"Product prices from {startDate} through {endDate}"
print(titleString) #for testing purposes only
traceData = []
#for product, location in recordDict:
for location in locationList:   #travesring location-wise
    traceData.append( go.Bar(   #appending the traces to a trace list
        x = productList,    #x-axis wil contains list of products
        y = [recordDict[(product,location)] for product in productList], #accessing the average price of a product in a location and adding to a list
        name = location #y-axis conatins the respective location
        ))
layout = go.Layout(title=titleString, barmode='group', xaxis_title='Product', yaxis_title='Average Price',yaxis_tickprefix='$', yaxis_tickformat=',.2f') #Creating a layout
fig = go.Figure(data=traceData, layout=layout) #Creating a figure
py.plot(fig, filename='graph1.html') #Creating a html file with results












