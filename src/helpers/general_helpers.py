from datetime import date, datetime


def list_days_to_birthday(check_date):
    today = date.today()
    bdat = datetime.strptime(check_date, '%d-%m-%Y')
    birthday = datetime(year=today.year, month=bdat.month, day=bdat.day)
    curdat = datetime(year=today.year, month=today.month, day=today.day)
    count = (curdat - birthday).days
    count = count if count > 0 else abs(count)
    return count
