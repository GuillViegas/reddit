from datetime import datetime
from helpers.database import generic_execute
from submission.models import Comment, Submission
from graph_tool.generation import graph_union, complete_graph
from graph_tool.util import find_vertex
import graph_tool as gt
import networkx as nx
import sql


def metric_by_month(report, after, before, period=1, key='count', simple=True):
    month = after.month
    year = after.year
    metrics = []

    while year < before.year or month < before.month:
        a_month, a_year = month, year

        month += period
        if month > 12:
            month -= 12
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


def generate_digraph(after=None, before=None, all_authors=False):
    if all_authors:
        authors = list({author for author in Comment.objects.all().values_list('author_id', flat=True)}.union(
            {author for author in Submission.objects.filter(
                id__in=[comment.submission_id for comment in Comment.objects.all()]
            ).values_list('author_id', flat=True)}
        ))
    else:
        authors = list({author for author in Submission.objects.filter(
            id__in=[comment.submission_id for comment in Comment.objects.all()]
        ).values_list('author_id', flat=True)})

    comments = Comment.objects.filter(
        author__in=authors, created_at__gte=after, created_at__lte=before)
    comments = [comment for comment in comments if comment.author.name != comment.submission.author.name]

    graph = nx.DiGraph()
    graph.add_nodes_from(authors)
    edges = {}

    for comment in comments:
        edges[(comment.author.name, comment.submission.author.name)] = (
            edges.setdefault((comment.author.name, comment.submission.author.name), 0) + 1)

    graph.add_weighted_edges_from([(edge[0], edge[1], edges[edge]) for edge in edges])

    graph.remove_nodes_from([n for n in nx.isolates(graph)])
    return graph


def generate_graph(after=None, before=None):
    submissions = Submission.objects.filter(id__in=[comment.submission_id for comment in Comment.objects.all()]).prefetch_related('author')

    graph = nx.Graph()
    authors = []
    for submission in submissions:

        if submission.created_at.replace(tzinfo=None) >= after and submission.created_at.replace(tzinfo=None) <= before:
            authors.append(submission.author.name)

        authors.extend([
            comment.author.name for comment in Comment.objects.filter(
                submission=submission, created_at__gte=after, created_at__lte=before).prefetch_related('author')])

        submission_graph = nx.complete_graph(authors)
        graph = nx.compose(graph, submission_graph)

    graph.remove_nodes_from([n for n in nx.isolates(graph)])
    return graph


def generate_graph_by_gt(after=None, before=None):
    submissions = [
        s for s in Submission.objects.filter(
            id__in=[comment.submission_id for comment in Comment.objects.all()]).prefetch_related('author')]

    graph = gt.Graph()
    graph.vp['author'] = graph.new_vp('string')
    for submission in submissions:
        authors = set()

        if submission.created_at.replace(tzinfo=None) >= after and submission.created_at.replace(tzinfo=None) <= before:
            authors.add(submission.author.name)

        authors = authors | set(
            comment.author.name for comment in Comment.objects.filter(
                submission=submission, created_at__gte=after, created_at__lte=before).prefetch_related('author'))

        s_graph = complete_graph(len(authors))
        s_graph.vertex_properties['author'] = s_graph.new_vp('string')
        s_graph.vertex_properties['author_idx'] = s_graph.new_vp('int')

        authors = list(authors)
        for author_idx, v in enumerate(s_graph.get_vertices()):
            s_graph.vertex_properties['author'][v] = authors[author_idx]
            rv = find_vertex(graph, graph.vp['author'], s_graph.vp['author'][v])
            s_graph.vertex_properties['author_idx'][v] = graph.vertex_index[rv[0]] if rv else -1

        graph, props = graph_union(graph, s_graph, s_graph.vp['author_idx'], [(graph.vp['author'], s_graph.vp['author'])])
        graph.vp['author'] = props[0]

    return graph


def generate_graph_by_period(graph_type, after, before, period, all_authors=None):
    month = after.month
    year = after.year
    graphs = []

    while year < before.year or month < before.month:
        a_month, a_year = month, year
        month += period
        if month > 12:
            year += 1
            month -= 12

        b_month, b_year = month, year
        graph = None

        if graph_type == 'digraph':
            graph = generate_digraph(
                after=datetime(a_year, a_month, 1, 0, 0, 0),
                before=datetime(b_year, b_month, 1, 0, 0, 0),
                all_authors=all_authors)

        else:
            graph = generate_graph_by_gt(
                after=datetime(a_year, a_month, 1, 0, 0, 0),
                before=datetime(b_year, b_month, 1, 0, 0, 0))

        # graph.graph['period'] = f'{a_month}/{a_year} - {b_month}/{b_year}'
        print(f'{a_month}/{a_year} - {b_month}/{b_year}')
        graphs.append(graph)

    return graphs
