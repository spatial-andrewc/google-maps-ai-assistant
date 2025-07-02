import asyncio
import re

from playwright.async_api import Page, Playwright, async_playwright

from app.browser.auth.totp import TOTP
from app.llm_agents.button_identifying_agent.agent import (
    ButtonIdentifyingAgent,
)
from app.llm_agents.button_identifying_agent.models import GooglePlaceButton
from app.llm_agents.recommendations_graph.graph import RecommendationsGraph

GOOGLE_MAPS_URL = "https://google.com/maps"

GOOGLE_BUTTONS_TO_IGNORE = [
    ["\ue5c4"],
    ["\ue8b6"],
    ["\ue5cd"],
    ["\ue5d2"],
    ["\ue866Saved"],
    ["\ue889Recents"],
    ["\ue32cGet the app"],
    ["\ue5d4"],
    ["\ue80dShare"],
    ["\ue5de"],
    ["\ue55c"],
    ["Terms"],
    ["Privacy"],
    ["Send product feedback"],
    ["1 km "],
    ['- button "Add note": Note'],
]


class GoogleMapsTravelAssistant:
    def __init__(
        self,
        google_email: str,
        google_password: str,
        google_2fa_secret: str,
        button_identifying_agent: ButtonIdentifyingAgent,
        recommendations_graph: RecommendationsGraph,
        traveller_profile: str,
        list_name: str,
    ):
        self.google_email = google_email
        self.google_password = google_password
        self.totp = TOTP(google_2fa_secret=google_2fa_secret, google_email=google_email)
        self.button_identifying_agent = button_identifying_agent
        self.traveller_profile = traveller_profile
        self.recommendations_graph = recommendations_graph
        self.list_name = list_name

    async def launch_browser(self, playwright: Playwright):
        browser = await playwright.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()
        await page.goto(GOOGLE_MAPS_URL)
        return page

    async def login(self, page: Page):
        await page.get_by_role("link", name="Sign in").click()
        await page.get_by_role("textbox", name="Email or phone").fill(self.google_email)
        await page.get_by_role("button", name="Next").click()
        await page.get_by_role("textbox", name="Enter your password").fill(self.google_password)
        await page.get_by_role("button", name="Next").click()
        await page.get_by_role("textbox", name="Enter code").click()
        await page.get_by_role("textbox", name="Enter code").fill(self.totp.now())
        await page.get_by_role("button", name="Next").click()

    async def navigate_to_list(self, page: Page):
        await page.wait_for_url("**/maps/@*", timeout=10000)
        await page.get_by_role("button", name="Menu").click()
        await page.get_by_role("menuitem", name="Saved").click()
        await page.get_by_role("button", name=re.compile(self.list_name, re.IGNORECASE)).click()

    async def get_place_buttons(self, page: Page) -> list[GooglePlaceButton]:
        await page.wait_for_timeout(3000)

        place_button_asyncio_tasks = []
        for button in await page.get_by_role("button").all():
            text_content = await button.all_text_contents()
            if (
                len(text_content) > 0
                and text_content[0].strip()
                and text_content not in GOOGLE_BUTTONS_TO_IGNORE
            ):
                aria_snapshot = await button.aria_snapshot()
                place_button_asyncio_tasks.append(
                    self.button_identifying_agent.identify_button(aria_snapshot)
                )

        return [
            place_button.button
            for place_button in (await asyncio.gather(*place_button_asyncio_tasks))
            if place_button.button
        ]

    async def add_note_to_place(self, page: Page, button_name: str, place_name: str, recommendation: str):
        await page.get_by_role("button", name=re.compile(button_name, re.IGNORECASE)).click()

        await page.get_by_role("button", name="Show place lists details").click()

        await page.get_by_role(
            "button", name=re.compile(f"Add note in {self.list_name}", re.IGNORECASE)
        ).click()

        await page.get_by_role("dialog").get_by_role("textbox").fill(recommendation)
        await page.get_by_role("button", name="Done").click()

    async def run(self):
        async with async_playwright() as playwright:
            page = await self.launch_browser(playwright=playwright)

            await self.login(page=page)
            await self.navigate_to_list(page=page)

            place_buttons = await self.get_place_buttons(page=page)
            place_recommendations = await self.recommendations_graph.get_recommendations(
                locations=[place_button.place_name for place_button in place_buttons],
                traveller_profile=self.traveller_profile,
            )

            for place_button, recommendation in zip(place_buttons, place_recommendations, strict=True):
                await self.add_note_to_place(
                    page=page,
                    button_name=place_button.button_name,
                    place_name=place_button.place_name,
                    recommendation=recommendation,
                )

            await page.pause()
