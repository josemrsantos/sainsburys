from nose.tools import with_setup
import scrape
from mock import patch


class mockResponse(object):
    def __init__(self, text, size=0):
        self.text = text
        self.headers = {'content-length': size}


class Test(object):

    def __init__(self):
        self.html_products_list = """
        <html>
        <head></head>
         <body>
            <div class="product"><a href=="product_1">product 1</a></div>
            <div class="product"><a href=="product_2">product 2</a></div>
            <div class="product"><a href=="product_3">product 3</a></div>
         </body>
        </html>
        """
        self.html_products_list_2 = """
        <html>
        <head></head>
         <body>
            <div class="products">
             <div class="productInfo"><a href=="product_1">product 1</a></div>
             <div class="productInfo"><a href=="product_2">product 2</a></div>
            </div>
         </body>
        </html>
        """
        self.html_product_1 = """
        <html>
        <head></head>
         <body>
            <div id="price">1.0</div>
            <div id="name">name_1</div>
            <div id="description">description_1</div>
         </body>
        </html>
        """
        self.html_product_2 = """
        <html>
        <head></head>
         <body>
            <div id="price">2.0</div>
            <div id="name">name_2</div>
            <div id="description">description_2</div>
         </body>
        </html>
        """
        self.html_products_list_2_no_price = """
        <html>
        <head></head>
         <body>
            <div class="products">
             <div class="productInfo"><a href=="product_1_no_price">product 1</a></div>
             <div class="productInfo"><a href=="product_2_no_price">product 2</a></div>
            </div>
         </body>
        </html>
        """
        self.html_product_1_no_price = """
        <html>
        <head></head>
         <body>
            <div id="name">name_1</div>
            <div id="description">description_1</div>
         </body>
        </html>
        """
        self.html_product_2_no_price = """
        <html>
        <head></head>
         <body>
            <div id="name">name_2</div>
            <div id="description">description_2</div>
         </body>
        </html>
        """

    def mock_get_function(self, url):
        print url
        if url == 'initial':
            return mockResponse(self.html_products_list_2)
        elif url == 'product_1':
            return mockResponse(self.html_product_1)
        elif url == 'product_2':
            return mockResponse(self.html_product_2)
        elif url == 'initial_no_price':
            return mockResponse(self.html_products_list_2_no_price)
        elif url == 'product_1_no_price':
            return mockResponse(self.html_product_1_no_price)
        elif url == 'product_2_no_price':
            return mockResponse(self.html_product_2_no_price)
        return None

    def test_get_data_from_html_list_products(self):
        html = self.html_products_list
        group_xpath = '//div[@class="product"]'
        items_xpath = {'title': 'a/text()', 'url': 'a/@href'}
        result = scrape.get_group_data_from_html(html, group_xpath, items_xpath)
        print result
        assert(len(result) == 3)
        assert({'title':'product 1', 'url': 'product_1'} in result)
        assert({'title':'product 2', 'url': 'product_2'} in result)
        assert({'title':'product 3', 'url': 'product_3'} in result)

    @patch('requests.get')
    def test_get_products_data(self, mock_get):
        mock_get.side_effect = self.mock_get_function
        result = scrape.scrape_products_sainsburys('initial',
                                                    product_items_xpath={'title':'body/div[@id="name"]/text()',
                                                                         'unit_price':'body/div[@id="price"]/text()'
                                                                        },
                                                    product_items_group_xpath='/html',
                                                    product_list_xpath={'url':'a/@href'},
                                                    product_list_group_xpath='//div[@class="products"]/div')
        print result
        assert result == {'total': 3.0,
                          'results': [{'size': '0.0kb', 'unit_price': 1.0, 'title': 'name_1'},
                                      {'size': '0.0kb', 'unit_price': 2.0, 'title': 'name_2'}]}

    @patch('requests.get')
    def test_sum_from_empty_is_zero(self, mock_get):
        mock_get.side_effect = self.mock_get_function
        result = scrape.scrape_products_sainsburys('initial_no_price',
                                                    product_items_xpath={'title':'body/div[@id="name"]/text()',
                                                                         'unit_price':'body/div[@id="price"]/text()'
                                                                        },
                                                    product_items_group_xpath='/html',
                                                    product_list_xpath={'url':'a/@href'},
                                                    product_list_group_xpath='//div[@class="products"]/div')
        print result
        assert result['total'] == 0
