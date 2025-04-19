import json
from Project import url_to_soup

def shop_all_products_url(url):
    soup = url_to_soup.get_soup_from_url(url)
    button_div = soup.find('div', class_='bottom-button-area is-large-btn text-align-center')
    href = button_div.find('a', class_='btn', href=True)
    return href['href']


def get_categories_link():
    url = 'https://newegg.com'
    soup = url_to_soup.get_soup_from_url(url)
    categories = soup.find_all('a', class_='menu-list-link bg-transparent-lightblue', href=True)
    categories_href = []
    for category in categories:
        categories_href.append(shop_all_products_url(category['href']))

    return categories_href

if __name__ == '__main__':
    cat = get_categories_link()

    with open("categories_all_products_links.json", "w") as file:
        json.dump(cat, file, indent=4)