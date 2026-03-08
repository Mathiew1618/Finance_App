from agent.main import FinanceAgent

agent = FinanceAgent(vault_path="/path/to/your/Obsidian/Vault")

def handle(symbol: str):
    return agent.handle_request(symbol)
