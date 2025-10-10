from psycopg import connect, rows
from config.config import DEV_ENV_CON
from common.domain.test_delist_announcement import TestDelistAnnouncement

def get_unprocessed_test_announcements():
    """
    Get all unprocessed test delist announcements.
    :return: A list of TestDelistAnnouncement objects
    """
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, announcement_date, coins, created_at, processed, notes
                FROM test_delist_announcement 
                WHERE processed = FALSE
                ORDER BY created_at ASC;
            """)
            result_rows = cur.fetchall()
            return [
                TestDelistAnnouncement(
                    id=row["id"],
                    title=row["title"],
                    announcement_date=row["announcement_date"],
                    coins=row["coins"],
                    created_at=row["created_at"],
                    processed=row["processed"],
                    notes=row["notes"]
                ) for row in result_rows
            ]

def insert_test_announcement(title, announcement_date, coins, notes=None):
    """
    Insert a new test delist announcement.
    :param title: The announcement title
    :param announcement_date: The delisting date (YYYY-MM-DD format)
    :param coins: List of coin symbols
    :param notes: Optional notes
    :return: The ID of the inserted announcement
    """
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO test_delist_announcement (title, announcement_date, coins, notes)
                VALUES (%s, %s, %s, %s)
                RETURNING id;
            """, (title, announcement_date, coins, notes))
            result = cur.fetchone()
            conn.commit()
            return result[0] if result else None

def mark_announcement_processed(announcement_id):
    """
    Mark a test announcement as processed.
    :param announcement_id: The ID of the announcement to mark as processed
    """
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE test_delist_announcement 
                SET processed = TRUE 
                WHERE id = %s;
            """, (announcement_id,))
            conn.commit()

def get_all_test_announcements():
    """
    Get all test announcements (processed and unprocessed).
    :return: A list of TestDelistAnnouncement objects
    """
    with connect(DEV_ENV_CON, row_factory=rows.dict_row) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT id, title, announcement_date, coins, created_at, processed, notes
                FROM test_delist_announcement 
                ORDER BY created_at DESC;
            """)
            result_rows = cur.fetchall()
            return [
                TestDelistAnnouncement(
                    id=row["id"],
                    title=row["title"],
                    announcement_date=row["announcement_date"],
                    coins=row["coins"],
                    created_at=row["created_at"],
                    processed=row["processed"],
                    notes=row["notes"]
                ) for row in result_rows
            ]

def delete_test_announcement(announcement_id):
    """
    Delete a test announcement.
    :param announcement_id: The ID of the announcement to delete
    """
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM test_delist_announcement 
                WHERE id = %s;
            """, (announcement_id,))
            conn.commit()

def clear_all_test_announcements():
    """
    Delete all test announcements.
    """
    with connect(DEV_ENV_CON) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                DELETE FROM test_delist_announcement;
            """)
            conn.commit()
