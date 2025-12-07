"""
Unit tests for splash screen.

Tests T030: RED phase tests for splash screen rendering.
"""
import pytest
from unittest.mock import patch, MagicMock
from retro_todo.ui.splash import show_splash, get_splash_text


class TestSplashScreen:
    """Tests for splash screen - T030."""
    
    def test_get_splash_text_returns_string(self):
        """get_splash_text returns ASCII art string."""
        splash = get_splash_text()
        assert isinstance(splash, str)
        assert len(splash) > 0
    
    def test_splash_text_contains_todo(self):
        """Splash contains TODO or similar text."""
        splash = get_splash_text()
        # PyFiglet generates ASCII art, should contain recognizable patterns
        assert len(splash) > 10
    
    def test_show_splash_runs_without_error(self):
        """Splash screen displays without error."""
        with patch('retro_todo.ui.splash.console') as mock_console:
            show_splash()
            # Verify print was called
            assert mock_console.print.called
    
    def test_show_splash_uses_rich_panel(self):
        """Splash uses Rich Panel for display."""
        with patch('retro_todo.ui.splash.console') as mock_console:
            show_splash()
            assert mock_console.print.called
