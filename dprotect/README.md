# dProtect — Hybrid Layered DDoS Defence

> Reconstructed starter documentation based on saved project architecture notes; this is not the original source tree.

A low-cost layered DDoS mitigation prototype for MSMEs, combining HAProxy, a rotating firewall-node policy, nftables, Nginx reverse-proxy filtering, and optional IDS/log monitoring.

## Architecture

```text
Internet / authorised lab traffic
          -> HAProxy
          -> one active firewall node (FW-A / FW-B / FW-C)
          -> Nginx reverse proxy
          -> protected web service
```

The intended controller keeps one healthy firewall node active for a minimum dwell period. On sustained load or health failure it selects a different healthy node with the lowest reported load, then applies a cooldown to reduce flapping. The included prototype is dry-run only and does not reconfigure live networking.

## Lab notes

Saved historical values: Mac host gateway `192.168.64.1`, HAProxy `192.168.64.3`, firewall A `192.168.64.4`. Verify these against the current QEMU network before use.

## Components

- HAProxy load balancing and health checks
- nftables/UFW filtering
- Nginx reverse proxy and request limits
- Optional Suricata, Zeek, Wazuh, CrowdSec, and Fail2Ban
- Python policy simulation

## Status and safety

TRL-3 prototype / development in progress. Templates require review and lab validation; this project does not guarantee production DDoS protection. Test only on systems you own or are authorised to assess. Never generate denial-of-service traffic against public systems.
