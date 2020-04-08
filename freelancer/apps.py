from django.apps import AppConfig


class FreelancerConfig(AppConfig):
    name = 'freelancer'
    def ready(self):
        import freelancer.signals

