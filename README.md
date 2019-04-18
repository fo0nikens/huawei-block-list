# huawei-block-list

From captured DNS requests from Huawei P30 Pro to a block list

## Setup

1. Setup [Algo VPN](https://github.com/trailofbits/algo) and enable adblocking feature on both server and client-side
2. Update `/usr/local/sbin/adblock.sh` to include [the raw version of block list](https://raw.githubusercontent.com/pe3zx/huawei-block-list/master/master.txt). The block list should be appended to `BLOCKLIST_URLS` variable.
3. Execute `/usr/local/sbin/adblock.sh` to apply new block list to dnsmasq. The script will be automatically executed by cron to pull and apply any updates.

```sh
# awk '{gsub(/"$/,"https://raw.githubusercontent.com/pe3zx/huawei-block-list/master/master.txt \"")}' /usr/local/sbin/adblock.sh
# sh /usr/local/sbin
```
