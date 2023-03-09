from rest_framework import decorators, response, status

from apps.core.views import CRUDViewSet, DestroyViewSet

from ..models.models import Review, ReviewImages
from ..permissions.permissions import ReviewImagePermissions, ReviewPermissions, permissions
from ..serializers.serializers import ReviewImagesSerializer, ReviewSerializer


class ReviewViewSet(CRUDViewSet):

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (ReviewPermissions, )

    def perform_destroy(self, instance) -> None:
        for image in instance.images.all():
            image.image.storage.delete(image.image.path)
        instance.delete()

    def perform_create(self, serializer) -> None:
        serializer.save(client=self.request.user.client)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        review = Review.objects.get(id=serializer.data["id"])
        if request.data.get("images", None) is not None:
            serializers = [
                ReviewImagesSerializer(data={
                    "image": image,
                    "review": review.pk,
                })
                for image in request.data.pop("images", [])
            ]
            for serializer in serializers:
                serializer.is_valid(raise_exception=True)
                serializer.save()
        return response.Response(
            data=ReviewSerializer(review).data,
            status=status.HTTP_201_CREATED,
        )

    @decorators.action(methods=("POST",), detail=True)
    def images(self, request, *args, **kwargs):
        if request.data.get("images", None) is None:
            return response.Response(
                data={"message": "Изображения отсутствуют"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializers = [
            ReviewImagesSerializer(data={
                "image": image,
                "review": self.kwargs["pk"],
            })
            for image in request.data.pop("images")
        ]
        for serializer in serializers:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        review = Review.objects.get(id=self.kwargs["pk"])
        return response.Response(
            ReviewImagesSerializer(
                review.images.all(),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )


class ReviewImageViewSet(DestroyViewSet):

    queryset = ReviewImages.objects.all()
    permission_classes = (
        permissions.IsAuthenticated & ReviewImagePermissions,
    )
