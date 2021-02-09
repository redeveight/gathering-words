from collections import Counter
import re
import os
import sqlite3
from sqlite3 import Error
from os import path
import time

file_name = "files/Mr. Robot - 01x01 - HELLOFRIEND.MOV.PROPER.LOL.English.srt"

create_table_sql = """ CREATE TABLE IF NOT EXISTS words (
                                        id integer PRIMARY KEY,
                                        word text NOT NULL,
                                        count integer
                                    ); """


def create_connection(db_file):
    create_table(db_file, create_table_sql)
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        #print(sqlite3.version)
    except Error as e:
        print(e)
    '''finally:
        if conn:
            conn.close()'''
    return conn


def create_table(db_file, create_table_sql):
    try:
        c = sqlite3.connect(db_file)
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_word_info(word_info):
    sql = ''' INSERT INTO words(word,count)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, word_info)
    conn.commit()
    return cur.lastrowid


def get_count_by_word(word):
    sql = ''' SELECT count FROM words WHERE word=? '''
    cur = conn.cursor()
    cur.execute(sql, (word,))

    rows = cur.fetchall()

    for row in rows:
        return row[0]


def select_all_words():
    cur = conn.cursor()
    cur.execute("SELECT word, count FROM words ORDER BY count DESC")

    rows = cur.fetchall()

    for row in rows:
        print(row)


def update_word_info(word_info):
    sql = ''' UPDATE words
              SET count = ?
              WHERE word = ?'''
    cur = conn.cursor()
    cur.execute(sql, word_info)
    conn.commit()


if __name__ == '__main__':
    conn = create_connection(r"words.db")

    with os.scandir('files/') as entries:
        for entry in entries:
            print(entry.name)
            file = open('files/' + entry.name, 'r')
            Text = file.read()

            Text = re.sub(r'\d*\n.*-->.*\n', ' ', Text)
            Text = re.sub(r'</?.*>', ' ', Text)
            #Text = re.sub(r'\d*', ' ', Text)

            for char in '-.,!?;[]()"%/\n':
                Text = Text.replace(char, ' ')
            Text = Text.lower()

            word_list = Text.split()
            #print(word_list)

            d = {}

            # counting number of times each word comes up in list of words (in dictionary)
            for word in word_list:
                d[word] = d.get(word, 0) + 1

            word_freq = []
            for key, value in d.items():
                word_freq.append((value, key))

            # word_freq.sort(reverse=True)
            with conn:
                for word_info in word_freq:
                    current_count_value = 0
                    try:
                        current_count_value = int(get_count_by_word(word_info[1]))
                    except TypeError:
                        reversed_word_info = (word_info[1], word_info[0])
                        insert_word_info(reversed_word_info)
                        continue

                    current_count_value = get_count_by_word(word_info[1])
                    new_word_info = (current_count_value + word_info[0], word_info[1])
                    update_word_info(new_word_info)

                #select_all_words()