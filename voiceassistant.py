import mysql.connector
from gtts import gTTS
import os
from datetime import datetime
import random
import speech_recognition as sr
import wikipedia
import webbrowser
import time
import pydub


# Establish the database connection
db_connection = mysql.connector.connect(
    host="localhost",
    user="mysql.session",
    password="admin",
    database="voice_assistant_db"
)

# Function to store country-capital information in the database
def store_country_capital(country_name, capital_name):
    cursor = db_connection.cursor()
    cursor.execute("INSERT INTO country_capital (country_name, capital_name) VALUES (%s, %s)", (country_name, capital_name))
    db_connection.commit()
    cursor.close()

# Function to get the capital of a specific country from the database
def get_capital_by_country(country_name):
    cursor = db_connection.cursor()
    cursor.execute("SELECT capital_name FROM country_capital WHERE country_name = %s", (country_name,))
    capital = cursor.fetchone()
    cursor.close()

    # For debugging
    print(f"Debug: Trying to get capital for {country_name}. Found: {capital}")

    return capital[0] if capital else None

def update_capital(country_name, new_capital):
    cursor = db_connection.cursor()
    cursor.execute("UPDATE country_capital SET capital_name = %s WHERE country_name = %s", (new_capital, country_name))
    db_connection.commit()
    cursor.close()
    speak(f"The capital of {country_name} has been updated to {new_capital}.")

# Function to delete the country-capital information from the database
def delete_country_capital(country_name):
    cursor = db_connection.cursor()
    cursor.execute("DELETE FROM country_capital WHERE country_name = %s", (country_name,))
    db_connection.commit()
    cursor.close()
    speak(f"The information for {country_name} has been deleted.")    

def speak(text):
    tts = gTTS(text=text, lang='en')
    tts.save("response.mp3")
    os.system("start response.mp3")
    # Wait for the duration of the audio file
    time.sleep(get_audio_duration("response.mp3"))

# Function to get the duration of an audio file
def get_audio_duration(file_path):
    audio_info = pydub.AudioSegment.from_mp3(file_path)
    return len(audio_info) / 1000.0  # Duration in seconds
    
def get_audio():
    recognizer = sr.Recognizer()  # Define the recognizer object
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
    return audio  

def get_wikipedia_summary(query):
    try:
        # Get a summary of the Wikipedia page for the given query
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        # Handle disambiguation pages
        return f"Ambiguous search term. Please provide more specific details. Options: {', '.join(e.options)}"
    except wikipedia.exceptions.PageError:
        # Handle page not found
        return "Sorry, I couldn't find information on that topic."      

# Function to process user commands
def process_command(command):
    if "store country capital" in command:
        # Extract country and capital information from the command
        # Assuming command format: "store country capital [country] [capital]"
        _, _, _, country_name, capital_name = command.split(maxsplit=4)
        store_country_capital(country_name, capital_name)
        speak(f"Country-capital information for {country_name} stored successfully.")

    elif "what is the capital of" in command:
        # Extract country name from the command
        # Assuming command format: "What is the capital of [country]"
        _, _, _, _, _, country_name = command.split(maxsplit=6)
        capital = get_capital_by_country(country_name)
        if capital:
            speak(f"The capital of {country_name} is {capital}.")
        else:
            speak(f"Capital information for {country_name} not found.")

    elif "update capital" in command:
        # Extract country name and new capital from the command
        # Assuming command format: "update capital of [country] to [new capital]"
        _, _, _, country_name, _, new_capital = command.split(maxsplit=5)
        update_capital(country_name, new_capital)

    elif "delete country" in command:
        # Extract country name from the command
        # Assuming command format: "delete country [country]"
        _, _, country_name = command.split(maxsplit=3)
        delete_country_capital(country_name)        

    elif "hello" in command:
        greetings = ["Hello!", "Hi there!", "How can I help you"]
        speak(random.choice(greetings))

    elif "thanks" in command:
        speak("You're welcome! If you have any more questions, feel free to ask.")

    elif "time" in command:
        current_time = datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")

    elif "date" in command:
        current_date = datetime.now().strftime("%Y-%m-%d")
        speak(f"Today's date is {current_date}")

    elif "calculate" in command:
        expression = command.replace("calculate", "").strip()
        try:
            result = eval(expression)
            speak(f"The result of {expression} is {result}")
        except Exception as e:
            speak("Sorry, I couldn't perform the calculation. Please check your expression.")
            
    elif "bye" in command:
        speak("Bye! Have a great day.")
        exit()

    elif "tell me about" in command:
        query = command.replace("tell me about", "").strip()
        result = get_wikipedia_summary(query)
        print(result)
        speak(result)

    elif "open youtube" in command:
        webbrowser.open("youtube.com") 
        speak("opening youtube")   

    elif "open new chat" in command:
        webbrowser.open("chat.openai.com") 
        speak("opening chatGPT")    
   
    else:
        speak("I'm sorry, I didn't understand that.")

def main():
    recognizer = sr.Recognizer()
    speak("Hello! I am your voice assistant")
    while True:   # Continuously listen for user commands
        audio_input = get_audio()
        try:
            command = recognizer.recognize_google(audio_input).lower()        # Convert audio input to text using Google's Speech Recognition
            print("You said:", command)
            process_command(command)
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Could you please repeat?")     # Handle the case when the speech recognition cannot understand the audio
main()            
