import MySQLdb

conn = MySQLdb.connect(
    host="edvin9kc.beget.tech", user="edvin9kc_edvin",
    passwd="iopl87jkl", db="edvin9kc_edvin")

cur = conn.cursor()

query = "DELETE FROM video_cards";

cur.execute(query)
conn.commit()


cur.close()
conn.close()