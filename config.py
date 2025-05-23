from dataclasses import dataclass
from environs import env


@dataclass
class TgBot:
    token: str


@dataclass
class DataBase:
    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str


@dataclass
class GoogleSheet:
    token: str


@dataclass
class Config:
    tg_bot: TgBot
    db: DataBase
    google_sheet: GoogleSheet


def load_config(path: str | None = None) -> Config:
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env("TOKEN")
        ),
        db=DataBase(
            db_host=env("DB_HOST"),
            db_port=env("DB_PORT"),
            db_name=env("DB_NAME"),
            db_user=env("DB_USER"),
            db_pass=env("DB_PASS"),
        ),
        google_sheet=GoogleSheet(
            token=env("GOOGLE_SHEET_TOKEN")
        )
    )
