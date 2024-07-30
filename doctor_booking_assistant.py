import os
import re
from langchain_groq import ChatGroq
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv

'''Loading the environment variables'''
load_dotenv()

'''Setting up the ChatGroq for the ChatModel'''
groq_api_key = os.getenv('GROQ_API_KEY')


'''Using the Gemma2 model for the ChatGroq'''
llm = ChatGroq(groq_api_key=groq_api_key, model_name="gemma2-9b-it")
'''Using the Mixtral model for the ChatGroq'''
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="mixtral-8x7b-32768")
'''Using the Mixtral model for the ChatGroq'''
# llm = ChatGroq(groq_api_key=groq_api_key, model_name="llama-3.1-70b-versatile")



'''System message template for the appointment booking assistant'''

template = """
You are an efficient appointment booking assistant. Your task is to help users schedule doctor appointments with a Hospital.

If the user expresses intent to book an appointment, collect the following information:
1. Doctor's name
2. Appointment start time
3. Appointment end time

If you find all the inputs in a single message, extract and validate the required details.
---
Example: "I want to book an appointment for Dr. John Doe tomorrow from 8 AM to 9 AM."
---
If any information is missing, please make sure to get the details to move forward else say the user that you need all the details to book the appointment.

Only ask for one piece of information at a time. Do not ask for all details in a single message.

If the user's query is not related to booking an appointment or is out of scope, respond with:
"I'm sorry, I didn't understand your query. I'm here to help with booking doctor appointments. How can I assist you with that?"

If the user wishes to cancel the operation at any point, respond with:
{{
"status": "cancelled"
}}

Remember to only ask for one piece of information at a time and to be polite and helpful throughout the conversation.

When all information is collected, output it in the following format without any additional text, markdown formatting, or code block indicators:
{{
"drName": Doctor,
"startDate": Start,
"endDate": End
}}

Output Format:
{{
"drName": "Name of the doctor captured from the query",
"startDate": "A valid ISO date time string",
"endDate": "A valid ISO date time string"
}}

The below are few examples of the output format:
---
Example-1:
User > I want to book an appointment
Assistant > Sure, I can help you with that, can you provide the date, time and the name of the
doctor you wanted to book the appointment for?
User > I want to book for tomorrow 8 AM to 9 AM for Dr. John Doe
Assistant > {{
"drName": "Dr. John Doe",
"startDate": "2024-11-01T08:00:00Z",
"endDate": "2024-01-11T09:00:00Z"
}}
Example 2:
User > Create appointment for Dr. John Doe from 8 am to 9 am on Tuesday
Assistant > {{
"drName": "Dr. John Doe",
"startDate": "2024-11-16T08:00:00Z",
"endDate": "2024-01-11T16:00:00Z"
}}
---

Always ensure the output JSON is properly formatted and follows the same structure.

To minimize token usage, keep responses concise and focused on the task at hand.
{chat_history}
Human: {query}
AI:
"""


'''Setup the prompt for the ChatGroq'''
prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(template),
    HumanMessagePromptTemplate.from_template("{query}")
])

'''Setting up the memory for the ChatGroq'''
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
chain = LLMChain(llm=llm, prompt=prompt, memory=memory)


'''Function to extract the appointment information from the text'''
def extract_appointment_info(text):
    """

    This function extracts the doctor's name, start date, and end date from the text.
    Input: text (str)
    Output: info (dict)
    
    """
    patterns = {
        "drName": r'"drName":\s*"([^"]+)"',
        "startDate": r'"startDate":\s*"([^"]+)"',
        "endDate": r'"endDate":\s*"([^"]+)"'
    }
    
    info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, text)
        info[key] = match.group(1) if match else None
    
    return info


'''Function to process the appointment booking'''
def process_booking(chain):
    """Process the appointment booking."""
    appointment_info = {"drName": None, "startDate": None, "endDate": None}

    while not all(appointment_info.values()):
        query = input("Human: ")
        if query.lower() == "bye":
            return False

        response = chain.run(query)
        print("Assistant: ",response)

        extracted_info = extract_appointment_info(response)
        appointment_info.update({k: v for k, v in extracted_info.items() if v is not None})

    print("Great! I've collected all the necessary information. Here's a summary of your appointment:")
    print(response)
    print("Is this information correct? (Yes/No)")
    
    if input("Human: ").lower() == "yes":
        print("Your appointment has been booked. Thank you for choosing us!")
        return True
    else:
        print("I apologize for the mistake. Let's start over. What would you like to change?")
        return True

def main():
    print("AI: Hello! I'm here to help you book a doctor's appointment. How can I assist you today?")

    while True:
        query = input("Human: ")
        
        if query.lower() == "bye":
            print("AI: Thank you for using our appointment booking service. Goodbye!")
            break

        response = chain.run(query)
        print("Assistant: ",response)

        if "book" in query.lower() or "appointment" in query.lower():
            if process_booking(chain) or not process_booking(chain):
                break
if __name__ == "__main__":
    main()
