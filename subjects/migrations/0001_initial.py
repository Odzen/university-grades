# Generated by Django 5.1.2 on 2024-10-23 00:53

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('number_credits', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('semester', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1)])),
                ('level', models.CharField(choices=[('BACHELOR', 'Bachelor'), ('MASTER', 'Master')], default='BACHELOR', max_length=100, verbose_name='Subject level')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'ordering': ['-created_at', 'name'],
            },
        ),
    ]