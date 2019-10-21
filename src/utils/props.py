from pyhocon import ConfigFactory
import os

def read_properties(basedir="./"):
    # conf = ConfigFactory.parse_file(basedir+'bot.properties')
    def_conf = ConfigFactory.parse_file(basedir+'bot.properties')

    for prop in def_conf:
        env = os.getenv(prop)
        def_conf[prop] = env if env is not None else def_conf[prop]
    return def_conf


