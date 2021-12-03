import re
from datetime import datetime
import numpy as np

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

def table(headers, values):
    lengths = {header: len(header) for header in headers}
    for value in values:
        for header in headers:
            if len(value[header]) > lengths[header]:
                lengths[header] = len(value[header])

    # headers
    break_line = "".join("".join(["|-" + "-" * lengths[header] + "-|"]) for header in headers)
    print(break_line)
    headers_line = ""
    for header in headers:
        half = (lengths[header] - len(header)) // 2
        extra = (lengths[header] - len(header)) % 2
        headers_line += "| " + " " * (half + extra) + header + " " * half + " |"
    print(headers_line)
    print(break_line)

    for val in values:
        row = ""
        for header in headers:
            v = val[header]
            half = (lengths[header] - len(v)) // 2
            extra = (lengths[header] - len(v)) % 2
            row += "| " + " " * (half + extra) + v + " " * half + " |"
        print(row)
    # end
    print(break_line)

def parse_timespan(span: str) -> int:
    times = re.findall("[0-9]+[a-zA-Z]", span)
    if len(times) <= 0:
        raise AssertionError("Incorrect formatting. Use <number><unit>, e.g. to say two days and five hours use 2d5h.")
    time_span = 0
    unit_conversion = {
        "s": 1,
        "m": 60,
        "h": 60 * 60,
        "d": 60 * 60 * 24,
        "w": 60 * 60 * 24 * 7,
        "M": 60 * 60 * 24 * 30,
        "y": 60 * 60 * 24 * 365
    }
    for time in times:
        value = int(time[0:-1])
        unit = time[-1]
        try:
            time_span += value * unit_conversion[unit]
        except KeyError as e:
            raise KeyError(f"Used time unit {unit}. Available time units are {list(unit_conversion.keys())}.") from e

    return time_span

def row_to_dict(cols, row):
    ret = {}
    for col in cols:
        if isinstance(row[col], float) and np.isnan(row[col]):
            v = "-"
        elif col == "start" or col == "end":
            v = date_format(row[col])
        elif col == "diff" or col == "total_time":
            v = sum_time(row[col])
        else:
            v = str(row[col])
        
        ret[col] = v

    return ret

def date_format(time: float) -> str:
    return datetime.fromtimestamp(time).strftime("%d-%m-%Y %H:%M")