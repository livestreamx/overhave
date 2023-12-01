import enum


class TestRunStatus(enum.StrEnum):
    """Enum for test run statuses."""

    __test__ = False

    STARTED = "STARTED"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"
    INTERNAL_ERROR = "INTERNAL_ERROR"

    @property
    def finished(self) -> bool:
        return self in (TestRunStatus.FAILED, TestRunStatus.SUCCESS, TestRunStatus.INTERNAL_ERROR)


class TestReportStatus(str, enum.Enum):
    """Enum for test run statuses."""

    __test__ = False

    EMPTY = "EMPTY"
    GENERATION_FAILED = "GENERATION_FAILED"
    GENERATED = "GENERATED"
    SAVED = "SAVED"

    @property
    def has_report(self) -> bool:
        return self in (TestReportStatus.GENERATED, TestReportStatus.SAVED)


class EmulationStatus(enum.StrEnum):
    """Enum for emulation statuses."""

    CREATED = "CREATED"
    REQUESTED = "REQUESTED"
    READY = "READY"
    ERROR = "ERROR"

    @property
    def processed(self) -> bool:
        return self in (EmulationStatus.READY, EmulationStatus.ERROR)


class DraftStatus(enum.StrEnum):
    """Enum for draft statuses."""

    REQUESTED = "REQUESTED"
    CREATING = "CREATING"
    CREATED = "CREATED"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DUPLICATE = "DUPLICATE"

    @property
    def is_succeed(self) -> bool:
        return self in (DraftStatus.CREATED, DraftStatus.DUPLICATE)
