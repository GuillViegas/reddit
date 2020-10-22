from helpers.database import generic_execute
from submission.models import Comment, Submission
import networkx as nx
import math
import sql


def metric_by_month(report, after, before, key='count', simple=True):
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

        metrics.append(
            (
                f'{a_month}/{a_year} - {b_month}/{b_year}',
                result[0][key] if simple else [r[key] for r in result]))

    return metrics

def generate_digraph():
    authors = list({author for author in Submission.objects.filter(
        id__in=[comment.submission_id for comment in Comment.objects.all()]
    ).values_list('author_id', flat=True)})

    comments = Comment.objects.filter(author__in=authors)
    comments = [comment for comment in comments if comment.author.name != comment.submission.author.name]

    graph = nx.DiGraph()
    graph.add_nodes_from(authors)
    edges = {}

    for comment in comments:
        edges[(comment.author.name, comment.submission.author.name)] = (
            edges.setdefault((comment.author.name, comment.submission.author.name), 0) + 1)

    graph.add_weighted_edges_from([(edge[0], edge[1], edges[edge]) for edge in edges])

    return graph

def generate_graph():
    submissions = Submission.objects.filter(id__in=[comment.submission_id for comment in Comment.objects.all()])

    graph = nx.Graph()
    for submission in submissions:
        authors = [submission.author.name]
        authors += [comment.author.name for comment in Comment.objects.filter(submission=submission)]

        submission_graph = nx.complete_graph(authors)
        graph = nx.compose(graph, submission_graph)

    return graph
