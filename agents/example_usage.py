"""
Example usage of the Electrical Components Agent
"""

from electrical_components_agent import (
    ElectricalComponentsAgent,
    ComponentType,
    QualityGrade,
)


def example_basic_search():
    """Example 1: Basic component search"""
    print("=" * 60)
    print("EXAMPLE 1: Basic Component Search")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent()
    
    # Search for 1k resistors with commercial grade
    result = agent.search_components(
        component_type=ComponentType.RESISTOR,
        specifications={"resistance": "1k", "power": "0.25w"},
        quality_grade=QualityGrade.COMMERCIAL,
        max_price_per_unit=0.15
    )
    
    print(f"Found {len(result.offers)} offers")
    for i, offer in enumerate(result.offers, 1):
        print(f"{i}. {offer.supplier_name}: ${offer.unit_price} "
              f"(Lead: {offer.lead_time_days}d, Stock: {offer.quantity_available})")


def example_offer_comparison():
    """Example 2: Detailed offer comparison"""
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Detailed Offer Comparison")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent()
    
    # Search for capacitors
    result = agent.search_components(
        component_type=ComponentType.CAPACITOR,
        specifications={"capacitance": "10uf", "voltage": "50v"},
        quality_grade=QualityGrade.INDUSTRIAL
    )
    
    # Get comparison analysis
    comparison = agent.compare_offers(result)
    
    print(f"Total offers: {comparison['total_offers']}")
    print(f"\nBest Value: {comparison['best_value']['supplier']} - ${comparison['best_value']['price']}")
    print(f"Cheapest: {comparison['cheapest']['supplier']} - ${comparison['cheapest']['price']}")
    print(f"Fastest Delivery: {comparison['fastest_delivery']['supplier']} - {comparison['fastest_delivery']['lead_time_days']} days")
    print(f"Highest Quality: {comparison['highest_quality']['supplier']} - {comparison['highest_quality']['quality_grade']}")
    print(f"\nPrice Statistics:")
    print(f"  Average: ${comparison['average_price']:.2f}")
    print(f"  Range: ${comparison['price_range']['min']:.2f} - ${comparison['price_range']['max']:.2f}")


def example_purchase_order_optimization():
    """Example 3: Purchase order with price optimization"""
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Purchase Order Optimization (Price)")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent()
    
    # Search for multiple components
    resistor_result = agent.search_components(
        component_type=ComponentType.RESISTOR,
        specifications={"resistance": "1k", "power": "0.25w"},
        quality_grade=QualityGrade.COMMERCIAL
    )
    
    transistor_result = agent.search_components(
        component_type=ComponentType.TRANSISTOR,
        specifications={"model": "2n2222"},
        quality_grade=QualityGrade.COMMERCIAL
    )
    
    # Create purchase order optimized for price
    components = [
        (resistor_result, 100),
        (transistor_result, 50)
    ]
    
    order = agent.optimize_purchase_order(components, optimization_strategy="price")
    
    summary = order.get_summary()
    print(f"Order ID: {summary['order_id']}")
    print(f"Total Items: {summary['total_items']}")
    print(f"Total Cost: ${summary['total_cost']:.2f}")
    print(f"Expected Delivery: {summary['expected_delivery']}")
    print(f"Suppliers: {', '.join(summary['suppliers'])}")


def example_quality_focused_order():
    """Example 4: Purchase order with quality optimization"""
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Purchase Order Optimization (Quality)")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent()
    
    # Search for components with industrial quality
    resistor_result = agent.search_components(
        component_type=ComponentType.RESISTOR,
        specifications={"resistance": "1k", "power": "0.25w"},
        quality_grade=QualityGrade.INDUSTRIAL
    )
    
    capacitor_result = agent.search_components(
        component_type=ComponentType.CAPACITOR,
        specifications={"capacitance": "10uf", "voltage": "50v"},
        quality_grade=QualityGrade.INDUSTRIAL
    )
    
    components = [
        (resistor_result, 150),
        (capacitor_result, 75)
    ]
    
    order = agent.optimize_purchase_order(components, optimization_strategy="quality")
    
    summary = order.get_summary()
    print(f"Order ID: {summary['order_id']}")
    print(f"Total Items: {summary['total_items']}")
    print(f"Total Cost: ${summary['total_cost']:.2f}")
    print(f"Components Ordered: {summary['component_count']}")
    
    # Show what was ordered
    for spec, offer, qty in order.components:
        print(f"  - {spec.component_type.value}: {qty} units from {offer.supplier_name} @ ${offer.unit_price}/ea")


def example_agent_status():
    """Example 5: Check agent status"""
    print("\n" + "=" * 60)
    print("EXAMPLE 5: Agent Status Report")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent(config={"budget_limit": 1000.0})
    
    # Perform some searches
    for _ in range(3):
        agent.search_components(
            component_type=ComponentType.RESISTOR,
            max_price_per_unit=0.10
        )
    
    # Create an order
    result = agent.search_components(
        component_type=ComponentType.RESISTOR,
        quality_grade=QualityGrade.COMMERCIAL
    )
    agent.optimize_purchase_order([(result, 100)])
    
    # Get status
    status = agent.get_agent_status()
    
    print(f"Searches Performed: {status['searches_performed']}")
    print(f"Purchase Orders Created: {status['purchase_orders_created']}")
    print(f"\nBudget Status:")
    print(f"  Total Limit: ${status['budget_utilization']['limit']:.2f}")
    print(f"  Spent: ${status['budget_utilization']['spent']:.2f}")
    print(f"  Remaining: ${status['budget_utilization']['remaining']:.2f}")
    print(f"  Utilization: {status['budget_utilization']['percentage_used']:.1f}%")
    print(f"\nSuppliers Used: {', '.join(status['suppliers_used']) if status['suppliers_used'] else 'None'}")


def example_delivery_optimization():
    """Example 6: Fast delivery optimization"""
    print("\n" + "=" * 60)
    print("EXAMPLE 6: Delivery Optimization")
    print("=" * 60)
    
    agent = ElectricalComponentsAgent()
    
    result = agent.search_components(
        component_type=ComponentType.TRANSISTOR,
        specifications={"model": "2n2222"}
    )
    
    # Get fastest delivery option
    fastest = result.get_fastest_delivery()
    print(f"Fastest delivery: {fastest.supplier_name} in {fastest.lead_time_days} days @ ${fastest.unit_price}")
    
    # Optimize for delivery
    order = agent.optimize_purchase_order(
        [(result, 50)],
        optimization_strategy="delivery"
    )
    
    summary = order.get_summary()
    print(f"Expected Delivery: {summary['expected_delivery']}")


if __name__ == "__main__":
    example_basic_search()
    example_offer_comparison()
    example_purchase_order_optimization()
    example_quality_focused_order()
    example_delivery_optimization()
    example_agent_status()
    
    print("\n" + "=" * 60)
    print("All examples completed successfully!")
    print("=" * 60)
