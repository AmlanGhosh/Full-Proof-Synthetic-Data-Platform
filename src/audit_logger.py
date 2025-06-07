
"""
Audit logger for storing validation metadata and compliance records.
"""

import json
import datetime
from typing import Dict, Any
import logging

class AuditLogger:
    def __init__(self, log_file: str = "validation_audit.log"):
        self.log_file = log_file
        logging.basicConfig(
            filename=log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def log_validation_event(self, event_type: str, validation_id: str, 
                           data: Dict[str, Any]) -> None:
        """Log validation event with metadata."""
        audit_record = {
            'timestamp': datetime.datetime.utcnow().isoformat(),
            'event_type': event_type,
            'validation_id': validation_id,
            'data': data
        }
        
        self.logger.info(json.dumps(audit_record))
    
    def log_validation_start(self, validation_id: str, config: Dict[str, Any]) -> None:
        """Log start of validation process."""
        self.log_validation_event('VALIDATION_START', validation_id, {
            'config': config,
            'status': 'started'
        })
    
    def log_validation_complete(self, validation_id: str, results: Dict[str, Any]) -> None:
        """Log completion of validation process."""
        self.log_validation_event('VALIDATION_COMPLETE', validation_id, {
            'results': results,
            'status': 'completed'
        })
    
    def log_human_review(self, validation_id: str, reviewer_id: str, 
                        decision: str, notes: str) -> None:
        """Log human review decisions."""
        self.log_validation_event('HUMAN_REVIEW', validation_id, {
            'reviewer_id': reviewer_id,
            'decision': decision,
            'notes': notes,
            'status': 'human_reviewed'
        })
    
    def log_compliance_check(self, validation_id: str, compliance_standard: str,
                           compliance_result: bool) -> None:
        """Log compliance check results."""
        self.log_validation_event('COMPLIANCE_CHECK', validation_id, {
            'standard': compliance_standard,
            'compliant': compliance_result,
            'status': 'compliance_checked'
        })
