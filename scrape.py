#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import requests
import re
from lxml import etree


def get_group_data_from_html(html, group_xpath, items_xpath):
    """ Input is:
        html - string with html text
        group_xpath - xpath to a list of items we want (rows)
         eg: '//div[@class="product"]'
        items_xpath - relative xpath inside group_xpath to get individual items (columns)
         eg: {'title': 'a/text()', 'url': 'a/@href'}
        returns a json with data.
         eg: [{'url': 'product_1', 'title': 'product 1'}, {'url': 'product_2', 'title': 'product 2'}]
    """
    tree = etree.HTML(html)
    tree_group = tree.xpath(group_xpath)
    result = []
    # Get rows (each element in the group xpath)
    for item in tree_group:
        result_item = {}
        # Get columns (each item in the items_xpath)
        for i in items_xpath:
            if item.xpath(items_xpath[i]):
                result_item[i] = item.xpath(items_xpath[i])[0].lstrip('=').strip('"')
            # By default, if xpath not found, returns empty string
            else:
                result_item[i] = ''
        result.append(result_item)
    return result


def scrape_products_sainsburys(url,
                               product_items_xpath=None,
                               product_items_group_xpath=None,
                               product_list_xpath=None,
                               product_list_group_xpath=None):
    """ Specific function to get data from sainsburys
        Given an URL will get data for all products listed.
        Returns result as dictionary
        eg: {"total": 15.1, "results": [{"size": "38.3kb",
                                         "description": "Apricots",
                                         "unit_price": 3.5,
                                         "title": "Sainsbury's Apricot Ripe & Ready x5"}]}
    """
    # Default values for xpaths
    if product_list_group_xpath is None:
        product_list_group_xpath = '//div[@class="productInfo"]'
    if product_list_xpath is None:
        product_list_xpath = {'url':'h3/a/@href'}
    if product_items_group_xpath is None:
        product_items_group_xpath = '/html'
    if product_items_xpath is None:
        product_items_xpath = {'title': 'body/div[@id="page"]/div/div[@id="content"]/div[2]/div[2]/div/div[1]/h1/text()',
                               'unit_price': 'body/div[@id="page"]/div/div[@id="content"]/div/div/div/div/div/div[@class="pricingAndTrolleyOptions"]/div/div/p[@class="pricePerUnit"]/text()[1]',
                               'description': '(body/div[@id="page"]/div[@id="main"]/div[@id="content"]/div[@class="section productContent"]/div[@class="mainProductInfoWrapper"]/div/div/div/productcontent/htmlcontent/h3[contains(text(), "Description")]/following::div[1]/descendant::*/text())[1]'
                              }
    # Get list of products
    html_list = requests.get(url).text
    list_product_urls = get_group_data_from_html(html_list, product_list_group_xpath, product_list_xpath)
    # Get each product data
    result = {'results':[], 'total':0.0}
    for product_url in list_product_urls:
        product_response = requests.get(product_url['url'])
        product_html = product_response.text
        product_size_kb = round(float(product_response.headers['content-length']) / 1024.0, 1)
        item_result = get_group_data_from_html(product_html, product_items_group_xpath, product_items_xpath)[0]
        # Set size
        item_result['size'] = "{}kb".format(product_size_kb)
        # Get price to float
        try:
            item_result['unit_price'] = float(re.findall(r"[-+]?\d*\.\d+|\d+", item_result['unit_price'])[0])
        except IndexError:
            item_result['unit_price'] = 0
        # update total
        result['total'] = round(result['total'] + item_result['unit_price'], 2)
        result['results'].append(item_result)
    return result


def main():
    """
    main
    """
    url = 'http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html'
    result = scrape_products_sainsburys(url)
    print json.dumps(result, indent=4, separators=(',', ': '))

if __name__ == '__main__':
    main()
