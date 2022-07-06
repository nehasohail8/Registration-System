# Generated by Django 4.0.5 on 2022-06-15 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('form', '0003_remove_contactform_itemid'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AddField(
            model_name='contactform',
            name='password',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contactform',
            name='username',
            field=models.CharField(default=234543234, max_length=100),
            preserve_default=False,
        ),
    ]
