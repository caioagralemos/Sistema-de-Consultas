# Generated by Django 4.2.3 on 2023-08-03 03:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Data',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dia', models.IntegerField()),
                ('mes', models.IntegerField()),
                ('ano', models.IntegerField()),
                ('hora', models.IntegerField()),
                ('minuto', models.IntegerField()),
                ('data_hora_completa', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
