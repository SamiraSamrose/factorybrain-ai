import asyncio
from typing import Dict, List, Any
from datetime import datetime, timedelta
import random

class ProcurementAgent:
    def __init__(self, db_session, anthropic_service):
        self.db = db_session
        self.anthropic = anthropic_service
        self.suppliers = {}
        self.negotiation_history = []
        self.cost_savings = 0.0
        
    async def monitor_inventory_levels(self) -> List[Dict[str, Any]]:
        inventory_items = await self.db.get_all_inventory()
        low_stock_items = []
        
        for item in inventory_items:
            if item.quantity <= item.reorder_level:
                low_stock_items.append({
                    "part_number": item.part_number,
                    "part_name": item.part_name,
                    "current_quantity": item.quantity,
                    "reorder_level": item.reorder_level,
                    "urgency": "critical" if item.quantity == 0 else "high"
                })
        
        return low_stock_items
    
    async def initiate_procurement(self, part_number: str, quantity: int, urgency: str = "medium") -> Dict[str, Any]:
        part = await self.db.get_inventory_item(part_number)
        
        suppliers = await self._find_suppliers(part_number)
        best_supplier = await self._negotiate_with_suppliers(suppliers, part_number, quantity, urgency)
        
        order = {
            "order_id": f"PO-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}",
            "part_name": part.part_name,
            "part_number": part_number,
            "quantity": quantity,
            "supplier": best_supplier["name"],
            "unit_price": best_supplier["quoted_price"],
            "total_price": best_supplier["quoted_price"] * quantity,
            "negotiated_price": best_supplier["negotiated_price"],
            "savings": (best_supplier["quoted_price"] - best_supplier["negotiated_price"]) * quantity,
            "status": "requested",
            "urgency": urgency,
            "estimated_delivery": datetime.utcnow() + timedelta(days=best_supplier["delivery_days"]),
            "created_at": datetime.utcnow()
        }
        
        self.cost_savings += order["savings"]
        await self.db.create_procurement_order(order)
        
        return order
    
    async def _find_suppliers(self, part_number: str) -> List[Dict[str, Any]]:
        supplier_database = [
            {"name": "Industrial Parts Co", "reliability": 0.95, "base_price_factor": 1.0},
            {"name": "MachineSupply Direct", "reliability": 0.90, "base_price_factor": 0.92},
            {"name": "Precision Components Ltd", "reliability": 0.88, "base_price_factor": 0.95},
            {"name": "Global Manufacturing Supplies", "reliability": 0.93, "base_price_factor": 0.98}
        ]
        
        available_suppliers = []
        for supplier in supplier_database:
            base_price = random.uniform(50, 200)
            available_suppliers.append({
                "name": supplier["name"],
                "quoted_price": base_price * supplier["base_price_factor"],
                "reliability": supplier["reliability"],
                "delivery_days": random.randint(2, 7)
            })
        
        return available_suppliers
    
    async def _negotiate_with_suppliers(self, suppliers: List[Dict], part_number: str, quantity: int, urgency: str) -> Dict[str, Any]:
        best_deal = None
        best_score = 0
        
        for supplier in suppliers:
            negotiation_prompt = f"""
            Negotiate pricing for industrial spare part procurement:
            Part: {part_number}
            Quantity: {quantity}
            Supplier: {supplier['name']}
            Quoted Price: ${supplier['quoted_price']:.2f}
            Urgency: {urgency}
            
            Provide a negotiation strategy and target price reduction.
            """
            
            negotiation_response = await self.anthropic.generate_negotiation_strategy(negotiation_prompt)
            
            target_reduction = 0.05 if urgency == "critical" else 0.12
            negotiated_price = supplier["quoted_price"] * (1 - target_reduction)
            
            deal_score = (
                (supplier["quoted_price"] - negotiated_price) * quantity * 0.4 +
                supplier["reliability"] * 100 * 0.3 +
                (10 - supplier["delivery_days"]) * 5 * 0.3
            )
            
            if deal_score > best_score:
                best_score = deal_score
                best_deal = {
                    **supplier,
                    "negotiated_price": negotiated_price,
                    "negotiation_strategy": negotiation_response,
                    "deal_score": deal_score
                }
        
        self.negotiation_history.append({
            "timestamp": datetime.utcnow().isoformat(),
            "part_number": part_number,
            "best_supplier": best_deal["name"],
            "savings": (best_deal["quoted_price"] - best_deal["negotiated_price"]) * quantity
        })
        
        return best_deal
    
    async def approve_purchase(self, order_id: str, approver: str) -> Dict[str, Any]:
        order = await self.db.get_procurement_order(order_id)
        
        order.status = "ordered"
        order.approved_by = approver
        await self.db.update_procurement_order(order)
        
        return {
            "order_id": order_id,
            "status": "approved_and_ordered",
            "approved_by": approver,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def track_delivery(self, order_id: str) -> Dict[str, Any]:
        order = await self.db.get_procurement_order(order_id)
        
        days_since_order = (datetime.utcnow() - order.created_at).days
        estimated_days = (order.estimated_delivery - order.created_at).days
        
        if days_since_order >= estimated_days:
            status = "delivered"
        elif days_since_order >= estimated_days * 0.7:
            status = "shipped"
        else:
            status = "ordered"
        
        return {
            "order_id": order_id,
            "current_status": status,
            "days_elapsed": days_since_order,
            "estimated_delivery": order.estimated_delivery.isoformat()
        }
    
    async def generate_procurement_report(self) -> Dict[str, Any]:
        orders = await self.db.get_all_procurement_orders()
        
        return {
            "timestamp": datetime.utcnow().isoformat(),
            "total_orders": len(orders),
            "total_spent": sum([o.total_price for o in orders]),
            "total_savings": self.cost_savings,
            "pending_orders": len([o for o in orders if o.status in ["requested", "ordered"]]),
            "average_delivery_time": np.mean([o.actual_delivery - o.created_at for o in orders if o.actual_delivery]),
            "top_suppliers": self._calculate_top_suppliers(orders)
        }
    
    def _calculate_top_suppliers(self, orders: List) -> List[Dict[str, Any]]:
        supplier_stats = {}
        
        for order in orders:
            if order.supplier not in supplier_stats:
                supplier_stats[order.supplier] = {"orders": 0, "total_value": 0}
            supplier_stats[order.supplier]["orders"] += 1
            supplier_stats[order.supplier]["total_value"] += order.total_price
        
        return sorted(
            [{"supplier": k, **v} for k, v in supplier_stats.items()],
            key=lambda x: x["total_value"],
            reverse=True
        )[:5]