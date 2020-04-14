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
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next


# Class that will do API calls, appending queue with weather information,
# sorting, printing, etc.
class linkedList:
    # default constructor
    def __init__(self):
        self.head = None
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
        for x in self.queue:
            if key.title() in x:
                return x
        return "Sorry, " + key.title() + " was not in the list. Perhaps you didn't check that city?"
        """current = self.head
        while current:
            if key.title() in current.data:
                return current.next.data + 'in ' + key.title()
            else:
                current = current.next
        return "Can't find within linked list"  # Will be None if not found"""

    """def reverse(self):
        current = self.head
        prev_node = None
        next_node = None
        while current:
            next_node = current.next
            current.next = prev_node
            prev_node = current
            current = next_node
        self.head = prev_node"""

    """def printList(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next"""

    # print list
    def printList(self):
        for x in self.queue:
            print(x)

    def sortAndPrintList(self):
        print('\nBefore Sort:')
        self.printList()
        self.queue.sort()
        print('\nAfter Sort:')
        self.printList()

    # clears the linked list, so they don't add up and up every time a user
    # enters in a zip code
    def deleteExistingNodes(self):
        current = self.head = None
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

                # parsing json
                temp = response["main"]["temp"]
                tempHigh = response["main"]["temp_max"]
                tempLow = response["main"]["temp_min"]
                humidity = response["main"]["humidity"]
                windSpeed = response["wind"]["speed"]
                cloudCover = response["clouds"]["all"]
                city = response["name"]
                country = response["sys"]["country"];
                description = response["weather"][0]["description"]

                # convert temp from K to F
                temp = ((temp - kelvin) * 9 / 5) + 32
                tempHigh = ((tempHigh - kelvin) * 9 / 5) + 32
                tempLow = ((tempLow - kelvin) * 9 / 5) + 32

                windSpeedConversion = 2.237

                # converts speed to MPH from m/s
                windSpeed *= windSpeedConversion

                # sets values
                # also, formats the float values to 0 decinals
                __temp = ("%.0f" % temp)
                __tempHigh = ("%.0f" % tempHigh)
                __tempLow = ("%.0f" % tempLow)
                __humidity = ("%.0f" % humidity)
                __windSpeed = ("%.0f" % windSpeed)
                __cloudCover = ("%.0f" % cloudCover)
                __city = city
                __country = country
                __description = description

                # creates a new linked list
                llist.append('City: ' + str(__city) + ' ')
                llist.append('Current Tempurature: ' + str(__temp) + ' F  ')
                llist.append('High Tempurature: ' + str(__tempHigh) + ' F  ')
                llist.append('Low Tempurature: ' + str(__tempLow) + ' F  ')
                llist.append('Humidity: ' + str(__humidity) + '%  ')
                llist.append('Wind Speed: ' + str(__windSpeed) + ' MPH  ')
                llist.append('Cloud Cover: ' + str(__cloudCover) + '%  ')
                llist.append('Description: ' + str(__description).title())

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
                promptUserForZipCode = raw_input('Make sure the zip code is 5 digits and is valid (-999): ')
                print('\n')

    # once the user is done adding cities,
    # there are some prompts to do some tasks
    def promptUserForAction(self, llist):

        # displays what actions user can do
        promptUserAction = raw_input(
            '\nEnter 0: Sort List Based on City Name\nEnter 1: Search for City\nEnter 2: Get Weather '
            'Info for Different City\nEnter 3: Exit\nPlease Make Selection: ')

        while promptUserAction != '3':
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
            promptUserAction = raw_input(
                '\nEnter 0: Sort List Based on City Name\nEnter 1: Search for City\nEnter 2: Get Weather '
                'Info for Different City\nEnter 3: Exit\nPlease Make Selection: ')


# main
if __name__ == '__main__':
    llist = linkedList()

    llist.makeAPICall(llist)
    llist.promptUserForAction(llist)

    del llist

    print('Thanks for checking the weather!')
