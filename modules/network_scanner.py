#!/usr/bin/env python3
"""
Network Scanner and Enumeration Module
Severity: HIGH
Author: Security Research Team
"""

import socket
import subprocess
import threading
import ipaddress
from typing import Dict, List, Optional
from concurrent.futures import ThreadPoolExecutor
import struct

ModuleInfo = {
    'name': 'network_scanner',
    'description': 'Comprehensive network scanning and enumeration',
    'author': 'Security Research Team',
    'severity': 'HIGH',
    'requirements': [],
    'category': 'network'
}

class NetworkScanner:
    """Network scanning and enumeration class"""
    
    def __init__(self):
        self.common_ports = {
            21: 'FTP',
            22: 'SSH',
            23: 'Telnet',
            25: 'SMTP',
            53: 'DNS',
            80: 'HTTP',
            110: 'POP3',
            143: 'IMAP',
            443: 'HTTPS',
            445: 'SMB',
            3306: 'MySQL',
            3389: 'RDP',
            5432: 'PostgreSQL',
            8080: 'HTTP-Proxy',
            8443: 'HTTPS-Alt',
        }
        
        self.open_ports = []
        self.services = {}
    
    def ping_host(self, host: str, timeout: int = 1) -> bool:
        """Check if host is alive"""
        try:
            # Try ICMP ping
            result = subprocess.run(
                ['ping', '-c', '1', '-W', str(timeout), host],
                capture_output=True,
                timeout=timeout + 1
            )
            return result.returncode == 0
        except:
            try:
                # Fallback to TCP connect
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(timeout)
                result = sock.connect_ex((host, 80))
                sock.close()
                return result == 0
            except:
                return False
    
    def scan_port(self, host: str, port: int, timeout: float = 0.5) -> bool:
        """Scan a single port"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            result = sock.connect_ex((host, port))
            sock.close()
            return result == 0
        except:
            return False
    
    def scan_ports(self, host: str, ports: List[int], threads: int = 100) -> Dict[int, str]:
        """Scan multiple ports"""
        results = {}
        
        def scan_worker(port):
            if self.scan_port(host, port):
                service = self.common_ports.get(port, 'Unknown')
                results[port] = service
                self.open_ports.append(port)
                print(f"[+] {host}:{port} - {service} OPEN")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            executor.map(scan_worker, ports)
        
        return results
    
    def scan_range(self, host: str, start_port: int = 1, end_port: int = 65535, threads: int = 100) -> Dict[int, str]:
        """Scan port range"""
        ports = list(range(start_port, end_port + 1))
        return self.scan_ports(host, ports, threads)
    
    def scan_common_ports(self, host: str) -> Dict[int, str]:
        """Scan common ports"""
        ports = list(self.common_ports.keys())
        return self.scan_ports(host, ports)
    
    def get_service_banner(self, host: str, port: int, timeout: float = 2.0) -> Optional[str]:
        """Grab service banner"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            sock.connect((host, port))
            
            # Try to receive banner
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            sock.close()
            
            return banner[:200]  # Limit banner length
        except:
            return None
    
    def scan_subnet(self, subnet: str, port: Optional[int] = None) -> Dict[str, List[int]]:
        """Scan entire subnet"""
        results = {}
        
        try:
            network = ipaddress.ip_network(subnet, strict=False)
            print(f"[*] Scanning subnet {subnet} ({network.num_addresses} hosts)...")
            
            for ip in network.hosts():
                ip_str = str(ip)
                if self.ping_host(ip_str):
                    print(f"[+] Host {ip_str} is alive")
                    
                    if port:
                        if self.scan_port(ip_str, port):
                            results[ip_str] = [port]
                    else:
                        open_ports = self.scan_common_ports(ip_str)
                        if open_ports:
                            results[ip_str] = list(open_ports.keys())
        except Exception as e:
            print(f"Error scanning subnet: {e}")
        
        return results
    
    def enumerate_services(self, host: str, ports: List[int]) -> Dict[int, Dict]:
        """Enumerate services on open ports"""
        enumeration = {}
        
        for port in ports:
            banner = self.get_service_banner(host, port)
            service_info = {
                'port': port,
                'service': self.common_ports.get(port, 'Unknown'),
                'banner': banner
            }
            
            # Additional enumeration based on port
            if port == 80 or port == 8080:
                service_info['http_headers'] = self.get_http_headers(host, port)
            elif port == 443 or port == 8443:
                service_info['https_info'] = self.get_https_info(host, port)
            
            enumeration[port] = service_info
        
        return enumeration
    
    def get_http_headers(self, host: str, port: int) -> Optional[Dict]:
        """Get HTTP headers"""
        try:
            import requests
            url = f"http://{host}:{port}"
            response = requests.get(url, timeout=5, verify=False)
            return dict(response.headers)
        except:
            return None
    
    def get_https_info(self, host: str, port: int) -> Optional[Dict]:
        """Get HTTPS/TLS information"""
        try:
            import ssl
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            
            with socket.create_connection((host, port), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=host) as ssock:
                    cert = ssock.getpeercert()
                    return {
                        'version': ssock.version(),
                        'cipher': ssock.cipher(),
                        'certificate': cert
                    }
        except:
            return None


def execute(target: str = None, ports: str = None, scan_type: str = "common", **kwargs) -> Dict:
    """Main execute function"""
    scanner = NetworkScanner()
    
    if not target:
        return {
            'success': False,
            'error': 'Target required',
            'usage': {
                'target': 'Target host or subnet (e.g., 192.168.1.1 or 192.168.1.0/24)',
                'ports': 'Port range (e.g., 1-1000) or "common"',
                'scan_type': 'Type: common, range, subnet'
            }
        }
    
    print(f"[*] Starting scan of {target}...")
    
    # Check if host is alive
    if '/' not in target:  # Not a subnet
        if not scanner.ping_host(target):
            print(f"[!] Host {target} appears to be down")
        else:
            print(f"[+] Host {target} is alive")
    
    results = {}
    
    if scan_type == "common":
        results = scanner.scan_common_ports(target)
    elif scan_type == "range" and ports:
        if '-' in ports:
            start, end = map(int, ports.split('-'))
            results = scanner.scan_range(target, start, end)
        else:
            port_list = [int(p) for p in ports.split(',')]
            results = scanner.scan_ports(target, port_list)
    elif scan_type == "subnet":
        port = int(ports) if ports and ports.isdigit() else None
        results = scanner.scan_subnet(target, port)
    
    # Enumerate services
    if '/' not in target and results:
        open_ports = list(results.keys()) if isinstance(results, dict) else results
        enumeration = scanner.enumerate_services(target, open_ports)
        results = {'ports': results, 'enumeration': enumeration}
    
    return {
        'success': True,
        'target': target,
        'results': results,
        'open_ports': scanner.open_ports
    }
