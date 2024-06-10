from datetime import timedelta
import uuid
from django.core.management.base import BaseCommand
from user_management.models import UserActivities
from django.utils import timezone
import random
import calendar



class Command(BaseCommand):
    help = 'Seed the UserActivities model with sample data'

    def handle(self, *args, **kwargs):
        activities = []
        start_date = timezone.now() - timedelta(days=365)
        end_date = timezone.now()  
        activity_types = ['convert-user', 'convert-other-system']

        while start_date <= end_date:
            days_in_month = calendar.monthrange(start_date.year, start_date.month)[1]
            num_activities = random.randint(40, 80)
            
            for _ in range(num_activities):
                activity_type = random.choice(activity_types)
                activities.append({
                    'user_id': uuid.uuid4(),
                    'ip_address': '192.168.1.1',
                    'activity_type': activity_type,
                    'created_at': start_date,
                })
                start_date += timedelta(days=random.randint(1, days_in_month))

        UserActivities.objects.bulk_create(
            [UserActivities(**activity) for activity in activities]
        )


        self.stdout.write(self.style.SUCCESS('Successfully seeded UserActivities data'))
