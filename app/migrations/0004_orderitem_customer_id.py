# Generated by Django 3.2.4 on 2021-06-11 16:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_order_orderitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='Customer_id',
            field=models.ForeignKey(default=1, null=True, on_delete=django.db.models.deletion.SET_NULL, to='app.customerregister'),
        ),
    ]
