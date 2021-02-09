import sqlite3
from sqlite3 import Error
import re
import os

create_table_sql = """ CREATE TABLE IF NOT EXISTS words (
                                        id integer PRIMARY KEY,
                                        word text NOT NULL,
                                        count integer
                                    ); """
files_path = "files/"
db_name = "words.db"


def create_connection(db_file):
    create_table(db_file, create_table_sql)
    connection = None
    try:
        connection = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return connection


def close_connection(connection):
    if connection:
        connection.close()


def create_table(db_file, create_table_sql):
    try:
        c = sqlite3.connect(db_file)
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def insert_word_info(word_info):
    sql = ''' INSERT INTO words(word,count)
              VALUES(?,?) '''
    cursor = connection.cursor()
    cursor.execute(sql, word_info)
    connection.commit()
    return cursor.lastrowid


def get_count_by_word(word):
    sql = ''' SELECT count FROM words WHERE word=? '''
    cursor = connection.cursor()
    cursor.execute(sql, (word,))

    rows = cursor.fetchall()
    for row in rows:
        return row[0]


def update_word_info(word_info):
    sql = ''' UPDATE words
              SET count = ?
              WHERE word = ?'''
    cursor = connection.cursor()
    cursor.execute(sql, word_info)
    connection.commit()


def select_all_words():
    cursor = connection.cursor()
    cursor.execute("SELECT word, count FROM words ORDER BY count DESC")

    rows = cursor.fetchall()
    for row in rows:
        print(row)


if __name__ == '__main__':
    connection = create_connection(db_name)
    with os.scandir(files_path) as entries:
        for entry in entries:
            print(entry.name)
            file = open(files_path + entry.name, 'r')
            Text = file.read()

            Text = re.sub(r'\d*\n.*-->.*\n', ' ', Text)
            Text = re.sub(r'</?.*>', ' ', Text)

            for char in '-.,!?;[]()"%/\n':
                Text = Text.replace(char, ' ')
            Text = Text.lower()

            word_list = Text.split()

            d = {}
            for word in word_list:
                d[word] = d.get(word, 0) + 1

            word_freq = []
            for key, value in d.items():
                word_freq.append((value, key))

            with connection:
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

                close_connection();
                #select_all_words()