from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path('create_listing/', views.create_listing, name='create_listing'),
    path("view_watchlist/", views.view_watchlist, name="view_watchlist"),
    path("listing/<int:listing_id>/", views.view_listing, name="view_listing"),
    path('add_watchlist/', views.add_watchlist, name='add_watchlist'),
    path('remove_watchlist/', views.remove_watchlist, name='remove_watchlist'),
    path('add_bid/', views.add_bid, name='add_bid'),
    path('comment/', views.comment, name='comment'),
    path('categories/', views.categories, name='categories'),
    path('category/<str:categor>/', views.categor, name='category'),
    path('close_auction/', views.close_auction, name='close_auction'),
    path('won/', views.won, name='won')

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)