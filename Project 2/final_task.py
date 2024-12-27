import random
import json
import os
import csv
from datetime import datetime  # Import the datetime module

# Constants for file paths and agent names
RESPONSE_FILE_PATH = r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 2\responses.json"
AGENT_NAMES = ["Jordan", "Alex", "Taylor", "Chris"]
LOG_FILE_PATH = r"C:\Users\Binay Ghimire\OneDrive - iTechno\Documents\TBC'\Level 4\Fundamentals of Computer Programming\Project_Work\Project 2\chat_log.csv"

# Function to load responses from the JSON file
def load_responses():
    if not os.path.exists(RESPONSE_FILE_PATH):
        print(f"Error: The file '{RESPONSE_FILE_PATH}' was not found. Please ensure the file exists.")
        return {}

    try:
        with open(RESPONSE_FILE_PATH, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON data from the response file.")
        return {}

# Function to generate a response based on user input
def respond_to_user(user_input, responses, user_name):
    user_input = user_input.lower()  # Normalize the input

    for keyword, random_responses in responses.items():
        if keyword in user_input:
            return random.choice(random_responses).replace("{name}", user_name)

    return "Sorry, I didn't quite catch that. Could you please rephrase?"

# Function to select a random agent name
def select_agent():
    return random.choice(AGENT_NAMES)

# Function to log the conversation to a CSV file with a timestamp
def log_conversation(user_input, agent_response, user_name, agent_name):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get the current time and format it
    with open(LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, user_name, user_input])  # Include timestamp, user message
        writer.writerow([timestamp, agent_name, agent_response])  # Include timestamp, agent response
        writer.writerow([])  # Add a break line between exchanges

# Function to handle the user's chat interaction
def start_chat():
    print("\nWelcome to the University of Poppleton Chatbot!")
    
    # Ask for user details
    user_name = input("Please enter your name: ").strip()
    print(f"\nHello, {user_name}! I'm here to assist you.\n")
    
    agent_name = select_agent()
    print(f"You're chatting with Agent {agent_name}. How can I help you today?\n")
    
    # Load responses from the file
    responses = load_responses()
    if not responses:
        print("No responses available. Exiting the chatbot.")
        return

    # Log header if file is empty
    if not os.path.exists(LOG_FILE_PATH) or os.stat(LOG_FILE_PATH).st_size == 0:
        with open(LOG_FILE_PATH, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "User", "Message"])  # Added Timestamp column
            writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), agent_name, f"Hello, {user_name}! I'm here to assist you."])
            writer.writerow([])  # Add a break line

    # Chat loop
    while True:
        user_input = input(f"{user_name}: ").strip()

        # Exit the chat if the user says 'bye', 'exit', or 'quit'
        if user_input in ["bye", "exit", "quit"]:
            print(f"\nAgent {agent_name}: Goodbye, {user_name}! Have a great day!\n")
            log_conversation(user_input, f"Goodbye, {user_name}! Have a great day!", user_name, agent_name)
            break

        # Generate and display the chatbot's response
        agent_response = respond_to_user(user_input, responses, user_name)
        print(f"\nAgent {agent_name}: {agent_response}\n")
        
        # Log the conversation to the CSV file
        log_conversation(user_input, agent_response, user_name, agent_name)

# Run the chatbot
if __name__ == "__main__":
    start_chat()
