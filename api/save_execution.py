from api.database import get_connection

def save_test_execution(data):

    conn = get_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO test_execution
    (test_name, status, execution_time, inquiry_no, inquiry_movetype, inquiry_creationdatetime)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    cursor.execute(query, (
        data["test_name"],
        data["status"],
        data["execution_time"],
        data["inquiry_no"],
        data["inquiry_movetype"],
        data["inquiry_creationdatetime"]
    ))

    conn.commit()
    cursor.close()
    conn.close()