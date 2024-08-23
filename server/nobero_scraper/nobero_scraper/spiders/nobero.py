import json
import re
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse, urljoin

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from bs4 import BeautifulSoup

class StringUtils:
    @staticmethod
    def remove_after_slash(input_string: str) -> str:
        """
        Remove everything after the first slash in the input string.
        
        Args:
            input_string (str): The input string to process.
        
        Returns:
            str: The processed string.
        """
        slash_index = input_string.find('/')
        if slash_index != -1:
            start_index = input_string.rfind(' ', 0, slash_index)
            result = input_string[:start_index].strip()
        else:
            result = input_string.strip()
        return result

    @staticmethod
    def convert_to_json(input_string: str) -> str:
        """
        Convert a string representation of a dictionary to a JSON string.
        
        Args:
            input_string (str): The input string to convert.
        
        Returns:
            str: The JSON string.
        """
        items = input_string.strip('{}').split(',')
        data = {}
        for item in items:
            key, value = item.split(':')
            key = key.strip().strip("'")
            value = value.strip().strip("'")
            data[key] = value
        return json.dumps(data)

class ProductParser:
    @staticmethod
    def parse_product_data(response: scrapy.http.Response, soup: BeautifulSoup) -> Optional[Dict[str, Any]]:
        """
        Parse product data from the response and BeautifulSoup object.
        
        Args:
            response (scrapy.http.Response): The Scrapy response object.
            soup (BeautifulSoup): The BeautifulSoup object of the response.
        
        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the parsed product data, or None if the category should be skipped.
        """
        product_data = {}

        # Extract and check category
        script_data = response.xpath('//script[@class="analytics"]/text()').get()
        category = re.search(r'"category":"(.*?)"', script_data)
        if category:
            product_data['category'] = category.group(1)
            if ProductParser.should_skip_category(product_data['category']):
                return None
        else:
            return None  # Skip if category can't be determined

        # Extract product URL
        product_data['url'] = response.url

        # Extract product title
        title = soup.find('h1')
        product_data['title'] = title.text.strip() if title else ''

        # Extract product price
        price_element = soup.find('h2', id='variant-price', class_='font-[familySemiBold] text-xl md:text-[1.75rem] text-[#1A1E31]')
        product_data['price'] = int(price_element.text.strip().replace('₹', '').replace(',', '')) if price_element else 0

        # Extract MRP
        mrp_element = soup.find('span', id='variant-compare-at-price', class_='line-through')
        product_data['MRP'] = int(mrp_element.text.strip().replace('₹', '').replace(',', '')) if mrp_element else 0

        # Extract last 7 day sale
        ProductParser._parse_last_7_day_sale(product_data, soup)

        # Extract product metafields
        ProductParser._parse_metafields(product_data, soup)

        # Extract product description
        product_data['description'] = ProductParser._parse_description(soup)

        # Extract product images
        product_data['product_urls'] = ProductParser._parse_product_images(soup)

        # Extract available SKUs (color, size)
        product_data['available_skus'] = ProductParser._parse_available_skus(soup)

        # Extract other product details
        ProductParser._parse_other_details(product_data, soup)

        return product_data

    @staticmethod
    def should_skip_category(category: str) -> bool:
        """
        Check if the given category should be skipped.

        Args:
            category (str): The category to check.

        Returns:
            bool: True if the category should be skipped, False otherwise.
        """
        skip_categories = [
            "Women Shorts",
            "Womens Coord Set",
            "Women T-shirt Dress",
            "Women Joggers",
            "Womens Tops",
            "Women Tees"
        ]
        return category in skip_categories

    @staticmethod
    def _parse_last_7_day_sale(product_data: Dict[str, Any], soup: BeautifulSoup) -> None:
        last_7_day_sale_element = soup.find('div', class_='product_bought_count')
        if last_7_day_sale_element:
            payload_str = last_7_day_sale_element.get('data-ga-view-payload-custom')
            json_string = StringUtils.convert_to_json(payload_str)
            payload_data = json.loads(json_string)
            product_data['last_7_day_sale'] = int(payload_data.get('product_count', 0))
        else:
            product_data['last_7_day_sale'] = 0

    @staticmethod
    def _parse_metafields(product_data: Dict[str, Any], soup: BeautifulSoup) -> None:
        for div in soup.find_all('div', class_='product-metafields-values'):
            key = div.find('h4').text.strip().lower()
            value = div.find('p').text.strip()
            product_data[key] = value

    @staticmethod
    def _parse_description(soup: BeautifulSoup) -> str:
        description_elements = soup.find('div', id='description_content').find_all(['strong', 'p'])
        description = ""
        for element in description_elements:
            span = element.find_next_sibling('span')
            if span:
                description += f"{element.text}: {span.text}\n"
            else:
                next_sibling = element.find_next_sibling()
                if next_sibling:
                    description += f"{element.text}: {next_sibling.text}\n"
                else:
                    description += f"{element.text}:\n"
        return description.replace('::', ':')

    @staticmethod
    def _parse_product_images(soup: BeautifulSoup) -> List[Dict[str, str]]:
        product_urls = []
        product_url = soup.find('script', class_='product-json').get_text()
        product_url = json.loads(product_url)

        seen_colors = set()
        seen_urls = set()

        for item in product_url:
            color = StringUtils.remove_after_slash(item["title"])
            url = 'https:' + item["featured_image"]["src"]
            if color not in seen_colors and url not in seen_urls:
                product_urls.append({"color": color, "imgurl": url})
                seen_colors.add(color)
                seen_urls.add(url)

        return product_urls

    @staticmethod
    def _parse_available_skus(soup: BeautifulSoup) -> List[Dict[str, Any]]:
        available_skus = []
        options = soup.find('select', {'name': 'id'}).find_all('option')

        for option in options:
            if option.get('data-variant-qty') != "0":
                variant = option.get('data-variant').split('-')
                color, size = variant[0], variant[1]

                color_found = next((item for item in available_skus if item["color"] == color), None)

                if color_found:
                    color_found["size"].append(size)
                else:
                    available_skus.append({"color": color, "size": [size]})

        return available_skus

    @staticmethod
    def _parse_other_details(product_data: Dict[str, Any], soup: BeautifulSoup) -> None:
        details = soup.find_all('div', class_='product-single__details')
        for detail in details:
            detail_title = detail.find('div', class_='product-single__details-title').text.strip()
            detail_value = detail.find('div', class_='product-single__details-value').text.strip()
            product_data[detail_title.lower().replace(' ', '_')] = detail_value

class NoberoSpider(CrawlSpider):
    """
    A spider to crawl and scrape product information from nobero.com,
    avoiding query URLs and focusing on main links.
    """
    name = "nobero"
    allowed_domains = ["nobero.com"]
    start_urls = ["https://nobero.com/pages/men"]

    rules = (
        Rule(
            LinkExtractor(
                allow=(r'/collections/[^/]+', r'/products/[^/]+'),
                deny=r'\?'
            ),
            callback='parse_item',
            follow=True,
            process_links='process_links'
        ),
    )

    def process_links(self, links: List[scrapy.link.Link]) -> List[scrapy.link.Link]:
        """
        Process and filter links before following them.

        This method removes query parameters from URLs and ensures only unique,
        clean URLs are followed.

        Args:
            links (List[scrapy.link.Link]): The list of extracted links.

        Returns:
            List[scrapy.link.Link]: The list of processed and filtered links.
        """
        cleaned_links = []
        seen_urls = set()

        for link in links:
            # Parse the URL and remove query parameters
            parsed_url = urlparse(link.url)
            clean_url = urljoin(link.url, parsed_url.path)

            # Only add the link if we haven't seen this clean URL before
            if clean_url not in seen_urls:
                link.url = clean_url
                cleaned_links.append(link)
                seen_urls.add(clean_url)

        return cleaned_links

    def parse_item(self, response: scrapy.http.Response) -> Optional[Dict[str, Any]]:
        """
        Parse a page and extract information based on its type (category or product).

        Args:
            response (scrapy.http.Response): The response object for the page.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the parsed data, or None if not a product page or if the category should be skipped.
        """
        if '/products/' in response.url:
            return self.parse_product(response)
        elif '/collections/' in response.url:
            self.parse_category(response)
        return None

    def parse_category(self, response: scrapy.http.Response) -> None:
        """
        Parse a category page and log information.

        Args:
            response (scrapy.http.Response): The response object for the category page.
        """
        category = response.url.split('/')[-1]
        self.logger.info(f"Parsing category: {category}")

    def parse_product(self, response: scrapy.http.Response) -> Optional[Dict[str, Any]]:
        """
        Parse a product page and extract product information.

        Args:
            response (scrapy.http.Response): The response object for the product page.

        Returns:
            Optional[Dict[str, Any]]: A dictionary containing the parsed product data, or None if the category should be skipped.
        """
        soup = BeautifulSoup(response.text, 'html.parser')
        product_data = ProductParser.parse_product_data(response, soup)
        if product_data:
            self.logger.info(f"Scraped product: {product_data['title']} (Category: {product_data['category']})")
        else:
            self.logger.info(f"Skipped product: {response.url}")
        return product_data

def main():
    """
    Main function to start the Scrapy crawler process.
    """
    process = CrawlerProcess(get_project_settings())
    process.crawl(NoberoSpider)
    process.start()

if __name__ == '__main__':
    main()