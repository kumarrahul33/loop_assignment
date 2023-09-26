# Generated by Django 4.1.3 on 2023-09-26 06:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Restaurants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('storeID', models.IntegerField()),
                ('businessHours', models.CharField(max_length=100)),
                ('originalTimeFormat', models.CharField(max_length=100)),
                ('timezone', models.CharField(default='America/Chicago', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(default='unknown', max_length=100)),
                ('extrapolated', models.BooleanField(default=False)),
                ('storeID', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.restaurants')),
                ('timeSlice', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='data.timeslice')),
            ],
        ),
    ]