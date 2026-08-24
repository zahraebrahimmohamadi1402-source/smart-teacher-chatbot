import asyncio
import edge_tts
import pygame


# =====================================================
# صدای فارسی خانم
# =====================================================

VOICE = "fa-IR-DilaraNeural"

# برای کلاس اول کمی آهسته‌تر
NORMAL_RATE = "-12%"
SLOW_RATE = "-25%"


# =====================================================
# ساخت فایل صوتی
# =====================================================

async def create_voice(text, rate):

    communicate = edge_tts.Communicate(
        text,
        VOICE,
        rate=rate
    )

    await communicate.save("voice.mp3")


# =====================================================
# پخش صدا
# =====================================================

def speak(text, rate=NORMAL_RATE):

    asyncio.run(
        create_voice(text, rate)
    )

    pygame.mixer.init()

    pygame.mixer.music.load("voice.mp3")
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.stop()
    pygame.mixer.quit()


# =====================================================
# تست صدا
# =====================================================

if __name__ == "__main__":

    speak(
        "آفرین! خیلی خوب نوشتی."
    )

    speak(
        "حالا جمله‌ی بعدی را آرام و واضح می‌گویم."
    )

    speak(
        "بابا، کاپیتانِ یک سفینه است."
    )