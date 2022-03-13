from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin, UserManager
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils.crypto import get_random_string


def raw_queryset_normal(raw_qs): 
        columns = raw_qs.columns
        data = []
        for row in raw_qs:
            r = {}
            for col in columns:
                r[col] = getattr(row, col)
            data.append(r)
        return data

'''ユーザーマネージャー'''
class CustomUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, sei_name, mei_name, yubin_bangou, jusyo, tel_bangou, email, password, **extra_fields):
        user = self.model(sei_name=sei_name, mei_name=mei_name, yubin_bangou=yubin_bangou, jusyo=jusyo,
            tel_bangou=tel_bangou, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, sei_name, mei_name, yubin_bangou, jusyo, tel_bangou, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(sei_name, mei_name, yubin_bangou, jusyo, tel_bangou, email, password, **extra_fields)

    def create_superuser(self, sei_name, mei_name, yubin_bangou, jusyo, tel_bangou, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(sei_name, mei_name, yubin_bangou, jusyo, tel_bangou, email, password, **extra_fields)


"""カスタムユーザーモデル."""
class User(AbstractBaseUser, PermissionsMixin):
    sei_name = models.CharField(_('姓'), max_length=30)
    mei_name = models.CharField(_('名'), max_length=150)
    yubin_bangou = models.CharField(_('郵便番号'), max_length=8)
    jusyo = models.CharField(_('住所'), max_length=100)
    tel_bangou = models.CharField(_('電話番号'), max_length=11)
    email = models.EmailField(_('メールアドレス'), unique=True)

    is_active = models.BooleanField(
        _('有効フラグ'),
        default=True,
        help_text=_(
            ''),
    )
    is_superuser = models.BooleanField(
        _('権限フラグ'),
        default=False,
        help_text=_(
            ''),
    )
    date_joined = models.DateTimeField(_('作成日時'), default=timezone.now)

    objects = CustomUserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_name(self):
        return self.sei_name + self.mei_name

    def send_email(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


''' オーダーモデル '''
class Order(models.Model):
    user_id = models.IntegerField(unique=True)
    naiyou = models.CharField(_('内容'), max_length=100)
    base = models.CharField(_('ベース'), max_length=100)
    flavor = models.CharField(_('フレーバー'), max_length=100)
    seibun = models.CharField(_('成分'), max_length=400, blank=True, null=True)
    other = models.CharField(_('その他'), max_length=400, blank=True, null=True)
    syoukei = models.CharField(_('小計'), max_length=100)
    zei = models.CharField(_('税'), max_length=100)
    zeikomi = models.CharField(_('税込'), max_length=100)
    send_price = models.CharField(_('送料'), max_length=100)
    sougaku = models.CharField(_('総額'), max_length=100)

    @staticmethod
    def select_inputadddata(uid):
        return Order.objects.raw('''
            SELECT 
            inputadddata.id AS id,
            inputadd.name AS name,
            inputadd.temp_id AS temp_id,
            inputadddata.data AS data
            FROM (
            SELECT id
            FROM papps_order
            WHERE user_id = %s
            ) AS porder
            INNER JOIN papps_inputadddata AS inputadddata ON porder.id = inputadddata.order_id
            INNER JOIN papps_inputadd AS inputadd ON inputadddata.inputadd_id = inputadd.id
        ''', [uid])
    

''' インプットモデル '''
class InputAdd(models.Model):
    temp_id = models.CharField(_('テンプレート用id'), max_length=10, unique=True)
    name = models.CharField(_('項目名'), max_length=100, unique=True)

    @staticmethod
    def insert_tempid():
        return get_random_string()

''' インプットデータモデル '''
class InputAddData(models.Model):
    order_id = models.IntegerField()
    inputadd_id = models.IntegerField()
    data = models.CharField(_('項目データ'), max_length=300, blank=True, null=True)

