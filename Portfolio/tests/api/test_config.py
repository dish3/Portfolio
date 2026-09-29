"""
Test Suite for Backend Configuration Management.
"""

from apps.api.app.core.config import Settings


def test_configuration_defaults() -> None:
    """Tests that default settings initialize without error and match project spec."""
    cfg = Settings()
    assert cfg.PROJECT_NAME == "NOVA"
    assert cfg.EMBEDDING_DIMENSION == 768
    assert cfg.GEMINI_MODEL == "gemini-2.5-flash"
    assert cfg.GEMINI_FAST_MODEL == "gemini-2.5-flash-lite"


def test_cors_origins_parsing() -> None:
    """Tests CORS origin string-to-list parsing."""
    cfg = Settings(CORS_ORIGINS="http://localhost:3000, https://portfolio.vercel.app")
    assert "http://localhost:3000" in cfg.CORS_ORIGINS
    assert "https://portfolio.vercel.app" in cfg.CORS_ORIGINS


def test_free_tier_constraints() -> None:
    """Verifies that default Gemini model selection complies with free-tier rules."""
    cfg = Settings()
    # Spec forbids assuming Pro models are free tier
    assert "pro" not in cfg.GEMINI_MODEL.lower()
    assert "pro" not in cfg.GEMINI_FAST_MODEL.lower()
