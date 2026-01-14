from neo4j import GraphDatabase
from config import NEO4J_URI, NEO4J_AUTH, llm_fast
import os

class KnowledgeGraph:
    def __init__(self):
        self.driver = None
        try:
            print(f"🔌 Connecting to: {NEO4J_URI}...")
            self.driver = GraphDatabase.driver(NEO4J_URI, auth=NEO4J_AUTH)
            self.driver.verify_connectivity()
            print("✅ SUCCESS: Database Connected!")
        except Exception as e:
            print(f"❌ DATABASE ERROR: {e}")
            self.driver = None

    def close(self):
        if self.driver:
            self.driver.close()

    def add_paper(self, title, insights):
        if not self.driver: return

        query = """
        MERGE (p:Paper {title: $title})
        WITH p
        UNWIND $insights as insight
        MERGE (i:Insight {desc: insight})
        MERGE (p)-[:REVEALED]->(i)
        """
        try:
            with self.driver.session() as session:
                session.run(query, title=title, insights=insights)
            print(f"✅ Saved to Neo4j: {title}")
        except Exception as e:
            print(f"⚠️ Failed to write: {e}")

    def visualize_graph(self, output_file="graph.html"):
        """Generates interactive HTML graph"""
        from pyvis.network import Network
        if not self.driver: return None

        query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 50"
        net = Network(height="600px", width="100%", bgcolor="#222222", font_color="white")
        
        try:
            with self.driver.session() as session:
                result = session.run(query)
                for record in result:
                    source = record["n"]
                    target = record["m"]
                    rel = record["r"]
                    
                    s_label = source.get("title", "Unknown Paper")
                    net.add_node(source.element_id, label=s_label, color="#FF6B6B", title="Paper")
                    
                    desc = target.get("desc", "Insight")
                    short_label = desc[:15] + "..." if len(desc) > 15 else desc
                    net.add_node(target.element_id, label=short_label, color="#4ECDC4", title=desc)
                    net.add_edge(source.element_id, target.element_id, title=rel.type)

            net.save_graph(output_file)
            return output_file
        except Exception as e:
            return None

    def query_graph(self, user_question):
        """Translates natural language to Cypher and runs it."""
        if not self.driver: return "Database is offline."

        # --- THE FIX IS HERE: Double Braces {{ }} around title and desc ---
        schema_prompt = """
        You are a Neo4j Cypher expert. 
        Schema: (Paper {{title: string}}) -[:REVEALED]-> (Insight {{desc: string}})
        
        Task: Convert the User's Question into a Cypher query.
        
        Step 1: Extract the CORE SUBJECT (remove "summarize", "tell me about").
        Step 2: Use that subject for the search.
        
        User Question: "{question}"
        
        CRITICAL RULES:
        1. Search 'p.title' OR 'i.desc'.
        2. Use 'CONTAINS' with 'toLower()'.
        3. Do NOT search for the word 'summarize'. Search only for the topic.
        4. Return ONLY the Cypher string. No markdown.
        """
        
        # This .format() was crashing before because of single braces. Now it works.
        prompt = schema_prompt.format(question=user_question)
        
        try:
            cypher_query = llm_fast.invoke(prompt).content.strip().replace("```cypher", "").replace("```", "")
            print(f"🤖 Generated Query: {cypher_query}")

            with self.driver.session() as session:
                result = session.run(cypher_query)
                data = [record.data() for record in result]
                
            if not data:
                return "I searched the graph but found no matching records."
            
            return str(data)
            
        except Exception as e:
            return f"Query failed: {e}"