[![Amazon_scraper](https://github.com/oxylabs/amazon-scraper/blob/main/amazon-scraper-github-banner.png)](https://oxylabs.io/products/web-api/scrape?utm_source=github&utm_medium=referral&utm_content=web_api_waitinglist&groupid=877) 

<a href="https://oxylabs.io"><img src="https://img.shields.io/badge/🚀_Get_Started-FF6B35?style=for-the-badge" alt="Get started"></a>
<a href="https://developers.oxylabs.io"><img src="https://img.shields.io/badge/📚_Documentation-4A90E2?style=for-the-badge" alt="Documentation"></a>
<a href="https://dashboard.oxylabs.io"><img src="https://img.shields.io/badge/📊_Dashboard-2EA44F?style=for-the-badge" alt="Dashboard"></a>
<a href="https://discord.gg/YOUR-INVITE"><img src="https://img.shields.io/badge/💬_Discord-5865F2?style=for-the-badge" alt="Discord"></a>
<a href="https://www.youtube.com/@oxylabs"><img src="https://img.shields.io/badge/▶️_YouTube-FF0000?style=for-the-badge" alt="YouTube"></a>

# Amazon product data scraper

This repository is a detailed guide & tool for developers and market researchers building a free Amazon product data scraper from scratch in Python. This project uses `requests` and `BeautifulSoup` to pull structured data straight from the page and turns it into a clean Amazon product dataset you can filter, analyze, and feed into your own tools as competitive intelligence or use a brand info source for sentiment analysis type tasks.

There are three ways to use it:

- **Follow the walkthrough** below and write the scraper yourself, step by step.
- **Run the ready-to-use template** – [`amazon_scraper.py`](amazon_scraper.py) explained and included in this repo. Point it at any Amazon search or category URL and get a CSV of product data back.
- **Use [Oxylabs Web API](#an-easier-solution-to-extract-amazon-data)** a managed service that handles request management, parsing, and returns real-time structured data from Amazon at scale.

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
  + [1. Sending a GET request with custom headers](#1-sending-a-get-request-with-custom-headers)
  + [2. Locating and scraping product name](#2-locating-and-scraping-product-name)
  + [3. Locating and scraping product rating](#3-locating-and-scraping-product-rating)
  + [4. Locating and scraping product price](#4-locating-and-scraping-product-price)
  + [5. Locating and scraping product image](#5-locating-and-scraping-product-image)
  + [6. Locating and scraping product description](#6-locating-and-scraping-product-description)
  + [7. Handling product listing](#7-handling-product-listing)
  + [8. Exporting scraped product data to a CSV file](#8-exporting-scraped-product-data-to-a-csv-file)
- [Reviewing the final script](#reviewing-the-final-script)
  + [Ready-to-use template script](#ready-to-use-template-script)
- [An easier solution to extract Amazon data](#an-easier-solution-to-extract-amazon-data)
  + [Scraping products from search results](#scraping-products-from-search-results)
  + [Extracting product details](#extracting-product-details)
  + [Scraping products by ASIN](#scraping-products-by-asin)
- [Practical use cases](#practical-use-cases)
- [FAQ](#faq)
- [Learn more](#learn-more)

## Setting up

Create a folder to save your code files. Also, creating a virtual environment is generally a good practice.

The following commands work on macOS and Linux. The commands will create a virtual environment and activate it:

```bash
python3 -m venv .env
source .env/bin/activate
```

If you are on Windows, these commands will vary a little:

```bash
python -m venv .env
.env\scripts\activate
```
### Installing packages

```bash
python3 -m pip install requests beautifulsoup4 lxml pandas
```

For Windows, use Python instead of Python3:

```bash
python -m pip install requests beautifulsoup4 lxml pandas
```

To try the Requests library, create a new file with the name amazon.py and enter the following:

```python
import requests
url = 'https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/dp/B098FKXT8L'

response = requests.get(url)

print(response.text)
```

Save the file and run it from the terminal:

```bash
python3 amazon.py
```

In most cases, you cannot view the HTML. Amazon will block this request and you will see the following text in the response:

```
To discuss automated access to Amazon data, please contact api-services-support@amazon.com.
```

If you print the `response.status_code`, you will see that instead of getting 200 (success), you may get 503 (error). Amazon knows this request was not using a browser and thus blocks it.

Many websites employ this practice. Amazon will block your requests and return an error code beginning with 500 or sometimes even 400.

The solution is to send HTTP headers along with your request just like an actual browser. Sometimes, sending only the `user-agent` is enough, but you may need to send more headers. A good example is sending the `accept-language` header.

To identify the user-agent sent by your browser, press `F12` and open the Network tab. Reload the page. Select the first request and examine `Request Headers`.

![](https://raw.githubusercontent.com/oxylabs/how-to-scrape-amazon-product-data/main/images/Amazon%20(1).jpg)

You can copy this user-agent and create a dictionary for the headers. The following shows a dictionary with the `user-agent` and `accept-language` headers:

```python
custom_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'accept-language': 'en-GB,en;q=0.9',
}
```

You can send this dictionary to the optional parameter of the `get` method as follows:

```python
response = requests.get(url, headers= custom_headers)
```

Executing the code with these changes may show the expected HTML with the product details.

You will not need Javascript rendering if you send as many headers as possible. If you need rendering, you will have to use tools like Playwright or Selenium. If the `User-Agent` and `Accept-Language` strings still bring you the `503` error, you can try to use the following headers:

```python
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

When scraping Amazon products, you will work with two types of pages where a product belongs – the category page and the product details page.

For example, open [this](https://www.amazon.com/b?node=12097479011) or search for Over-Ear Headphones on Amazon. The page that shows the search results is the category page.

The category page displays the product title, product image, product rating, price, category information, and the product URL among various product metadata. If you want more details, such as a brief product description, you will get them only from the product details page. The same category-page structure works for any other category too – electronics, cell phones, pet supplies, Kindle Store, digital music, or DVDs – just swap the node ID in the URL.

To examine the structure of the product details page, open a product URL, such as [this](https://www.amazon.com/Bose-QuietComfort-45-Bluetooth-Canceling-Headphones/dp/B098FKXT8L), in Chrome or any other modern browser, right-click the product title, and select Inspect. You will see that the HTML markup of the product title is highlighted.

![](https://raw.githubusercontent.com/oxylabs/how-to-scrape-amazon-product-data/main/images/Amazon%20(2).jpg)

You will see that it is a span tag with its id attribute set to `productTitle`.

Similarly, if you right-click the price and select Inspect, you will see the HTML markup of the price.

![](https://raw.githubusercontent.com/oxylabs/how-to-scrape-amazon-product-data/main/images/Amazon%20(3).jpg)

You can see that the dollar component of the price is in a span tag with the class `a-price-whole`, and the cents component is in another span tag with the class set to `a-price-fraction`. Similarly, you can locate other product metadata: the rating, image, and description.

### 1. Sending a GET request with custom headers

```python
from bs4 import BeautifulSoup

response = requests.get(url, headers=custom_headers)
soup = BeautifulSoup(response.text, 'lxml')
```

This guide uses CSS selectors. You can now use the `Soup` object to query for specific information.

### 2. Locating and scraping product name

The product name or title is located in a `span` element with its id `productTitle`. It's easy to select elements using a unique ID.

```python
title_element = soup.select_one('#productTitle')
```

Send the CSS selector to the `select_one` method, which returns an element instance. You can extract information from the text using the `text` attribute.

```python
title = title_element.text
```

Upon printing, you will see that there are few white spaces. To fix that, add `.strip()` function call as follows:

```python
title = title_element.text.strip()
```

### 3. Locating and scraping product rating

Create a selector for rating:

```css
#acrPopover
```

The following statement can select the element that contains the rating:

```python
rating_element = soup.select_one('#acrPopover')
```

Note that the rating value is actually in the title attribute:

```python
rating_text = rating_element.attrs.get('title')
print(rating_text)
# prints '4.6 out of 5 stars'
```

Lastly, use the `replace` method to get the number:

```python
rating = rating_text.replace('out of 5 stars','')
```

### 4. Locating and scraping product price

The product price is located in two places: below the product title and on the Buy Now box. You can use either of these tags.

Create a CSS selector for the price:

```css
span.a-offscreen
```

The CSS selector can be passed to the `select_one` method of BeautifulSoup as follows:

```pyhton
price_element = soup.select_one('span.a-offscreen')
```

You can now print the price:

```python
print(price_element.text)
```

### 5. Locating and scraping product image

Let's scrape the default image. This image has the CSS selector as `#landingImage`. Write the following to get the image URL from the `src` attribute:

```python
image_element = soup.select_one('#landingImage')
image = image_element.attrs.get('src')
```

### 6. Locating and scraping product description

The methodology remains the same – create a CSS selector and use the `select_one` method.

```css
#productDescription
```

You can extract the element as follows:

```python
description_element = soup.select_one('#productDescription').text.strip()
print(description_element)
```

### 7. Handling product listing

To reach the product information, begin with product listing or category pages.

For example, [here](https://www.amazon.com/b?node=12097479011) is the category page for over-ear headphones.

Amazon marks every real search result with `data-component-type="s-search-result"` and a `data-asin` attribute carrying that product's ASIN. Reading the ASIN directly off the card is more reliable than following a title link, since Amazon frequently renames the inner markup around that link.

The CSS selector is as follows:

```css
div[data-component-type="s-search-result"][data-asin]
```

You can read the `data-asin` attribute and build each product's URL from it directly, then run a loop:

```python
from urllib.parse import urljoin

def parse_listing(listing_url):
    global visited_urls
    response = requests.get(listing_url, headers=custom_headers)
    print(response.status_code)
    soup_search = BeautifulSoup(response.text, "lxml")
    result_cards = soup_search.select('div[data-component-type="s-search-result"][data-asin]')
    page_data = []

    for card in result_cards:
        asin = card.get("data-asin")
        full_url = urljoin(listing_url, f"/dp/{asin}")
        if full_url not in visited_urls:
            visited_urls.add(full_url)
            print(f"Scraping product from {full_url[:100]}", flush=True)
            product_info = get_product_info(full_url)
            if product_info:
                page_data.append(product_info)
```

The `visited_urls` set is what removes duplicates here – it tracks every product URL already scraped, so a listing that reappears across paginated search results doesn't get processed twice.

#### Handling pagination

The link to the next page contains the text "Next". Look for this link using the contains operator of CSS as follows:

```python
    next_page_el = soup_search.select_one('a.s-pagination-next')
    if next_page_el:
        next_page_url = next_page_el.attrs.get('href')
        next_page_url = urljoin(listing_url, next_page_url)
        print(f'Scraping next page: {next_page_url}', flush=True)
        page_data += parse_listing(next_page_url)

    return page_data
```

### 8. Exporting scraped product data to a CSV file

The scraped data is being returned as Python dictionary objects. It is intentional. 

You can create a list that contains all the scraped products:

```python
def main():
    data = []
    search_url = "https://www.amazon.com/s?k=bose&rh=n%3A12097479011&ref=nb_sb_noss"
    data = parse_listing(search_url)
```

This `page_data` can then be used to create a Pandas `DataFrame` object, the easiest way to turn raw scraped listings into a proper Amazon dataset sample – sort it, filter it, or merge it with other sources before exporting:

```python
    df = pd.DataFrame(data)
    df.to_csv("headphones.csv", index=False)
```

If you're running this across many categories or many runs, consider converting the CSV output to a binary format like Parquet afterward – it loads faster and takes up less space once you're past a few hundred thousand rows. Otherwise, parsing into a strict JSON output is recommended for more flexible workflows.

## Reviewing the final script

Putting together everything, here is the final script:

```python
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
    result_cards = soup_search.select('div[data-component-type="s-search-result"][data-asin]')
    page_data = []

    for card in result_cards:
        asin = card.get("data-asin")
        full_url = urljoin(listing_url, f"/dp/{asin}")
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
    df.to_csv("headphones.csv", index=False)


if __name__ == '__main__':
    main()
```

### Ready-to-use template script

This simple script, cleaned up with command-line arguments and pagination limits, is included in this repo as [`amazon_scraper.py`](amazon_scraper.py) – download it and adjust it to your own needs. It's a quick way to pull a product summary for every listing on a search or category page, without writing any of the scraping logic yourself.

```bash
python3 -m pip install -r requirements.txt
python3 amazon_scraper.py "https://www.amazon.com/s?k=bose&rh=n%3A12097479011&ref=nb_sb_noss" --max-pages 2 --output products.csv
```

It accepts any Amazon search or category URL, follows pagination up to `--max-pages` (default 1), and writes the same product data columns – `title`, `price`, `rating`, `image`, `description`, `url` – to the CSV file you name with `--output` (default `amazon_products.csv`).

## An easier solution to extract Amazon data

You can simplify the whole process with [Oxylabs Web API](https://oxylabs.io/products/web-api/scrape/ecommerce/amazon) (try it for free with $5 welcome credit). Each Amazon target has its own endpoint under `https://webapi.oxylabs.io/v1/scrape/amazon`, authenticated with a Bearer API key instead of the request headers and pagination logic above.

| Endpoint | Description |
| --- | --- |
| `/v1/scrape/amazon` | Submit any Amazon URL you like |
| `/v1/scrape/amazon/search` | Search results for a search term of your choice |
| `/v1/scrape/amazon/product` | Product page of an ASIN of your choice |
| `/v1/scrape/amazon/pricing` | List of offers available for an ASIN of your choice |
| `/v1/scrape/amazon/bestsellers` | Best seller items in a category of your choice, including each item's sales rank |
| `/v1/scrape/amazon/sellers` | Seller information of a seller of your choice |

### Scraping products from search results

Extract comprehensive product data with the following code:

```python
import os
import requests
from pprint import pprint

# Structure payload.
payload = {
    'query': 'bose',  # Search for "bose"
    'category_id': '12097479011',  # category id for headphones
    'start_page': 1,
    'pages': 10,
    'output': ['json'],
}

# Get response
response = requests.post(
    'https://webapi.oxylabs.io/v1/scrape/amazon/search',
    headers={'Authorization': f"Bearer {os.environ['OXYLABS_WEB_API_KEY']}"},
    json=payload,
)

# Print prettified response to stdout.
pprint(response.json())
```

Notice how it requests 10 pages beginning with the page 1. Also, we limit the search to category ID 12097479011, which is Amazon's category ID for headphones. The `output: ['json']` parameter asks for a strict JSON response, so you get the same predictable structure on every call.

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeRh5LeNNTxEWn_0dcb25ef-f532-49c2-8ef5-5960d9773bd3_amazon_product_search.png%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

### Extracting product details

You only need the product URL, regardless of the country where the Amazon store is located. The only code change is the payload.

The following payload extracts details, such as name, price, stock availability, description, and more, for the Bose QC 45:

```python
payload = {
    'url': 'https://www.amazon.com/dp/B098FKXT8L',
    'output': ['json'],
}
```

Send the above data to the generic URL endpoint instead of `/search`:

```python
response = requests.post(
    'https://webapi.oxylabs.io/v1/scrape/amazon',
    headers={'Authorization': f"Bearer {os.environ['OXYLABS_WEB_API_KEY']}"},
    json=payload,
)
```

![](https://oxylabs.io/_next/image?url=https%3A%2F%2Foxylabs.io%2Foxylabs-web%2FZpBeRx5LeNNTxEWo_fddcfa94-6d5c-4a61-b9ff-7035108bf36d_amazon_product_details.png%3Fauto%3Dformat%2Ccompress&w=1200&q=75)

### Scraping products by ASIN

Another way to get data is by the ASIN – Amazon's own product ID – instead of a URL. You need to modify the payload and switch to the `/product` endpoint:

```python
payload = {
    'query': 'B098FKXT8L',
    'domain': 'co.uk',
    'autoselect_variant': True,
    'output': ['json'],
}

response = requests.post(
    'https://webapi.oxylabs.io/v1/scrape/amazon/product',
    headers={'Authorization': f"Bearer {os.environ['OXYLABS_WEB_API_KEY']}"},
    json=payload,
)
```

Note the optional parameter `domain`. Use this parameter to get Amazon data from any domain, such as amazon.co.uk. `autoselect_variant` follows the listing's default variant instead of returning the bare parent listing – useful when a parent ASIN returns no price.

For the full parameter reference across all six endpoints, see the [Amazon Scraper](https://github.com/oxylabs/amazon-scraper) repository or the [Amazon API reference](https://developers.oxylabs.io/api-reference/dedicated-scrapers/commerce-scrapers#amazon).

Looking to scrape more other Amazon data? [Amazon ASIN Scraper](https://github.com/oxylabs/amazon-asin-scraper), [Handle Amazon CAPTCHA](https://github.com/oxylabs/how-to-handle-amazon-captcha), [How to Scrape Amazon Prices](https://github.com/oxylabs/how-to-scrape-amazon-prices), [Amazon Scraper (Web API overview)](https://github.com/oxylabs/amazon-scraper)

## Practical use cases

Both the free script and Web API return the same kind of Amazon product data, so they support the same workflows, from production dashboards to a class project on market trends:

1. **Price and catalog monitoring** – track price, rating, sales rank, and availability changes for a list of ASINs or an entire product category (use the `/bestsellers` endpoint to pull rank directly).
2. **Competitive intelligence** – compare product data across competing listings in the same category to benchmark pricing, positioning, and competitor strategies.
3. **Market research** – scrape whole product categories to spot trends in pricing, ratings, and descriptions over time, useful for product research and validating new business ideas.
4. **Catalog enrichment** – pull structured product data (title, price, image, description) into your own database, storefront, or Amazon product dataset for further analysis.
5. **Brand protection** – monitor listings for unauthorized sellers and price violations across your supply chain.

## Why choose Oxylabs?

- **Pay for results, not attempts:** Amazon requests start from $0.50 per 1,000 results ([see pricing](https://oxylabs.io/products/web-api/scrape/pricing)).
- **Any Amazon marketplace:** get localized product data from any marketplace via the `domain` parameter, with prices reported in US dollars or the local currency.
- **Built-in proxy management:** a rotating proxy pool, so you don't manage IPs or get blocked yourself.
- **Access handled for you:** CAPTCHA handling, JavaScript rendering, and anti-bot fingerprinting are included.
- **Flexible output:** choose JSON, Markdown, HTML, or a screenshot, delivered in the response or to your own cloud storage, such as Google Cloud Storage – making it easy to feed straight into your own dataset or BI pipeline.
- **Dedicated support:** get help from integration to debugging, through 24/7 live chat.

## FAQ

### Is it legal to scrape Amazon product data?

Scraping publicly available data is generally allowed, but the answer depends on your jurisdiction, the type of data you collect, and how you use it. Respect Amazon's terms, avoid personal data, and get legal advice for your specific project.

### Why did my search results come back empty?

Amazon frequently changes its search-results markup. This guide's listing selector reads the `data-asin` attribute straight off each `div[data-component-type="s-search-result"]` card, which is more resilient than selecting a title link – but if Amazon changes this markup again, inspect a live results page and adjust the selector in [`amazon_scraper.py`](amazon_scraper.py) accordingly.

### Should I use the free script or Web API?

Use the free script for small, one-off jobs on a single search or category page. Choose Web API when you need larger volumes, multiple marketplaces, or reliable access without managing proxies and headers yourself.

### Can I scrape other Amazon marketplaces, like amazon.co.uk?

Yes, the free script works on any Amazon domain – just pass that domain's URL. With Web API, set the `domain` parameter instead, e.g. `co.uk` or `de`.

## Learn more

For a full blog-length walkthrough of everything in this guide, see [How to Web Scrape Product Data From Amazon: Python Guide](https://oxylabs.io/blog/how-to-scrape-amazon-product-data) on the Oxylabs blog. For the complete Web API reference – every Amazon endpoint, parameter, and more code examples – see the [Amazon Scraper](https://github.com/oxylabs/amazon-scraper) repository or the [Amazon API reference](https://developers.oxylabs.io/api-reference/dedicated-scrapers/commerce-scrapers#amazon).

## Featured in Technical Communities

This guide has been shared across developer communities:
- [How to Web Scrape Product Data From Amazon: Python Guide](https://oxylabs.io/blog/how-to-scrape-amazon-product-data) – Oxylabs Blog
- [How To Scrape Amazon Product Data Using Python](https://dev.to/oxylabs-io/how-to-scrape-amazon-product-data-using-python-2gj3) – DEV Community

## Contacts

If you have questions or need further help, reach out at [support@oxylabs.io](mailto:support@oxylabs.io), through live chat on the [Oxylabs Dashboard](https://dashboard.oxylabs.io), or join our [Discord community](https://discord.gg/Pds3gBmKMH). For enterprise inquiries, contact your dedicated account manager.
