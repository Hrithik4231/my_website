# Importing necessary libraries
import nltk
import requests
from nltk.chat.util import Chat, reflections

# Ensure NLTK data is downloaded
nltk.download('punkt')

# Define pattern-response pairs for basic conversation
pairs = [
    ["(hi|hello|hey)", ["Hello! How can I assist you with your travel plans?"]],
    ["(recommend a hotel in|find hotels in) (.*)", ["Searching for hotels in %2..."]],
    ["(what's the weather in|weather in) (.*)", ["Checking the weather in %2..."]],
    ["(what should I pack for|packing list for) (.*)", ["Let me check the weather in %2 for packing suggestions."]],
    ["(famous places to visit in|places to visit in) (.*)", ["Let me find some famous places in %2 for you."]],
    ["quit", ["Thank you for using AI Travel Buddy. Safe travels!"]]
]
chatbot = Chat(pairs, reflections)

# Function to find hotels using Google Places API
def find_hotels(location):
    api_key = "AIzaSyC-AWfer89PDpn3YbaDGY65Dhm5Z4_xci0"  # Google Places API key
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query=hotels+in+{location}&key={api_key}"
    response = requests.get(url).json()
    if response.get("results"):
        hotels = [place["name"] for place in response["results"][:5]]  # Get top 5 hotels
        return hotels
    else:
        return ["No hotels found."]

# Function to check weather using OpenWeather API
def get_weather(location):
    api_key = "7caa8096f9a12c99fb6e91c22cad6bdc"  # OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={location}&appid={api_key}&units=metric"
    response = requests.get(url).json()
    if response.get("cod") == 200:
        weather = response["weather"][0]["description"]
        temp = response["main"]["temp"]
        return weather, temp
    else:
        return None, None

# Function to suggest packing items based on the weather
def packing_list(weather, temperature):
    items = []
    if temperature < 10:  # Cold weather
        items.append("warm clothes")
        items.append("sweaters or jackets")
        items.append("thermal wear")
        items.append("hats and gloves")
    elif 10 <= temperature < 20:  # Mild weather
        items.append("light jackets")
        items.append("long-sleeve shirts")
        items.append("comfortable pants")
    elif temperature >= 20:  # Warm weather
        items.append("lightweight clothing")
        items.append("sunglasses")
        items.append("hats")
    
    # Always suggest some common essentials
    items.extend(["toiletries", "medications", "electronic chargers", "travel documents"])
    
    return items

# Function to suggest famous places based on the country
def famous_places(country):
    places = {
        "france": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral"],
        "italy": ["Colosseum", "Venice Canals", "Leaning Tower of Pisa"],
        "japan": ["Mount Fuji", "Tokyo Tower", "Kinkaku-ji (Golden Pavilion)"],
        "india": ["Taj Mahal", "Jaipur City", "Kerala Backwaters", "Charminar", "Gateway of India", "Vrindavan"],
        "usa": ["Statue of Liberty", "Grand Canyon", "Disneyland"],
        "australia": ["Sydney Opera House", "Great Barrier Reef", "Uluru"],
        "china" : ["Great wall of china", "forbidden city", "the bund", "temple of heaven", "Leshan Giant Buddha"],
        "Africa": ["Victoria falls", "Maasai Mara National reserve", "kenya"]
    }
    return places.get(country.lower(), ["No famous places found."])

# Function to suggest food items/snacks based on country
def food_items(country):
    snacks = {
        "france": ["baguette", "croissant", "cheese"],
        "italy": ["pasta", "gelato", "pizza"],
        "japan": ["sushi", "ramen", "mochi"],
        "india": ["samosa", "biryani", "chai"],
        "usa": ["hot dog", "popcorn", "chocolate chip cookies"],
        "australia": ["Vegemite", "meat pie", "lamingtons"]
    }
    return snacks.get(country.lower(), ["No snack recommendations found."])

# List of available commands for user guidance
available_commands = """
The given input is wrong. Please use these inputs given below:

1. recommend a hotel in | find hotels in
2. what's the weather in | weather in
3. what should I pack for | packing list for
4. famous places to visit in | places to visit in
5. quit
"""

# Main chatbot interaction loop
print("AI Travel Buddy: Hi there! Type 'quit' to exit.")
while True:
    user_input = input("You: ").lower()
    response = chatbot.respond(user_input)
    
    if response is not None:
        print("AI Travel Buddy:", response[0])
        if "find hotels in" in user_input:
            location = user_input.split("in")[-1].strip()
            hotels = find_hotels(location)
            print(f"AI Travel Buddy: Here are some hotels in {location}: {', '.join(hotels)}")
        elif "weather in" in user_input:
            location = user_input.split("in")[-1].strip()
            weather_info, temperature = get_weather(location)
            if weather_info:
                print(f"AI Travel Buddy: The weather in {location} is currently {weather_info} with a temperature of {temperature}°C.")
            else:
                print("AI Travel Buddy: Sorry, I couldn't retrieve the weather information.")
        elif "packing list for" in user_input:
            location = user_input.split("for")[-1].strip()
            weather_info, temperature = get_weather(location)
            if weather_info:
                items = packing_list(weather_info, temperature)
                print(f"AI Travel Buddy: Based on the weather in {location}, you should pack: {', '.join(items)}.")
            else:
                print("AI Travel Buddy: Sorry, I couldn't retrieve the weather information.")
        elif "famous places to visit in" in user_input:
            country = user_input.split("in")[-1].strip()
            places = famous_places(country)
            print(f"AI Travel Buddy: Famous places to visit in {country.capitalize()}: {', '.join(places)}.")
        elif "food items to carry for" in user_input:
            country = user_input.split("for")[-1].strip()
            snacks = food_items(country)
            print(f"AI Travel Buddy: Snacks to carry for {country.capitalize()}: {', '.join(snacks)}.")
    else:
        print("AI Travel Buddy:", available_commands)

    if user_input == "quit":
        print("AI Travel Buddy: Thank you for using AI Travel Buddy. Safe travels!")
        break
