from mkdocs.plugins import BasePlugin
import os
import json

class EnhancedSearchPlugin(BasePlugin):
    def on_post_build(self, config):
        """
        Enhanced search index by adding additional metadata to search results
        """
        search_index_path = os.path.join(config['site_dir'], 'search', 'search_index.json')
        
        if os.path.exists(search_index_path):
            with open(search_index_path, 'r', encoding='utf-8') as f:
                search_index = json.load(f)
            
            # Add custom boost to certain pages
            docs_dir = config['docs_dir']
            boost_file = os.path.join(docs_dir, 'search-boost.yml')
            
            boosts = {}
            if os.path.exists(boost_file):
                with open(boost_file, 'r', encoding='utf-8') as f:
                    for line in f:
                        if ':' in line and not line.startswith('#'):
                            path, boost = line.split(':', 1)
                            path = path.strip()
                            try:
                                boost = float(boost.strip())
                                boosts[path] = boost
                            except ValueError:
                                pass
            
            # Apply boosts to search index
            for doc in search_index.get('docs', []):
                location = doc.get('location', '')
                for path, boost in boosts.items():
                    if path in location:
                        doc['boost'] = boost
                        break
            
            # Save enhanced search index
            with open(search_index_path, 'w', encoding='utf-8') as f:
                json.dump(search_index, f)
                
        return config
