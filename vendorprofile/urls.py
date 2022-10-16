from django.urls import path, include

from vendorprofile.views import *

app_name = 'vendor_profile'
urlpatterns = [
    path('vendor/profile/<int:vendor_id>', VendorProfileView.as_view(), name='VendorProfileView'),
    path('vendor/profile/update', VendorProfileUpdateView.as_view(), name='VendorProfileUpdate'),
    path('vendor/filter', FilterProfileView.as_view(), name='FilterProfile'),
    path('vendor/category/wise/filter/<str:pk>', FilterVendorCategoryWiseView.as_view(), name='FilterVendorProfileByCategory'),
    path('vendor/name/wise/filter/<str:query>', FilterVendorNameWiseView.as_view(), name='FilterVendorProfile'),
    path('vendor/review/create/<int:vendor_id>/<int:reservation_id>', ReviewsAndRatingsView.as_view(), name='CreateReviewsAndRatings'),
    path('vendor/review/update/<int:review_id>', ReviewsAndRatingsView.as_view(), name='UpdateReviewsAndRatings'),
    path('vendor/rating/<int:vendor_id>', CalculateReviewView.as_view(), name='CalculateReview'),
    # path('vendor/review/delete/<int:review_id>', ReviewsAndRatingsView.as_view(), name='DeleteReviewsAndRatings'),
    path('businesscategorylist', BusinessCategoryList.as_view(), name='BusinessCategoryListAPIView'),
    path('businesscategorylist/<str:pk>/', BusinessCategoryDetails.as_view(), name='BusinessCategoryListAPIView'),
    path('home/page/information/<str:type>', HomePageInformation.as_view(), name='HomePageInformationAPIView'),

    path('VendorAPIView', VendorAPIView.as_view(), name='VendorAPIView'),

]
