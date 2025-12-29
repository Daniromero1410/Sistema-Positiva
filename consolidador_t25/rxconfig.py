"""Reflex configuration for Consolidador T25."""
import reflex as rx
import os

# Database configuration
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/consolidador_t25"
)

config = rx.Config(
    app_name="consolidador_t25",
    db_url=DATABASE_URL,
    tailwind={
        "theme": {
            "extend": {
                "colors": {
                    "positiva": {
                        "green": "#00A651",
                        "green-dark": "#008C45",
                        "green-light": "#E8F5E9",
                        "blue-dark": "#1A365D",
                        "blue-medium": "#2D4A6F",
                        "blue-light": "#EBF4FF",
                        "orange": "#F7941D",
                        "yellow": "#FFC107",
                        "red": "#DC3545",
                    }
                }
            }
        }
    },
)
