from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .constants import GENDER_TYPE, ACCOUNT_TYPE
from .models import UserAddress, UserAccount

# create a user registration form
class UserRegistrationForm(UserCreationForm):
    # our model combination data 
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': "date"}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    country = forms.CharField(max_length=100)
    # add extra characteristics 
    class Meta:
        model = User # this is for the built in user model form django 
        fields = ['username', 'password1', 'password2','first_name', 'last_name', 'email', 'birth_date', 'gender', 'account_type', 'street_address', 'city', 'country']
    
    def save(self, commit=True):
        our_user = super().save(commit=False) # initially we will not save anything
        if commit ==True:
            our_user.save() # user model a data save korlam
            account_type = self.cleaned_data.get('account_type')
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            country = self.cleaned_data.get('country')


            UserAddress.objects.create(
                user = our_user,
                street_address = street_address,
                city = city,
                country = country
            )

            UserAccount.objects.create(
                user = our_user,
                account_type = account_type,
                birth_date = birth_date,
                gender = gender,
                account_no = 1000 + our_user.id
            )

        return our_user

    # form design
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                
                'class' : (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-800 border border-sky-300 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                ) 
            })

            
# user information update form
class UserUpdateForm(forms.ModelForm):
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms.ChoiceField(choices=GENDER_TYPE)
    account_type = forms.ChoiceField(choices=ACCOUNT_TYPE)
    street_address = forms.CharField(max_length=100)
    city = forms.CharField(max_length= 100)
    country = forms.CharField(max_length=100)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        # if the user has account 
        if self.instance:
            try:
                user_account = self.instance.account
                user_address = self.instance.address
            except UserAccount.DoesNotExist:
                user_account = None
                user_address = None

            if user_account:
                self.fields['account_type'].initial = user_account.account_type
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['country'].initial = user_address.country

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

            # Get or create UserAccount and UserAddress
            user_account, created_account = UserAccount.objects.get_or_create(user=user)
            user_address, created_address = UserAddress.objects.get_or_create(user=user)

            # Assign or auto-generate account_no if it doesn't already exist
            if created_account or not user_account.account_no:
                user_account.account_no = 1000 + user.id

            # Update other fields
            user_account.account_type = self.cleaned_data['account_type']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            # Update UserAddress fields
            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.country = self.cleaned_data['country']
            user_address.save()

        return user
