from helpers.database import generic_execute
import math
import sql


def metric_by_month(report, after, before):
    month = after.month
    year = after.year
    metrics = []

    while year < before.year or month < before.month:
        a_month, a_year = month, year
        month += 1
        if month == 13:
            month = 1
            year += 1

        b_month, b_year = month, year

        result = generic_execute(
            getattr(sql, report.upper()),
            {'after': f'{a_year}-{a_month}-01', 'before': f'{b_year}-{b_month}-01'})

        metrics.append((f'{a_month}/{a_year} - {b_month}/{b_year}', result[0]['count']))

    return metrics
