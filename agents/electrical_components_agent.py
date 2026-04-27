"""
Main electrical components agent module
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Dict, Optional, Tuple
from datetime import datetime, timedelta
import json


class ComponentType(Enum):
    """Supported electrical component types."""
    RESISTOR = "resistor"
    CAPACITOR = "capacitor"
    INDUCTOR = "inductor"
    DIODE = "diode"
    TRANSISTOR = "transistor"
    MICROCONTROLLER = "microcontroller"
    SENSOR = "sensor"
    CONNECTOR = "connector"
    TRANSFORMER = "transformer"
    RELAY = "relay"
    IC = "ic"
    LED = "led"
    SWITCH = "switch"
    OSCILLATOR = "oscillator"


class QualityGrade(Enum):
    """Component quality grades."""
    INDUSTRIAL = "industrial"  # Widest temperature range, highest reliability
    MILITARY = "military"      # Highest specifications, most testing
    COMMERCIAL = "commercial"  # Standard commercial grade
    CONSUMER = "consumer"       # Consumer/hobbyist grade


class SupplierRating(Enum):
    """Supplier reliability ratings."""
    PREMIUM = "premium"        # Fast delivery, excellent support
    STANDARD = "standard"      # Reliable, standard service
    BUDGET = "budget"          # Low cost, longer delivery times
    SPECIALTY = "specialty"    # Specialized components only


@dataclass
class ComponentSpecification:
    """Specification for an electrical component."""
    component_type: ComponentType
    description: str
    specifications: Dict = field(default_factory=dict)
    quantity: int = 1
    quality_grade: QualityGrade = QualityGrade.COMMERCIAL
    
    def __hash__(self):
        return hash(f"{self.component_type}_{self.description}_{self.quantity}")


@dataclass
class SupplierOffer:
    """An offer from a supplier for a component."""
    supplier_name: str
    supplier_rating: SupplierRating
    component_id: str
    unit_price: float
    quantity_available: int
    lead_time_days: int
    quality_grade: QualityGrade
    availability_score: float
    reliability_score: float
    
    def get_total_cost(self, quantity: int) -> float:
        """Calculate total cost for quantity."""
        return self.unit_price * quantity
    
    def get_value_score(self) -> float:
        """Calculate value score: quality and availability weighted score."""
        quality_weight = 0.4
        availability_weight = 0.3
        reliability_weight = 0.3
        
        quality_factor = 1.0 if self.quality_grade == QualityGrade.MILITARY else \
                        0.9 if self.quality_grade == QualityGrade.INDUSTRIAL else \
                        0.8 if self.quality_grade == QualityGrade.COMMERCIAL else 0.6
        
        return (quality_factor * quality_weight +
                self.availability_score * availability_weight +
                self.reliability_score * reliability_weight)


@dataclass
class SearchResult:
    """Result of a component search."""
    component_spec: ComponentSpecification
    offers: List[SupplierOffer]
    search_timestamp: datetime = field(default_factory=datetime.now)
    
    def get_best_value(self) -> Optional[SupplierOffer]:
        """Get offer with best price-quality ratio."""
        if not self.offers:
            return None
        
        sorted_offers = sorted(
            self.offers,
            key=lambda x: (-x.get_value_score(), x.unit_price)
        )
        return sorted_offers[0]
    
    def get_cheapest(self) -> Optional[SupplierOffer]:
        """Get cheapest offer."""
        if not self.offers:
            return None
        return min(self.offers, key=lambda x: x.unit_price)
    
    def get_fastest_delivery(self) -> Optional[SupplierOffer]:
        """Get offer with fastest delivery."""
        if not self.offers:
            return None
        return min(self.offers, key=lambda x: x.lead_time_days)
    
    def get_highest_quality(self) -> Optional[SupplierOffer]:
        """Get highest quality offer."""
        if not self.offers:
            return None
        
        quality_order = {
            QualityGrade.MILITARY: 4,
            QualityGrade.INDUSTRIAL: 3,
            QualityGrade.COMMERCIAL: 2,
            QualityGrade.CONSUMER: 1
        }
        
        return max(self.offers, key=lambda x: quality_order.get(x.quality_grade, 0))


@dataclass
class PurchaseOrder:
    """A purchase order for components."""
    order_id: str
    components: List[Tuple[ComponentSpecification, SupplierOffer, int]] = field(default_factory=list)
    total_cost: float = 0.0
    expected_delivery: datetime = None
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_component(self, spec: ComponentSpecification, offer: SupplierOffer, quantity: int):
        """Add component to purchase order."""
        self.components.append((spec, offer, quantity))
        self.total_cost += offer.get_total_cost(quantity)
    
    def get_summary(self) -> Dict:
        """Get order summary."""
        return {
            "order_id": self.order_id,
            "total_items": sum(qty for _, _, qty in self.components),
            "total_cost": self.total_cost,
            "expected_delivery": self.expected_delivery.isoformat() if self.expected_delivery else None,
            "suppliers": list(set(offer.supplier_name for _, offer, _ in self.components)),
            "component_count": len(self.components)
        }


class ElectricalComponentsAgent:
    """Main agent for managing electrical component searches and procurement."""
    
    def __init__(self, config: Optional[Dict] = None):
        """Initialize the agent.
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.search_history: List[SearchResult] = []
        self.purchase_orders: List[PurchaseOrder] = []
        self.supplier_database = self._initialize_supplier_database()
        self.component_database = self._initialize_component_database()
        self.budget_limit = self.config.get("budget_limit", 10000.0)
        self.current_spend = 0.0
    
    def _initialize_supplier_database(self) -> Dict[str, Dict]:
        """Initialize supplier database with sample data."""
        return {
            "digikey": {
                "rating": SupplierRating.PREMIUM,
                "reliability_score": 0.95,
                "avg_lead_time": 2,
                "specialties": ["electronics", "industrial", "commercial"]
            },
            "mouser": {
                "rating": SupplierRating.PREMIUM,
                "reliability_score": 0.94,
                "avg_lead_time": 2,
                "specialties": ["electronics", "industrial"]
            },
            "aliexpress": {
                "rating": SupplierRating.BUDGET,
                "reliability_score": 0.70,
                "avg_lead_time": 14,
                "specialties": ["consumer", "hobbyist"]
            },
            "newark": {
                "rating": SupplierRating.STANDARD,
                "reliability_score": 0.90,
                "avg_lead_time": 3,
                "specialties": ["commercial", "industrial"]
            },
            "bisco": {
                "rating": SupplierRating.STANDARD,
                "reliability_score": 0.88,
                "avg_lead_time": 3,
                "specialties": ["industrial", "commercial"]
            }
        }
    
    def _initialize_component_database(self) -> Dict[str, List[SupplierOffer]]:
        """Initialize component database with sample data."""
        return {
            "resistor_sample": [
                SupplierOffer("digikey", SupplierRating.PREMIUM, "RES-1K-0.25W-DK", 0.08, 10000, 1, QualityGrade.INDUSTRIAL, 0.95, 0.95),
                SupplierOffer("mouser", SupplierRating.PREMIUM, "RES-1K-0.25W-MS", 0.09, 8000, 1, QualityGrade.COMMERCIAL, 0.90, 0.94),
                SupplierOffer("aliexpress", SupplierRating.BUDGET, "RES-1K-0.25W-AE", 0.02, 50000, 14, QualityGrade.CONSUMER, 0.85, 0.70),
            ],
            "capacitor_sample": [
                SupplierOffer("digikey", SupplierRating.PREMIUM, "CAP-10UF-50V-DK", 0.25, 5000, 1, QualityGrade.INDUSTRIAL, 0.98, 0.95),
                SupplierOffer("mouser", SupplierRating.PREMIUM, "CAP-10UF-50V-MS", 0.27, 4500, 1, QualityGrade.INDUSTRIAL, 0.92, 0.94),
                SupplierOffer("aliexpress", SupplierRating.BUDGET, "CAP-10UF-50V-AE", 0.08, 20000, 14, QualityGrade.CONSUMER, 0.80, 0.70),
            ],
            "transistor_sample": [
                SupplierOffer("digikey", SupplierRating.PREMIUM, "TRN-2N2222-DK", 0.35, 3000, 1, QualityGrade.INDUSTRIAL, 0.95, 0.95),
                SupplierOffer("newark", SupplierRating.STANDARD, "TRN-2N2222-NK", 0.38, 2500, 3, QualityGrade.COMMERCIAL, 0.85, 0.90),
                SupplierOffer("aliexpress", SupplierRating.BUDGET, "TRN-2N2222-AE", 0.12, 15000, 14, QualityGrade.CONSUMER, 0.75, 0.70),
            ]
        }
    
    def search_components(
        self,
        component_type: ComponentType,
        specifications: Optional[Dict] = None,
        quality_grade: QualityGrade = QualityGrade.COMMERCIAL,
        max_price_per_unit: Optional[float] = None,
        min_availability: float = 0.5,
        max_lead_time_days: Optional[int] = None
    ) -> SearchResult:
        """Search for components matching criteria."""
        spec = ComponentSpecification(
            component_type=component_type,
            description=f"{component_type.value}_{json.dumps(specifications or {})}",
            specifications=specifications or {},
            quality_grade=quality_grade
        )
        
        sample_key = f"{component_type.value}_sample"
        offers = self.component_database.get(sample_key, [])
        
        filtered_offers = []
        for offer in offers:
            if max_price_per_unit and offer.unit_price > max_price_per_unit:
                continue
            if offer.availability_score < min_availability:
                continue
            if max_lead_time_days and offer.lead_time_days > max_lead_time_days:
                continue
            
            quality_order = {QualityGrade.MILITARY: 4, QualityGrade.INDUSTRIAL: 3,
                           QualityGrade.COMMERCIAL: 2, QualityGrade.CONSUMER: 1}
            if quality_order.get(offer.quality_grade, 0) < quality_order.get(quality_grade, 0):
                continue
            
            filtered_offers.append(offer)
        
        result = SearchResult(spec, filtered_offers)
        self.search_history.append(result)
        return result
    
    def compare_offers(self, search_result: SearchResult) -> Dict:
        """Compare all offers in a search result."""
        if not search_result.offers:
            return {"error": "No offers available"}
        
        return {
            "total_offers": len(search_result.offers),
            "best_value": {
                "supplier": search_result.get_best_value().supplier_name,
                "price": search_result.get_best_value().unit_price,
                "value_score": search_result.get_best_value().get_value_score()
            },
            "cheapest": {
                "supplier": search_result.get_cheapest().supplier_name,
                "price": search_result.get_cheapest().unit_price,
                "savings_vs_best": search_result.get_best_value().unit_price - search_result.get_cheapest().unit_price
            },
            "fastest_delivery": {
                "supplier": search_result.get_fastest_delivery().supplier_name,
                "lead_time_days": search_result.get_fastest_delivery().lead_time_days
            },
            "highest_quality": {
                "supplier": search_result.get_highest_quality().supplier_name,
                "quality_grade": search_result.get_highest_quality().quality_grade.value
            },
            "average_price": sum(o.unit_price for o in search_result.offers) / len(search_result.offers),
            "price_range": {
                "min": min(o.unit_price for o in search_result.offers),
                "max": max(o.unit_price for o in search_result.offers)
            }
        }
    
    def optimize_purchase_order(
        self,
        components: List[Tuple[SearchResult, int]],
        optimization_strategy: str = "balance"
    ) -> PurchaseOrder:
        """Optimize purchase order based on strategy."""
        if self.current_spend >= self.budget_limit:
            raise ValueError("Budget limit reached")
        
        order_id = f"PO-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        order = PurchaseOrder(order_id)
        
        max_delivery_days = 0
        
        for search_result, quantity in components:
            if optimization_strategy == "price":
                offer = search_result.get_cheapest()
            elif optimization_strategy == "quality":
                offer = search_result.get_highest_quality()
            elif optimization_strategy == "delivery":
                offer = search_result.get_fastest_delivery()
            else:
                offer = search_result.get_best_value()
            
            cost = offer.get_total_cost(quantity)
            if self.current_spend + cost > self.budget_limit:
                raise ValueError(f"Adding this component exceeds budget")
            
            order.add_component(search_result.component_spec, offer, quantity)
            self.current_spend += cost
            max_delivery_days = max(max_delivery_days, offer.lead_time_days)
        
        order.expected_delivery = datetime.now() + timedelta(days=max_delivery_days)
        self.purchase_orders.append(order)
        
        return order
    
    def get_search_history(self) -> List[Dict]:
        """Get search history."""
        return [
            {
                "timestamp": result.search_timestamp.isoformat(),
                "component_type": result.component_spec.component_type.value,
                "offers_found": len(result.offers),
                "best_price": result.get_cheapest().unit_price if result.offers else None
            }
            for result in self.search_history
        ]
    
    def get_agent_status(self) -> Dict:
        """Get current agent status."""
        return {
            "searches_performed": len(self.search_history),
            "purchase_orders_created": len(self.purchase_orders),
            "budget_utilization": {
                "spent": self.current_spend,
                "limit": self.budget_limit,
                "remaining": self.budget_limit - self.current_spend,
                "percentage_used": (self.current_spend / self.budget_limit * 100) if self.budget_limit > 0 else 0
            },
            "suppliers_used": list(set(
                offer.supplier_name 
                for order in self.purchase_orders 
                for _, offer, _ in order.components
            )),
            "last_search": self.search_history[-1].search_timestamp.isoformat() if self.search_history else None
        }
