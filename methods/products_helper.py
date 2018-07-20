from products.models import Cartridge, CartridgeRecipe, PackageCartridge, \
    PackageCartridgeRecipe, Supply, ExtraIngredient
from sales.models import CartridgeTicketDetail
import calendar, json
from django.db.models import Count, Sum


class ProductsHelper(object):
    def __init__(self):
        super(ProductsHelper, self).__init__()
        self.__cartridges = None
        self.__packages_cartridges = None
        self.__supplies = None
        self.__extra_ingredients = None
        self.__all_cartridges_recipes = None
        self.__elements_in_warehouse = None
        self.__all_packages_cartridges_recipes = None
        self.__cartridges_sales = None

    def get_all_supplies(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__supplies is None:
            self.set_supplies()
        return self.__supplies

    @property
    def cartridges(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__cartridges is None:
            self.set_cartridges()
        return self.__cartridges

    @property
    def packages_cartridges(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__packages_cartridges is None:
            self.set_packages_cartridges()
        return self.__packages_cartridges

    def get_extra_ingredients(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__extra_ingredients is None:
            self.set_extra_ingredients()

        return self.__extra_ingredients

    def get_cartridges_recipes(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__all_cartridges_recipes is None:
            self.set_cartridges_recipes()

        return self.__all_cartridges_recipes

    def get_packages_cartridges_recipes(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__all_packages_cartridges_recipes is None:
            self.set_package_cartridges_recipes()

        return self.__all_packages_cartridges_recipes

    def get_elements_in_warehouse(self):
        """
        :rtype: django.db.models.query.QuerySet
        """
        if self.__elements_in_warehouse is None:
            self.set_elements_in_warehouse()
        return self.__elements_in_warehouse

    def get_cartridges_sales(self):
        if self.__cartridges_sales_by_dates() is None:
            self.set_cartridges_sales()
        return self.__cartridges_sales_by

    def get_cartridges_sales_by_date(self,year,month,category):

        names = []
        tick_sales = []

        all_cartridges_ticket_details = Cartridge.objects.filter(cartridgeticketdetail__ticket_base__created_at__year=year,
                                                                 cartridgeticketdetail__ticket_base__created_at__month=month) \
                                                                .annotate(num_sales=Sum('cartridgeticketdetail__quantity')).order_by('name')

        if category == 'food_sold':
            filter_all_cartridges_ticket_details = all_cartridges_ticket_details.filter(
                category='FD')
        if category == 'drinks_sold':
            filter_all_cartridges_ticket_details = all_cartridges_ticket_details.filter(
                category='CO')
        if category == 'select':
            filter_all_cartridges_ticket_details = all_cartridges_ticket_details

        for tick_cartridges in filter_all_cartridges_ticket_details:
            tick_sales.append(tick_cartridges.num_sales)
            names.append(tick_cartridges.name)

        all_cartridges_pack_ticket_details = PackageCartridge.objects.filter(packagecartridgeticketdetail__ticket_base__created_at__year=year,
                                                                             packagecartridgeticketdetail__ticket_base__created_at__month=month) \
                                            .annotate(num_sales=Sum('packagecartridgeticketdetail__quantity')).order_by('name')

        recipes = PackageCartridgeRecipe.objects.select_related(
            'cartridge').select_related('package_cartridge')

        for tick_pack in all_cartridges_pack_ticket_details:
            cartridges_in_pack = recipes.filter(package_cartridge=tick_pack)
            for cart in cartridges_in_pack:
                if cart.cartridge.name in names:
                    tick_sales[names.index(
                        cart.cartridge.name)] += tick_pack.num_sales
                else:
                    if category == 'food_sold':
                        if cart.cartridge.category == "FD":
                            names.append(cart.cartridge.name)
                            tick_sales.append(tick_pack.num_sales)
                    if category == 'drinks_sold':
                        if cart.cartridge.category == "CO":
                            names.append(cart.cartridge.name)
                            tick_sales.append(tick_pack.num_sales)
                    if category == 'select':
                        names.append(cart.cartridge.name)
                        tick_sales.append(tick_pack.num_sales)
        obj = {
            'names': names,
            'tick_sales': tick_sales,
        }

        sales_data = json.dumps(obj)

        range_day = calendar.monthrange(year, month)

        sales_data_by_date = []
        for i in range(range_day[0] + 1, range_day[1] + 1):
            name_d = []
            num_d = []

            cartridge_per_day = Cartridge.objects.filter(cartridgeticketdetail__ticket_base__created_at__year=year,
                                                        cartridgeticketdetail__ticket_base__created_at__month=month,
                                                        cartridgeticketdetail__ticket_base__created_at__day=i)\
                                        .annotate(num_sales=Sum('cartridgeticketdetail__quantity')).order_by('name')

            if category == 'food_sold':
                filter_cartridge_per_day = cartridge_per_day.filter(
                    category='FD')
            if category == 'drinks_sold':
                filter_cartridge_per_day = cartridge_per_day.filter(
                    category='CO')
            if category == 'select':
                filter_cartridge_per_day = cartridge_per_day

            for tick_cartridges in filter_cartridge_per_day:
                name_d.append(tick_cartridges.name)
                num_d.append(tick_cartridges.num_sales)

            packagecartridge_per_day = PackageCartridge.objects.filter(packagecartridgeticketdetail__ticket_base__created_at__year=year,
                                                                                packagecartridgeticketdetail__ticket_base__created_at__month=month,
                                                                                packagecartridgeticketdetail__ticket_base__created_at__day=i)\
                                            .annotate(num_sales=Sum('packagecartridgeticketdetail__quantity')).order_by('name')

            recipes = PackageCartridgeRecipe.objects.select_related(
                'cartridge').select_related('package_cartridge')

            for tick_pack in packagecartridge_per_day:
                cartridges_in_pack = recipes.filter(
                    package_cartridge=tick_pack)
                for cart in cartridges_in_pack:
                    if cart.cartridge.name in name_d:
                        num_d[name_d.index(
                            cart.cartridge.name)] += tick_pack.num_sales
                    else:
                        if category == 'food_sold':
                            if cart.cartridge.category == "FD":
                                name_d.append(cart.cartridge.name)
                                num_d.append(tick_pack.num_sales)
                        if category == 'drinks_sold':
                            if cart.cartridge.category == "CO":
                                name_d.append(cart.cartridge.name)
                                num_d.append(tick_pack.num_sales)
                        if category == 'select':
                            name_d.append(cart.cartridge.name)
                            num_d.append(tick_pack.num_sales)

            obj = {
                'names': name_d,
                'tick_sales': num_d,
            }

            sales_data_by_date.append(obj)

        final_dates = []
        final_names = []

        for sale_data_bd in sales_data_by_date:
            a = sale_data_bd['names']
            for name in a:
                if name not in final_names:
                    final_names.append(name)

        for name in final_names:
            dates = []
            for sale_data_bd in sales_data_by_date:
                a = sale_data_bd['names']
                b = sale_data_bd['tick_sales']
                if name in a:
                    dates.append(b[a.index(name)])
                else:
                    dates.append(0)
            final_dates.append(dates)

        modify_sales_data_by_date = {
            'final_name': final_names,
            'final_dates': final_dates,
        }

        json_sales_data_by_date = json.dumps(modify_sales_data_by_date)

        final_data = {
            'sales_data': sales_data,
            'json_sales_data_by_date': json_sales_data_by_date,
        }

        return final_data


    def set_supplies(self):
        self.__supplies = Supply.objects. \
            select_related('category'). \
            select_related('supplier'). \
            select_related('location').order_by('name')

    def set_cartridges(self):
        self.__cartridges = Cartridge.objects.order_by('subcategory', 'name')

    def set_packages_cartridges(self):
        self.__packages_cartridges = PackageCartridge.objects.all()

    def set_cartridges_recipes(self):
        self.__all_cartridges_recipes = CartridgeRecipe.objects. \
            select_related('cartridge'). \
            select_related('supply'). \
            all()

    def set_package_cartridges_recipes(self):
        self.__all_packages_cartridges_recipes = PackageCartridgeRecipe.objects. \
            select_related('package_cartridge'). \
            select_related('cartridge'). \
            all()

    def set_extra_ingredients(self):
        self.__extra_ingredients = ExtraIngredient.objects. \
            select_related('ingredient'). \
            select_related('cartridge'). \
            all()

    def set_elements_in_warehouse(self):
        self.__elements_in_warehouse = Warehouse.objects.select_related('supply').all().order_by('supply__name')

    def set_cartridges_sales(self):
        self.__elements_in_warehouse = Cartridge.objects.select_related('supply').all().order_by('supply__name')
