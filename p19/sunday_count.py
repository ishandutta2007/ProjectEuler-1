# sunday_count.py
# Count the months b/w 1901 and 2000 where day 1 falls on a Sunday

def no_days_in_feb (year):
    if (year % 4) != 0:
        return 28
    if (year % 100) != 0:
        return 29
    if (year % 400) != 0:
        return 28
    return 29

def fill_no_days_in_month (month_day_dict):
    for month in range(0, 8, 2):
        month_day_dict[month] = 31
    for month in range(7, 13, 2):
        month_day_dict[month] = 31

    # April, June, Sept, and November
    month_day_dict[3] = 30
    month_day_dict[5] = 30
    month_day_dict[8] = 30
    month_day_dict[10] = 30

NUM_MONTHS = 12
DAYS_IN_WEEK = 7
month_day_dict = {}
fill_no_days_in_month (month_day_dict)
start_day = 2  # 1/1/1901 was a Tuesday, 0 will correspond to Sunday
sunday_mo_count = 0
start_year = 1901
end_year = 2000

for year in range(start_year, end_year+1):
    month_day_dict[1] = no_days_in_feb (year)
    for month in range(NUM_MONTHS):
        if start_day == 0:
            sunday_mo_count += 1
        start_day = (start_day + month_day_dict[month]) % DAYS_IN_WEEK

print sunday_mo_count
