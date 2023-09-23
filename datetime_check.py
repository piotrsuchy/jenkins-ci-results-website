import datetime
import pytz

def print_time():
    local_tz = pytz.timezone('Europe/Warsaw')
    local_time = datetime.datetime.now(tz=local_tz)
    print(local_time)

print_time()
