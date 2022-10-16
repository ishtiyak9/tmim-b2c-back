class GenderType:
    M = 'M'
    F = 'F'

    CHOICES = (
        (M, "Male"),
        (F, "Female")
    )


class UserType:
    CUSTOMER = 'Customer'
    VENDOR = 'Vendor'
    CHOICES = (
        (CUSTOMER, "Customer"),
        (VENDOR, "Vendor")
    )


PASS_REST_CONFIRM_EXPIRE_MINUTE = 5


class LanguageType:
    EN = 'en'
    AR = 'ar'

    CHOICES = (
        (EN, "English"),
        (AR, "Arabic"),
    )
