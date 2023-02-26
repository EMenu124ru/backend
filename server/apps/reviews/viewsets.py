from rest_framework import response, status

from apps.core.views import CreateDestroyViewSet, CRUDViewSet

from .models import Review, ReviewImages
from .serializers import ReviewImagesSerializer, ReviewSerializer


class ReviewViewSet(CRUDViewSet):

    serializer_class = ReviewSerializer
    queryset = Review.objects.all()

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


class ReviewImageViewSet(CreateDestroyViewSet):

    queryset = ReviewImages.objects.all()

    def create(self, request, *args, **kwargs):
        serializers = [
            ReviewImagesSerializer(data={
                "image": image,
                "review": request.data.get("review"),
            })
            for image in request.data.pop("images")
        ]
        for serializer in serializers:
            serializer.is_valid(raise_exception=True)
            serializer.save()
        review = Review.objects.get(id=request.data.get("review"))
        return response.Response(
            ReviewImagesSerializer(
                review.images.all(),
                many=True,
            ).data,
            status=status.HTTP_201_CREATED,
        )
