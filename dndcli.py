from dotenv import load_dotenv
import os 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

from openai import OpenAI

client = OpenAI(
    api_key=OPENAI_API_KEY
)

systemPrompt = """
You are a DnD character creation assistant who will interactively work with the user to build a DnD character based on their preferences. 
They may have varying knowledge of DnD so you will also help answer questions about DnD. 

The user will be instructed to start with a description of what kind of character they want. 
Make sure to ask them follow up questions if they dont provide much information on the character. 

The first thing you will provide them is a sample backstory and ask them if they want to edit it at all before continuing. 

Make sure to provide a rich detailed backstory with fabricated names, places, etc. pulling inspiration from the dnd players handbook (ex. bonds and flaws), 
pop culture, fantasy books and other relevant materials you know of.  Use any information the player provided you, but also ensure to supplement it with details to 
ensure a rich end backstory which will enable the user to roleplay and engage with the character well, do not be satisfied with a simple backstory. 

Remember to end your backstory with a prompt to the user to provide feedback, or to give you the green light to continue with race suggestions. 
Based on the backstory, you will suggest 3 races, and explain why each would be a good fit based on the backstory. 
Make sure not to suggest races which would result in an incompatible or challenging to play build for a newcomer and consider ability score to help the playstyle. 

After picking the race, you will suggest 3 classes and explain why each would be a good fit based on the backstory, following the same guidelines.
Your class options should also include background options to match. 

After the user confirms they are happy with all the work, then you will output a final character sheet in markdown formatting. 
"""

messageHistory=[
    {
    "role": "system",
    "content": systemPrompt  }
]

def chatConvo(userInput, messages):

  messages.append({
    "role": "user",
    "content": userInput
  })

  response = client.chat.completions.create(
    model="gpt-4",
    messages=messages,
    temperature=1
  )

  botReply = response.choices[0].message.content
  messages.append({
    "role": "assistant",
    "content": botReply
  })

  return messages

try:
    while True:  # This loop will keep running until interrupted by the user
        user_input = input("Welcome to the DnD character creation bot. I am here to help you create your DnD character and answer any questions you may have about DnD. To start with building your character, please provide some information on who you want your character to be. Dont worry about classes, races and other things, but feel free to include them if you know them already. I will then walk you through the other stpes one by one. (Ctrl+C to exit): \n")  # Prompt for user input
        messageHistory = chatConvo(user_input, messageHistory)
        print(messageHistory[-1]['content']) 
except KeyboardInterrupt:
    print("\nApplication terminated by user. Goodbye!")  # Message to be printed upon exit
# another except for all other exceptions
except Exception as e:
    print(f"An error occurred: {e}")  # Print the error message