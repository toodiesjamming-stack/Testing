# Red Team Exploit Framework

**?? WARNING: AUTHORIZED USE ONLY ??**

This framework is designed exclusively for authorized penetration testing and security assessment purposes. Unauthorized use of this software is illegal and may result in criminal prosecution.

## Legal Disclaimer

This toolkit is provided for legitimate security testing purposes only. Users must:
- Have explicit written authorization before testing any system
- Comply with all applicable laws and regulations
- Use responsibly and ethically
- Not use for malicious purposes

The authors assume no responsibility for misuse of this software.

## Features

### Core Framework
- Modular exploit architecture
- Dynamic module loading
- Interactive command shell
- Session logging and tracking
- Payload generation system

### Exploit Modules

#### Web Exploits
- **web_rce.py**: Web-based Remote Code Execution exploits
  - Multiple encoding techniques
  - Command injection detection
  - Reverse shell payloads
  - Severity: CRITICAL (11/10)

- **sqli_exploit.py**: Advanced SQL Injection exploitation
  - Error-based detection
  - Union-based extraction
  - Boolean-based blind
  - Time-based blind
  - Database enumeration
  - Automated data extraction
  - Severity: CRITICAL (11/10)

#### Network Tools
- **network_scanner.py**: Comprehensive network scanning
  - Port scanning (single, range, common ports)
  - Subnet scanning
  - Service enumeration
  - Banner grabbing
  - HTTP/HTTPS information gathering
  - Severity: HIGH

#### Post-Exploitation
- **post_exploit.py**: Post-exploitation tools
  - System information gathering
  - User enumeration
  - Process enumeration
  - Network connection enumeration
  - Sensitive file discovery
  - Persistence mechanisms
  - Loot collection
  - Severity: CRITICAL

### Payload Generators

#### Reverse Shells
- **reverse_shell.py**: Multi-language reverse shell generator
  - Python
  - Bash
  - PowerShell
  - Perl
  - Ruby
  - PHP
  - Base64 encoded variants

#### Webshells
- **webshell.py**: Web-based shell generators
  - PHP webshell
  - Python Flask webshell
  - ASP webshell
  - JSP webshell
  - Obfuscation options

### Utilities
- **encoder.py**: Payload encoding utilities
  - Base64 encoding/decoding
  - URL encoding/decoding
  - Hex encoding/decoding
  - Unicode encoding
  - HTML entity encoding
  - ROT13 encoding
  - Multiple encoding combinations

## Installation

```bash
# Clone repository
git clone <repository-url>
cd red-team-exploit-framework

# Install dependencies
pip3 install -r requirements.txt

# Make scripts executable
chmod +x framework.py
chmod +x modules/*.py
chmod +x payloads/*.py
chmod +x utils/*.py
```

## Usage

### Interactive Mode

```bash
python3 framework.py -i
```

Interactive commands:
- `list` - List all loaded modules
- `info <module>` - Show module information
- `use <module>` - Select module for use
- `generate <payload_type>` - Generate payload
- `exit` - Exit framework

### Command Line Mode

```bash
# List modules
python3 framework.py -l

# Execute module
python3 framework.py -m web_rce --url http://target.com --param cmd --command "whoami"

# Generate payload
python3 framework.py -g reverse_shell --host 192.168.1.100 --port 4444 --language python
```

### Module Examples

#### Web RCE Exploit
```python
from framework import ExploitFramework

framework = ExploitFramework()
framework.load_module("modules/web_rce.py")

result = framework.execute_module(
    "web_rce",
    url="http://target.com/page.php",
    param="cmd",
    command="id"
)

print(result)
```

#### SQL Injection
```python
framework.load_module("modules/sqli_exploit.py")

result = framework.execute_module(
    "sqli_exploit",
    url="http://target.com/login.php",
    param="user",
    action="dump"
)
```

#### Network Scanning
```python
framework.load_module("modules/network_scanner.py")

result = framework.execute_module(
    "network_scanner",
    target="192.168.1.0/24",
    scan_type="subnet",
    ports="80,443,22"
)
```

#### Post-Exploitation
```python
framework.load_module("modules/post_exploit.py")

result = framework.execute_module(
    "post_exploit",
    action="loot"
)
```

### Payload Generation

#### Reverse Shell
```python
from payloads.reverse_shell import generate

payload = generate(
    host="192.168.1.100",
    port=4444,
    language="python"
)
print(payload)
```

#### Webshell
```python
from payloads.webshell import generate

shell = generate(
    language="php",
    obfuscation=True
)
print(shell)
```

### Encoding Utilities

```python
from utils.encoder import PayloadEncoder

encoder = PayloadEncoder()

# Base64 encode
encoded = encoder.base64_encode("whoami")

# Multiple encoding
encoded = encoder.multiple_encode(
    "whoami",
    methods=["base64", "url", "hex"]
)
```

## Module Development

Create custom modules by following this structure:

```python
#!/usr/bin/env python3
"""
Module Description
Severity: HIGH/CRITICAL
Author: Your Name
"""

ModuleInfo = {
    'name': 'module_name',
    'description': 'Module description',
    'author': 'Author name',
    'severity': 'HIGH',
    'requirements': ['dependency1', 'dependency2'],
    'category': 'category'
}

def execute(**kwargs):
    """Main execute function"""
    # Your exploit code here
    return {
        'success': True,
        'result': 'Exploit results'
    }
```

## Architecture

```
red-team-exploit-framework/
??? framework.py          # Core framework
??? modules/              # Exploit modules
?   ??? web_rce.py
?   ??? sqli_exploit.py
?   ??? network_scanner.py
?   ??? post_exploit.py
??? payloads/             # Payload generators
?   ??? reverse_shell.py
?   ??? webshell.py
??? utils/                # Utilities
?   ??? encoder.py
??? requirements.txt      # Dependencies
??? README.md            # This file
```

## Security Considerations

1. **Authorization**: Always obtain written authorization before testing
2. **Scope**: Stay within authorized scope
3. **Logging**: All activities are logged to session files
4. **Isolation**: Use in isolated test environments when possible
5. **Disclosure**: Follow responsible disclosure practices

## Best Practices

1. Document all testing activities
2. Use dedicated test environments
3. Clean up any persistence mechanisms after testing
4. Report findings responsibly
5. Follow OWASP guidelines
6. Comply with penetration testing standards

## Contributing

Contributions are welcome for:
- New exploit modules
- Payload generators
- Utility functions
- Documentation improvements
- Bug fixes

Please ensure all contributions include:
- Proper documentation
- Authorization warnings
- Error handling
- Logging

## License

This software is provided for educational and authorized security testing purposes only. See LICENSE file for details.

## Support

For issues, questions, or contributions, please use the project's issue tracker.

## Acknowledgments

Built for security professionals and authorized penetration testers. Use responsibly.

---

**Remember: With great power comes great responsibility. Use this toolkit ethically and legally.**
