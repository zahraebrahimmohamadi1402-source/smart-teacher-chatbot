# تشخیص فرمان‌های دستیار املا


COMMANDS = {
    "START": [
        "آماده‌ام",
        "آماده ام"
    ],

    "REPEAT": [
        "تکرار کن",
        "تکرارکن",
        "دوباره بگو"
    ],

    "WROTE": [
        "نوشتم"
    ],

    "DID_NOT_WRITE": [
        "ننوشتم"
    ],

    "DONT_KNOW": [
        "بلد نیستم"
    ],

    "HOW_TO_WRITE": [
        "چجوری بنویسم",
        "چجوری بنویسم؟",
        "چگونه بنویسم",
        "چگونه بنویسم؟"
    ],

    "WAIT": [
        "صبر کن",
        "صبرکن"
    ],

    "SLOWER": [
        "آرام‌تر بگو",
        "آرام تر بگو",
        "آرامتر بگو"
    ],

    "NEXT": [
        "بعدی"
    ],

    "FINISH": [
        "تمام شد"
    ]
}


def normalize_text(text):
    """
    متن را برای تشخیص راحت‌تر یکدست می‌کند.
    """

    text = text.strip()

    text = text.replace("‌", " ")
    text = text.replace("ي", "ی")
    text = text.replace("ك", "ک")
    text = text.replace("؟", "")
    text = text.replace(".", "")

    return text


def detect_command(text):
    """
    بررسی می‌کند آیا متن یکی از فرمان‌های مجاز است یا نه.
    """

    text = normalize_text(text)

    for command, phrases in COMMANDS.items():

        for phrase in phrases:

            if text == normalize_text(phrase):
                return command

    return "UNKNOWN"