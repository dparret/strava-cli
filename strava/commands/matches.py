import click

from strava.formatters import format_property, apply_formatters
from strava import api
from strava.decorators import output_option, login_required, format_result, TableFormat, OutputType
from strava.utils import ride_count_matches

ACTIVITY_COLUMNS = ('key', 'value')


@click.command(name='matches',
               help='Count number of matches for a provided watts input.')
@click.argument('activity_id', required=True, nargs=1)
@click.option('--from', '-f', 'from_', nargs=3, type=int, default=None,
              help='Select the start time to narrow the computation to a specific part of the activity.\n If not select the start of the activity is used.\n Need to be entered as 3 numbers, first is the hours, second the minutes ans last the seconds.')
@click.option('--to', '-t', 'to', nargs=3, type=int, default=None,
              help='Select the end time to narrow the computation to a specific part of the activity.\n If not select the end of the activity is used.\n Need to be entered as 3 numbers, first is the hours, second the minutes ans last the seconds.')
@click.option('--watts', '-w', type=int, required=True,
                help='Count the number of matches above that number of watts.')
@click.option('--min_time', '-time', type=int, default=10,
              help='Minimal threshold to cound matches. Has to be provided in seconds, by default 10.')
@output_option()
@login_required
def count_matches(output, activity_id, from_, to, watts, min_time):
    activity = api.get_activity(activity_id)
    metrics, formatters = ride_count_matches(activity, from_, to, watts, min_time)
    return _format_activity(metrics, formatters, output)


@format_result(table_columns=ACTIVITY_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_activity(metrics, formatters, output=None):
    return metrics if output == OutputType.JSON.value else _as_table(metrics, formatters)


def _as_table(metrics, formatters):
    return [{'key': format_property(k), 'value': v} for k, v in apply_formatters(metrics, formatters).items()]
