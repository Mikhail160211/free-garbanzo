#!/usr/bin/python

# This is a simple echo bot using the decorator mechanism.
# It echoes any incoming text messages.
import random
import os
import telebot
from config import *
from main import *

bot = telebot.TeleBot(token)
guess_animal = ["Lion", "Tiger", "Elephant", "Giraffe", "Monkey", "Zebra", "Bear", "Wolf", "Fox", "Deer", "Rabbit", "Squirrel", "Owl", "Eagle", "Penguin", "Dolphin", "Whale", "Shark", "Octopus", "Turtle", "Snake", "Lizard", "Frog", "Crocodile", "Hippopotamus", "Rhinoceros", "Chimpanzee", "Gorilla", "Panda", "Koala", "Kangaroo", "Ostrich", "Peacock", "Swan", "Duck", "Chicken", "Cow", "Horse", "Sheep", "Pig", "Dog", "Cat", "Mouse", "Rat", "Hamster", "Guinea", "Pig", "Ferret", "Goldfish", "Parrot", "Canary", "Sparrow", "Pigeon", "Ant", "Bee", "Butterfly", "Spider", "Snail", "Worm"]
animal = guess_animal[0]
# Handle '/start' and '/help'
@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, """\
Hi there, I am a AI.
I am here to generate the things you say.You can geneate a image writing "/generate (the thing you want to genertare) or you can try to guess the animal by writing "/guess"!\
""")
    

    
@bot.message_handler(commands=['generate'])
def generate_image(message):
    prompt = message.text.split(" ", 1)[1] if len(message.text.split(" ")) > 1 else "cat"
    bot.reply_to(message, "Generating...")
#    bot.send_chat_action(chat.id, 'typing')
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(prompt, pipeline_id)
    files = api.check_generation(uuid)[0]
    
    # Сохраняем изображение на диск
    api.save_image(files, "generated_image.jpg")

    with open("generated_image.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Here is your image!")























@bot.message_handler(commands=["guess"])
def guess_1(message):
    global guess_animal, animal
    animal = random.choice(guess_animal )
    bot.reply_to(message, "Generating...")
#    bot.send_chat_action(chat.id, 'typing')
    api = FusionBrainAPI('https://api-key.fusionbrain.ai/', API_KEY, SECRET_KEY)
    pipeline_id = api.get_pipeline()
    uuid = api.generate(animal, pipeline_id)
    files = api.check_generation(uuid)[0]
    
    # Сохраняем изображение на диск
    api.save_image(files, "generated_image.jpg")

    with open("generated_image.jpg", "rb") as photo:
        bot.send_photo(message.chat.id, photo, caption="Try to guess it good luck(write the first letter in big)!")
    




# Handle all other messages with content_type 'text' (content_types defaults to ['text'])
@bot.message_handler(func=lambda message: True)
def check_image(message):
    global animal
    answer = message.text
    if answer == animal:
        bot.reply_to(message, "You guessed it right!")
    else:
        bot.reply_to(message, "Try again!")
    
bot.infinity_polling()