from typing import Dict, List
from common.python import database_operations as db

class Env_setup():
    def __init__(self, max_open_orders: int, order_value: float, max_risk: float, opperation_active: bool):
        # utilizar aqui alguma tabela da base ou arquivo json para definir todas as restrições e parâmetros
        self.max_open_orders = max_open_orders
        self.order_value = order_value
        self.max_risk = max_risk
        self.opperation_active = opperation_active
        self.get_active_pairs()

    def get_active_pairs(self):
        # listar aqui para todas as moedas ativas, as que estão com orderns abertas ou não
        self.active_pairs = db.get_active_pairs()

    def get_current_balance(self) -> float:
        #after mvp
        pass

    def get_risk_rate(self) -> float:
        #after mvp
        pass
    
    def get_total_orders(self) -> int:
        #after mvp
        pass

    def get_total_orders_value(self) -> float:
        #after mvp
        pass





