# Generated by Django 3.1.4 on 2022-03-13 10:04

from django.db import migrations, models
import django.utils.timezone
import papps.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='InputAdd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('temp_id', models.CharField(max_length=10, unique=True, verbose_name='テンプレート用id')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='項目名')),
            ],
        ),
        migrations.CreateModel(
            name='InputAddData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_id', models.IntegerField()),
                ('inputadd_id', models.IntegerField()),
                ('data', models.CharField(blank=True, max_length=300, null=True, verbose_name='項目データ')),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField(unique=True)),
                ('naiyou', models.CharField(max_length=100, verbose_name='内容')),
                ('base', models.CharField(max_length=100, verbose_name='ベース')),
                ('flavor', models.CharField(max_length=100, verbose_name='フレーバー')),
                ('seibun', models.CharField(blank=True, max_length=400, null=True, verbose_name='成分')),
                ('other', models.CharField(blank=True, max_length=400, null=True, verbose_name='その他')),
                ('syoukei', models.CharField(max_length=100, verbose_name='小計')),
                ('zei', models.CharField(max_length=100, verbose_name='税')),
                ('zeikomi', models.CharField(max_length=100, verbose_name='税込')),
                ('send_price', models.CharField(max_length=100, verbose_name='送料')),
                ('sougaku', models.CharField(max_length=100, verbose_name='総額')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('sei_name', models.CharField(max_length=30, verbose_name='姓')),
                ('mei_name', models.CharField(max_length=150, verbose_name='名')),
                ('yubin_bangou', models.CharField(max_length=8, verbose_name='郵便番号')),
                ('jusyo', models.CharField(max_length=100, verbose_name='住所')),
                ('tel_bangou', models.CharField(max_length=11, verbose_name='電話番号')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='メールアドレス')),
                ('is_active', models.BooleanField(default=True, help_text='', verbose_name='有効フラグ')),
                ('is_superuser', models.BooleanField(default=False, help_text='', verbose_name='権限フラグ')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='作成日時')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', papps.models.CustomUserManager()),
            ],
        ),
    ]
