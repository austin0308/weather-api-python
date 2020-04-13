import requests

"""
Created by Austin Le
Email: ale3@dmacc.edu
Date: 3/25/2020
"""

class Node:
    """
    A node in a singly-linked list.
    """
    def __init__(self, data=None, next=None):
        self.data = data
        self.next = next

class linkedList:
    def __init__(self):
        self.head = None
        self.queue = []

    def append(self, data):
        if not self.head:
            self.head = Node(data=data)
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = Node(data=data)

    def addToQueue(self):
        current = self.head
        weatherInfo = ''
        while current:
            weatherInfo += str(current.data)
            current = current.next
        self.queue.append(weatherInfo)



    def find(self, key):
        current = self.head
        while current:
            if key.title() in current.data:
                return current.next.data + 'in ' + key.title()
            else:
                current = current.next
        return "Can't find within linked list"  # Will be None if not found
    """
    def remove(self, key):
        current = self.head
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        # Unlink it from the list
        if prev is None:
            self.head = current.next
        elif current:
            prev.next = current.next
            current.next = None
    """
    def reverse(self):
        current = self.head
        prev_node = None
        next_node = None
        while current:
            next_node = current.next
            current.next = prev_node
            prev_node = current
            current = next_node
        self.head = prev_node

    def printList(self):
        current = self.head
        while current:
            print(current.data)
            current = current.next

    def printQueue(self):
        for x in self.queue:
            print(x)

# Code execution starts here
if __name__ == '__main__':


    promptUserForZipCode = raw_input('Please Enter Zip Code: ')
    llist = linkedList()
    while promptUserForZipCode != '-999':
        try:

            # makes an API call
            apiCall = "https://api.openweathermap.org/data/2.5/weather?zip=" + promptUserForZipCode + ",us&appid=e679c963c847aaf2fea95221eee2ec65"

            # gets json response
            response = requests.get(apiCall).json()

            # kelvin unit to convert to F
            kelvin = 273.15;

            # parsing json
            temp = response["main"]["temp"];
            tempHigh = response["main"]["temp_max"];
            tempLow = response["main"]["temp_min"];
            humidity = response["main"]["humidity"];
            windSpeed = response["wind"]["speed"];
            cloudCover = response["clouds"]["all"];
            city = response["name"];
            country = response["sys"]["country"];
            description = response["weather"][0]["description"];

            # convert temp from K to F
            temp = ((temp - kelvin) * 9 / 5) + 32;
            tempHigh = ((tempHigh - kelvin) * 9 / 5) + 32;
            tempLow = ((tempLow - kelvin) * 9 / 5) + 32;

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
            llist.append('Humidity: ' + str(__humidity) + '% ')
            llist.append('Wind Speed: ' + str(__windSpeed) + ' MPH  ')
            llist.append('Cloud Cover: ' + str(__cloudCover) + '%  ')
            llist.append('Description: ' + str(__description).title())

            llist.addToQueue()
            promptUserForZipCode = raw_input('Please Enter Zip Code: ')

        except:
            print('error')
    #llist.printQueue()
    print(llist.find("Urbandale"))
    print(llist.find("johnston"))
    llist.reverse()
    llist.printList()