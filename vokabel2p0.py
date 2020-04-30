# -*- coding: utf-8 -*-
"""
Created on Thu Apr 30 09:57:31 2020

@author: kaise
"""

import sqlite3
import MySQLdb

def create_remote_connection():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = MySQLdb.connect(
            host = 'db4free.net', 
            user = 'jayjay123', 
            passwd = 'yzm][h20+}rNV6y=', 
            db = 'vocabulary', 
            port = 3306)
        return conn
    except sqlite3.Error as e:
        print(e) 
        
    return conn

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e) 
        
    return conn

def create_tables(conn):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :return:
    """
    
    sql_create_vocabulary_table = """ CREATE TABLE IF NOT EXISTS vocabulary (
                                        english text NOT NULL,
                                        german text NOT NULL,
                                        lection text NOT NULL
                                    ); """
    
    try:
        c = conn.cursor()
        c.execute(sql_create_vocabulary_table)
    except Error as e:
        print(e)
    
def insert_new_vocabulary(conn, english, deutsch):
    """
    :param conn:
    :param english: the english word
    :param deutsch: the german word
    :return: last row id if vocabulary was successfully inserted, 0 if it already existed
    """
    
    sql = ''' INSERT INTO vocabulary(english, german,lection)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute("SELECT rowid FROM vocabulary WHERE english = ?", (english,))
    data=cur.fetchone()
    if data is None:
        cur.execute(sql, (english, deutsch, "standard",))
        return cur.lastrowid
    else:
        return 0
    
def get_vocabulary_list(conn, lection):
    """
    calculate the ratio between won and played turnaments
    Parameters
    ----------
    conn : 
        database connection.
    lection : 
        the specific lection if we do not want to show all
    Returns
    list of vocabulary
    -------

    """
    
    vocabulary_list = []
    cur = conn.cursor()
    cur.execute("SELECT * FROM vocabulary WHERE lection = ?", (lection,))
    for word in cur.fetchall():
        vocabulary_list.append(word)
    
    return vocabulary_list

def print_vocabulary_list(vocabulary_list):
    """
    Parameters
    ----------
    vocabulary_list : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for index, word in enumerate(vocabulary_list):
        print("%i: %25s | %s"%(index, word[0], word[1]))
    

def show_menu(conn):
    cmd = ""
    
    while( not (cmd =="exit") ):
        cmd = input("Enter Command: ")
        
        if(cmd == "list"):
            print("we want to print a list of all vocabulary")
            print_vocabulary_list(get_vocabulary_list(conn,"standard"))
        elif(cmd == "new"):
            english = input("Enter english word: ")
            deutsch = input("Enter german word: ")
            
            result = insert_new_vocabulary(conn, english, deutsch)
    
            if(result == 0):
                print("this vocabulary is already in the database")


if __name__ == "__main__":
        
    conn = create_connection(r"vocabulary.db")
    #conn = create_remote_connection()
    create_tables(conn)
    
    show_menu(conn)
    
    if(conn):
        conn.commit()
        conn.close()