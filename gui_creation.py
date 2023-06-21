import tkinter as tk
from tkinter import *
from PIL import Image, ImageTk

import parser_1
import world
import fake_characters

# defining all constant variables
game_width = 1300
game_height = 700
background_color = '#DADADA'
loading_img_url = 'loading_pic.jpg'
starting_room = 'SF'

# dictionary storing the paths for all the images
images_url = {
    "DD" : "dragon_dungeon.jpg",    "HF" : "haunted_forest.jpg","R1" : "road_1.jpg",    "BF" : "battlefield.jpg", 
    "EC" : "enemy_castle.jpg",      "R2" : "road_2.jpg",        "B1" : "bridge_1.jpg",  "SF" : "Spawning_field.jpg", 
    "B2" : "bridge_2.jpg",      "R3" : "road_3.jpg",    "Mage" : "mage_laboratory.jpg", "Doc" : "doctor_office.jpg",
    "R4" : "road_4.jpg",        "GC" : "goblin_cave.jpg", "OC" : "ogre_cave.jpg",   "EOC" : "entry_of_the_castle.jpg", 
    "VL" : "village_of_the_hero.jpg", "R5" : "road_5.jpg",  "F1" : "field_1.jpg",   "F2" : "field_2.jpg",
    "KR" : "king_room.jpg",     "AR" : "armorer.jpg",       "R6" : "road_6.jpg",    "OVL" : "other_village.jpg", 
    "SFO" : "safe_forest.jpg",
}

class Main:
    def __init__(self):
        self.lib_of_rooms = world.rooms  # a dictionary with all the rooms in the game
        self.current_room = self.lib_of_rooms[starting_room]

        self.enemies_dead = 0
        self.types_defeated = []
        self.total_exp = 0
        self.total_items = 0
        self.total_items_used = 0
        self.items_found = 0
        self.total_items_dropped = 0
        self.boss_defeated = False
        
        # this variable stores the exits for all the rooms
        self.exits = world.update_exits(world.World,world.room_data)
        
        # initializing the main game window
        self.main = Tk()
        self.main.title('Rise Of Conquest')  # name still to be defined
        self.main.resizable(False, False)

        # label stating what room we are in
        self.room_in_label = Label(self.main, text='Castle Conquest: Rise of Conquest', font=('consolas', 30))
        self.room_in_label.pack()

        # canvas creates the space where we will put all our features
        self.canvas = Canvas(self.main, bg=background_color, height=game_height, width=game_width)
        self.canvas.pack()

        # load the image
        self.img_open = Image.open(loading_img_url)
        self.img = ImageTk.PhotoImage(self.img_open)
        self.image = self.canvas.create_image(350, 300, anchor=CENTER, image=self.img)

        # creates box for text instructions and log
        self.text_box = Text(self.main, width=50, height=25, font=('consolas', 14))
        self.text_box.config(state=DISABLED)  # makes it so that it can't take an input
        self.canvas.create_window(1000, 300, window=self.text_box)

        # creates input box
        self.input_box = Entry(self.main, width=50, border=5, font=('consolas', 14))
        self.canvas.create_window(1000, 600, window=self.input_box)

        # creates enter button
        self.enter_button = Button(self.main, width=55, text='Enter Answer', font=('consolas', 13),
                                    command=self.__check)
        self.canvas.create_window(1000, 650, window=self.enter_button)
        
        # binds the enter key with the self.check function
        self.main.bind('<Return>', self.__check)

        self.main.update()  # updates the main window

        # setting the geometry and position of the window
        main_width = self.main.winfo_width()
        main_height = self.main.winfo_height()
        screen_width = self.main.winfo_screenwidth()
        screen_height = self.main.winfo_screenheight()

        x = int((screen_width / 2) - (main_width / 2))
        y = int((screen_height / 2) - (main_height / 2))

        self.main.geometry(f'{main_width}x{main_height}+{x}+{y}')

        # welcome message
        self.load_text('Welcome to Castle Conquest: Rise of Conquest! \n\n'
                        'You are a citizen of a land ruled by a corrupt \nleader.'
                        '\nYou embark on a journey to dethrone the tyrant \ngovernment and bring justice to the oppressed. '
                        '\nAlong the way, you will face challenging enemies, gain powerful perks and '
                        'weapons, and grow stronger \nAt any point in time you can always go up, down, \nleft, or right '
                        'with the commands "up","down",\n"left","right", and "inventory" to check your \ninventory. '
                        '\n\nType "Play" to start the game.')

        # counter to be able to tell how many times the player has made a move throughout the game
        # starts at -1 so the initial move doesn't count
        # because it is uploaded in the update_room method which is called in the beginning
        self.move_counter = -1

        self.main.mainloop()

    def __check(self, enter=''):    # the enter parameter is needed because when binding the <<enter>> key to a 
                                    # function 2 parameters are needed in order to work
        # checks if user presses enter
        enterQ = self.get_input()

        if enterQ == 'play':           
            self.start_game()

    def start_game(self):
        # this method runs the initial game conditions
        self.text_box.config(state=NORMAL)  # allows the text box to change its content
        self.text_box.delete('1.0', 'end')  # deletes the initial text
        self.update_image(images_url[starting_room])
        self.createMap()
        self.create_character()

    def create_character(self, input=''):
        # this function is used to display the possible characters to choose from.
        # then, it gets your response and assings the player to a certain character Mage, Thief...
        # for the party
        self.enter_button.config(command=self.create_character) # this two lines are used to re-configure 
        self.main.bind('<Return>', self.create_character)       # the enter button to the function we need
        self.text_box.config(state=NORMAL)
        self.text_box.delete('1.0', 'end')

        characters = ['Mage', 'Thief', "Hunter", 'Swordsman']

        choice = self.get_input()
        
        self.load_text('Select your character!')
        self.load_text('Each character has different attributes and skills\n')

        for i, character in enumerate(characters):  # prints the character list
            self.load_text(f"{i + 1}. {character}")
            
        self.player = False  # variable assigned to see if the player has made a choice
        try:
            # creates the character
            self.player = fake_characters.Character(choice, self.load_text)
        except ValueError:
            pass
        
        if self.player != False:
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', 'end')
            self.load_text(f'Good Choice, your character is now {self.player.name}\n')
            self.load_text(f'Enter "help" to see what commands are available!\n')

            # reconfigures the enter button to call parser function
            self.enter_button.config(command=self.call_parser)
            self.main.bind('<Return>', self.call_parser)
            # updates the starting room
            self.update_room_gui(room=starting_room, i=1, j=2)
       
    def load_text(self, text):
        # uploads text to the in-game text box
        self.text_box.config(state=NORMAL)  # makes it able to add text again
        self.text_box.insert(tk.END, f'{text}\n')
        self.text_box.config(state=DISABLED)
        
    def load_input(self):
        # uploads the input to the text box
        # has a different formatting than normal text (it has the ">> ")
        self.text_box.config(state=NORMAL) 
        self.text_box.insert(tk.END, f'>> {self.input}\n')
        self.text_box.config(state=DISABLED)

    def get_input(self,input=''):
        # takes the input from the user
        input = self.input_box.get().lower()
        self.input_box.delete(0, END)  # deletes the content of the input box
        return input

    def createMap(self):
        # uses create_map function from world.py to display the map in our window
        self.canvas.delete(self.image)  # deletes the loading pic
        rooms = world.prepare_data()
        self.game_map = world.create_map(self.canvas, rooms)

    def update_image(self, imageURL):
        # updates the image url
        self.img = Image.open(imageURL)
        self.img_open = ImageTk.PhotoImage(self.img)

        image_container = self.canvas.create_image(350, 300)
        self.canvas.lower(image_container)
        self.canvas.itemconfig(image_container, image=self.img_open)

    def call_parser(self, input=''):  # takes the input from the parser to decide what to do
        self.input = self.get_input()

        parser = parser_1.Parser(self.input)
        verb, noun = parser.parse()  # assigns a value to the verb and noun
        
        self.accepted_verbs = parser.accepted_verbs
        self.accepted_nouns = parser.accepted_nouns
        
        self.load_input()  # loads the input
        
        # parser returns noun as invalid if the input is not a valid command
        self.perform_action(verb,noun)
    
    def update_room_gui(self, room, i, j): 
        # i and j are the indexes to find the full name of the rooms in the 2D list
        self.update_image(images_url[room])
        
        # updates the room after you move
        self.move_counter += 1
        full_name = world.World[i][j]
        
        # updates the label on the top of the page
        self.room_in_label.config(text='  Room: {}'.format(full_name))
        self.room_in_label.pack()

        # calls the functions from world.py and prints the message for the room you are in
        rooms = world.prepare_data()
        self.load_text(world.describe_room(rooms[room]))  # takes room_abbrev because that is the key to the
                                                          # values in world.py

        # asks question
        self.load_text('\nWhere would you want to go?')

        # this if is to avoid loading the message more than once
        if self.move_counter == 0:
            self.load_text('\nOn the left you have a map of the world so you canknow '
                        'where you are situated at all times and how \nto get to each location\n'
                        '\nScroll down if the page gets full.')

    def change_room(self, direction):
        # change room is the method that allows the player to actually move around the map
        # using the matrix World from world.py
        # changes the room you are in
        room_name_abbrev = self.current_room.name # the name of the room abbreviated, for ex: 'DD'
        
        # this if statement accesses the matrix with the rooms and figures out which way it is going
        if direction in self.exits[room_name_abbrev]['exits']:
            i, j = world.find_room_indices(world.temp, room_name_abbrev)
            if direction == "north":
                self.current_room = self.lib_of_rooms[world.temp[i - 1][j]]
                self.update_room_gui(self.current_room.name, i=i-1, j=j)
            elif direction == "south":
                self.current_room = self.lib_of_rooms[world.temp[i + 1][j]]
                self.update_room_gui(self.current_room.name, i=i+1, j=j)
            elif direction == "east":
                self.current_room = self.lib_of_rooms[world.temp[i][j + 1]]
                self.update_room_gui(self.current_room.name, i=i, j=j+1)
            elif direction == "west":
                self.current_room = self.lib_of_rooms[world.temp[i][j - 1]]
                self.update_room_gui(self.current_room.name, i=i, j=j-1)
        else:
            self.load_text("You cannot go in that direction.")

    def perform_action(self, verb, noun=''):
        # perform action is the function that allows the player to perfom all the possible actions
        # such as taking an item, using an item, asking for help with the commands, changing room, see your stats...
        # it basically use  the parser and some if statements to identify the request
        # check if the verb is valid
        if verb not in self.accepted_verbs:
            print("I don't understand what you mean by '%s'." % verb)
            return

        if verb == 'go':
            # check if there's a valid exit in the current room
            self.change_room(noun)
            # update the room description and image
            #current_room = self.map.get_room(self.player.current_room)
            #self.show_image(current_room.image)

        elif verb == 'look':
            # display the room description and image
            self.load_text(self.current_room.description)
            
            # we will do images if we have enough time
            #self.show_image(current_room.image) 
            
        elif verb == 'attack':
            self.combat()

        elif verb == 'help':
            self.load_text(
                '\nWelcome to the help menu! Here you can find a listof all the commands you can use in the game:\n\n'
                '"go" + <<direction>>: This command will allow you to move in the direction you inputted.\n'
                '"attack": This command attacks the enemy in the room'
                '"take" + <<item>>: This command will allow you to \ntake an item from the room you are in.\n'
                '"drop" + <<item>>: This command will allow you to \ndrop an item from your inventory.\n'
                '"use" + <<potion>>: This command will allow you to consume a potion from your inventory.\n'
                '"inventory": This command will allow you to see the items you have in your inventory.\n'
                '"look": This command will allow you to look around the room you are in.\n'
                '"stats": This command will allow you to look at your current stats\n'
                '"help": This command will allow you to see the \nhelp menu. (But it seems you already know this one:P)')

        elif verb == 'use':
            found_item = None
            # check if the player has the item
            for item in self.player.inventory:
                if item.name == noun:
                    found_item = item
                    break
            if found_item is None:
                self.load_text("You don't have that item.")
                return

            # use the item and update player stats
            found_item.use(self.player)
            
            #cases for all the different items
            if item.name == "Magic Scroll":
                message = world.boost_strength(self.player)
                self.load_text(message)
            elif item.name == "Enchanted Sword":
                message2 = world.boost_strength(self.player)
                self.load_text(message2)
            elif item.name == "Potion":
                message3 = world.heal(self.player)
                self.load_text(message3)
            elif item.name == "King's Crown":
                message4 = world.boost_dexterity(self.player)
                self.load_text(message4)
            elif item.name == "Spooky Gem":
                message5 = world.boost_stealth(self.player)
                self.load_text(message5)
            elif item.name == "Shiny Shield":
                message6 = world.boost_dexterity(self.player)
                self.load_text(message6)
            elif item.name == "Battle Helmet":
                message7 = world.boost_health_helmet(self.player)
                self.load_text(message7)

            self.player.inventory.remove(found_item)

            self.total_items -= 1

            self.total_items_used += 1

        elif verb == 'take':
            # check if the item is in the room
            item = str(self.current_room.items) 
            if noun not in item:
                self.load_text("There's no such item in the room. Please remember to use the notation"
                            " <<verb>> <<noun>>.")
                return

            # add the item to the player's inventory
            item = self.current_room.items[0]
            self.player.inventory.append (item)
            self.current_room.items.remove(item)
            self.load_text("You took the %s." % item)
            self.total_items += 1
            self.items_found += 1

        elif verb == 'inventory':
            # check if the player has any items
            if len(self.player.inventory) == 0:
                self.load_text("You don't have any items.")
                return

            # display the player's inventory
            self.load_text("You have the following items:")
            for item in self.player.inventory:
                self.load_text(f"{item.name}: {item.description}")

        elif verb == 'drop':
            # check if the player has the item
            if noun not in self.player.inventory:
                self.load_text("You don't have that item.")
                return
            elif noun == '':
                self.load_text("You can't drop nothing. Please choose an item from your inventory.")
                return

            # drop the item and remove it from the player's inventory
            if not len(self.player.inventory) == 0:
                index_of_item = 0
                for i in range(len(self.player.inventory)):
                    if self.player.inventory[i] == noun: 
                        index_of_item = i
                        return
            item = self.player.inventory[index_of_item]
            self.current_room.items.append(item)
            self.player.inventory.remove(item)
            self.load_text("You drop the %s." % item)
            self.total_items -= 1
            self.total_items_dropped += 1
        
        elif verb == 'stats':
            # prints the stats of the player
            stats = self.player.stats()
            self.load_text(stats)
        

    def combat(self):
        #this function is used for the combat system of the game
        num_of_enemies = len(self.current_room.enemies)
        if num_of_enemies == 0:
            self.load_text("There's no one to attack.")
        # combat system
        else: 
            enemy = self.current_room.enemies[0]
            damage = self.player.attack(enemy)
            self.load_text(f"You're fighting a Level {enemy.level} {enemy.type}.\n")
            if enemy.health > 0:
                # player attacks first
                self.load_text("You attacked the %s and dealt %d damage." % (enemy.type, damage))
                self.load_text(f"The {enemy.type} now has {enemy.health} health.\n")

                # enemy attacks
                damage = enemy.attack(self.player)

                if self.player.health < 1:
                    self.load_text(f"The {enemy.type} attacks you and deals {damage} damage.\n"
                                   "You now have 0 health left\n"
                                   "\nYOU ARE DEAD! Press enter twice to exit the game")
    
                    self.killer = enemy # saves the name of the enemy that killed you as a variable 
                    
                    # reconfigures the button to run the end_game method
                    self.enter_button.config(command=self.end_game,text='Exit')
                    self.main.bind('<Return>', self.end_game)
                    self.end_scene_counter = 0
                else: 
                    self.load_text(f"The {enemy.type} attacks you and deals {damage} damage.")
                    self.load_text(f'You now have {round(self.player.health)} left')

            # check if the enemy still alive
            if enemy.health < 1:
                if enemy.type == 'boss':
                    self.load_text("You attacked the %s and dealt %d damage." % (enemy.type, damage))
                    self.load_text("\nCongratulations! You defeated the final boss of \nthe game.\n\n"
                                   "You became the hero you were always meant to be \nand will be "
                                   "remembered as a legend in your villagefor centuries!\n\n"
                                   f"You gained {enemy.experience} experience points.\n")
                                   
                    self.current_room.enemies.remove(enemy)
                    self.player.gain_experience(enemy)
                    self.total_exp += enemy.experience
                    self.enemies_dead += 1
                    self.types_defeated.append(enemy.type)
                    
                    self.load_text("\nPress <<Enter>> to see your stats.")
                    
                    self.boss_defeated = True
                    self.enter_button.config(command=self.end_game,text='Exit')
                    self.main.bind('<Return>', self.end_game)
                    self.end_scene_counter = 0
                else: 
                    self.load_text("You attacked the %s and dealt %d damage." % (enemy.type, damage))
                    self.load_text("\nYou defeated the %s!" % enemy.type)
                    self.current_room.enemies.remove(enemy)
                    self.player.gain_experience(enemy)
                    self.load_text(f"You gained {enemy.experience} experience points.")
                    self.total_exp += enemy.experience
                    self.enemies_dead += 1
                    self.types_defeated.append(enemy.type)     

    def level_up(self):
        self.player.gain_experience(self.player)

    def end_game(self, event=None):  # roll end scene
        if self.end_scene_counter == 0:
            self.text_box.config(state=NORMAL)
            self.text_box.delete('1.0', 'end')
            
            if self.boss_defeated == False:
                self.load_text(f"You died at the hands of the {self.killer.type}.\n\n"
                            "You had a good run! \n\n"
                            f"Try again and get revenge on the {self.killer.type} that \nkilled you!")
                if self.enemies_dead < 2:
                    self.load_text(f"\nYou are a disgrace to the human race, \nno wonder your parents left you")
                elif self.enemies_dead >= 2 or self.enemies_dead < 4:
                    self.load_text(f"\n\nOh so you have some skill? \nToo bad it's not good enough")
                else:
                    self.load_text(f"\n\nHmmm..., maybe you are as good as they say you are")
            
            self.load_text(f"Total EXP gained: {self.total_exp}\n\n"
                        f"Total number of items found: {self.items_found}\n\n"
                        f"Total number of items used: {self.total_items_used}\n\n"
                        f"Total number of items dropped: {self.total_items_dropped}\n\n"
                        f"Total number of items remaining: {self.total_items - self.total_items_dropped}\n\n"
                        f"There was a total of 5 enemies\n\n"
                        f"You defeated a total of {self.enemies_dead} / 5 enemies \n\n"
                        f"You defeated these enemies: " + ", ".join(self.types_defeated))

            self.end_scene_counter += 1
        else: 
            self.main.destroy()
        

if __name__ == '__main__':
    game = Main()
