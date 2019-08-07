def format_time_diff(s, e):
    """ Foramt """
    total_seconds = (e-s).total_seconds()
    n, seconds = divmod(total_seconds, 60)
    hours, minutes = divmod(n, 60)
    return "{0:02d}:{1:02d}:{2:02d}".format(int(hours), int(minutes), int(seconds+0.5))
