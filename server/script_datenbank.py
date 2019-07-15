""" 
Erwartet:
python script_datenbank.py new_user.json

new_user.json ist so aufgebaut:
{"type":"TypeHere","creatorID":"IDHere","key":"KeyHere"}
"""

import sqlite3 as lite
import sys
import json
import fileinput


def add_user(user_dictionary):
    try:
        con = lite.connect('db.sqlite3')
        with con:
            cur = con.cursor()
            cur.execute("INSERT INTO blockchain_key(creatorID, key, type) VALUES(\"{0}\",\"{1}\",\"{2}\")".format(user_dictionary["creatorID"], user_dictionary["key"], user_dictionary["type"]))
            cur.execute("select * from blockchain_key")
            for line in cur.fetchall():
                print(line)
    except:
        print("ERROR while connecting or creating new user")
    finally:
        if con:
            con.close()


if __name__ == "__main__":
    string = ""
    for line in fileinput.input():
        string += line
    u_dic = json.loads(line.encode('ascii','ignore'))
    add_user(u_dic)
