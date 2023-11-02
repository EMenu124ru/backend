from rest_framework import decorators, response, status

from apps.core.viewsets import CreateReadUpdateDestroyViewSet
from apps.reviews.models import Review
from apps.reviews.permissions import ReviewPermissions
from apps.reviews.serializers import ReviewImageSerializer, ReviewSerializer


class ReviewViewSet(CreateReadUpdateDestroyViewSet):
    serializer_class = ReviewSerializer
    queryset = Review.objects.all()
    permission_classes = (ReviewPermissions,)

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
                ReviewImageSerializer(data={
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
                data={"images": "Изображения отсутствуют"},
                status=status.HTTP_400_BAD_REQUEST,
                exception=True,
            )
        serializers = [
            ReviewImageSerializer(data={
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
            ReviewImageSerializer(
                review.images.all(),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )
