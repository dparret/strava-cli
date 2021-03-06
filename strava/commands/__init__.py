# List all commands available in the cli.
from .activities_default import get_all_activities
from .activities_weekly import get_weekly_activities, weekly_activities
from .activity_default import get_activity
from .activity_weekly import get_weekly_activity
from .activity_constrain import get_constrain_activity
from .activity_lap import get_lap_activity
from .upload import post_upload
from .config import set_config
from .login import login
from .logout import logout
from .profile import get_profile
from .stats import get_stats
from .calendar_week import get_cw
from .report import get_report
from .zones_heartrate import get_zones_heartrate
from .zones_power import get_zones_power
from .form_get import get_form
from .form_predict import predict_form
from .form_generate import predict_generate
from .form_weekly import get_form_week
from .matches import count_matches
