# Solar Rooftop Analysis Tool - Deployment Guide

## Hugging Face Spaces Deployment

This application is designed to be deployed on Hugging Face Spaces using Streamlit.

### Quick Deploy to Hugging Face Spaces

1. **Create a new Space on Hugging Face:**
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose "Streamlit" as the SDK
   - Set visibility to "Public" or "Private"

2. **Upload files:**
   - Upload all files from this repository
   - Make sure to include the `requirements.txt` and `packages.txt`

3. **Set Environment Variables:**
   - In your Space settings, add:
   - `OPENROUTER_API_KEY` = your OpenRouter API key

4. **The Space will automatically build and deploy**

### Required Files for Deployment

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `packages.txt` - System packages (for image processing)
- All Python modules (`solar_analyzer.py`, `solar_calculations.py`, etc.)

### Environment Variables

Set these in your Hugging Face Space settings:

```
OPENROUTER_API_KEY=your_openrouter_api_key_here
```

### Demo Mode

The application includes a demo mode that works without API keys, showing sample analysis results.

### Features

- AI-powered rooftop analysis using satellite imagery
- Solar panel layout optimization
- Energy production calculations
- Financial analysis and ROI projections
- Interactive charts and reporting
- Export capabilities (JSON, CSV)

### Support

For issues or questions, please check the main README.md file or create an issue in the repository.
