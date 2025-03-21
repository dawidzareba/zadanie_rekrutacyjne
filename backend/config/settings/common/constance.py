CONSTANCE_BACKEND = "constance.backends.database.DatabaseBackend"
CONSTANCE_DATABASE_CACHE_BACKEND = "default"
CONSTANCE_DEFAULT_SETTING_PERMISSIONS = "apps.users.permissions.IsSuperUser"
CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

CONSTANCE_CONFIG = {
    "SHORT_URL_LENGTH": (
        6,
        "Length of the short URL you are looking for",
        int,
    ),
    "GENERATE_URL_MAX_RETRIES": (
        5,
        "Number of maximum retries to generate URLs",
        int,
    ),
}


CONSTANCE_CONFIG_FIELDSETS = {
    "Technical settings": (
        "SHORT_URL_LENGTH",
        "GENERATE_URL_MAX_RETRIES",
    )
}
