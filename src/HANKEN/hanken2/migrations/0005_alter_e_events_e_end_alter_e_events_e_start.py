# Generated by Django 4.0.3 on 2022-03-10 01:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hanken2', '0004_alter_p_places_p_ido_alter_u_users_u_mail_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='e_events',
            name='e_end',
            field=models.DateField(blank=True, default='0000-00-00'),
        ),
        migrations.AlterField(
            model_name='e_events',
            name='e_start',
            field=models.DateField(blank=True, default='0000-00-00'),
        ),
    ]
