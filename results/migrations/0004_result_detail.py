# Generated by Django 3.0.3 on 2021-07-01 19:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mcqs', '0003_auto_20210617_1143'),
        ('results', '0003_auto_20210617_1143'),
    ]

    operations = [
        migrations.CreateModel(
            name='Result_detail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=500)),
                ('selected_answer', models.CharField(max_length=300)),
                ('correct_answer', models.CharField(max_length=300)),
                ('test_name', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mcqs.Test')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
