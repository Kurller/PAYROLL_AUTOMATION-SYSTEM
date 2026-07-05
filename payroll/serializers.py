from rest_framework import serializers

class PayrollUploadSerializer(serializers.Serializer):
    file = serializers.FileField()

    def validate_file(self, value):
        allowed_extensions = ['csv', 'xlsx']

        extension = value.name.split('.')[-1].lower()

        if extension not in allowed_extensions:
            raise serializers.ValidationError(
                "Only CSV and Excel files are allowed"
            )

        return value