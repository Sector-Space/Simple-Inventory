import sys, time, os, pyperclip

#Users with passwords
users = {'user1': 'password', 'user2': 'securepassword'}

#All the different inventories
inventory1 = {'Title': 'Inventory 1', 'Torches': 6, 'Gold Coins': 42, 'Daggers': 1}
inventory2 = {'Title': 'Inventory 2', 'Flashlights': 6, 'Nails': 42, 'Hammers': 1}
inventory3 = {'Title': 'Inventory 3', 'Rockets': 5, 'Computers': 3, 'Parachutes': 7}

#The inventories each user can access 
#NOTE it would be good if this is changed per users in the users dictionary
userInventories = {'user1': [inventory1, inventory2], 
                   'user2': [inventory1, inventory2, inventory3]}

#A list of all the inventories
allInventories = [inventory1, inventory2, inventory3]

userLoop = True

#Attempts allowed for login on each password and username
allowedAttempts = 5

#The main program loop, it takes the username for displaying the correct inventories allowed
def mainPageLoop(username):

    #Get the inventories a user can acess with the dictionary
    inventoryGroup = userInventories.get(username)

    #The loop for user input
    while True:
        os.system('cls')
        print('<:>>' + username + '/Main')
        #To find the number of inventories the user can access
        numberOfInventories = 0
        
        #Prints out the inventories and counts them
        if len(inventoryGroup) != 0:
            for i in range(len(inventoryGroup)):
                print(str(i+1) + ': ' + inventoryTitle(inventoryGroup[i]))
                numberOfInventories = i + 1
        else:
            print('Error: There are no inventories to display!')
        
        #User Prompt                                                                      #TODO if there are no inventories this is funky
        promptAnswer1 = input(f'Enter the number of the inventory you would like to access (1-{str(numberOfInventories)}) or (h) for help: ')

        #To check if the user entererd the command to quit
        if promptAnswer1.isalpha():
            #Change to lowercase for less user/program confusion
            promptAnswer1 = promptAnswer1.lower()

            #To quit
            if promptAnswer1 == 'q':
                print('Quitting...')
                quit(1)

            #To save data 
            #By setting the user inventories to the inventory group that got changed
            elif promptAnswer1 == 's':

                #Doesn't actually do anything becuase both things refrence the same objects, the save option will only do something when external file support is added.
                print('Saving...')
                userInventories[username] = inventoryGroup
                print('Done.')

                pressEnter(0)

            #To print the possible commands to the help screen
            elif promptAnswer1 == 'h':
                print('''Type in a command to execute or a number to enter an inventory \nAvailable commands are:
                  
            h : to show this help screen
            q : to quit the program
            s : to save the current data* Doesn't really save becuase there is no support for outside files

            rm : to remove an inventory from list, takes the number of the inventory
                      
            add : to create an inventory
                ''')
                pressEnter(0)

            #To remove an inventory from the list
            elif promptAnswer1 == 'rm':
                inventoryToRemove = input(f'Which inventory (1-{str(numberOfInventories)}) would you like to remove?: ')

                #Check that the input is a valid input
                if inventoryToRemove.isdecimal():
                    #Convert answer to an int to be used as the index for the list of dictionaries
                    inventoryToRemove = int(inventoryToRemove)

                    #If the response is a valid index
                    if inventoryToRemove <= numberOfInventories and inventoryToRemove != 0:
                        #Remove the inventory
                        print(f'Are you sure you want to remove {inventoryTitle(inventoryGroup[inventoryToRemove-1])}?')
                        pressEnter(.1)
                        del inventoryGroup[inventoryToRemove-1]
                        print('Done.')
                    else:
                        print('Input not in range. Please enter a valid input.')
                else:
                    print('The input is not a valid input. Please try again.')

                pressEnter(0)
                
            #To create an inventory
            elif promptAnswer1 == 'add':
                #Ask for an inventory name
                inventoryName = input('What do you want to name the inventory?: ')

                #To know if the inventory name was flagged as already used
                nameInInventory = False

                #Cycle through inventories looking for the entered name
                for index in range(len(allInventories)):

                    #Find the name of each inventory
                    name = allInventories[index].get('Title')

                    if inventoryName == name:
                        nameInInventory = True
                        break
                    else:
                        #name not in inventory
                        continue

                #If the name showed up during the checking
                if nameInInventory:
                    print('Sorry inventory title already exists (either in user or global). Please enter valid name')

                #If the inventory name wasn't flagged create the inventory
                else:
                    print('Creating inventory with name ' + inventoryName)
                    #Make a version of the inventory name with no spaces for use later with naming
                    noWhiteInventoryName = ''.join(inventoryName.split())
                    #Create dictionary seperatly, and add to all inventories and then the inventoryGroup
                    inventoryGroup.append(createInventory(noWhiteInventoryName, inventoryName))
                    #Adds to username inventories once saved
                
                pressEnter(0)

            #If no valid text command inputted
            else:
                print('Please enter a valid input.')

        elif promptAnswer1.isdecimal():
            #Convert answer to an int to be used as the index for the list of dictionaries
            promptAnswer1 = int(promptAnswer1)

            #If the response is a valid index
            if promptAnswer1 <= numberOfInventories and promptAnswer1 != 0:
                #Enter the inventory page
                inventoryPageLoop(inventoryGroup[promptAnswer1-1])
            else:
                print('Input not in range. Please enter a valid input.')
        
        #If no vaild inputs found
        else:
            print('Please enter a valid input.')

        #Time before refreshing the screen
        time.sleep(1)

#Displays the inventory page
def inventoryPageLoop(inventory):

    #The loop for user input
    while True:
        #Clears the screen, prints header, and can manipulate the inventory
        os.system('cls')

        #For use in the header
        newInventoryTitle = '_'.join(inventoryTitle(inventory).split())

        #Print everything to the screen
        print('<:>>' + username + '/' + newInventoryTitle)        #To show the user where they are in the program
        print((f' {inventoryTitle(inventory)} ').center(30, '=')) #To display the inventory title
        printInventory(inventory, 20, 8)

        #The user prompt
        promptAnswer2 = input('What would you like to do? (h for help)')

        #To check user commands
        if promptAnswer2.isalpha():
            promptAnswer2 = promptAnswer2.lower()

            #To return to the Main Page
            if promptAnswer2 == 'b':
                break

            #To quit the program
            if promptAnswer2 == 'q':
                print('Quitting...')
                quit(1)

            #To print the possible commands to the help screen
            elif promptAnswer2 == 'h':
                print('''Available commands are:
                  
            b : to return to main
            h : to show this help screen
            q : to quit the program

            add : to add an item to the inventory
            del : to delete an item from the inventory
            mod : to modify the amount of an item
            raw : to copy the raw inventory data to your clipboard
            ren : to rename an item

            retitle : to change the name of the current inventory
            deldata : to delete all the data in the inventory
                ''')
                pressEnter(.5)
            
            #To add an item to the inventory
            elif promptAnswer2 == 'add':
                newItem = input('What do you want to name the new item?: ')

                #Check if the item already exists
                if newItem in inventory.keys():
                    print('Sorry, ' + newItem + ' already exists.')
                else: 
                    newItemValue = input('What shall be the value of ' + newItem + '?: ')

                    #Make sure it is a number and then add it too the list of items
                    if newItemValue.isdecimal():
                        print('Adding ' + newItem + ' to inventory.')
                        inventory[newItem] = int(newItemValue)
                        time.sleep(.2)
                        print('Done.')
                    else:
                        print('Unvalid entry. Please enter an integer.')

                pressEnter(0)

            #To delete an item from the inventory
            elif promptAnswer2 == 'del':
                delItem = input('Type exactly the item you want to remove: ')

                #Check if the item is there and then delete it
                if delItem in inventory.keys():
                    del inventory[delItem]
                else:
                    print('No item matches for, ' + delItem)

                pressEnter(0)

            #To change the amount of an item *Possibly rename
            elif promptAnswer2 == 'mod':
                item = input('Which item would you like to change?: ')

                #If the item exists then change it
                if item in inventory.keys():
                    newValue = input('To what should the value be?: ')
                    inventory[item] = int(newValue)
                
                else:
                    print('Sorry ' + item + ', Does not exist.')

                pressEnter(0)

            #To rename an item in the inventory
            elif promptAnswer2 == 'ren':
                #Ask for item and if there is such an item ask for the new name
                item = input('Which item would you like to rename?: ')
                if item in inventory.keys():
                    newName = input('What do you want to rename it to?: ')
                    if newName in inventory.keys():
                        print('There is already an item with that name.')
                    else:
                        print('Renaming ' + item + ' to, ' + newName)
                        #Solution to keep order from https://stackoverflow.com/questions/59196031/how-do-i-rename-a-key-while-preserving-order-in-dictionaries-python-3-7
                        replacement = {item: newName}
                        for k in list(inventory.keys()):
                            inventory[replacement.get(k, k)] = inventory.pop(k)

                #What to do if there is no item that they entered
                else:
                    print('Sorry ' + item + ', Does not exist.')

                pressEnter(0)

            #To rename the title of the inventory
            elif promptAnswer2 == 'retitle':
                #Ask for new title and change the value of title to the new title
                newTitle = input('What would you like to rename the inventory?: ')
                inventory['Title'] = newTitle
                print('Done.')
                pressEnter(0)

            #To copy the raw inventory data into the clipboard
            elif promptAnswer2 == 'raw':
                print('Copying the raw inventory data into clipboard...')
                pyperclip.copy(str(inventory))
                time.sleep(.3)
                print('Done.')
                pressEnter(0)

            #To delete all the data in the inventory, excluding the title
            elif promptAnswer2 == 'deldata':
                print('Are you sure you want to delete all the data in this inventory?')
                pressEnter(0)

                for k in list(inventory.keys()):
                    #Delete everything that is not the title
                    if k != 'Title':
                        del inventory[k]

                print('Done.')
                pressEnter(0)

            #If no valid text command was entered
            else:
                print('Please enter a valid input.')
                time.sleep(1)

        #If no vaild inputs found
        else:
            print('Please enter a valid input.')
            time.sleep(1)
    
    #Say to user that they are returning to main
    print('Returning to Main...')

#Finds and returns the title of the inventory given
def inventoryTitle(inventory):
    #Returns 'no title' if no title was found
    inventoryTitle = inventory.get('Title', 'No Title')
    return inventoryTitle

#Print inventory data in a formatted form, takes the inventory, and the left and right justify values
def printInventory(inventory, leftWidth, rightWidth):
    #Loop through and display items left and right justified
    for k, v in inventory.items():
        #Excludes the tile from the inventory values
        if k != 'Title':
            print(k.ljust(leftWidth) + str(v).rjust(rightWidth))

    #Adds and extra line for cleanness
    print()

#For use in creating an inventory takes the name and the name without whitespaces
#Returns a new dictionary/inventory with the name given
def createInventory(noWhiteName, name):
    #Create new dictionary/inventory with name

    #Makes a dictionary and then turns it into one with the name of noWhiteName, it is how it is because the inventory needs to be made in the global setting
    global x
    x = noWhiteName
    globals()[str(x)] = {'Title': str(name)}
    noWhiteName = {'Title': str(name)}

    #print(noWhiteName)

    #Add it to the list of all the inventories
    allInventories.append(noWhiteName)

    #For debugging
    #print(allInventories)

    return noWhiteName

#For a pause in the program askign for user to continue
def pressEnter(delay):
    waitForEnter = input('Enter to continue...')
    #Time before screen refresh
    time.sleep(delay)

#An easy function to call and quit the program
def quit(secs):
    time.sleep(secs)
    sys.exit()


###### MAIN PROGRAM STARTS BELOW ######


#Clear screen and begin
os.system('cls')
print(f'Running From: {os.getcwd()}')
print()
print('Welcome to Simple Inventory.')
print()

#TODO Get the credentials and data from saved files
    #Find File
    #Decrypt data
    #Pickout data
    #Set the found data
    #Close file

#The loop for asking for logging in
while userLoop:
    #To keep track of login attempts
    userAttempts = 0
    passwordAttempts = 0

    #If login attempts are under a limit allow user to try and log in
    while userAttempts < allowedAttempts:
        username = input('Enter username: ')
        username = username.lower()

        #If the username is in users ask for the password
        if username in users.keys():

            #If password attempts are under a limit ask them to enter their password
            while passwordAttempts < allowedAttempts:
                time.sleep(.4)
                password = input('What is the password for, ' + username + '?: ')

                #Keep going if password is correct, get password here to not have the correct one stored before it is needed
                if password == users.get(username):
                    time.sleep(.4)
                    print('Password sucessful. Logging in...')
                    time.sleep(.7)

                    #Enter the main loop/database
                    mainPageLoop(username)
                    print('Main page escaped. Will quit')
                    quit(1)

                #If the password is not correct
                else:
                    time.sleep(.4)
                    print('Password is not correct.')
                    passwordAttempts += 1
                    print('Used Password Attempts: ' + str(passwordAttempts) + '/' + str(allowedAttempts))
                print()

        #If username is not registered
        else:
            time.sleep(.4)
            print('Username is not registerd.')
            userAttempts += 1
            print('Used Username Attempts: ' + str(userAttempts) + '/' + str(allowedAttempts))
            print()
            continue

        break
    
    #What to do when attempts are used up    
    print('Attempts maxed out, quitting...')
    quit(1)