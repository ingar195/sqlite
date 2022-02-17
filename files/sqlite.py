import logging
import sqlite3


def connect():
    conn = create_connection("db.sqlite3")

    if conn is not None:

        sql_create_hosts_table = f""" CREATE TABLE IF NOT EXISTS hosts (
            id integer PRIMARY KEY,
            host_name text NOT NULL,
            online boolean NOT NULL,
            host_available boolean NOT NULL
            ); """
        create_table(conn, sql_create_hosts_table)

        sql_create_instructions_table = f""" CREATE TABLE IF NOT EXISTS instructions (
            id integer PRIMARY KEY,
            name text NOT NULL,
            program_path text NOT NULL,
            working_dir text NOT NULL,
            args text NOT NULL
            ); """
        create_table(conn, sql_create_instructions_table)

    else:
        logging.error("Error! cannot create the database connection.")

    return conn


def create_connection(db_file):
    try:
        conn = sqlite3.connect(db_file)
        return conn

    except sqlite3.Error as e:
        logging.error(e)


def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)

    except sqlite3.Error as e:
        logging.error(e)


def sql(sql_command):
    logging.debug(sql_command)
    try:
        conn = connect()
        conn.execute(sql_command)
        conn.commit()
        conn.close()

    except sqlite3.Error as e:
        logging.error(e)


def get_all_tables():
    conn = connect()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = c.fetchall()
    logging.debug(tables)
    return tables


def append_db(table_name, data):
    conn = connect()
    logging.debug(table_name)
    logging.debug(data)
    sql_command = ""

    if table_name == "hosts":
        logging.debug("hosts")

        search_return = search_db(table_name, data['host_name'])

        sql_command = f"""
            INSERT INTO hosts(id, host_name, online, host_available)
            VALUES(null,'{data['host_name']}','{data['online']}','{data['host_available']}') """

    elif table_name == "instructions":
        logging.debug("instructions")

        search_return = search_db("instructions", data['name'])

        sql_command = f"""
            INSERT INTO instructions(id, name, program_path, working_dir, args)
            VALUES(null,'{data['name']}','{data['program_path']}','{data['working_dir']}','{data['args']}') """

    elif table_name == "groups":
        logging.debug("groups")
        # logging.debug(data['content'])

        groups_append(data)
        search_return = None
    else:
        logging.error("Table name not found")

    if search_return is None and table_name != "groups":
        sql(sql_command)
        logging.info("Appended to DB")

    else:
        logging.error(f"Already in DB: {data}")


def groups_append(data):
    logging.debug(data)

    for name in data:
        table_name = name
        logging.debug(table_name)
        logging.debug(data[table_name])

        search_return = get_all_tables()

        db_list = []
        for db in search_return:
            db_list.append(db[0])
        logging.debug(db_list)

        # Check if DB already exists
        if not table_name in db_list:
            logging.debug(table_name)
            sql(f""" CREATE TABLE {table_name} (
                id integer PRIMARY KEY,
                program text NOT NULL,
                host_name text NOT NULL,
                pid text NOT NULL
                ); """)

            # Store all hosts and instructions in lists
            hosts_dump = dump_table("hosts")
            instructions_dump = dump_table("instructions")
            logging.debug(hosts_dump)
            logging.debug(instructions_dump)

            for group in data[table_name]:
                logging.debug("----------------------------------------------------")
                logging.debug(group)

                # {"name": "Web",
                # "content": [{"name": "Facebook", "host_name": "INGAR-G", "pid": ""},
                #             {"Google": "Miner", "host_name": "a", "pid": ""}]}
                sql_command = f"""INSERT INTO {table_name}
                                (id, program, host_name, pid)
                                VALUES(null, '{group['name']}', '{group['host_name']}','0') """
                sql(sql_command)

                logging.debug("----------------------------------------------------end")


def search_db(table_name, phrase):
    logging.debug(f"Searching {table_name} for {phrase}")
    conn = connect()
    try:
        if table_name == "hosts":
            sql_command = f""" SELECT * FROM {table_name} WHERE host_name = '{phrase}';"""

        elif table_name == "instructions" or table_name == "groups":
            sql_command = f""" SELECT * FROM {table_name} WHERE name = '{phrase}';"""
        
        else:
            sql_command = f""" SELECT * FROM {table_name};"""

        if sql_command is not None:
            cursor = conn.cursor()
            cursor.execute(sql_command)
            search_results = cursor.fetchall()
            logging.debug(type(search_results))
            logging.debug(len(search_results))
            if len(search_results) != 0:
                return search_results
            else:
                logging.error(f"No results found for {phrase}")

        else:
            logging.error("No SQL command found")

    except sqlite3.Error as e:
        logging.error(e)


def dump_table(table):
    conn = connect()
    sql_command = f""" SELECT * FROM {table};"""
    cursor = conn.cursor()
    cursor.execute(sql_command)
    search_results = cursor.fetchall()

    logging.debug(search_results)
    return search_results


def get_groups(table):    
    exclude  = ("hosts", "instructions")
    groups = []
    for table in get_all_tables():
        if table[0] not in exclude:
            logging.debug(table[0])
            groups.append(table[0])
    logging.debug(groups)
    return groups


def update_db(table_name, db_colum_name, data, search_phrase, db_colum_value):
    logging.debug(f"Update {table_name} with {data}")
    conn = connect()

    sql_command = f""" UPDATE {table_name} SET {db_colum_name} = '{data}' WHERE {db_colum_value} = '{search_phrase}'"""

    logging.info(f"Updating table: {table_name}, colum:{db_colum_name} with: {data}")
    sql(sql_command)
