import re
def time_to_mili(hhmmss):
    assert re.match(r"[0-9]?[0-9]:[0-5][0-9]:[0-5][0-9]", hhmmss)
    h, m, s = map(int, hhmmss.split(":"))
    mili = h*3.6*10**6
    mili += m*6*10**4
    mili += s*1000
    return round(mili)