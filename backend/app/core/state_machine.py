"""State machine definitions and validation for Slots, Appointments, Threads, and Decisions."""
from datetime import datetime, timezone
from enum import Enum
from typing import Optional
from app.core.exceptions import ClinicException


class SlotStatus(str, Enum):
    OPEN = "OPEN"
    HELD = "HELD"
    CONFIRMED = "CONFIRMED"


class AppointmentStatus(str, Enum):
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"
    PENDING_MOVE = "PENDING_MOVE"


class ThreadStatus(str, Enum):
    ACTIVE = "ACTIVE"
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    EXPIRED = "EXPIRED"
    HANDOFF = "HANDOFF"


class MessageDirection(str, Enum):
    OUTBOUND = "OUTBOUND"
    INBOUND = "INBOUND"


class MessageIntent(str, Enum):
    ACCEPTED = "ACCEPTED"
    DECLINED = "DECLINED"
    COUNTER = "COUNTER"
    OFF_SCRIPT = "OFF_SCRIPT"
    NO_ANSWER = "NO_ANSWER"


class DecisionType(str, Enum):
    DISPLACEMENT_APPROVAL = "DISPLACEMENT_APPROVAL"
    EMERGENCY_SCHEDULING = "EMERGENCY_SCHEDULING"
    OFF_SCRIPT_HANDOFF = "OFF_SCRIPT_HANDOFF"
    EXCHANGE_LIMIT_EXCEEDED = "EXCHANGE_LIMIT_EXCEEDED"
    UNAVAILABLE_SLOT_REQUEST = "UNAVAILABLE_SLOT_REQUEST"


class DecisionStatus(str, Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"


class SlotStateMachine:
    """Enforces allowed state transitions for slots."""

    VALID_TRANSITIONS = {
        SlotStatus.OPEN: {SlotStatus.HELD},
        SlotStatus.HELD: {SlotStatus.CONFIRMED, SlotStatus.OPEN},
        SlotStatus.CONFIRMED: {SlotStatus.OPEN},  # upon cancellation
    }

    @classmethod
    def validate_transition(cls, from_status: SlotStatus, to_status: SlotStatus) -> bool:
        allowed = cls.VALID_TRANSITIONS.get(from_status, set())
        if to_status not in allowed:
            raise ClinicException(
                f"Invalid slot transition from {from_status.value} to {to_status.value}"
            )
        return True

    @staticmethod
    def is_expired(hold_expires_at: Optional[datetime]) -> bool:
        if not hold_expires_at:
            return False
        # Normalize comparison
        if hold_expires_at.tzinfo is None:
            return datetime.utcnow() > hold_expires_at
        return datetime.now(timezone.utc) > hold_expires_at
