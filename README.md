# README

## Check for Rewards if Your Running a Validator

### Configure
```
[devops@flare src]$ cp config.yml.example config.yml

```

Edit the `config.yml` file

* Use a Flare Node available to you.
* Who to send the Rewards To
* A default amount 
* And if you want wrap or not ?


### Help

```
[devops@flare src]$ ./claim_rewards.py -h
usage: claim_rewards.py [OPTION] ...

Flare Validator Rewards - Check and Claim

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c, --claim           If you want to claim an amount
  -r REWARDS, --rewards REWARDS
                        Amount of Rewards you want to claim

Written by Dustin Lee [FTSO Express]

If you like it, send some VP My Way

FLR: 0xc0452CEcee694Ab416d19E95a0907f022DEC5664
SGB: 0x33ddae234e403789954cd792e1febdbe2466adc2
---
[devops@flare src]$ 
```

### Check Rewards

```
[devops@flare src]$ ./claim_rewards.py 
╭─────────────────────────────────────────────────╮
│ FTSO Express - Validator Reward Checker/Claimer │
╰─────────────────────────────────────────────────╯
[17:41:35] INFO     Validator Rewards Total   [FLARE] : 549.272402559692378579                                                                                                                                        claim_rewards.py:106
           INFO     Validator Rewards Claimed [FLARE] : 549.272402559692371904                                                                                                                                         claim_rewards.py:107
           INFO     Rewards Claimable [6675] WEI      : 0.000000000000006675 FLR                                                                                                                                       claim_rewards.py:191
[devops@flare src]$ 

```

### Claim Rewards - Default (as setup in config.yml)

```
[devops@flare src]$ ./claim_rewards.py --claim
╭─────────────────────────────────────────────────╮
│ FTSO Express - Validator Reward Checker/Claimer │
╰─────────────────────────────────────────────────╯
[17:50:15] INFO     Validator Rewards Total   [FLARE] : 549.272402559692378579                                                                                                                                         claim_rewards.py:106
           INFO     Validator Rewards Claimed [FLARE] : 549.272402559692372004                                                                                                                                         claim_rewards.py:107
           INFO     Rewards Claimable [6575] WEI      : 0.000000000000006575 FLR                                                                                                                                       claim_rewards.py:191
[17:50:16] INFO     Validator Rewards Total   [FLARE] : 549.272402559692378579                                                                                                                                         claim_rewards.py:106
           INFO     Validator Rewards Claimed [FLARE] : 549.272402559692372004                                                                                                                                         claim_rewards.py:107
[devops@flare src]$ 
```

### Claim Rewards - Specific Amount (i.e. 0.0000000000000001 FLR)
```
[devops@flare src]$ ./claim_rewards.py --claim --rewards 0.0000000000000001
╭─────────────────────────────────────────────────╮
│ FTSO Express - Validator Reward Checker/Claimer │
╰─────────────────────────────────────────────────╯
[17:49:11] INFO     Validator Rewards Total   [FLARE] : 549.272402559692378579                                                                                                                                         claim_rewards.py:106
           INFO     Validator Rewards Claimed [FLARE] : 549.272402559692371904                                                                                                                                         claim_rewards.py:107
           INFO     Rewards Claimable [6675] WEI      : 0.000000000000006675 FLR                                                                                                                                       claim_rewards.py:191
           INFO     Claiming Rewards   [100] WEI      : 0.000000000000000100 FLR                                                                                                                                       claim_rewards.py:202
[17:49:14] INFO     Validator Rewards Total   [FLARE] : 549.272402559692378579                                                                                                                                         claim_rewards.py:106
           INFO     Validator Rewards Claimed [FLARE] : 549.272402559692372004                                                                                                                                         claim_rewards.py:107
[devops@flare src]$
```