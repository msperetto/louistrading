from typing import Dict, List

class env_setup():
    def __init__(self, coins: List, max_open_orders: int, order_value: float, max_risk: float):
        # utilizar aqui alguma tabela da base ou arquivo json para definir todas as restrições e parâmetros
        self.active_coins = coins
        self.max_open_orders = max_open_orders
        self.order_value = order_value
        self.max_risk = max_risk

    def get_coin_status(self):
        # listar aqui para todas as moedas ativas, as que estão com orderns abertas ou não
        pass

    def get_current_balance(self) -> float:
        pass

    def get_risk_rate(self) -> float:
        pass
    
    def get_total_orders(self) -> int:
        pass

    def get_total_orders_value(self) -> float:
        pass





