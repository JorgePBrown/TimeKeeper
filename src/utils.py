def sum_time(time):
    ret = ""
    # secs
    #secs = time % 60
    remainder = time // 60
    #ret = f"{int(secs)} seconds" + ret
    if remainder == 0:
        return ret
    # mins
    mins = remainder % 60
    remainder = remainder // 60
    ret = f"{int(mins)} minutes" + ret
    if remainder == 0:
        return ret
    # hours
    hours = remainder % 24
    remainder = remainder // 24
    ret = f"{int(hours)} hours, " + ret
    if remainder == 0:
        return ret
    # days
    days = remainder
    ret = f"{int(days)} days, " + ret

    return ret