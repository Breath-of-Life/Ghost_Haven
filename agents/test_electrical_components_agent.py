"""
Unit tests for Electrical Components Agent
"""

import pytest
from datetime import datetime, timedelta
from electrical_components_agent import (
    ElectricalComponentsAgent,
    ComponentType,
    QualityGrade,
    ComponentSpecification,
    SupplierOffer,
    SupplierRating,
    SearchResult,
)


class TestComponentSpecification:
    """Tests for ComponentSpecification class."""
    
    def test_create_component_specification(self):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor",
            specifications={"resistance": "1k", "power": "0.25w"}
        )
        assert spec.component_type == ComponentType.RESISTOR
        assert spec.description == "1k Resistor"
        assert spec.quantity == 1
    
    def test_component_specification_hash(self):
        spec1 = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor",
            quantity=1
        )
        spec2 = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor",
            quantity=1
        )
        assert hash(spec1) == hash(spec2)


class TestSupplierOffer:
    """Tests for SupplierOffer class."""
    
    def test_create_supplier_offer(self):
        offer = SupplierOffer(
            supplier_name="DigiKey",
            supplier_rating=SupplierRating.PREMIUM,
            component_id="RES-1K",
            unit_price=0.10,
            quantity_available=5000,
            lead_time_days=2,
            quality_grade=QualityGrade.INDUSTRIAL,
            availability_score=0.95,
            reliability_score=0.95
        )
        assert offer.supplier_name == "DigiKey"
        assert offer.unit_price == 0.10
    
    def test_get_total_cost(self):
        offer = SupplierOffer(
            supplier_name="DigiKey",
            supplier_rating=SupplierRating.PREMIUM,
            component_id="RES-1K",
            unit_price=0.10,
            quantity_available=5000,
            lead_time_days=2,
            quality_grade=QualityGrade.INDUSTRIAL,
            availability_score=0.95,
            reliability_score=0.95
        )
        assert offer.get_total_cost(100) == 10.0
    
    def test_get_value_score(self):
        offer = SupplierOffer(
            supplier_name="DigiKey",
            supplier_rating=SupplierRating.PREMIUM,
            component_id="RES-1K",
            unit_price=0.10,
            quantity_available=5000,
            lead_time_days=2,
            quality_grade=QualityGrade.INDUSTRIAL,
            availability_score=0.95,
            reliability_score=0.95
        )
        score = offer.get_value_score()
        assert 0 <= score <= 1


class TestSearchResult:
    """Tests for SearchResult class."""
    
    @pytest.fixture
    def sample_offers(self):
        return [
            SupplierOffer("DigiKey", SupplierRating.PREMIUM, "RES-1K-DK", 0.08, 5000, 2,
                         QualityGrade.INDUSTRIAL, 0.95, 0.95),
            SupplierOffer("Mouser", SupplierRating.PREMIUM, "RES-1K-MS", 0.09, 4000, 2,
                         QualityGrade.COMMERCIAL, 0.90, 0.94),
            SupplierOffer("AliExpress", SupplierRating.BUDGET, "RES-1K-AE", 0.02, 50000, 14,
                         QualityGrade.CONSUMER, 0.85, 0.70),
        ]
    
    def test_create_search_result(self, sample_offers):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor"
        )
        result = SearchResult(spec, sample_offers)
        assert len(result.offers) == 3
    
    def test_get_best_value(self, sample_offers):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor"
        )
        result = SearchResult(spec, sample_offers)
        best = result.get_best_value()
        assert best is not None
        assert best.supplier_name in ["DigiKey", "Mouser"]
    
    def test_get_cheapest(self, sample_offers):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor"
        )
        result = SearchResult(spec, sample_offers)
        cheapest = result.get_cheapest()
        assert cheapest.supplier_name == "AliExpress"
        assert cheapest.unit_price == 0.02
    
    def test_get_fastest_delivery(self, sample_offers):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor"
        )
        result = SearchResult(spec, sample_offers)
        fastest = result.get_fastest_delivery()
        assert fastest.lead_time_days == 2
    
    def test_get_highest_quality(self, sample_offers):
        spec = ComponentSpecification(
            component_type=ComponentType.RESISTOR,
            description="1k Resistor"
        )
        result = SearchResult(spec, sample_offers)
        highest = result.get_highest_quality()
        assert highest.quality_grade == QualityGrade.INDUSTRIAL


class TestElectricalComponentsAgent:
    """Tests for main ElectricalComponentsAgent class."""
    
    @pytest.fixture
    def agent(self):
        return ElectricalComponentsAgent(config={"budget_limit": 5000.0})
    
    def test_agent_initialization(self, agent):
        assert agent.budget_limit == 5000.0
        assert agent.current_spend == 0.0
        assert len(agent.search_history) == 0
        assert len(agent.purchase_orders) == 0
    
    def test_search_components(self, agent):
        result = agent.search_components(
            component_type=ComponentType.RESISTOR,
            specifications={"resistance": "1k"},
            quality_grade=QualityGrade.COMMERCIAL
        )
        assert result is not None
        assert len(agent.search_history) == 1
    
    def test_search_with_price_filter(self, agent):
        result = agent.search_components(
            component_type=ComponentType.RESISTOR,
            max_price_per_unit=0.05
        )
        # Should filter out offers above price limit
        for offer in result.offers:
            assert offer.unit_price <= 0.05
    
    def test_search_with_quality_filter(self, agent):
        result = agent.search_components(
            component_type=ComponentType.RESISTOR,
            quality_grade=QualityGrade.INDUSTRIAL
        )
        # All offers should meet quality requirement
        for offer in result.offers:
            quality_order = {
                QualityGrade.MILITARY: 4,
                QualityGrade.INDUSTRIAL: 3,
                QualityGrade.COMMERCIAL: 2,
                QualityGrade.CONSUMER: 1
            }
            assert quality_order.get(offer.quality_grade, 0) >= quality_order.get(QualityGrade.INDUSTRIAL, 0)
    
    def test_compare_offers(self, agent):
        result = agent.search_components(ComponentType.RESISTOR)
        comparison = agent.compare_offers(result)
        
        assert "best_value" in comparison
        assert "cheapest" in comparison
        assert "fastest_delivery" in comparison
        assert "highest_quality" in comparison
        assert "average_price" in comparison
    
    def test_optimize_purchase_order_price(self, agent):
        result = agent.search_components(ComponentType.RESISTOR)
        order = agent.optimize_purchase_order([(result, 100)], optimization_strategy="price")
        
        assert order is not None
        assert len(order.components) == 1
        assert order.total_cost > 0
    
    def test_optimize_purchase_order_quality(self, agent):
        result = agent.search_components(ComponentType.RESISTOR)
        order = agent.optimize_purchase_order([(result, 100)], optimization_strategy="quality")
        
        assert order is not None
        for spec, offer, qty in order.components:
            assert offer.quality_grade >= QualityGrade.COMMERCIAL
    
    def test_optimize_purchase_order_delivery(self, agent):
        result = agent.search_components(ComponentType.RESISTOR)
        order = agent.optimize_purchase_order([(result, 50)], optimization_strategy="delivery")
        
        assert order is not None
        # Check that selected offers have reasonable lead times
        for spec, offer, qty in order.components:
            assert offer.lead_time_days >= 0
    
    def test_optimize_purchase_order_balance(self, agent):
        result = agent.search_components(ComponentType.RESISTOR)
        order = agent.optimize_purchase_order([(result, 75)], optimization_strategy="balance")
        
        assert order is not None
        assert order.expected_delivery is not None
    
    def test_budget_enforcement(self, agent):
        # Set very low budget
        agent.budget_limit = 0.50
        result = agent.search_components(ComponentType.RESISTOR)
        
        # Should raise error when trying to exceed budget
        with pytest.raises(ValueError):
            agent.optimize_purchase_order([(result, 100)], optimization_strategy="price")
    
    def test_multiple_component_order(self, agent):
        result1 = agent.search_components(ComponentType.RESISTOR)
        result2 = agent.search_components(ComponentType.CAPACITOR)
        
        order = agent.optimize_purchase_order(
            [(result1, 50), (result2, 30)],
            optimization_strategy="balance"
        )
        
        assert len(order.components) == 2
    
    def test_search_history(self, agent):
        agent.search_components(ComponentType.RESISTOR)
        agent.search_components(ComponentType.CAPACITOR)
        
        history = agent.get_search_history()
        assert len(history) == 2
    
    def test_agent_status(self, agent):
        agent.search_components(ComponentType.RESISTOR)
        result = agent.search_components(ComponentType.CAPACITOR)
        agent.optimize_purchase_order([(result, 50)], optimization_strategy="price")
        
        status = agent.get_agent_status()
        
        assert status["searches_performed"] == 2
        assert status["purchase_orders_created"] == 1
        assert "budget_utilization" in status
        assert status["budget_utilization"]["spent"] > 0
    
    def test_empty_search_results(self, agent):
        result = agent.search_components(
            component_type=ComponentType.RESISTOR,
            max_price_per_unit=0.001  # Unrealistic price
        )
        assert len(result.offers) == 0


class TestSupplierDatabase:
    """Tests for supplier database initialization."""
    
    def test_supplier_database_initialization(self):
        agent = ElectricalComponentsAgent()
        assert len(agent.supplier_database) > 0
        assert "digikey" in agent.supplier_database
        assert "mouser" in agent.supplier_database
    
    def test_component_database_initialization(self):
        agent = ElectricalComponentsAgent()
        assert len(agent.component_database) > 0
        
        for component_list in agent.component_database.values():
            assert len(component_list) > 0
            for offer in component_list:
                assert isinstance(offer, SupplierOffer)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
