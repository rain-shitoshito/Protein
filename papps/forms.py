import re
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, UserCreationForm, PasswordChangeForm,
    PasswordResetForm, SetPasswordForm
)
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

''' Login '''
class LoginForm(AuthenticationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'

''' パスワード変更フォーム '''
class MyPasswordChangeForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'

''' Order2 '''
class UserCreateForm(forms.ModelForm):

    email_conf = forms.EmailField(label='確認用メールアドレス', required=True)
    password_conf = forms.CharField(label='確認用パスワード', min_length=8, required=True)

    class Meta:
        model = User
        fields = ('sei_name', 'mei_name', 'yubin_bangou', 'jusyo', 'tel_bangou', 'email', 'email_conf', 'password', 'password_conf',)

    field_order = ['sei_name', 'mei_name', 'yubin_bangou', 'jusyo', 'tel_bangou', 'email', 'email_conf', 'password', 'password_conf']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        placeholder = ['姓', '名', '123-4567', '住所', '07012345678', 'aaa@gmail.com', 'aaa@gmail.com', 'Abcd1234', 'Abcd1234']

        cnt = 0
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'
            field.widget.attrs['placeholder'] = placeholder[cnt]
            cnt += 1


    def clean_yubin_bangou(self):
        yubin_bangou = self.cleaned_data['yubin_bangou']
        pattern = r'^[0-9]{3}\-[0-9]{4}$'
        if re.match(pattern, yubin_bangou):
            return yubin_bangou
        else:
            raise forms.ValidationError('郵便番号ではありません')

    def clean_tel_bangou(self):
        tel_bangou = self.cleaned_data['tel_bangou']
        pattern = '^[0-9]{10}$'
        pattern2 = '^[0-9]{11}$'
        if re.match(pattern, tel_bangou) or re.match(pattern2, tel_bangou):
            return tel_bangou
        else:
            raise forms.ValidationError('電話番号ではありません')

    def _clean_email(self, email):
        email_pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if re.match(email_pattern, email):
            return email
        else:
            return forms.ValidationError('メールアドレスを入力してください')


    def _clean_password(self, password):
        password_pattern = r'\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,20}\Z'
        if re.match(password_pattern, password):
            return password
        else:
            return forms.ValidationError('半角小文字大文字数字を使用した8～20文字で入力してください')

    def clean_email(self):
        email = self.cleaned_data['email']
        val = self._clean_email(email)
        if type(val) is forms.ValidationError:
            raise val
        else: 
            return email

    def clean_email_conf(self):
        email_conf = self.cleaned_data['email_conf']
        val = self._clean_email(email_conf)
        if type(val) is forms.ValidationError:
            raise val
        else: 
            return email_conf

    def clean_password(self):
        password = self.cleaned_data['password']
        val = self._clean_password(password)
        if type(val) is forms.ValidationError:
            raise val
        else: 
            return password

    def clean_password_conf(self):
        password_conf = self.cleaned_data['password_conf']
        val = self._clean_password(password_conf)
        if type(val) is forms.ValidationError:
            raise val
        else: 
            return password_conf

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        email_conf = cleaned_data.get('email_conf')
        password = cleaned_data.get('password')
        password_conf = cleaned_data.get('password_conf')

        if email != email_conf or password != password_conf:
            raise forms.ValidationError('メールアドレスまたはパスワードが不一致です')
        return cleaned_data


''' オーダー '''
class InputAddForm(forms.ModelForm):

    class Meta:
        model = InputAdd
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'

''' ユーザデータ編集 '''
class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ( 'yubin_bangou', 'jusyo', 'tel_bangou', 'email',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'
        
''' オーダデータ編集 '''
class OrderEditForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'
        self.fields['user_id'].widget = forms.HiddenInput()


''' InputAddData登録・編集 '''
class InputAddDataForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        iaq = InputAdd.objects.all()
        for q in iaq:
            self.fields[q.temp_id] = forms.CharField(label=q.name, required=False)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'

''' id検索 '''
class SearchIdForm(forms.Form):
    email = forms.EmailField(label='メールアドレスからID検索', required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'input_1'
