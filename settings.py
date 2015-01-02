import datetime

NEXTBUS_ROUTES = ('90', '92', '93')
NEXTBUS_URLS = ('http://www.nextbus.com/api/pub/v1/agencies/wmata/routes/90/stops/6579/predictions?coincident=true&direction=90_90_0&destination=6627',)

def not_asleep():
    now = datetime.datetime.now()

    sleep_hours = (0, 1, 2, 3, 4, 5, 6, 7)
    if now.weekday() in (0, 6):
        sleep_hours = (2, 3, 4, 5, 6, 7, 8)

    return not (now.hour in sleep_hours)


NEXTBUS_HOURS = {
	'90': not_asleep,
	'92': not_asleep,
    '93': not_asleep
}

TIMEOUT = 300 
