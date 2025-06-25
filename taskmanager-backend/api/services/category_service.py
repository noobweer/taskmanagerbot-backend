from ..models import *
from ..serializers import CategorySerializer


class CategoryService:
    def __init__(self):
        self.Category = Category.objects

    def create_category(self, data):
        try:
            category_name = data.get('name')

            if not all([category_name]):
                return {'is_created': False,
                        'message': 'Send all required fields (name)'}

            if self.Category.filter(name=category_name).exists():
                return {'is_created': False, 'message': f'Category already exists ({category_name})'}

            self.Category.create(name=category_name)
            return {'is_created': True, 'message': f'Category created successfully'}
        except Exception as e:
            return {'is_created': False, 'message': str(e)}

    def edit_category(self, data):
        try:
            category_id = data.get('id')
            category_name = data.get('name')

            if not all([category_id, category_name]):
                return {'is_edited': False,
                        'message': 'Send all required fields (id, name)'}

            if not self.Category.filter(id=category_id).exists():
                return {'is_edited': False, 'message': f'Invalid category_id ({category_id})'}
            category_obj = self.Category.get(id=category_id)

            category_obj.name = category_name
            category_obj.save()
            return {'is_edited': True, 'message': 'Category edited successfully'}
        except Exception as e:
            return {'is_edited': False, 'message': str(e)}

    def delete_category(self, data):
        category_id = data.get('id')

        if not all([category_id]):
            return {'is_deleted': False,
                    'message': 'Send all required fields (id)'}

        if not self.Category.filter(id=category_id).exists():
            return {'is_deleted': False, 'message': f'Invalid category_id ({category_id})'}

    def categories(self):
        try:
            categories_list = self.Category.all()
            serializer = CategorySerializer(categories_list, many=True)
            return {'success': True, 'categories': serializer.data}
        except Exception as e:
            print(e)
            return {'success': False, 'categories': []}