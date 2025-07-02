import pyotp


class TOTP:
    def __init__(self, google_2fa_secret: str, google_email: str):
        self.totp = pyotp.TOTP(
            s=google_2fa_secret,
            name=google_email,
            issuer="Google",
            digits=6,
        )

    def now(self):
        return self.totp.now()
