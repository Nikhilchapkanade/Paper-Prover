import chainlit as cl
import os
import shutil
from agents.swarm import app_swarm
from backend.pdf_engine import extract_text_from_pdf
from backend.vision import analyze_charts
from backend.graph_db import KnowledgeGraph
from config import llm_fast

# Initialize Database
kg = KnowledgeGraph()

@cl.on_chat_start
async def start():
    # 1. Welcome Message
    await cl.Message(content="**🧠 Omni-Scholar Lab Online**\nUpload a PDF to start the Cognitive Swarm.").send()
    
    files = None
    while files == None:
        files = await cl.AskFileMessage(
            content="Waiting for file...", 
            accept=["application/pdf"],
            max_size_mb=50,
            timeout=180
        ).send()
    
    pdf_file = files[0]
    
    # 2. Save File Safely
    upload_dir = "data/uploads"
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir)
    
    destination_path = os.path.join(upload_dir, pdf_file.name)
    
    with open(pdf_file.path, "rb") as f_src:
        with open(destination_path, "wb") as f_dest:
            shutil.copyfileobj(f_src, f_dest)
        
    msg = cl.Message(content=f"Analyzing **{pdf_file.name}**...")
    await msg.send()
    
    # 3. Extract Data
    raw_text = extract_text_from_pdf(destination_path)
    vision_json = analyze_charts(destination_path)
    
    # 4. Run Swarm
    initial_state = {
        "paper_content": raw_text,
        "vision_data": vision_json,
        "debate_history": [],
        "critique_count": 0
    }
    
    final_insight = ""
    
    async for event in app_swarm.astream(initial_state):
        for node_name, state_update in event.items():
            if "debate_history" in state_update:
                latest_msg = state_update["debate_history"][-1]
                async with cl.Step(name=node_name) as step:
                    step.output = latest_msg
                    final_insight = latest_msg
    
    # 5. Update Database
    kg.add_paper(title=pdf_file.name, insights=[final_insight])
    
    # 6. Generate & Show Graph
    html_file = kg.visualize_graph("data/graph.html")
    
    response_elements = []
    if html_file and os.path.exists(html_file):
        response_elements.append(
            cl.File(name="Knowledge_Graph.html", path=html_file, display="inline")
        )
    
    await cl.Message(
        content=f"✅ **Analysis Complete.**\n\n**Final Verdict:**\n{final_insight}\n\n👇 **Interactive Knowledge Graph:**",
        elements=response_elements
    ).send()

# --- NEW: CHAT HANDLER (Talk to the Graph) ---
@cl.on_message
async def main(message: cl.Message):
    # 1. Get User Input
    user_input = message.content
    
    # 2. Show thinking indicator
    msg = cl.Message(content="🤔 Consulting the Oracle...")
    await msg.send()
    
    # 3. Query the Graph (Text-to-Cypher)
    raw_answer = kg.query_graph(user_input)
    
    # 4. Humanize the result using Llama 3
    final_response = llm_fast.invoke(f"User asked: '{user_input}'. Database found: '{raw_answer}'. Summarize this answer nicely.").content
    
    # 5. Send back to UI
    msg.content = final_response
    await msg.update()