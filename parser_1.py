# This program will be used to create a parser for the text adventure game. The parser would have the capabilities of
# a) Recognize the verbs and nouns in the input from a predetermined dictionary of verbs and nouns with many synonyms
# and alternatives.
# b) Join the verbs and nouns to specific actions that are then communicated to the gui, and then to the relevant
# receiver (e.g. go up would communicate with the gui, which in turn connects to the word to update the current room in
# the player class and move the player).
# d) Uses the library logging to log the actions of the parser.

import logging

logger = logging.getLogger('parser')
logger.addHandler(logging.NullHandler())


class Parser:
    def __init__(self, command):
        self.command = command
        
        # creates a list of all the accepted verbs that the player can input as valid
        self.accepted_verbs = {
            '': '',
            'resume': 'continue',
            'advance': 'continue',
            'attack': 'attack',
            'pounce': 'attack',
            'hit': 'attack',
            'assault': 'attack',
            'harm': 'attack',
            'hurt': 'attack',
            'stab': 'attack',
            'shoot': 'attack',
            'kill': 'attack',
            'consume': 'eat',
            'eat': 'eat',
            'devour': 'eat',
            'swallow': 'eat',
            'ingest': 'eat',
            'chew': 'eat',
            'munch': 'eat',
            'nibble': 'eat',
            'bite': 'eat',
            'back': 'back',
            'open': 'open',
            'unlock': 'open',
            'reveal': 'open',
            'unblock': 'open',
            'close': 'close',
            'shut': 'close',
            'bolt': 'close',
            'secure': 'close',
            'lock': 'close',
            'block': 'close',
            'drop': 'drop',
            'abandon': 'drop',
            'dump': 'drop',
            'release': 'drop',
            'leave': 'drop',
            'enter': 'go',
            'go': 'go',
            'walk': 'go',
            'move': 'go',
            'travel': 'go',
            'head': 'go',
            'proceed': 'go',
            'get': 'take',
            'take': 'take',
            'grab': 'take',
            'collect': 'take',
            'pick up': 'take',
            'seize': 'take',
            'acquire': 'take',
            'snatch': 'take',
            'obtain': 'take',
            'listen': 'listen',
            'hear': 'listen',
            'overhear': 'listen',
            'eavesdrop': 'listen',
            'hint': 'hint',
            'advice': 'hint',
            'idea': 'hint',
            'information': 'hint',
            'inventory': 'inventory',
            'access': 'inventory',
            'look': 'look',
            'glance': 'look',
            'peer': 'look',
            'read': 'look',
            'see': 'look',
            'study': 'look',
            'view': 'look',
            'gaze': 'look',
            'peep': 'look',
            'observe': 'look',
            'spot': 'look',
            'inspect': 'look',
            'examine': 'look',
            'search': 'look',
            'check': 'look',
            'score': 'score',
            'help': 'help',
            'use': 'use',
            'stats': 'stats'
            }
        
        # creates a list of all the accepted verbs that the player can input as valid
        self.accepted_nouns = {
            '': '',
            'u': 'north',
            'up': 'north',
            'd': 'south',
            'down': 'south',
            'l': 'west',
            'left': 'west',
            'r': 'east',
            'right': 'east',
            'n': 'north',
            'north': 'north',
            's': 'south',
            'south': 'south',
            'e': 'east',
            'east': 'east',
            'w': 'west',
            'west': 'west',
            'sword': "Enchanted Sword",
            'Sword': "Enchanted Sword",
            'scroll': "Magic Scroll",
            'Scroll': "Magic Scroll",
            'potion': "Potion",
            'Potion': "Potion",
            'crown': "King's Crown",
            'Crown': "King's Crown",
            'gem': "Spooky Gem",
            'Gem': "Spooky Gem",
            'shield': "Shiny Shield",
            'Shield': "Shiny Shield",
            'helmet': "Battle Helmet",
            'Helmet': "Battle Helmet",
        }
    
    def parse(self):
        command = self.command.lower()
        command = self.command.split()

        verb = ''
        noun = ''
        for word in command:
            if word in self.accepted_verbs:
                verb = self.accepted_verbs[word]
            elif word in self.accepted_nouns:
                noun = self.accepted_nouns[word]
            else:
                print(f'{word} is not a valid command.')

        self.possible_actions = print("The verb you inputted is: {}, and the noun is: {}.".format(verb, noun))
        return verb, noun

