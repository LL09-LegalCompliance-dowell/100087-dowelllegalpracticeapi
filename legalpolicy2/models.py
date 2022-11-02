from django.db import models


class IAgreeToPolicyTracker(models.Model):
    policy_request_id = models.CharField(max_length=255, unique=True)
    i_agree = models.BooleanField(default=False)
    log_datetime = models.DateTimeField()



    def __repr__(self) -> str:
        return f"<IAgreeToPolicyTracker: policy_request_id({self.policy_request_id}), i_agree({self.i_agree}), >"



