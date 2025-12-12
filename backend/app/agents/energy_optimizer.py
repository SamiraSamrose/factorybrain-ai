import numpy as np
from typing import Dict, List, Any
from datetime import datetime, timedelta

class EnergyOptimizerAgent:
    def __init__(self, db_session, raindrop_service):
        self.db = db_session
        self.raindrop = raindrop_service
        self.co2_reduction_target = 0.20
        self.baseline_emissions = None
        self.optimization_actions = []
        
    async def calculate_energy_consumption(self) -> Dict[str, float]:
        machines = await self.db.get_all_machines()
        
        total_power = sum([m.power_consumption for m in machines if m.power_consumption and m.is_active])
        avg_power = np.mean([m.power_consumption for m in machines if m.power_consumption and m.is_active])
        
        co2_emissions = total_power * 0.5
        
        consumption_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "total_power_kw": total_power,
            "average_power_kw": avg_power,
            "estimated_co2_kg": co2_emissions,
            "active_machines": len([m for m in machines if m.is_active])
        }
        
        await self.raindrop.store_energy_metrics(consumption_data)
        
        if self.baseline_emissions is None:
            self.baseline_emissions = co2_emissions
        
        return consumption_data
    
    async def optimize_energy_usage(self) -> Dict[str, Any]:
        machines = await self.db.get_all_machines()
        current_consumption = await self.calculate_energy_consumption()
        
        optimization_plan = {
            "timestamp": datetime.utcnow().isoformat(),
            "current_power_kw": current_consumption["total_power_kw"],
            "current_co2_kg": current_consumption["estimated_co2_kg"],
            "actions": []
        }
        
        high_power_machines = [m for m in machines if m.power_consumption and m.power_consumption > 60]
        high_power_machines.sort(key=lambda x: x.power_consumption, reverse=True)
        
        for machine in high_power_machines[:3]:
            if machine.efficiency < 85:
                action = {
                    "machine_id": machine.machine_id,
                    "action_type": "reduce_load",
                    "current_power": machine.power_consumption,
                    "target_power": machine.power_consumption * 0.85,
                    "expected_savings_kw": machine.power_consumption * 0.15,
                    "reason": "Low efficiency with high power consumption"
                }
                optimization_plan["actions"].append(action)
                await self._apply_power_reduction(machine.machine_id, 0.85)
        
        idle_machines = [m for m in machines if m.status == "idle" and m.power_consumption > 10]
        for machine in idle_machines:
            action = {
                "machine_id": machine.machine_id,
                "action_type": "standby_mode",
                "current_power": machine.power_consumption,
                "target_power": 5,
                "expected_savings_kw": machine.power_consumption - 5,
                "reason": "Machine idle, switching to standby"
            }
            optimization_plan["actions"].append(action)
            await self._apply_standby_mode(machine.machine_id)
        
        total_savings= sum([a["expected_savings_kw"] for a in optimization_plan["actions"]])
optimization_plan["total_savings_kw"] = total_savings
optimization_plan["estimated_co2_reduction_kg"] = total_savings * 0.5
optimization_plan["co2_reduction_percentage"] = (
(optimization_plan["estimated_co2_reduction_kg"] / current_consumption["estimated_co2_kg"]) * 100
if current_consumption["estimated_co2_kg"] > 0 else 0
)
self.optimization_actions.append(optimization_plan)
    return optimization_plan

async def _apply_power_reduction(self, machine_id: str, reduction_factor: float):
    machine = await self.db.get_machine(machine_id)
    machine.power_consumption *= reduction_factor
    await self.db.update_machine(machine)

async def _apply_standby_mode(self, machine_id: str):
    machine = await self.db.get_machine(machine_id)
    machine.power_consumption = 5
    machine.status = "standby"
    await self.db.update_machine(machine)

async def schedule_off_peak_operations(self) -> Dict[str, Any]:
    current_hour = datetime.utcnow().hour
    
    is_off_peak = current_hour < 6 or current_hour > 22
    
    schedule = {
        "timestamp": datetime.utcnow().isoformat(),
        "current_hour": current_hour,
        "is_off_peak": is_off_peak,
        "scheduled_operations": []
    }
    
    if is_off_peak:
        machines = await self.db.get_all_machines()
        non_critical = [m for m in machines if m.type != "critical_production"]
        
        for machine in non_critical[:5]:
            schedule["scheduled_operations"].append({
                "machine_id": machine.machine_id,
                "operation": "maintenance_cycle",
                "scheduled_time": datetime.utcnow().isoformat(),
                "reason": "Off-peak energy pricing"
            })
    
    return schedule

async def calculate_co2_impact(self) -> Dict[str, Any]:
    current_consumption = await self.calculate_energy_consumption()
    
    total_reduction = sum([
        action.get("estimated_co2_reduction_kg", 0)
        for action in self.optimization_actions
    ])
    
    impact_report = {
        "timestamp": datetime.utcnow().isoformat(),
        "baseline_co2_kg": self.baseline_emissions,
        "current_co2_kg": current_consumption["estimated_co2_kg"],
        "total_reduction_kg": total_reduction,
        "reduction_percentage": (total_reduction / self.baseline_emissions * 100) if self.baseline_emissions else 0,
        "target_percentage": self.co2_reduction_target * 100,
        "target_met": (total_reduction / self.baseline_emissions) >= self.co2_reduction_target if self.baseline_emissions else False,
        "optimization_actions_count": len(self.optimization_actions)
    }
    
    return impact_report

async def generate_energy_report(self) -> Dict[str, Any]:
    consumption = await self.calculate_energy_consumption()
    co2_impact = await self.calculate_co2_impact()
    
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "energy_metrics": consumption,
        "co2_impact": co2_impact,
        "recent_optimizations": self.optimization_actions[-10:],
        "recommendations": self._generate_recommendations(consumption, co2_impact)
    }

def _generate_recommendations(self, consumption: Dict, co2_impact: Dict) -> List[str]:
    recommendations = []
    
    if consumption["average_power_kw"] > 50:
        recommendations.append("Consider upgrading to energy-efficient equipment")
    
    if co2_impact.get("reduction_percentage", 0) < co2_impact.get("target_percentage", 20):
        recommendations.append("Increase off-peak operation scheduling")
    
    if len(self.optimization_actions) < 5:
        recommendations.append("Enable continuous energy monitoring for better optimization")
    
    return recommendations