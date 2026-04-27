"""
Configuration utilities for Electrical Components Agent
"""

from enum import Enum
from typing import Dict, List, Optional


class SupplierRegistry:
    """Registry for managing electrical component suppliers."""
    
    SUPPLIERS = {
        "digikey": {
            "name": "DigiKey",
            "rating": 4.5,
            "avg_lead_time": 2,
            "specialty": ["electronics", "industrial", "commercial"],
            "min_order": 1,
            "supports_bulk": True,
        },
        "mouser": {
            "name": "Mouser Electronics",
            "rating": 4.4,
            "avg_lead_time": 2,
            "specialty": ["electronics", "industrial"],
            "min_order": 1,
            "supports_bulk": True,
        },
        "newark": {
            "name": "Newark Electronics",
            "rating": 4.0,
            "avg_lead_time": 3,
            "specialty": ["commercial", "industrial"],
            "min_order": 1,
            "supports_bulk": True,
        },
        "bisco": {
            "name": "Bisco Industries",
            "rating": 3.9,
            "avg_lead_time": 3,
            "specialty": ["industrial", "commercial"],
            "min_order": 1,
            "supports_bulk": True,
        },
        "aliexpress": {
            "name": "AliExpress",
            "rating": 3.5,
            "avg_lead_time": 14,
            "specialty": ["consumer", "hobbyist"],
            "min_order": 1,
            "supports_bulk": False,
        },
        "ebay": {
            "name": "eBay",
            "rating": 3.3,
            "avg_lead_time": 7,
            "specialty": ["consumer", "surplus"],
            "min_order": 1,
            "supports_bulk": False,
        }
    }
    
    @classmethod
    def get_supplier(cls, supplier_id: str) -> Optional[Dict]:
        """Get supplier details by ID."""
        return cls.SUPPLIERS.get(supplier_id)
    
    @classmethod
    def list_all(cls) -> Dict[str, Dict]:
        """List all suppliers."""
        return cls.SUPPLIERS
    
    @classmethod
    def get_suppliers_for_component(cls, component_type: str) -> List[str]:
        """Get suppliers that carry a specific component type."""
        matching = []
        for supplier_id, details in cls.SUPPLIERS.items():
            if component_type.lower() in [s.lower() for s in details.get("specialty", [])]:
                matching.append(supplier_id)
        return matching if matching else list(cls.SUPPLIERS.keys())
    
    @classmethod
    def get_premium_suppliers(cls) -> List[str]:
        """Get premium suppliers (rating > 4.0)."""
        return [sid for sid, details in cls.SUPPLIERS.items() if details["rating"] > 4.0]


class CacheManager:
    """Manages caching for improved performance."""
    
    def __init__(self, ttl_seconds: int = 3600):
        self.cache: Dict = {}
        self.ttl_seconds = ttl_seconds
        self.timestamps: Dict = {}
    
    def get(self, key: str) -> Optional:
        """Get value from cache if not expired."""
        if key not in self.cache:
            return None
        
        import time
        if time.time() - self.timestamps.get(key, 0) > self.ttl_seconds:
            del self.cache[key]
            del self.timestamps[key]
            return None
        
        return self.cache[key]
    
    def set(self, key: str, value):
        """Set value in cache."""
        import time
        self.cache[key] = value
        self.timestamps[key] = time.time()
    
    def clear(self):
        """Clear all cache."""
        self.cache.clear()
        self.timestamps.clear()


class ComponentRecommender:
    """Recommends alternative components based on requirements."""
    
    # Common component alternatives
    ALTERNATIVES = {
        "resistor_1k_0.25w": ["resistor_1k_0.5w", "resistor_1k_1w"],
        "capacitor_10uf_50v": ["capacitor_10uf_63v", "capacitor_10uf_100v"],
        "transistor_2n2222": ["transistor_2n3904", "transistor_bc547"],
    }
    
    @classmethod
    def get_alternatives(cls, component_id: str) -> List[str]:
        """Get list of alternative components."""
        return cls.ALTERNATIVES.get(component_id, [])
    
    @classmethod
    def recommend_by_specs(cls, specs: Dict) -> List[Dict]:
        """Recommend components based on specifications."""
        # Simplified recommendation logic
        recommendations = []
        
        if specs.get("power") == "0.25w":
            recommendations.append({
                "reason": "Higher power rating for reliability",
                "alternatives": ["0.5w", "1w"]
            })
        
        if specs.get("voltage") and specs["voltage"] < 50:
            recommendations.append({
                "reason": "Higher voltage rating for safety margin",
                "alternatives": ["63v", "100v"]
            })
        
        return recommendations


class PriceComparator:
    """Compares and analyzes component prices."""
    
    @staticmethod
    def calculate_bulk_discount(unit_price: float, quantity: int) -> float:
        """Calculate bulk discount based on quantity."""
        if quantity >= 500:
            return unit_price * 0.80  # 20% off
        elif quantity >= 250:
            return unit_price * 0.85  # 15% off
        elif quantity >= 100:
            return unit_price * 0.90  # 10% off
        elif quantity >= 50:
            return unit_price * 0.95  # 5% off
        return unit_price
    
    @staticmethod
    def calculate_total_cost_per_unit(
        unit_price: float,
        quantity: int,
        shipping_cost: float = 0.0,
        tax_rate: float = 0.0
    ) -> float:
        """Calculate total cost per unit including shipping and tax."""
        subtotal = unit_price * quantity
        shipping_per_unit = shipping_cost / quantity if quantity > 0 else 0
        tax = subtotal * tax_rate / quantity if quantity > 0 else 0
        return unit_price + shipping_per_unit + tax
    
    @staticmethod
    def compare_suppliers(offers: List) -> Dict:
        """Compare prices across suppliers."""
        if not offers:
            return {}
        
        prices = [o.unit_price for o in offers]
        return {
            "min": min(prices),
            "max": max(prices),
            "avg": sum(prices) / len(prices),
            "median": sorted(prices)[len(prices) // 2],
            "range": max(prices) - min(prices)
        }


class InventoryOptimizer:
    """Optimizes inventory levels and ordering."""
    
    @staticmethod
    def calculate_economic_order_quantity(
        annual_demand: int,
        ordering_cost: float,
        holding_cost_per_unit: float
    ) -> int:
        """Calculate Economic Order Quantity (EOQ)."""
        if holding_cost_per_unit <= 0:
            return 0
        
        import math
        eoq = math.sqrt((2 * annual_demand * ordering_cost) / holding_cost_per_unit)
        return int(eoq)
    
    @staticmethod
    def calculate_reorder_point(
        daily_usage: float,
        lead_time_days: int,
        safety_stock: int = 0
    ) -> int:
        """Calculate reorder point."""
        return int(daily_usage * lead_time_days) + safety_stock
    
    @staticmethod
    def calculate_safety_stock(
        daily_usage: float,
        lead_time_days: int,
        service_level: float = 0.95
    ) -> int:
        """Calculate safety stock based on service level."""
        # Simplified calculation
        import math
        z_score = 1.65 if service_level == 0.95 else 2.33  # Common z-scores
        std_dev = daily_usage * 0.2  # Assume 20% std deviation
        return int(z_score * std_dev * math.sqrt(lead_time_days))
    
    @staticmethod
    def get_inventory_status(
        current_stock: int,
        reorder_point: int,
        safety_stock: int
    ) -> str:
        """Get inventory status."""
        if current_stock <= safety_stock:
            return "CRITICAL"
        elif current_stock <= reorder_point:
            return "REORDER"
        else:
            return "HEALTHY"


class QualityAnalyzer:
    """Analyzes component quality metrics."""
    
    QUALITY_METRICS = {
        "military": {
            "mtbf_hours": 1000000,
            "temp_range": (-55, 125),
            "price_multiplier": 3.0
        },
        "industrial": {
            "mtbf_hours": 100000,
            "temp_range": (-40, 85),
            "price_multiplier": 2.0
        },
        "commercial": {
            "mtbf_hours": 50000,
            "temp_range": (0, 40),
            "price_multiplier": 1.0
        },
        "consumer": {
            "mtbf_hours": 10000,
            "temp_range": (0, 40),
            "price_multiplier": 0.5
        }
    }
    
    CERTIFICATIONS = {
        "military": ["MIL-STD-810", "MIL-SPEC"],
        "industrial": ["ISO 9001", "IEC 60950"],
        "commercial": ["CE", "RoHS"],
        "consumer": ["Generic"]
    }
    
    @classmethod
    def get_mtbf(cls, quality_grade: str) -> int:
        """Get MTBF for quality grade."""
        return cls.QUALITY_METRICS.get(quality_grade, {}).get("mtbf_hours", 0)
    
    @classmethod
    def get_operating_temperature_range(cls, quality_grade: str) -> tuple:
        """Get operating temperature range."""
        return cls.QUALITY_METRICS.get(quality_grade, {}).get("temp_range", (0, 40))
    
    @classmethod
    def get_certifications(cls, quality_grade: str) -> List[str]:
        """Get certifications for quality grade."""
        return cls.CERTIFICATIONS.get(quality_grade, [])
    
    @classmethod
    def calculate_total_cost_of_ownership(
        cls,
        unit_price: float,
        quantity: int,
        mtbf_hours: int = 50000,
        failure_cost: float = 0.0,
        warranty_years: int = 1
    ) -> float:
        """Calculate total cost of ownership."""
        purchase_cost = unit_price * quantity
        
        # Estimate failure-related costs
        failure_rate = 1.0 / (mtbf_hours / 8760) if mtbf_hours > 0 else 0.1
        failure_losses = quantity * failure_rate * warranty_years * failure_cost
        
        total_tco = purchase_cost + failure_losses
        return total_tco


class AgentConfig:
    """Configuration management for the agent."""
    
    def __init__(self):
        import os
        from dotenv import load_dotenv
        
        load_dotenv()
        
        self.budget_limit = float(os.getenv("BUDGET_LIMIT", "10000.0"))
        self.cache_ttl = int(os.getenv("CACHE_TTL", "3600"))
        self.default_quality_grade = os.getenv("DEFAULT_QUALITY_GRADE", "commercial")
        self.max_lead_time_days = int(os.getenv("MAX_LEAD_TIME_DAYS", "30"))
        self.min_availability = float(os.getenv("MIN_AVAILABILITY", "0.5"))
        self.preferred_suppliers = os.getenv("PREFERRED_SUPPLIERS", "digikey,mouser").split(",")
        self.default_optimization_strategy = os.getenv("DEFAULT_OPTIMIZATION_STRATEGY", "balance")
    
    def to_dict(self) -> Dict:
        """Convert config to dictionary."""
        return {
            "budget_limit": self.budget_limit,
            "cache_ttl": self.cache_ttl,
            "default_quality_grade": self.default_quality_grade,
            "max_lead_time_days": self.max_lead_time_days,
            "min_availability": self.min_availability,
            "preferred_suppliers": self.preferred_suppliers,
            "default_optimization_strategy": self.default_optimization_strategy,
        }
