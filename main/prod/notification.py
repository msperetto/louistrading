from prod.telegram_notify import TelegramNotify

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

        msg += f"Operation Time: {operation_time}\n"
        msg += f"Volume: USDT {volume}\n"
        msg += f"Quantity: {quantity}\n"
        msg += f"Average Order Price: USDT {average_price}\n"
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
        operation_time,
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
        msg += f"Operation Time: {entry_time}\n"
        msg += f"Average Order Price Entry: USDT {entry_price}\n\n"

        msg += f"<i>Close Details:</i>\n"
        msg += f"Operation Time: {operation_time}\n"
        msg += f"Volume: USDT {volume}\n"
        msg += f"Quantity: {quantity}\n"
        msg += f"Average Order Price Close: USDT {average_price}\n"
        msg += f"Order ID Sell: {order_id}\n\n"

        msg += f"Spread: {spread}\n"
        msg += f"Profit: {profit}\n"
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


    def notify_open_orders(self, open_orders):

        if not open_orders:
            self.send_message_alert("No open orders (Mercado).")
            return

        msg = "<b>Open Orders - Mercado</b>\n\n"

        for order in open_orders:
            msg += "Pair: {}\n".format(order["symbol"])
            msg += "ID: {}\n".format(order["id"])
            msg += "Status: {}\n".format(order["status"])
            msg += "Amount: {}\n".format(order["amount"])
            msg += "Filled: {}\n".format(order["filled"])
            msg += "\n"

        self.send_message_alert(msg)

