from functools import reduce

import click
import pandas as pd

from strava import api
from strava.formatters import noop_formatter
from strava.utils import to_dataframe, filter_stream_by_from_to, compute_hrtss


def run_detail(activity, from_, to):
    sensors = ['time', 'heartrate']

    # Gets the streams needed.
    stream_by_keys = [to_dataframe(api.get_streams(activity.get('id'), key=key)) for key in sensors]

    # Try to merge the streams.
    try:
        stream_to_merge = [df.drop_duplicates('distance') for df in stream_by_keys]
        stream = reduce(lambda left, right: pd.merge(left, right, on='distance'), stream_to_merge)
    except KeyError:
        try:
            stream_to_merge = [df.drop_duplicates('time') for df in stream_by_keys]
            stream = reduce(lambda left, right: pd.merge(left, right, on='time'), stream_to_merge)
        except KeyError:
            click.echo('Enable to merge the streams on distance or time.')

    stream = filter_stream_by_from_to(stream, from_, to)

    # Could had more cases here:
    # TODO rTSS (Run Training Stress Score)
    metrics, formatters = _run_detail(stream)
    return metrics, formatters


def _run_detail(stream):
    # Computes metrics.
    metrics = dict({
        'tss': compute_hrtss(stream),
    })
    formatters = {
        'tss': noop_formatter,
    }
    return metrics, formatters
