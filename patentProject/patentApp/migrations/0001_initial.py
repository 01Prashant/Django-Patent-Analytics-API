# Generated by Django 5.1.1 on 2024-09-09 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('patent_id', models.CharField(max_length=100)),
                ('title', models.TextField()),
                ('assignee', models.CharField(max_length=255, null=True)),
                ('inventor', models.TextField(null=True)),
                ('priority_date', models.DateField(null=True)),
                ('filing_date', models.DateField(null=True)),
                ('publication_date', models.DateField(null=True)),
                ('grant_date', models.DateField(null=True)),
                ('result_link', models.URLField(null=True)),
                ('representative_figure_link', models.URLField(null=True)),
            ],
        ),
    ]
