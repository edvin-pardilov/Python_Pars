import MySQLdb

from db import conn

cur = conn.cursor()

query = "DELETE FROM video_cards";

cur.execute(query)
conn.commit()


cur.close()
conn.close()