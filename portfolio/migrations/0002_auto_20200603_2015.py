# Generated by Django 3.0.6 on 2020-06-03 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sizes',
            options={'verbose_name': 'Size', 'verbose_name_plural': 'Sizes'},
        ),
        migrations.RenameField(
            model_name='artpiece',
            old_name='price',
            new_name='base_price',
        ),
        migrations.RemoveField(
            model_name='sizes',
            name='price',
        ),
        migrations.AddField(
            model_name='artpiece',
            name='is_for_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='sizes',
            name='printing_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True),
        ),
        migrations.AlterField(
            model_name='artcollection',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='artpiece',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='codeproject',
            name='name',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
