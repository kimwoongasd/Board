# Generated by Django 3.2.4 on 2021-07-02 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='pub_date',
            field=models.DateTimeField(verbose_name='date published'),
        ),
    ]
