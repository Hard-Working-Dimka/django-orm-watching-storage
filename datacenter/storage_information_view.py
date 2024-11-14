from datacenter.models import Visit
from django.shortcuts import render
from datacenter.models import get_duration
from datacenter.models import format_duration


def storage_information_view(request):
    all_non_ended_visits = Visit.objects.filter(leaved_at=None)
    non_closed_visits = []
    for non_ended_visit in all_non_ended_visits:
        duration = get_duration(non_ended_visit.entered_at)
        non_closed_visits.append(
            {
                'who_entered': non_ended_visit.passcard.owner_name,
                'entered_at': non_ended_visit.entered_at,
                'duration': format_duration(duration),
            }
        )
    context = {
        'non_closed_visits': non_closed_visits,
    }
    return render(request, 'storage_information.html', context)
