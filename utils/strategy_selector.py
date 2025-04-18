def get_strategy_by_name(name: str):
    name = name.lower()
    
    if name == "ema":
        from XAUUSD_Data.agents.backtesting_agent import EmaCrossStrategy
        return EmaCrossStrategy
    elif name == "ml":
        from XAUUSD_Data.agents.backtesting_agent import MLStrategy
        return MLStrategy
    else:
        raise ValueError(f"❌ Unknown strategy: {name}")
