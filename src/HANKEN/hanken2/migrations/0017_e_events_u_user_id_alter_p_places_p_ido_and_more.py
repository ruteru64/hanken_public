# Generated by Django 4.0.3 on 2022-03-11 13:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hanken2', '0016_alter_s_seats_t_ticket_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='e_events',
            name='u_user_id',
            field=models.ForeignKey(db_column='u_user_id', default=3, on_delete=django.db.models.deletion.CASCADE, to='hanken2.u_users'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='p_places',
            name='p_ido',
            field=models.CharField(blank=True, default='99', max_length=17),
        ),
        migrations.AlterField(
            model_name='p_places',
            name='p_kedo',
            field=models.CharField(blank=True, default='360', max_length=18),
        ),
    ]