from sheet_reader import SheetReader
import web_automater

# Generate a .txt file with complete list
sheet_reader = SheetReader()

new_items = sheet_reader.get_new_ingredients()
if len(new_items) > 0:
    with open('new_ingredients.txt', 'w') as f:
        for item in new_items:
            f.write("{}\n".format(item))

    print('Please add new ingredients listed in "new_ingredients.txt"')
    quit()

shopping_list = sheet_reader.get_shopping_list()

web_automater.build_cart(shopping_list)

# For a breakpoint
i = 1
