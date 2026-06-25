import os
import duckdb
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, SystemMessage
from dotenv import load_dotenv

load_dotenv()

# DuckDB setup
# Use the processed data CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(current_dir, "..", "data", "processed", "hotel_bookings_features.csv")
# Use forward slashes for DuckDB paths on Windows
csv_path_duckdb = csv_path.replace("\\", "/")

@tool
def run_read_only_sql(query: str) -> str:
    """Executes a SELECT statement using DuckDB against the hotel bookings dataset."""
    if "insert" in query.lower() or "update" in query.lower() or "delete" in query.lower() or "drop" in query.lower():
        return "Error: Only SELECT queries are allowed."
        
    conn = duckdb.connect(database=':memory:')
    
    # We must ensure the query references the CSV table correctly if the LLM didn't format it right.
    # The LLM should query from read_csv_auto('path') or we create a view.
    try:
        conn.execute(f"CREATE VIEW bookings AS SELECT * FROM read_csv_auto('{csv_path_duckdb}')")
        # Replace the abstract table name if LLM used it
        query = query.replace("hotel_bookings", "bookings")
        result = conn.execute(query).df()
        if len(result) > 50:
            return result.head(50).to_string() + "\n... (truncated to 50 rows)"
        return result.to_string()
    except Exception as e:
        return f"Error executing query: {str(e)}"
    finally:
        conn.close()

@tool
def get_kpi(metric: str) -> str:
    """Retrieves standard KPIs like total_bookings, cancellation_rate, adr."""
    conn = duckdb.connect(database=':memory:')
    conn.execute(f"CREATE VIEW bookings AS SELECT * FROM read_csv_auto('{csv_path_duckdb}')")
    
    try:
        if metric.lower() == "total_bookings":
            res = conn.execute("SELECT COUNT(*) FROM bookings").fetchone()[0]
            return f"Total Bookings: {res}"
        elif metric.lower() == "cancellation_rate":
            res = conn.execute("SELECT AVG(is_canceled) * 100 FROM bookings").fetchone()[0]
            return f"Cancellation Rate: {res:.2f}%"
        elif metric.lower() == "adr":
            res = conn.execute("SELECT AVG(adr) FROM bookings").fetchone()[0]
            return f"Average Daily Rate (ADR): {res:.2f}"
        else:
            return "Unknown KPI. Available KPIs: total_bookings, cancellation_rate, adr."
    except Exception as e:
        return f"Error: {str(e)}"
    finally:
        conn.close()

class AIAnalystAgent:
    def __init__(self):
        # We assume GOOGLE_API_KEY is in environment or .env
        api_key = os.getenv("GOOGLE_API_KEY", "")
        if not api_key:
            # Fallback or placeholder handling
            pass
            
        self.llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0, api_key=api_key) if api_key else None
        
        self.tools = [run_read_only_sql, get_kpi]
        
        if self.llm:
            # System prompt setup
            system_prompt = """
            You are a helpful AI Data Analyst for a Hotel Intelligence Platform.
            You can answer questions about hotel bookings, cancellations, ADR, lead times, and customer segments.
            You have access to a table named 'bookings' with the hotel dataset.
            The 'bookings' table contains features such as 'hotel', 'is_canceled', 'lead_time', 'arrival_date_month', 'stays_in_weekend_nights', 'stays_in_week_nights', 'adults', 'children', 'babies', 'meal', 'country', 'market_segment', 'distribution_channel', 'is_repeated_guest', 'previous_cancellations', 'previous_bookings_not_canceled', 'reserved_room_type', 'assigned_room_type', 'booking_changes', 'deposit_type', 'agent', 'company', 'days_in_waiting_list', 'customer_type', 'adr', 'required_car_parking_spaces', 'total_of_special_requests', 'reservation_status', 'reservation_status_date', 'total_nights', 'total_guests', 'prior_cancel_flag', 'lead_time_bucket', 'season'.
            
            Use the tools available to find the data.
            When you run a SQL query, use the 'run_read_only_sql' tool with a valid DuckDB SQL SELECT statement querying the 'bookings' table.
            ALWAYS use LIMIT 10 in your queries unless the user specifically asks for more rows.
            ALWAYS format the tool's raw data output into a clean Markdown table in your final response.
            Then provide a clear, concise business explanation of the result to the user.
            """
            
            # Create LangGraph ReAct agent
            self.agent = create_react_agent(self.llm, self.tools, state_modifier=system_prompt)
        
    def ask(self, question: str) -> str:
        if not self.llm:
            # Fallback Demo Mode for portfolio viewers who don't have an API key
            q_lower = question.lower()
            if "cancellation rate" in q_lower and "segment" in q_lower:
                return "Based on the data, the **Online TA** segment has the highest cancellation rate at approximately **35.1%**.\n\n*Note: This is a simulated response. Please enter a Gemini API Key to query the database dynamically.*"
            elif "adr" in q_lower or "average daily rate" in q_lower:
                return "The Average Daily Rate (ADR) for **City Hotels** is generally higher and more consistent year-round compared to **Resort Hotels**, which see massive spikes during the Summer months.\n\n*Note: This is a simulated response. Please enter a Gemini API Key to query the database dynamically.*"
            elif "country" in q_lower or "countries" in q_lower:
                return "| Country | Total Bookings |\n|---|---|\n| PRT | 48,590 |\n| GBR | 12,129 |\n| FRA | 10,415 |\n| ESP | 8,568 |\n| DEU | 7,287 |\n\n*Note: This is a simulated response. Please enter a Gemini API Key to query the database dynamically.*"
            else:
                return f"**(Demo Mode)** You asked: '{question}'.\n\nI am currently running in offline demo mode. To see me generate real SQL queries and analyse the database dynamically, please provide a free Google Gemini API Key in the sidebar!"

        try:
            # Run the agent graph
            messages = self.agent.invoke({"messages": [("user", question)]})
            
            # Extract the final AI message content
            return messages["messages"][-1].content
        except Exception as e:
            return f"An error occurred while processing your request: {str(e)}"

if __name__ == "__main__":
    # Test script
    agent = AIAnalystAgent()
    print("Testing LangGraph agent...")
    res = agent.ask("What is the total number of bookings?")
    print("Response:", res)
