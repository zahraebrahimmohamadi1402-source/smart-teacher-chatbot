def classify_input(text, speech_confident=True):
    """
    تشخیص نوع ورودی دانش‌آموز

    UNCLEAR:
        ورودی واقعاً نامفهوم است.

    OFF_TOPIC:
        ورودی واضح است ولی فرمان املا نیست.
    """

    text = text.strip()

    # هیچ چیزی دریافت نشده
    if not text:
        return "UNCLEAR"

    # اگر سیستم تشخیص صدا اعلام کند
    # که صدا نامطمئن بوده
    if speech_confident is False:
        return "UNCLEAR"

    # در حالت فعلی که با کیبورد تست می‌کنیم،
    # هر متن واضحی که فرمان املا نباشد،
    # خارج از موضوع محسوب می‌شود.
    return "OFF_TOPIC"