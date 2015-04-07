from django.dispatch import Signal


registry_ready = Signal(providing_args=["registry"])
