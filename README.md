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





