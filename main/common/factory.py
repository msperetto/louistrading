import sys
from backtesting._util import _Indicator
import pandas as pd

class Factory:
    """_summary_
    Class made to handle the instantiation of Filter, Trigger, Trade and Trend objects.
    In backtest and prod the Strategy classes hold the proper classes to be instantiated.
    When the classes are passed to backtest manager or in prod StrategyManager, the Factory
    will get the correct attributes for each Strategy class and instantiate it correctly.

    """
    @staticmethod
    def create(class_name: str, obj_caller, **kwargs):
        cls = None
        for module in sys.modules.values():
            cls = getattr(module, class_name, None)
            if cls:
                break  # Para ao encontrar a classe

        if not cls:
            raise ValueError(f"Class {class_name} not found")

        # Obter os parâmetros do construtor da classe
        constructor_params = cls.__init__.__code__.co_varnames[1:cls.__init__.__code__.co_argcount]

        # Filtrar os kwargs para incluir apenas os parâmetros necessários pelo construtor
        filtered_kwargs = {key: kwargs[key] for key in constructor_params if key in kwargs}

        # Converter _Indicator em lambdas (exceto 'data')
        lambda_kwargs = {
            key: (lambda key=key, obj_caller=obj_caller: getattr(obj_caller, key)[:len(getattr(obj_caller, key))])
            if (isinstance(value, _Indicator) and key != 'data') or isinstance(value, pd.Series) else value
            for key, value in filtered_kwargs.items()
        }

        # Instanciar a classe com os argumentos processados
        return cls(**lambda_kwargs)
