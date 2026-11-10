import json
import yaml
from decimal import Decimal
from .models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter


def import_from_dict(data, shop_name):
    result = {'created': 0, 'updated': 0, 'errors': [],}
    shop, _ = Shop.objects.get_or_create(name=shop_name)
    categories_map = {}
    for cat_data in data.get('categories', []):
        cat, created = Category.objects.get_or_create(name=cat_data['name'],)
        cat.shops.add(shop)
        categories_map[cat_data['id']] = cat
    for good in data.get('goods', []):
        try:
            category = categories_map.get(good.get('category'))
            if not category:
                result['errors'].append(f"Товар {good['id']}: категория не найдена.")
                continue
            product, _ = Product.objects.get_or_create(name=good['name'], defaults={'category': category},)
            if product.category != category:
                product.category = category
                product.save()

            product_info, created = ProductInfo.objects.update_or_create(
                shop=shop,
                defaults={
                    'product': product,
                    'quantity': good.get('quantity', 0),
                    'price': Decimal(str(good.get('price', 0))),
                },
            )
            if created:
                result['created'] += 1
            else:
                result['updated'] += 1
            for param_name, param_value in good.get('parameters', {}).items():
                param, _ = Parameter.objects.get_or_create(name=param_name)
                ProductParameter.objects.update_or_create(
                    product_info=product_info,
                    parameter=param,
                    defaults={'value': str(param_value)},
                )
        except Exception as e:
            result['errors'].append(f"Товар {good.get('id', '?')}: {str(e)}")
    return result


def import_from_file(file_path, shop_name):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    if file_path.endswith('.yaml') or file_path.endswith('.yml'):
        data = yaml.safe_load(content)
    elif file_path.endswith('.json'):
        data = json.loads(content)
    else:
        raise ValueError('Неподдерживаемый формат. Требуется YAML|JSON.')
    if shop_name is None:
        shop_name = data.get('shop', 'Импортированный магазин')
    return import_from_dict(data, shop_name)


def import_from_uploaded_file(file_obj, shop_name):
    content = file_obj.read().decode('utf-8')
    filename = getattr(file_obj, 'name', '')
    if filename.endswith('.yaml') or filename.endswith('.yml'):
        data = yaml.safe_load(content)
    elif filename.endswith('.json'):
        data = json.loads(content)
    else:
        try:
            data = json.loads(content)
        except json.JSONDecodeError:
            data = yaml.safe_load(content)
    if shop_name is None:
        shop_name = data.get('shop', 'Импортированный магазин')
    return import_from_dict(data, shop_name)