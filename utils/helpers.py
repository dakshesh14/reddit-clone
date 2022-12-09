import uuid
import random


def get_uuid():
    return str(uuid.uuid4())[:8]


prefixes = [
    "Fluffy", "Fuzzy", "Sparky", "Kitty", "Puppy", "Bunny", "Cuddles", "Smokey",
    "Peanut", "Buttercup", "Sugar", "Sweetie", "Kisses", "Bubbles", "Angel", "Cupcake",
    "Darling", "Love", "Honey", "Baby", "Snuggles", "Cotton", "Puddles", "Cupid", "Pookie",
    "Lucky", "Giggles", "Dream", "Star", "Lovebug", "Honeybun", "Cupcake", "Sugarplum",
    "Sweetpea", "Honeydew", "Butterbean", "Peaches", "Kissy", "Tootsie", "Honeybee",
    "Muffin", "Cupcake", "Sweetiepie", "Snickerdoodle", "Snuggly", "Cuddlebug", "Butterball",
    "Sugarbear"
]
suffixes = [
    "Tiger", "Lion", "Panda", "Giraffe", "Zebra", "Leopard", "Hippo",
    "Rhino", "Elephant", "Cheetah", "Wolf", "Fox", "Bear", "Moose", "Deer",
    "Raccoon", "Squirrel", "Skunk", "Rabbit", "Hedgehog", "Otter", "Badger",
    "Beaver", "Mink", "Weasel", "Ferret", "Sable", "Marten", "Marmot",
    "Muskrat", "Porcupine", "Seal", "Walrus", "Whale", "Dolphin", "Shark",
    "Octopus", "Squid", "Lobster", "Crab", "Eel", "Jellyfish", "Starfish",
    "Coral", "Apple", "Banana", "Orange", "Pear", "Peach", "Plum", "Grape",
    "Cherry", "Strawberry", "Raspberry", "Blueberry", "Blackberry", "Lemon",
    "Lime", "Coconut", "Watermelon", "Cantaloupe", "Honeydew", "Mango", "Papaya",
    "Kiwi", "Guava", "Pineapple", "Pomegranate",
]
pre_prefixes = [
    "Super", "Ultra", "Mega", "Hyper", "Turbo",
    "Laser", "Plasma", "Neon", "Quantum", "Giga", "Nano",
    "Atomic", "Galactic", "Cosmic", "Mystic", "Epic", "Legendary",
]


def get_random_name() -> str:
    name = f"{random.choice(prefixes)}{random.choice(suffixes)}"
    if random.random() < 0.2:
        name = f"{random.choice(pre_prefixes)}{name}"
    return name
