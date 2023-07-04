from flask import Flask, request, jsonify
from googlesearch import Search, SearchOptions, Result
import json

app = Flask(__name__)

@app.route('/search', methods=['GET'])
def search():
    search_term = request.args.get('q')
    country_code = request.args.get('country')
    language_code = request.args.get('language')
    limit = int(request.args.get('limit', 10))
    start = int(request.args.get('start', 1))
    user_agent = request.headers.get('User-Agent')
    over_limit = request.args.get('over_limit') == 'true'
    proxy_addr = request.args.get('proxy')
    follow_next_page = request.args.get('follow_next_page') == 'true'
    
    options = SearchOptions(
        CountryCode=country_code,
        LanguageCode=language_code,
        Limit=limit,
        Start=start,
        UserAgent=user_agent,
        OverLimit=over_limit,
        ProxyAddr=proxy_addr,
        FollowNextPage=follow_next_page
    )
    
    results, error = Search(search_term, options)
    
    if error:
        return jsonify({'error': str(error)})
    
    result_list = []
    
    for result in results:
        result_dict = {
            'Rank': result.Rank,
            'URL': result.URL,
            'Title': result.Title,
            'Description': result.Description
        }
        result_list.append(result_dict)
    
    return jsonify({'results': result_list})

if __name__ == '__main__':
    app.run()
