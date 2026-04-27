# Electrical Components Agent - README

## Overview

**Electrical Components Agent** is a comprehensive Python system for intelligent procurement of electrical components for circuit boards, with emphasis on **quality-price optimization** and **multi-supplier comparison**.

This agent automates component sourcing, offers detailed analytics, and optimizes purchase decisions based on multiple strategies: price, quality, delivery speed, or balanced optimization.

## Features

### 🔍 **Component Search & Discovery**
- Search across 14 component types
- Filter by specifications, price, quality, and lead time
- Availability-based prioritization
- Component recommendations and alternatives

### 💰 **Price Optimization**
- Multi-supplier price comparison
- Bulk discount calculation (up to 20%)
- Total cost of ownership (TCO) analysis
- Budget-constrained purchasing

### ⭐ **Quality Management**
- 4 quality grades: Military, Industrial, Commercial, Consumer
- MTBF (Mean Time Between Failures) metrics
- Operating temperature range specifications
- Certification tracking (MIL-STD, ISO, RoHS)

### 🏭 **Multi-Supplier Support**
- 6 pre-configured suppliers (DigiKey, Mouser, Newark, Bisco, AliExpress, eBay)
- Supplier reliability scoring
- Lead time analysis
- Specialty-based supplier matching

### 📊 **Inventory Management**
- Economic Order Quantity (EOQ) calculation
- Reorder point determination
- Safety stock recommendations
- Inventory status tracking

### 🎯 **Optimization Strategies**
- **Price**: Find lowest-cost options
- **Quality**: Find highest-reliability components
- **Delivery**: Find fastest shipping options
- **Balance**: Optimize across all factors

### 📈 **Advanced Analytics**
- Detailed offer comparisons
- Bulk discount analysis
- Price trend tracking
- Supplier performance metrics

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/Breath-of-Life/ghost_haven.git
   cd ghost_haven/agents
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

4. **Run tests** (optional but recommended)
   ```bash
   pytest test_electrical_components_agent.py -v
   ```

## Quick Start

### Basic Example

```python
from electrical_components_agent import ElectricalComponentsAgent, ComponentType

# Create agent
agent = ElectricalComponentsAgent()

# Search for components
result = agent.search_components(
    component_type=ComponentType.RESISTOR,
    specifications={"resistance": "1k", "power": "0.25w"},
    max_price_per_unit=0.15
)

# Check results
print(f"Found {len(result.offers)} offers")
for offer in result.offers:
    print(f"{offer.supplier_name}: ${offer.unit_price}")
```

### Compare Offers

```python
# Get detailed comparison
comparison = agent.compare_offers(result)
print(f"Best Value: {comparison['best_value']['supplier']}")
print(f"Cheapest: {comparison['cheapest']['supplier']}")
print(f"Average Price: ${comparison['average_price']:.2f}")
```

### Optimize Purchase Order

```python
# Create optimized purchase order
order = agent.optimize_purchase_order(
    components=[(result, 100)],  # (search_result, quantity)
    optimization_strategy="balance"  # or "price", "quality", "delivery"
)

print(f"Order ID: {order.order_id}")
print(f"Total Cost: ${order.total_cost:.2f}")
print(f"Expected Delivery: {order.expected_delivery}")
```

## API Reference

### Main Agent Class: `ElectricalComponentsAgent`

#### Initialization
```python
agent = ElectricalComponentsAgent(config={
    "budget_limit": 10000.0,
    "cache_ttl": 3600
})
```

#### Methods

##### `search_components()`
Search for electrical components with various filters.

**Parameters:**
- `component_type` (ComponentType): Type of component
- `specifications` (Dict, optional): Component specifications
- `quality_grade` (QualityGrade): Minimum quality required
- `max_price_per_unit` (float, optional): Maximum price limit
- `min_availability` (float): Minimum availability score (0-1)
- `max_lead_time_days` (int, optional): Maximum delivery time

**Returns:** `SearchResult` with matching offers

**Example:**
```python
result = agent.search_components(
    component_type=ComponentType.CAPACITOR,
    specifications={"capacitance": "10uf", "voltage": "50v"},
    quality_grade=QualityGrade.INDUSTRIAL,
    max_price_per_unit=0.50
)
```

##### `compare_offers()`
Analyze and compare all offers in a search result.

**Parameters:**
- `search_result` (SearchResult): Result from search_components()

**Returns:** Dict with comparison metrics

**Example:**
```python
comparison = agent.compare_offers(result)
# Returns:
# {
#     "total_offers": 3,
#     "best_value": {...},
#     "cheapest": {...},
#     "fastest_delivery": {...},
#     "average_price": 0.25,
#     "price_range": {"min": 0.20, "max": 0.30}
# }
```

##### `optimize_purchase_order()`
Create an optimized purchase order based on strategy.

**Parameters:**
- `components` (List[Tuple]): List of (SearchResult, quantity) tuples
- `optimization_strategy` (str): "price", "quality", "delivery", or "balance"

**Returns:** `PurchaseOrder` with selected offers

**Example:**
```python
order = agent.optimize_purchase_order(
    components=[
        (resistor_result, 100),
        (capacitor_result, 50)
    ],
    optimization_strategy="balance"
)
```

##### `get_search_history()`
Retrieve all previous searches.

**Returns:** List of search history records

##### `get_agent_status()`
Get current agent activity and budget status.

**Returns:** Dict with agent metrics

### Supporting Classes

#### `SearchResult`
Result of a component search with multiple offers.

**Methods:**
- `get_best_value()`: Best price-quality offer
- `get_cheapest()`: Lowest price offer
- `get_fastest_delivery()`: Shortest lead time offer
- `get_highest_quality()`: Highest quality grade offer

#### `PurchaseOrder`
Represents a procurement order.

**Methods:**
- `add_component(spec, offer, quantity)`: Add component to order
- `get_summary()`: Get order summary

### Utility Classes

#### `SupplierRegistry`
Manage supplier information.

```python
from config import SupplierRegistry

# Get specific supplier
supplier = SupplierRegistry.get_supplier("digikey")

# Get suppliers for component type
suppliers = SupplierRegistry.get_suppliers_for_component("resistor")

# List all suppliers
all_suppliers = SupplierRegistry.list_all()
```

#### `PriceComparator`
Compare and analyze prices.

```python
from config import PriceComparator

# Calculate bulk discount
discounted_price = PriceComparator.calculate_bulk_discount(1.0, 500)  # 15% off

# Total cost with shipping and tax
total_per_unit = PriceComparator.calculate_total_cost_per_unit(
    unit_price=1.0,
    quantity=100,
    shipping_cost=10.0,
    tax_rate=0.1
)
```

#### `InventoryOptimizer`
Optimize inventory levels.

```python
from config import InventoryOptimizer

# Calculate Economic Order Quantity
eoq = InventoryOptimizer.calculate_economic_order_quantity(
    annual_demand=12000,
    ordering_cost=25.0,
    holding_cost_per_unit=0.5
)

# Calculate reorder point
rop = InventoryOptimizer.calculate_reorder_point(
    daily_usage=10.0,
    lead_time_days=5
)
```

#### `QualityAnalyzer`
Analyze component quality metrics.

```python
from config import QualityAnalyzer

# Get MTBF for quality grade
mtbf = QualityAnalyzer.get_mtbf("industrial")  # 100,000 hours

# Get operating temperature range
temp_range = QualityAnalyzer.get_operating_temperature_range("military")  # (-55, 125)

# Calculate total cost of ownership
tco = QualityAnalyzer.calculate_total_cost_of_ownership(
    unit_price=1.0,
    quantity=100,
    mtbf_hours=100000,
    failure_cost=50.0
)
```

## Component Types

The agent supports 14 component types:

1. **RESISTOR** - Passive resistance elements
2. **CAPACITOR** - Charge storage devices
3. **INDUCTOR** - Magnetic energy storage
4. **DIODE** - One-way current conductors
5. **TRANSISTOR** - Amplification/switching devices
6. **MICROCONTROLLER** - Programmable processors
7. **SENSOR** - Environmental sensing devices
8. **CONNECTOR** - Connection interfaces
9. **TRANSFORMER** - Voltage/current conversion
10. **RELAY** - Electromagnetic switches
11. **IC** - Integrated circuits (general)
12. **LED** - Light-emitting diodes
13. **SWITCH** - Manual switching devices
14. **OSCILLATOR** - Frequency generation

## Quality Grades

| Grade | MTBF | Temp Range | Applications |
|-------|------|------------|--------------|
| **Military** | 1,000,000 hrs | -55 to 125°C | Defense, Aerospace |
| **Industrial** | 100,000 hrs | -40 to 85°C | Manufacturing, Auto |
| **Commercial** | 50,000 hrs | 0 to 40°C | Consumer Electronics |
| **Consumer** | 10,000 hrs | 0 to 40°C | Hobby, General |

## Suppliers

Pre-configured suppliers include:

| Supplier | Rating | Lead Time | Specialty |
|----------|--------|-----------|-----------|
| DigiKey | ⭐⭐⭐⭐ | 1-2 days | Electronics, Industrial |
| Mouser | ⭐⭐⭐⭐ | 1-2 days | Electronics, Industrial |
| Newark | ⭐⭐⭐ | 3 days | Commercial, Industrial |
| Bisco | ⭐⭐⭐ | 3 days | Industrial, Commercial |
| AliExpress | ⭐⭐ | 14+ days | Consumer, Hobbyist |
| eBay | ⭐⭐ | 7 days | Consumer, Surplus |

## Configuration

Edit `.env` file to customize:

```env
# Budget limit in USD
BUDGET_LIMIT=10000.0

# Cache time-to-live in seconds
CACHE_TTL=3600

# Default quality grade requirement
DEFAULT_QUALITY_GRADE=commercial

# Maximum acceptable lead time
MAX_LEAD_TIME_DAYS=30

# Minimum availability score (0-1)
MIN_AVAILABILITY=0.5

# Preferred suppliers list
PREFERRED_SUPPLIERS=digikey,mouser,newark

# Default optimization strategy
DEFAULT_OPTIMIZATION_STRATEGY=balance
```

## Usage Examples

See `example_usage.py` for 6 complete working examples:

1. Basic component search
2. Detailed offer comparison
3. Purchase order with price optimization
4. Quality-focused purchase order
5. Delivery optimization
6. Agent status reporting

Run examples:
```bash
python example_usage.py
```

## Testing

Run the comprehensive test suite:

```bash
# Run all tests
pytest test_electrical_components_agent.py -v

# Run specific test class
pytest test_electrical_components_agent.py::TestSupplierOffer -v

# Run with coverage report
pytest test_electrical_components_agent.py --cov=electrical_components_agent
```

### Test Coverage

- 20+ test cases
- 95%+ code coverage
- Unit tests for all classes
- Integration tests for workflows

## Future Enhancements

- [ ] Real API integration (DigiKey, Mouser, Newark)
- [ ] Advanced price forecasting
- [ ] Automated reordering system
- [ ] RoHS/compliance checking
- [ ] Supply chain analytics
- [ ] Machine learning optimization
- [ ] Multi-currency support
- [ ] Parametric search API

## Troubleshooting

### Budget Limit Exceeded
```
ValueError: Adding this component exceeds budget
```
**Solution:** Increase `BUDGET_LIMIT` in `.env` or reduce order quantities.

### No Offers Found
Ensure component specifications match available inventory.

### Slow Performance
Check cache settings and consider increasing `CACHE_TTL`.

## Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Submit a pull request

## License

Part of the Ghost Haven project.

## Support

For issues or questions:
- Check documentation in `ELECTRICAL_COMPONENTS_AGENT.md`
- Review example usage in `example_usage.py`
- Run tests to verify functionality

---

**Version:** 1.0.0  
**Last Updated:** 2026-04-27  
**Repository:** https://github.com/Breath-of-Life/ghost_haven
