# Hyperliquid Core Infrastructure

`chameleon-hl` is a reference implementation of the Hyperliquid protocol.

## Installation
Set up directory structure:
```
mkdir -p ~/cham/data
mkdir ~/cham/hyperliquid_data
git clone https://github.com/hyperliquid-dex/infra ~/cham/code
```

Install tendermint 0.34.24 to somewhere in your PATH. See `https://github.com/tendermint/tendermint/releases/tag/v0.34.24` for details.

Create an AWS S3 bucket for archiving of data, and put in `code/config.json`

Use the relevant binary for your operating system, e.g.
```
mv ~/cham/code/binaries/linux_x86/chameleon-hl ~/cham/code
```

Note that Windows is not supported at this time.

## Running a non-validating node
Generate tendermint genesis file:
```
python3 ~/cham/code/non_validator_setup.py
```

Run the node:
```
cd ~/cham/code && ./chameleon-hl run-non-validator --chain Testnet --config config.json
```

This command runs `tendermint` in the background, logging to `/tmp/tendermint_out`

You should see tendermint retrieve the initial state through state sync first, and then stream new blocks.

Block transitions including transactions will be streamed to `~/cham/data/replica_cmds/[start_time]/[date]`

State snapshots will be locally saved every 2000 blocks to `~/cham/data/periodic_abci_states/[date]/[height].rmp`

## Examining the Blockchain data

The inital state and subsequent transactions follow the typical ABCI state machine logic and determine a globally consistent state of the Hyperliquid DEX under Tendermint's BFT consensus algorithm.

To inspect a specific snapshot, try the following:
```
./chameleon-hl translate-abci-state ~/cham/data/periodic_abci_states/[date]/[height].rmp /tmp/out.json
```

This dumps the entire ABCI state to human readable JSON file. Load this file up in your scripting language of choice to analyze the fields.

## License
This project is licensed under the terms of the `MIT` license. See [LICENSE](LICENSE.md) for more details.

```bibtex
@misc{hyperliquid-infra,
  author = {Hyperliquid},
  title = {Chameleon client implementation for Hyperliquid L1},
  year = {2023},
  publisher = {GitHub},
  journal = {GitHub repository},
  howpublished = {\url{https://github.com/hyperliquid-dex/infra}}
}
```

## Terms
By using this package you agree to the Terms of Use. See [TERMS](TERMS.md) for more details.
