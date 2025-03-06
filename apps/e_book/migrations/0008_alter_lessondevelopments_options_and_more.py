# Generated by Django 5.1.6 on 2025-03-06 02:07

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_book', '0007_lessondevelopments_name_en_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lessondevelopments',
            options={'verbose_name': 'Lesson Development', 'verbose_name_plural': '8. Lesson Developments'},
        ),
        migrations.AlterModelOptions(
            name='question',
            options={'verbose_name': 'Question', 'verbose_name_plural': '6. Questions'},
        ),
        migrations.AlterModelOptions(
            name='quiz',
            options={'verbose_name': 'Quiz', 'verbose_name_plural': '5. Quizzes'},
        ),
        migrations.AlterModelOptions(
            name='videos',
            options={'verbose_name': 'Video', 'verbose_name_plural': '7. Videos'},
        ),
        migrations.AddField(
            model_name='category',
            name='is_enter_page',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Enter Page'),
        ),
        migrations.CreateModel(
            name='EnterPage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True, verbose_name='Name')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Short Description')),
                ('created_at', models.DateField(auto_now_add=True, null=True, verbose_name='Publication Date')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='enter_pages', to='e_book.category')),
            ],
            options={
                'verbose_name': 'Enter Page',
                'verbose_name_plural': '4. Enter Pages',
                'ordering': ['created_at'],
            },
        ),
    ]
