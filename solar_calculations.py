"""
Solar energy calculations and financial analysis
"""
import math
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any
from config import get_config

class SolarCalculations:
    """Handle solar energy production and financial calculations"""
    
    def __init__(self, latitude: float = 37.7749, longitude: float = -122.4194):
        self.config = get_config()
        self.latitude = latitude
        self.longitude = longitude
        
    def calculate_solar_irradiance(self, tilt: float, azimuth: float) -> Dict[str, float]:
        """Calculate solar irradiance based on location and panel orientation"""
        
        # Simplified solar irradiance calculation
        # In a real application, you'd use NREL data or pvlib
        
        # Base annual irradiance for the location (kWh/m²/year)
        base_irradiance = self._get_base_irradiance()
        
        # Tilt factor (optimal tilt is approximately equal to latitude)
        optimal_tilt = abs(self.latitude)
        tilt_factor = math.cos(math.radians(abs(tilt - optimal_tilt))) * 0.9 + 0.1
        
        # Azimuth factor (180° is optimal - south facing)
        azimuth_deviation = abs(azimuth - 180)
        azimuth_factor = math.cos(math.radians(azimuth_deviation)) * 0.8 + 0.2
        
        # Combined factors
        total_irradiance = base_irradiance * tilt_factor * azimuth_factor
        
        return {
            "annual_irradiance": total_irradiance,
            "daily_average": total_irradiance / 365,
            "peak_sun_hours": total_irradiance / 1000,  # Approximate peak sun hours
            "tilt_factor": tilt_factor,
            "azimuth_factor": azimuth_factor
        }
    
    def calculate_energy_production(self, system_power_kw: float, 
                                  irradiance_data: Dict[str, float],
                                  shading_factor: float = 1.0) -> Dict[str, Any]:
        """Calculate annual energy production"""
        
        # System efficiency factors
        inverter_efficiency = 0.96
        dc_losses = 0.95  # DC wiring, connections
        ac_losses = 0.98  # AC wiring
        soiling_factor = 0.95  # Dust, dirt on panels
        temperature_factor = 0.90  # Temperature derating
        
        total_efficiency = (inverter_efficiency * dc_losses * ac_losses * 
                          soiling_factor * temperature_factor * shading_factor)
        
        # Annual production calculation
        annual_production = (system_power_kw * irradiance_data["peak_sun_hours"] * 
                           365 * total_efficiency)
        
        # Monthly breakdown (simplified seasonal variation)
        monthly_factors = [0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.3, 1.2, 1.1, 0.9, 0.7, 0.6]
        monthly_production = [annual_production * factor / 12 for factor in monthly_factors]
        
        return {
            "annual_production_kwh": annual_production,
            "monthly_production_kwh": monthly_production,
            "daily_average_kwh": annual_production / 365,
            "system_efficiency": total_efficiency,
            "capacity_factor": annual_production / (system_power_kw * 8760),
            "co2_offset_tons": annual_production * 0.0004  # Approximate CO2 offset
        }
    
    def calculate_financial_analysis(self, system_power_kw: float, 
                                   annual_production_kwh: float,
                                   panel_type: str = "standard_residential") -> Dict[str, Any]:
        """Calculate comprehensive financial analysis"""
        
        # System costs
        panel_specs = self.config["solar_panels"][panel_type]
        install_costs = self.config["installation"]
        financial_params = self.config["financial"]
        
        # Total system cost
        equipment_cost = system_power_kw * 1000 * panel_specs["cost_per_watt"]
        installation_cost = (system_power_kw * 1000 * install_costs["base_cost_per_watt"] +
                           system_power_kw * 1000 * install_costs["inverter_cost_per_watt"] +
                           install_costs["electrical_cost"] +
                           install_costs["permit_cost"] +
                           install_costs["inspection_cost"] +
                           system_power_kw * install_costs["estimated_install_hours_per_kw"] * 
                           install_costs["labor_cost_per_hour"])
        
        total_cost = equipment_cost + installation_cost
        
        # Tax incentives
        federal_credit = total_cost * financial_params["federal_tax_credit"]
        net_cost = total_cost - federal_credit
        
        # Annual savings calculation
        electricity_rate = financial_params["average_electricity_rate"]
        annual_savings = annual_production_kwh * electricity_rate
        
        # Payback period
        simple_payback = net_cost / annual_savings if annual_savings > 0 else float('inf')
        
        # 25-year financial projection
        years = 25
        cash_flows = []
        cumulative_savings = 0
        
        for year in range(1, years + 1):
            # Account for electricity rate increases and system degradation
            year_rate = electricity_rate * (1 + financial_params["annual_rate_increase"]) ** (year - 1)
            year_production = annual_production_kwh * (1 - financial_params["system_degradation"]) ** (year - 1)
            year_savings = year_production * year_rate
            
            cumulative_savings += year_savings
            cash_flows.append({
                "year": year,
                "production_kwh": year_production,
                "electricity_rate": year_rate,
                "annual_savings": year_savings,
                "cumulative_savings": cumulative_savings,
                "net_benefit": cumulative_savings - net_cost
            })
        
        # NPV calculation
        discount_rate = financial_params["discount_rate"]
        npv = -net_cost + sum([cf["annual_savings"] / (1 + discount_rate) ** cf["year"] 
                              for cf in cash_flows])
        
        # IRR approximation (simplified)
        irr = self._calculate_irr(net_cost, [cf["annual_savings"] for cf in cash_flows])
        
        return {
            "costs": {
                "equipment_cost": equipment_cost,
                "installation_cost": installation_cost,
                "total_cost": total_cost,
                "federal_tax_credit": federal_credit,
                "net_cost": net_cost,
                "cost_per_watt": total_cost / (system_power_kw * 1000)
            },
            "savings": {
                "annual_savings": annual_savings,
                "monthly_savings": annual_savings / 12,
                "lifetime_savings": cumulative_savings,
                "simple_payback_years": simple_payback
            },
            "returns": {
                "npv": npv,
                "irr": irr,
                "roi_25_year": (cumulative_savings - net_cost) / net_cost * 100
            },
            "cash_flow_projection": cash_flows
        }
    
    def _get_base_irradiance(self) -> float:
        """Get base solar irradiance for location (simplified)"""
        # This is a simplified calculation
        # In practice, you'd use NREL or other solar databases
        
        # Approximate annual irradiance based on latitude
        if abs(self.latitude) < 25:  # Tropical
            return 2000
        elif abs(self.latitude) < 35:  # Subtropical
            return 1800
        elif abs(self.latitude) < 45:  # Temperate
            return 1600
        else:  # Northern/Southern regions
            return 1400
    
    def _calculate_irr(self, initial_investment: float, cash_flows: List[float]) -> float:
        """Calculate Internal Rate of Return (simplified approximation)"""
        # Simplified IRR calculation using approximation
        # For more accuracy, you'd use scipy.optimize or numpy financial functions
        
        total_cash_flow = sum(cash_flows)
        average_annual_return = total_cash_flow / len(cash_flows)
        
        if initial_investment <= 0:
            return 0
        
        # Simple approximation
        irr_approx = (average_annual_return / initial_investment) * 100
        
        # Cap at reasonable values
        return min(max(irr_approx, 0), 50)
    
    def get_system_recommendations(self, roof_analysis: Dict[str, Any], 
                                 financial_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate system recommendations based on analysis"""
        
        recommendations = []
        priority_items = []
        
        # Roof condition recommendations
        roof_condition = roof_analysis["roof_analysis"]["roof_condition"]
        if roof_condition in ["poor", "fair"]:
            recommendations.append("Consider roof repairs or replacement before solar installation")
            priority_items.append("roof_condition")
        
        # Shading recommendations
        shading_impact = roof_analysis["shading_analysis"]["overall_shading_impact"]
        if shading_impact in ["moderate", "high"]:
            recommendations.append("Consider tree trimming or removal to reduce shading")
            recommendations.append("Evaluate micro-inverters or power optimizers for shaded areas")
        
        # Financial recommendations
        payback = financial_analysis["savings"]["simple_payback_years"]
        if payback < 7:
            recommendations.append("Excellent financial return - highly recommended")
        elif payback < 10:
            recommendations.append("Good financial return - recommended")
        elif payback < 15:
            recommendations.append("Moderate return - consider if environmental benefits are important")
        else:
            recommendations.append("Long payback period - may not be financially optimal")
        
        # System size recommendations
        system_power = roof_analysis.get("panel_layout", {}).get("total_system_power", 0) / 1000
        if system_power < 3:
            recommendations.append("Small system size - consider if it meets your energy needs")
        elif system_power > 10:
            recommendations.append("Large system - verify electrical panel capacity")
        
        return {
            "recommendations": recommendations,
            "priority_items": priority_items,
            "overall_feasibility": self._assess_overall_feasibility(roof_analysis, financial_analysis),
            "next_steps": [
                "Get professional site assessment",
                "Obtain multiple installer quotes",
                "Check local permitting requirements",
                "Verify utility net metering policies",
                "Consider financing options"
            ]
        }
    
    def _assess_overall_feasibility(self, roof_analysis: Dict[str, Any], 
                                  financial_analysis: Dict[str, Any]) -> str:
        """Assess overall project feasibility"""
        
        # Scoring factors
        roof_rating = roof_analysis["solar_suitability"]["overall_rating"]
        payback = financial_analysis["savings"]["simple_payback_years"]
        
        roof_score = {"excellent": 4, "good": 3, "fair": 2, "poor": 1}.get(roof_rating, 2)
        
        if payback < 7:
            financial_score = 4
        elif payback < 10:
            financial_score = 3
        elif payback < 15:
            financial_score = 2
        else:
            financial_score = 1
        
        total_score = (roof_score + financial_score) / 2
        
        if total_score >= 3.5:
            return "Highly Recommended"
        elif total_score >= 2.5:
            return "Recommended"
        elif total_score >= 1.5:
            return "Consider with Caution"
        else:
            return "Not Recommended"
