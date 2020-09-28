#Ben Bohnen
#CNA 330 9/27/2020
#This Program creates a networkDB using SQLite

import sqlite3
from sqlite3 import Error

def create_initial_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

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

def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
        :param conn: Connection object
        :param create_table_sql: a CREATE TABLE statement
        :return:
        """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)

def create_host(conn, host):
    """
    Create a new host into the hosts table
    :param conn:
    :param host:
    :return: host id
    """
    sql = ''' INSERT INTO hosts(hostname,url,ip,local_or_remote,description)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host)
    conn.commit()
    return cur.lastrowid

def create_new_host(conn, host):
    """
    Create a new host into the hosts table
    :param conn:
    :param host:
    :return: host id
    """
    sql = ''' INSERT INTO hosts(hostname,url,ip,local_or_remote,description)
              VALUES(?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, host)
    conn.commit()
    return cur.lastrowid

def select_all_hosts(conn):
    """
    Query all rows in the hosts table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM hosts")

    rows = cur.fetchall()

    for row in rows:
        print(row)

def select_host_by_local_or_remote(conn, local_or_remote):
    """
    Query tasks by local_or_remote
    :param conn: the Connection object
    :param local_or_remote:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM hosts WHERE local_or_remote=?", (local_or_remote,))

    rows = cur.fetchall()

    for row in rows:
        print(row)

def table_input():
    database = r"C:\sqlite\db\network.db"

    sql_create_hosts_table = """ CREATE TABLE IF NOT EXISTS hosts (
                                        id integer PRIMARY KEY,
                                        hostname text,
                                        url text, ip text,
                                        local_or_remote text,
                                        description text
                                    ); """
    # create a database connection
    conn = create_connection(database)

    # create table
    if conn is not None:
        # create hosts table
        create_table(conn, sql_create_hosts_table)
    else:
        print("Error! cannot create the database connection.")

def hosts_input():
    database = r"C:\sqlite\db\network.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        # Define hosts
        #host = (id, hostname, url, ip, local_or_remote, description);

        host_1 = ('localhost', 'N/A', '127.0.0.1', 'local', 'loopback')
        host_2 = ('router', 'N/A', '10.0.0.1', 'local', 'Default Gateway')
        host_3 = ('FrankenSystem', 'N/A', '10.0.0.15', 'local', 'Local address for my headless gaming host')
        host_4 = ('MSI', 'N/A', '10.0.0.13', 'local', 'Laptop')
        host_5 = ('Puget Systems', 'www.pugetsystems.com', '104.20.179.42', 'remote', 'Puget Systems Home Page')
        host_6 = ("No Man's Sky", "www.nomanssky.com", '40.114.41.245', 'remote', "NMS official website")
        host_7 = ('Steam', 'https://store.steampowered.com/', '23.193.145.218', 'remote', "Steam store webpage")
        host_8 = ('NVIDIA', 'www.nvidia.com', '104.112.186.212', 'remote', 'NVIDIA home page')
        host_9 = ('Amazon', 'www.amazon.com', '13.224.15.188', 'remote', 'Amazon home page')


        # create hosts
        create_host(conn, host_1)
        create_host(conn, host_2)
        create_host(conn, host_3)
        create_host(conn, host_4)
        create_host(conn, host_5)
        create_host(conn, host_6)
        create_host(conn, host_7)
        create_host(conn, host_8)
        create_host(conn, host_9)

def query_hosts():
    database = r"C:\sqlite\db\network.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        print("1. Query host by local hosts:")
        select_host_by_local_or_remote(conn, 'local')

        print("2. Query host by remote hosts:")
        select_host_by_local_or_remote(conn, 'remote')

        print("2. Query all hosts")
        select_all_hosts(conn)

def main():
    task = int(input("Enter 1 to create table and hosts, 2 for query, or 3 to enter a new host (4 to exit): "))
    while task != 0:
        if task == 1:
            table_input() #creates a table called "Hosts"
            hosts_input() #Enters 4 local hosts and 5 remote hosts into the table
            print("Table has been created and hosts have been entered.")
            task = int(input("Enter 1 to create table and hosts, 2 for query, or 3 to enter a new host (4 to exit): "))
        elif task == 2:
            query_hosts() #Queries for local hosts, remote hostes, and all hosts
            task == 0
            task = int(input("Enter 1 to create table and hosts, 2 for query, or 3 to enter a new host (4 to exit): "))
        elif task == 4:
            print("Goodbye")
            break
        elif task == 3:
            database = r"C:\sqlite\db\network.db"

            # create a database connection
            conn = create_connection(database)
            hostname = input("Please enter hostname: ")
            url = input("Please enter url: ")
            ip = input("Please enter ip: ")
            localremote = input("Please enter if local or remote (use all lower case): ")
            desc = input("Please enter a description: ")
            host = (hostname, url, ip, localremote, desc)
            create_new_host(conn, host) #creates a new host using the user input
            task = int(input("Enter 1 to create table and hosts, 2 for query, or 3 to enter a new host (4 to exit): "))
        else:
            task = int(input("Enter 1 to create table and hosts, 2 for query, or 3 to enter a new host (4 to exit): "))


if __name__ == '__main__':
    create_initial_connection(r"C:\sqlite\db\network.db")
    main()

