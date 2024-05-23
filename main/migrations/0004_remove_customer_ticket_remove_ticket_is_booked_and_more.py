import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_remove_customer_ticket_customer_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='ticket',
        ),
        migrations.RemoveField(
            model_name='ticket',
            name='is_booked',
        ),
        migrations.AddField(
            model_name='ticket',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='main.customer'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='seat_number',
            field=models.CharField(max_length=4),
        ),
    ]
