import asyncio
from elevenlabs import generate, Voice
from typing import Dict, Any

class VoiceService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.voice_id = "21m00Tcm4TlvDq8ikWAM"
        self.alert_history = []
        
    async def generate_voice_alert(self, message: str, severity: str = "medium") -> Dict[str, Any]:
        voice_settings = {
            "stability": 0.75,
            "similarity_boost": 0.85
        }
        
        if severity == "critical":
            message = f"CRITICAL ALERT: {message}"
            voice_settings["stability"] = 0.9
        elif severity == "high":
            message = f"High Priority Alert: {message}"
        
        try:
            audio = generate(
                text=message,
                voice=Voice(voice_id=self.voice_id),
                model="eleven_monolingual_v1",
                api_key=self.api_key
            )
            
            alert_record = {
                "message": message,
                "severity": severity,
                "timestamp": datetime.utcnow().isoformat(),
                "audio_generated": True
            }
            
            self.alert_history.append(alert_record)
            
            return {
                "success": True,
                "audio_data": audio,
                "message": message,
                "severity": severity
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "message": message
            }
    
    async def alert_machine_overheating(self, machine_id: str, temperature: float):
        message = f"Machine {machine_id} bearings overheating. Current temperature: {temperature} degrees Celsius. Immediate inspection required."
        return await self.generate_voice_alert(message, severity="critical")
    
    async def provide_repair_steps(self, machine_id: str, issue_type: str) -> Dict[str, Any]:
        repair_instructions = {
            "overheating": [
                "Step 1: Shut down the machine immediately",
                "Step 2: Allow cooling period of 30 minutes",
                "Step 3: Inspect bearing lubrication levels",
                "Step 4: Check cooling system functionality",
                "Step 5: Replace bearings if wear detected"
            ],
            "mechanical_stress": [
                "Step 1: Reduce operational load to 50 percent",
                "Step 2: Inspect mounting bolts and fasteners",
                "Step 3: Check alignment of rotating components",
                "Step 4: Measure vibration levels with diagnostic tool",
                "Step 5: Replace worn components as needed"
            ],
            "pressure_abnormality": [
                "Step 1: Check all pressure sensors for accuracy",
                "Step 2: Inspect hydraulic lines for leaks",
                "Step 3: Verify pump operation",
                "Step 4: Clean or replace filters",
                "Step 5: Recalibrate pressure control systems"
            ]
        }
        
        steps = repair_instructions.get(issue_type, ["Contact maintenance supervisor for specialized guidance"])
        
        full_message = f"Repair instructions for Machine {machine_id}, issue type {issue_type}. "
        full_message += ". ".join(steps)
        
        voice_response = await self.generate_voice_alert(full_message, severity="medium")
        
        return {
            "machine_id": machine_id,
            "issue_type": issue_type,
            "repair_steps": steps,
            "voice_alert": voice_response
        }
    
    async def log_verbal_instruction(self, operator_id: str, instruction: str) -> Dict[str, Any]:
        log_entry = {
            "operator_id": operator_id,
            "instruction": instruction,
            "timestamp": datetime.utcnow().isoformat(),
            "logged": True
        }
        
        confirmation_message = f"Instruction logged from operator {operator_id}: {instruction}"
        voice_confirmation = await self.generate_voice_alert(confirmation_message, severity="low")
        
        return {
            "log_entry": log_entry,
            "voice_confirmation": voice_confirmation
        }
    
    async def generate_status_update(self, machines_status: Dict[str, str]) -> Dict[str, Any]:
        operational = len([s for s in machines_status.values() if s == "operational"])
        total = len(machines_status)
        
        message = f"Plant status update. {operational} of {total} machines operational. "
        
        issues = [mid for mid, status in machines_status.items() if status != "operational"]
        if issues:
            message += f"Machines requiring attention: {', '.join(issues[:3])}"
        else:
            message += "All systems functioning normally."
        
        return await self.generate_voice_alert(message, severity="low")
