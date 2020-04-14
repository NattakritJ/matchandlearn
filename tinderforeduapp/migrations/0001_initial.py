# Generated by Django 3.0.3 on 2020-04-14 20:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_one', models.TextField(blank=True, max_length=200)),
                ('user_two', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='RequestSender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('request_list', models.TextField(blank=True, max_length=200)),
                ('request_message', models.TextField(blank=True, max_length=600)),
                ('receiver', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectContainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.TextField(blank=True, max_length=200)),
                ('subject_store', models.TextField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(blank=True, max_length=200)),
                ('firstname', models.TextField(blank=True, max_length=200)),
                ('lastname', models.TextField(blank=True, max_length=200)),
                ('age', models.TextField(blank=True, max_length=10)),
                ('school', models.TextField(blank=True, max_length=200)),
                ('school_common_name', models.TextField(blank=True, max_length=200)),
                ('gender', models.TextField(blank=True)),
                ('fb_link', models.TextField(null=True)),
                ('match_request', models.IntegerField(default=0)),
                ('massage_list', models.IntegerField(default=0)),
                ('expertise_subject', models.ManyToManyField(blank=True, related_name='Userinfos', to='tinderforeduapp.SubjectContainer')),
                ('match', models.ManyToManyField(blank=True, to='tinderforeduapp.MatchContainer')),
                ('request', models.ManyToManyField(blank=True, to='tinderforeduapp.RequestSender')),
            ],
        ),
        migrations.CreateModel(
            name='ProfilePic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(default='default.png', upload_to='media')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='tinderforeduapp.UserInfo')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=100)),
                ('last_name', models.CharField(blank=True, max_length=100)),
                ('college', models.CharField(blank=True, max_length=100)),
                ('email', models.EmailField(max_length=150)),
                ('age', models.TextField(blank=True, max_length=10)),
                ('gender', models.TextField()),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=80, null=True)),
                ('comment', models.CharField(max_length=500, null=True)),
                ('star', models.CharField(max_length=500, null=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, null=True)),
                ('active', models.BooleanField(default=True, null=True)),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='tinderforeduapp.UserInfo')),
            ],
            options={
                'ordering': ['created_on'],
            },
        ),
    ]
