import sqlite3
from sqlite3 import Error

import os, sys

DB_FILE = 'db.sqlite3'
ASSIGNMENTS = 5
ASSI_FILE = '../CheppyData/Refactory/question_'+str(ASSIGNMENTS)+'/description/'
TC_FILE = '../CheppyData/Refactory/question_'+str(ASSIGNMENTS)+'/testsuite/'
SOL_FILE = '../CheppyData/Refactory/question_'+str(ASSIGNMENTS)+'/reference/'


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# def assignment(conn):
#     sql = """INSERT INTO cheppy_assignment(title, problem, constraint, format, answer) VALUES(?, ?, ?, ?, ?)"""
#     cur = conn.cursor()

#     for (root, dirs, files) in os.walk(ASSI_FILE):
#         for file in files:
#             if file == "description.txt":


#             program = open(root+file).read().strip()

#     cur.execute(sql, (title, problem, constraint, format, answer))
#     conn.commit()
#     conn.close()


def testsuite(conn):
    in_tc_map = {}
    out_tc_map = {}
    for (root, dirs, files) in os.walk(TC_FILE):
        for file in files:
            if file == "global.py":
                continue

            in_out, tc_no = file.split('.')[0].split('_')
            tc = open(root+file).read().strip()

            if in_out == "input":
                in_tc_map[tc_no] = tc
            elif in_out == "output":
                out_tc_map[tc_no] = tc
    
    sql = """INSERT INTO cheppy_testsuite(assignment_no_id, tc_no, in_tc, out_tc, open_tc) VALUES(?, ?, ?, ?, ?)"""
    cur = conn.cursor()

    cur.execute("Select * from cheppy_assignment where assignment_no = ?", (ASSIGNMENTS, ))
    res = cur.fetchone()
    assignment_no = res[0]

    for tc_no, in_tc in in_tc_map.items():
        cur.execute(sql, (assignment_no, tc_no, in_tc, out_tc_map[tc_no], True))
    
    conn.commit()
    conn.close()


def solution(conn):
    sql = """INSERT INTO cheppy_solution(assignment_no_id, program) VALUES(?, ?)"""
    cur = conn.cursor()

    cur.execute("Select * from cheppy_assignment where assignment_no = ?", (ASSIGNMENTS, ))
    res = cur.fetchone()
    assignment_no = res[0]

    for (root, dirs, files) in os.walk(SOL_FILE):
        for file in files:
            program = open(root+file).read().strip()
            cur.execute(sql, (assignment_no, program))
    
    conn.commit()
    conn.close()


# conn = create_connection(DB_FILE)
# testsuite(conn)
# conn = create_connection(DB_FILE)
# solution(conn)




