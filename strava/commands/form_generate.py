import datetime
import os

from dateparser import parse
import click


@click.command(name='generate',
               help='Generate a templates for: strava form predict.')
@click.option('--from_date', '-from', type=str, default='today',
              help="The first date in the txt file generated.")
@click.option('--to_date', '-to', type=str, required=True,
              help="The last date in the txt file generated.")
@click.option('--default_tss', '-tss', type=int, default=0,
              help='The default TSS value to be used with all generated entries.')
@click.option('--txt_path', '-txt', type=str,
              help='Full path to a txt file containing planed TSS. Will override any arguments.'
                   'The format should follow (for each line): 2021-03-02 150')
def predict_generate(from_date, to_date, default_tss, txt_path):
    # Check the file doesn't exist.
    if os.path.exists(txt_path):
        click.confirm('A file already exists, do you want to overwrite it?', abort=True)
        os.remove(txt_path)

    # Format the dates.
    formatted_from = parse(from_date).date()
    formatted_to = parse(to_date).date()

    with open(txt_path, 'a') as file:
        line_time = formatted_from
        while line_time and line_time <= formatted_to:
            tss_line = f"{line_time.strftime('%Y-%m-%d')} {default_tss} \n"
            file.write(f'{tss_line}')
            line_time = line_time + datetime.timedelta(days=1)
