# idea is to return user save data as a json,
# and to potentially build the internal entity classes
# based on the user's JSON

def portfolio_to_json(portfolio):
    return {'symbols': portfolio.symbols}


def user_data_to_json(user):
    """
    Returns all the data required for the user profile as a json
    :param user: User to jsonify
    :return: JSON representation of the user
    """
    return {'portfolio': portfolio_to_json(user.current_portfolio)}
