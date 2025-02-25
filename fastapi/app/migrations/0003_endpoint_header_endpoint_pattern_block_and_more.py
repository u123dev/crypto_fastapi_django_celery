# Generated by Django 4.1.3 on 2025-02-16 07:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("app", "0002_currency_provider_endpoint_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="endpoint",
            name="header",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="endpoint",
            name="pattern_block",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name="endpoint",
            name="pattern_timestamp",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="endpoint",
            name="currency",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="endpoint_currencies",
                to="app.currency",
            ),
        ),
        migrations.AlterField(
            model_name="endpoint",
            name="provider",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.PROTECT,
                related_name="endpoint_providers",
                to="app.provider",
            ),
        ),
        migrations.CreateModel(
            name="Block",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("block_number", models.IntegerField()),
                (
                    "created_at",
                    models.DateTimeField(blank=True, db_index=True, null=True),
                ),
                ("stored_at", models.DateTimeField(auto_now=True, db_index=True)),
                (
                    "currency",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="block_currencies",
                        to="app.currency",
                    ),
                ),
                (
                    "provider",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="block_providers",
                        to="app.provider",
                    ),
                ),
            ],
            options={
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddConstraint(
            model_name="block",
            constraint=models.UniqueConstraint(
                fields=("block_number", "currency"), name="unique_currency_block_number"
            ),
        ),
    ]
