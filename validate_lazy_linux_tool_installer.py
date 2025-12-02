#!/usr/bin/env python3
"""
Quick validation script for Lazy-Linux-Tool-Installer.py
Checks code structure and basic functionality without running full tests.
"""

import importlib.util
import os
import sys

def validate_module():
    """Validate the module can be imported and has required components."""
    print("Validating Lazy-Linux-Tool-Installer.py...")
    
    # Load module
    script_path = os.path.join(os.path.dirname(__file__), "Lazy-Linux-Tool-Installer.py")
    if not os.path.exists(script_path):
        print(f"Error: {script_path} not found!")
        return False
    
    spec = importlib.util.spec_from_file_location(
        "lazy_linux_tool_installer",
        script_path
    )
    dlt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(dlt)
    
    errors = []
    warnings = []
    
    # Check required classes exist
    required_classes = ['SystemChecker', 'Installer', 'ToolManager', 'Tool', 'InstallMethod']
    for cls_name in required_classes:
        if not hasattr(dlt, cls_name):
            errors.append(f"Missing class: {cls_name}")
        else:
            print(f"✓ Found class: {cls_name}")
    
    # Check ToolManager has TOOLS
    if hasattr(dlt.ToolManager, 'TOOLS'):
        tool_count = len(dlt.ToolManager.TOOLS)
        print(f"✓ Found {tool_count} tools in TOOLS dictionary")
        
        # Validate each tool
        for name, tool in dlt.ToolManager.TOOLS.items():
            if not isinstance(tool, dlt.Tool):
                errors.append(f"Tool '{name}' is not a Tool instance")
                continue
            
            # Check required fields
            if not tool.name:
                errors.append(f"Tool '{name}' missing name")
            if not tool.command:
                errors.append(f"Tool '{name}' missing command")
            if not tool.method:
                errors.append(f"Tool '{name}' missing method")
            if not tool.package:
                errors.append(f"Tool '{name}' missing package")
            if not tool.description:
                warnings.append(f"Tool '{name}' missing description")
            if not tool.category:
                warnings.append(f"Tool '{name}' missing category")
            
            # Check eget tools have github_repo
            if tool.method == dlt.InstallMethod.EGET and not tool.github_repo:
                errors.append(f"Tool '{name}' uses EGET but missing github_repo")
    else:
        errors.append("ToolManager.TOOLS not found")
    
    # Check functions exist
    required_functions = ['get_user_consent', 'update_package_lists', 'main']
    for func_name in required_functions:
        if not hasattr(dlt, func_name):
            errors.append(f"Missing function: {func_name}")
        else:
            print(f"✓ Found function: {func_name}")
    
    # Summary
    print("\n" + "="*70)
    if errors:
        print(f"❌ Found {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
    else:
        print("✓ No errors found!")
    
    if warnings:
        print(f"\n⚠ Found {len(warnings)} warnings:")
        for warning in warnings:
            print(f"  - {warning}")
    
    print("="*70)
    
    return len(errors) == 0

if __name__ == '__main__':
    success = validate_module()
    sys.exit(0 if success else 1)

