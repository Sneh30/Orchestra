from dataclasses import dataclass


@dataclass(slots=True)
class AppError(Exception):
    code: str
    message: str
    status_code: int = 500
    details: dict[str, object] | None = None


class NotFoundError(AppError):
    def __init__(self, resource: str, identifier: str) -> None:
        super().__init__(
            code="not_found",
            message=f"{resource} '{identifier}' was not found.",
            status_code=404,
            details={"resource": resource, "identifier": identifier},
        )


class ValidationAppError(AppError):
    def __init__(self, message: str, details: dict[str, object] | None = None) -> None:
        super().__init__(code="validation_error", message=message, status_code=422, details=details)


class UnauthorizedError(AppError):
    def __init__(self) -> None:
        super().__init__(
            code="unauthorized",
            message="A valid API key is required for this request.",
            status_code=401,
        )

