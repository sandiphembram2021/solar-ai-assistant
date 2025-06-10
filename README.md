# ☀️ Solar Rooftop Analysis Tool

An AI-powered rooftop analysis tool that uses satellite imagery to assess solar installation potential. This project integrates multiple AI services to provide accurate solar potential assessments, installation recommendations, and ROI estimates for both homeowners and solar professionals.

## 🎯 Project Overview

This tool analyzes rooftop satellite/aerial imagery to provide comprehensive solar installation assessments including:

- **Rooftop Structure Analysis**: AI-powered detection of roof area, shape, material, and condition
- **Obstruction Detection**: Identification of chimneys, vents, HVAC units, and other obstacles
- **Shading Analysis**: Assessment of nearby trees, buildings, and shadow impacts
- **Solar Panel Layout**: Optimal panel placement and system sizing
- **Energy Production Estimates**: Annual and monthly energy generation forecasts
- **Financial Analysis**: Cost estimates, ROI calculations, and 25-year projections
- **Regulatory Compliance**: Consideration of local codes and requirements

## 🚀 Features

### AI-Powered Analysis
- **Vision AI Integration**: Uses OpenRouter API with Claude 3.5 Sonnet for image analysis
- **Structured Output**: Extracts detailed rooftop characteristics from satellite imagery
- **Confidence Scoring**: Provides reliability metrics for analysis results

### Comprehensive Assessment
- **Multiple Panel Types**: Standard, high-efficiency, and premium solar panels
- **Location-Based Calculations**: Solar irradiance based on geographic coordinates
- **Shading Impact**: Detailed analysis of shading sources and mitigation strategies
- **Installation Complexity**: Assessment of accessibility and structural considerations

### Financial Modeling
- **Cost Breakdown**: Equipment, installation, permits, and labor costs
- **Incentive Calculations**: Federal tax credits and local rebates
- **ROI Analysis**: Payback period, NPV, and IRR calculations
- **25-Year Projections**: Long-term financial performance modeling

### Professional Reporting
- **Interactive Visualizations**: Charts and graphs for energy and financial data
- **Executive Summary**: Key findings and recommendations
- **Detailed Reports**: Comprehensive analysis with technical specifications
- **Export Options**: JSON and CSV data export for further analysis

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- OpenRouter API key (get from [openrouter.ai](https://openrouter.ai/))

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd solar_ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env file and add your OpenRouter API key
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. **Open in browser**
   - The application will open automatically at `http://localhost:8501`

## 📖 Usage Guide

### 1. Upload Image
- Upload a clear satellite or aerial image of the rooftop
- Supported formats: JPG, JPEG, PNG, TIFF
- Ensure good resolution and minimal cloud cover

### 2. Configure Parameters
- **Location**: Set latitude and longitude coordinates
- **Panel Type**: Choose from standard, high-efficiency, or premium panels
- **Electricity Rate**: Enter local electricity cost per kWh
- **Shading Adjustment**: Fine-tune shading impact assessment

### 3. Run Analysis
- Click "Analyze Rooftop" to start the AI-powered analysis
- The system will process the image and generate comprehensive results

### 4. Review Results
- **Quick Metrics**: System size, production, savings, and payback period
- **Detailed Analysis**: Roof characteristics, panel layout, and recommendations
- **Financial Projections**: 25-year cash flow and ROI analysis

### 5. Generate Report
- **Interactive Charts**: Energy production and financial visualizations
- **Comprehensive Report**: Executive summary and detailed findings
- **Export Data**: Download JSON reports and CSV financial projections

## 🔧 Configuration

### Panel Types
The tool supports three panel categories:
- **Standard Residential**: 400W, 20% efficiency, $3.50/W
- **High Efficiency**: 450W, 22% efficiency, $4.00/W
- **Premium**: 500W, 24% efficiency, $4.50/W

### Financial Parameters
- Federal tax credit: 30%
- System degradation: 0.5% annually
- Warranty period: 25 years
- Default electricity rate: $0.13/kWh

### Analysis Parameters
- Minimum roof area: 20 m²
- Panel spacing: 0.5m
- Edge setback: 1.0m
- Optimal roof tilt: 10-60°

## 🧪 Example Use Cases

### Homeowner Assessment
```
Input: Residential rooftop image
Output: 
- 8.5 kW system recommendation
- $28,000 annual energy production
- $3,400 annual savings
- 7.2-year payback period
```

### Solar Professional Analysis
```
Input: Commercial building image
Output:
- 45 kW system design
- Detailed obstruction mapping
- Installation complexity assessment
- Professional site visit recommendations
```

### Real Estate Evaluation
```
Input: Property listing image
Output:
- Solar potential rating
- Property value enhancement estimate
- Energy independence assessment
- Environmental impact metrics
```

## 📊 Technical Implementation

### Architecture
- **Frontend**: Streamlit web interface
- **AI Integration**: OpenRouter API with Claude 3.5 Sonnet
- **Calculations**: Custom solar energy and financial modeling
- **Visualizations**: Plotly interactive charts
- **Data Export**: JSON and CSV formats

### Key Modules
- `app.py`: Main Streamlit application
- `solar_analyzer.py`: AI vision analysis
- `solar_calculations.py`: Energy and financial calculations
- `report_generator.py`: Report generation and visualization
- `config.py`: Configuration management

### AI Integration
- **Vision Model**: Claude 3.5 Sonnet for image analysis
- **Prompt Engineering**: Structured JSON output extraction
- **Error Handling**: Fallback mechanisms and validation
- **Context Management**: Multi-source data integration

## 🔮 Future Improvements

### Enhanced AI Capabilities
- **3D Roof Modeling**: Advanced geometric analysis
- **Seasonal Shading**: Time-based shadow calculations
- **Weather Integration**: Local climate data incorporation
- **Satellite Data**: Real-time imagery updates

### Advanced Features
- **Multiple Roof Sections**: Complex building analysis
- **Battery Storage**: Energy storage system integration
- **Grid Integration**: Net metering and utility analysis
- **Maintenance Scheduling**: Predictive maintenance recommendations

### Professional Tools
- **CAD Integration**: Technical drawing export
- **Permit Automation**: Automated permit application generation
- **Installer Network**: Connection to certified installers
- **Performance Monitoring**: Post-installation tracking



## 🚀 Deployment

### Hugging Face Spaces

This application is ready for deployment on Hugging Face Spaces:

1. **Fork this repository** to your GitHub account
2. **Create a new Space** on [Hugging Face Spaces](https://huggingface.co/spaces)
3. **Choose Streamlit** as the SDK
4. **Connect your GitHub repository**
5. **Set environment variables** in Space settings:
   - `OPENROUTER_API_KEY` = your OpenRouter API key
6. **Deploy automatically** - the Space will build and run

### Local Development

For local development, see the installation instructions above.

### Environment Variables

Required for full functionality:
- `OPENROUTER_API_KEY`: Your OpenRouter API key for AI analysis

The application includes a demo mode that works without API keys.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For questions or support, please open an issue on GitHub or contact the development team.

---

**Developed for Solar Industry AI Assistant Internship Assessment**

*Demonstrating AI integration, solar industry knowledge, and professional development skills*
