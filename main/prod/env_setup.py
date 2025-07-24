from typing import Dict, List
from common.dao import database_operations as db

class Env_setup():
    def __init__(self, base_config):
        # utilizar aqui alguma tabela da base ou arquivo json para definir todas as restrições e parâmetros
        self.max_open_orders = base_config["max_open_orders"]
        self.order_value = base_config["order_value"]
        self.max_risk = base_config["max_risk"]
        self.opperation_active = base_config["opperation_active"]
        self.leverage_long_value = base_config["leverage_long_value"]
        self.leverage_short_value = base_config["leverage_short_value"]
        self.use_stop_loss_orders = base_config["use_stop_loss_orders"]
        self.use_stop_gain_orders = base_config["use_stop_gain_orders"]
        self.stop_loss_percentage = base_config["stop_loss_percentage"]
        self.stop_gain_percentage = base_config["stop_gain_percentage"]
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





