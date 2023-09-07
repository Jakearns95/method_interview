from enum import Enum


class EntityStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    INCOMPLETE = "incomplete"


class AccountStatus(str, Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    CLOSED = "closed"
    PROCESSING = "processing"


class PaymentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SENT = "sent"
    FAILED = "failed"
    CANCELED = "canceled"
    REVERSAL_REQUIRED = "reversal_required"
    REVERSAL_PROCESSING = "reversal_processing"
    REVERSED = "reversed"
