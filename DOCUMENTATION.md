# 📚 Solar Rooftop Analysis Tool - Technical Documentation

## 🏗️ Architecture Overview

### System Components

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   OpenRouter    │    │   Solar         │
│   Frontend      │◄──►│   API           │    │   Calculations  │
│                 │    │   (Vision AI)   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Image         │    │   Roof          │    │   Financial     │
│   Processing    │    │   Analysis      │    │   Modeling      │
│                 │    │                 │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         └───────────────────────┼───────────────────────┘
                                 ▼
                    ┌─────────────────┐
                    │   Report        │
                    │   Generation    │
                    │                 │
                    └─────────────────┘
```

### Data Flow

1. **Image Upload**: User uploads satellite/aerial rooftop image
2. **AI Analysis**: OpenRouter API processes image with vision model
3. **Data Extraction**: Structured roof characteristics extracted
4. **Panel Layout**: Optimal solar panel placement calculated
5. **Energy Modeling**: Production estimates based on location/orientation
6. **Financial Analysis**: Cost, savings, and ROI calculations
7. **Report Generation**: Comprehensive analysis with visualizations

## 🔧 Module Documentation

### `config.py`
**Purpose**: Central configuration management

**Key Components**:
- API configuration (OpenRouter settings)
- Solar panel specifications (3 types)
- Installation cost parameters
- Financial modeling constants
- Geographic defaults
- Analysis parameters

**Configuration Categories**:
```python
{
    "api": {...},           # API settings
    "solar_panels": {...},  # Panel specifications
    "installation": {...},  # Installation costs
    "financial": {...},     # Financial parameters
    "analysis": {...},      # Analysis settings
    "report": {...}         # Report configuration
}
```

### `solar_analyzer.py`
**Purpose**: AI-powered rooftop analysis using vision models

**Key Classes**:
- `SolarRooftopAnalyzer`: Main analysis class

**Key Methods**:
- `analyze_rooftop_structure()`: AI vision analysis of rooftop
- `estimate_panel_layout()`: Calculate optimal panel placement
- `encode_image()`: Convert PIL Image to base64

**AI Integration**:
- Uses Claude 3.5 Sonnet via OpenRouter API
- Structured JSON prompt engineering
- Fallback mechanisms for API failures
- Confidence scoring for results

### `solar_calculations.py`
**Purpose**: Solar energy and financial calculations

**Key Classes**:
- `SolarCalculations`: Energy and financial modeling

**Key Methods**:
- `calculate_solar_irradiance()`: Location-based solar irradiance
- `calculate_energy_production()`: Annual energy estimates
- `calculate_financial_analysis()`: ROI and cost analysis
- `get_system_recommendations()`: Generate recommendations

**Calculation Models**:
- Solar irradiance based on latitude/orientation
- System efficiency factors (inverter, wiring, soiling)
- 25-year financial projections with degradation
- NPV and IRR calculations

### `report_generator.py`
**Purpose**: Comprehensive report generation and visualization

**Key Classes**:
- `SolarReportGenerator`: Report and chart generation

**Key Methods**:
- `generate_executive_summary()`: Executive summary text
- `create_*_chart()`: Various visualization methods
- `generate_detailed_report()`: Full Streamlit report
- `export_report_data()`: Data export functionality

**Visualizations**:
- Roof area breakdown (pie chart)
- Monthly energy production (bar chart)
- Financial projections (line chart)
- Shading impact analysis (bar chart)

### `app.py`
**Purpose**: Main Streamlit application interface

**Key Functions**:
- `main()`: Primary application flow
- `analyze_rooftop()`: Orchestrate complete analysis
- `display_results()`: Show analysis results
- `generate_report()`: Create comprehensive report

**UI Components**:
- Image upload interface
- Configuration sidebar
- Tabbed results display
- Interactive charts and metrics

## 🧮 Technical Algorithms

### Solar Irradiance Calculation

```python
def calculate_solar_irradiance(tilt, azimuth):
    base_irradiance = get_base_irradiance_for_location()
    
    # Tilt optimization (optimal ≈ latitude)
    tilt_factor = cos(|tilt - latitude|) * 0.9 + 0.1
    
    # Azimuth optimization (180° = south is optimal)
    azimuth_factor = cos(|azimuth - 180°|) * 0.8 + 0.2
    
    return base_irradiance * tilt_factor * azimuth_factor
```

### Panel Layout Optimization

```python
def estimate_panel_layout(roof_analysis):
    usable_area = roof_analysis["usable_area_sqm"]
    
    # Apply spacing factor (15% reduction)
    effective_area = usable_area * 0.85
    
    # Calculate maximum panels
    max_panels = effective_area / panel_area
    
    # Reduce for obstructions
    obstruction_impact = count_obstructions() * 2.5
    
    # Apply shading reduction
    shading_factor = get_shading_factor(shading_level)
    
    final_panels = (max_panels - obstruction_impact) * shading_factor
    
    return final_panels
```

### Financial Modeling

```python
def calculate_25_year_projection():
    for year in range(1, 26):
        # Account for electricity rate increases
        year_rate = base_rate * (1 + rate_increase) ** (year - 1)
        
        # Account for system degradation
        year_production = base_production * (1 - degradation) ** (year - 1)
        
        # Calculate annual savings
        year_savings = year_production * year_rate
        
        # NPV calculation
        npv += year_savings / (1 + discount_rate) ** year
```

## 🎨 Prompt Engineering

### Vision Analysis Prompt Structure

The AI vision analysis uses carefully crafted prompts to extract structured data:

```
Analyze this satellite/aerial image of a rooftop for solar panel installation potential.
Provide a detailed JSON response with the following structure:

{
    "roof_analysis": {
        "roof_area_sqm": <estimated total roof area>,
        "usable_area_sqm": <area suitable for solar panels>,
        "roof_shape": "<rectangular/L-shaped/complex/irregular>",
        ...
    },
    "orientation_analysis": {...},
    "obstructions": {...},
    "shading_analysis": {...},
    "access_and_installation": {...},
    "solar_suitability": {...}
}
```

**Key Prompt Engineering Techniques**:
- Structured JSON output specification
- Specific value ranges and options
- Clear measurement units
- Confidence scoring requirements
- Fallback handling instructions

## 📊 Data Models

### Roof Analysis Data Structure

```python
roof_analysis = {
    "roof_analysis": {
        "roof_area_sqm": float,
        "usable_area_sqm": float,
        "roof_shape": str,
        "roof_material": str,
        "roof_condition": str,
        "roof_age_estimate": str
    },
    "orientation_analysis": {
        "primary_roof_direction": str,
        "roof_tilt_estimate": int,
        "multiple_orientations": bool,
        "optimal_sections": List[str]
    },
    "obstructions": {
        "chimneys": int,
        "vents": int,
        "skylights": int,
        "hvac_units": int,
        "satellite_dishes": int,
        "other_obstructions": List[str]
    },
    "shading_analysis": {
        "nearby_trees": str,
        "neighboring_buildings": str,
        "self_shading": str,
        "overall_shading_impact": str
    },
    "solar_suitability": {
        "overall_rating": str,
        "confidence_score": float,
        "key_advantages": List[str],
        "key_challenges": List[str],
        "recommendations": List[str]
    }
}
```

### Financial Analysis Data Structure

```python
financial_analysis = {
    "costs": {
        "equipment_cost": float,
        "installation_cost": float,
        "total_cost": float,
        "federal_tax_credit": float,
        "net_cost": float,
        "cost_per_watt": float
    },
    "savings": {
        "annual_savings": float,
        "monthly_savings": float,
        "lifetime_savings": float,
        "simple_payback_years": float
    },
    "returns": {
        "npv": float,
        "irr": float,
        "roi_25_year": float
    },
    "cash_flow_projection": List[{
        "year": int,
        "production_kwh": float,
        "electricity_rate": float,
        "annual_savings": float,
        "cumulative_savings": float,
        "net_benefit": float
    }]
}
```

## 🔒 Error Handling

### API Error Handling
- Retry mechanisms for transient failures
- Fallback to default analysis if API unavailable
- Graceful degradation of functionality
- User-friendly error messages

### Data Validation
- Input validation for uploaded images
- Configuration parameter validation
- Calculation result sanity checks
- JSON parsing error handling

### User Experience
- Progress indicators during analysis
- Clear error messages with solutions
- Fallback demo mode without API
- Comprehensive logging for debugging

## 🚀 Performance Optimization

### Image Processing
- Image compression before API calls
- Optimal image format conversion
- Size limits to prevent timeouts
- Efficient base64 encoding

### Calculation Efficiency
- Vectorized operations with NumPy
- Cached configuration loading
- Optimized financial projections
- Minimal redundant calculations

### UI Responsiveness
- Asynchronous API calls
- Progress indicators
- Lazy loading of visualizations
- Efficient state management

## 🧪 Testing Strategy

### Unit Tests
- Individual function testing
- Mock API responses
- Edge case validation
- Configuration testing

### Integration Tests
- End-to-end workflow testing
- API integration validation
- Data flow verification
- Error handling testing

### User Acceptance Tests
- Real image analysis
- Complete workflow validation
- Performance benchmarking
- Usability testing

## 📈 Future Enhancements

### Technical Improvements
- 3D roof modeling capabilities
- Real-time satellite data integration
- Advanced shading calculations
- Machine learning model training

### Feature Additions
- Multiple roof section analysis
- Battery storage integration
- Grid tie analysis
- Maintenance scheduling

### Professional Features
- CAD drawing export
- Permit application automation
- Installer network integration
- Performance monitoring dashboard
