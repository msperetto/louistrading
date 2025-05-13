from prod.telegram_notify import TelegramNotify
from common.constants import DATETIME_FORMAT

class Notification(TelegramNotify):
    def notify_opened_trade(
        self,
        pair,
        trade_id,
        side,
        strategy,
        operation_time,
        volume,
        quantity,
        average_price,
        order_id
    ):

        msg = f"<b>🆕Opened Trade</b>:\n"
        msg += f"Pair: {pair}\n"
        msg += f"Trade ID: {trade_id}\n"
        msg += f"Side: {side}\n"
        msg += f"Strategy: {strategy}\n\n"

        msg += f"Operation Time (UTC): {operation_time}\n"
        msg += f"Volume: USDT {round(float(volume), 2)}\n"
        msg += f"Quantity: {quantity}\n"
        msg += f"Average Order Price: USDT {round(float(average_price), 2)}\n"
        msg += f"Order ID: {order_id}\n\n"

        self.send_message_operation(msg)
    
    def notify_closed_trade(
        self,
        pair,
        trade_id,
        side,
        strategy,
        entry_time,
        entry_price,
        entry_quantity,
        entry_order_id,
        entry_volume,
        operation_time_close,
        volume,
        quantity,
        average_price,
        order_id,
        spread,
        profit,
        ROI
    ):

        msg = f"<b>✅Closed Trade</b>:\n"
        msg += f"Pair: {pair}\n"
        msg += f"Trade ID: {trade_id}\n"
        msg += f"Side: {side}\n"
        msg += f"Strategy: {strategy}\n\n"

        msg += f"<i>Entry Details:</i>\n"
        try:
            operation_time = entry_time.strftime(DATETIME_FORMAT)
        except ValueError:
            operation_time = 'Error Value'
        except TypeError:
            operation_time = 'Error Type'
        except Exception as e:
            operation_time = f'Error: {e}'

        msg += f"Operation Time (UTC): {operation_time}\n"
        msg += f"Volume: USDT {round(float(entry_volume), 2)}\n"
        msg += f"Quantity: {entry_quantity}\n"
        msg += f"Average Order Price: USDT {entry_price}\n"
        msg += f"Order ID Buy: {entry_order_id}\n\n"

        msg += f"<i>Close Details:</i>\n"
        msg += f"Operation Time (UTC): {operation_time_close}\n"
        msg += f"Volume: USDT {round(float(volume), 2)}\n"
        msg += f"Quantity: {quantity}\n"
        msg += f"Average Order Price: USDT {average_price}\n"
        msg += f"Order ID Sell: {order_id}\n\n"

        msg += f"Spread: {round(float(spread)*100, 2)}%\n"
        msg += f"Profit: USDT {round(float(profit), 2)}\n"
        msg += f"ROI: {ROI}"

        self.send_message_operation(msg)

    def notify_alert(self, alerts, many=True):
        msg = ""
        if many:
            msg += f"<b>ALERTS</b>: \n"
            for alert in alerts:
                msg += self._get_emoji_from_alert(alert)
                msg += f"{alert.pair} - {alert.message}\n"
        else:
            msg += self._get_emoji_from_alert(alerts)
            msg += f"<b>Alert:</b> - {alerts.pair} - {alerts.message}\n"

        self.send_message_alert(msg)

