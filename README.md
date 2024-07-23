# Doctor Appointment Booking Assistant

## Overview

This project implements a Doctor Appointment Booking Assistant using langchain and the Groq API. The assistant helps users schedule doctor appointments by collecting necessary information through a conversational interface.

## Sample Working of the Assistant
![Screenshot 2024-07-23 090457](https://github.com/user-attachments/assets/5cf6e52e-640c-494a-bc95-4a3cb4b1f6f4)
![Screenshot 2024-07-23 090546](https://github.com/user-attachments/assets/ae3cfb4f-634f-447d-8c72-65c691a1602c)
![Screenshot 2024-07-23 090716](https://github.com/user-attachments/assets/d2033c39-502f-4995-92e7-dbafdabada7a)

## Features

- Integration with Groq API for natural language processing
- Extraction and validation of appointment details
- Confirmation and summary of booked appointments
- Natural language processing for appointment booking
- Conversation memory to maintain context
- Information extraction and validation
- JSON output formatting

## Requirements

- Python 3.7+
- `langchain_groq`
- `langchain`
- `python-dotenv`

## Installation

1. Clone the repository:
git clone https://github.com/JoshiSneh/doctor-booking-assistant.git
cd doctor-booking-assistant
2. Install the required packages:
pip install -r requirements.txt
3. Set up your environment variables:
Create a `.env` file in the project root and add your Groq API key:
GROQ_API_KEY=your_groq_api_key_here

## Usage

Run the main script to start the appointment booking assistant:
python appointment_assistant.py
Copy
Follow the prompts to book an appointment. The assistant will guide you through the process, asking for the doctor's name, appointment start time, and end time.
At last to close the assistant we have to write `bye` to exit the application.

## Code Structure

- `appointment_assistant.py`: Main script containing the appointment booking logic
- `load_dotenv()`: Loads environment variables
- `ChatGroq`: Initializes the chat model using the Groq API
- `ChatPromptTemplate`: Defines the system message and conversation flow
- `ConversationBufferMemory`: Maintains conversation history
- `extract_appointment_info()`: Extracts appointment details from the AI's response
- `process_booking()`: Handles the appointment booking workflow
- `main()`: Runs the main conversation loop

