# Generated by Django 4.0.3 on 2022-03-11 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hanken2', '0013_alter_s_seats_t_ticket_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='s_seats',
            name='t_ticket_id',
            field=models.OneToOneField(db_column='t_ticket_id', null=True, on_delete=django.db.models.deletion.CASCADE, to='hanken2.t_tickets'),
        ),
    ]
