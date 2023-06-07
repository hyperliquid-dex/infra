import argparse
import json
import os
import requests
import tomli
import tomli_w
import subprocess

TESTNET_RPC = "http://35.73.179.90:26657"

TESTNET_INFO = {
    "NvTestnet": {
        "id": "442c9dbe66e4ebb195e429f9583a5f57940304b1",
        "ip": "35.73.179.90",
    },
    "NvTestnet2": {
        "id": "a2487a8f787a3c29c0fb40325a589d4235788bf8",
        "ip": "35.73.66.171",
    },
}

CONFIG_HOME = os.path.expanduser("~/cham/nv_tendermint/config")


def query_trust_height():
    trust_height = 1
    for node in TESTNET_INFO.values():
        resp = requests.post(f"{TESTNET_RPC}/commit?height=1").json()
        earliest_height = int(resp["error"]["data"].split(' ')[-1])
        trust_height = max(trust_height, earliest_height)
    return trust_height


def query_trust_params():
    trust_height = query_trust_height()
    resp = requests.post(f"{TESTNET_RPC}/commit?height={trust_height}").json()
    commit_details = resp["result"]["signed_header"]["commit"]
    trust_height = int(commit_details["height"])
    trust_hash = commit_details["block_id"]["hash"]
    return (trust_height, trust_hash)


def download_genesis():
    resp = requests.post(f"{TESTNET_RPC}/genesis").json()
    with open(f"{CONFIG_HOME}/genesis.json", "w") as f:
        json.dump(resp["result"]["genesis"], f, indent=4)


def update_tendermint_config():
    config_fln = f"{CONFIG_HOME}/config.toml"
    with open(config_fln, "rb") as f:
        config = tomli.load(f)

    persistent_peers = ",".join([f'{v["id"]}@{v["ip"]}:26656' for v in TESTNET_INFO.values()])
    rpc_servers = ",".join([f'tcp://{v["ip"]}:26657' for v in TESTNET_INFO.values()])

    config["p2p"]["persistent_peers"] = persistent_peers
    config["statesync"]["enable"] = True
    config["statesync"]["rpc_servers"] = rpc_servers
    (trust_height, trust_hash) = query_trust_params()
    config["statesync"]["trust_height"] = trust_height
    config["statesync"]["trust_hash"] = trust_hash

    with open(config_fln, "wb") as f:
        tomli_w.dump(config, f)


def main():
    parser = argparse.ArgumentParser(description="run public non-validator node")
    parser.add_argument("--chain", required=True)
    args = parser.parse_args()

    chain = args.chain
    assert chain == "Testnet"

    os.makedirs(CONFIG_HOME, exist_ok=True)
    subprocess.call(["tendermint", "init", "--home", os.path.dirname(CONFIG_HOME)])
    download_genesis()
    update_tendermint_config()


if __name__ == "__main__":
    main()
