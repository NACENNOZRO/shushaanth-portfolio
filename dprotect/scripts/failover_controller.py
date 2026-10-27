#!/usr/bin/env python3
"""dProtect firewall rotation policy prototype (dry-run only).

Does not change HAProxy, nftables, routing, or any live system.
"""
from __future__ import annotations
import argparse
import time
from dataclasses import dataclass
from typing import Iterable

@dataclass
class Node:
    name: str
    healthy: bool = True
    load: float = 0.0  # illustrative normalized load: 0.0–1.0

class RotationPolicy:
    def __init__(self, nodes: Iterable[Node], active: str,
                 dwell_seconds: int = 300, cooldown_seconds: int = 120,
                 load_threshold: float = 0.80) -> None:
        self.nodes = list(nodes)
        if not self.nodes:
            raise ValueError("At least one node is required")
        if active not in {n.name for n in self.nodes}:
            raise ValueError("Active node must exist")
        self.active = active
        self.dwell_seconds = max(0, dwell_seconds)
        self.cooldown_seconds = max(0, cooldown_seconds)
        self.load_threshold = load_threshold
        self.last_switch = 0.0
        self.activated_at = time.monotonic()

    def evaluate(self, now: float | None = None) -> str | None:
        now = time.monotonic() if now is None else now
        current = next(n for n in self.nodes if n.name == self.active)
        if now - self.activated_at < self.dwell_seconds:
            return None
        if now - self.last_switch < self.cooldown_seconds:
            return None
        if current.healthy and current.load < self.load_threshold:
            return None
        candidates = [n for n in self.nodes if n.name != self.active and n.healthy]
        if not candidates:
            return None
        return min(candidates, key=lambda n: n.load).name

    def apply_dry_run(self, candidate: str, now: float | None = None) -> None:
        """Record a simulated switch; no network changes are made."""
        now = time.monotonic() if now is None else now
        self.active = candidate
        self.last_switch = now
        self.activated_at = now

def simulate() -> None:
    now = 1000.0
    nodes = [Node("fw-a", True, 0.92), Node("fw-b", True, 0.35), Node("fw-c", True, 0.48)]
    policy = RotationPolicy(nodes, "fw-a", dwell_seconds=300, cooldown_seconds=120)
    policy.activated_at = now - 360
    candidate = policy.evaluate(now=now)
    print(f"active={policy.active}")
    print(f"rotation_candidate={candidate or 'none (no switch advised)'}")
    if candidate:
        policy.apply_dry_run(candidate, now=now)
        print(f"simulated_active_after_switch={policy.active}")
        print("Dry run only: no live network configuration changed.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--simulate", action="store_true", help="run a deterministic dry-run example")
    args = parser.parse_args()
    if args.simulate:
        simulate()
    else:
        parser.print_help()
