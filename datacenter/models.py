from django.db import models
from django.utils.timezone import localtime

SECONDS_PER_HOUR = 3600
SECONDS_PER_MINUTE = 60


class Passcard(models.Model):
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    passcode = models.CharField(max_length=200, unique=True)
    owner_name = models.CharField(max_length=255)

    def __str__(self):
        if self.is_active:
            return self.owner_name
        return f'{self.owner_name} (inactive)'


class Visit(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    passcard = models.ForeignKey(Passcard, on_delete=models.CASCADE)
    entered_at = models.DateTimeField()
    leaved_at = models.DateTimeField(null=True)

    def __str__(self):
        return '{user} entered at {entered} {leaved}'.format(
            user=self.passcard.owner_name,
            entered=self.entered_at,
            leaved=(
                f'leaved at {self.leaved_at}'
                if self.leaved_at else 'not leaved'
            )
        )


def get_duration(visit_at, leaved_at=localtime()):
    delta = (localtime(leaved_at) - localtime(visit_at)).total_seconds()
    return delta


def is_visit_long(visit_at, leaved_at=localtime(), minutes_limit=60):
    duration_minutes = get_duration(visit_at, leaved_at) // SECONDS_PER_MINUTE
    return duration_minutes <= minutes_limit


def format_duration(duration):
    minutes = (duration % SECONDS_PER_HOUR) // SECONDS_PER_MINUTE
    hours = duration // SECONDS_PER_HOUR
    return f'{int(hours)}ч {int(minutes)}мин'
