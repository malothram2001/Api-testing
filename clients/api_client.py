
import requests


class APIClient:
    def __init__(
        self,
        base_url: str,
        token: str = "",
        timeout: float = 15,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

        self.session.headers.update({
            "Accept": "application/json",
        })

        if token:
            self.session.headers["Authorization"] = (
                f"Bearer {token}"
            )

    def request(self, method: str, path: str, **kwargs):
        if not path or not path.strip():
            raise ValueError(
                "API path is missing. Set ADD_FARMER_PATH in .env."
            )

        url = f"{self.base_url}/{path.lstrip('/')}"

        return self.session.request(
            method=method.upper(),
            url=url,
            timeout=self.timeout,
            **kwargs,
        )

    def close(self) -> None:
        self.session.close()
