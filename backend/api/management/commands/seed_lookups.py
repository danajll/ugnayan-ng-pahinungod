from django.core.management.base import BaseCommand
from api.models import Program, Subject


PROGRAMS = [
    ("AFFIRMATIVE_ACTION_PROGRAM", "Affirmative Action Program"),
    ("DISASTER_RISK_REDUCTION", "Disaster Risk Reduction Related Program"),
    ("TUTORIAL_SERVICE_PROGRAM", "Tutorial Service Program"),
    ("UP_BARMM_MBHTE_MOU", "Programs under the UP BARMM-MBHTE MOU"),
    ("TEACHER_DEVELOPMENT_PROGRAM", "Teacher Development Program"),
    ("UGNAYAN_NG_PAHINUNGOD_ONLINE", "Ugnayan ng Pahinungod Online Program"),
    ("ENVIRONMENTAL_AWARENESS_PROGRAM", "Environmental Awareness Program"),
]

SUBJECTS = [
    ("READING_COMP_FILIPINO", "Reading Comprehension Filipino"),
    ("LANG_PROF_FILIPINO", "Language Proficiency Filipino"),
    ("MATH", "Mathematics"),
    ("READING_COMP_ENGLISH", "Reading Comprehension English"),
    ("LANG_PROF_ENGLISH", "Language Proficiency English"),
]


class Command(BaseCommand):
    help = "Seed Program and Subject lookup tables"

    def handle(self, *args, **options):
        for code, name in PROGRAMS:
            Program.objects.update_or_create(code=code, defaults={"name": name})
        for code, name in SUBJECTS:
            Subject.objects.update_or_create(code=code, defaults={"name": name})
        self.stdout.write(self.style.SUCCESS("Lookup tables seeded."))