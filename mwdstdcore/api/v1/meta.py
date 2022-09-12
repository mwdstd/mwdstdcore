from importlib import metadata
from .core import api
from ..utils import json_call


self_package_name = 'mwdstdcore'

try:
    self_version = metadata.version(self_package_name)
    self_description = metadata.metadata(self_package_name)['Summary']
except metadata.PackageNotFoundError:
    import tomlkit
    with open('pyproject.toml') as pyproject:
        file_contents = pyproject.read()

    content = tomlkit.parse(file_contents)['tool']['poetry']
    self_version = f'{content["version"]}-dev'
    self_description = content['description']

@api.route('/ver', methods=['GET'])
@json_call
def api_ver():
    return {
        'name': self_package_name, 
        'version': self_version, 
        'buildDate': 0, 
        'description': self_description, 
        'homepage': 'https://github.com/mwdstd/mwdstdcore'
    }