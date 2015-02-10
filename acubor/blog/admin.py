from django.contrib import admin
from django import forms
from redactor.widgets import RedactorEditor

from blog.models import Blog


class BlogForm(forms.ModelForm):
    #content = RedactorField()

    class Meta:
        model = Blog
        exclude = ['author']
        widgets = {
            'content': RedactorEditor(),
        }

        #def save(self, commit=True):
        #    # Save the provided password in hashed format
        #    user = super(UserCreationForm, self).save(commit=False)
        #    user.set_password(self.cleaned_data["password1"])
        #    if commit:
        #        user.save()
        #    return user


class BlogAdmin(admin.ModelAdmin):
    form = BlogForm

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        super(BlogAdmin, self).save_model(request, obj, form, change)


admin.site.register(Blog, BlogAdmin)
