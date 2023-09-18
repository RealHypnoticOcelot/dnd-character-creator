import random
import asyncio
import aiohttp
import datetime

def selector(attribute_name, attribute_list):
    while attributes[attribute_name] == []: # while whatever attribute being selected is empty
        for i in attribute_list:
            if input(f"Include {attribute_name} from {i}(Total amount: {len(attribute_list[i])})? y/n: ").lower() == "y":
                attributes[attribute_name] += (attribute_list[i]) # add all races from selected expansion to  master race list
        if attributes[attribute_name] == []: # send error if no expansions are selected
            print("Must select at least one expansion!")
            print(attributes[attribute_name])

async def getinfo(attribute, attribute_selection, data):
    attribute_selection = attribute_selection.lower().replace(" ", "-")
    async with aiohttp.ClientSession() as session:
        async with session.get(f'https://www.dnd5eapi.co/api/{attribute}s/{attribute_selection}') as resp:
            resp = await resp.json()
            for i in data:
                print(f"{resp[i]}\n")

attributes = {
    "race":[],
    "class":[],
    "alignment":["Lawful Good", "Lawful Neutral", "Lawful Evil", "Neutral Good", "Neutral", "Neutral Evil", "Chaotic Good", "Chaotic Neutral", "Chaotic Evil"]
}

extrainfo = {
    "race":['alignment', 'age', 'size_description', 'language_desc'],
    "alignment":['desc']
}

races = {
    "Player's Handbook":['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Halfling', 'Half-Orc', 'Human', 'Tiefling']
}
classes = {
    "Player's Handbook":['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard'],
}

selector('race', races)
selector('class', classes)

allinfo = ""
for i in attributes:
    randomchoice = random.choice(attributes[i])
    allinfo += (f"{i.title()}: {randomchoice}\n") # create list of saved info in case you want to save it to a txt file
    print(f"\nYour {i} is {randomchoice}")
    if i in extrainfo:
        if input(f"Learn more about your {i}? y/n: ").lower() == "y": # get info about it from api, classes don't have any descriptions so it's disabled
            asyncio.run(getinfo(i, randomchoice, extrainfo[i]))
if input("Save data to a file? y/n: ").lower() == "y":
    file = open(f"character_{datetime.datetime.today().replace(microsecond=0)}.txt", "w")
    file.write(allinfo.rstrip("\n"))
    file.close()