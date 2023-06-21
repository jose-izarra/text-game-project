from fake_characters import *
from tkinter import *

# class that creates each room in the game
class Room:
    def __init__(self, name, description, exits, items, enemies):
        self.name = name
        self.description = description
        self.exits = exits
        self.items = items
        self.enemies = enemies if enemies is not None else []

    def get_exits(self):
        return list(self.exits)

    def enemy_count(self):
        return len(self.enemies)

class Item:
    def __init__(self, name, description, use_function):
        self.name = name
        self.description = description
        self.use_function = use_function  # stores a function to perform when used 

    def use(self, character):
        self.use_function(character)

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

def heal(character):
    # this function is used for items, when used increase health by 50
    character.health = min(100, character.health + 50)
    message3 = "50 health restored."
    return message3

def boost_stealth(character):
    # this function is used for items, when used increase stealth by 10
    character.stealth += 10
    message5 = "Stealth increased by 10."
    return message5

def boost_strength(character):
    # this function is used for items, when used increase strength by 10
    character.strength += 10
    message2 = "Strength increased by 10."
    return message2

def boost_dexterity(character):
    # this function is used for items, when used increase dexterity by &0
    character.dexterity += 10
    message6 = "Dexterity increased by 10."
    return message6

def boost_health_helmet(character):
    # this function is used for items, when used increase health by 20 and strength by 5
    character.health += 20
    character.strength += 5
    message7 = "Health increased by 20 and Strength increased by 5."
    return message7

DD = "Dragon Dungeon"
HF = "Haunted Forest"
R1 = "Road 1"
BF = "Battlefield"
EC = "Enemy Castle"
R2 = "Road 2"
B1 = "Bridge 1"
SF = "Spawn Field"
B2 = "Bridge 2"
R3 = "Road 3"
Doc = "Doctor"
Mage = "Mage laboratory"
R4 = "Road 4"
GC = "Goblin cave"
OC = "Ogre cave"
EOC = "Entry of the castle"
VL = "Village of the hero"
R5 = "Road 5"
F1 = "Field 1"
F2 = "Field 2"
KR = "The King's Room"
AR = "Armorer"
R6 = "Road 6"
OVL = "Other village"
SFO = "Safe forest"

# This is the matrix reprensentig the world each abbreviation is a room
# there are 25 rooms on a 5x5 map
World = [
        [DD, HF,R1, BF, EC],
        [R2, B1, SF, B2, R3],
        [Doc, Mage, R4, GC, OC],
        [EOC, VL, R5, F1, F2],
        [KR, AR, R6, OVL, SFO]
        ]

# this temp is used in line 243 of gui_creation.py to pass into find_room_indices function
temp = [
        ["DD", 'HF','R1', 'BF', 'EC'],
        ['R2', 'B1', 'SF', 'B2', 'R3'],
        ['Doc', 'Mage', 'R4', 'GC', 'OC'],
        ['EOC', 'VL', 'R5', 'F1', 'F2'],
        ['KR', 'AR', 'R6', 'OVL', 'SFO']
        ]

def find_room_indices(world, room_key):
    #the goal of this function is to find the index of the room in the matrix World
    for i, row in enumerate(world):
        for j, room in enumerate(row):
            if room == room_key:
                return i, j
    
name_to_key = {
    "Dragon Dungeon": "DD",
    "Haunted Forest": "HF",
    "Road 1": "R1",
    "Battlefield": "BF",
    "Enemy Castle": "EC",
    "Road 2": "R2",
    "Bridge 1": "B1",
    "Spawn Field": "SF",
    "Bridge 2": "B2",
    "Road 3": "R3",
    "Doctor": "Doc",
    "Mage laboratory": "Mage",
    "Road 4": "R4",
    "Goblin cave": "GC",
    "Ogre cave": "OC",
    "Entry of the castle": "EOC",
    "Village of the hero": "VL",
    "Road 5": "R5",
    "Field 1": "F1",
    "Field 2": "F2",
    "The King's Room": "KR",
    "Armorer": "AR",
    "Road 6": "R6",
    "Other village": "OVL",
    "Safe forest": "SFO"
}

# added this function to be able to access the key pair values in other docs
def room_to_abbrev():
    global name_to_key
    return name_to_key

#information on every room in order to create rooms later with the class
room_data = {
    "DD": {"description": "You are in a dark and terrifying Dragon Dungeon.", 
            "exits": {}, "items":[], "enemies":[]},
    "HF": {"description": "You have entered a Haunted Forest, filled with eerie sounds and shadows.",  
            "exits": {}, "items":[], "enemies":[]},
    "R1": {"description": "You are on Road 1, a dusty path leading to the Dragon Dungeon.", 
            "exits": {}, "items":[], "enemies":[]},
    "BF": {"description": "You find yourself on a Battlefield, littered with the remnants of a great war.", 
            "exits": {}, "items":[], "enemies":[]},
    "EC": {"description": "You stand at the entrance of the Enemy Castle, with its towering walls and menacing gates.", 
            "exits": {}, "items":[], "enemies":[]},
    "R2": {"description": "You are on Road 2, a quiet path running along the castle's walls.", 
            "exits": {}, "items":[], "enemies":[]},
    "B1": {"description": "You have reached Bridge 1, a sturdy wooden structure crossing a deep river.", 
            "exits": {}, "items":[], "enemies":[]},
    "SF": {"description": "You are in the Spawn Field, a peaceful meadow with beautiful flowers and singing birds.", 
            "exits": {}, "items":[], "enemies":[]},
    "B2": {"description": "You have reached Bridge 2, a stone bridge spanning a wide river.", 
            "exits": {}, "items":[], "enemies":[]},
    "R3": {"description": "You are on Road 3, a path filled with travelers heading to the nearby village.", 
            "exits": {}, "items":[], "enemies":[]},
    "Doc": {"description": "You are in the Doctor's office, a place of healing and knowledge.", 
            "exits": {}, "items":[], "enemies":[]},
    "Mage": {"description": "You have entered the Mage Laboratory, filled with magical artifacts and mysterious potions.", 
            "exits": {}, "items":[], "enemies":[]},
    "R4": {"description": "You are on Road 4, an ancient path that connects the Mage Laboratory to the Goblin Cave.",
            "exits": {}, "items":[], "enemies":[]},
    "GC": {"description": "You have entered the Goblin Cave, a dark and damp place filled with strange creatures.",
            "exits": {}, "items":[], "enemies":[]},
    "OC": {"description": "You have discovered the Ogre Cave, where large ogres dwell and plan their attacks.", 
            "exits": {}, "items":[], "enemies":[]},
    "EOC": {"description": "You are at the Entry of the Castle, with its magnificent architecture and imposing towers.", 
            "exits": {}, "items":[], "enemies":[]},
    "VL": {"description": "You have arrived at the Village of the Hero, a bustling place filled with brave adventurers.", 
            "exits": {}, "items":[], "enemies":[]},
    "R5": {"description": "You are on Road 5, the main street of the Village of the Hero.", 
            "exits": {}, "items":[], "enemies":[]},
    "F1": {"description": "You are in Field 1, a vast, open field where farmers work tirelessly to grow crops.", 
            "exits": {}, "items":[], "enemies":[]},
    "F2": {"description": "You are in Field 2, a fertile area filled with lush vegetation and a variety of crops.", 
            "exits": {}, "items":[], "enemies":[]},
    "KR": {"description": "You have entered the King's Room, an opulent chamber adorned with luxurious furnishings.", 
            "exits": {}, "items":[], "enemies":[]},
    "AR": {"description": "You are in the Armorer's workshop, surrounded by weapons, armor, and skilled craftsmen.", 
            "exits": {}, "items":[], "enemies":[]},
    "R6": {"description": "You are on Road 6, a well-traveled path that leads to another village.", 
            "exits": {}, "items":[], "enemies":[]},
    "OVL": {"description": "You have arrived at the Other Village, a peaceful settlement filled with friendly villagers.", 
            "exits": {}, "items":[], "enemies":[]},
    "SFO": {"description": "You are in the Safe Forest, a serene place teeming with life and natural beauty.", 
            "exits": {}, "items":[], "enemies":[]}
}

#creating Item
potion = Item("Potion", "A potion that restores 50 points of health up to a 100.", heal)
scroll = Item("Magic Scroll", "A scroll containing a powerful spell.", boost_strength)
crown = Item("King's Crown", "The crown of the king.", boost_dexterity)
gem = Item("Spooky Gem", "A mysterious gem found in the Haunted Forest.", boost_stealth)
sword = Item("Enchanted Sword", "A powerful sword infused with magic.", boost_strength)
shield = Item("Shiny Shield", "A strong shield that can protect from enemy attacks.", boost_dexterity)
helmet = Item("Battle Helmet", "A sturdy helmet worn by warriors.", boost_health_helmet)


# dictionary calls the enemy class generation in fake_characters
enemy_groups = {
    "Goblin": goblins,
    "Orcs": orcs,
    "Dragon": dragons,
    "Boss": bosses,
    "Undead": undead,
}


# add enemy
room_data["DD"]["enemies"].extend(enemy_groups["Dragon"])  # Dragon Dungeon - dragon
room_data["HF"]["enemies"].extend(enemy_groups["Undead"])  # Haunted Forest - undead
room_data["OC"]["enemies"].extend(enemy_groups["Orcs"])  # Ogre Cave - orcs
room_data["EC"]["enemies"].extend(enemy_groups["Boss"])  # Entry of the Castle - boss
room_data["GC"]["enemies"].extend(enemy_groups["Goblin"])  # Goblin Camp - goblins

#add items
room_data["Doc"]["items"].append(potion)
room_data["Mage"]["items"].append(scroll)
room_data["KR"]["items"].append(crown)
room_data["GC"]["items"].append(gem)
room_data["BF"]["items"].append(helmet)
room_data["AR"]["items"].append(shield)
room_data["SF"]["items"].append(potion)
room_data["F1"]["items"].append(potion)
room_data["OVL"]["items"].append(sword)
room_data["SFO"]["items"].append(potion)
room_data["R6"]["items"].append(potion)
def update_exits(World, room_data):
    #update exits assign all the possible exits of each room
    #if it is possible to go south, north... it is added to exit if not it is not added
    #it uses the matric world
    for i in range(len(World)):
        for j in range(len(World[i])):
            room_name = World[i][j]
            room_key = name_to_key[room_name]
            exits = {}

            if i > 0:
                exits["north"] = name_to_key[World[i - 1][j]]
            if i < len(World) - 1:
                exits["south"] = name_to_key[World[i + 1][j]]
            if j > 0:
                exits["west"] = name_to_key[World[i][j - 1]]
            if j < len(World[i]) - 1:
                exits["east"] = name_to_key[World[i][j + 1]]

            room_data[room_key]["exits"] = exits
    return room_data


# Update room_data exits based on World grid

def create_rooms(room_data):
    #this function create all the rooms through a for loop in order to be more efficien
    #it uses the dictionary of dictionary room_data to do it
    rooms = {}
    for key, data in room_data.items():
        rooms[key] = Room(key, data["description"], data["exits"], items=data['items'], enemies=data['enemies'])
    return rooms

def describe_room(room):
    #Describe room inform the player on the number of enemies and which item are in the room
    description = room.description

    # Check for enemies in the room
    if room.enemy_count() > 0:
        print(f"There is {room.enemy_count()} enemy in this room.")
        description += f"\nThere is {room.enemy_count()} enemy in this room!"
    else:
        print("There are no enemies in this room.")
        description += "\nThere are no enemies in this room."

    # Check for items in the room
    if len(room.items) > 0:
        item_names = ', '.join([item.name for item in room.items])
        print(f"There are these items in the room: {item_names}")
        description += f"\nThere are these items in the room: {item_names}"
    else:
        print("There are no items in this room.")
        description += "\nThere are no items in this room."

    return description

    





def prepare_data():
    #prepare data just update the exits and create room at once, it makes it easier and shaper for
    #some par in the GUI
    global room_data
    room_data = update_exits(World, room_data)
    rooms= create_rooms(room_data)
    return rooms

rooms= prepare_data()

#Jose map
def create_map(canvas, rooms):
    #This function create the map using the rooms
    x_counter = 90
    y_counter = 40
    rect_width = 140
    rect_height = 30
    line_width = 1
    line_color = "#2D2D2D"
    rect_fill = "#1C1C1C"

    # Configure text color, size, and font
    text_color = "#FF8C00"  # Dark orange color
    text_size = 12
    text_font = ("Times New Roman", text_size, "bold")  # Using Courier font

    for i, row in enumerate(World): #world is the matrix representing the map
        for j, room_name in enumerate(row):

            # Draw rectangle
            canvas.create_rectangle(x_counter - rect_width // 2, y_counter - rect_height // 2,
                                    x_counter + rect_width // 2, y_counter + rect_height // 2,
                                    width=line_width, fill=rect_fill, outline=line_color)

            # Draw room name
            canvas.create_text(x_counter, y_counter, text=room_name, fill=text_color, font=text_font)

            x_counter += rect_width + line_width

        x_counter = 90
        y_counter += rect_height + line_width


if __name__ == '__main__':
    room_data = update_exits(World, room_data)
    rooms = create_rooms(room_data)
    current_room = rooms["SF"]  # Start in the Spawn Field
    describe_room(current_room)