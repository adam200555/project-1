import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import scan_import  # noqa: E402

SAMPLE = ROOT / "scans" / "sample-nmap.xml"


def test_hosts_that_are_down_are_skipped():
    ips = [h["ip"] for h in scan_import.parse_nmap(SAMPLE)]
    assert ips == ["192.168.56.101", "192.168.56.102"]


def test_only_open_ports_are_kept():
    host = scan_import.parse_nmap(SAMPLE)[0]
    assert sorted(p["number"] for p in host["ports"]) == [21, 22, 80, 3306]


def test_service_details_are_parsed():
    ftp = next(p for p in scan_import.parse_nmap(SAMPLE)[0]["ports"] if p["number"] == 21)
    assert (ftp["service"], ftp["product"], ftp["version"]) == ("ftp", "vsftpd", "2.3.4")


def test_missing_values_are_empty_strings_not_none():
    for host in scan_import.parse_nmap(SAMPLE):
        assert host["hostname"] is not None and host["os"] is not None
        for port in host["ports"]:
            assert None not in port.values()
