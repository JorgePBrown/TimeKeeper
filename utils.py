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