from django.conf import settings
from django.db import models



class ProductPhoto(models.Model):

    caption = models.CharField(max_length=120, null=True, blank=True)
    photo = models.ImageField(upload_to='products')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)


class RecipePhoto(models.Model):

    caption = models.CharField(max_length=120, null=True, blank=True)
    photo = models.ImageField(upload_to='recipes')
    recipe = models.ForeignKey('Recipe', on_delete=models.CASCADE)



class Provider(models.Model):

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=200, null=True, blank=True)
    url = models.URLField(max_length=200)

    def __str__(self):
        return str(self.name)


class ProductProvider(Provider):
    pass


class SupplementProvider(Provider):
    pass


class ProductOffering(models.Model):

    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    provider = models.ForeignKey(ProductProvider, on_delete=models.PROTECT)
    url = models.URLField(max_length=200)


class SupplementOffering(models.Model):

    supplement = models.ForeignKey('Supplement', on_delete=models.CASCADE)
    provider = models.ForeignKey(SupplementProvider, on_delete=models.PROTECT)
    url = models.URLField(max_length=200)



class Product(models.Model):

    providers = models.ManyToManyField(ProductProvider, through=ProductOffering)

    name = models.CharField(max_length=120)
    desc = models.CharField(max_length=3000, blank=True)
    carbs = models.FloatField()
    proteins = models.FloatField()
    fats = models.FloatField()
    calories = models.FloatField()

    def __str__(self):
        return str(self.name)


class ProductDeal(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='deals', on_delete=models.CASCADE)
    products = models.ManyToManyField(ProductOffering)
    suplements = models.ManyToManyField(SupplementOffering)
    created_on = models.DateTimeField(auto_now_add=True)



class Tag(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):
        return str(self.name)


class Comment(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    contents = models.CharField(max_length=2000)
    recipe = models.ForeignKey('Recipe', related_name='comments', on_delete=models.CASCADE)


class Ingredient(models.Model):

    product = models.ForeignKey(Product, related_name='+', on_delete=models.PROTECT)
    recipe = models.ForeignKey('Recipe', related_name='ingredients', on_delete=models.PROTECT)
    amount = models.FloatField()


class Recipe(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    tags = models.ManyToManyField(Tag)
    based_on = models.ForeignKey('Recipe', null=True, blank=True, on_delete=models.SET_NULL)

    is_custom = models.BooleanField()
    title = models.CharField(max_length=120, blank=True)
    content = models.TextField(max_length=120, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField()


    def __str__(self):
        return str(self.title)


class Meal(models.Model):

    BREAKFAST = 'B1'
    SECOND_BREAKFAST = 'B2'
    DINNER = 'D1'
    SECOND_DINNER = 'D2'
    SUPPER = 'S1'
    SECOND_SUPPER = 'S2'

    MEAL_TYLE_CHOICES = (
        (BREAKFAST, 'Breakfast'),
        (SECOND_BREAKFAST, 'Second Breakfast'),
        (DINNER, 'Dinner'),
        (SECOND_DINNER, 'Second Dinner'),
        (SUPPER, 'Supper'),
        (SECOND_SUPPER, 'Second Supper'),
    )

    recipe = models.ForeignKey('Recipe', related_name='meals', on_delete=models.CASCADE)
    plan = models.ForeignKey('Plan', related_name='meals', on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    meal_type = models.CharField(max_length=2, choices=MEAL_TYLE_CHOICES)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.name}: {self.recipe.title}'


class Plan(models.Model):

    REGULAR = 'RE'
    REDUCTION = 'RD'
    GAIN = 'GA'

    PLAN_TYPE_CHOCIES = (
        (REGULAR, 'Regular'),
        (REDUCTION, 'Reduction'),
        (GAIN, 'Gain')
        )

    recipes = models.ManyToManyField(Recipe, through='Meal')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=120, blank=True)
    plan_type = models.CharField(max_length=2, choices=PLAN_TYPE_CHOCIES)
    created_on = models.DateTimeField(auto_now_add=True)


class PlanExecution(models.Model):

    plan = models.ForeignKey(Plan, related_name='executions', on_delete=models.CASCADE)
    started_on = models.DateTimeField()
    finished_on = models.DateTimeField()


class Supplements(models.Model):

    supplement = models.ForeignKey('Supplement', related_name='+', on_delete=models.PROTECT)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    dosage = models.FloatField()


class Supplement(models.Model):

    name = models.CharField(max_length=120)
    description = models.CharField(max_length=3000)
    providers = models.ManyToManyField(SupplementProvider, through=SupplementOffering)


