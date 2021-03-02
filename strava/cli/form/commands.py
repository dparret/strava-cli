import click

from strava.commands import predict_form, predict_generate, get_form


@click.group(name='form', help='[GROUP] Predict fitness, fatigue and form with upcoming training.')
def cli_predict_form():
    pass


cli_predict_form.add_command(get_form)
cli_predict_form.add_command(predict_form)
cli_predict_form.add_command(predict_generate)
