import uuid
import random

# google
from google.oauth2 import id_token
from google.auth.transport import requests


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


def validate_google_token(token, client_id):

    try:
        id_info = id_token.verify_oauth2_token(
            token, requests.Request(), client_id
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            return None

        data = {
            'email': id_info['email'],
        }

        return data

    except ValueError:
        return None
