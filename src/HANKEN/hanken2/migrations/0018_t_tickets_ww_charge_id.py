# Generated by Django 4.0.3 on 2022-03-14 15:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hanken2', '0017_e_events_u_user_id_alter_p_places_p_ido_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='t_tickets',
            name='ww_charge_id',
            field=models.OneToOneField(db_column='ww_charge_id', default=1, on_delete=django.db.models.deletion.CASCADE, to='hanken2.ww_charges_ww'),
            preserve_default=False,
        ),
    ]