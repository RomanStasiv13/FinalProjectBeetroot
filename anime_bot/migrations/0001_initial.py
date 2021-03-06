# Generated by Django 4.0.4 on 2022-05-18 10:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genres',
            fields=[
                ('id_g', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Studio',
            fields=[
                ('id_s', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Anime',
            fields=[
                ('id_a', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('title_eng', models.CharField(blank=True, max_length=255, null=True)),
                ('title_jap', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField()),
                ('url_img', models.CharField(max_length=255)),
                ('year', models.IntegerField(blank=True, null=True)),
                ('score', models.FloatField()),
                ('episodes', models.IntegerField(blank=True, null=True)),
                ('rating', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('trailer_url', models.URLField(blank=True, null=True)),
                ('demographics_genres', models.ManyToManyField(blank=True, related_name='animes_demoghraph', to='anime_bot.genres')),
                ('explicit_genres', models.ManyToManyField(blank=True, related_name='animes_explicit', to='anime_bot.genres')),
                ('genres', models.ManyToManyField(blank=True, related_name='animes', to='anime_bot.genres')),
                ('id_s', models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='anime_bot.studio')),
                ('themes', models.ManyToManyField(blank=True, related_name='animes_theme', to='anime_bot.genres')),
            ],
        ),
    ]
