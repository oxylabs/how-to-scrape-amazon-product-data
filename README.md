[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

[![](https://dcbadge.vercel.app/api/server/eWsVUJrnG5)](https://discord.gg/GbxmdGhZjq)

# Scraping Amazon Product Data With Python

You can find an extended version of this guide on our [blog](https://oxylabs.io/blog/scrape-amazon-product-data).

This guide uses Python to scrape the following data points from Amazon:

- Product name
- Product rating
- Product price
- Product images
- Product description

## Contents

- [Setting up](#setting-up)
  + [Installing packages](#installing-packages)
- [Scraping product data](#scraping-product-data)
  + [1. Sending a GET request with custom headers](#1.-sending-a-get-request-with-custom-headers)
  + [2. Locating and scraping product name](#2.-locating-and-scraping-product-name)
  + [3. Locating and scraping product rating](#3.-locating-and-scraping-product-rating)
  + [4. Locating and scraping product price](#4.-locating-and-scraping-product-price)
  + [5. Locating and scraping product image](#5.-locating-and-scraping-product-image)
  + [6. Locating and scraping product description](#6.-locating-and-scraping-product-description)
  + [7. Handling product listing](#7.-handling-product-listing)
  + [8. Exporting scraped product data to a CSV file](#8.-exporting-scraped-product-data-to-a-CSV-file)
- [Reviewing the final script](#reviewing-the-final-script)
- [An easier solution to extract Amazon data](#an-easier-solution-to-extract-Amazon-data)
  + [Scraping products from search results](#scraping-products-from-search-results)
  + [Extracting product details](#extracting-product-details)
  + [Scraping products by ASIN](#scraping-products-by-ASIN)

## Setting up

Create a folder to save your code files. Also, creating a virtual environment is generally a good practice.

The following commands work on macOS and Linux. The commands will create a virtual environment and activate it:

```
python3 -m venv .env
source .env/bin/activate
```

If you are on Windows, these commands will vary a little:

```
python -m venv .env
.env\scripts\activate
```
### Installing packages

```
python3 -m pip install requests beautifulsoup4 lxml pandas
```

For Windows, use Python instead of Python3:

```
python -m pip install requests beautifulsoup4 lxml pandas
```

To try the Requests library, create a new file with the name amazon.py and enter the following:

```
import requests
url = 'https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/dp/B098FKXT8L'

response = requests.get(url)

print(response.text)
```

Save the file and run it from the terminal:

```
python3 amazon.py
```

In most cases, you cannot view the desired HTML. Amazon will block this request, and you will see the following text in the response:

```
To discuss automated access to Amazon data, please contact api-services-support@amazon.com.
```

If you print the `response.status_code`, you will see that instead of getting 200, which means success, you may get 503, which means an error.

Amazon knows this request was not using a browser and thus blocks it.

Many websites employ this practice. Amazon will block your requests and return an error code beginning with 500 or sometimes even 400.

The solution is simple in most cases. You can send the headers along with your request that a browser would.

Sometimes, sending only the `user-agent` is enough. At other times, you may need to send more headers. A good example is sending the `accept-language` header.

To identify the user-agent sent by your browser, press F12 and open the Network tab. Reload the page. Select the first request and examine Request Headers.

![](https://raw.githubusercontent.com/oxylabs/how-to-scrape-amazon-product-data/main/images/Amazon%20(1).jpg?token=GHSAT0AAAAAACW62VSTLRWZD5SJMWB7ZKI6ZWYLXUA)

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeQh5LeNNTxEWk_ZmK9sZm069VX1icx_Amazon-1-.jpg%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

You can copy this user-agent and create a dictionary for the headers. 

The following shows a dictionary with the `user-agent` and `accept-language` headers:

```
custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}
```

You can send this dictionary to the optional parameter of the `get` method as follows:

```
response = requests.get(url, headers= custom_headers)
```

Executing the code with these changes may show the expected HTML with the product details.

You will not need Javascript rendering if you send as many headers as possible. If you need rendering, you will have to use tools like Playwright or Selenium. If the `User-Agent` and `Accept-Language` strings still bring you the `503` error, you can try to use the following headers:

```
custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}
```

It’s also a good idea to rotate different `User-Agent` strings and try your requests again to overcome the `503` error.

## Scraping product data

When web scraping Amazon products, typically, you would work with two categories of pages — the category page and the product details page.

For example, open [this](https://www.amazon.com/b?node=12097479011) or search for Over-Ear Headphones on Amazon. The page that shows the search results is the category page.

The category page displays the product title, product image, product rating, product price, and, most importantly, the product URLs page. If you want more details, such as product descriptions, you will get them only from the product details page.

Let's examine the structure of the product details page.

Open a product URL, such as [this](https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/dp/B098FKXT8L), in Chrome or any other modern browser, right-click the product title, and select Inspect. You will see that the HTML markup of the product title is highlighted.

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeQx5LeNNTxEWl_ZmK9xZm069VX1ic0_Amazon-2-.jpg%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

You will see that it is a span tag with its id attribute set to `productTitle`.

Similarly, if you right-click the price and select Inspect, you will see the HTML markup of the price.

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeRR5LeNNTxEWm_ZmK905m069VX1ic4_Amazon-3-.jpg%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

You can see that the dollar component of the price is in a span tag with the class `a-price-whole`, and the cents component is in another span tag with the class set to `a-price-fraction`.

Similarly, you can locate the rating, image, and description.

### 1. Sending a GET request with custom headers

```
from bs4 import BeautifulSoup

response = requests.get(url, headers=custom_headers)
soup = BeautifulSoup(response.text, 'lxml')
```

This guide uses CSS selectors. You can now use the `Soup` object to query for specific information.

### 2. Locating and scraping product name

The product name or title is located in a `span` element with its id `productTitle`. It's easy to select elements using a unique ID.

```
title_element = soup.select_one('#productTitle')
```

Send the CSS selector to the `select_one` method, which returns an element instance. You can extract information from the text using the `text` attribute.

```
title = title_element.text
```

Upon printing, you will see that there are few white spaces. To fix that, add `.strip()` function call as follows:

```
title = title_element.text.strip()
```

### 3. Locating and scraping product rating

Create a selector for rating:

```
#acrPopover
```

The following statement can select the element that contains the rating:

```
rating_element = soup.select_one('#acrPopover')
```

Note that the rating value is actually in the title attribute:

```
rating_text = rating_element.attrs.get('title')
print(rating_text)
# prints '4.6 out of 5 stars'
```

Lastly, use the `replace` method to get the number:

```
rating = rating_text.replace('out of 5 stars','')
```

### 4. Locating and scraping product price

The product price is located in two places: below the product title and on the Buy Now box. You can use either of these tags.

Create a CSS selector for the price:

```
span.a-offscreen
```

The CSS selector can be passed to the `select_one` method of BeautifulSoup as follows:

```
price_element = soup.select_one('span.a-offscreen')
```

You can now print the price:

```
print(price_element.text)
```

### 5. Locating and scraping product image

Let's scrape the default image. This image has the CSS selector as `#landingImage`. Write the following to get the image URL from the `src` attribute:

```
image_element = soup.select_one('#landingImage')
image = image_element.attrs.get('src')
```

### 6. Locating and scraping product description

The methodology remains the same — create a CSS selector and use the `select_one` method.

```
#productDescription
```

You can extract the element as follows:

```
description_element = soup.select_one('#productDescription').text.strip()
print(description_element)
```

### 7. Handling product listing

To reach the product information, begin with product listing or category pages.

For example, [here](https://www.amazon.com/b?node=12097479011) is the category page for over-ear headphones.

Notice that all the products are contained in a `div` with the special attribute `[data-asin]`. In the `div`, all the product links are in an `h2` tag.

The CSS Selector is as follows:

```
[data-asin] h2 a
```

You can read the `href` attribute of this selector and run a loop. However, note that the links will be relative. You would need to use the `urljoin` method to parse these links.

```
from urllib.parse import urljoin

def parse_listing(listing_url):
    global visited_urls
    response = requests.get(listing_url, headers=custom_headers)
    print(response.status_code)
    soup_search = BeautifulSoup(response.text, "lxml")
    link_elements = soup_search.select("[data-asin] h2 a")
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scraping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)
```

#### Handling pagination

The link to the next page contains the text "Next". Look for this link using the contains operator of CSS as follows:

```
    next_page_el = soup_search.select_one('a.s-pagination-next')
    if next_page_el:
        next_page_url = next_page_el.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)
        print(f'Scraping next page: {next_page_url}', flush=True)
        page_data += parse_listing(next_page_url)

    return page_data
```

### 8. Exporting scraped product data to a CSV file

The scraped data is being returned as a dictionary. It is intentional. 

You can create a list that contains all the scraped products:

```
def main():
    data = []
    search_url = "https://www.amazon.com/s?k=bose&rh=n%3A12097479011&ref=nb_sb_noss"
    data = parse_listing(search_url)
```

This `page_data` can then be used to create a Pandas `DataFrame` object:

```
    df = pd.DataFrame(data)
    df.to_csv("headphones.csv", index=False)
```

## Reviewing the final script

Putting together everything, here is the final script:

```
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import pandas as pd

custom_headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    'Accept-Language': 'da, en-gb, en',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
}

visited_urls = set()

def get_product_info(url):
    response = requests.get(url, headers=custom_headers)
    if response.status_code != 200:
        print(f"Error in getting webpage: {url}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    title_element = soup.select_one("#productTitle")
    title = title_element.text.strip() if title_element else None

    price_element = soup.select_one('span.a-offscreen')
    price = price_element.text if price_element else None

    rating_element = soup.select_one("#acrPopover")
    rating_text = rating_element.attrs.get("title") if rating_element else None
    rating = rating_text.replace("out of 5 stars", "") if rating_text else None

    image_element = soup.select_one("#landingImage")
    image = image_element.attrs.get("src") if image_element else None

    description_element = soup.select_one("#productDescription")
    description = description_element.text.strip() if description_element else None

    return {
        "title": title,
        "price": price,
        "rating": rating,
        "image": image,
        "description": description,
        "url": url
    }


def parse_listing(listing_url):
    global visited_urls
    response = requests.get(listing_url, headers=custom_headers)
    print(response.status_code)
    soup_search = BeautifulSoup(response.text, "lxml")
    link_elements = soup_search.select("[data-asin] h2 a")
    page_data = []

    for link in link_elements:
        full_url = urljoin(listing_url, link.attrs.get("href"))
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scraping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)

    next_page_el = soup_search.select_one('a.s-pagination-next')
    if next_page_el:
        next_page_url = next_page_el.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)
        print(f'Scraping next page: {next_page_url}', flush=True)
        page_data += parse_listing(next_page_url)

    return page_data


def main():
    data = []
    search_url = "https://www.amazon.com/s?k=bose&rh=n%3A12097479011&ref=nb_sb_noss"
    data = parse_listing(search_url)
    df = pd.DataFrame(data)
    df.to_csv("headphones.csv", orient='records')


if __name__ == '__main__':
    main()
```

## An easier solution to extract Amazon data

You can simplify the whole process with Oxylabs [Amazon Scraper](https://oxylabs.io/products/scraper-api/ecommerce/amazon) (a free trial is available).

### Scraping products from search results

Extract product data with the following code:

```
import requests
from pprint import pprint

# Structure payload.
payload = {
    'source': 'amazon_search',
    'query': 'bose',  # Search for "bose"
    'start_page': 1,
    'pages': 10,
    'parse': True,
    'context': [
        {'key': 'category_id', 'value': 12097479011}  # category id for headphones
    ],
}

# Get response
response = requests.request(
    'POST',
    'https://realtime.oxylabs.io/v1/queries',
    auth=('USERNAME', 'PASSWORD'),
    json=payload,
)

# Print prettified response to stdout.
pprint(response.json())
```

Notice how it requests 10 pages beginning with the page 1. Also, we limit the search to category ID 12097479011, which is Amazon's category ID for headphones. You’ll get the data in JSON format:

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeRh5LeNNTxEWn_0dcb25ef-f532-49c2-8ef5-5960d9773bd3_amazon_product_search.png%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

### Extracting product details

You only need the product URL, irrespective of the country in the Amazon store. The only change in code is the payload. 

The following payload extracts details, such as name, price, stock availability, description, and more, for the Bose QC 45:

```
payload = {
    'source': 'amazon',
    'url': 'https://www.amazon.com/dp/B098FKXT8L',
    'parse': True
}
```

The output:

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeRx5LeNNTxEWo_fddcfa94-6d5c-4a61-b9ff-7035108bf36d_amazon_product_details.png%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

### Scraping products by ASIN

Another way to get data is by the ASIN of a product. You need to modify the payload:

```
payload = {
    'source': 'amazon_product',
    'domain': 'co.uk',
    'query': 'B098FKXT8L',
    'parse': True,
    'context': [
        {'key': 'autoselect_variant', 'value': True}
    ]
}
```

Note the optional parameter `domain`. Use this parameter to get Amazon data from any domain, such as amazon.co.uk.
