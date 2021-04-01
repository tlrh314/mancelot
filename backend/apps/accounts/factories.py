import factory
from faker import Factory
from django.conf import settings
from django_countries import countries

from accounts.models import UserModel
from catalogue.models import Product
from catalogue.models import FavoriteProduct
from catalogue.factories import ProductFactory

faker = Factory.create("nl_NL")


class UserModelFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = UserModel
        django_get_or_create = ("email",)

    email = factory.LazyAttribute(lambda _: faker.email())
    full_name = factory.LazyAttribute(lambda _: "TestUser " + faker.name())
    address = factory.LazyAttribute(lambda _: faker.street_address())
    zip_code = factory.LazyAttribute(lambda _: faker.postcode())
    city = factory.LazyAttribute(lambda _: faker.city())
    country = "NL"  # alternatively, use code below to randomly select
    # country = factory.LazyAttribute(lambda _:
    #     list(countries)[faker.random_int(min=0, max=len(countries)-1)][0]  # ('NL', 'Nederland')
    # )
    iban = factory.LazyAttribute(lambda _: faker.iban())

    is_active = True
    is_staff = False
    is_superuser = False

    @factory.post_generation
    def favorites(self, create, extracted, **kwargs):  # M2M relation
        if not create or kwargs.get("skip"):
            return

        if extracted:
            for favorite_product in extracted:
                self.favorites.add(favorite_product)
            return

        # Create Product instances if there are less than twenty-five available
        if Product.objects.count() < 25:
            ProductFactory.create_batch(25 - Product.objects.count())

        number_of_favorites_to_add = faker.random_int(
            min=0, max=Product.objects.count() - 1
        )
        all_products_randomly_ordered = Product.objects.order_by("?")
        for j in range(number_of_favorites_to_add):
            fav = FavoriteProduct(
                product=all_products_randomly_ordered[j],
                user=self,
                quantity=faker.random_int(min=1, max=10),
            )
            fav.save()
            self.favorites.add(fav)


class AdminFactory(UserModelFactory):
    is_staff = True
    is_superuser = True
