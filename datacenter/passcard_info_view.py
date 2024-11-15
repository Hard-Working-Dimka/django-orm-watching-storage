from datacenter.models import Passcard
from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import is_visit_long
from datacenter.models import format_duration
from django.shortcuts import get_object_or_404


def passcard_info_view(request, passcode):
    person_passcard = get_object_or_404(Passcard, passcode=passcode)
    person_visits = Visit.objects.filter(passcard=person_passcard)

    this_passcard_visits = []
    for visit in person_visits:
        if visit.leaved_at:
            duration = get_duration(visit.entered_at, leaved_at=visit.leaved_at)
            is_strange = is_visit_long(visit.entered_at, leaved_at=visit.leaved_at, minutes_limit=60)
        else:
            is_strange = str(is_visit_long(visit.entered_at, minutes_limit=60)) + ' (еще в хранилище)'
            duration = get_duration(visit.entered_at)

        this_passcard_visits.append(
            {
                'entered_at': visit.entered_at,
                'duration': format_duration(duration),
                'is_strange': is_strange
            },
        )
    context = {
        'passcard': person_passcard,
        'this_passcard_visits': this_passcard_visits
    }
    return render(request, 'passcard_info.html', context)
