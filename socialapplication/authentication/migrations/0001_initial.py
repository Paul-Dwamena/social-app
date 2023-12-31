# Generated by Django 4.2 on 2023-08-27 20:29

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
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(blank=True, error_messages={'unique': 'A user with that email already exists.'}, max_length=254, unique=True, verbose_name='email address')),
                ('username', models.CharField(blank=True, max_length=20)),
                ('phone', models.CharField(blank=True, max_length=15)),
                ('firstname', models.CharField(blank=True, max_length=100, null=True)),
                ('lastname', models.CharField(blank=True, max_length=100, null=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('password', models.TextField(blank=True, null=True)),
                ('is_firsttime', models.BooleanField(default=True)),
                ('emailverified', models.BooleanField(default=False)),
                ('profile_url', models.TextField(blank=True, null=True)),
                ('following_count', models.IntegerField(blank=True, default=0, null=True)),
                ('follower_count', models.IntegerField(blank=True, default=0, null=True)),
                ('datecreated', models.DateTimeField(auto_now_add=True)),
                ('account_type', models.CharField(choices=[('public', 'public'), ('private', 'private')], default='public', max_length=10)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'auth_user',
                'abstract': False,
                'managed': True,
            },
        ),
    ]
