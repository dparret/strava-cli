import click

from strava.commands import login, logout, get_profile, get_stats, set_config, post_upload, get_cw, get_report, \
    count_matches
from strava.cli.activity import commands as activity
from strava.cli.activities import commands as activities
from strava.cli.zones import commands as zones
from strava.cli.form import commands as predict_form


@click.group()
@click.version_option()
def cli():
    pass


cli.add_command(login)
cli.add_command(logout)
cli.add_command(get_profile)
cli.add_command(get_stats)
cli.add_command(set_config)
cli.add_command(post_upload)
cli.add_command(get_cw)
cli.add_command(get_report)
cli.add_command(count_matches)

cli.add_command(activity.cli_activity)
cli.add_command(activities.cli_activities)
cli.add_command(zones.cli_zones)
cli.add_command(predict_form.cli_predict_form)

if __name__ == '__main__':
    cli()
