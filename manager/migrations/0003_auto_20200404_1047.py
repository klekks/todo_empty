# Generated by Django 3.0.5 on 2020-04-04 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0002_api_api_token'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('i', models.IntegerField(unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='api',
            name='api_token',
            field=models.CharField(default=None, max_length=64, unique=True),
        ),
        migrations.AlterField(
            model_name='api',
            name='token',
            field=models.CharField(max_length=64, primary_key=True, serialize=False, unique=True),
        ),
    ]
