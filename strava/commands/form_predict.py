from dateparser import parse
import click

from strava.decorators import output_option, login_required

from strava.utils.form import get_form_with_formatted_date


@click.command(name='predict',
               help='Predicts the fitness, fatigue and form for a given day.'
                    'Planed TSS can be provided as args following: %Y-%m-%d tss, i.e. 2021-03-02 150.'
                    'Usage example: strava predict 2021-03-02 150 2021-03-03 200 -d tomorrow')
@click.argument('args', nargs=-1)
@click.option('--date', '-d', type=str, default='today',
              help="The date for which fitness, fatigue and form should be computed. By default is today.")
@click.option('--txt_path', '-txt', type=str,
              help='Full path to a txt file containing planed TSS. Will override any arguments.'
                   'The format should follow (for each line): 2021-03-02 150')
@output_option()
@login_required
def predict_form(output, date, args, txt_path):
    if txt_path:
        tss_dict = {}
        with open(txt_path, 'r') as file:
            line = file.readline()
            while line:
                split_line = line.split(' ')
                tss_entry = {split_line[0]: int(split_line[1])}
                tss_dict.update(tss_entry)
                line = file.readline()
    else:
        tss_dict = dict(zip(args[::2], args[1::2]))
        # Convert value types to int.
        for key in tss_dict:
            tss_dict[key] = int(tss_dict[key])

    formatted_date = parse(date).date()
    return get_form_with_formatted_date(output, formatted_date, tss_dict)
