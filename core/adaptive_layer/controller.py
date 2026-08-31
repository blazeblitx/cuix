"""
CUIX Phase 11 & Phase 12: Adaptation Controller & Atomic Rollback Manager
Manages real-time DOM adaptations, state snapshots, and instant rollbacks.
"""

from typing import Dict, Any, List, Optional
import time

class AdaptationCheckpoint:
    def __init__(self, checkpoint_id: str, intervention_id: str, target_selector: str, original_style: str):
        self.checkpoint_id = checkpoint_id
        self.intervention_id = intervention_id
        self.target_selector = target_selector
        self.original_style = original_style
        self.timestamp = time.time()
        self.is_active = True

class AdaptationController:
    def __init__(self):
        self.checkpoints: Dict[str, AdaptationCheckpoint] = {}

    def create_checkpoint(self, intervention_id: str, target_selector: str, current_style: str) -> AdaptationCheckpoint:
        chk_id = f"chk_{int(time.time() * 1000)}_{len(self.checkpoints) + 1}"
        checkpoint = AdaptationCheckpoint(chk_id, intervention_id, target_selector, current_style)
        self.checkpoints[chk_id] = checkpoint
        return checkpoint

    def rollback_checkpoint(self, checkpoint_id: str) -> Optional[AdaptationCheckpoint]:
        """Rollback specific adaptation checkpoint."""
        checkpoint = self.checkpoints.get(checkpoint_id)
        if checkpoint and checkpoint.is_active:
            checkpoint.is_active = False
            return checkpoint
        return None

    def rollback_all(self) -> List[AdaptationCheckpoint]:
        """Rolls back all active UI adaptations across the document."""
        rolled_back = []
        for chk in self.checkpoints.values():
            if chk.is_active:
                chk.is_active = False
                rolled_back.append(chk)
        return rolled_back
