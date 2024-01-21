import os
import time
from openai import OpenAI

client = OpenAI()


thread = client.beta.threads.create()

assistants = {
    "application": {
        "id": "asst_AST4aDQalNFLck0uh2nc0ZNJ",
        "function": {
            "name": "application_extraction",
            "description": "This function extracts application points from a sermon transcript. Each application point will be returned as an object in an array, containing a summary and a sample passage from the text. An application point tells the audience what they are supposed to do based on what they heard in the sermon that day.",
            "parameters": {
                "type": "object",
                "properties": {
                "application": {
                    "type": "array",
                    "description": "This is a list of all the applications given in the sermon transcript. Any of these keywords/phrases may be good signs that an application point is being given: Apply, Should, Must, Ought to, Need to, Encourage you to, Challenge you to, Consider, Reflect on, Think about, Act on, Implement, Embrace, Adopt, Engage in, Practice, Observe, Follow, Uphold, Commit to, Dedicate yourself to, Hold fast to, Bear in mind, Remember, Keep in mind, Learn from, Draw from, Take away, Walk in, Live out, Abide in, Transform, Change, Repent, Turn to, Seek, Pursue, Strive for, Desire, Yearn for, Pray for, Ask for, Call upon, Lean on, Trust in, Rely on, Depend on, Hope in, Rejoice in, Find joy in.",
                    "items": {
                    "type": "object",
                    "properties": {
                        "summary": {
                        "type": "string",
                        "description": "A concise summary of the application point. Max 5 words."
                        },
                        "sample": {
                        "type": "string",
                        "description": "A direct quote from the sermon that exemplifies this application point. Should be a complete idea and may include multiple sentences."
                        }
                    },
                    "required": [
                        "summary",
                        "sample"
                    ]
                    }
                }
                },
                "required": [
                "application"
                ]
            }
        }
    },
    "illustration": {
        "id": "asst_C6xW15xyPhq0jHDG7Bl6uni2",
        "function": "illustration_extraction"
    },
    "points": {
        "id": "asst_zKl850FmRCjIM0Axz5dZZqgI",
        "function": "points_extraction"
    }
}

def extract_sermon_details(sermon, assistant):
    thread = client.beta.threads.create()
    
    message = client.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=sermon[:32768]
    )
    # print(f"This is the starting Message: {message}")
    run = client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant["id"],
        tools=[{"type": "function", "function": assistant["function"]}]
    )
    # print(f"Run 1: {run}")
    complete = False
    while complete == False:    
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id
        )
        if run.status == "complete":
            required_actions = run.required_action.submit_tool_outputs.tool_calls
            for tool_call in required_actions:
                if tool_call.name == 'application_extraction':
                    application_extraction_arguments = tool_call.arguments
                    print(application_extraction_arguments)
                    break
            complete = True
            run = client.beta.threads.runs.submit_tool_outputs(
                thread_id=thread.id,
                run_id=run.id,
                tool_outputs=[
                    {
                    "tool_call_id": required_actions[0].id,
                    "output": application_extraction_arguments
                    }
                ]
            )
        time.sleep(3)
            
    # print(f"Run 2: {run}")
    messages = client.beta.threads.messages.list(
        thread_id=thread.id
    )
    # print(f"This is the list of all the messages: {messages}")

sermon_file_path = "transcripts/1000593346263.txt"
sermon = ""

sample_sermon_text = "I am preaching a sermon and I have one application point: That you should love God with all your hear, soul, mind, and strength. This is the most important thing you can ever do in life."

try:
    with open(sermon_file_path, 'r') as file:
        sermon += file.read()
except FileNotFoundError:
    print(f"File not found: {file_path}")  # Print out if file not found

extract_sermon_details(sample_sermon_text, assistants["application"])