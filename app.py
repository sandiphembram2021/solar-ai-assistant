"""
Solar Rooftop Analysis Tool - Main Application
AI-powered rooftop analysis for solar installation potential assessment
"""
import streamlit as st
import os
from dotenv import load_dotenv
from PIL import Image
import json
import pandas as pd
from typing import Dict, Any

# Load environment variables
load_dotenv()

# Import custom modules
from config import get_config, validate_config

# Import deployment configuration
try:
    from app_config import HF_SPACE, OPENROUTER_API_KEY
    if HF_SPACE:
        st.info("Running in Hugging Face Spaces mode")
except ImportError:
    HF_SPACE = False
    OPENROUTER_API_KEY = None
from solar_analyzer import SolarRooftopAnalyzer
from solar_calculations import SolarCalculations
from report_generator import SolarReportGenerator

# Page configuration
st.set_page_config(
    page_title="Solar Rooftop Analysis Tool",
    page_icon="🌞",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B35;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2E8B57;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #FF6B35;
    }
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        border: 1px solid #ffeaa7;
        border-radius: 0.25rem;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">Solar Rooftop Analysis Tool</h1>', unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <p style="font-size: 1.2rem; color: #666;">
            AI-powered rooftop analysis for solar installation potential assessment
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Check configuration
    if not validate_config():
        st.error("OpenRouter API key not found. Please set OPENROUTER_API_KEY environment variable.")
        st.info("Get your API key from https://openrouter.ai/")
        st.stop()
    
    # Sidebar
    with st.sidebar:
        st.header("Configuration")

        # Location settings
        st.subheader("Location")
        latitude = st.number_input("Latitude", value=37.7749, format="%.4f")
        longitude = st.number_input("Longitude", value=-122.4194, format="%.4f")

        # Panel type selection
        st.subheader("Panel Type")
        config = get_config()
        panel_options = list(config["solar_panels"].keys())
        panel_type = st.selectbox(
            "Select panel type:",
            panel_options,
            format_func=lambda x: x.replace("_", " ").title()
        )

        # Analysis parameters
        st.subheader("Analysis Parameters")
        custom_electricity_rate = st.number_input(
            "Electricity Rate ($/kWh)",
            value=0.13,
            min_value=0.05,
            max_value=0.50,
            step=0.01,
            format="%.3f"
        )

        shading_adjustment = st.slider(
            "Shading Adjustment Factor",
            min_value=0.5,
            max_value=1.0,
            value=1.0,
            step=0.05,
            help="Adjust for additional shading not detected in image"
        )
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["Image Analysis", "Results", "Report"])

    with tab1:
        st.header("Upload Rooftop Image")

        # Image upload
        uploaded_file = st.file_uploader(
            "Choose a satellite or aerial image of the rooftop",
            type=['jpg', 'jpeg', 'png', 'tiff'],
            help="Upload a clear satellite or aerial image showing the rooftop you want to analyze"
        )

        if uploaded_file is not None:
            # Display uploaded image
            image = Image.open(uploaded_file)

            col1, col2 = st.columns([2, 1])

            with col1:
                st.image(image, caption="Uploaded Rooftop Image", use_column_width=True)

            with col2:
                st.info("**Image Requirements:**")
                st.write("• Clear view of the rooftop")
                st.write("• Minimal cloud cover")
                st.write("• Recent imagery preferred")
                st.write("• Good resolution")

                # Image info
                st.write(f"**Image Size:** {image.size[0]} x {image.size[1]} pixels")
                st.write(f"**File Size:** {uploaded_file.size / 1024:.1f} KB")

            # Analysis button
            if st.button("Analyze Rooftop", type="primary", use_container_width=True):
                analyze_rooftop(image, latitude, longitude, panel_type,
                              custom_electricity_rate, shading_adjustment)

    with tab2:
        if 'analysis_results' in st.session_state:
            display_results()
        else:
            st.info("Please upload an image and run the analysis first.")

    with tab3:
        if 'analysis_results' in st.session_state:
            generate_report()
        else:
            st.info("Please upload an image and run the analysis first.")

def analyze_rooftop(image: Image.Image, latitude: float, longitude: float, 
                   panel_type: str, electricity_rate: float, shading_factor: float):
    """Perform comprehensive rooftop analysis"""
    
    with st.spinner("Analyzing rooftop with AI..."):
        try:
            # Initialize analyzers
            analyzer = SolarRooftopAnalyzer()
            calculator = SolarCalculations(latitude, longitude)

            # Step 1: AI Vision Analysis
            st.write("Analyzing rooftop structure...")
            roof_analysis = analyzer.analyze_rooftop_structure(image)

            # Step 2: Panel Layout Estimation
            st.write("Calculating optimal panel layout...")
            panel_layout = analyzer.estimate_panel_layout(roof_analysis)

            # Step 3: Energy Production Calculation
            st.write("Calculating energy production...")

            # Get roof orientation for irradiance calculation
            roof_direction = roof_analysis["orientation_analysis"]["primary_roof_direction"]
            roof_tilt = roof_analysis["orientation_analysis"]["roof_tilt_estimate"]

            # Convert direction to azimuth
            direction_to_azimuth = {
                "north": 0, "northeast": 45, "east": 90, "southeast": 135,
                "south": 180, "southwest": 225, "west": 270, "northwest": 315
            }
            azimuth = direction_to_azimuth.get(roof_direction, 180)

            # Calculate irradiance and energy production
            irradiance_data = calculator.calculate_solar_irradiance(roof_tilt, azimuth)

            system_power_kw = panel_layout["panel_layout"]["total_system_power"] / 1000
            energy_production = calculator.calculate_energy_production(
                system_power_kw, irradiance_data, shading_factor
            )

            # Step 4: Financial Analysis
            st.write("Performing financial analysis...")

            # Update electricity rate in config
            config = get_config()
            config["financial"]["average_electricity_rate"] = electricity_rate

            financial_analysis = calculator.calculate_financial_analysis(
                system_power_kw, energy_production["annual_production_kwh"], panel_type
            )

            # Step 5: Generate Recommendations
            st.write("Generating recommendations...")
            recommendations = calculator.get_system_recommendations(roof_analysis, financial_analysis)

            # Store results in session state
            st.session_state.analysis_results = {
                "roof_analysis": roof_analysis,
                "panel_layout": panel_layout,
                "energy_production": energy_production,
                "financial_analysis": financial_analysis,
                "recommendations": recommendations,
                "parameters": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "panel_type": panel_type,
                    "electricity_rate": electricity_rate,
                    "shading_factor": shading_factor
                }
            }

            st.success("Analysis completed successfully!")
            st.balloons()

        except Exception as e:
            error_msg = str(e)

            # Provide specific error messages based on the error type
            if "RGBA" in error_msg or "JPEG" in error_msg:
                st.error("Image format error: The uploaded image has transparency which has been automatically converted.")
                st.info("The analysis will continue with the converted image. Please try uploading the image again.")
            elif "401" in error_msg or "authentication" in error_msg.lower():
                st.error("API authentication failed. Please check your OpenRouter API key.")
                st.info("The system will use fallback analysis. For full AI features, verify your API key in the .env file.")
            elif "timeout" in error_msg.lower():
                st.error("API request timed out. Please try again.")
                st.info("This might be due to network issues or high API load.")
            elif "rate limit" in error_msg.lower():
                st.error("API rate limit exceeded. Please wait a moment and try again.")
                st.info("The system will use fallback analysis for now.")
            else:
                st.error(f"Analysis failed: {error_msg}")
                st.info("The system will use fallback analysis. If the problem persists, check your API configuration.")

            # Still show some results using fallback
            st.warning("Using fallback analysis mode...")

            # Initialize analyzers for fallback
            analyzer = SolarRooftopAnalyzer()
            calculator = SolarCalculations(latitude, longitude)

            # Use default analysis
            roof_analysis = analyzer._get_default_analysis()
            panel_layout = analyzer.estimate_panel_layout(roof_analysis)

            # Continue with energy and financial calculations
            irradiance_data = calculator.calculate_solar_irradiance(25, 180)  # Default values
            system_power_kw = panel_layout["panel_layout"]["total_system_power"] / 1000
            energy_production = calculator.calculate_energy_production(
                system_power_kw, irradiance_data, shading_factor
            )

            financial_analysis = calculator.calculate_financial_analysis(
                system_power_kw, energy_production["annual_production_kwh"], panel_type
            )

            recommendations = calculator.get_system_recommendations(roof_analysis, financial_analysis)

            # Store fallback results
            st.session_state.analysis_results = {
                "roof_analysis": roof_analysis,
                "panel_layout": panel_layout,
                "energy_production": energy_production,
                "financial_analysis": financial_analysis,
                "recommendations": recommendations,
                "parameters": {
                    "latitude": latitude,
                    "longitude": longitude,
                    "panel_type": panel_type,
                    "electricity_rate": electricity_rate,
                    "shading_factor": shading_factor
                },
                "fallback_mode": True
            }

            st.info("Fallback analysis completed. Results are based on typical roof characteristics.")

def display_results():
    """Display analysis results"""

    results = st.session_state.analysis_results

    st.header("Analysis Results")

    # Quick metrics
    col1, col2, col3, col4 = st.columns(4)

    system_power = results["panel_layout"]["panel_layout"]["total_system_power"] / 1000
    annual_production = results["energy_production"]["annual_production_kwh"]
    annual_savings = results["financial_analysis"]["savings"]["annual_savings"]
    payback = results["financial_analysis"]["savings"]["simple_payback_years"]

    with col1:
        st.metric("System Size", f"{system_power:.1f} kW",
                 f"{results['panel_layout']['panel_layout']['total_panels']} panels")

    with col2:
        st.metric("Annual Production", f"{annual_production:,.0f} kWh",
                 f"{annual_production/365:.1f} kWh/day")

    with col3:
        st.metric("Annual Savings", f"${annual_savings:,.0f}",
                 f"${annual_savings/12:.0f}/month")

    with col4:
        st.metric("Payback Period", f"{payback:.1f} years",
                 f"ROI: {results['financial_analysis']['returns']['roi_25_year']:.1f}%")

    # Overall assessment
    feasibility = results["recommendations"]["overall_feasibility"]
    if feasibility == "Highly Recommended":
        st.success(f"**Overall Assessment: {feasibility}**")
    elif feasibility == "Recommended":
        st.success(f"**Overall Assessment: {feasibility}**")
    elif feasibility == "Consider with Caution":
        st.warning(f"**Overall Assessment: {feasibility}**")
    else:
        st.error(f"**Overall Assessment: {feasibility}**")

    # Detailed breakdown
    with st.expander("Roof Analysis Details"):
        roof_data = results["roof_analysis"]["roof_analysis"]
        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Total Roof Area:** {roof_data['roof_area_sqm']:.0f} m²")
            st.write(f"**Usable Area:** {roof_data['usable_area_sqm']:.0f} m²")
            st.write(f"**Roof Shape:** {roof_data['roof_shape'].replace('_', ' ').title()}")
            st.write(f"**Roof Material:** {roof_data['roof_material'].replace('_', ' ').title()}")

        with col2:
            st.write(f"**Roof Condition:** {roof_data['roof_condition'].title()}")
            st.write(f"**Estimated Age:** {roof_data['roof_age_estimate'].replace('_', ' ')}")
            orientation = results["roof_analysis"]["orientation_analysis"]
            st.write(f"**Primary Direction:** {orientation['primary_roof_direction'].title()}")
            st.write(f"**Roof Tilt:** {orientation['roof_tilt_estimate']}°")

def generate_report():
    """Generate comprehensive report"""

    results = st.session_state.analysis_results
    report_generator = SolarReportGenerator()

    # Generate detailed report
    report_generator.generate_detailed_report(results)

    # Export options
    st.subheader("Export Options")

    col1, col2 = st.columns(2)

    with col1:
        # JSON export
        export_data = report_generator.export_report_data(results)
        json_str = json.dumps(export_data, indent=2, default=str)

        st.download_button(
            label="Download JSON Report",
            data=json_str,
            file_name="solar_analysis_report.json",
            mime="application/json"
        )

    with col2:
        # CSV export for financial projections
        cash_flows = results["financial_analysis"]["cash_flow_projection"]
        df = pd.DataFrame(cash_flows)
        csv = df.to_csv(index=False)

        st.download_button(
            label="Download Financial Projections (CSV)",
            data=csv,
            file_name="solar_financial_projections.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
