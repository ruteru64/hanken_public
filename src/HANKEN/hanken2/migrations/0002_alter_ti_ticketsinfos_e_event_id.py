# Generated by Django 4.0.3 on 2022-03-09 04:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hanken2', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ti_ticketsinfos',
            name='e_event_id',
            field=models.OneToOneField(blank=True, db_column='e_event_id', default=-1, on_delete=django.db.models.deletion.CASCADE, to='hanken2.e_events'),
        ),
    ]