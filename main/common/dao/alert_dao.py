from psycopg import connect, rows
from config.config import DEV_ENV_CON
from common.domain.alert import Alert  

def insert_alert(pair, alert_type, active, message):

    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO alert(pair, alert_type, active, message)
                VALUES(%s, %s, %s, %s)
                RETURNING id, date, pair, alert_type, active, message;
            """, (pair, alert_type, active, message))
            conn.commit()
            insertion = cur.fetchone()
            return Alert(
                        id=insertion["id"],
                        date=insertion["date"],
                        pair=insertion["pair"],
                        alert_type=insertion["alert_type"],
                        active=insertion["active"],
                        message=insertion["message"]
                   )

def get_active_alerts():
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, date, pair, alert_type, active, message
                FROM alert
                WHERE active = True;
            """)
            return [Alert(
                        id=alert["id"],
                        date=alert["date"],
                        pair=alert["pair"],
                        alert_type=alert["alert_type"],
                        active=alert["active"],
                        message=alert["message"]
                   ) for alert in cur.fetchall()]
            