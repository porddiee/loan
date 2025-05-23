# Generated by Django 3.1.5 on 2021-09-04 08:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('loginApp', '0002_auto_20210902_1926'),
        ('loanApp', '0006_auto_20210903_2034'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanrequest',
            name='status_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name='loanrequest',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loan_customer', to='loginApp.customersignup'),
        ),
    ]
