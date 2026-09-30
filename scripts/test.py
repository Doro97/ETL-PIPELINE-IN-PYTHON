result = graph.invoke(initial_state, config)
print(f"[ask] graph.invoke returned -- template_id={result.get('template_id')!r} flags={result.get('flags')!r} data_points_count={len(result.get('data_points', []))}")
