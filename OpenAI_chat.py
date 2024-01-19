import configparser #works with config.ini file
import argparse #for parsing out arguments
import sys # system access options
import os #environment-based variables
import openai #OpenAI API
import pandas as pd #Pandas dataframes
import datetime #datetime libraries
import pytz #timezone
from gtts import gTTS #text to speech locally
from dotenv import load_dotenv #load dotenv
from pygame import mixer #pygame is for playing voices

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API key
openai.organization=os.getenv("ORG_ID")
openai.api_key = os.getenv("OPENAI_API_KEY")

def cls(): #Clear Screen Function
    os.system('cls')

def update_env_file(env_file_path, key, value):
    # Read the existing content of the .env file
    with open(env_file_path, 'r') as file:
        content = file.readlines()

    # Check if the key exists in the .env file
    key_exists = False
    for index, line in enumerate(content):
        if line.startswith(key):
            key_exists = True
            content[index] = f"{key}={value}\n"
            break

    # If the key does not exist, add it to the end of the .env file
    if not key_exists:
        content.append(f"{key}={value}\n")

    # Write the updated content back to the .env file
    with open(env_file_path, 'w') as file:
        file.writelines(content)

class Conversations:
    def __init__(self, venv_path, current_model, current_role, current_conversation, name, audio_toggle, no_of_convos):
        self.venv_path = venv_path
        self.current_model = current_model
        self.current_role = current_role
        self.current_conversation = current_conversation
        self.name = name
        self.audio_toggle = audio_toggle
        self.no_of_convos = no_of_convos

    def get_number_of_conversations(self):
        return self.no_of_convos

    def increment_number_of_conversations(self):
        self.no_of_convos += 1

    def save_last_conversation_used(self):
        update_env_file(self.venv_path, 'LAST_CONVERSATION_USED', self.current_conversation)

    def save_number_of_conversations(self):
        update_env_file(self.venv_path, 'NUMBER_OF_CONVERSATIONS', self.no_of_convos)

    def prompt_user(self, prompt_message):
        user_input = str(input(str(prompt_message)))
        return user_input

    def start_new_conversation(self):
        active_convo = int(self.no_of_convos)+1
        total_convo = active_convo
        self.increment_number_of_conversations()
        self.current_conversation = total_convo
        self.save_last_conversation_used()
        self.save_number_of_conversations()
        return active_convo, total_convo

    def load_conversation(self):
        # TODO: implement loading of conversations from log files
        pass

    def delete_conversation(self):
        # TODO: implement deleting of conversations and log files
        pass

class Models:
    def __init__(self):
        self.models = {}
        self.load_models()

    def load_models(self):
        models = openai.Model.list()
        for model in models["data"]:
            self.models[model.id] = model

    def list_models(self):
        model_names = [model.id for model in self.models.values()]
        return "\n ".join(model_names)

    def get_model(self, model_id):
        return self.models.get(model_id, None)

    def update_default_model(self, model_id):
        try:
            model = self.get_model(model_id)
            if model is None:
                print(f"Invalid model ID: {model_id}")
                return False

            env_file_path = os.getenv("ENV_FILE_PATH")
            update_env_file(env_file_path, "DEFAULT_MODEL", model_id)
            print(f"Successfully set default model to {model.id}")
            return True
        except Exception as e:
            print(f"Failed to update default model: {e}")
            return False

class Roles:
    def __init__(self):
        self.current_role = os.getenv("LAST_ROLE_USED")
        self.role_log_file = os.getenv("ROLE_LOG_FILE")
        
    def get_roles(self):
        """
        Gets a list of roles from the role log file.
        """
        try:
            roles_df = pd.read_csv(self.role_log_file)
            role_names = roles_df['Role'].tolist()
            return role_names
        except Exception as e:
            print("Error getting roles: ", e)
            return None
    
    def add_role(self, role_name):
        """
        Adds a new role to the role log file.
        """
        try:
            roles_df = pd.read_csv(self.role_log_file)
            new_role = {
                'Role': role_name,
                'DateTime': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            roles_df = roles_df.append(new_role, ignore_index=True)
            roles_df.to_csv(self.role_log_file, index=False)
            print(f"{role_name} added to roles.")
        except Exception as e:
            print("Error adding role: ", e)
            
    def set_current_role(self, role_name):
        """
        Sets the current role to use with the OpenAI API function call.
        """
        try:
            roles_df = pd.read_csv(self.role_log_file)
            if role_name in roles_df['Role'].tolist():
                os.environ["LAST_ROLE_USED"] = role_name
                self.current_role = role_name
                print(f"Current role set to {role_name}.")
            else:
                print(f"{role_name} is not a valid role.")
        except Exception as e:
            print("Error setting current role: ", e)

class Settings:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Set up OpenAI API key
        openai.organization=os.getenv("ORG_ID")
        openai.api_key = os.getenv("OPENAI_API_KEY")

        # Initialize settings dictionary
        self.settings = {
            "audio_toggle": os.getenv("AUDIO_TOGGLE"),
            "last_model_used": os.getenv("LAST_MODEL_USED"),
            "last_role_used": os.getenv("LAST_ROLE_USED"),
            "last_conversation_used": os.getenv("LAST_CONVERSATION_USED"),
            "number_of_conversations": os.getenv("NUMBER_OF_CONVERSATIONS"),
            "default_env_path": os.getenv("DEFAULT_ENV_PATH")
        }

    def view_settings(self):
        print("\nCurrent Settings:")
        for key, value in self.settings.items():
            print(f"{key}: {value}")

    def update_settings(self, setting_name, new_setting):
        self.settings[setting_name] = new_setting
        env_path = os.getenv("ENV_PATH")
        update_env_file(env_path, setting_name.upper(), new_setting)
        print(f"\n{setting_name} has been updated to: {new_setting}")
