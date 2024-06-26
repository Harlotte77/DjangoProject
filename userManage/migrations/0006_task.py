# Generated by Django 4.2.11 on 2024-04-18 08:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('userManage', '0005_admin'),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=64, verbose_name='标题')),
                ('detail', models.TextField(verbose_name='任务详细信息')),
                ('level', models.SmallIntegerField(choices=[(1, '紧急'), (2, '重要'), (3, '次要')], default=2, verbose_name='任务级别')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userManage.admin', verbose_name='任务负责人')),
            ],
        ),
    ]
