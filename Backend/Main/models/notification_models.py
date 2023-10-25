from django.db import models
import json

notification_choice = (
    ('APPROVED', 'APPROVED'),
    ('DELETED', 'DELETED'),
    ('DECLINED', 'DECLINED'),
    ('CREATED', 'CREATED'),
    ('EDITED', 'EDITED'),
)


reciever_group = (
    ('OPERATIONS', 'OPERATIONS'),
    ('PRINCIPAL', 'PRINCIPAL'),
    ('DIRECTORS', 'DIRECTORS'),
    ('ACCOUNTANT', 'ACCOUNTANT'),
)

class Notification (models.Model):
    sender = models.ForeignKey("Authentication.CustomUser", on_delete=models.CASCADE)
    notification_reciever_group = models.CharField(max_length=50, choices=reciever_group)

    notification_message = models.TextField()
    date_time = models.DateTimeField(auto_now=True)
    users_have_seen_notification = models.JSONField()
    notification_type = models.CharField(max_length=50, choices=notification_choice)



    def delete_notification (self):
        pass 
        
# signals invoke when invoked




def create_notification( *args, **kwargs):
    pass