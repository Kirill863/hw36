# Generated by Django 5.2.1 on 2025-07-30 14:57

import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('username_ru', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('username_en', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, null=True, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('first_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('first_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('last_name_ru', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('last_name_en', models.CharField(blank=True, max_length=150, null=True, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.ImageField(blank=True, help_text='Загрузите ваш аватар', null=True, upload_to='users/avatars/%Y/%m/%d/', verbose_name='Аватар')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Дата рождения')),
                ('phone_number', models.CharField(blank=True, max_length=17, null=True, validators=[django.core.validators.RegexValidator(message="Номер телефона должен быть в формате: '+799999999'. До 15 цифр.", regex='^\\+?1?\\d{9,15}$')], verbose_name='Телефон')),
                ('telegram_id', models.CharField(blank=True, help_text='Ваш ID в Telegram', max_length=100, null=True, verbose_name='Telegram ID')),
                ('github_id', models.CharField(blank=True, help_text='Ваш профиль на GitHub', max_length=100, null=True, verbose_name='GitHub ID')),
                ('email_verified', models.BooleanField(default=False, verbose_name='Email подтвержден')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['-date_joined'],
                'indexes': [models.Index(fields=['username'], name='users_user_usernam_65d164_idx'), models.Index(fields=['email'], name='users_user_email_6f2530_idx')],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
