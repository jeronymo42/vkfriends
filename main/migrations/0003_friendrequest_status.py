# Generated by Django 4.2.1 on 2023-05-10 09:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_user_password_alter_user_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='status',
            field=models.IntegerField(choices=[(0, 'Norelatons'), (1, 'Send Request'), (2, 'Get Request'), (3, 'Friends')], default=0),
            preserve_default=False,
        ),
    ]
