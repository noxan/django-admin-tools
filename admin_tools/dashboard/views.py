from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.generic.simple import direct_to_template

try:
    from django.views.decorators.csrf import csrf_exempt
except ImportError:
    from django.contrib.csrf.middleware import csrf_exempt

from forms import DashboardPreferencesForm
from models import DashboardPreferences


@login_required
@csrf_exempt
def set_preferences(request):
    """
    This view serves and validates a preferences form.
    """
    if request.method == "POST":
        host = "http://%s" % request.META['HTTP_HOST']
        pathname = request.META['HTTP_REFERER'][len(host):]
    try:
        preferences = DashboardPreferences.objects.get(user=request.user, pathname=pathname)
    except DashboardPreferences.DoesNotExist:
        preferences = None
    if request.method == "POST":
        #host = "http://%s" % request.META['HTTP_HOST']
        #pathname = request.META['HTTP_REFERER'][len(host):]
        form = DashboardPreferencesForm(
            user=request.user,
            pathname=pathname,
            data=request.POST,
            instance=preferences
        )
        if form.is_valid():
            preferences = form.save()
            if request.is_ajax():
                return HttpResponse('true')
            request.user.message_set.create(message='Preferences saved')
        elif request.is_ajax():
            return HttpResponse('false')
    else:
        form = DashboardPreferencesForm(user=request.user, instance=preferences)
    return direct_to_template(request, 'admin_tools/dashboard/preferences_form.html', {
        'form': form,   
    })
