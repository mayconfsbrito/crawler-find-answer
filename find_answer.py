"""Crawler to find the answer."""
from requests_html import HTMLSession, HTML


def decode_token(token):
    """Method to decode the token.

    Args:
        token (str): encoded token extracted from html content.
    Returns:
        decoded_token: decoded token.
    """
    replacements = {'a': 'z', 'b': 'y', 'c': 'x', 'd': 'w', 'e': 'v',
                    'f': 'u', 'g': 't', 'h': 's', 'i': 'r', 'j': 'q',
                    'k': 'p', 'l': 'o', 'm': 'n', 'n': 'm', 'o': 'l',
                    'p': 'k', 'q': 'j', 'r': 'i', 's': 'h', 't': 'g',
                    'u': 'f', 'v': 'e', 'w': 'd', 'x': 'c', 'y': 'b',
                    'z': 'a'}
    decoded_token = ''
    for digit in token:
        if replacements.get(digit):
            decoded_token += replacements.get(digit)
        else:
            decoded_token += digit
    return decoded_token


def find_answer(url, headers):
    """Method to get the answer.

    Args:
        url (str): url of the site with the answer.
        headers (dict): headers of the post.
    Returns:
        answer (str): answer found in the site.
        status_code (int): number of the status code of the request.
    """
    with HTMLSession() as session:
        r = session.get(url)
        token = get_token(r.content.decode('utf-8'))
        token = decode_token(token)
        data = {"token": token}
        response = session.post(url, data=data, headers=headers)
        return response.html.xpath('span/text()', first=True)


def get_token(content):
    """Method to get the token.

    Args:
        content (str): text content of the html request.
    Returns:
        token (str): token extracted from html content.
    """
    html = HTML(html=content)
    token = html.find('input', first=True).attrs.get('value')
    return token

if __name__ == '__main__':
    url = 'http://applicant-test.us-east-1.elasticbeanstalk.com/'
    headers = {
        'Host': 'applicant-test.us-east-1.elasticbeanstalk.com',
        'Origin': 'http://applicant-test.us-east-1.elasticbeanstalk.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                      'AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/71.0.3578.98 Safari/537.36',
        'Referer': 'http://applicant-test.us-east-1.elasticbeanstalk.com/',
    }
    answer = find_answer(url, headers)
    print(f'Answer: {answer}')
