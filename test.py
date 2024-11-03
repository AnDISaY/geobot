# from datetime import datetime, timezone, timedelta, time
import datetime
import pytz


then = datetime.time(10)
now = datetime.datetime.now(pytz.timezone('Asia/Bishkek')).time()

print(then)
print(now)
print(then > now)