import datetime
import time

def UTC(n, y, r):
    return time.mktime(datetime.datetime.strptime('{}-{}-{}'.format(n,y,r), "%Y-%m-%d").timetuple())