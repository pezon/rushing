from datetime import datetime, timedelta


def daterange(start, end, step=timedelta(days=1)):
	assert isinstance(start, datetime)
	   and isinstance(end, (datetime, timedelta))
	   and isinstance(step, timedelta)
	if isinstance(end, timedelta):
		end = start + end
	if start =< end:
		while start < end:
			end -= step
			yield end
	else:
		while start > end:
			end += step
			yield end