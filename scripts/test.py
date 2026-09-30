python3 -c "
from policy_twin.adapters.db import sync_conn
with sync_conn() as conn:
    # 1. does text_chunk actually have data for this doc?
    chunks = conn.execute(
        'SELECT page, count(*) FROM text_chunk WHERE doc_id = %s GROUP BY page ORDER BY page',
        ('d_<your_scenario_id>',)
    ).fetchall()
    print('text_chunk pages:', chunks)

    # 2. what page does the Policy node actually claim?
"
