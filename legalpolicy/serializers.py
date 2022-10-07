from rest_framework import serializers, status
from .. utils.dowell import (
    save_document,
    update_document,

    LEGAL_POLICY_COLLECTION,
    LEGAL_POLICY_DOCUMENT_NAME,
    LEGAL_POLICY_KEY
)


class LegalPolicySerializer(serializers.Serializer):
    """
     Retrieve, update and  create Dowell legal policy
    """
    pass