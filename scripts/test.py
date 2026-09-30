python3 -c "
from policy_twin.adapters.db import sync_conn
from policy_twin.adapters.graph import age_setup_sync, parse_agtype

graph_name = 'scenario_sc_b99447fca5'

with sync_conn() as conn:
    age_setup_sync(conn)
    sql = f'''
        SELECT * FROM cypher('{graph_name}', \$\$
            MATCH (n) RETURN n.doc_id AS doc_id, count(*) AS c
        \$\$) AS (doc_id agtype, c agtype)
    '''
    for row in conn.execute(sql).fetchall():
        print(parse_agtype(row['doc_id']), parse_agtype(row['c']))
"
