python3 -c "
from policy_twin.adapters.db import sync_conn
from policy_twin.adapters.graph import age_setup_sync, parse_agtype
graph_name = 'scenario_<your_scenario_id>'
with sync_conn() as conn:
    age_setup_sync(conn)
    sql = f\"SELECT * FROM cypher('{graph_name}', \$\$ MATCH (p:Policy) RETURN p.name AS name, p.doc_id AS doc_id, p.page AS page \$\$) AS (name agtype, doc_id agtype, page agtype)\"
    for row in conn.execute(sql).fetchall():
        print(parse_agtype(row['name']), parse_agtype(row['doc_id']), parse_agtype(row['page']))
"
