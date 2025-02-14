{
  "name": "Pos Order Reference Receipt (KM)",
  "summary": "Pos Order Reference Receipt.",
  "category": "Point Of Sale",
  "version": "16.0",
  "author":"Ahmed Elmahdi",
  "description":  """
      Pos Order Reference In Receipt
      Pos Order Number In Receipt
      Work Offline & Online
    """,
  "depends":  [
    'point_of_sale', 'pos_restaurant', 'base'
  ],
  "assets": {
	  'point_of_sale.assets': [
      'am_pos_order_ref/static/src/js/main.js',
      'am_pos_order_ref/static/src/xml/pos.xml'
		],
  },
  "images": ['static/description/image.png'],
  "application": True,
  "installable": True,
  "auto_install": False,
  "pre_init_hook": "pre_init_check",
  'license': 'LGPL-3',
  'live_test_url':'https://youtu.be/i2Nm1DBysPg',
  'price': 12,
  'currency': 'EUR',
}
