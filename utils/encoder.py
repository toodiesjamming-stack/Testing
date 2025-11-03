#!/usr/bin/env python3
"""
Payload Encoding Utilities
Author: Security Research Team
"""

import base64
import urllib.parse
import binascii
import codecs

class PayloadEncoder:
    """Encode payloads in various formats"""
    
    @staticmethod
    def base64_encode(payload: str) -> str:
        """Base64 encode payload"""
        return base64.b64encode(payload.encode()).decode()
    
    @staticmethod
    def base64_decode(encoded: str) -> str:
        """Base64 decode payload"""
        try:
            return base64.b64decode(encoded).decode()
        except:
            return ""
    
    @staticmethod
    def url_encode(payload: str) -> str:
        """URL encode payload"""
        return urllib.parse.quote(payload)
    
    @staticmethod
    def url_decode(encoded: str) -> str:
        """URL decode payload"""
        return urllib.parse.unquote(encoded)
    
    @staticmethod
    def hex_encode(payload: str) -> str:
        """Hex encode payload"""
        return binascii.hexlify(payload.encode()).decode()
    
    @staticmethod
    def hex_decode(encoded: str) -> str:
        """Hex decode payload"""
        try:
            return binascii.unhexlify(encoded).decode()
        except:
            return ""
    
    @staticmethod
    def unicode_encode(payload: str) -> str:
        """Unicode encode payload"""
        return ''.join([f'\\u{ord(c):04x}' for c in payload])
    
    @staticmethod
    def html_encode(payload: str) -> str:
        """HTML entity encode"""
        encoded = ""
        for char in payload:
            if ord(char) > 127:
                encoded += f"&#{ord(char)};"
            else:
                encoded += char
        return encoded
    
    @staticmethod
    def rot13_encode(payload: str) -> str:
        """ROT13 encode"""
        return codecs.encode(payload, 'rot13')
    
    @staticmethod
    def double_encode(payload: str, method: str = "url") -> str:
        """Double encode payload"""
        if method == "url":
            return urllib.parse.quote(urllib.parse.quote(payload))
        elif method == "base64":
            encoded = base64.b64encode(payload.encode()).decode()
            return base64.b64encode(encoded.encode()).decode()
        return payload
    
    @staticmethod
    def multiple_encode(payload: str, methods: list) -> str:
        """Apply multiple encoding methods"""
        result = payload
        for method in methods:
            if method == "base64":
                result = PayloadEncoder.base64_encode(result)
            elif method == "url":
                result = PayloadEncoder.url_encode(result)
            elif method == "hex":
                result = PayloadEncoder.hex_encode(result)
            elif method == "unicode":
                result = PayloadEncoder.unicode_encode(result)
        return result


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: encoder.py <method> <payload>")
        print("Methods: base64, url, hex, unicode, html, rot13")
        sys.exit(1)
    
    method = sys.argv[1].lower()
    payload = sys.argv[2]
    
    encoder = PayloadEncoder()
    
    if method == "base64":
        print(encoder.base64_encode(payload))
    elif method == "url":
        print(encoder.url_encode(payload))
    elif method == "hex":
        print(encoder.hex_encode(payload))
    elif method == "unicode":
        print(encoder.unicode_encode(payload))
    elif method == "html":
        print(encoder.html_encode(payload))
    elif method == "rot13":
        print(encoder.rot13_encode(payload))
    else:
        print(f"Unknown method: {method}")
