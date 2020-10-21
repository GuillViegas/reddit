from django.db import connections


def generic_execute(query, params={}):
    cursor = connections["default"].cursor()

    cursor.execute(query, params)

    if cursor.description:
        columns = [col[0] for col in cursor.description if cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        cursor.close()

        return rows

    msg = cursor.statusmessage
    cursor.close()

    return msg
