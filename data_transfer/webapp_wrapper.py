# idea is to return user save data as a json,
# and to potentially build the internal entity classes
# based on the user's JSON

class PortfolioWebWrapper:
    """
    Manager class for Portfolio, that interfaces with the web frontend
    """

    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.categories = []  # keys: color, title, symbols(list)
        self.display_symbols = []

    def get_symbols(self):
        return self.portfolio.symbols

    def remove_symbol(self, symbol):
        """
        Removes a symbol from the portfolio.
        Will remove it from any categories it's in
        """
        if symbol in self.portfolio.symbols:
            self.portfolio.symbols.remove(symbol)

        for category in self.categories:
            if symbol in category['symbols']:
                category['symbols'].remove(symbol)

    def remove_symbol_from_category(self, symbol, category):
        for c in self.categories:
            if c['title'] == category:
                if symbol in c['symbols']:
                    c['symbols'].remove(symbol)

    def get_categories(self):
        return self.categories

    def get_category_names(self):
        return [category['title'] for category in self.categories]

    def add_symbol(self, symbol):
        self.portfolio.symbols.append(symbol)

    def add_category(self, cat_data):
        """
        Adds a category. If the category title already exists, modifies existing category
        :param cat_data: data containing keys title, symbols, color(optional)
        """
        # Remove duplicate symbols
        tmp_symbols = []
        for s in cat_data['symbols']:
            if s not in tmp_symbols:
                tmp_symbols.append(s)
        cat_data['symbols'] = tmp_symbols

        # Update existing category if duplicate title
        for category in self.categories:
            if category['title'] == cat_data['title']:
                category['symbols'] += [s for s in cat_data['symbols'] if s not in category['symbols']]
                if 'color' in cat_data and cat_data['color'] is not None:
                    category['color'] = cat_data['color']
                return

        # Add new category
        if cat_data['color'] is None:
            cat_data['color'] = '#555555'
        self.categories.append(cat_data)

    def refresh_display_symbols(self):
        """
        Refreshes display symbols. For now, puts all categories at the top and symbols
        at the bottom.

        :return:
        """
        # Remove button on category removes from category, remove button on symbol removes the symbol
        self.display_symbols = self.get_categories() + self.get_symbols()

    def to_json(self):
        """Delivers a JSON representation of the portfolio"""
        self.refresh_display_symbols()
        return {'symbols': self.display_symbols}


def user_data_to_json(user):
    """
    Returns all the data required for the user profile as a json
    :param user: User to jsonify
    :return: JSON representation of the user
    """
    return {'portfolio': user.current_portfolio.to_json()}
