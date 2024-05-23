from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_rename_seat_customer_ticket'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='ticket',
        ),
        migrations.AddField(
            model_name='customer',
            name='ticket',
            field=models.ManyToManyField(related_name='custormers', to='main.ticket'),
        ),
    ]
