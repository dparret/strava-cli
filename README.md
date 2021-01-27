# Strava command-line interface

This repo is a fork of [strava-cli](https://github.com/bwilczynski/strava-cli). 
All kudos to [bwilczynski](https://github.com/bwilczynski) for the great work.

## Installation

To install it do `make install` from the root of the repo. 

## Usage

```sh
Usage: strava [OPTIONS] COMMAND [ARGS]...
```

### Get Started

[Create application](https://www.strava.com/settings/api) and run `strava config` to provide 
your application's Client ID and Client Secret.

Alternatively set the following environment variables before running `strava`:

```sh
export STRAVA_CLIENT_ID={YOUR_CLIENT_ID}
export STRAVA_CLIENT_SECRET={YOUR_CLIENT_SECRET}
```

Login to your Strava service (opens a web browser sending user to Strava login service):

```sh
strava login
```

For usage and help content, pass in the `--help` parameter, for example:

```sh
strava --help
```

### Available commands

Get recent, yearly, total stats:

```console
➜ strava stats  

Type           Count  Distance     Moving time    Elevation gain
-----------  -------  -----------  -------------  ----------------
run recent         0               00:00
run ytd            0               00:00
run all          196  2165.29 km   193h 41m       57982 m
ride recent       15  465.23 km    19h 1m         1520 m
ride ytd          11  317.48 km    13h 14m        1436 m
ride all         381  13675.15 km  551h 14m       204692 m
swim recent        0               00:00
swim ytd           0               00:00
swim all           1  2.05 km      43:40

```

List your recent activities:

```console
➜ strava activities list -pp 5

        Id  Start date                 Type         Name                                     Moving time    Distance
----------  -------------------------  -----------  ---------------------------------------  -------------  ----------
4667970175  2021-01-23 14:33:58+01:00  VirtualRide  Watopia                                  1h 13m         40.02 km
4663583443  2021-01-22 18:39:40+01:00  Workout      Core and legs                            54:58
4658375016  2021-01-21 18:48:11+01:00  VirtualRide  Richmond - Easy spin                     38:35          19.13 km
4650565494  2021-01-20 08:26:48+01:00  Ride         Kind of easy ride                        1h 30m         31.08 km
4647855447  2021-01-19 18:11:31+01:00  Ride         Oops zwift connection was crazy tonight  1h 2m          23.16 km
```

List your weekly activities or the activities for a specific week:
```console
➜ strava activities week --current

        Id  Start date                 Type         Name                                     Moving time    Distance
----------  -------------------------  -----------  ---------------------------------------  -------------  ----------
4642378106  2021-01-18 17:33:29+01:00  Workout      Core and leg routine                     1h 17m
4647855447  2021-01-19 18:11:31+01:00  Ride         Oops zwift connection was crazy tonight  1h 2m          23.16 km
4650565494  2021-01-20 08:26:48+01:00  Ride         Kind of easy ride                        1h 30m         31.08 km
4658375016  2021-01-21 18:48:11+01:00  VirtualRide  Richmond - Easy spin                     38:35          19.13 km
4663583443  2021-01-22 18:39:40+01:00  Workout      Core and legs                            54:58
4667970175  2021-01-23 14:33:58+01:00  VirtualRide  Watopia                                  1h 13m         40.02 km
```

You can get more information about specific activities by doing:
```console 
➜ strava activity list 4667970175

Name:                  Watopia
                       20' warm up P Z1
                       5x 7/3min P Z2/Z4
                       5' P Z1
Id:                    4667970175 (https://www.strava.com/activities/4667970175)
---                    ---
Gear:                  Canyon (9773.83 km)
Start date:            2021-01-23 14:33:58+01:00
Moving time:           1h 13m
Distance:              40.02 km
Average heartrate:     147 bpm
Total elevation gain:  328 m
---                    ---
```

And additional details:
```console 
➜ strava activity list 4667970175 --details

Name:                  Watopia
                       20' warm up P Z1
                       5x 7/3min P Z2/Z4
                       5' P Z1
Id:                    4667970175 (https://www.strava.com/activities/4667970175)
---                    ---
Gear:                  Canyon (9773.83 km)
Start date:            2021-01-23 14:33:58+01:00
Moving time:           1h 13m
Distance:              40.02 km
Average heartrate:     147 bpm
Total elevation gain:  328 m
---                    ---
Tss:                   53
Average power:         197 W
Normalized power:      218 W
Intensity factor:      0.66
Variability index:     1.11
Efficiency factor:     1.28
Average cadence:       91 rpm
Ftp:                   330 W
---                    ---
```

Listing all that information for a specific week is possible as well:
```console
➜ strava activity week --week_number 1 2021
Name:                  First of the season
                       Very nice valley
Id:                    4565601437 (https://www.strava.com/activities/4565601437)
---                    ---
Gear:                  N/A
Start date:            2021-01-04 12:47:18+01:00
Moving time:           1h 3m
Distance:              15.83 km
Average heartrate:     145 bpm
Total elevation gain:  142 m
---                    ---

Name:                  From the bottom to top!
                       Amazing day. Should have bring more food.
Id:                    4586844829 (https://www.strava.com/activities/4586844829)
---                    ---
Gear:                  N/A
Start date:            2021-01-08 12:20:13+01:00
Moving time:           2h 34m
Distance:              41.14 km
Average heartrate:     129 bpm
Total elevation gain:  379 m
---                    ---
```

Basic totals can be done from list of detailed activities
```console
➜ strava activity week --week_number 1 2021 -t

Name:                  First of the season
                       Very nice valley
Id:                    4565601437 (https://www.strava.com/activities/4565601437)
---                    ---
Gear:                  N/A
Start date:            2021-01-04 12:47:18+01:00
Moving time:           1h 3m
Distance:              15.83 km
Average heartrate:     145 bpm
Total elevation gain:  142 m
---                    ---

...

Name:                  From the bottom to top!
                       Amazing day. Should have bring more food.
Id:                    4586844829 (https://www.strava.com/activities/4586844829)
---                    ---
Gear:                  N/A
Start date:            2021-01-08 12:20:13+01:00
Moving time:           2h 34m
Distance:              41.14 km
Average heartrate:     129 bpm
Total elevation gain:  379 m
---                    ---

Total
Number of activities:  4
Total time:            6h 19m
Total tss:             0
---                    ---
```

For further analysis, you can constrain the computation to specific part of your activity:
```console
➜ strava activity constrain 4667970175 --from 0 10 0 --to 0 50 0

Name:                  Watopia
                       20' warm up P Z1
                       5x 7/3min P Z2/Z4
                       5' P Z1
Id:                    4667970175 (https://www.strava.com/activities/4667970175)
---                    ---
Gear:                  Canyon (9773.83 km)
Start date:            2021-01-23 14:33:58+01:00
Moving time:           1h 13m
Distance:              40.02 km
Average heartrate:     147 bpm
Total elevation gain:  328 m
---                    ---
Tss:                   30
Average power:         208 W
Normalized power:      223 W
Intensity factor:      0.68
Variability index:     1.07
Efficiency factor:     1.3
Average cadence:       92 rpm
Ftp:                   330 W
---                    ---
```
