import datetime

import click
from strava.utils import activities_ga_kwargs, filter_unique_week_flag

from strava.decorators import output_option, login_required

from strava.utils.form import get_form_with_formatted_date

_DAY_TITLE = ['## Monday', '## Tuesday', '## Wednesday', '## Thursday', '## Friday', '## Saturday', '## Sunday']

@click.command(name='week',
               help='Provides the fitness, fatigue and form for all day of a week.'
               )
@click.option('--current', '-c', is_flag=True, default=False,
              help='[DEFAULT] Get the current week fitness, fatigue and form.')  # It's tricky, this is set in the function itself
@click.option('--last', '-l', is_flag=True, default=False,
              help='Get the last week fitness, fatigue and form.')
@click.option('--calendar_week', '-cw', type=int, nargs=2,
              help='Get the fitness, fatigue and form for the specified calendar week.\n '
                   'Need two arguments (week number, year) like: -cw 2 2021.')
@output_option()
@login_required
def get_form_week(output, current, last, calendar_week):
    # If no flag is set, we use --current.
    if filter_unique_week_flag(current, last, calendar_week) == 0:
        current = True

    timestamp = activities_ga_kwargs(current, last, calendar_week)
    first_day = datetime.datetime.fromtimestamp(timestamp['after']).date()
    last_day = datetime.datetime.fromtimestamp(timestamp['before']).date()

    day = first_day
    while day <= last_day:
        click.echo(f'{_DAY_TITLE[day.weekday()]}')
        get_form_with_formatted_date(output, day)
        click.echo()
        day = day + datetime.timedelta(days=1)
