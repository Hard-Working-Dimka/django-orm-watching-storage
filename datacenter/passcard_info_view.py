from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import is_visit_long
from datacenter.models import format_duration
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    passcard_certain_person = get_object_or_404(Passcard, passcode=passcode)
    visits_certain_person = Visit.objects.filter(passcard=passcard_certain_person)

    this_passcard_visits = []
    for visit in visits_certain_person:
        if visit.leaved_at is None:
            is_strange = str(is_visit_long(visit.entered_at, minutes_limit=60)) + ' (еще в хранилище)'
            duration = get_duration(visit.entered_at)
        else:
            duration = get_duration(visit.entered_at, leaved_at=visit.leaved_at)
            is_strange = is_visit_long(visit.entered_at, leaved_at=visit.leaved_at, minutes_limit=60)

        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': format_duration(duration),
                'is_strange': is_strange
            },
        )
    context = {
        'passcard': passcard_certain_person,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
