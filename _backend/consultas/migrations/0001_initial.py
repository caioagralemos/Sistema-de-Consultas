# Generated by Django 4.2.3 on 2023-08-02 22:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('medico', '__first__'),
        ('paciente', '__first__'),
        ('datas', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consulta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('servico', models.CharField(choices=[('consulta', 'Consulta'), ('aftas', 'Aftas'), ('hipersensibilidade', 'Hipersensibilidade'), ('pos_cirurgia', 'Pós-cirurgia'), ('lesoes', 'Lesões'), ('nevralgia', 'Nevralgia')], default='consulta')),
                ('ehParte2', models.BooleanField(default=False)),
                ('data', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='datas.data')),
                ('medico', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultas', to='medico.medico')),
                ('paciente', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='consultas', to='paciente.paciente')),
            ],
            options={
                'ordering': ['data__ano', 'data__mes', 'data__dia', 'data__hora', 'data__minuto'],
            },
        ),
    ]
