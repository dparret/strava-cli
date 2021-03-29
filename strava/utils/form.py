import datetime
import itertools
import math
import shelve

import pandas as pd

from strava import api
from strava.decorators import OutputType, format_result, TableFormat
from strava.formatters import noop_formatter, format_property, apply_formatters
from strava.utils.activity_common import add_metrics_to_activity

from strava.config.local_store import _get_fullpath


_FORM_COLUMNS = ('key', 'value')


def get_form_with_formatted_date(output, date, planed=None):
    CTL, ATL, TSB = compute_fitness_fatigue_form(date, planed)
    result = {
        'Fitness (CTL)': CTL,
        'Fatigue (ATL)': ATL,
        'Form (TSB)': TSB,
    }
    return result if output == OutputType.JSON.value else _format_result(result)


def compute_fitness_fatigue_form(date=datetime.datetime.today().date(), planed=None):
    # Define the window.
    end = datetime.datetime(date.year, date.month, date.day) + datetime.timedelta(days=1)
    start = end - datetime.timedelta(days=42)
    act_in_window = api.get_activities(per_page=100, before=end.timestamp(), after=start.timestamp())
    ids_in_window = [a.get('id') for a in act_in_window]

    # Compute and store daily TSS values.
    cache = shelve.open(_get_fullpath('cache'))
    tss_list = []
    for act_id in ids_in_window:
        id_str = str(act_id)
        if id_str in cache:
            tss_entry = cache[id_str]
            tss_list.append(tss_entry)
        else:
            tss_entry = get_tss_entry(act_id)
            cache[id_str] = tss_entry
            tss_list.append(tss_entry)
    cache.close()
    daily_tss = compute_daily_tss(tss_list)

    # Add planed TSS to daily values.
    if planed:
        daily_tss.update(planed)

    # Compute values.
    delta = end - start
    tss_table = pd.DataFrame(columns=('date', 'tss'))
    for i in range(delta.days + 1):
        day = start + datetime.timedelta(days=i)
        st_day = day.strftime('%Y-%m-%d')
        if st_day in daily_tss.keys():
            tss_entry = daily_tss[st_day]
        else:
            tss_entry = 0
        tss_table = tss_table.append({'date': st_day, 'tss': tss_entry}, ignore_index=True)

    CTL = compute_CTL(tss_table[(len(tss_table) - 42):(len(tss_table) - 1)])
    ATL = compute_ATL(tss_table[(len(tss_table) - 7):(len(tss_table) - 1)])
    TSB = CTL - ATL

    return CTL, ATL, TSB


@format_result(table_columns=_FORM_COLUMNS, show_table_headers=False, table_format=TableFormat.PLAIN)
def _format_result(result, output=None):
    formatters = {
        'Fitness (CTL)': noop_formatter,
        'Fatigue (ATL)': noop_formatter,
        'Form (TSB)': noop_formatter,
    }
    return result if output == OutputType.JSON.value else _as_table(result, formatters)


def _as_table(result, formatters):
    return [{'key': format_property(k), 'value': v} for k, v in apply_formatters(result, formatters).items()]


def compute_CTL(tss_table):
    #TODO is ewm capable of doing the same?
    CTL_yesterday = 0
    for index, row in tss_table.iterrows():
        alpha = math.exp(-1/42)
        CTL = row['tss'] * (1-alpha) + CTL_yesterday * alpha
        CTL_yesterday = CTL

    return round(CTL)


def compute_ATL(tss_table):
    #TODO is ewm capable of doing the same?
    ATL_yesterday = 0
    for index, row in tss_table.iterrows():
        alpha = math.exp(-1/7)
        ATL = row['tss'] * (1-alpha) + ATL_yesterday * alpha
        ATL_yesterday = ATL

    return round(ATL)


def get_tss_entry(act_id):
    activity = api.get_activity(act_id)
    tss_entry = add_metrics_to_activity(activity)[0].get('tss')
    date = activity.get('start_date')[0:10]
    return {date: tss_entry}


def compute_daily_tss(tss_entries):
    grouped_entries = [list(g) for _, g in itertools.groupby(tss_entries, lambda x: x.keys())]
    daily_tss = [{[k for k, v in g[0].items()][0]: sum([(v) for g1 in g for k, v in g1.items() if v is not None])} for g in grouped_entries]

    dict_tss = {}
    for dt in daily_tss:
        dict_tss.update(dt)

    return dict_tss


def write_cache(key, value):
    cache = shelve.open(_get_fullpath('cache'))
    cache[key] = value
    cache.close()


def read_cache(key):
    cache = shelve.open(_get_fullpath('cache'))
    if key in cache:
        value = cache[key]
    cache.close()
    return value


def list_cache():
    cache = shelve.open(_get_fullpath('cache'))
    keys = list(cache.keys())
    cache.close()
    return keys


def delete_cache(key):
    cache = shelve.open(_get_fullpath('cache'))
    try:
        del cache[key]
    except KeyError:
        pass
    cache.close()


def clean_cache():
    cache = shelve.open(_get_fullpath('cache'))
    keys = list(cache.keys())
    for key in keys:
        del cache[key]
    cache.close()
