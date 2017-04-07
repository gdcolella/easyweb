import yaml
from os import path


_conf_dir = path.abspath(path.join(__file__, '..', 'conf'))


def get_config(name):
    expected_file = path.join(_conf_dir, name+'.yaml')
    if not path.exists(expected_file):
        raise Exception("No configuration file for {}".format(name))
    with open(expected_file, 'r') as confFile:
        return yaml.load(confFile)
