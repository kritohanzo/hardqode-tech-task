from admin_auto_filters.filters import AutocompleteFilter


class UserFilter(AutocompleteFilter):
    """
    Фильтр для админки,
    позволяющий искать записи на основе поля 'user'.
    """

    title = "Пользователь"
    field_name = "user"


class ProductFilter(AutocompleteFilter):
    """
    Фильтр для админки,
    позволяющий искать записи на основе поля 'product'.
    """

    title = "Продукт"
    field_name = "product"


class LessonFilter(AutocompleteFilter):
    """
    Фильтр для админки,
    позволяющий искать записи на основе поля 'lesson'.
    """

    title = "Урок"
    field_name = "lesson"
