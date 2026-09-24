@router.post("/scenarios", status_code=202, response_model=ScenarioStatus)
async def create_scenario(
    background_tasks: BackgroundTasks,
    file: UploadFile | None = None,
    gcs_uri: str | None = Query(None, description="GCS URI (gs://bucket/path) -- alternative to multipart upload"),
    pool: asyncpg.Pool = Depends(get_db),
):
    if not file and not gcs_uri:
        raise HTTPException(400, "Provide either a file upload or gcs_uri")

    if file:
        data = await file.read()
        filename = file.filename or "upload.pdf"
        content_type = file.content_type or "application/pdf"
    else:
        from policy_twin.adapters.blob import read_blob
        blob_path = gcs_uri.replace("gs://", "")
        data = read_blob(blob_path)
        filename = gcs_uri.split("/")[-1]
        content_type = "application/pdf"

    sha = hashlib.sha256(data).hexdigest()

    # Check whether this exact file was already uploaded and fully processed.
    async with pool.acquire() as conn:
        existing = await conn.fetchrow(
            "SELECT doc_id FROM source_document WHERE sha256 = $1 AND status = 'active'",
            sha,
        )

    if existing:
        existing_doc_id = existing["doc_id"]
        existing_scenario_id = (
            existing_doc_id[2:] if existing_doc_id.startswith("d_") else existing_doc_id
        )
        if _extraction_already_complete(existing_scenario_id):
            print(f"[create_scenario] duplicate file (sha256={sha[:12]}...) -- "
                  f"reusing scenario_id={existing_scenario_id}, skipping extraction")
            return ScenarioStatus(
                scenario_id=existing_scenario_id,
                status="ready",
                created_at=datetime.now(timezone.utc),
            )
        # else: a prior attempt exists but never finished (e.g. crashed mid-extraction) --
        # fall through and process as a new upload rather than returning a dead end.
        print(f"[create_scenario] duplicate file found but extraction incomplete for "
              f"{existing_scenario_id} -- reprocessing as new scenario")

    scenario_id = f"sc_{_uid.uuid4().hex[:10]}"
    now = datetime.now(timezone.utc)
    doc_id = f"d_{scenario_id}"

    from policy_twin.adapters.blob import store_blob
    blob_path = f"scenarios/{scenario_id}/{filename}"
    store_blob(blob_path, data)

    async with pool.acquire() as conn:
        await conn.execute(
            """
            INSERT INTO source_document
                (doc_id, publication, url, publisher, fetched_at, sha256, byte_size, mime, blob_uri, status)
            VALUES ($1, $2, $3, 'scenario_upload', $4, $5, $6, $7, $8, 'active')
            """,
            doc_id, f"scenario-{scenario_id}", f"upload://{scenario_id}/{filename}",
            now, sha, len(data), content_type, blob_path,
        )

    create_scenario_graph(scenario_id)
    background_tasks.add_task(_process_scenario_document, doc_id, None)

    return ScenarioStatus(scenario_id=scenario_id, status="processing", created_at=now)


def _extraction_already_complete(scenario_id: str) -> bool:
    """True only if the scenario's graph genuinely has nodes -- not just
    that a source_document row exists. A row can exist with an empty
    graph if a prior extraction attempt crashed (auth failure, LLM error,
    etc.) before writing anything.
    """
    from policy_twin.adapters.db import sync_conn
    from policy_twin.adapters.graph import age_setup_sync, parse_agtype

    graph_name = f"scenario_{scenario_id}"
    try:
        with sync_conn() as conn:
            age_setup_sync(conn)
            sql = f"SELECT * FROM cypher('{graph_name}', $$ MATCH (n) RETURN count(n) AS c $$) AS (c agtype)"
            row = conn.execute(sql).fetchone()
            return parse_agtype(row["c"]) > 0
    except Exception:
        # graph doesn't exist yet, or query failed -- treat as not complete
        return False
