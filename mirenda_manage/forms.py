from django import forms
from .models import Project, Task
from .models import CustomUser as User


class ProjectForm(forms.ModelForm):
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),  # initially, no users are included
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Project
        fields = ['name', 'description', 'users']

    def __init__(self, *args, **kwargs):
        request = kwargs.pop('request', None)
        super(ProjectForm, self).__init__(*args, **kwargs)
        if request:
            self.fields['users'].queryset = User.objects.exclude(user_id=request.user.user_id)


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)  # add any other fields that you have in your custom user model

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['name', 'description', 'project', 'deadline']
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        self.project = kwargs.pop('project', None)
        super(TaskForm, self).__init__(*args, **kwargs)
        self.fields['project'].widget = forms.HiddenInput()
        if self.project:
            self.fields['project'].initial = self.project
            self.fields['project'].disabled = True
