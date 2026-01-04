import random
from colorama import Fore
from os import system, name, path
import pygame
import time
from google.cloud import texttospeech

# Set up Text-to-Speech client
client = texttospeech.TextToSpeechClient()

def text_to_speech(text, output_file, lang_code):
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(language_code=lang_code, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL)
    audio_config = texttospeech.AudioConfig(audio_encoding=texttospeech.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)
    
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
    print(f'Audio content written to file {output_file}')

text_dictionary = {
    "apple": "A fruit that is typically red, green, or yellow.",
    "banana": "A long, curved fruit with a thick peel and soft, sweet flesh inside.",
    # Add more words and definitions
}

pygame.mixer.init()

def clear():
    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux
    else:
        _ = system('clear')

def Wort(palabra):
    time.sleep(1)
    sounddir = "sounds"
    pygame.mixer.music.load(f"{sounddir}/ubersetzen.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    pygame.mixer.music.load(f"{sounddir}/{palabra}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.load(f"{sounddir}/auf Deutsch.mp3")
    pygame.mixer.music.play()
    time.sleep(1)

def Play(sound):
    sounddir = "sounds"
    pygame.mixer.music.load(f"{sounddir}/{sound}.mp3")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

def Salir():
    sounddir = "sounds"
    print("Bis bald !")
    pygame.mixer.music.load(f"{sounddir}/bisbald.mp3")
    pygame.mixer.music.play()
    time.sleep(1)
    exit(0)

dict = {}
respuesta = ""

# Open the file for reading
with open('palabras.txt', 'r') as file:
    # Read each line in the file
    for line in file:
        # Strip whitespace and any trailing newline characters from the line
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
        
        # Split the line into a key-value pair
        key, value = line.split(',', 1)  # Assumes only one comma per line
        
        # Add the key-value pair to the dictionary
        dict[key] = value

        # Generating sounds in spanish
        output_file = f"sounds/sp/{key}.mp3"
        if not path.exists(output_file):
            text_to_speech(f"{key}", output_file, "es-ES")
        else:
            print(f"audio for {key} already exists. Skipping.")

        # Generating sounds in german
        output_file = f"sounds/de/{value}.mp3"
        if not path.exists(output_file):
            text_to_speech(f"{value}", output_file, "de-DE")  
        else:
            print(f"audio for {value} already exists. Skipping.")

while True:
    clear()
    if respuesta == "nein":
        Salir()
    Punkte = 0
    Leben = 3
    Punkte_pro_Leben = 5
    gut_gemacht = ""
    Play("hallochen")
    respuesta = input("Hallochen ! Magst du spielen ? (ja / nein) ")
    while (pygame.mixer.music.get_busy()):
        pass
    while ( respuesta != "nein" ):
        gut_gemacht = ""
        palabra_random = random.choice(list(dict.keys()))
        while (pygame.mixer.music.get_busy()):
            pass
        Wort(f"sp/{palabra_random}")
        respuesta = input(f"übersetzen {Fore.RED}{palabra_random}{Fore.WHITE} auf Deutsch: ")
        if respuesta == "nein":
            Salir()
        if (respuesta == dict[palabra_random]):
            Punkte = Punkte + 1
            if Punkte == Punkte_pro_Leben:
                Leben = Leben + 1
                Punkte = 0
                Play("herz-plus")
                gut_gemacht = "\U0001f44d Du hast einen neuen Herz gewonnen ! \U0001F49D"
            elif Punkte < 1 and gut_gemacht == "":
                print(f"\N{face screaming in fear}", end='')
            print(f"Sehr gut ! The anwort ist {Fore.GREEN}{dict[palabra_random]}{Fore.WHITE}")
            if gut_gemacht == "":
                Play("bell")
                Play("Sehr gut")
                Play(f"de/{dict[palabra_random]}")
            else:
                Play("gewonnen")
            print(f"Punkte: {Punkte} {gut_gemacht}", end='')
            for i in range(Punkte):
                print(f"\N{slightly smiling face}", end='')
            print()
            print(f"Leben:  {Leben} ", end='')
            for i in range(Leben):
                print(f"\u2764\uFE0F", end='')        
            print()
        else:
            Punkte = Punkte - 1
            if Punkte <= 0:
                Leben = Leben - 1

            print(f"Tut mir leid ! \N{crying face}. The anwort ist {Fore.GREEN}{dict[palabra_random]}{Fore.WHITE}")
            Play("tutmirleid")
            Play("anwort-ist")
            Play(f"de/{dict[palabra_random]}")
            
            if Leben == 0:
                print("GAME OVER: \N{skull}")
                Play("gameover")
                Play("game-over")
                time.sleep(3)
                break            
            
            Play("leben-minus")
            print(f"Punkte: {Punkte} ", end='')
            if Punkte < 1:
                print(f"\N{face screaming in fear}", end='')
            for i in range(Punkte):
                print(f"\N{slightly smiling face}", end='')
            print()
            print(f"Leben:  {Leben} ", end='')
            for i in range(Leben):
                print(f"\u2764\uFE0F", end='')        
            print()
