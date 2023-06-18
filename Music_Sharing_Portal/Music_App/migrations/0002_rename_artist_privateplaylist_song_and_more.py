# Generated by Django 4.2.2 on 2023-06-18 16:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Music_App', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='privateplaylist',
            old_name='artist',
            new_name='song',
        ),
        migrations.RenameField(
            model_name='privateplaylist',
            old_name='uploaded_by',
            new_name='user',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='allowed_emails',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='cover_image',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='duration',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='mp3_file',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='name',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='privacy',
        ),
        migrations.RemoveField(
            model_name='privateplaylist',
            name='shared_by',
        ),
        migrations.AlterField(
            model_name='sharerequest',
            name='song',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Music_App.song'),
        ),
    ]
