from langgraph.graph import StateGraph
from groq import Groq

# Use your actual Groq API key here
groq = Groq(api_key="your_groq_api_key_here")

def coach_response(state):
    user_input = state["input"]
    response = groq.chat.completions.create(
        model="llama3-70b-8192",  # Replace if needed
        messages=[
            {"role": "system", "content": "You are an interview coach. Give helpful feedback and ask one follow-up question."},
            {"role": "user", "content": user_input}
        ]
    )
    state["response"] = response.choices[0].message.content.strip()
    return state

builder = StateGraph()
builder.add_node("coach", coach_response)
builder.set_entry_point("coach")
interview_graph = builder.compile()
