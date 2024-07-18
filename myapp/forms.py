from django import forms
from django.contrib.contenttypes.models import ContentType
from .models import UserPermission, User


class UserPermissionsForm(forms.ModelForm):
    class Meta:
        model = UserPermission
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        allowed_models = ['user', 'backend', 'frontend', 'database']
        self.fields['object_content_type'].queryset = ContentType.objects.filter(
            model__in=allowed_models).exclude(app_label='auth')
        self.fields['subject_content_type'].queryset = ContentType.objects.filter(
            model__in=allowed_models).exclude(app_label='auth')

        if self.instance and self.instance.pk:
            if self.instance.object_content_type:
                model_class = self.instance.object_content_type.model_class()
                self.fields['object_id'].queryset = model_class.objects.all()
            if self.instance.subject_content_type:
                model_class = self.instance.subject_content_type.model_class()
                self.fields['subject_id'].queryset = model_class.objects.all()
        else:
            self.fields['object_id'].queryset = User.objects.none()
            self.fields['subject_id'].queryset = User.objects.none()

        self.fields['object_content_type'].widget.attrs.update({'onchange': 'updateObjectId(this);'})
        self.fields['subject_content_type'].widget.attrs.update({'onchange': 'updateSubjectId(this);'})