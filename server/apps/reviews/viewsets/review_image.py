from apps.core.viewsets import DestroyViewSet
from apps.reviews.models import ReviewImage
from apps.reviews.permissions import ReviewImagePermissions, permissions


class ReviewImageViewSet(DestroyViewSet):
    queryset = ReviewImage.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & ReviewImagePermissions,
    )
