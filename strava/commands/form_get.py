from dateparser import parse
import click

from strava.decorators import output_option, login_required

from strava.utils.form import get_form_with_formatted_date


@click.command(name='get',
               help='Provides the fitness, fatigue and form for a given day.'
               )
@click.option('--date', '-d', type=str, default='today',
              help="The date for which fitness, fatigue and form should be computed. By default is today.")
@output_option()
@login_required
def get_form(output, date):
    formatted_date = parse(date).date()
    return get_form_with_formatted_date(output, formatted_date)
