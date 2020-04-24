import requests

"""
Created by Austin Le
Email: ale3@dmacc.edu
Date: 3/25/2020

This project demonstrates a linked list, a queue/list, and a simple sort.
User enters in a zip code, which then makes an API call. Each attribute, such as
temp, high temp, wind speed, etc., is a node within a linked list. Once the API call is
done, it creates a linked list, which then appends each node to a queue. 

Then it deletes all the nodes so it doesn't add up and up when user continuously enters in zip. But, the previous 
city checked was stored in a queue, so no lost data.

When the user decided to stop, it will prompt the user to search queue for city, sort queue baased on city name,
make more calls, or exit

Here is the link to the API I used: https://openweathermap.org/current
Anyone can sign up for a free account to obtain their API key.
Then you can start making API calls!
"""


# Class for Linked List
class Node:
    # default contructor for head, and next value
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


# Class that will do API calls, appending queue with weather information,
# sorting, printing, etc.
class linkedList:
    # default constructor
    def __init__(self):
        self.head = None
        self.temp = 0
        self.tempHigh = 0
        self.tempLow = 0
        self.humidity = 0
        self.windSpeed = 0
        self.cloudCover = 0
        self.city = 'City'
        self.country = 'US'
        self.description = 'Clear Skies'
        self.queue = []

    # adds a new node
    def append(self, data):
        if not self.head:
            self.head = Node(data=data)
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(data=data)

    # adds to the queue
    def addToList(self):
        current = self.head
        weatherInfo = ''
        while current:
            weatherInfo += current.data
            current = current.next
        self.queue.append(weatherInfo)

    # finds a certain item within queue
    def find(self, key):
        print('\n')
        for x in self.queue:
            if key.title() in x:
                return x
        return "Sorry, " + key.title() + " was not in the list. Perhaps you didn't check that city?"
    
    # print list
    def printList(self):
        for x in self.queue:
            print(x)

    def removeCityFromQueue(self, cityName):
        for x in self.queue:
            if cityName in x:
                self.queue.remove(x)
                return '\n\n' + cityName.title() + ' has been removed.'
        return "Sorry, " + cityName.title() + " was not in the list. Perhaps you didn't check that city?"

    def printCitiesChecked(self):
        numberOfSpaces = 2
        for x in self.queue:
            city = x.split('  ')
            ' '.join(city[:numberOfSpaces]), ' '.join(city[numberOfSpaces:])
            print(city[0])


    def sortAndPrintList(self):
        print('\n*** Before Sort ***')
        self.printList()
        self.queue.sort()
        print('\n*** After Sort ***')
        self.printList()

    # clears the linked list, so they don't add up and up every time a user
    # enters in a zip code
    def deleteExistingNodes(self):
        # makes the head None
        current = self.head = None
        # iterates through each node to delete
        while current:
            del current.next.data
            current = current.next

    # function to make an API call
    def makeAPICall(self, llist):

        # asks for user input
        promptUserForZipCode = raw_input('Please Enter Zip Code (-999 to Exit): ')

        while promptUserForZipCode != '-999':
            try:
                # makes an API call
                apiCall = "https://api.openweathermap.org/data/2.5/weather?zip=" + promptUserForZipCode + ",us&appid=e679c963c847aaf2fea95221eee2ec65"

                # gets json response
                response = requests.get(apiCall).json()

                # kelvin unit to convert to F
                kelvin = 273.15

                # to convert windspeed from m/s to MPH
                windSpeedConversion = 2.237

                # sets values by parsing the JSON response.
                # also, formats the float values to 0 decimals
                self.temp = "%.0f" % float((((response["main"]["temp"] - kelvin) * 9) / 5) + 32) # convert from Kelvin to Fahrenheit
                self.tempHigh = "%.0f" % float((((response["main"]["temp_max"] - kelvin) * 9) / 5) + 32) # convert from Kelvin to Fahrenheit
                self.tempLow = "%.0f" % float((((response["main"]["temp_min"] - kelvin) * 9) / 5) + 32) # convert from Kelvin to Fahrenheit
                self.humidity = "%.0f" % float(response["main"]["humidity"])
                self.windSpeed = "%.0f" % float(((response["wind"]["speed"] * windSpeedConversion) + response["wind"]["speed"])) # convert from m/s to MPH
                self.cloudCover = ("%.0f" % response["clouds"]["all"])
                self.city = response["name"]
                self.country = response["sys"]["country"];
                self.description = response["weather"][0]["description"]

                # creates a new linked list
                llist.append('City: ' + str(self.city) + ' ')
                llist.append('Current Tempurature: ' + str(self.temp) + ' F  ')
                llist.append('High Tempurature: ' + str(self.tempHigh) + ' F  ')
                llist.append('Low Tempurature: ' + str(self.tempLow) + ' F  ')
                llist.append('Humidity: ' + str(self.humidity) + '%  ')
                llist.append('Wind Speed: ' + str(self.windSpeed) + ' MPH  ')
                llist.append('Cloud Cover: ' + str(self.cloudCover) + '%  ')
                llist.append('Description: ' + str(self.description).title())

                # adds to list
                llist.addToList()

                # deletes all nodes
                llist.deleteExistingNodes()

                # promt user input again
                promptUserForZipCode = raw_input('Please Enter Zip Code (-999 to Exit): ')
            except:
                # try catch statement to if they have an error
                # in their zip code, or an error trying to make the request
                print('\n\nSorry, there was an error')
                promptUserForZipCode = raw_input('Make sure the zip code is 5 digits, and double-check it is valid (-999): ')
                print('\n')

    # once the user is done adding cities,
    # there are some prompts to do some tasks
    def promptUserForAction(self, llist):

        print('\n\n*** Cities Checked So Far ***')
        llist.printList()
        # displays what actions user can do
        promptUserAction = raw_input(
            '\nEnter 0: Sort List Based on City Name\nEnter 1: Search for City\nEnter 2: Get Weather '
            'Info for Different City\nEnter 3: Print Current List\nEnter 4: Remove City\nEnter 5: Exit\n\nPlease Make Selection: ')

        while promptUserAction != '5':
            # sorts and prints list
            if promptUserAction == '0':
                llist.sortAndPrintList()
            # searches list for city
            elif promptUserAction == '1':
                promptForCity = raw_input('Please Enter the City Name: ')
                print(llist.find(promptForCity))
            # makes more API calls
            elif promptUserAction == '2':
                llist.makeAPICall(llist)
            elif promptUserAction == '3':
                print('\n*** Cities You Have Checked ***')
                llist.printList()
            elif promptUserAction == '4':
                print('\n\n*** Cities You Can Remove ***')
                llist.printCitiesChecked()
                cityToRemove = raw_input('\nWhat city do you want to remove?: ')
                print(llist.removeCityFromQueue(cityToRemove.title()))
                print('\n\nList After Removal')
                llist.printList()
            promptUserAction = raw_input(
                '\nEnter 0: Sort List Based on City Name\nEnter 1: Search for City\nEnter 2: Get Weather '
                'Info for Different City\nEnter 3: Print Current List\nEnter 4: Remove City\nEnter 5: Exit\n\nPlease Make Selection: ')


# main
if __name__ == '__main__':
    # greet user
    print('*** Check Weather Information ***')
    # creates a linkedList object
    llist = linkedList()

    # calls the make API call function and passes the object in
    llist.makeAPICall(llist)

    # prompts user to make decisions
    llist.promptUserForAction(llist)

    # deletes object when the user decides to fully exit
    del llist

    # thank user for using the program
    print('\nThanks for checking the weather!')
