class DBAbstract:
    def get_key_value_format(self):
        """
        Returns those attributes' list, values and str_format for which value is not none and attribute's name does not
        start with '_'. '_' indicates that the attribute is not a table's column.
        :return: str, list, str
        """
        str_keys = ''
        values = list()
        str_format = ''
        for attr, value in self.__dict__.items():
            if value is not None and not attr.startswith('_'):
                if str_keys:
                    str_keys += ', '
                    str_format += ', '

                str_keys += attr
                values.append(value)
                str_format += '%s'

        return str_keys, values, str_format
