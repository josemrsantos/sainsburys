## Installation 

### Prerequisites

* python 2.7
* nosetests (for testing)
* lxml
* requests
* mock


### Run

python scrape.py
(will output the result in JSON format)

### Run tests

nosetests

If nosetests is not installed :
* rm -rf ve_folder
* mkdir ve_folder
* virtualenv ve_folder/
* source ve_folder/bin/activate
* pip install -r requirements.txt
* nosetests


## "User story":
`
build a console application that scrapes the Sainsbury’s grocery site - Ripe Fruits page and returns a JSON array of
all the products on the page.
You need to follow each link and get the size (in kb) of the linked HTML (no assets) and the description to display in
the JSON

Each element in the JSON results array should contain ‘title’, ‘unit_price’, ‘size’ and ‘description’ keys
corresponding to items in the table.

Additionally, there should be a total field which is a sum of all unit prices on the page.

    The link to use is: http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html

Example JSON:
{
 "results":[
 {
 "title":"Sainsbury's Avocado, Ripe & Ready x2",
 "size": "90.6kb",
 "unit_price": 1.80,
 "description": "Great to eat now - refrigerate at home 1 of 5 a day 1 avocado counts as 1 of your 5..."
 },
 {
 "title":"Sainsbury's Avocado, Ripe & Ready x4",
 "size": "87kb",
 "unit_price": 2.00,
 "description": "Great to eat now - refrigerate at home 1 of 5 a day 1 avocado counts as 1 of your 5..."
 }
 ],
 "total": 3.80
}

`