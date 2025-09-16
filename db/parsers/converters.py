from db.models import Term


class Converter:

    def __init__(self, file_field_name: str, model_field_name: str):
        self.file_field_name = file_field_name
        self.model_field_name = model_field_name

    def convert(self, data):
        return data


class TermNameConverter(Converter):

    def __init__(self, file_field_name: str, model_field_name: str, dictionary_cache: list[Term]):
        super().__init__(file_field_name, model_field_name)
        self.dictionary_cache = dictionary_cache

    def convert(self, data):
        term = list(filter(lambda t: t.name == data, self.dictionary_cache))
        if term:
            return term[0].id

