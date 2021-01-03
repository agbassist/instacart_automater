import gspread
from ingredient import Ingredient


class SheetReader:

    def __init__(self, credentials='google_credentials.json', spreadsheet_name='Copy of Grocery Shopping'):
        self._gc = gspread.service_account(credentials)
        self._spread_sheet = self._gc.open(spreadsheet_name)
        self._ingredients = []
        self._ingredient_names = []

    def __get_ingredients(self):
        self._ingredients = []

        # Build a list of all ingredients available
        worksheet = self._spread_sheet.worksheet('Ingredients')
        ingredient_names = worksheet.col_values(1)[1:]
        ingredient_quantities = worksheet.col_values(3)[1:]

        for i, ingredient_name in enumerate(ingredient_names):
            if int(ingredient_quantities[i]) != 0:
                self._ingredients.append(Ingredient(ingredient_name))

    def __get_ingredient_names(self):
        self._ingredient_names = []

        # Build a list of all ingredients available
        worksheet = self._spread_sheet.worksheet('Ingredients')

        for ingredient_name in worksheet.col_values(1)[1:]:
            self._ingredient_names.append(ingredient_name)

    def get_shopping_list(self):

        # Refresh the ingredients list
        self.__get_ingredients()

        # Get the menu
        worksheet = self._spread_sheet.worksheet('Menu')
        values = worksheet.col_values(1)

        # Get our shopping list and recipes list
        general_start = values.index('General')+1
        general_end = values.index('Recipes')
        general = values[general_start: general_end]
        general_quantities = worksheet.col_values(
            2)[general_start: general_end]

        recipes = values[values.index('Recipes')+1:]

        for ingredient in self._ingredients:
            if ingredient.name in general:
                ingredient.add(
                    general_quantities[general.index(ingredient.name)])

        # Collect all ingredients
        for recipe in recipes:

            # Get the information for each item in the recipe
            worksheet = self._spread_sheet.worksheet(recipe)
            items = worksheet.col_values(1)[2:]
            quantities = worksheet.col_values(2)[2:]
            units = worksheet.col_values(3)[2:]

            for ingredient in self._ingredients:
                if ingredient.name in items:
                    ingredient.add(quantities[items.index(ingredient.name)])

        # Build the list of things to buy
        worksheet = self._spread_sheet.worksheet('Ingredients')
        ingredient_names = worksheet.col_values(1)[1:]
        search_terms = worksheet.col_values(2)[1:]
        quantities = worksheet.col_values(3)[1:]

        shopping_list = []

        for index, ingredient in enumerate(self._ingredients):
            if ingredient.quantity > 0:
                sheet_index = ingredient_names.index(ingredient.name)
                shopping_item = Ingredient(search_terms[sheet_index])
                quantity = (ingredient.quantity //
                            int(quantities[sheet_index]))
                if (ingredient.quantity % int(quantities[sheet_index])) > 0:
                    quantity = quantity + 1
                shopping_item.add(quantity)
                shopping_list.append(shopping_item)

        for item in shopping_list:
            print('{} : {}'.format(item.name, item.quantity))

        return(shopping_list)

    def get_new_ingredients(self):

        new_ingredients = []

        # Refresh the ingredients list
        self.__get_ingredient_names()

        # Get the menu
        worksheet = self._spread_sheet.worksheet('Menu')
        values = worksheet.col_values(1)

        # Get our shopping list and recipes list
        general_start = values.index('General')+1
        general_end = values.index('Recipes')
        general = values[general_start: general_end]

        recipes = values[values.index('Recipes')+1:]

        for ingredient in general:
            if ingredient not in self._ingredient_names:
                new_ingredients.append(ingredient)

        # Collect all ingredients
        for recipe in recipes:

            # Get the information for each item in the recipe
            worksheet = self._spread_sheet.worksheet(recipe)
            items = worksheet.col_values(1)[2:]

            for ingredient in items:
                if ingredient not in self._ingredient_names:
                    new_ingredients.append(ingredient)

        # return a set to remove duplicates
        return(set(new_ingredients))
