from datetime import datetime, timedelta
from collections import OrderedDict

def gen_date(start, end):
    date_generated = [start + timedelta(days=x) for x in range(0, (end-start).days)]
    return date_generated


def parse_date(delimiter, base_format):
    dates = []
    for i in delimiter:
        date = base_format.replace("-", i)
        dates.append(date)
    return dates


def date_gen_format(date, format):
    try:
        date = datetime.strftime(date, format)
        return date
    except ValueError:
        pass


def main():
    
    delimiter = ("", " ", "-", " - ", "/", " / ", ".", " . ")
    
    base_format = ["%d-%m-%y", "%d-%m-%Y", "%Y-%m-%d"]
    
    start = datetime(2022, 1, 1)
    end = datetime(2025, 12, 31)
    
    x = 1
    for date in gen_date(start, end):
        for i in base_format:
            with open(f"dicts/{x}.txt", "w") as f:
                for j in parse_date(delimiter, i):
                    f.write(date_gen_format(date, j) + "\n")
            x += 1

    month = list(OrderedDict(((start + timedelta(_)).strftime(r"%b%y"), None) for _ in range((end - start).days)).keys())
    for i in month:
        with open(f"dicts/{x}.txt", "a") as f:
            f.write(i + "\n")
        x += 1
        



if __name__ == '__main__':
    main()
