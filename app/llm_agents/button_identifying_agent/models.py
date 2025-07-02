from pydantic import BaseModel, Field


class GooglePlaceButton(BaseModel):
    button_name: str = Field(description="The name of the button element as defined on the ARIA snapshot")
    place_name: str = Field(
        description="The name of the google place - usually the first item in the full_name"
    )
    children: list[dict[str, str]] = Field(
        description="A list of ARIA snapshot metadata items for this button, such as text and img alt attributes"  # noqa: E501
    )


class GooglePlaceButtonResult(BaseModel):
    is_google_place_button: bool = Field(
        description="A boolean flag to indicate whether the ARIA snapshot was determined to be a google place button or not"  # noqa: E501
    )
    aria_snapshot: str = Field(description="The aria_snapshot of the button element")
    rationale: str = Field(
        description="The rationale behind why the ARIA snapshot was determined to be a google place button or not"  # noqa: E501
    )
    button: GooglePlaceButton | None = Field(
        description="The schema representing the google place button", default=None
    )
