# Generated by Django 4.0.4 on 2022-06-13 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('items', '0003_alter_item_description_alter_prestamo_comentario_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prestamo',
            name='fecha_devuelto',
            field=models.DateTimeField(null=True, verbose_name='fecha devuelto'),
        ),
    ]
