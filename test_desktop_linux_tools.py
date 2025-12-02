#!/usr/bin/env python3
"""
Test suite for Desktop-Linux-Tools.py
Non-invasive tests using mocks to avoid actual system modifications.
Platform-independent - works on Mac, Linux, and Windows.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os
import subprocess
import shutil

# Import the module to test (handle hyphen in filename)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "desktop_linux_tools",
    os.path.join(os.path.dirname(__file__), "Desktop-Linux-Tools.py")
)
dlt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(dlt)


class TestSystemChecker(unittest.TestCase):
    """Test SystemChecker class."""
    
    @patch.object(dlt, 'shutil')
    def test_is_debian_like_true(self, mock_shutil):
        """Test Debian detection when apt-get exists."""
        mock_shutil.which.return_value = '/usr/bin/apt-get'
        self.assertTrue(dlt.SystemChecker.is_debian_like())
        mock_shutil.which.assert_called_with('apt-get')
    
    @patch.object(dlt, 'shutil')
    def test_is_debian_like_false(self, mock_shutil):
        """Test Debian detection when apt-get doesn't exist."""
        mock_shutil.which.return_value = None
        self.assertFalse(dlt.SystemChecker.is_debian_like())
    
    @patch.object(dlt, 'os')
    def test_is_root_true(self, mock_os):
        """Test root detection when running as root."""
        mock_os.geteuid.return_value = 0
        self.assertTrue(dlt.SystemChecker.is_root())
    
    @patch.object(dlt, 'os')
    def test_is_root_false(self, mock_os):
        """Test root detection when not running as root."""
        mock_os.geteuid.return_value = 1000
        self.assertFalse(dlt.SystemChecker.is_root())
    
    @patch.object(dlt, 'shutil')
    def test_has_command_true(self, mock_shutil):
        """Test command existence check when command exists."""
        mock_shutil.which.return_value = '/usr/bin/vim'
        self.assertTrue(dlt.SystemChecker.has_command('vim'))
    
    @patch.object(dlt, 'shutil')
    def test_has_command_false(self, mock_shutil):
        """Test command existence check when command doesn't exist."""
        mock_shutil.which.return_value = None
        self.assertFalse(dlt.SystemChecker.has_command('nonexistent'))
    
    @patch.object(dlt, 'shutil')
    def test_check_system_success(self, mock_shutil):
        """Test system check when all requirements are met."""
        def which_side_effect(cmd):
            if cmd == 'apt-get':
                return '/usr/bin/apt-get'
            elif cmd == 'sudo':
                return '/usr/bin/sudo'
            return None
        mock_shutil.which.side_effect = which_side_effect
        is_compatible, error = dlt.SystemChecker.check_system()
        self.assertTrue(is_compatible)
        self.assertIsNone(error)
    
    @patch.object(dlt, 'shutil')
    def test_check_system_no_debian(self, mock_shutil):
        """Test system check when not Debian-based."""
        mock_shutil.which.return_value = None
        is_compatible, error = dlt.SystemChecker.check_system()
        self.assertFalse(is_compatible)
        self.assertIsNotNone(error)
        self.assertIn('Debian', error)
    
    @patch.object(dlt, 'shutil')
    def test_check_system_no_sudo(self, mock_shutil):
        """Test system check when sudo is missing."""
        def which_side_effect(cmd):
            if cmd == 'apt-get':
                return '/usr/bin/apt-get'
            elif cmd == 'sudo':
                return None
            return None
        mock_shutil.which.side_effect = which_side_effect
        is_compatible, error = dlt.SystemChecker.check_system()
        self.assertFalse(is_compatible)
        self.assertIsNotNone(error)
        self.assertIn('sudo', error)


class TestInstaller(unittest.TestCase):
    """Test Installer class."""
    
    @patch.object(dlt, 'subprocess')
    def test_run_command_success(self, mock_subprocess):
        """Test successful command execution."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['test'], 0)
        result = dlt.Installer.run_command(['test', 'cmd'])
        self.assertEqual(result.returncode, 0)
        mock_subprocess.run.assert_called_once()
        # Verify timeout is set
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
    
    @patch.object(dlt, 'subprocess')
    def test_run_command_failure(self, mock_subprocess):
        """Test failed command execution."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['test'], 1)
        result = dlt.Installer.run_command(['test', 'cmd'])
        self.assertEqual(result.returncode, 1)
    
    @patch.object(dlt.subprocess, 'run')
    def test_run_command_file_not_found(self, mock_run):
        """Test command execution when command not found."""
        mock_run.side_effect = FileNotFoundError("Command not found")
        with patch('builtins.print'):  # Suppress print output
            result = dlt.Installer.run_command(['nonexistent'])
        self.assertEqual(result.returncode, 1)  # FileNotFoundError returns 1 per implementation
        # CompletedProcess defaults to None for stdout/stderr when not specified
        self.assertIsNone(result.stdout)
        self.assertIsNone(result.stderr)
    
    @patch.object(dlt.subprocess, 'run')
    def test_run_command_timeout(self, mock_run):
        """Test command execution timeout."""
        # TimeoutExpired needs cmd and timeout args
        timeout_expired = subprocess.TimeoutExpired(['test', 'cmd'], 30)
        mock_run.side_effect = timeout_expired
        with patch('builtins.print'):  # Suppress print output
            result = dlt.Installer.run_command(['test', 'cmd'], timeout=30)
        self.assertEqual(result.returncode, 124)  # TimeoutExpired returns 124 per implementation
        # CompletedProcess defaults to None for stdout/stderr when not specified
        self.assertIsNone(result.stdout)
        self.assertIsNone(result.stderr)
    
    @patch.object(dlt, 'subprocess')
    def test_install_via_apt_success(self, mock_subprocess):
        """Test successful apt installation."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sudo'], 0)
        result = dlt.Installer.install_via_apt('vim')
        self.assertTrue(result)
        # Check that timeout is included in call
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
    
    @patch.object(dlt, 'subprocess')
    def test_install_via_apt_failure(self, mock_subprocess):
        """Test failed apt installation."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sudo'], 1)
        result = dlt.Installer.install_via_apt('vim')
        self.assertFalse(result)
    
    @patch.object(dlt, 'subprocess')
    def test_install_via_pip_success(self, mock_subprocess):
        """Test successful pip installation."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['pip3'], 0)
        result = dlt.Installer.install_via_pip('glances')
        self.assertTrue(result)
        # Verify timeout is set
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
    
    @patch.object(dlt, 'subprocess')
    def test_install_via_snap_success(self, mock_subprocess):
        """Test successful snap installation."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sudo'], 0)
        result = dlt.Installer.install_via_snap('code', classic=True)
        self.assertTrue(result)
        # Verify timeout is set
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
    
    @patch.object(dlt, 'subprocess')
    @patch.object(dlt, 'os')
    @patch.object(dlt, 'shutil')
    def test_install_via_eget_success(self, mock_shutil, mock_os, mock_subprocess):
        """Test successful eget installation."""
        mock_shutil.which.return_value = '/usr/local/bin/eget'
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['eget'], 0)
        mock_os.path.exists.return_value = True
        
        result = dlt.Installer.install_via_eget('sharkdp/bat', 'bat')
        self.assertTrue(result)
        # Verify timeout is set for network operations
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
        self.assertGreaterEqual(call_kwargs['timeout'], 30)
    
    @patch.object(dlt, 'subprocess')
    @patch.object(dlt, 'os')
    @patch.object(dlt, 'shutil')
    def test_install_via_eget_no_eget(self, mock_shutil, mock_os, mock_subprocess):
        """Test eget installation when eget is not installed."""
        mock_shutil.which.return_value = None
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sh'], 0)
        mock_os.path.exists.side_effect = [False, True]  # eget not found, then eget binary exists
        
        result = dlt.Installer.install_via_eget('sharkdp/bat', 'bat')
        # Should try to install eget first with longer timeout
        self.assertTrue(mock_subprocess.run.called)
        # Check that eget installation has longer timeout
        calls = [call for call in mock_subprocess.run.call_args_list if len(call[0]) > 0 and 'curl' in str(call[0][0])]
        if calls:
            call_kwargs = calls[0][1]
            self.assertGreaterEqual(call_kwargs.get('timeout', 0), 60)
    
    @patch.object(dlt, 'subprocess')
    def test_check_apt_available_true(self, mock_subprocess):
        """Test apt package availability check when available."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(
            ['apt-cache'], 0, stdout='vim\nvim-common\n'
        )
        result = dlt.Installer.check_apt_available('vim')
        self.assertTrue(result)
        # Verify timeout is set
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
    
    @patch.object(dlt, 'subprocess')
    def test_check_apt_available_false(self, mock_subprocess):
        """Test apt package availability check when not available."""
        mock_subprocess.run.return_value = subprocess.CompletedProcess(
            ['apt-cache'], 0, stdout=''
        )
        result = dlt.Installer.check_apt_available('nonexistent')
        self.assertFalse(result)


class TestToolManager(unittest.TestCase):
    """Test ToolManager class."""
    
    def test_tools_dict_not_empty(self):
        """Test that TOOLS dictionary is populated."""
        self.assertGreater(len(dlt.ToolManager.TOOLS), 0)
    
    def test_tools_have_required_fields(self):
        """Test that all tools have required fields."""
        for dict_key, tool in dlt.ToolManager.TOOLS.items():
            self.assertIsInstance(tool, dlt.Tool)
            # Note: tool.name may differ from dict key (e.g., network-manager -> nmtui)
            self.assertIsNotNone(tool.name, f"Tool '{dict_key}' missing name")
            self.assertIsNotNone(tool.command, f"Tool '{dict_key}' missing command")
            self.assertIsNotNone(tool.method, f"Tool '{dict_key}' missing method")
            self.assertIsNotNone(tool.package, f"Tool '{dict_key}' missing package")
            self.assertIsNotNone(tool.description, f"Tool '{dict_key}' missing description")
            self.assertIsNotNone(tool.category, f"Tool '{dict_key}' missing category")
    
    def test_get_tools_by_category(self):
        """Test tools grouped by category."""
        categories = dlt.ToolManager.get_tools_by_category()
        self.assertIsInstance(categories, dict)
        self.assertGreater(len(categories), 0)
        
        # Check that all tools are in categories
        total_in_categories = sum(len(tools) for tools in categories.values())
        self.assertEqual(total_in_categories, len(dlt.ToolManager.TOOLS))
    
    @patch.object(dlt, 'shutil')
    def test_check_tool_installed_true(self, mock_shutil):
        """Test tool installation check when installed."""
        mock_shutil.which.return_value = '/usr/bin/vim'
        tool = dlt.ToolManager.TOOLS['vim']
        result = dlt.ToolManager.check_tool_installed(tool)
        self.assertTrue(result)
    
    @patch.object(dlt, 'shutil')
    def test_check_tool_installed_false(self, mock_shutil):
        """Test tool installation check when not installed."""
        mock_shutil.which.return_value = None
        tool = dlt.ToolManager.TOOLS['vim']
        result = dlt.ToolManager.check_tool_installed(tool)
        self.assertFalse(result)
    
    @patch.object(dlt.Installer, 'check_apt_available')
    @patch.object(dlt.Installer, 'install_via_apt')
    def test_install_tool_apt_success(self, mock_install, mock_check):
        """Test installing tool via apt."""
        mock_check.return_value = True
        mock_install.return_value = True
        tool = dlt.ToolManager.TOOLS['vim']
        result = dlt.ToolManager.install_tool(tool)
        self.assertTrue(result)
        mock_install.assert_called_once()
    
    @patch.object(dlt.Installer, 'check_apt_available')
    def test_install_tool_apt_not_available(self, mock_check):
        """Test installing tool via apt when not available."""
        mock_check.return_value = False
        tool = dlt.ToolManager.TOOLS['vim']
        result = dlt.ToolManager.install_tool(tool)
        self.assertFalse(result)
    
    @patch.object(dlt.Installer, 'install_via_pip')
    def test_install_tool_pip(self, mock_install):
        """Test installing tool via pip."""
        mock_install.return_value = True
        tool = dlt.ToolManager.TOOLS['glances']
        result = dlt.ToolManager.install_tool(tool)
        self.assertTrue(result)
        mock_install.assert_called_once()
    
    def test_install_tool_builtin(self):
        """Test builtin tool (no installation needed)."""
        tool = dlt.ToolManager.TOOLS['systemctl']
        result = dlt.ToolManager.install_tool(tool)
        self.assertTrue(result)  # Builtin tools always return True
    
    @patch.object(dlt.Installer, 'install_via_eget')
    @patch.object(dlt, 'shutil')
    def test_install_tool_eget(self, mock_shutil, mock_install):
        """Test installing tool via eget."""
        mock_shutil.which.return_value = '/usr/local/bin/eget'
        mock_install.return_value = True
        tool = dlt.ToolManager.TOOLS['lazygit']
        result = dlt.ToolManager.install_tool(tool)
        self.assertTrue(result)
        mock_install.assert_called_once()


class TestToolDataClass(unittest.TestCase):
    """Test Tool dataclass."""
    
    def test_tool_creation(self):
        """Test creating a Tool instance."""
        tool = dlt.Tool(
            name="test",
            command="test",
            method=dlt.InstallMethod.APT,
            package="test-pkg",
            description="Test tool",
            category="Test"
        )
        self.assertEqual(tool.name, "test")
        self.assertEqual(tool.method, dlt.InstallMethod.APT)
    
    def test_tool_defaults(self):
        """Test Tool default values."""
        tool = dlt.Tool(
            name="test",
            command="test",
            method=dlt.InstallMethod.APT,
            package="test",
            description="Test",
            category="Test"
        )
        self.assertTrue(tool.requires_root)  # Default should be True
        self.assertFalse(tool.classic)  # Default should be False
        self.assertIsNone(tool.github_repo)  # Default should be None


class TestGetUserConsent(unittest.TestCase):
    """Test get_user_consent function."""
    
    @patch('builtins.input')
    def test_get_user_consent_yes(self, mock_input):
        """Test user consent when user says yes."""
        mock_input.return_value = 'y'
        result = dlt.get_user_consent()
        self.assertTrue(result)
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_get_user_consent_no(self, mock_input):
        """Test user consent when user says no."""
        mock_input.return_value = 'n'
        result = dlt.get_user_consent()
        self.assertFalse(result)
        mock_input.assert_called_once()
    
    @patch('builtins.input')
    def test_get_user_consent_invalid_then_valid(self, mock_input):
        """Test user consent with invalid input then valid."""
        mock_input.side_effect = ['invalid', 'maybe', 'y']
        result = dlt.get_user_consent()
        self.assertTrue(result)
        self.assertEqual(mock_input.call_count, 3)
    
    @patch('builtins.input')
    def test_get_user_consent_max_attempts(self, mock_input):
        """Test user consent with max attempts reached."""
        mock_input.return_value = 'invalid'
        result = dlt.get_user_consent()
        self.assertFalse(result)
        # Should call input max_attempts times (5)
        self.assertEqual(mock_input.call_count, 5)
    
    @patch('builtins.input')
    def test_get_user_consent_keyboard_interrupt(self, mock_input):
        """Test user consent with keyboard interrupt."""
        mock_input.side_effect = KeyboardInterrupt()
        result = dlt.get_user_consent()
        self.assertFalse(result)


class TestMainFunction(unittest.TestCase):
    """Test main function logic - simplified to avoid infinite loops and real execution."""
    
    @patch.object(dlt.SystemChecker, 'check_system')
    def test_main_system_check_fails(self, mock_check):
        """Test main when system check fails."""
        mock_check.return_value = (False, "System not compatible")
        # Mock sys.exit to prevent actual exit and raise SystemExit instead
        with patch('sys.exit', side_effect=SystemExit(1)) as mock_exit, \
             patch('sys.stderr'), \
             patch('builtins.print'):
            with self.assertRaises(SystemExit) as cm:
                dlt.main()
            self.assertEqual(cm.exception.code, 1)
        # Verify check_system was called
        mock_check.assert_called_once()
    
    @patch('builtins.input')
    @patch.object(dlt, 'get_user_consent')
    @patch.object(dlt.SystemChecker, 'check_system')
    @patch.object(dlt.SystemChecker, 'is_root', return_value=True)
    def test_main_user_declines(self, mock_is_root, mock_check, mock_consent, mock_input):
        """Test main when user declines installation."""
        mock_check.return_value = (True, None)
        mock_consent.return_value = False  # User declines
        mock_input.return_value = ''  # Final input if it gets there
        with patch('sys.exit', side_effect=SystemExit(0)) as mock_exit, \
             patch('builtins.print'):
            with self.assertRaises(SystemExit) as cm:
                dlt.main()
            self.assertEqual(cm.exception.code, 0)
    
    @patch('builtins.input')
    @patch.object(dlt, 'update_package_lists')
    @patch.object(dlt, 'get_user_consent')
    @patch.object(dlt.SystemChecker, 'check_system')
    @patch.object(dlt.SystemChecker, 'is_root', return_value=True)
    @patch.object(dlt.ToolManager, 'get_tools_by_category')
    @patch.object(dlt.ToolManager, 'check_tool_installed')
    @patch.object(dlt.ToolManager, 'install_tool')
    @patch('builtins.print')  # Suppress print output
    def test_main_success_flow(self, mock_print, mock_install, mock_check_installed,
                                mock_get_categories, mock_is_root, mock_sys_check,
                                mock_consent, mock_update, mock_input):
        """Test successful main execution flow."""
        mock_sys_check.return_value = (True, None)
        mock_consent.return_value = True  # User accepts
        mock_update.return_value = True
        mock_input.return_value = ''  # Final "Press Enter"
        
        # Setup mock categories - use empty dict to speed up test
        mock_get_categories.return_value = {}
        mock_check_installed.return_value = False
        mock_install.return_value = True
        
        with patch('sys.exit', side_effect=SystemExit(0)):
            with self.assertRaises(SystemExit) as cm:
                dlt.main()
            self.assertEqual(cm.exception.code, 0)
        # Should call input once for final "Press Enter"
        self.assertEqual(mock_input.call_count, 1)


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
