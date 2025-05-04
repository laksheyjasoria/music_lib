import isodate

def iso8601_to_seconds(duration):
    return int(isodate.parse_duration(duration).total_seconds())
