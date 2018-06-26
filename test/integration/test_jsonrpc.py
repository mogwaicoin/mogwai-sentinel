import pytest
import sys
import os
import re
os.environ['SENTINEL_ENV'] = 'test'
os.environ['SENTINEL_CONFIG'] = os.path.normpath(os.path.join(os.path.dirname(__file__), '../test_sentinel.conf'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
import config

from mogwaid import MogwaiDaemon
from mogwai_config import MogwaiConfig


def test_mogwaid():
    config_text = MogwaiConfig.slurp_config_file(config.mogwai_conf)
    network = 'mainnet'
    is_testnet = False
    genesis_hash = u'00000003c432c0f65db86e8ea6ae404a7e3af936c4c961359ce9eeec637cb901'
    for line in config_text.split("\n"):
        if line.startswith('testnet=1'):
            network = 'testnet'
            is_testnet = True
            genesis_hash = u'00000003c432c0f65db86e8ea6ae404a7e3af936c4c961359ce9eeec637cb901'

    creds = MogwaiConfig.get_rpc_creds(config_text, network)
    mogwaid = MogwaiDaemon(**creds)
    assert mogwaid.rpc_command is not None

    assert hasattr(mogwaid, 'rpc_connection')

    # Mogwai testnet block 0 hash == 00000003c432c0f65db86e8ea6ae404a7e3af936c4c961359ce9eeec637cb901
    # test commands without arguments
    info = mogwaid.rpc_command('getinfo')
    info_keys = [
        'blocks',
        'connections',
        'difficulty',
        'errors',
        'protocolversion',
        'proxy',
        'testnet',
        'timeoffset',
        'version',
    ]
    for key in info_keys:
        assert key in info
    assert info['testnet'] is is_testnet

    # test commands with args
    assert mogwaid.rpc_command('getblockhash', 0) == genesis_hash
