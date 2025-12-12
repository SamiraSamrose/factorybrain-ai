import asyncio
from typing import Dict, List, Any
from datetime import datetime
import numpy as np

class PlantOptimizationAgent:
    def __init__(self, db_session, raindrop_service, cerebras_service):
        self.db = db_session
        self.raindrop = raindrop_service
        self.cerebras = cerebras_service
        self.kpis = {}
        self.sub_agents = []
        self.optimization_history = []
        
    async def monitor_kpis(self) -> Dict[str, float]:
        machines = await self.db.get_all_machines()
        
        total_efficiency = np.mean([m.efficiency for m in machines if m.efficiency])
        avg_health = np.mean([m.health_score for m in machines])
        total_power = sum([m.power_consumption for m in machines if m.power_consumption])
        failure_risk = np.mean([m.failure_probability for m in machines])
        
        self.kpis = {
            "overall_efficiency": total_efficiency,
            "average_health": avg_health,
            "total_power_consumption": total_power,
            "failure_risk": failure_risk,
            "active_machines": len([m for m in machines if m.is_active]),
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.raindrop.store_kpis(self.kpis)
        return self.kpis
    
    async def optimize_workload_distribution(self, production_demand: float) -> Dict[str, Any]:
        machines = await self.db.get_all_machines()
        available_machines = [m for m in machines if m.status == "operational" and m.health_score > 70]
        
        workload_allocation = {}
        total_capacity = sum([m.efficiency for m in available_machines])
        
        for machine in available_machines:
            allocation_ratio = machine.efficiency / total_capacity
            workload = production_demand * allocation_ratio
            
            energy_factor = 1.0
            if machine.power_consumption > 50:
                energy_factor = 0.85
            
            workload_allocation[machine.machine_id] = {
                "allocated_load": workload * energy_factor,
                "efficiency": machine.efficiency,
                "health_score": machine.health_score,
                "power_consumption": machine.power_consumption
            }
        
        optimization_result = {
            "timestamp": datetime.utcnow().isoformat(),
            "production_demand": production_demand,
            "workload_allocation": workload_allocation,
            "total_efficiency": np.mean([m.efficiency for m in available_machines]),
            "estimated_power": sum([m.power_consumption * workload_allocation[m.machine_id]["allocated_load"] / 100 
                                   for m in available_machines if m.machine_id in workload_allocation])
        }
        
        self.optimization_history.append(optimization_result)
        return optimization_result
    
    async def direct_sub_agents(self) -> List[Dict[str, Any]]:
        kpis = await self.monitor_kpis()
        directives = []
        
        if kpis["failure_risk"] > 0.6:
            directives.append({
                "agent": "anomaly_detector",
                "action": "increase_monitoring_frequency",
                "reason": "High failure risk detected"
            })
        
        if kpis["total_power_consumption"] > 1000:
            directives.append({
                "agent": "energy_optimizer",
                "action": "activate_reduction_mode",
                "reason": "Power consumption exceeds threshold"
            })
        
        if kpis["average_health"] < 75:
            directives.append({
                "agent": "procurement_agent",
                "action": "prepare_spare_parts_inventory",
                "reason": "Overall health declining"
            })
        
        return directives
    
    async def generate_optimization_report(self) -> Dict[str, Any]:
        kpis = await self.monitor_kpis()
        
        report = {
            "timestamp": datetime.utcnow().isoformat(),
            "current_kpis": kpis,
            "optimization_actions": len(self.optimization_history),
            "sub_agent_directives": await self.direct_sub_agents(),
            "recommendations": []
        }
        
        if kpis["overall_efficiency"] < 80:
            report["recommendations"].append("Consider workload redistribution to higher efficiency machines")
        
        if kpis["failure_risk"] > 0.5:
            report["recommendations"].append("Schedule preventive maintenance for high-risk machines")
        
        return report