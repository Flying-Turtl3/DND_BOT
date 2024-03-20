import autogen

from dotenv import load_dotenv
import os 

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# config_list = autogen.config_list_from_json(
#     "OAI_CONFIG_LIST",
#     filter_dict={
#         "model": ["gpt-4-turbo-preview"],
#     },
# )

config_list = [
                {
                    "model": "gpt-4",
                    "api_key": OPENAI_API_KEY
                }
                ]

llm_config = {"config_list": config_list, "cache_seed": 42}
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 2,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="ALWAYS",
)
coder = autogen.AssistantAgent(
    name="Coder",
    llm_config=llm_config,
)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)
groupchat = autogen.GroupChat(agents=[user_proxy, coder, pm], messages=[], max_round=12)
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

user_proxy.initiate_chat(
    manager, message="Find the latest weather details for Scarborough Ontario Canada and summarize the 7 day forecast. Also provide the source."
)