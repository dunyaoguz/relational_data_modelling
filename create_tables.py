import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def create_database():
    """
    Spins up a local postgres database called sparkifydb. If already exists, drops the existing one and creates a new one.
    """
    # connect to default database
    conn = psycopg2.connect(database='postgres', user='dunya', port='5432')
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create sparkify database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS sparkifydb")
    cur.execute("CREATE DATABASE sparkifydb WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect(database='sparkifydb', user='dunya', port='5432')
    cur = conn.cursor()

    return cur, conn


def drop_tables(cur, conn):
    """
    Drops all the tables in schema. 
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
    Creates the tables in the schema.
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    cur, conn = create_database()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()
