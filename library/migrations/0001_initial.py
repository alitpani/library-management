# Generated by Django 3.2.7 on 2024-03-23 10:17

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Books',
            fields=[
                ('book_id', models.AutoField(primary_key=True, serialize=False)),
                ('book_name', models.CharField(max_length=255)),
                ('number_od_copies', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Members',
            fields=[
                ('member_id', models.AutoField(primary_key=True, serialize=False)),
                ('member_name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('reservation_id', models.AutoField(primary_key=True, serialize=False)),
                ('reservation_date', models.DateTimeField(default=datetime.datetime(2024, 3, 23, 10, 17, 3, 960321))),
                ('fulfillment_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='library.books')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reservations', to='library.members')),
            ],
        ),
        migrations.CreateModel(
            name='Circulation',
            fields=[
                ('circulation_id', models.AutoField(primary_key=True, serialize=False)),
                ('checkout_date', models.DateTimeField(blank=True, null=True)),
                ('return_time', models.IntegerField(default=30)),
                ('return_date', models.DateTimeField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='circulations', to='library.books')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='circulations', to='library.members')),
            ],
        ),
    ]
