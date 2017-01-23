import re
import json
from calendar import month_name


class Persian:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = self.load_data()
        self.regex = re.compile(r'\s*(\d+)\s(\w+)\s([^\[]*)\s*(:?\[(\d+)\s([\w\s]+)\])?\s*', flags=re.U)

    def load_data(self):
        with open(self.file_name, encoding='utf8') as f:
            return f.readlines()

    def extractor(self):
        for line in self.data:
            match = self.regex.match(line)
            try:
                d1, m1, desc, d2, m2, _ = match.groups()
            except ValueError:
                d1, m1, desc = match.groups()
                yield d1, m1, desc, None
            except AttributeError:
                pass
            else:
                yield d1, m1, desc, (d2, m2)

    def parser(self):
        eng_months = list(month_name)
        events = []
        for d1, m1, desc, (d2, m2) in self.extractor():
            dictionary = {}
            dictionary['persian_date'] = d1, m1
            if d2:
                if m2.capitalize() in eng_months:
                    dictionary['english_date'] = d2, m2.capitalize()
                else:
                    dictionary['arabic_date'] = (d2, m2)
            dictionary['description'] = desc
            dictionary['key_words'] = desc.split()
            events.append(dictionary)
        return events

    def build_wordnet(self):
        data = self.parser()
        with open("persian.json", 'w') as f:
            json.dump(data, f, indent=4)


p = Persian('raw_data/persian-events.txt')
p.build_wordnet()
