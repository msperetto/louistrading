import psycopg
from config.config import MARLIN_DB_CON as DEV_ENV_CON
from common.domain.list_announcement import ListAnnouncement

def get_list_announcements() -> list[ListAnnouncement]:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, captured_date
                FROM list_announcement;
                """)
            return [ListAnnouncement(row['id'], row['title'], row['captured_date']) for row in cur.fetchall()]

def get_list_announcement_by_id(announcement_id: int) -> ListAnnouncement:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, captured_date 
                FROM list_announcement 
                WHERE id = %s;
                """, (announcement_id,))
            row = cur.fetchone()
            if row:
                return ListAnnouncement(row['id'], row['title'], row['captured_date'])
            return None


def insert_list_announcement(announcement_id:int, title: str, captured_date: str) -> ListAnnouncement:
    with psycopg.connect(DEV_ENV_CON, row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO list_announcement (id, title, captured_date) 
                VALUES (%s, %s, %s) 
                RETURNING id, title, captured_date;
                """, (announcement_id, title, captured_date,))
            row = cur.fetchone()
            return ListAnnouncement(row['id'], row['title'], row['captured_date'])