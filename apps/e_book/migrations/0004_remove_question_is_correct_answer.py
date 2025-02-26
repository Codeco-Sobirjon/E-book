# Generated by Django 5.1.6 on 2025-02-24 06:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_book', '0003_question_is_correct'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='is_correct',
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=300, verbose_name='Answer Text')),
                ('is_correct', models.BooleanField(default=False, verbose_name='Is Correct')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='e_book.question')),
            ],
            options={
                'verbose_name': 'Answer',
                'verbose_name_plural': 'Answers',
            },
        ),
    ]
