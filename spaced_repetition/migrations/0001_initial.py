# Generated by Django 2.2.1 on 2019-08-14 18:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=300)),
                ('url', models.TextField(blank=True, max_length=500, null=True)),
                ('comment', models.TextField(blank=True, max_length=2000, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('last_review_at', models.DateField()),
                ('level', models.IntegerField()),
            ],
        ),
    ]