from datetime import datetime

class Trade:
    def __init__(self, 
                 id: int, 
                 open: bool, 
                 open_time: datetime, 
                 close_time: datetime, 
                 side: str, 
                 pair: str, 
                 profit: float, 
                 spread: float, 
                 roi: float, 
                 strategy_id: int):
        self.id = id
        self.open = open
        self.open_time = open_time
        self.close_time = close_time
        self.side = side
        self.pair = pair
        self.profit = profit
        self.spread = spread
        self.roi = roi
        self.strategy_id = strategy_id

    def __repr__(self):
        return (f"Trade(id={self.id}, open={self.open}, open_time={self.open_time}, close_time={self.close_time}, "
                f"side='{self.side}', pair='{self.pair}', profit={self.profit}, spread={self.spread}, "
                f"roi={self.roi}, strategy_id={self.strategy_id})")