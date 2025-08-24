import requests
from locust import HttpUser, between, task

from config import HOST


class RestfulBookerUser(HttpUser):
    host = HOST
    wait_time = between(1, 3)
    token: str | None = None
    booking_id: int | None = None

    def on_start(self) -> None:
        """Executed at the start of each virtual user"""
        self.login()
        self.create_booking()

    def login(self) -> None:
        """Authentication and token retrieval"""
        response = self.client.post(
            "/auth",
            json={
                "username": "admin",
                "password": "password123",
            },
        )
        if response.status_code == requests.codes.ok:
            self.token = response.json()["token"]

    def create_booking(self) -> None:
        """Create a test booking"""
        booking_data = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2023-01-01",
                "checkout": "2023-01-05",
            },
            "additionalneeds": "Breakfast",
        }
        response = self.client.post(
            "/booking",
            json=booking_data,
            headers={"Content-Type": "application/json"},
        )
        if response.status_code == requests.codes.ok:
            self.booking_id = response.json()["bookingid"]

    @task
    def get_all_bookings(self) -> None:
        """Get all bookings"""
        self.client.get("/booking")

    @task
    def get_booking_by_id(self) -> None:
        """Get a specific booking"""
        if self.booking_id:
            self.client.get(f"/booking/{self.booking_id}")

    @task
    def update_booking(self) -> None:
        """Full booking update"""
        if self.booking_id and self.token:
            updated_data = {
                "firstname": "James",
                "lastname": "Brown",
                "totalprice": 222,
                "depositpaid": True,
                "bookingdates": {
                    "checkin": "2023-01-01",
                    "checkout": "2023-01-10",
                },
                "additionalneeds": "Lunch",
            }
            self.client.put(
                f"/booking/{self.booking_id}",
                json=updated_data,
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"token={self.token}",
                },
            )

    @task
    def partial_update_booking(self) -> None:
        """Partial booking update"""
        if self.booking_id and self.token:
            patch_data = {
                "additionalneeds": "Dinner",
            }
            self.client.patch(
                f"/booking/{self.booking_id}",
                json=patch_data,
                headers={
                    "Content-Type": "application/json",
                    "Cookie": f"token={self.token}",
                },
            )

    @task
    def delete_booking(self) -> None:
        """Delete booking"""
        if self.booking_id and self.token:
            self.client.delete(
                f"/booking/{self.booking_id}",
                headers={"Cookie": f"token={self.token}"},
            )
            # After deletion, create a new booking
            self.create_booking()
