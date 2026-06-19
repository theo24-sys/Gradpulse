# Generated manually

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_unismartmastercourse'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='accepted_terms_at',
            field=models.DateTimeField(blank=True, help_text='Timestamp when user accepted Privacy Policy & Terms of Service', null=True),
        ),
    ]
