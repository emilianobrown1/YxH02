import time
from typing import Dict, List

class BarracksManager:
    TRAINING_DETAILS = {
        "shinobi": {"cost": 1_000_000, "time_per_troop": 5},
        "wizard": {"cost": 2_000_000, "time_per_troop": 10},
        "sensei": {"cost": 3_000_000, "time_per_troop": 15}
    }
    
    BARRACKS_CAPACITY = 5

    def __init__(self):
        self.barracks: List[Dict] = []  # Format: [{"purchase_time": float, "training_queue": []}, ...]
        self.troops: Dict[str, int] = {"shinobi": 0, "wizard": 0, "sensei": 0}

    def initialize_barracks(self, raw_barracks_data):
        """Migrate old barracks data to new format"""
        if not isinstance(self.barracks, list):
            self.barracks = []
            
        for entry in raw_barracks_data:
            if isinstance(entry, dict):
                if "training_queue" not in entry:
                    self.barracks.append({
                        "purchase_time": entry.get("timestamp", time.time()),
                        "training_queue": []
                    })
                else:
                    self.barracks.append(entry)
            else:
                self.barracks.append({
                    "purchase_time": entry,
                    "training_queue": []
                })

    def process_completed_trainings(self):
        """Move completed trainings to available troops"""
        current_time = time.time()
        completed = {"shinobi": 0, "wizard": 0, "sensei": 0}

        for barrack in self.barracks:
            to_remove = []
            for idx, batch in enumerate(barrack["training_queue"]):
                if current_time >= batch["start_time"] + batch["duration"]:
                    completed[batch["troop_type"]] += batch["quantity"]
                    to_remove.append(idx)
            
            # Remove in reverse order to preserve indices
            for idx in reversed(to_remove):
                del barrack["training_queue"][idx]

        for troop, count in completed.items():
            self.troops[troop] += count

        return completed

    def get_available_capacity(self):
        """Calculate available training slots"""
        return sum(
            self.BARRACKS_CAPACITY - sum(b["quantity"] for b in barrack["training_queue"])
            for barrack in self.barracks
        )

    def start_training(self, troop_type: str, quantity: int, user_gold: int) -> int:
        """Returns: (gold_cost, training_duration)"""
        if troop_type not in self.TRAINING_DETAILS:
            raise ValueError("Invalid troop type")

        detail = self.TRAINING_DETAILS[troop_type]
        max_possible = min(quantity, self.get_available_capacity())
        
        if max_possible <= 0:
            return (0, 0)

        total_cost = detail["cost"] * max_possible
        if user_gold < total_cost:
            return (0, 0)

        # Calculate duration (max time for parallel batches)
        training_duration = detail["time_per_troop"] * 60  # Convert to seconds
        
        # Distribute across barracks
        remaining = max_possible
        for barrack in self.barracks:
            available = self.BARRACKS_CAPACITY - sum(b["quantity"] for b in barrack["training_queue"])
            assign = min(available, remaining)
            
            if assign > 0:
                barrack["training_queue"].append({
                    "troop_type": troop_type,
                    "quantity": assign,
                    "start_time": time.time(),
                    "duration": training_duration
                })
                remaining -= assign
                
            if remaining == 0:
                break

        return (total_cost, training_duration)

    def get_ongoing_trainings(self):
        ongoing = {"shinobi": 0, "wizard": 0, "sensei": 0}
        for barrack in self.barracks:
            for batch in barrack["training_queue"]:
                ongoing[batch["troop_type"]] += batch["quantity"]
        return ongoing

    def get_barracks_status(self):
        status = []
        for idx, barrack in enumerate(self.barracks, 1):
            if barrack["training_queue"]:
                batch = barrack["training_queue"][0]
                remaining = (batch["start_time"] + batch["duration"] - time.time()) // 60
                status.append(f"Barrack #{idx}: Training {batch['quantity']} {batch['troop_type']}s ({remaining}m left)")
            else:
                status.append(f"Barrack #{idx}: 🟢 Ready")
        return status