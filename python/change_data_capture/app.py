import psycopg2
import psycopg2.extras
import datetime
import time
from utils import consume

# For logical replication, we use connection_factory parameter
LogicalReplicationConnection = psycopg2.extras.LogicalReplicationConnection

DB_CONFIG = {
    "database": "mydb",
    "user": "myuser",
    "password": "password",
    "host": "localhost",
    "port": 5431,
}

REPLICATION_SLOT_NAME = "my_replication_slot"

try:
    conn = psycopg2.connect(
        **DB_CONFIG, connection_factory=LogicalReplicationConnection
    )

    print("database is connected successfully.")

    cur = conn.cursor()

    cur.start_replication(slot_name=REPLICATION_SLOT_NAME, decode=True, start_lsn="0/0")

    print(f"Starting replication stream for slot '{REPLICATION_SLOT_NAME}'...")

    while True:
        msg = cur.read_message()

        if msg:
            # consume the message and push to kinesis
            consume(msg)
            cur.send_feedback(flush_lsn=msg.data_start)
        else:
            now = datetime.datetime.now()
            timeout = 10.0 - (now - cur.io_timestamp).total_seconds()

            if timeout <= 0:
                cur.send_feedback()
                timeout = 10.0

            # Wait for more data
            time.sleep(0.1)
except KeyboardInterrupt as e:
    print("\nCDC client gracefully stopped by user.")

except Exception as e:
    print(f"Error: {e}")

finally:
    
    if 'cur' in locals() and cur:
        cur.close()
    if 'conn' in locals() and conn:
        conn.close()
        print("Connection closed.")