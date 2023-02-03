class ParseDictToObject:
    def __init__(self, **dictionary) -> None:
        self.content = dictionary
        self.dict_to_object(dictionary)

    def get_dict(self):
        for key, values in self.content.items():
            if isinstance(values, ParseDictToObject):
                self.content[key] = values.get_dict()
            elif isinstance(values, list):
                for index in range(len(values)):
                    if isinstance(values[index], ParseDictToObject):
                        self.content[key][index] = values[index].get_dict()
        return self.content

    def serialize(self) -> dict:
        return self.get_dict()

    def dict_to_object(self, dictionary):
        for key, values in dictionary.items():
            if isinstance(values, dict):
                dictionary[key] = ParseDictToObject(**values.copy())
            elif isinstance(values, list):
                for index in range(len(values)):
                    if isinstance(values[index], dict):
                        val_dict = values[index].copy()
                        dictionary[key][index] = ParseDictToObject(**val_dict)
        self.__dict__.update(dictionary)
