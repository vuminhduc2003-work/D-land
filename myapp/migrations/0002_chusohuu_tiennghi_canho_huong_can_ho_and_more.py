# Generated by Django 5.1.3 on 2024-11-29 14:06

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChuSoHuu',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ho_ten', models.CharField(max_length=100)),
                ('so_dien_thoai', models.CharField(max_length=15)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='TienNghi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ten_tien_nghi', models.CharField(max_length=50)),
                ('mo_ta', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='canho',
            name='huong_can_ho',
            field=models.CharField(choices=[('Đông', 'Đông'), ('Tây', 'Tây'), ('Nam', 'Nam'), ('Bắc', 'Bắc')], default=django.utils.timezone.now, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='canho',
            name='chu_so_huu',
            field=models.ManyToManyField(related_name='can_ho', to='myapp.chusohuu'),
        ),
        migrations.CreateModel(
            name='Phong',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ma_phong', models.CharField(max_length=20, unique=True)),
                ('ten_phong', models.CharField(max_length=100)),
                ('loai_phong', models.CharField(choices=[('Phòng khách', 'Phòng khách'), ('Phòng ngủ', 'Phòng ngủ'), ('Phòng bếp', 'Phòng bếp'), ('Phòng tắm', 'Phòng tắm')], max_length=50)),
                ('dien_tich', models.DecimalField(decimal_places=2, max_digits=5)),
                ('can_ho', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='phong', to='myapp.canho')),
            ],
        ),
    ]
