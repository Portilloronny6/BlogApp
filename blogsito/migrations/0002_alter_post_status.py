# Generated by Django 4.1 on 2022-10-03 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogsito', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='status',
            field=models.CharField(choices=[('DF', 'Draft'), ('PB', 'Published')], default='DF', max_length=2),
        ),
    ]
