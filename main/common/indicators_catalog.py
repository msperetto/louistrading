# Dicionário com os atributos da instância, prefixos e os nomes dos atributos de comprimento
indicators_catalog = {
    "intraday_ema_short": {"period_type": "intraday", "prefix": "ema", "length_attr": "intraday_ema_short"},
    "intraday_ema_medium": {"period_type": "intraday", "prefix": "ema", "length_attr": "intraday_ema_medium"},
    "intraday_ema_long": {"period_type": "intraday", "prefix": "ema", "length_attr": "intraday_ema_long"},
    "intraday_sma_short": {"period_type": "intraday", "prefix": "sma", "length_attr": "intraday_sma_short"},
    "intraday_sma_medium": {"period_type": "intraday", "prefix": "sma", "length_attr": "intraday_sma_medium"},
    "intraday_sma_long": {"period_type": "intraday", "prefix": "sma", "length_attr": "intraday_sma_long"},
    "intraday_rsi": {"period_type": "intraday", "prefix": "rsi", "length_attr": "intraday_rsi", "layer_cheap": "intraday_rsi_layer_cheap","layer_expensive": "intraday_rsi_layer_expensive"},
    "trend_ema_short": {"period_type": "trend", "prefix": "ema", "length_attr": "trend_ema_short"},
    "trend_ema_medium": {"period_type": "trend", "prefix": "ema", "length_attr": "trend_ema_medium"},
    "trend_ema_long": {"period_type": "trend", "prefix": "ema", "length_attr": "trend_ema_long"},
    "trend_sma_short": {"period_type": "trend", "prefix": "sma", "length_attr": "trend_sma_short"},
    "trend_sma_medium": {"period_type": "trend", "prefix": "sma", "length_attr": "trend_sma_medium"},
    "trend_sma_long": {"period_type": "trend", "prefix": "sma", "length_attr": "trend_sma_long"},
}
