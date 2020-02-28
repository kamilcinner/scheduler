from django.utils import timezone

from bs4 import BeautifulSoup
from urllib import request


class Subject:
    def __init__(self, name=None, lecturer=None, class_=None, time_start=None, time_end=None):
        self.name = name
        self.lecturer = lecturer
        self.class_ = class_
        self.time_start = time_start
        self.time_end = time_end


def get_pollub_subjects_list():
    url = 'http://we1.pollub.pl/ats4/plan.php?type=0&id=6200&winW=943&winH=852&loadBG=000000'
    req = request.urlopen(url).read().decode('UTF-8')
    soup = BeautifulSoup(req, 'html.parser')
    result = soup.find_all('div', class_='coursediv')
    r2 = BeautifulSoup(str(result), 'html.parser')

    tab = []
    subjects = []
    for r in r2.contents:
        soup = BeautifulSoup(str(r), 'html.parser')
        if soup.text != ', ':
            tab.append(soup.contents)
            for i in soup.contents:
                strings = BeautifulSoup(str(i), 'html.parser').strings
                my_strings = []
                for s in strings:
                    if s != '\n' and s != '[' and s != ']':
                        my_strings.append(str(s))
                if len(my_strings) > 3:
                    subject = Subject()
                    subject.name = str(my_strings[0])
                    if subject.name.find(', lekt') != -1:
                        subject.lecturer = 'Enter Your lecturer name'
                        subject.class_ = 'Enter Your classroom name'
                    else:
                        subject.lecturer = str(my_strings[1])
                        subject.class_ = str(my_strings[2])

                    time = my_strings[len(my_strings) - 1]
                    subject.time_start = str(time[:5])
                    subject.time_end = str(time[8:13])

                    subjects.append(subject)

    return subjects


WEEK_DAYS = (
    ('Monday',       0),
    ('Tuesday',      1),
    ('Wednesday',    2),
    ('Thursday',     3),
    ('Friday',       4),
    ('Saturday',     5),
    ('Sunday',       6)
)


class WeekDay:
    def __init__(self, date, activities):
        self.date = date
        self.activities = activities

    @property
    def get_week_day_name(self):
        return self.date.strftime('%A')


def get_default_time(hours_shift=0):
    t = timezone.now()
    t += timezone.timedelta(hours=hours_shift, minutes=-t.minute, seconds=-t.second, microseconds=-t.microsecond)
    return t.astimezone(timezone.get_default_timezone()).time()
