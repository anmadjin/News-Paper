from django.core.management.base import BaseCommand, CommandError
from ...models import Category, Post


class Command(BaseCommand):
    help = 'Удаляет все новости и статьи из указанной категории'

    def add_arguments(self, parser):
        parser.add_argument('category', type=str, help='Название категории')

    def handle(self, *args, **options):
        category_name = options['category']

        answer = input(f'Вы действительно хотите удалить все статьи в категории "{category_name}"? (yes/no): ')

        if answer.lower() != 'yes':
            self.stdout.write(self.style.ERROR('Операция отменена'))
            return

        try:
            category = Category.objects.get(name=category_name)

            posts_count = Post.objects.filter(category=category).count()

            if posts_count == 0:
                self.stdout.write(self.style.WARNING(f'В категории "{category_name}" нет новостей'))
                return

            Post.objects.filter(category=category).delete()

            self.stdout.write(
                self.style.SUCCESS(f'Успешно удалено {posts_count} новостей из категории "{category_name}"')
            )

        except Category.DoesNotExist:
            self.stdout.write(
                self.style.ERROR(f'Категория "{category_name}" не найдена')
            )