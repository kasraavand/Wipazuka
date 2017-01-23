"""."""
import json
import csv


class PersianWipazuka:
    """Creat a WordNet from the corresponding json file."""

    def __init__(self, *args, **kwargs):
        """Initializer."""
        inp_file_name = kwargs['inp_file_name']
        self.wordnet_name = kwargs['wordnet_name']
        self.raw_data = self.read_input(inp_file_name)
        self.wordnet = self.load_wordnet()

    def read_input(self, file_name):
        with open(file_name) as f:
            return json.load(f)

    def load_wordnet(self):
        d = {}
        with open('general_wordnet/wn-data-fas.tab', encoding='utf8') as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader)
            for id_type, lemma, word in reader:
                id_, type_ = id_type.split('-')
                d[word] = {'id': id_, 'type': type_}
            return d

    def create_new_keywords(self):
        for d in self.raw_data:
            key_words = d['key_words']
            new_key_words = []
            for word in key_words:
                try:
                    type_ = d.get(word)['type']
                except TypeError:
                    new_key_words.append(word)
                else:
                    if type_ == 'n':
                        new_key_words.append(word)
            d['key_words'] = new_key_words
            yield d

    def create_wordnet(self):
        with open(self.wordnet_name, 'w') as f:
            json.dump(list(self.create_new_keywords()), f, indent=4)


PW = PersianWipazuka(inp_file_name='persian.json',
                     wordnet_name='date_wordnet.json')
PW.create_wordnet()
