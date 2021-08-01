import sqlite3

con = sqlite3.connect('Admin/db.sqlite')
cur = con.cursor()
cur.execute('''
            CREATE TABLE IF NOT EXISTS Users
            (id INTEGER,
            first_name STRING,
            lang STRING,
            stage INTEGER)''')
first_insert = '''
INSERT INTO Users VALUES ('{}', '{}', 'a', 0)
'''
select_id = '''
SELECT id
FROM Users
WHERE id = '{}'
'''
select_first_name = '''
SELECT first_name
FROM Users
WHERE id = '{}'
'''
select_lang = '''
SELECT lang
FROM Users
WHERE id = '{}'
'''
select_stage = '''
SELECT stage
FROM Users
WHERE id = '{}'
'''
update_id = '''
UPDATE Users
SET id = '{}'
WHERE id = '{}'
'''
update_first_name = '''
UPDATE Users
SET first_name = '{}'
WHERE id = '{}'
'''
update_lang = '''
UPDATE Users
SET lang = '{}'
WHERE id = '{}'
'''
update_stage = '''
UPDATE Users
SET stage = '{}'
WHERE id = '{}'
'''