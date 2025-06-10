"""
Generate comprehensive solar analysis reports
"""
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from typing import Dict, List, Any
from config import get_config

class SolarReportGenerator:
    """Generate comprehensive reports and visualizations"""
    
    def __init__(self):
        self.config = get_config()
    
    def generate_executive_summary(self, roof_analysis: Dict[str, Any], 
                                 panel_layout: Dict[str, Any],
                                 energy_production: Dict[str, Any],
                                 financial_analysis: Dict[str, Any],
                                 recommendations: Dict[str, Any]) -> str:
        """Generate executive summary of the analysis"""
        
        system_power = panel_layout["panel_layout"]["total_system_power"] / 1000
        annual_production = energy_production["annual_production_kwh"]
        annual_savings = financial_analysis["savings"]["annual_savings"]
        payback = financial_analysis["savings"]["simple_payback_years"]
        net_cost = financial_analysis["costs"]["net_cost"]
        
        summary = f"""
        ## Executive Summary
        
        **Overall Assessment: {recommendations["overall_feasibility"]}**
        
        ### Key Findings:
        - **Roof Suitability**: {roof_analysis["solar_suitability"]["overall_rating"].title()}
        - **Recommended System Size**: {system_power:.1f} kW ({panel_layout["panel_layout"]["total_panels"]} panels)
        - **Annual Energy Production**: {annual_production:,.0f} kWh
        - **Annual Savings**: ${annual_savings:,.0f}
        - **System Cost**: ${net_cost:,.0f} (after federal tax credit)
        - **Payback Period**: {payback:.1f} years
        
        ### Environmental Impact:
        - **CO₂ Offset**: {energy_production["co2_offset_tons"]:.1f} tons per year
        - **Equivalent**: Planting {energy_production["co2_offset_tons"] * 16:.0f} trees annually
        
        ### Financial Highlights:
        - **25-Year Savings**: ${financial_analysis["savings"]["lifetime_savings"]:,.0f}
        - **Return on Investment**: {financial_analysis["returns"]["roi_25_year"]:.1f}%
        - **Net Present Value**: ${financial_analysis["returns"]["npv"]:,.0f}
        """
        
        return summary
    
    def create_roof_analysis_chart(self, roof_analysis: Dict[str, Any]) -> go.Figure:
        """Create roof analysis visualization"""
        
        # Roof area breakdown
        total_area = roof_analysis["roof_analysis"]["roof_area_sqm"]
        usable_area = roof_analysis["roof_analysis"]["usable_area_sqm"]
        unusable_area = total_area - usable_area
        
        fig = go.Figure(data=[
            go.Pie(
                labels=['Usable for Solar', 'Unusable (Obstructions/Setbacks)'],
                values=[usable_area, unusable_area],
                hole=0.4,
                marker_colors=['#2E8B57', '#CD5C5C']
            )
        ])
        
        fig.update_layout(
            title="Roof Area Analysis",
            annotations=[dict(text=f'{total_area:.0f} m²<br>Total Area', 
                            x=0.5, y=0.5, font_size=16, showarrow=False)]
        )
        
        return fig
    
    def create_energy_production_chart(self, energy_production: Dict[str, Any]) -> go.Figure:
        """Create energy production visualization"""
        
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_production = energy_production["monthly_production_kwh"]
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            x=months,
            y=monthly_production,
            marker_color='#FFD700',
            name='Monthly Production'
        ))
        
        # Add average line
        avg_production = energy_production["annual_production_kwh"] / 12
        fig.add_hline(y=avg_production, line_dash="dash", 
                     annotation_text=f"Average: {avg_production:.0f} kWh")
        
        fig.update_layout(
            title="Monthly Energy Production Forecast",
            xaxis_title="Month",
            yaxis_title="Energy Production (kWh)",
            showlegend=False
        )
        
        return fig
    
    def create_financial_projection_chart(self, financial_analysis: Dict[str, Any]) -> go.Figure:
        """Create financial projection visualization"""
        
        cash_flows = financial_analysis["cash_flow_projection"]
        years = [cf["year"] for cf in cash_flows]
        cumulative_savings = [cf["cumulative_savings"] for cf in cash_flows]
        net_benefit = [cf["net_benefit"] for cf in cash_flows]
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        # Cumulative savings
        fig.add_trace(
            go.Scatter(x=years, y=cumulative_savings, name="Cumulative Savings",
                      line=dict(color='#2E8B57', width=3)),
            secondary_y=False,
        )
        
        # Net benefit
        fig.add_trace(
            go.Scatter(x=years, y=net_benefit, name="Net Benefit",
                      line=dict(color='#4169E1', width=3)),
            secondary_y=False,
        )
        
        # Break-even line
        fig.add_hline(y=0, line_dash="dash", line_color="red",
                     annotation_text="Break-even")
        
        fig.update_xaxes(title_text="Year")
        fig.update_yaxes(title_text="Amount ($)", secondary_y=False)
        
        fig.update_layout(
            title="25-Year Financial Projection",
            hovermode='x unified'
        )
        
        return fig
    
    def create_system_comparison_table(self) -> pd.DataFrame:
        """Create system comparison table"""
        
        panel_types = self.config["solar_panels"]
        
        comparison_data = []
        for panel_type, specs in panel_types.items():
            comparison_data.append({
                "Panel Type": panel_type.replace("_", " ").title(),
                "Power Rating (W)": specs["power_rating"],
                "Efficiency (%)": f"{specs['efficiency']*100:.1f}%",
                "Cost per Watt ($)": f"${specs['cost_per_watt']:.2f}",
                "Area (m²)": specs["area"]
            })
        
        return pd.DataFrame(comparison_data)
    
    def create_shading_impact_chart(self, roof_analysis: Dict[str, Any]) -> go.Figure:
        """Create shading impact visualization"""
        
        shading_sources = ['Trees', 'Buildings', 'Self-Shading', 'Other']
        shading_levels = [
            roof_analysis["shading_analysis"]["nearby_trees"],
            roof_analysis["shading_analysis"]["neighboring_buildings"],
            roof_analysis["shading_analysis"]["self_shading"],
            "minimal"  # placeholder for other
        ]
        
        # Convert to numeric values
        level_values = {"none": 0, "minimal": 1, "low": 1, "moderate": 2, "significant": 3, "high": 3}
        numeric_values = [level_values.get(level, 1) for level in shading_levels]
        
        colors = ['#90EE90' if v <= 1 else '#FFD700' if v == 2 else '#FF6347' for v in numeric_values]
        
        fig = go.Figure(data=[
            go.Bar(x=shading_sources, y=numeric_values, marker_color=colors)
        ])
        
        fig.update_layout(
            title="Shading Impact Analysis",
            xaxis_title="Shading Source",
            yaxis_title="Impact Level",
            yaxis=dict(tickmode='array', tickvals=[0, 1, 2, 3], 
                      ticktext=['None', 'Low', 'Moderate', 'High'])
        )
        
        return fig
    
    def generate_detailed_report(self, analysis_results: Dict[str, Any]) -> None:
        """Generate detailed report in Streamlit"""
        
        st.header("Detailed Analysis Report")

        # Unpack results
        roof_analysis = analysis_results["roof_analysis"]
        panel_layout = analysis_results["panel_layout"]
        energy_production = analysis_results["energy_production"]
        financial_analysis = analysis_results["financial_analysis"]
        recommendations = analysis_results["recommendations"]

        # Executive Summary
        st.markdown(self.generate_executive_summary(
            roof_analysis, panel_layout, energy_production,
            financial_analysis, recommendations
        ))
        
        # Key Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "System Size",
                f"{panel_layout['panel_layout']['total_system_power']/1000:.1f} kW",
                f"{panel_layout['panel_layout']['total_panels']} panels"
            )
        
        with col2:
            st.metric(
                "Annual Production",
                f"{energy_production['annual_production_kwh']:,.0f} kWh",
                f"{energy_production['daily_average_kwh']:.1f} kWh/day"
            )
        
        with col3:
            st.metric(
                "Annual Savings",
                f"${financial_analysis['savings']['annual_savings']:,.0f}",
                f"${financial_analysis['savings']['monthly_savings']:.0f}/month"
            )
        
        with col4:
            st.metric(
                "Payback Period",
                f"{financial_analysis['savings']['simple_payback_years']:.1f} years",
                f"ROI: {financial_analysis['returns']['roi_25_year']:.1f}%"
            )
        
        # Charts
        st.subheader("Analysis Charts")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(self.create_roof_analysis_chart(roof_analysis), use_container_width=True)
            st.plotly_chart(self.create_shading_impact_chart(roof_analysis), use_container_width=True)

        with col2:
            st.plotly_chart(self.create_energy_production_chart(energy_production), use_container_width=True)

        st.plotly_chart(self.create_financial_projection_chart(financial_analysis), use_container_width=True)

        # Detailed Tables
        st.subheader("Detailed Information")
        
        # System specifications
        with st.expander("System Specifications"):
            spec_data = {
                "Specification": [
                    "Total Roof Area", "Usable Area", "Panel Count", "System Power",
                    "Panel Efficiency", "Roof Coverage", "System Efficiency"
                ],
                "Value": [
                    f"{roof_analysis['roof_analysis']['roof_area_sqm']:.0f} m²",
                    f"{roof_analysis['roof_analysis']['usable_area_sqm']:.0f} m²",
                    f"{panel_layout['panel_layout']['total_panels']} panels",
                    f"{panel_layout['panel_layout']['total_system_power']/1000:.1f} kW",
                    f"{panel_layout['panel_layout']['panel_efficiency']*100:.1f}%",
                    f"{panel_layout['panel_layout']['roof_coverage_percentage']:.1f}%",
                    f"{energy_production['system_efficiency']*100:.1f}%"
                ]
            }
            st.table(pd.DataFrame(spec_data))
        
        # Financial breakdown
        with st.expander("Financial Breakdown"):
            cost_data = {
                "Cost Component": [
                    "Equipment Cost", "Installation Cost", "Total Cost",
                    "Federal Tax Credit", "Net Cost", "Cost per Watt"
                ],
                "Amount": [
                    f"${financial_analysis['costs']['equipment_cost']:,.0f}",
                    f"${financial_analysis['costs']['installation_cost']:,.0f}",
                    f"${financial_analysis['costs']['total_cost']:,.0f}",
                    f"-${financial_analysis['costs']['federal_tax_credit']:,.0f}",
                    f"${financial_analysis['costs']['net_cost']:,.0f}",
                    f"${financial_analysis['costs']['cost_per_watt']:.2f}/W"
                ]
            }
            st.table(pd.DataFrame(cost_data))
        
        # Recommendations
        st.subheader("Recommendations")

        for i, rec in enumerate(recommendations["recommendations"], 1):
            st.write(f"{i}. {rec}")

        if recommendations["priority_items"]:
            st.warning("Priority Items: " + ", ".join(recommendations["priority_items"]))

        # Next steps
        with st.expander("Next Steps"):
            for i, step in enumerate(recommendations["next_steps"], 1):
                st.write(f"{i}. {step}")
    
    def export_report_data(self, analysis_results: Dict[str, Any]) -> Dict[str, Any]:
        """Export analysis data for download"""
        
        return {
            "summary": {
                "analysis_date": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
                "overall_feasibility": analysis_results["recommendations"]["overall_feasibility"],
                "system_size_kw": analysis_results["panel_layout"]["panel_layout"]["total_system_power"] / 1000,
                "annual_production_kwh": analysis_results["energy_production"]["annual_production_kwh"],
                "annual_savings_usd": analysis_results["financial_analysis"]["savings"]["annual_savings"],
                "payback_years": analysis_results["financial_analysis"]["savings"]["simple_payback_years"]
            },
            "detailed_analysis": analysis_results
        }
