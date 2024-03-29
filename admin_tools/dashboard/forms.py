from django import forms

from admin_tools.dashboard.models import DashboardPreferences


class DashboardPreferencesForm(forms.ModelForm):
    """
    This form allows the user to edit dashboard preferences. It doesn't show
    the user field. It expects the user to be passed in from the view.
    """

    def __init__(self, user, dashboard_id, *args, **kwargs):
        super(DashboardPreferencesForm, self).__init__(*args, **kwargs)
        self.user = user
        self.dashboard_id = dashboard_id

    def save(self, *args, **kwargs):
        preferences = super(DashboardPreferencesForm, self).save(
            commit=False,
            *args,
            **kwargs
        )
        preferences.user = self.user
        preferences.dashboard_id = self.dashboard_id
        preferences.save()
        return preferences

    class Meta:
        fields = ('dashboard_id', 'data',)
        model = DashboardPreferences
