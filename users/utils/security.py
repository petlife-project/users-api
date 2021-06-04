from os import path


def load_private_key():
    private_key_path = path.abspath(path.dirname(__file__) + '/../resources/private.pem')
    with open(private_key_path, 'rb') as pem_file:
        return pem_file.read()


def load_public_key():
    public_key_path = path.abspath(path.dirname(__file__) + '/../resources/public.pem')
    with open(public_key_path, 'rb') as pem_file:
        return pem_file.read()
