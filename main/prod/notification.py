from prod.telegram_notify import TelegramNotify

class Notification(TelegramNotify):
    def notify_operation(
        self,
        pair,
        order_buy,
        order_sell,
        status,
    ):

        msg += f"<b>Operação efetivada</b>:\n"
        msg += f"pair: {coin}\n"

        if order_buy:
            msg += f"Exchange Buy: {order_buy['exchange_id']}\n"
            msg += f"Volume Buy: {order_buy['symbol']} {order_buy.get('volume', '0')}\n"
            msg += f"Quantity Buy: {pair} {order_buy.get('quantity', '0')}\n"
            msg += f"Average Order Price Buy: {order_buy['symbol']} {order_buy.get('average_price', 'N/A')}\n"
            msg += f"Order ID Buy: {order_buy['order_id']}\n\n"

        if order_sell:
            msg += f"Exchange Sell: {order_sell['exchange_id']}\n"
            msg += (
                f"Volume Sell: {order_sell['symbol']} {order_sell.get('volume', '0')}\n"
            )
            msg += f"Quantity Sell: {pair} {order_sell.get('quantity', '0')}\n"
            msg += f"Average Order Price Sell: {order_sell['symbol']} {order_sell.get('average_price', 'N/A')}\n"
            msg += f"Order ID Sell: {order_sell['order_id']}\n\n"

        msg += f"Profit: USD {round(real_profit, 2):,}\n"

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

    def notify_canceled_orders(self, canceled_orders):

        if not canceled_orders:
            self.send_message_alert("No orders canceled (Mercado).")
            return

        msg = "<b>Canceled Orders - Mercado</b>\n\n"

        for order in canceled_orders:
            msg += "Pair: {}\n".format(order["symbol"])
            msg += "ID: {}\n".format(order["id"])
            msg += "Status: {}\n".format(order["status"])
            msg += "Amount: {}\n".format(order["amount"])
            msg += "Filled: {}\n".format(order["filled"])
            msg += "\n"

        self.send_message_alert(msg)
