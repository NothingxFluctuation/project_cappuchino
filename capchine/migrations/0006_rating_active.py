# Generated by Django 2.2.3 on 2019-08-09 18:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('capchine', '0005_auto_20190809_2213'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='active',
            field=models.BooleanField(default=True),
        ),
    ]
