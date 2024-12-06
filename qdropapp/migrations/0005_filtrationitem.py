# Generated by Django 5.0.4 on 2024-12-01 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qdropapp', '0004_watersolution'),
    ]

    operations = [
        migrations.CreateModel(
            name='FiltrationItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text="Title of the filtration item (e.g., 'Dual Media Filter')", max_length=255)),
                ('description', models.TextField(help_text='Description of the filtration item')),
                ('image', models.ImageField(help_text='Image for the filtration item', upload_to='filtration_items/')),
                ('button_text', models.CharField(default='Download Catalog', help_text='Button text', max_length=255)),
                ('button_link', models.URLField(blank=True, help_text='Optional button link', null=True)),
            ],
        ),
    ]
