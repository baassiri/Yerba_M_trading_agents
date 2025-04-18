from XAUUSD_Data.agents.agent_orchestrator import run_orchestrator
from XAUUSD_Data.agents.log_agent import init_log_db
init_log_db()

if __name__ == "__main__":
    run_orchestrator()
