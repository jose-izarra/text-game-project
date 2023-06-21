import random

# class for creating the main character
class Character:
    def __init__(self, type, callback=None):
        self.type = type
        self.level = 1
        self.health = 100 # initial & max health
        self.current_room = 'SF' # starting room
        self.inventory = []
        self.experience = 0
        self.callback = callback
        
        # selects stats for different characters
        if self.type == 'mage': 
            self.name = 'Alice The Mage'
            self.dexterity = 8 + self.level
            self.strength = 13 + self.level
            self.stealth = 6 + self.level
            self.tracking = 4 + self.level
        elif self.type == 'thief':
            self.name = 'Bob the Thief'
            self.dexterity = 9 + self.level
            self.strength = 12 + self.level
            self.stealth = 8 + self.level
            self.tracking = 6 + self.level
        elif self.type == 'hunter':
            self.name = 'Charlie the Hunter'
            self.dexterity = 7 + self.level
            self.strength = 14 + self.level
            self.stealth = 5 + self.level
            self.tracking = 9 + self.level
        elif self.type == 'swordsman': 
            self.name = 'Dave the Swordsman'
            self.dexterity = 6 + self.level
            self.strength = 17 + self.level
            self.stealth = 4 + self.level
            self.tracking = 5 + self.level        
        else: 
            raise ValueError('Please input a valid character')

    def take_item(self, room, item):
        # takes the item from the room and adds it to the inventory
        taken_item = room.take_item(item)
        if taken_item is not None:
            self.inventory.append(taken_item)
            print(f"{taken_item.name} has been added to your inventory.")

    def use_item(self, item):
        # uses the item
        if item in self.inventory:
            item.use()
            self.inventory.remove(item)
        else:
            print("You don't have this item in your inventory.")

    def attack(self, target):
        # method for dealing damage to the enemy
        hit_chance = self.dexterity * 0.1
        rand = random.randint(0,1)
        if hit_chance >= rand:
            damage = int(self.strength + self.strength*0.2)
            target.health -= damage
            print(f"{self.name} hit {target.type} for {damage} damage!")
        else:
            print(f"{self.name} missed {target.type}!")
            damage = 0 
        return damage

    def gain_experience(self, enemy):
        # adds experience to the player after defeating an enemy
        experience_needed = 10 + self.level * 10  # Example: 100 experience needed per level
        self.experience += enemy.experience  # Add experience from enemy

        # if the experience of the player is enough, level up 
        if self.experience >= experience_needed:
            self.level_up()
            self.experience -= experience_needed  # Reset experience towards next level

    def level_up(self):
        # boosts the characters attributes to become stronger
        self.level += 1
        self.dexterity += 10
        self.strength += 10
        self.stealth += 10
        self.tracking += 10
        self.health += 20
        self.experience_needed = 10 + self.level * 10
        self.callback(f"You leveled up to level {self.level}!\n"
                f"You now have {round(self.health)} health and {round(self.experience)} experience points.\n"
                f"You need {round(self.experience_needed)} experience points to level up again.")
        
    def stats(self):
        # returns a string with all the current stats of the player
        stats = f"Name: {self.name}\nLevel: {self.level}\nHealth: {self.health}\nExperience: {self.experience}\nDexterity: {self.dexterity}\nStrength: {self.strength}\nStealth: {self.stealth}\nTracking: {self.tracking}"
        return stats

class Enemy:
    def __init__(self, type, level):
        self.type = type
        self.level = level
        
        # assigns the values for each of the enemies 
        if self.type == 'goblin': 
            self.dodge = 0.4  # probability that it dodges
            self.weak_to = 'swordsman' # weak to this character type
            self.experience = 10  # experience it gives when it dies
            self.health = 7  + round(self.level * 1.5) # health it takes to be killed
            self.damage = 7  # base damage
        elif self.type == 'orc': 
            self.dodge = 0.2
            self.weak_to = 'mage' 
            self.experience = 10
            self.health = 20 + round(self.level * 1.5)
            self.damage = 5
        elif self.type == 'dragon': 
            self.dodge = 0.1
            self.weak_to = 'hunter' 
            self.experience = 50
            self.health = 150 + round(self.level * 1.5)
            self.damage = 17
        elif self.type == 'undead': 
            self.dodge = 0.6
            self.weak_to = 'mage' 
            self.experience = 5
            self.health = 6 + round(self.level * 1.5)
            self.damage = 4
        elif self.type == 'boss': 
            self.dodge = 0.8
            self.weak_to = 'hunter' 
            self.experience = 100
            self.health = 300 + round(self.level * 1.5)
            self.damage = 20

    def attack(self, character):
        hit_chance = random.random()
        
        if hit_chance < self.level/character.dexterity:
            damage = round(self.level + random.randint(0, 25))
            character.health -= damage
            print(f"The {self.type} hit {character.name} for {damage:.1f} damage!")
            return damage
        else:
            print(f"The {self.type} missed!")

# generates enemys for each type with a range of possible levels     
goblins = [Enemy("goblin", random.randint(1, 5))]
orcs = [Enemy("orc", random.randint(5, 10)) ]
dragons = [Enemy("dragon", random.randint(10, 15)) ]
undead = [Enemy("undead", random.randint(3, 8))]
bosses = [Enemy("boss", random.randint(15, 20))]


# List of available characters
characters = [
    Character('mage'),
    Character("thief"),
    Character("hunter"),
    Character("swordsman"),
]

if __name__ == '__main__':
    # Code for testing this file
    print("Select your character:")
    for i, character in enumerate(characters):
        print(f"{i + 1}. {character.name}")
    
    choice = int(input("Enter your choice (1-4): "))
    if choice < 1 or choice > 4:
        print("Invalid choice.")
        exit()

    player = characters[choice - 1]
    print(player.name)
    
