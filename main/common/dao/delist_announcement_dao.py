import psycopg
from config.config import DEV_ENV_CON
from common.domain.delist_announcement import DelistAnnouncement

def get_delist_announcement_by_date(announcement_date: str) -> DelistAnnouncement:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, announcement_date, coin 
                FROM delist_announcement 
                WHERE announcement_date = %s;
                """, (announcement_date,))
            row = cur.fetchone()
            if row:
                return DelistAnnouncement(row['id'], row['announcement_date'], row['coin'])
            return None


def get_delist_announcement_by_coin(coin: str) -> DelistAnnouncement:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, announcement_date, coin 
                FROM delist_announcement 
                WHERE coin = %s;
                """, (coin,))
            row = cur.fetchone()
            if row:
                return DelistAnnouncement(row['id'], row['announcement_date'], row['coin'])
            return None


def get_delist_announcements() -> list[DelistAnnouncement]:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, announcement_date, coin
                FROM delist_announcement;
                """)
            return [DelistAnnouncement(row['id'], row['announcement_date'], row['coin']) for row in cur.fetchall()]


def insert_delist_announcement(announcement_date: str, coin: str) -> DelistAnnouncement:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO delist_announcement (announcement_date, coin) 
                VALUES (%s, %s) 
                RETURNING id, announcement_date, coin;
                """, (announcement_date, coin,))
            row = cur.fetchone()
            return DelistAnnouncement(row['id'], row['announcement_date'], row['coin'])


