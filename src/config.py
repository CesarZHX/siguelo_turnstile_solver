"""Configuration."""

from os import environ

from dotenv import load_dotenv
from twocaptcha import TwoCaptcha

load_dotenv()

OFFICE, YEAR, TITLE = (environ[f"SIGUELO_{key}"] for key in ("OFFICE", "YEAR", "TITLE"))

TWO_CAPTCHA_API_KEY: str = environ["2CAPTCHA_API_KEY"]
TWO_CAPTCHA: TwoCaptcha = TwoCaptcha(TWO_CAPTCHA_API_KEY)


GET_TERMS_AGREEDMENT_SCRIPT: str = 'sessionStorage.getItem("termCondi") === "1"'
ACCEPT_TERMS_BTN: str = ".btn-sunarp-cyan"
SIGUELO_URL: str = "https://sigueloplus.sunarp.gob.pe/siguelo/"

CHANNEL: str = "msedge"
HEADLESS: bool = False
