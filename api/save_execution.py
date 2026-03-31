from api.database import get_connection


def save_test_execution(data):
    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO test_execution
    (test_name, status, execution_time, inquiry_no, inquiry_movetype, inquiry_creationdatetime)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    execution_time_raw = data.get("execution_time", 0)

    if isinstance(execution_time_raw, str):
        execution_time = float(execution_time_raw.replace("s", ""))
    else:
        execution_time = float(execution_time_raw)

    cursor.execute(query, (
        data.get("test_name"),
        data.get("status"),
        execution_time,
        data.get("inquiry_no"),
        data.get("inquiry_movetype"),
        data.get("inquiry_creationdatetime")
    ))

    conn.commit()
    cursor.close()
    conn.close()