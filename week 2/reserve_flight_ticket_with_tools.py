import os
from dotenv import load_dotenv
from openai import OpenAI
import json
import gradio as gr


load_dotenv(override=True)
openai_api_key = os.getenv('OPENAI_API_KEY')

if openai_api_key:
    print(f"OpenAI API Key exists and begins {openai_api_key[:8]}")
else:
    print("OpenAI API Key not set")


# Initialize

openai = OpenAI()
MODEL = 'gpt-4o-mini'


system_message = "You are a helpful assistant for an Airline called FlightAI. "
system_message += "Give short, courteous answers, no more than 1 sentence. "
system_message += "Always be accurate. If you don't know the answer, say so."

# Let's start by making a useful function

ticket_prices = {"london": "$799", "paris": "$899", "tokyo": "$1400", "berlin": "$499"}

def get_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    return ticket_prices.get(city, "Unknown")


def process_reservation(destination_city):
    print("Tool for return fligh was called")
    print("You have made your reservation")


def get_return_ticket_price(destination_city):
    print(f"Tool get_ticket_price called for {destination_city}")
    city = destination_city.lower()
    price =  ticket_prices.get(city, "Unknown")
    return  int(price[1:]) * 2 if price != "Unknown" else 0


price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a ticket to the destination city. Call this whenever you need to know the ticket price, this is a one way ticket, for example when a customer asks 'How much is a ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}


process_reservation = {
    "name": "process_reservation",
    "description": "Process the reservation for the flight ticket. Call it when you want to do the actual reservation, for example when a customer asks 'I want to reserve now or proceed to reservation'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}

return_ticket_price = {
    "name": "get_return_ticket_price",
    "description": "get the return flight ticket price, this is return ticket. Call it when you want know the price of return flight, for example when a customer asks 'How much is a return ticket to this city'",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False
    }
}


# And this is included in a list of tools:

tools = [
         {"type": "function", "function": price_function},
         {"type": "function", "function": process_reservation},
         {"type": "function", "function": return_ticket_price}
        ]


def chat(message, history):
    messages = [{"role": "system", "content": system_message}] + history + [{"role": "user", "content": message}]
    response = openai.chat.completions.create(model=MODEL, messages=messages, tools=tools)

    if response.choices[0].finish_reason=="tool_calls":
        message = response.choices[0].message
        response, city, reservation_message = handle_tool_call(message)
        messages.append(message)
        messages.append(response)
        response = openai.chat.completions.create(model=MODEL, messages=messages)
    
    return response.choices[0].message.content


def handle_tool_call(message):
    tool_call = message.tool_calls[0]
    arguments = json.loads(tool_call.function.arguments)
    city = arguments.get('destination_city')
    price = 0
    message = "This prices is subject to change in time of reservation"
    if tool_call.function.name == "get_ticket_price": ## not sure how to make the condition
        price = get_ticket_price(city)
    if tool_call.function.name == "get_return_ticket_price":
        price = get_return_ticket_price(city)
    if tool_call.function.name == "process_reservation":
        message = "Reservation was done successfully"
        
    response = {
        "role": "tool",
        "content": json.dumps({"destination_city": city,"price": price, "message": message}),
        "tool_call_id": tool_call.id
    }
    return response, city, message


gr.ChatInterface(fn=chat, type="messages").launch()