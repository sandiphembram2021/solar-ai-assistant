"""
Configuration settings for the Solar Rooftop Analysis Tool
"""
import os
from typing import Dict, Any

# API Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Vision Model Configuration
VISION_MODEL = "anthropic/claude-3.5-sonnet"  # High-quality vision model
BACKUP_VISION_MODEL = "openai/gpt-4-vision-preview"

# Solar Panel Specifications
SOLAR_PANEL_SPECS = {
    "standard_residential": {
        "power_rating": 400,  # Watts
        "efficiency": 0.20,   # 20%
        "width": 1.65,        # meters
        "height": 1.00,       # meters
        "area": 1.65,         # square meters
        "cost_per_watt": 3.50 # USD per watt installed
    },
    "high_efficiency": {
        "power_rating": 450,  # Watts
        "efficiency": 0.22,   # 22%
        "width": 1.65,        # meters
        "height": 1.00,       # meters
        "area": 1.65,         # square meters
        "cost_per_watt": 4.00 # USD per watt installed
    },
    "premium": {
        "power_rating": 500,  # Watts
        "efficiency": 0.24,   # 24%
        "width": 1.65,        # meters
        "height": 1.00,       # meters
        "area": 1.65,         # square meters
        "cost_per_watt": 4.50 # USD per watt installed
    }
}

# Installation Costs (USD)
INSTALLATION_COSTS = {
    "base_cost_per_watt": 1.50,
    "inverter_cost_per_watt": 0.30,
    "electrical_cost": 2000,
    "permit_cost": 500,
    "inspection_cost": 300,
    "labor_cost_per_hour": 75,
    "estimated_install_hours_per_kw": 8
}

# Financial Parameters
FINANCIAL_PARAMS = {
    "federal_tax_credit": 0.30,  # 30% federal tax credit
    "average_electricity_rate": 0.13,  # USD per kWh
    "annual_rate_increase": 0.03,  # 3% annual increase
    "system_degradation": 0.005,  # 0.5% annual degradation
    "warranty_years": 25,
    "discount_rate": 0.06  # 6% discount rate for NPV
}

# Geographic and Weather Defaults
DEFAULT_LOCATION = {
    "latitude": 37.7749,   # San Francisco
    "longitude": -122.4194,
    "timezone": "America/Los_Angeles"
}

# Analysis Parameters
ANALYSIS_PARAMS = {
    "min_roof_area": 20,      # Minimum roof area in sq meters
    "panel_spacing": 0.5,     # Spacing between panels in meters
    "edge_setback": 1.0,      # Setback from roof edges in meters
    "obstruction_buffer": 2.0, # Buffer around obstructions in meters
    "min_tilt_angle": 10,     # Minimum roof tilt for solar
    "max_tilt_angle": 60,     # Maximum roof tilt for solar
    "optimal_azimuth": 180,   # South-facing (degrees)
    "azimuth_tolerance": 45   # Acceptable deviation from south
}

# Shading Analysis
SHADING_PARAMS = {
    "tree_height_estimate": 8,    # Average tree height in meters
    "building_height_estimate": 6, # Average building height in meters
    "shadow_factor_threshold": 0.8 # Minimum acceptable solar access
}

# Report Configuration
REPORT_CONFIG = {
    "currency_symbol": "$",
    "energy_unit": "kWh",
    "power_unit": "kW",
    "area_unit": "sq ft",
    "include_monthly_breakdown": True,
    "include_seasonal_analysis": True,
    "include_financial_projections": True
}

# Streamlit Configuration
STREAMLIT_CONFIG = {
    "page_title": "Solar Rooftop Analysis Tool",
    "page_icon": "☀️",
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

# Image Processing
IMAGE_CONFIG = {
    "max_upload_size": 10,  # MB
    "supported_formats": ["jpg", "jpeg", "png", "tiff"],
    "max_resolution": (4096, 4096),
    "compression_quality": 85
}

def get_config() -> Dict[str, Any]:
    """Return complete configuration dictionary"""
    return {
        "api": {
            "openrouter_key": OPENROUTER_API_KEY,
            "base_url": OPENROUTER_BASE_URL,
            "vision_model": VISION_MODEL,
            "backup_model": BACKUP_VISION_MODEL
        },
        "solar_panels": SOLAR_PANEL_SPECS,
        "installation": INSTALLATION_COSTS,
        "financial": FINANCIAL_PARAMS,
        "location": DEFAULT_LOCATION,
        "analysis": ANALYSIS_PARAMS,
        "shading": SHADING_PARAMS,
        "report": REPORT_CONFIG,
        "streamlit": STREAMLIT_CONFIG,
        "image": IMAGE_CONFIG
    }

def validate_config() -> bool:
    """Validate that required configuration is present"""
    if not OPENROUTER_API_KEY:
        return False
    return True
