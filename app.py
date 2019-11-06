from flask import Flask

from views.alerts import alert_blueprint
from views.items import item_blueprint

# alert = Alert("35dd94187e8c4d3cb4477c58756224b5", 2000)
# alert.save_to_mongo()

# url = "https://www.johnlewis.com/2018-apple-ipad-pro-12-9-inch-a12x-bionic-ios-wi-fi-cellular-512gb/space-grey/p3834614"
# query = {"class": "price price--large"}
#
# ipad = Item(url, tag_name="p", query=query)
# ipad.save_to_mongo()
#
# item_loaded=Item.all()
# print(item_loaded)
# print(item_loaded[0].load_price())

app = Flask(__name__)

app.register_blueprint(item_blueprint, url_prefix='/items')
app.register_blueprint(alert_blueprint, url_prefix='/alerts')

if __name__ == '__main__':
    app.run(debug=True)
