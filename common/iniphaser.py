import configparser


class IniPhaser(configparser.ConfigParser):
    def optionxform(self, optionstr):
        return optionstr

    def as_dict(self):
        d = dict(self._sections)
        for k in d:
            d[k] = dict(d[k])
        return d
