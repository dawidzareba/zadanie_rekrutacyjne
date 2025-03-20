from django.db import models
import random
import string


class Url(models.Model):
    original_url = models.URLField(max_length=2048)
    short_code = models.CharField(max_length=10, unique=True, db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    @classmethod
    def _process_short_code(cls, length: int) -> str | None:
        characters = string.ascii_letters + string.digits
        short_code = "".join(random.choice(characters) for _ in range(length))
        if not cls.objects.filter(short_code=short_code).exists():
            return short_code

        return None

    @classmethod
    def _generate_short_code(cls, max_attempts: int, length: int) -> str | None:
        for _ in range(max_attempts):
            short_code = cls._process_short_code(length=length)
            if short_code:
                return short_code

        return None

    @classmethod
    def create_short_code(cls, length=6):
        max_attempts = 10
        short_code = cls._generate_short_code(max_attempts=max_attempts, length=length)

        if not short_code:
            return cls.create_short_code(length=length + 1)

        return short_code
