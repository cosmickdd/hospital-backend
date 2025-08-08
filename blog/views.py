# blog/views.py
from rest_framework import generics, permissions, filters
from .models import TherapyArticle
from .serializers import TherapyArticleSerializer
from rest_framework.permissions import IsAdminUser

class TherapyArticleListView(generics.ListAPIView):
    serializer_class = TherapyArticleSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['category', 'title']

    def get_queryset(self):
        queryset = TherapyArticle.objects.all()
        category = self.request.query_params.get('category')
        if category:
            queryset = queryset.filter(category=category)
        return queryset

class TherapyArticleDetailView(generics.RetrieveAPIView):
    queryset = TherapyArticle.objects.all()
    serializer_class = TherapyArticleSerializer
    permission_classes = (permissions.AllowAny,)

class TherapyArticleBySlugView(generics.RetrieveAPIView):
    queryset = TherapyArticle.objects.all()
    serializer_class = TherapyArticleSerializer
    lookup_field = 'slug'
    permission_classes = (permissions.AllowAny,)

# Admin-only CRUD
class TherapyArticleCreateView(generics.CreateAPIView):
    queryset = TherapyArticle.objects.all()
    serializer_class = TherapyArticleSerializer
    permission_classes = (IsAdminUser,)

class TherapyArticleUpdateView(generics.UpdateAPIView):
    queryset = TherapyArticle.objects.all()
    serializer_class = TherapyArticleSerializer
    permission_classes = (IsAdminUser,)

class TherapyArticleDeleteView(generics.DestroyAPIView):
    queryset = TherapyArticle.objects.all()
    serializer_class = TherapyArticleSerializer
    permission_classes = (IsAdminUser,)
