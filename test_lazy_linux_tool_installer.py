#!/usr/bin/env python3
"""
Test suite for Lazy-Linux-Tool-Installer.py
Non-invasive tests using mocks to avoid actual system modifications.
Platform-independent - works on Mac, Linux, and Windows.
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, call
import sys
import os
import subprocess
import shutil
import io
import json
import contextlib
import urllib.request
import urllib.error

# Import the module to test (handle hyphen in filename)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location(
    "lazy_linux_tool_installer",
    os.path.join(os.path.dirname(__file__), "Lazy-Linux-Tool-Installer.py")
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
            elif cmd == 'curl':
                return '/usr/bin/curl'
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
            elif cmd == 'curl':
                return '/usr/bin/curl'
            return None
        mock_shutil.which.side_effect = which_side_effect
        is_compatible, error = dlt.SystemChecker.check_system()
        self.assertFalse(is_compatible)
        self.assertIsNotNone(error)
        self.assertIn('sudo', error)

    @patch.object(dlt, 'shutil')
    def test_check_system_no_curl(self, mock_shutil):
        """Test system check when curl is missing."""
        def which_side_effect(cmd):
            if cmd == 'apt-get':
                return '/usr/bin/apt-get'
            elif cmd == 'sudo':
                return '/usr/bin/sudo'
            elif cmd == 'curl':
                return None
            return None
        mock_shutil.which.side_effect = which_side_effect
        is_compatible, error = dlt.SystemChecker.check_system()
        self.assertFalse(is_compatible)
        self.assertIsNotNone(error)
        self.assertIn('curl', error)


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
    def test_run_command_called_process_error(self, mock_run):
        """Test command execution when CalledProcessError is raised."""
        error = subprocess.CalledProcessError(5, ['test', 'cmd'])
        mock_run.side_effect = error
        with patch('builtins.print'):  # Suppress print output
            result = dlt.Installer.run_command(['test', 'cmd'])
        self.assertEqual(result.returncode, 5)  # Should return the error's return code
        self.assertIsInstance(result, subprocess.CompletedProcess)
    
    @patch.object(dlt.subprocess, 'run')
    def test_run_command_file_not_found(self, mock_run):
        """Test command execution when command not found."""
        mock_run.side_effect = FileNotFoundError("Command not found")
        with patch('builtins.print'):  # Suppress print output
            result = dlt.Installer.run_command(['nonexistent'])
        self.assertEqual(result.returncode, 127)  # Standard exit code for command not found
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
    @patch.object(dlt, 'shutil')
    def test_install_via_npm_success(self, mock_shutil, mock_subprocess):
        """npm already present: install the package globally."""
        mock_shutil.which.return_value = '/usr/bin/npm'
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sudo'], 0)
        self.assertTrue(dlt.Installer.install_via_npm('neoss'))
        self.assertIn('timeout', mock_subprocess.run.call_args[1])

    @patch.object(dlt.Installer, 'install_via_apt')
    @patch.object(dlt, 'subprocess')
    @patch.object(dlt, 'shutil')
    def test_install_via_npm_bootstraps_npm(self, mock_shutil, mock_subprocess, mock_apt):
        """npm missing: apt-install npm first rather than failing with 'not found'."""
        mock_shutil.which.return_value = None
        mock_apt.return_value = True
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['sudo'], 0)
        self.assertTrue(dlt.Installer.install_via_npm('neoss'))
        mock_apt.assert_called_once_with('npm')

    @patch.object(dlt.Installer, 'install_via_apt')
    @patch.object(dlt, 'shutil')
    def test_install_via_npm_gives_up_if_npm_unavailable(self, mock_shutil, mock_apt):
        """If npm cannot be installed, report failure instead of pressing on."""
        mock_shutil.which.return_value = None
        mock_apt.return_value = False
        self.assertFalse(dlt.Installer.install_via_npm('neoss'))

    @patch.object(dlt.Installer, 'install_binary_to_path')
    @patch.object(dlt, 'subprocess')
    @patch.object(dlt, 'os')
    @patch.object(dlt, 'shutil')
    def test_install_via_eget_success(self, mock_shutil, mock_os, mock_subprocess, mock_install_bin):
        """Test successful eget installation."""
        mock_shutil.which.return_value = '/usr/local/bin/eget'
        mock_subprocess.run.return_value = subprocess.CompletedProcess(['eget'], 0)
        mock_os.path.exists.return_value = True
        mock_install_bin.return_value = True
        
        result = dlt.Installer.install_via_eget('sharkdp/bat', 'bat')
        self.assertTrue(result)
        mock_install_bin.assert_called_once_with('bat', 'bat')
        # Verify timeout is set for network operations
        call_kwargs = mock_subprocess.run.call_args[1]
        self.assertIn('timeout', call_kwargs)
        self.assertGreaterEqual(call_kwargs['timeout'], 30)

    @patch.object(dlt.Installer, 'install_eget')
    @patch.object(dlt, 'subprocess')
    @patch.object(dlt, 'os')
    @patch.object(dlt, 'shutil')
    def test_install_via_eget_no_eget(self, mock_shutil, mock_os, mock_subprocess, mock_install_eget):
        """Test eget installation when eget is not installed."""
        mock_shutil.which.return_value = None
        mock_install_eget.return_value = False
        
        result = dlt.Installer.install_via_eget('sharkdp/bat', 'bat')
        self.assertFalse(result)
        mock_install_eget.assert_called_once()

    def test_parse_checksums_file(self):
        """Test checksum file parsing."""
        content = "abc123  foo.tar.gz\ndef456 *bar.tar.gz\n"
        mapping = dlt.Installer.parse_checksums_file(content)
        self.assertEqual(mapping['foo.tar.gz'], 'abc123')
        self.assertEqual(mapping['bar.tar.gz'], 'def456')

    def test_is_plausible_binary_rejects_missing(self):
        """Test binary sanity check rejects missing paths."""
        self.assertFalse(dlt.Installer.is_plausible_binary('/tmp/definitely-missing-linux-tools-bin'))

    def test_no_curl_pipe_to_shell_in_installer_source(self):
        """Guard against reintroducing curl|sh / curl|bash bootstrap."""
        source_path = os.path.join(os.path.dirname(__file__), 'Lazy-Linux-Tool-Installer.py')
        with open(source_path, encoding='utf-8') as handle:
            source = handle.read()
        self.assertNotIn('| sh', source)
        self.assertNotIn('| bash', source)
        self.assertNotIn('getcroc.schollz.com', source)
        self.assertNotIn('eget.sh |', source)
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
    
    @patch.object(dlt, 'shutil')
    @patch.object(dlt.Installer, 'check_apt_available')
    @patch.object(dlt.Installer, 'install_via_apt')
    def test_install_tool_apt_success(self, mock_install, mock_check, mock_shutil):
        """Test installing tool via apt."""
        mock_check.return_value = True
        mock_install.return_value = True
        mock_shutil.which.return_value = '/usr/bin/vim'
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
    
    @patch.object(dlt, 'shutil')
    @patch.object(dlt.Installer, 'install_via_pip')
    def test_install_tool_pip(self, mock_install, mock_shutil):
        """Test installing tool via pip."""
        mock_install.return_value = True
        mock_shutil.which.return_value = '/usr/bin/glances'
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

    @patch.object(dlt.Installer, 'install_via_npm')
    @patch.object(dlt, 'shutil')
    def test_install_tool_npm(self, mock_shutil, mock_install):
        """Test installing tool via npm."""
        mock_shutil.which.return_value = '/usr/local/bin/neoss'
        mock_install.return_value = True
        tool = dlt.ToolManager.TOOLS['neoss']
        self.assertTrue(dlt.ToolManager.install_tool(tool))
        mock_install.assert_called_once_with('neoss')

    def test_every_method_is_handled_by_install_tool(self):
        """Every InstallMethod a tool actually uses must have a dry-run branch.

        Adding an enum member without wiring it up would otherwise leave the
        tool silently unhandled, which is how neoss and eg went unnoticed.
        """
        used = {t.method for t in dlt.ToolManager.TOOLS.values()}
        for method in used:
            with self.subTest(method=method.value):
                tool = next(t for t in dlt.ToolManager.TOOLS.values() if t.method == method)
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    handled = dlt.ToolManager.install_tool(tool, dry_run=True)
                self.assertTrue(handled)
                self.assertTrue(buf.getvalue().strip(),
                                f"{method.value} produced no dry-run output")

    def test_eget_tools_declare_a_repo_and_others_do_not(self):
        """A github_repo is required for eget and meaningless for anything else."""
        for name, tool in dlt.ToolManager.TOOLS.items():
            with self.subTest(tool=name):
                if tool.method == dlt.InstallMethod.EGET:
                    self.assertTrue(tool.github_repo,
                                    f"{name} installs via eget but names no repo")
                else:
                    self.assertIsNone(tool.github_repo,
                                      f"{name} does not use eget but names a repo")


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

    def setUp(self):
        # Keep argparse from choking on unittest CLI args (e.g. python -m unittest ...)
        self._argv_patcher = patch.object(sys, 'argv', ['Lazy-Linux-Tool-Installer.py'])
        self._argv_patcher.start()

    def tearDown(self):
        self._argv_patcher.stop()
    
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


@unittest.skipUnless(
    os.environ.get("LINUX_TOOLS_NETWORK_TESTS") == "1",
    "network test; set LINUX_TOOLS_NETWORK_TESTS=1 to run",
)
class TestEgetToolsResolveUpstream(unittest.TestCase):
    """Ask GitHub whether every eget tool can still actually be fetched.

    The mocked tests above prove the installer calls eget correctly. They
    cannot prove eget will find anything at the other end, and that is the
    failure that reached users: neoss stopped attaching release assets when it
    moved to npm, and eg never cut a GitHub release at all. Both were declared
    as eget tools for a long time, and both failed only at install time on a
    real machine.

    This test is off by default because it needs the network and spends
    GitHub's unauthenticated rate limit. Set GITHUB_TOKEN to raise that limit.
    """

    # Files that mention Linux but are not something eget can install: update
    # manifests, checksums, signatures, and distro packages it will not unpack.
    NON_BINARY_SUFFIXES = (
        ".yml", ".yaml", ".json", ".txt", ".md", ".sha256", ".sha256sum",
        ".sig", ".asc", ".pem", ".sbom", ".deb", ".rpm",
    )

    @classmethod
    def _usable_linux_asset(cls, asset_name: str) -> bool:
        lowered = asset_name.lower()
        return "linux" in lowered and not lowered.endswith(cls.NON_BINARY_SUFFIXES)

    def _get(self, url: str) -> dict:
        headers = {
            "User-Agent": "Linux-Tools-test",
            "Accept": "application/vnd.github+json",
        }
        token = os.environ.get("GITHUB_TOKEN")
        if token:
            headers["Authorization"] = f"Bearer {token}"
        request = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(request, timeout=30) as response:
            return json.load(response)

    def _require_api_budget(self, needed: int) -> None:
        """Skip before starting rather than half-checking the list.

        Anonymous callers get sixty requests an hour, which one run can
        exhaust. Discovering that partway through would leave most tools
        unchecked while the run still reported success, so establish up front
        that the whole sweep can complete.
        """
        try:
            rate = self._get("https://api.github.com/rate_limit")["rate"]
        except urllib.error.URLError as error:
            raise unittest.SkipTest(f"network unavailable: {error.reason}")
        if rate["remaining"] < needed:
            raise unittest.SkipTest(
                f"GitHub API budget too low: {rate['remaining']} left, {needed} "
                f"needed. Set GITHUB_TOKEN (export GITHUB_TOKEN=$(gh auth token))."
            )

    def test_every_eget_tool_resolves_to_a_downloadable_asset(self):
        eget_tools = {
            name: tool.github_repo
            for name, tool in dlt.ToolManager.TOOLS.items()
            if tool.method == dlt.InstallMethod.EGET
        }
        self.assertTrue(eget_tools, "expected the installer to define eget tools")
        self._require_api_budget(len(eget_tools))

        failures = []
        for name, repo in sorted(eget_tools.items()):
            try:
                release = self._get(
                    f"https://api.github.com/repos/{repo}/releases/latest"
                )
            except urllib.error.HTTPError as error:
                if error.code in (403, 429):
                    raise unittest.SkipTest(
                        f"rate limited after checking {len(failures)} tools; "
                        f"set GITHUB_TOKEN and rerun"
                    )
                failures.append(
                    f"{name}: no published release at {repo} (HTTP {error.code}), "
                    f"so eget has nothing to download"
                )
                continue
            except urllib.error.URLError as error:
                raise unittest.SkipTest(f"network unavailable: {error.reason}")

            assets = [asset["name"] for asset in release.get("assets", [])]
            if not [a for a in assets if self._usable_linux_asset(a)]:
                failures.append(
                    f"{name}: {repo} release {release.get('tag_name')!r} publishes "
                    f"no Linux binary eget can install (assets: {assets or 'none'})"
                )

        self.assertEqual(
            [], failures,
            "eget tools that cannot actually be installed:\n  "
            + "\n  ".join(failures),
        )


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)
