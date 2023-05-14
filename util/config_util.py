from cryptography.fernet import Fernet
import configparser

key = 'C-ldMemrQlPHAj7DNCiRUt3Z3rUPxPHNeUqrBIwWfJU='
fernet = Fernet(key)
config_path = './config.ini'

def read_config() -> configparser.ConfigParser:
    conf = configparser.ConfigParser()
    is_ok = conf.read(config_path)
    return conf

def encode(data : str) -> str:
    encode = fernet.encrypt(data.encode()).decode()
    return encode
def decode(encode : str) -> str:
    decode = fernet.decrypt(encode).decode()
    return decode

def set_value(section : str, key : str, value : str):
    conf = read_config()
    if not conf.has_section(section):
        conf.add_section(section)
    conf[section][key] = encode(value)
    with open(config_path, 'w') as f:
        conf.write(f)

def get_value(section : str, key : str) -> str | None:
    conf = read_config()
    if conf.has_section(section):
        if conf.has_option(section, key):
            value = conf.get(section, key)
            return decode(value)
    return None

if __name__ == '__main__':
    pass