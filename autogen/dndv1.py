import autogen

import sqlite3
import json

from dotenv import load_dotenv
import os 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def get_race_info(race_name) -> str:
    # Connect to the SQLite database
    conn = sqlite3.connect('dnd_races.db')
    c = conn.cursor()
    
    # SQL query to select the race data
    c.execute("SELECT * FROM races WHERE Race = ?", (race_name,))
    
    # Fetch the result
    result = c.fetchone()
    
    # Close the database connection
    conn.close()
    
    # Check if the race was found
    if result:
        # Create a dictionary with the column names as keys and the row data as values
        data = {
            "Race": result[0],
            "AbilityScoreIncrease": result[1],
            "Traits": result[2],
            "TraitDescriptions": result[3]
        }
        # Convert the dictionary to a JSON string
        return json.dumps(data, indent=4)
    else:
        return json.dumps({"error": "Race not found"}, indent=4)

backgroundWriterPrompt = """
You are a DnD 5e character creation assistant who will interactively work with the user to build a DnD character background based on their preferences.  
You will only build the background independent of race, class and other parameters which are handled by other agents. 
The user will be instructed to start with a description of what kind of character they want. 
Make sure to ask them follow up questions if they dont provide much information on the character. 
You will iterate on the backstory with the user and ask the user to say when they are satisfied with the backstory. 
When this happens you will say BACKSTORY COMPLETE and provide the full completed backstory for the next agent to take over. 
"""

classWriterPrompt = """
You are a DnD 5e race selection assistant, you will receive a background from the background agent and you will use this to suggest 3 potential classes to the user. 
If you did not see BACKSTORY COMPLETE, make sure the backgroundWriter agent has completed the backstory before you proceed, they need to get final confirmation from the user. 
You will provide detailed rationale on why the 3 suggested classes are a good fit for the given backstory and you will only select from classes available in the player handbook, excluding expansions. 
If the user suggests a class outside of your list which you think is not a good choice, provide feedback to the user on why, but let them make the final call. 
When the user has provided their confirmation on their class selection, you will simply respond with CLASS SELECTED. 
"""

raceWriterPrompt = """
You are a DnD race selection assistant, you will receive a background and class from the other agents and you will use this to suggest 3 potential races the user can select from. 
Make sure not to suggest races which would result in an incompatible or challenging to play build for a newcomer and consider ability score to help the playstyle. 
You will explain why the suggested races are a good fit for the character keeping in mind they may not understand the DnD terminology and stats, so explain it in a natural language way. 
You also have access to a get_race_info function which you can use to get some metadata on the races you picked. Please call this function for each suggested race and include the json output after your summarized response for the user to reference. 
"""

config_list = [
                {
                    "model": "gpt-4-turbo-preview",
                    "api_key": OPENAI_API_KEY
                }
                ]

llm_config = {"config_list": config_list, "cache_seed": 42}
llm_config_race = {"config_list": config_list, "cache_seed": 42, "functions": [
        {
            "name": "get_race_info",
            "description": "Retrieves information about a specific race from the 'dnd_races' database, including ability score increases, traits, and descriptions of those traits.",
            "parameters": {
                "type": "object",
                "properties": {
                    "race_name": {
                        "type": "string",
                        "description": "The name of the race to retrieve information for. This is used to query the database and fetch race-specific details."
                    }
                },
                "required": ["race_name"]
            }
        }
    ]}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="The human user who is inputting character requirements and asking DnD questions",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="ALWAYS",
)

# planner = autogen.UserProxyAgent(
#     name="planner",
#     system_message="This is the planner who decides which agent needs to respond to the latest human input. The planner will ensure background is created first, followed by the classes and will send any other questions to the qna agent",
#     code_execution_config=False,
# )

backgroundWriter = autogen.AssistantAgent(
    name="backgroundWriter",
    system_message=backgroundWriterPrompt,
    llm_config=llm_config,
)
classWriter = autogen.AssistantAgent(
    name="classWriter",
    system_message=classWriterPrompt,
    llm_config=llm_config,
)
raceWriter = autogen.AssistantAgent(
    name="raceWriter",
    system_message=raceWriterPrompt,
    llm_config=llm_config,
)

qna = autogen.AssistantAgent(
    name="qna",
    system_message="A DnD expert who can answer any questions about DnD 5e",
    llm_config=llm_config,
)

groupchat = autogen.GroupChat(agents=[user_proxy, backgroundWriter, classWriter, qna, raceWriter], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="I want to be a drunken monk"
)


