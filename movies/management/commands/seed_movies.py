import random
from decimal import Decimal
from django.core.management.base import BaseCommand
from movies.models import Movie


# ─── داده‌های فیک ───────────────────────────────────────────────────────────

TITLES = [
    "The Lost Horizon", "Echoes of Tomorrow", "Shadows of the Past",
    "Beyond the Stars", "The Silent Storm", "City of Ghosts",
    "The Last Frontier", "Broken Wings", "Midnight Mirage",
    "The Iron Curtain", "Whispers in the Dark", "The Forgotten Kingdom",
    "Rise of the Phoenix", "Code of Silence", "The Golden Hour",
    "Storm Chasers", "The Hidden Path", "Neon Dreams",
    "The Crimson Tide", "Edge of Eternity", "Paper Walls",
    "The Glass Kingdom", "Into the Abyss", "Burning Sands",
    "The Last Waltz", "Cold Pursuit", "The Wanderer",
    "Shattered Mirrors", "The Blue Lagoon", "Starfall",
]

GENRES = [
    "Drama", "Action", "Thriller", "Sci-Fi", "Comedy",
    "Horror", "Romance", "Adventure", "Mystery", "Fantasy",
    "Animation", "Documentary", "Crime", "Western", "Biography",
]

DIRECTORS = [
    "James Carter", "Sofia Rossi", "Liam O'Brien", "Yuki Tanaka",
    "Elena Moreau", "Marcus Williams", "Nadia Petrov", "Carlos Mendez",
    "Aisha Okafor", "Henrik Larsson", "Priya Nair", "Tobias Müller",
    "Mei-Ling Zhou", "André Dupont", "Sara Al-Hassan",
]

ACTORS = [
    "Tom Blake", "Jessica Lane", "Ryan Kowalski", "Emma Hartley",
    "David Chen", "Olivia Park", "Samuel Torres", "Grace Kim",
    "Nathan Ford", "Isabella Russo", "Leo Nakamura", "Amara Diallo",
    "Ethan Hayes", "Zoe Reeves", "Marco Ferretti", "Ava Collins",
    "Lucas Brandt", "Sofia Delgado", "Jack Morrison", "Lily Zhang",
]

PRODUCERS = [
    "Apex Studios", "BlueSky Productions", "Redline Films",
    "Orbit Entertainment", "Golden Gate Pictures", "Phantom Works",
    "Titan Media Group", "Silver Lining Films", "Nova Pictures",
    "Ironwood Productions",
]

COUNTRIES = [
    "USA", "UK", "France", "Germany", "Japan",
    "Italy", "Canada", "Australia", "Spain", "South Korea",
    "Brazil", "India", "Mexico", "Sweden", "Netherlands",
]

DESCRIPTION_TEMPLATES = [
    "در دنیایی که {theme}، یک {role} مجبور می‌شود با {conflict} روبرو شود و تنها راه نجات را بیابد.",
    "داستان {role} که پس از {event}، زندگی‌اش کاملاً دگرگون می‌شود و باید بین {choice} یکی را انتخاب کند.",
    "یک {role} تنها، در میان {setting}، درگیر مبارزه‌ای بی‌امان با {conflict} می‌شود.",
    "وقتی {event} اتفاق می‌افتد، {role} باید تمام آنچه می‌داند را زیر سؤال ببرد تا حقیقت را کشف کند.",
    "سفری پرماجرا در دل {setting} که {role} را به مرز {conflict} می‌کشاند.",
]

THEMES = ["آشوب و نظم در هم می‌آمیزند", "آینده نامشخص است", "گذشته هرگز نمی‌میرد"]
ROLES = ["کارآگاه", "دانشمند", "سرباز", "هنرمند", "پزشک", "معلم", "مهاجر"]
CONFLICTS = ["دشمنان پنهان", "اسرار خانوادگی", "نیروهای تاریکی", "فساد سیستماتیک"]
EVENTS = ["یک حادثه مرگبار", "ناپدید شدن عزیزی", "کشف یک راز بزرگ", "بازگشت به گذشته"]
SETTINGS = ["شهری ناشناس", "بیابانی بی‌انتها", "آینده‌ای دیستوپیک", "جنگل‌های مرموز"]
CHOICES = ["عشق و وظیفه", "حقیقت و بقا", "خانواده و قدرت"]


def fake_description():
    template = random.choice(DESCRIPTION_TEMPLATES)
    return template.format(
        theme=random.choice(THEMES),
        role=random.choice(ROLES),
        conflict=random.choice(CONFLICTS),
        event=random.choice(EVENTS),
        setting=random.choice(SETTINGS),
        choice=random.choice(CHOICES),
    )


def fake_actors(n=3):
    return "، ".join(random.sample(ACTORS, min(n, len(ACTORS))))


# ─── Management Command ──────────────────────────────────────────────────────

class Command(BaseCommand):
    help = "دیتابیس فیلم‌ها را با داده‌های فیک پر می‌کند"

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=20,
            help="تعداد فیلم‌هایی که باید ایجاد شوند (پیش‌فرض: 20)",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="قبل از اضافه کردن، تمام فیلم‌های موجود را حذف کن",
        )

    def handle(self, *args, **options):
        count = options["count"]

        if options["clear"]:
            deleted, _ = Movie.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"✓ {deleted} فیلم قبلی حذف شد."))

        # از عناوین تکراری جلوگیری می‌کنیم
        available_titles = list(TITLES)
        if count > len(available_titles):
            # اگر بیشتر از تعداد عناوین موجود خواست، شماره اضافه می‌کنیم
            for i in range(count - len(available_titles)):
                available_titles.append(f"Untitled {i + 1}")

        selected_titles = random.sample(available_titles, min(count, len(available_titles)))

        movies = []
        for title in selected_titles:
            movies.append(Movie(
                title=title,
                genre=random.choice(GENRES),
                actors=fake_actors(random.randint(2, 4)),
                rating=Decimal(str(round(random.uniform(4.0, 9.5), 1))),
                director=random.choice(DIRECTORS),
                country=random.choice(COUNTRIES),
                producer=random.choice(PRODUCERS),
                year=random.randint(1990, 2025),
                description=fake_description(),
            ))

        Movie.objects.bulk_create(movies)

        self.stdout.write(
            self.style.SUCCESS(f"✓ {len(movies)} فیلم با موفقیت به دیتابیس اضافه شد.")
        )