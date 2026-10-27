# Architecture and rotation policy

## Traffic path
1. HAProxy accepts traffic on the lab-facing frontend.
2. Traffic is forwarded to the currently selected firewall node.
3. The firewall applies network filtering.
4. Nginx reverse proxy applies HTTP request controls and forwards to the protected service.
5. Telemetry from HAProxy, firewall nodes, Nginx, and optional IDS tools informs the operator.

## Rotation behaviour
The target design uses one active firewall node at a time, not a fixed VM2 → VM3 → VM4 sequence. The controller should maintain a minimum dwell time, detect sustained load or node health failure, select a different healthy node, apply a cooldown, and log each decision. This repository's Python example only demonstrates candidate selection; it does not update HAProxy or firewall rules.

## Historical lab values
- Mac host gateway: `192.168.64.1`
- HAProxy: `192.168.64.3`
- Firewall A: `192.168.64.4`

These are historical notes, not guaranteed current values. Confirm interfaces, routes, and addresses in your QEMU private network before use.

## Security
Keep management endpoints private and authenticated. Review firewall policies before applying them and maintain console access for recovery. Use bounded, authorised tests on an isolated lab network only.