#!/usr/bin/env python3
"""
Red Team Exploit Framework - Core Framework
Author: Security Research Team
Purpose: Authorized penetration testing and security assessment only
WARNING: Use only on systems you own or have explicit written authorization to test
"""

import os
import sys
import json
import argparse
import importlib.util
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

class ExploitFramework:
    """Core framework for exploit management and execution"""
    
    def __init__(self):
        self.name = "RedTeam Exploit Framework"
        self.version = "1.0.0"
        self.modules = {}
        self.payloads = {}
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.log_file = f"exploit_session_{self.session_id}.log"
        
        # Setup logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
        
        self.logger.warning("=" * 80)
        self.logger.warning("RED TEAM EXPLOIT FRAMEWORK - AUTHORIZED USE ONLY")
        self.logger.warning("=" * 80)
        self.logger.warning("WARNING: This tool is for authorized security testing only.")
        self.logger.warning("Unauthorized use is illegal and unethical.")
        self.logger.warning("=" * 80)
        
    def load_module(self, module_path: str) -> bool:
        """Dynamically load exploit modules"""
        try:
            spec = importlib.util.spec_from_file_location("module", module_path)
            if spec is None:
                self.logger.error(f"Could not load spec from {module_path}")
                return False
                
            module = importlib.util.module_from_spec(spec)
            if spec.loader is None:
                self.logger.error(f"Could not load module loader from {module_path}")
                return False
                
            spec.loader.exec_module(module)
            
            # Register module if it has required attributes
            if hasattr(module, 'ModuleInfo'):
                info = module.ModuleInfo
                module_name = info.get('name', Path(module_path).stem)
                self.modules[module_name] = {
                    'module': module,
                    'info': info,
                    'path': module_path
                }
                self.logger.info(f"Loaded module: {module_name}")
                return True
            else:
                self.logger.warning(f"Module {module_path} missing ModuleInfo, skipping")
                return False
                
        except Exception as e:
            self.logger.error(f"Error loading module {module_path}: {e}")
            return False
    
    def load_all_modules(self, modules_dir: str = "modules"):
        """Load all modules from directory"""
        modules_path = Path(modules_dir)
        if not modules_path.exists():
            self.logger.warning(f"Modules directory {modules_dir} not found")
            return
            
        for module_file in modules_path.glob("*.py"):
            if module_file.name != "__init__.py":
                self.load_module(str(module_file))
    
    def list_modules(self) -> List[str]:
        """List all loaded modules"""
        return list(self.modules.keys())
    
    def get_module_info(self, module_name: str) -> Optional[Dict]:
        """Get information about a specific module"""
        if module_name in self.modules:
            return self.modules[module_name]['info']
        return None
    
    def execute_module(self, module_name: str, **kwargs) -> Dict:
        """Execute an exploit module"""
        if module_name not in self.modules:
            return {
                'success': False,
                'error': f"Module {module_name} not found"
            }
        
        module_obj = self.modules[module_name]['module']
        info = self.modules[module_name]['info']
        
        self.logger.info(f"Executing module: {module_name}")
        self.logger.info(f"Description: {info.get('description', 'N/A')}")
        
        try:
            if hasattr(module_obj, 'execute'):
                result = module_obj.execute(**kwargs)
                self.logger.info(f"Module {module_name} execution completed")
                return {
                    'success': True,
                    'module': module_name,
                    'result': result
                }
            else:
                return {
                    'success': False,
                    'error': f"Module {module_name} missing execute() function"
                }
        except Exception as e:
            self.logger.error(f"Error executing module {module_name}: {e}")
            return {
                'success': False,
                'error': str(e)
            }
    
    def generate_payload(self, payload_type: str, **kwargs) -> Optional[str]:
        """Generate payload using payload generators"""
        payload_generators = Path("payloads")
        if not payload_generators.exists():
            self.logger.warning("Payloads directory not found")
            return None
            
        payload_file = payload_generators / f"{payload_type}.py"
        if not payload_file.exists():
            self.logger.error(f"Payload generator {payload_type} not found")
            return None
        
        try:
            spec = importlib.util.spec_from_file_location("payload", str(payload_file))
            if spec is None or spec.loader is None:
                return None
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            if hasattr(module, 'generate'):
                return module.generate(**kwargs)
            else:
                self.logger.error(f"Payload generator {payload_type} missing generate() function")
                return None
        except Exception as e:
            self.logger.error(f"Error generating payload {payload_type}: {e}")
            return None
    
    def interactive_shell(self):
        """Interactive command shell"""
        print(f"\n[{self.name} v{self.version}]")
        print("Type 'help' for commands, 'exit' to quit\n")
        
        while True:
            try:
                cmd = input("exploit> ").strip()
                if not cmd:
                    continue
                    
                parts = cmd.split()
                command = parts[0].lower()
                
                if command == "exit" or command == "quit":
                    print("Exiting framework...")
                    break
                elif command == "help":
                    self.show_help()
                elif command == "list":
                    modules = self.list_modules()
                    if modules:
                        print("\nAvailable modules:")
                        for mod in modules:
                            info = self.get_module_info(mod)
                            desc = info.get('description', 'No description') if info else 'No info'
                            print(f"  - {mod}: {desc}")
                    else:
                        print("No modules loaded")
                elif command == "info":
                    if len(parts) > 1:
                        module_name = parts[1]
                        info = self.get_module_info(module_name)
                        if info:
                            print(f"\nModule: {module_name}")
                            print(f"Description: {info.get('description', 'N/A')}")
                            print(f"Author: {info.get('author', 'N/A')}")
                            print(f"Severity: {info.get('severity', 'N/A')}")
                            print(f"Requirements: {info.get('requirements', 'N/A')}")
                        else:
                            print(f"Module {module_name} not found")
                    else:
                        print("Usage: info <module_name>")
                elif command == "use":
                    if len(parts) > 1:
                        module_name = parts[1]
                        if module_name in self.modules:
                            print(f"Using module: {module_name}")
                            print("Set options with: set <option> <value>")
                            print("Execute with: run")
                            # Module context would be implemented here
                        else:
                            print(f"Module {module_name} not found")
                    else:
                        print("Usage: use <module_name>")
                elif command == "generate":
                    if len(parts) > 1:
                        payload_type = parts[1]
                        payload = self.generate_payload(payload_type)
                        if payload:
                            print(f"\nGenerated payload:\n{payload}")
                        else:
                            print(f"Failed to generate payload: {payload_type}")
                    else:
                        print("Usage: generate <payload_type>")
                else:
                    print(f"Unknown command: {command}. Type 'help' for commands.")
                    
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except EOFError:
                break
            except Exception as e:
                print(f"Error: {e}")
    
    def show_help(self):
        """Display help information"""
        help_text = """
Available Commands:
  help                    - Show this help message
  list                    - List all loaded modules
  info <module>           - Show detailed information about a module
  use <module>            - Select a module for use
  generate <payload_type> - Generate a payload
  exit/quit               - Exit the framework
        """
        print(help_text)


def main():
    parser = argparse.ArgumentParser(
        description="Red Team Exploit Framework - Authorized testing only",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
WARNING: This tool is for authorized security testing only.
Unauthorized use is illegal and may result in criminal prosecution.
        """
    )
    
    parser.add_argument("-m", "--module", help="Module to execute")
    parser.add_argument("-l", "--list", action="store_true", help="List all modules")
    parser.add_argument("-i", "--interactive", action="store_true", help="Start interactive shell")
    parser.add_argument("-g", "--generate", help="Generate payload (type)")
    parser.add_argument("--load-dir", default="modules", help="Directory containing modules")
    
    args = parser.parse_args()
    
    framework = ExploitFramework()
    framework.load_all_modules(args.load_dir)
    
    if args.list:
        modules = framework.list_modules()
        print("\nLoaded modules:")
        for mod in modules:
            print(f"  - {mod}")
    elif args.module:
        result = framework.execute_module(args.module)
        print(json.dumps(result, indent=2))
    elif args.generate:
        payload = framework.generate_payload(args.generate)
        if payload:
            print(payload)
    elif args.interactive:
        framework.interactive_shell()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
