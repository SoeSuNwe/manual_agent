import requests
import re

def search_location(query):
    """Search for location information using DuckDuckGo HTML search"""
    print(f"\n  🔎 Search query: {query}")
    
    try:
        # Use DuckDuckGo HTML endpoint for better results
        url = "https://html.duckduckgo.com/html/"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        data = {"q": f"{query} location city country"}
        
        print(f"  📡 Requesting: {url}")
        response = requests.post(url, headers=headers, data=data, timeout=10)
        print(f"  📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            # Extract text snippets from results (capture full content including HTML tags)
            snippet_matches = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', response.text, re.DOTALL)
            
            if snippet_matches:
                # Clean HTML tags from each snippet
                snippets = []
                for i, snippet in enumerate(snippet_matches[:3], 1):
                    clean_snippet = re.sub(r'<[^>]+>', '', snippet).strip()
                    clean_snippet = re.sub(r'\s+', ' ', clean_snippet)  # Normalize whitespace
                    if clean_snippet:
                        snippets.append(clean_snippet)
                        print(f"  📄 Result {i}: {clean_snippet[:100]}...")
                
                if snippets:
                    result = " ".join(snippets)
                    print(f"  ✅ Found {len(snippets)} results")
                    return result
        
        # Fallback: Try Wikipedia search
        print("  ⚠️ DuckDuckGo returned no results, trying Wikipedia...")
        return search_wikipedia(query)
        
    except Exception as e:
        print(f"  ❌ DuckDuckGo error: {e}")
        return search_wikipedia(query)

def search_wikipedia(query):
    """Fallback search using Wikipedia API"""
    try:
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 3
        }
        
        print(f"  📡 Wikipedia search: {query}")
        response = requests.get(url, params=params, timeout=10)
        print(f"  📥 Status: {response.status_code}")
        data = response.json()
        
        results = []
        for item in data.get("query", {}).get("search", []):
            # Clean HTML tags from snippet
            snippet = re.sub(r'<[^>]+>', '', item.get("snippet", ""))
            title = item.get("title", "")
            results.append(f"{title}: {snippet}")
        
        if results:
            result = " ".join(results)
            print(f"  ✅ Wikipedia found {len(results)} results")
            print(f"  📄 Result: {result[:150]}...")
            return result
        
        print("  ⚠️ No Wikipedia results")
        return f"No results found for: {query}"
        
    except Exception as e:
        print(f"  ❌ Wikipedia error: {e}")
        return f"Search failed for: {query}"
