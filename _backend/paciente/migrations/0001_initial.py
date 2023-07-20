# Generated by Django 4.2.3 on 2023-07-20 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Paciente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=70)),
                ('cpf', models.CharField(max_length=14)),
                ('aftas', models.BooleanField(default=False)),
                ('hipersensibilidade', models.BooleanField(default=False)),
                ('lesoes', models.BooleanField(default=False)),
                ('pos_cirurgia', models.BooleanField(default=False)),
                ('nevralgia', models.BooleanField(default=False)),
                ('consulta', models.BooleanField(default=False)),
            ],
        ),
    ]
