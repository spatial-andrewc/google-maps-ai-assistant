from enum import StrEnum, auto

from pydantic import BaseModel


class TravellerDemographic(BaseModel):
    name: str
    age: int
    gender: str
    relationship_status: str
    nationality: str
    cultural_background: str
    languages_spoken: list[str]


class TransportationStyle(StrEnum):
    walkable = auto()
    public_transit = auto()
    rental_car = auto()
    e_mobility = auto()


class AccommodationPreference(StrEnum):
    hostel = auto()
    hotel = auto()
    Airbnb = auto()
    camping = auto()


class TravellerContext(BaseModel):
    destinations: list[str]
    start_day: int
    start_month: int
    end_day: int
    end_month: int
    budget_low: int
    budget_high: int
    accommodation_preference: list[AccommodationPreference]
    transportation_style: list[TransportationStyle]


class TravellerInterests(BaseModel):
    activity_types: list[str]
    pace: str
    social_preferences: str


class PlanningStyle(StrEnum):
    spontaneous = "spontaneous"
    flexible = "flexible"
    detailed = "detailed"


class DiscoveryPreference(StrEnum):
    hidden_gems = "hidden_gems"
    iconic_landmarks = "iconic_landmarks"
    trending_spots = "trending_spots"
    local_favorites = "local_favorites"


class ImmersionLevel(StrEnum):
    cultural_immersion = "cultural_immersion"
    balanced = "balanced"
    comfort_zone = "comfort_zone"


class TravellerPersonality(BaseModel):
    planning_style: PlanningStyle
    discovery_preferences: list[DiscoveryPreference]
    immersion_level: ImmersionLevel
    eco_conscious: bool
    photo_driven: bool
    textual_overview: str


class TravellerProfile(BaseModel):
    demographic: TravellerDemographic
    context: TravellerContext
    interests: TravellerInterests
    personality: TravellerPersonality
