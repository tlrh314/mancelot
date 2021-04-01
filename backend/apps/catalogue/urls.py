from rest_framework import routers

from catalogue.api import (
    CeceLabelViewSet,
    CertificateViewSet,
    CategoryViewSet,
    SubcategoryViewSet,
    PaymentOptionViewSet,
    StoreViewSet,
    BrandViewSet,
    SizeViewSet,
    ColorViewSet,
    MaterialViewSet,
    ProductViewSet,
)


router = routers.SimpleRouter()
router.register("catalogue/label", CeceLabelViewSet)
router.register("catalogue/certificate", CertificateViewSet)
router.register("catalogue/category", CategoryViewSet)
router.register("catalogue/subcategory", SubcategoryViewSet)
router.register("catalogue/paymentoption", PaymentOptionViewSet)
router.register("catalogue/store", StoreViewSet)
router.register("catalogue/brand", BrandViewSet)
router.register("catalogue/size", SizeViewSet)
router.register("catalogue/color", ColorViewSet)
router.register("catalogue/material", MaterialViewSet)
router.register("catalogue/product", ProductViewSet)


app_name = "catalogue"  # namespace the urls
urlpatterns = []
