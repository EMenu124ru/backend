from apps.core.views import CRUDViewSet, DestroyViewSet

from apps.reviews.models import ReviewImage
from apps.reviews.permissions import ReviewImagePermissions, permissions


class ReviewImageViewSet(DestroyViewSet):
    queryset = ReviewImage.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & ReviewImagePermissions,
    )
