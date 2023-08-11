import psycopg

from psycopg import sql


def run_sql(conn_str: str, query: str):
    with psycopg.connect(conn_str, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(query)


def create_table(conn_str: str, table_name: str, columns: list[str], primary_key: str):
    query = sql.SQL(
        "CREATE TABLE IF NOT EXISTS public.{0} ({1}, CONSTRAINT {0}_pkey PRIMARY KEY ({2}))"
    ).format(
        sql.SQL(table_name),
        sql.SQL(', ').join(map(sql.SQL, columns)),
        sql.SQL(', ').join(map(sql.SQL, primary_key))
    )
    run_sql(conn_str=conn_str, query=query)
