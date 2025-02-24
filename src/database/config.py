INSERT_QUERY = """
INSERT INTO pipeline (run_id, timestamp, predictions, summary, traceability, log_status)
VALUES (%s, %s, %s, %s, %s, %s)
"""
