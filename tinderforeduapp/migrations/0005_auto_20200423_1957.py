# Generated by Django 3.0.3 on 2020-04-23 12:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tinderforeduapp', '0004_auto_20200423_0251'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilepic',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='image', to='tinderforeduapp.UserInfo'),
        ),
    ]
