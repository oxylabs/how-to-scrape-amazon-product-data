# Scraping Amazon Product Data With Python

[![Oxylabs promo code](https://user-images.githubusercontent.com/129506779/250792357-8289e25e-9c36-4dc0-a5e2-2706db797bb5.png)](https://oxylabs.go2cloud.org/aff_c?offer_id=7&aff_id=877&url_id=112)

You can find an extended version on our [blog](https://oxylabs.io/blog/scrape-amazon-product-data).

This guide uses Oxylabs [Amazon Scraper](https://oxylabs.io/products/scraper-api/ecommerce/amazon) along with Python to scrape the following data points:

- Product name
- Product rating
- Product price
- Product images
- Product description

## Setting up for scraping

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
 g









