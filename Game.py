import random
import turtle
class GameStart(object):
    def __init__(self, count):
        self.count = count
        print ("There are ", self.count, "players playing.")
    def YouWin(self, winner):
        print("You are the winner: " + winner.name + "! Congratulations!!! :)")
        winner.win = True
    def YouLose(self, loser):
        print ("Sorry: "+ loser.name + " you have lost! :(")
        loser.lose = True
    def Draw(self):
        print ("This Game is a draw. Nobody won but at least nobody lost! :|")
    def GameOver(self):
        print("This game is over! I hope you all had fun! :)")
    def GameOn(self):
        names = ["Mr. Green", "Ms. Scarlet", "Ms. Peacock", "Prof. Plum", "Col. Mustard", "Mrs. White"]
        rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room","Billiard Room", "Library", "Cellar", "Study", "Lounge"]
        weapons = ["Candlestick", "Knife", "Lead Pipe", "Pistol", "Rope", "Wrench"]
        playing = self.count - 1
        Players = []
        File = []
        Rooms =[]
        Halls = []
        Navi = []
        mCardList = []
        kCardList = []
        wn = turtle.Screen()
        control = 0
        # initialize the players
        while control <= playing:
            name = names[control]
            Players.append(Player(name, control))
            control = control + 1
        #create the confidential file
        rand2 = random.randint(0, len(names) - 1)
        File.append(ConfCards(names[rand2], "Suspect"))
        del names[rand2]
        rand2 = random.randint(0, len(rooms)-1)
        File.append(ConfCards(rooms[rand2], "Room"))
        del rooms[rand2]
        rand2 = random.randint(0, len(weapons)-1)
        File.append(ConfCards(weapons[rand2], "Weapon"))
        del weapons[rand2]
        #give the players the remaining suspect cards
        length = len(names)
        x = 0
        control = 0
        test = 1
        while x < length:
            if control > playing:
                control = 0
            rand2 = random.randint(0, len(names)-1)
            Players[control].AddCard(Cards(names[rand2], Players[control].name, "Suspect"))
            mCardList.append(Cards(names[rand2], Players[control].name, "Suspect"))
            del names[rand2]
            control += 1
            x = x+1
        #give the remaining room cards
        length = len(rooms)
        x = 0
        control = 0
        while x < length:
            if control > len(Players)-1:
                control = 0
            rand2 = random.randint(0, len(rooms)-1)
            Players[control].AddCard(Cards(rooms[rand2], Players[control].name, "Room"))
            mCardList.append(Cards(rooms[rand2], Players[control].name, "Room"))
            del rooms[rand2]
            control = control+1
            x = x + 1
        #give the remaining weapon cards
        length = len(weapons)
        x = 0
        control = 0
        while x < length:
            if control > len(Players)-1:
                control = 0
            rand2 = random.randint(0, len(weapons)-1)
            Players[control].AddCard(Cards(weapons[rand2], Players[control].name, "Weapon"))
            mCardList.append(Cards(weapons[rand2], Players[control].name, "Weapon"))
            del weapons[rand2]
            control = control+1
            x = x+1
        x = 0
        #Create the Halls
        while x < 16:
            Halls.append(Hall(x))
            x += 1
        #Occupy the start points in Halls
        Halls[0].Occupied()
        Halls[1].Occupied()
        if playing > 1:
            for x in range (2,len(Players)):
                if x == 2:
                    Halls[7].Occupied()
                if x == 3:
                    Halls[10].Occupied()
                if x == 4:
                    Halls[14].Occupied()
                if x == 5:
                    Halls[15].Occupied()

        #Create the entry points for the Halls
        y =0
        while y < len(Halls):
            Halls[y].Enter()
            y = y+1
        #Create the Rooms
        rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Cellar", "Study","Lounge"]
        for i in rooms:
            Rooms.append(Room(i))
        y = 0
        #Create entry points for rooms
        while y < len(Rooms):
            Rooms[y].Enter()
            y = y+1
        #Create the navigation list
        for h in Halls:
            Navi.append(h)
        for r in Rooms:
            Navi.append(r)
        #let the players take turns until they win, or all of them lose
        losers = 0
        x = -1
        while losers < playing + 1 and Players[x].win == False:
            x = x + 1
            while Players[x].lose == True:
                x = x + 1
                if x > playing:
                    x = 0
            Players[x].Turn(Players, Navi, kCardList, mCardList, File)
            if Players[x].lose == True:
                self.YouLose(Players[x])
                losers = losers + 1
            if Players[x].win == True:
                self.YouWin(Players[x])
        if losers == playing +1:
            self.Draw()
        self.GameOver()

class Player (object):
    def __init__(self, name, count):
        self.win = False
        self.lose = False
        self.skip = False
        self.card = []
        self.name = name
        self.count = count + 1
        print("Player",self.count," is ", self.name)
        if self.count == 1:
            self.location = "Hall_1"
        if self.count == 2:
            self.location = "Hall_2"
        if self.count == 3:
            self.location = "Hall_7"
        if self.count == 4:
            self.location = "Hall_10"
        if self.count == 5:
            self.location = "Hall_14"
        if self.count == 6:
            self.location = "Hall_15"
    def Help(self, k):
        print("Player", self.count, " cards are:")
        for x in self.card:
            print (x.name)
        print("Known cards are: ")
        for x in k:
            print ("Owner: ", x.owner)
            print("Card:", x.name)
    def AddCard(self,object):
        self.card.append(object)
    def Turn (self, players, nav, kcards, mcards, conf):
        rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Cellar", "Study", "Lounge"]
        print ("It is now the turn of ", self.name)
        print("What would you like to do? Enter the number for the option you would like:")
        print("1 = Navigate the Game Board:")
        print("2 = Make a Suggestion:")
        print("3 = Make an Accusation:")
        print("4 = Skip:")
        print("5 = Look at all of the available cards:")
        turn = int(input('What would you like to do?'))
        valid = False
        for x in rooms:
            if self.location == x:
                valid = True
        while turn < 1 or turn > 5 or ((turn == 2 or turn == 3) and valid == False):
            turn = int(input ("You have entered an invalid option please try again (6 is the max, 2 is the minimum): "))
        while turn == 5:
            self.Help(kcards)
            self.lose = False
            turn = int(input('What else would you like to do?'))
            print("1 = Navigate the Game Board:")
            print("2 = Make a Suggestion:")
            print("3 = Make an Accusation:")
            print("4 = Skip:")
            print("5 = Look at all of the available cards:")
        if turn == 1:
            self.Navigate(nav)
        if turn == 2 and valid == True:
            self.Suggest(players, kcards, mcards, conf)
        if turn == 3 and valid == True:
            count = self.Suggest(players, kcards, mcards, conf)
            self.Accuse(count, kcards)
        if turn == 4:
            self.lose = False
    def Navigate(self,loc):
        x = 0
        while x < len(loc):
            if loc[x].name == self.location:
                break
            x = x + 1
        turn = "Y"
        while turn == "Y":
            print ("Here are your navigation options: ",loc[x].canEnter)
            nav = str (input("Where would you like to go?:"))
            y = 0
            while y < len(loc[x].canEnter[y]):
                if nav == loc[x].canEnter[y]:
                    break
                y = y + 1
            if nav == loc[x].canEnter[y]:
                w = 0
                while loc[x].canEnter[y] != loc[w].name:
                    w = w + 1
                if loc[w].type == Hall and loc[w].occupied == True:
                    print ("This hall is occupied and you cannot enter")
                    turn = str(input("If you would like to try to re-enter a location enter Y, if you would like to exit enter anything else to Quit: "))
                else:
                    print ("You are able to navigate")
                    self.location = loc[w].name
                    turn = "Q"
            if nav != loc[x].canEnter[y]:
                print("Your input was invalid")
                turn = str(input("If you would like to try to re-enter a location enter Y, if you would like to exit enter anything else to Quit: "))
    def Suggest(self, players, kcards, mcards):
        names = ["Mr. Green", "Ms. Scarlet", "Ms. Peacock", "Prof. Plum", "Col. Mustard", "Mrs. White"]
        rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billiard Room", "Library", "Cellar", "Study", "Lounge"]
        weapons = ["Candlestick", "Knife", "Lead Pipe", "Pistol", "Rope", "Wrench"]
        valid = 0
        print("These are your suspect options:")
        for x in names:
            print(x)
        print("These are your weapon options:")
        for x in weapons:
            print(x)
        while valid < 2:
            suspect = str(input("Enter suspect suggestion: "))
            room = self.location
            print("Your room selection is your current location")
            weapon = str(input("Enter weapon suggestion: "))
            valid = 0
            for x in names:
                if suspect == x:
                    valid = valid + 1
            for x in weapons:
                if weapon == x:
                    valid = valid + 1
            if valid < 2:
                print("Error with one of your entries. Please enter them again")
        y = 0
        count = 0
        for x in players:
            if suspect == x.name:
                x.locattion = self.location
        while y < len(mcards):
            if suspect == mcards[y].name:
                print (mcards[y].name, " is owned by: ", mcards[y].owner)
                mcards[y].hidden = False
                kcards.append(mcards[y])
                count = count + 1
            if weapon == mcards[y].name:
                print(mcards[y].name, " is owned by: ", mcards[y].owner)
                mcards[y].hidden = False
                kcards.append(mcards[y])
                count = count + 1
            if room == mcards[y].name:
                print(mcards[y].name, " is owned by: ", mcards[y].owner)
                mcards[y].hidden = False
                kcards.append(mcards[y])
                count = count + 1
            y = y + 1
        print("There were ",str(count) + " cards you suggested incorrectly.")
        return count
    def Accuse(self, count, kcards):
        if count > 0:
            self.lose = True
            for x in self.card:
                kcards.append(x)
        if count == 0:
            self.win = True
class ConfCards (object):
    def __init__(self, name, type):
        self.confidential = True
        self.owner = "NULL"
        self.hidden = True
        self.name = name
        self.type = type

class Cards (object):
    def __init__(self, name, owner, type):
        self.name = name
        self.owner = owner
        self.type = type
        self.confidential = False
        self.hidden = True

class Room (object):
    def __init__(self, name):
        self.occupied = False
        self.corner = False
        self.canEnter = []
        self.name = name
        self.type = "Room"
    def Enter(self):
        # rooms = ["Kitchen", "Ballroom", "Conservatory", "Dining Room", "Billard Room", "Library", "Cellar", "Study","Lounge"]
        if self.name == "Kitchen":
            self.corner = True
            self.canEnter.append("Hall_1")
            self.canEnter.append("Hall_3")
            self.canEnter.append("Study")
        if self.name == "Conservatory":
            self.corner = True
            self.canEnter.append("Hall_2")
            self.canEnter.append("Hall_7")
            self.canEnter.append("Lounge")
        if self.name == "Lounge":
            self.corner = True
            self.canEnter.append("Hall_10")
            self.canEnter.append("Hall_15")
            self.canEnter.append("Conservatory")
        if self.name == "Study":
            self.corner = True
            self.canEnter.append("Hall_14")
            self.canEnter.append("Hall_16")
            self.canEnter.append("Kitchen")
        if self.name == "Ballroom":
            self.corner = False
            self.canEnter.append("Hall_1")
            self.canEnter.append("Hall_2")
            self.canEnter.append("Hall_5")
        if self.name == "Dining Room":
            self.corner = False
            self.canEnter.append("Hall_3")
            self.canEnter.append("Hall_8")
            self.canEnter.append("Hall_10")
        if self.name == "Billiard Room":
            self.corner = False
            self.canEnter.append("Hall_7")
            self.canEnter.append("Hall_9")
            self.canEnter.append("Hall_14")
        if self.name == "Library":
            self.corner = False
            self.canEnter.append("Hall_12")
            self.canEnter.append("Hall_15")
            self.canEnter.append("Hall_16")
        if self.name == "Cellar":
            self.corner = False
            self.canEnter.append("Hall_5")
            self.canEnter.append("Hall_8")
            self.canEnter.append("Hall_9")
            self.canEnter.append("Hall_12")

class Hall (object):
    def __init__(self, count):
        self.name = "Hall_"+str(count+1)
        self.occupied = False
        self.canEnter = []
        self.type = "Hall"
    def Occupied(self):
            self.occupied = True
    def Enter(self):
        if self.name == "Hall_1":
            self.canEnter.append("Kitchen")
            self.canEnter.append("Ballroom")
            self.canEnter.append("Hall_4")
        if self.name == "Hall_2":
            self.canEnter.append("Hall_6")
            self.canEnter.append("Ballroom")
            self.canEnter.append("Conservatory")
        if self.name == "Hall_3":
            self.canEnter.append("Hall_4")
            self.canEnter.append("Kitchen")
            self.canEnter.append("Dining Room")
        if self.name == "Hall_4":
            self.canEnter.append("Hall_1")
            self.canEnter.append("Hall_3")
            self.canEnter.append("Hall_5")
            self.canEnter.append("Hall_8")
        if self.name == "Hall_5":
            self.canEnter.append("Hall_4")
            self.canEnter.append("Hall_6")
            self.canEnter.append("Ballroom")
            self.canEnter.append("Cellar")
        if self.name == "Hall_6":
            self.canEnter.append("Hall_2")
            self.canEnter.append("Hall_5")
            self.canEnter.append("Hall_7")
            self.canEnter.append("Hall_9")
        if self.name == "Hall_7":
            self.canEnter.append("Hall_2")
            self.canEnter.append("Hall_5")
            self.canEnter.append("Hall_7")
            self.canEnter.append("Hall_9")
        if self.name == "Hall_8":
            self.canEnter.append("Hall_4")
            self.canEnter.append("Hall_11")
            self.canEnter.append("Dining Room")
            self.canEnter.append("Cellar")
        if self.name == "Hall_9":
            self.canEnter.append("Cellar")
            self.canEnter.append("Hall_6")
            self.canEnter.append("Hall_13")
            self.canEnter.append("Billiard Room")
        if self.name == "Hall_10":
            self.canEnter.append("Dining Room")
            self.canEnter.append("Hall_11")
            self.canEnter.append("Lounge")
        if self.name == "Hall_11":
            self.canEnter.append("Hall_8")
            self.canEnter.append("Hall_10")
            self.canEnter.append("Hall_12")
            self.canEnter.append("Hall_15")
        if self.name == "Hall_12":
            self.canEnter.append("Hall_11")
            self.canEnter.append("Hall_13")
            self.canEnter.append("Cellar")
            self.canEnter.append("Library")
        if self.name == "Hall_13":
            self.canEnter.append("Hall_12")
            self.canEnter.append("Hall_9")
            self.canEnter.append("Hall_14")
            self.canEnter.append("Hall_6")
        if self.name == "Hall_14":
            self.canEnter.append("Billiard Room")
            self.canEnter.append("Study")
            self.canEnter.append("Hall_13")
        if self.name == "Hall_15":
            self.canEnter.append("Lounge")
            self.canEnter.append("Hall_11")
            self.canEnter.append("Library")
        if self.name == "Hall_16":
            self.canEnter.append("Library")
            self.canEnter.append("Hall_13")
            self.canEnter.append("Study")

print ("Would you like to play Clue?")
go = input ("Enter Y for Yes and N for No: ")
while go != "Y" and go != "N":
    go = input("You have entered an invalid option please try again (Y is Yes and N is No): ")
while go == "Y":
    counter = int(input("How many players would like to play? (6 is the max, 2 is the minimum): "))
    while counter < 2 or counter > 6:
        counter = int (input ("You have entered an invalid number of players please try again (6 is the max, 2 is the minimum): "))
    Game = GameStart(counter)
    Game.GameOn()
    print("Would you like to play Clue again?")
    go = input("Enter Y for Yes and N for No: ")
    while go != "Y" and go != "N":
        go = input("You have entered an invalid option please try again (Y is Yes and N is No): ")
print ("Ok cool! :) Have a great day!")