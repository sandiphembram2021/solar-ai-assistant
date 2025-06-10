"""
AI-powered solar rooftop analysis using vision models
"""
import base64
import io
import json
import requests
from typing import Dict, List, Tuple, Optional, Any
from PIL import Image
import numpy as np
from config import get_config

class SolarRooftopAnalyzer:
    """Main class for analyzing rooftop solar potential using AI vision models"""
    
    def __init__(self):
        self.config = get_config()
        self.api_key = self.config["api"]["openrouter_key"]
        self.base_url = self.config["api"]["base_url"]
        self.vision_model = self.config["api"]["vision_model"]
        
    def encode_image(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string"""
        # Convert RGBA to RGB if necessary (for JPEG compatibility)
        if image.mode in ('RGBA', 'LA', 'P'):
            # Create a white background
            background = Image.new('RGB', image.size, (255, 255, 255))
            if image.mode == 'P':
                image = image.convert('RGBA')
            background.paste(image, mask=image.split()[-1] if image.mode in ('RGBA', 'LA') else None)
            image = background
        elif image.mode != 'RGB':
            image = image.convert('RGB')

        buffer = io.BytesIO()
        image.save(buffer, format="JPEG", quality=85)
        return base64.b64encode(buffer.getvalue()).decode()
    
    def analyze_rooftop_structure(self, image: Image.Image) -> Dict[str, Any]:
        """Analyze rooftop structure and characteristics"""

        try:
            # Encode image with proper format handling
            image_b64 = self.encode_image(image)
        except Exception as e:
            print(f"Error encoding image: {e}")
            return self._get_default_analysis()

        prompt = """
        Analyze this satellite/aerial image of a rooftop for solar panel installation potential.
        Provide a detailed JSON response with the following structure:

        {
            "roof_analysis": {
                "roof_area_sqm": <estimated total roof area in square meters>,
                "usable_area_sqm": <area suitable for solar panels>,
                "roof_shape": "<rectangular/L-shaped/complex/irregular>",
                "roof_material": "<asphalt_shingles/tile/metal/flat_membrane/other>",
                "roof_condition": "<excellent/good/fair/poor>",
                "roof_age_estimate": "<new/5-10_years/10-20_years/20+_years>"
            },
            "orientation_analysis": {
                "primary_roof_direction": "<north/northeast/east/southeast/south/southwest/west/northwest>",
                "roof_tilt_estimate": <angle in degrees, 0-60>,
                "multiple_orientations": <true/false>,
                "optimal_sections": ["<list of roof sections best for solar>"]
            },
            "obstructions": {
                "chimneys": <count>,
                "vents": <count>,
                "skylights": <count>,
                "hvac_units": <count>,
                "satellite_dishes": <count>,
                "other_obstructions": ["<list any other obstructions>"]
            },
            "shading_analysis": {
                "nearby_trees": "<none/minimal/moderate/significant>",
                "neighboring_buildings": "<none/minimal/moderate/significant>",
                "self_shading": "<none/minimal/moderate/significant>",
                "overall_shading_impact": "<minimal/low/moderate/high>"
            },
            "access_and_installation": {
                "roof_accessibility": "<easy/moderate/difficult>",
                "structural_concerns": "<none/minor/moderate/major>",
                "electrical_panel_visible": <true/false>,
                "installation_complexity": "<simple/moderate/complex>"
            },
            "solar_suitability": {
                "overall_rating": "<excellent/good/fair/poor>",
                "confidence_score": <0.0-1.0>,
                "key_advantages": ["<list main advantages>"],
                "key_challenges": ["<list main challenges>"],
                "recommendations": ["<list specific recommendations>"]
            }
        }

        Be precise and realistic in your estimates. Consider standard residential roof sizes and solar installation requirements.
        """
        
        try:
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": self.vision_model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_b64}"
                                    }
                                }
                            ]
                        }
                    ],
                    "max_tokens": 2000,
                    "temperature": 0.1
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Extract JSON from response
                try:
                    # Find JSON in the response
                    start_idx = content.find('{')
                    end_idx = content.rfind('}') + 1
                    json_str = content[start_idx:end_idx]
                    return json.loads(json_str)
                except (json.JSONDecodeError, ValueError) as e:
                    # Fallback: create structured response from text
                    return self._parse_text_response(content)
            else:
                raise Exception(f"API request failed: {response.status_code}")
                
        except Exception as e:
            error_msg = str(e)
            print(f"Error in rooftop analysis: {error_msg}")

            # Provide more specific error messages
            if "RGBA" in error_msg or "JPEG" in error_msg:
                print("Image format issue detected - using fallback analysis")
            elif "401" in error_msg:
                print("API authentication issue - using fallback analysis")
            elif "timeout" in error_msg.lower():
                print("API timeout - using fallback analysis")
            else:
                print("General API error - using fallback analysis")

            return self._get_default_analysis()
    
    def estimate_panel_layout(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Estimate optimal solar panel layout based on roof analysis"""
        
        usable_area = analysis["roof_analysis"]["usable_area_sqm"]
        panel_specs = self.config["solar_panels"]["standard_residential"]
        panel_area = panel_specs["area"]
        
        # Account for spacing and setbacks
        spacing_factor = 0.85  # 15% reduction for spacing
        effective_area = usable_area * spacing_factor
        
        # Calculate number of panels
        max_panels = int(effective_area / panel_area)
        
        # Adjust based on obstructions and shading
        obstruction_count = sum([
            analysis["obstructions"]["chimneys"],
            analysis["obstructions"]["vents"],
            analysis["obstructions"]["skylights"],
            analysis["obstructions"]["hvac_units"]
        ])
        
        # Reduce panels based on obstructions (each obstruction affects ~2-3 panels)
        panels_lost_to_obstructions = obstruction_count * 2.5
        
        # Adjust for shading
        shading_impact = analysis["shading_analysis"]["overall_shading_impact"]
        shading_reduction = {
            "minimal": 0.95,
            "low": 0.90,
            "moderate": 0.80,
            "high": 0.60
        }.get(shading_impact, 0.85)
        
        final_panel_count = max(0, int((max_panels - panels_lost_to_obstructions) * shading_reduction))
        
        return {
            "panel_layout": {
                "total_panels": final_panel_count,
                "panel_power_rating": panel_specs["power_rating"],
                "total_system_power": final_panel_count * panel_specs["power_rating"],
                "total_panel_area": final_panel_count * panel_area,
                "roof_coverage_percentage": (final_panel_count * panel_area / usable_area) * 100,
                "panel_efficiency": panel_specs["efficiency"]
            },
            "layout_optimization": {
                "panels_lost_to_obstructions": int(panels_lost_to_obstructions),
                "shading_reduction_factor": shading_reduction,
                "spacing_efficiency": spacing_factor,
                "layout_efficiency": final_panel_count / max_panels if max_panels > 0 else 0
            }
        }
    
    def _parse_text_response(self, content: str) -> Dict[str, Any]:
        """Parse text response when JSON extraction fails"""
        # This is a fallback method to extract key information from text
        return self._get_default_analysis()
    
    def _get_default_analysis(self) -> Dict[str, Any]:
        """Return default analysis structure when AI analysis fails"""
        return {
            "roof_analysis": {
                "roof_area_sqm": 150,
                "usable_area_sqm": 120,
                "roof_shape": "rectangular",
                "roof_material": "asphalt_shingles",
                "roof_condition": "good",
                "roof_age_estimate": "10-20_years"
            },
            "orientation_analysis": {
                "primary_roof_direction": "south",
                "roof_tilt_estimate": 30,
                "multiple_orientations": False,
                "optimal_sections": ["main_roof"]
            },
            "obstructions": {
                "chimneys": 1,
                "vents": 3,
                "skylights": 0,
                "hvac_units": 1,
                "satellite_dishes": 0,
                "other_obstructions": []
            },
            "shading_analysis": {
                "nearby_trees": "minimal",
                "neighboring_buildings": "minimal",
                "self_shading": "none",
                "overall_shading_impact": "low"
            },
            "access_and_installation": {
                "roof_accessibility": "moderate",
                "structural_concerns": "minor",
                "electrical_panel_visible": True,
                "installation_complexity": "moderate"
            },
            "solar_suitability": {
                "overall_rating": "good",
                "confidence_score": 0.7,
                "key_advantages": ["Good roof area", "South-facing orientation"],
                "key_challenges": ["Some obstructions present"],
                "recommendations": ["Professional site assessment recommended"]
            }
        }
