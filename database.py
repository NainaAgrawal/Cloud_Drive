import pymysql.cursors
import pandas as pd

conn = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'root',
    password = 'root',
    )
cursor = conn.cursor()

queries = [
    "drop database if exists cloud",
    "create database cloud",
    "use cloud",

    """CREATE TABLE users (
    user_id int auto_increment primary key,
    f_name varchar(15),
    l_name varchar(15) NOT NULL,
    dob datetime DEFAULT NULL,
    email varchar(50) DEFAULT NULL,
    phone_no char(10) DEFAULT NULL,
    passwd varchar(50) DEFAULT NULL,
    question varchar(30) DEFAULT NULL,
    signup_date datetime DEFAULT NULL
    )""",

    """CREATE TABLE file (
    file_id char(6) NOT NULL primary key,
    user_id char(6) DEFAULT NULL,
    category varchar(20) DEFAULT NULL,
    uploaded_date datetime DEFAULT NULL,
    updated_date datetime DEFAULT NULL
    )""",

    """ CREATE TABLE document (
    file_id char(6) NOT NULL,
    file_name varchar(30),
    document_size int(15) DEFAULT NULL
    ) """,

    """CREATE TABLE image (
    file_id char(6) NOT NULL ,
    file_name varchar(30),
    image_size int(15) DEFAULT NULL
    )""",


    """CREATE TABLE others (
    file_id char(6) NOT NULL ,
    file_name varchar(30)
    ) """,


    """CREATE TABLE starred (
    file_id char(6) NOT NULL ,
    file_name varchar(30),
    starred_date datetime DEFAULT NULL
    ) """,


    """CREATE TABLE trash (
    file_id char(6) NOT NULL,
    file_name varchar(30),
    trash_size char(6) DEFAULT NULL,
    trash_date datetime DEFAULT NULL,
    no_of_days datetime DEFAULT NULL
    )""",

    """CREATE TABLE video (
    file_id char(6) NOT NULL,
    file_name varchar(30),
    image_size int(15) DEFAULT NULL)"""
    
]

for i in queries:
    cursor.execute(i)
    conn.commit()