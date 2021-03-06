# Generated by Django 3.1.7 on 2021-06-06 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Foodadd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('food_name', models.CharField(max_length=30)),
                ('food_photo', models.ImageField(blank=True, null=True, upload_to='foodPhotos/%Y/%m/')),
                ('food_ingredients', models.TextField(blank=True, null=True)),
                ('mutfak_tur', models.CharField(choices=[('Afrika', 'Afrika'), ('Asya', 'Asya'), ('Avrupa', 'Avrupa'), ('Orta Doğu', 'Orta Doğu'), ('Kuzey Amerika', 'Kuzey Amerika'), ('Güney Amerika', 'Güney Amerika'), ('Okyanusya', 'Okyanusya'), ('Diğer', 'Diğer')], default='Diğer', max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Food',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.foodadd')),
                ('userfk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User ID')),
            ],
        ),
    ]
