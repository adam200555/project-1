"""Import an nmap XML scan into Neo4j as an attack-surface graph.

Usage:
    python scan_import.py scans/lab.xml

Graph model:
    (Host)-[:HAS_PORT]->(Port)-[:RUNS]->(Service)
Services are shared between hosts, so you can ask "which hosts run vsftpd 2.3.4?".
"""
import os
import sys

from defusedxml import ElementTree as ET
from neo4j import GraphDatabase

URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
AUTH = (os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD", "password123"))

IMPORT = """
UNWIND $hosts AS h
MERGE (host:Host {ip: h.ip})
SET host.hostname = h.hostname, host.os = h.os
WITH host, h
UNWIND h.ports AS p
MERGE (port:Port {host: h.ip, number: p.number, protocol: p.protocol})
MERGE (host)-[:HAS_PORT]->(port)
MERGE (svc:Service {name: p.service, product: p.product, version: p.version})
MERGE (port)-[:RUNS]->(svc)
"""


def parse_nmap(path):
    """Return a list of hosts (dicts) from an nmap XML file. Only hosts that are up
    and ports that are open are kept. Missing values become empty strings, because
    Neo4j cannot MERGE on a null property."""
    hosts = []
    root = ET.parse(path).getroot()
    for h in root.findall("host"):
        status = h.find("status")
        if status is None or status.get("state") != "up":
            continue
        ip = next(
            (a.get("addr") for a in h.findall("address") if a.get("addrtype") == "ipv4"),
            None,
        )
        if ip is None:
            continue
        hostname_el = h.find("hostnames/hostname")
        os_el = h.find("os/osmatch")
        ports = []
        for p in h.findall("ports/port"):
            state = p.find("state")
            if state is None or state.get("state") != "open":
                continue
            svc = p.find("service")
            ports.append(
                {
                    "number": int(p.get("portid")),
                    "protocol": p.get("protocol") or "",
                    "service": (svc.get("name") if svc is not None else "") or "unknown",
                    "product": (svc.get("product") if svc is not None else "") or "",
                    "version": (svc.get("version") if svc is not None else "") or "",
                }
            )
        hosts.append(
            {
                "ip": ip,
                "hostname": (hostname_el.get("name") if hostname_el is not None else "") or "",
                "os": (os_el.get("name") if os_el is not None else "") or "",
                "ports": ports,
            }
        )
    return hosts


def main(path):
    hosts = parse_nmap(path)
    with GraphDatabase.driver(URI, auth=AUTH) as driver:
        driver.verify_connectivity()
        driver.execute_query(IMPORT, hosts=hosts)
    total_ports = sum(len(h["ports"]) for h in hosts)
    print(f"Imported {len(hosts)} hosts and {total_ports} open ports from {path}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: python scan_import.py <nmap-scan.xml>")
    main(sys.argv[1])
