#!/usr/bin/env python

import os
import yaml
import json

from web3 import Web3, HTTPProvider
from web3.middleware import geth_poa_middleware

import argparse

import logging
from rich.logging import RichHandler
from rich import print
from rich.traceback import install
from rich.panel import Panel
from rich.pretty import pprint

from attributedict.collections import AttributeDict

install(show_locals=False)

def init_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog = 'claim_rewards.py',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        usage="%(prog)s [OPTION] ...",
        description="Flare Validator Rewards - Check and Claim",
        epilog = """

Written by Dustin Lee [FTSO Express]

If you like it, send some VP My Way

FLR: 0xc0452CEcee694Ab416d19E95a0907f022DEC5664
SGB: 0x33ddae234e403789954cd792e1febdbe2466adc2
---
""",
        # add_help=True
    )

    parser.add_argument(
        "-v", "--version", action="version",
        version = f"{parser.prog} version 1.0.0"
    )

    parser.add_argument(
        "-c", "--claim", action='store_true',
        help='If you want to claim an amount'
    )

    parser.add_argument(
        "-r", "--rewards", action='store',
        help='Amount of Rewards you want to claim'
    )

    # parser.add_argument(
    #     "-h", "--help", action='help',
    #     help='Amount of Rewards you want to claim'
    # )

    return parser

# Global setting
logging.basicConfig(
    level="INFO",
    # level="NOTSET",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
)

log = logging.getLogger("rich")

with open("config.yml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

# Pull In Config
FTSO_NODE_C_CHAIN_URL = f"{cfg['nodes']['flare']['node']['url']}{cfg['nodes']['flare']['node']['c_chain']}"
log.debug(f"FTSO C Chain: {FTSO_NODE_C_CHAIN_URL}")
VALIDATOR_PRIVATE_KEY = os.getenv('VALIDATOR_PRIVATE_KEY', cfg['validator']['private_key'])
log.debug(f"VALIDATOR PRIVATE KEY LOADED")
CONTRACT_VALIDATOR_REWARD_MANAGER_ADDRESS = cfg['contracts']['validator_reward_manager']['address']
log.debug(f"Validator Address: {CONTRACT_VALIDATOR_REWARD_MANAGER_ADDRESS}")
CONTRACT_VALIDATOR_REWARD_MANAGER_ABI = cfg['contracts']['validator_reward_manager']['abi']
# log.debug(f"Validator ABI: {CONTRACT_VALIDATOR_REWARD_MANAGER_ABI}")
GAS_LIMIT = cfg['blockchain']['flare']['gas_limit']
log.debug(f"GAS_LIMIT: {GAS_LIMIT}")
GAS_PRICE = cfg['blockchain']['flare']['gas_price']
log.debug(f"GAS_PRICE: {GAS_PRICE}")
REWARD_TO_CLAIM = cfg['rewards']['claim']['_rewardAmount']
# log.debug(f"REWARD_TO_CLAIM: {REWARD_TO_CLAIM}")
log.debug(f"REWARD_TO_CLAIM: {REWARD_TO_CLAIM} FLR")


def check_rewards_available(web3: Web3, _validator_account, _contract_validator_reward_manager):
    
    contract_validator_reward_manager_balance = web3.fromWei(web3.eth.get_balance(CONTRACT_VALIDATOR_REWARD_MANAGER_ADDRESS),'ether')
    log.debug(f"Validator Reward Manager Balance: {contract_validator_reward_manager_balance}")
    try:
        _totalReward_wei, _claimedReward_wei = _contract_validator_reward_manager.functions.getStateOfRewards(_validator_account.address).call()
        _totalReward = web3.fromWei(_totalReward_wei ,'ether')
        _claimedReward = web3.fromWei(_claimedReward_wei ,'ether')
    except Exception as e:
        log.exception(f"Help: {e}")
    log.info(f"Validator Rewards Total   [FLARE] : {_totalReward}")
    log.info(f"Validator Rewards Claimed [FLARE] : {_claimedReward}")
    return _totalReward_wei - _claimedReward_wei


# function claim(address _rewardOwner, address payable _recipient, uint256 _rewardAmount, bool _wrap) external;
def claim_reward( web3: Web3, _validator_account, _contract_validator_reward_manager,
    _rewardOwner = cfg['rewards']['claim']['_rewardOwner'],
    _recipient = cfg['rewards']['claim']['_recipient'],
    _rewardAmount = cfg['rewards']['claim']['_rewardAmount'], 
    _wrap = cfg['rewards']['claim']['_wrap']):
    
    try:
        nonce = web3.eth.getTransactionCount(_validator_account.address)
        log.debug(f"NONCE: {nonce}")
    except Exception as error:
        log.exception(f"Claim [GET_NONCE] : {error}")

    try:        
        _submission_txn = _contract_validator_reward_manager.functions.claim(
                _rewardOwner, _recipient, _rewardAmount, _wrap
            ).buildTransaction(
                {'nonce': nonce, 'gas': GAS_LIMIT,'gasPrice': web3.toWei(GAS_PRICE, 'gwei')}
            )
        log.debug(f"submission_txn: {_submission_txn}")
    except Exception as error:
        log.exception(f"Claim [SUBMISSION_TXN] : {error}")
    
    try:
        _signed_txn = web3.eth.account.signTransaction(_submission_txn, VALIDATOR_PRIVATE_KEY)
        log.debug(f"signed_txn",{_signed_txn})
    except Exception as error:
        log.exception(f"Claim [SIGNED_TXN] : {error}")


    try:
        _txn_id = web3.toHex(web3.eth.sendRawTransaction(_signed_txn.rawTransaction))
        log.debug(f"TX ID: {_txn_id}")
    except Exception as error:
        log.exception(f"Claim [SEND TX] : {error}")

    try:
        # Wait for Receipt
        _txn_receipt = web3.eth.waitForTransactionReceipt(_txn_id,timeout=240)
        log.debug(f"TX RCPT: {_txn_receipt}")
    except Exception as error:
        log.exception(f"Claim [TX RECEIPT] : {error}")
    
    return (_txn_id, _txn_receipt)


def main() -> None:

    parser = init_argparse()
    args = parser.parse_args()

    print(Panel.fit("[bold yellow]FTSO Express - Validator Reward Checker/Claimer", border_style="red"))

    if "FTSO_URL" in os.environ:
        web3 = Web3(HTTPProvider(os.getenv('FTSO_URL', FTSO_NODE_C_CHAIN_URL)))
        log.debug(f"FTSO_URL: {FTSO_NODE_C_CHAIN_URL}")
    else:
        web3 = Web3(HTTPProvider(FTSO_NODE_C_CHAIN_URL))
        log.debug(f"FTSO_URL: {FTSO_NODE_C_CHAIN_URL}")
        
    log.debug(f"FTSO_URL: {FTSO_NODE_C_CHAIN_URL}")

    # Avalanche Networks Require This
    web3.middleware_onion.inject(geth_poa_middleware, layer=0)

    if web3.isConnected():
        # Setup Account to be Used
        validator_account = web3.eth.account.privateKeyToAccount(VALIDATOR_PRIVATE_KEY)
        # Configure the default account to use
        web3.eth.default_account = validator_account.address
    else:
        log.warning(f"Not Connected to FLARE NODE [ {FTSO_NODE_C_CHAIN_URL} ]")

    contract_validator_reward_manager = web3.eth.contract(
        address=CONTRACT_VALIDATOR_REWARD_MANAGER_ADDRESS, 
        abi=CONTRACT_VALIDATOR_REWARD_MANAGER_ABI
    )

    _rewards_available_wei = check_rewards_available(web3, validator_account, contract_validator_reward_manager)
    _rewards_available = web3.fromWei(_rewards_available_wei,'ether')
    log.info(f"Rewards Claimable [{_rewards_available_wei}] WEI      : {_rewards_available:.18f} FLR")

    if args.claim:
        if args.rewards:
            _arg_rewards = float(args.rewards)
            _arg_rewards_wei = web3.toWei(_arg_rewards,'ether')
            # log.debug(f"Rewards Amount    : {args.rewards} FLR Requested ")
            # log.debug(f"Rewards to Claim  [{_arg_rewards_wei}] WEI : {_arg_rewards:.18f} FLR Requested ")
            # log.debug(f"Rewards Claimable [{_rewards_available_wei}] WEI : {_rewards_available:.18f} FLR Requested ")

            if (_rewards_available_wei - _arg_rewards_wei) > 0:
                log.info(f"Claiming Rewards   [{_arg_rewards_wei}] WEI      : {_arg_rewards:.18f} FLR")
                # Mock
                # _txn_id, _txn_receipt  = ("Wassup",AttributeDict({'status': 0}))
                # The Real Deal
                _txn_id, _txn_receipt  = claim_reward(web3, validator_account, contract_validator_reward_manager, _rewardAmount=_arg_rewards_wei)
                log.debug(f"TXN Receipt: {_txn_receipt.status}: {type(_txn_receipt.status)}")
                if not _txn_receipt.status == 1:
                    log.exception(f"Rewards Not Claimed -- Please Investigate -- TXN ID [{_txn_id}]")
            else:
                log.warning(f"Not Enough Rewards: {_rewards_available_wei}")


        _rewards_available = check_rewards_available(web3, validator_account, contract_validator_reward_manager)
        # log.info(f"Amount of Rewards Available: {_rewards_available} [{web3.fromWei(_rewards_available,'ether')}] FLR")

if __name__ == "__main__":
    # log.setLevel("DEBUG")
    main()