"""Domain-specific exceptions for ClinicFrontDesk."""


class ClinicException(Exception):
    """Base exception for clinic domain errors."""
    def __init__(self, message: str, status_code: int = 400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code


class SlotNotAvailableError(ClinicException):
    """Raised when a requested slot is not open."""
    def __init__(self, slot_id: int, message: str = "Slot is not available"):
        super().__init__(f"{message} (slot_id={slot_id})", status_code=409)
        self.slot_id = slot_id


class SlotAlreadyHeldError(ClinicException):
    """Raised when an atomic hold fails because the slot was already taken."""
    def __init__(self, slot_id: int):
        super().__init__(f"Slot {slot_id} is already held or booked by another transaction", status_code=409)
        self.slot_id = slot_id


class SlotHoldExpiredError(ClinicException):
    """Raised when attempting to confirm or operate on an expired hold."""
    def __init__(self, slot_id: int):
        super().__init__(f"Slot hold for {slot_id} has expired", status_code=410)
        self.slot_id = slot_id


class PatientNotOptedInError(ClinicException):
    """Raised when attempting outreach to a patient without waitlist opt-in."""
    def __init__(self, patient_id: int):
        super().__init__(f"Patient {patient_id} has not opted in to waitlist notifications", status_code=403)
        self.patient_id = patient_id


class ClinicalDetailsViolationError(ClinicException):
    """Raised when outbound message contains prohibited clinical details."""
    def __init__(self, word_or_reason: str):
        super().__init__(f"Safety violation: Outbound message must not contain clinical details: {word_or_reason}", status_code=422)


class ConfirmedAppointmentRequiresApprovalError(ClinicException):
    """Raised when attempting to move a confirmed appointment without doctor approval."""
    def __init__(self, appointment_id: int):
        super().__init__(f"Moving confirmed appointment {appointment_id} requires doctor approval and patient consent", status_code=403)
        self.appointment_id = appointment_id


class NegotiationExchangesExceededError(ClinicException):
    """Raised when negotiation exceeds the maximum configured exchanges."""
    def __init__(self, thread_id: int, exchanges: int):
        super().__init__(f"Negotiation thread {thread_id} reached maximum exchanges ({exchanges})", status_code=400)
        self.thread_id = thread_id


class PatientNotFoundError(ClinicException):
    def __init__(self, identifier: str):
        super().__init__(f"Patient not found: {identifier}", status_code=404)


class AppointmentNotFoundError(ClinicException):
    def __init__(self, appointment_id: int):
        super().__init__(f"Appointment {appointment_id} not found", status_code=404)


class DecisionNotFoundError(ClinicException):
    def __init__(self, decision_id: int):
        super().__init__(f"Decision {decision_id} not found", status_code=404)


class ChannelError(ClinicException):
    """Raised on channel transport issues."""
    def __init__(self, message: str):
        super().__init__(message, status_code=502)
