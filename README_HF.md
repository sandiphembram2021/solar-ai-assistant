---
title: Solar Rooftop Analysis Tool
emoji: ☀️
colorFrom: orange
colorTo: yellow
sdk: streamlit
sdk_version: 1.29.0
app_file: app.py
pinned: false
license: mit
---

# Solar Rooftop Analysis Tool

An AI-powered rooftop analysis tool that uses satellite imagery to assess solar installation potential. This application integrates multiple AI services to provide accurate solar potential assessments, installation recommendations, and ROI estimates for both homeowners and solar professionals.

## Features

- **AI-Powered Analysis**: Uses OpenRouter API with Claude 3.5 Sonnet for vision analysis
- **Comprehensive Assessment**: Roof area, shape, material, and condition analysis
- **Solar Panel Layout**: Optimal placement with obstruction consideration
- **Energy Production**: Location-based solar irradiance calculations
- **Financial Modeling**: 25-year ROI projections with tax incentives
- **Professional Reporting**: Interactive charts and exportable data

## How to Use

1. **Upload Image**: Upload a satellite or aerial rooftop image
2. **Configure Settings**: Set location, panel type, and analysis parameters
3. **Run Analysis**: Click "Analyze Rooftop" for AI-powered assessment
4. **View Results**: Check results and detailed reports with charts
5. **Export Data**: Download JSON reports and CSV financial projections

## Demo Mode

The application includes a demo mode that works without API configuration, showing realistic sample analysis results.

## Configuration

For full AI functionality, you need an OpenRouter API key. The application will work in demo mode without it.

## Technical Details

- **Frontend**: Streamlit web interface
- **AI Integration**: OpenRouter API with Claude 3.5 Sonnet
- **Calculations**: Custom solar energy and financial modeling
- **Visualizations**: Plotly interactive charts
- **Export**: JSON and CSV formats

## Requirements

See `requirements.txt` for Python dependencies and `packages.txt` for system packages.

## License

MIT License - see LICENSE file for details.

---

*Developed for Solar Industry AI Assistant Assessment*
