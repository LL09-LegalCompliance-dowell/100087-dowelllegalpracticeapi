from django.db import models


class IAgreeToPolicyTracker(models.Model):
    policy_request_id = models.CharField(max_length=255, unique=True)
    session_id = models.CharField(max_length=255, default=" ")
    i_agree = models.BooleanField(default=False)
    log_datetime = models.DateTimeField()
    i_agreed_datetime = models.DateTimeField(null=True)
    legal_policy_type = models.CharField(max_length=255, default=" ")



    def __repr__(self) -> str:
        return f"<IAgreeToPolicyTracker: session_id({self.session_id}), policy_request_id({self.policy_request_id}), i_agree({self.i_agree}), >"


    def format(self):
        return {
            "event_id": self.policy_request_id,
            "session_id": self.session_id,
            "i_agree": self.i_agree,
            "log_datetime": self.log_datetime.isoformat(),
            "i_agreed_datetime": self.i_agreed_datetime.isoformat() if self.i_agree else None,
            "legal_policy_type": self.legal_policy_type
        }



