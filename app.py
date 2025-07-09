# Backend - app.py (Flask Application)
from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import random
import re
import requests
import os
from datetime import datetime
import logging

app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Business name generation data
NAME_PATTERNS = {
    'prefixes': ['Pro', 'Elite', 'Prime', 'Alpha', 'Beta', 'Max', 'Ultra', 'Meta', 'Neo', 'Zen', 'Apex', 'Core', 'Smart', 'Quick', 'Fast', 'Bright', 'Swift', 'Bold', 'Pure', 'True', 'Next', 'Super', 'Mega', 'Hyper', 'Quantum'],
    'suffixes': ['Hub', 'Lab', 'Works', 'Studios', 'Group', 'Co', 'Inc', 'Solutions', 'Systems', 'Tech', 'Forge', 'Craft', 'Vault', 'Space', 'Zone', 'Nest', 'Base', 'Point', 'Edge', 'Force', 'Genius', 'Masters', 'Pros', 'Experts'],
    'connectors': ['&', 'and', '+', 'x', '']
}

INDUSTRY_KEYWORDS = {
    'tech': ['Digital', 'Cyber', 'Data', 'Cloud', 'AI', 'Quantum', 'Pixel', 'Code', 'Logic', 'Neural', 'Sync', 'Binary', 'Matrix', 'Byte', 'Node', 'Soft', 'Net', 'Web', 'App', 'Bit'],
    'food': ['Flavor', 'Taste', 'Fresh', 'Gourmet', 'Savory', 'Spice', 'Crisp', 'Golden', 'Delicious', 'Artisan', 'Organic', 'Farm', 'Kitchen', 'Recipe', 'Feast', 'Bite', 'Dish', 'Cuisine', 'Chef', 'Cook'],
    'fitness': ['Fit', 'Strong', 'Power', 'Energy', 'Vital', 'Active', 'Peak', 'Muscle', 'Flex', 'Endure', 'Sprint', 'Lift', 'Pump', 'Core', 'Balance', 'Tone', 'Burn', 'Train', 'Sweat', 'Rush'],
    'creative': ['Design', 'Art', 'Creative', 'Vision', 'Inspire', 'Imagine', 'Craft', 'Studio', 'Canvas', 'Palette', 'Sketch', 'Dream', 'Muse', 'Concept', 'Idea', 'Brand', 'Visual', 'Style', 'Trend', 'Pixel'],
    'business': ['Enterprise', 'Venture', 'Capital', 'Growth', 'Success', 'Profit', 'Strategic', 'Global', 'Corporate', 'Professional', 'Executive', 'Premier', 'Leading', 'Expert', 'Champion', 'Elite', 'Prime', 'Top', 'Best', 'First'],
    'retail': ['Shop', 'Store', 'Market', 'Boutique', 'Outlet', 'Plaza', 'Mall', 'Mart', 'Emporium', 'Bazaar', 'Trade', 'Commerce', 'Sale', 'Deal', 'Buy', 'Sell', 'Goods', 'Items', 'Products', 'Merchandise'],
    'health': ['Health', 'Wellness', 'Care', 'Medical', 'Clinic', 'Therapy', 'Heal', 'Cure', 'Life', 'Vitality', 'Recovery', 'Treatment', 'Medicine', 'Doctor', 'Nurse', 'Patient', 'Healthy', 'Pure', 'Clean', 'Safe']
}

def detect_industry(keywords):
    """Detect industry based on input keywords"""
    keywords_lower = keywords.lower()
    
    industry_scores = {}
    for industry, words in INDUSTRY_KEYWORDS.items():
        score = sum(1 for word in words if word.lower() in keywords_lower)
        industry_scores[industry] = score
    
    # Check for specific keywords
    if any(word in keywords_lower for word in ['tech', 'software', 'digital', 'ai', 'app', 'web', 'code', 'programming']):
        return 'tech'
    elif any(word in keywords_lower for word in ['food', 'restaurant', 'coffee', 'cuisine', 'catering', 'chef', 'cook']):
        return 'food'
    elif any(word in keywords_lower for word in ['fitness', 'gym', 'health', 'workout', 'sports', 'training']):
        return 'fitness'
    elif any(word in keywords_lower for word in ['design', 'creative', 'art', 'marketing', 'agency', 'brand']):
        return 'creative'
    elif any(word in keywords_lower for word in ['shop', 'store', 'retail', 'boutique', 'market', 'sell']):
        return 'retail'
    elif any(word in keywords_lower for word in ['medical', 'healthcare', 'clinic', 'therapy', 'wellness']):
        return 'health'
    
    # Return industry with highest score
    return max(industry_scores, key=industry_scores.get) if industry_scores else 'business'

def generate_creative_name(base_word, industry):
    """Generate creative business name variations"""
    base_word = re.sub(r'[^a-zA-Z]', '', base_word)
    if len(base_word) < 3:
        return None
    
    industry_words = INDUSTRY_KEYWORDS.get(industry, INDUSTRY_KEYWORDS['business'])
    
    patterns = [
        # Compound words
        lambda: random.choice(industry_words) + base_word.capitalize(),
        # Prefix + base word
        lambda: random.choice(NAME_PATTERNS['prefixes']) + base_word.capitalize(),
        # Base word + suffix
        lambda: base_word.capitalize() + random.choice(NAME_PATTERNS['suffixes']),
        # Blended words
        lambda: blend_words(random.choice(industry_words), base_word),
        # Modified spelling
        lambda: modify_spelling(base_word.capitalize()),
        # Industry + suffix
        lambda: random.choice(industry_words) + random.choice(NAME_PATTERNS['suffixes']),
        # Prefix + industry word
        lambda: random.choice(NAME_PATTERNS['prefixes']) + random.choice(industry_words),
    ]
    
    pattern = random.choice(patterns)
    try:
        return pattern()
    except:
        return base_word.capitalize() + random.choice(NAME_PATTERNS['suffixes'])

def blend_words(word1, word2):
    """Blend two words together"""
    if len(word1) < 3 or len(word2) < 3:
        return word1 + word2
    
    # Different blending strategies
    strategies = [
        lambda: word1[:len(word1)//2] + word2[len(word2)//2:],
        lambda: word1[:2] + word2[2:],
        lambda: word1[:-2] + word2[-2:],
        lambda: word1[:3] + word2[3:] if len(word2) > 3 else word1 + word2,
    ]
    
    return random.choice(strategies)()

def modify_spelling(word):
    """Modify word spelling for creativity"""
    modifications = [
        lambda w: w.replace('er', 'r') if w.endswith('er') else w,
        lambda w: w.replace('s', 'z') if w.endswith('s') else w,
        lambda w: w.replace('c', 'k') if 'c' in w else w,
        lambda w: w.replace('ph', 'f') if 'ph' in w else w,
        lambda w: w + 'y' if not w.endswith('y') and len(w) > 4 else w,
        lambda w: w[:-1] + 'x' if len(w) > 4 and w[-1] in 'aeiou' else w,
    ]
    
    modified = word
    for mod in random.sample(modifications, min(2, len(modifications))):
        modified = mod(modified)
    
    return modified

def check_domain_availability(domain):
    """Check if domain is available (simplified simulation)"""
    # In a real implementation, you'd use a domain API like Namecheap or GoDaddy
    # For demo purposes, we'll simulate availability
    return random.choice([True, False])

def generate_business_names(keywords, count=8):
    """Generate business names based on keywords"""
    industry = detect_industry(keywords)
    words = [word.strip() for word in re.findall(r'\b\w+\b', keywords.lower()) if len(word.strip()) > 2]
    
    names = set()
    
    # Generate names from input words
    for word in words:
        for _ in range(3):
            name = generate_creative_name(word, industry)
            if name and 4 <= len(name) <= 20:
                names.add(name)
    
    # Generate names from industry keywords
    industry_words = INDUSTRY_KEYWORDS.get(industry, INDUSTRY_KEYWORDS['business'])
    while len(names) < count:
        base_word = random.choice(industry_words + words)
        name = generate_creative_name(base_word, industry)
        if name and 4 <= len(name) <= 20:
            names.add(name)
    
    # Convert to list and add domain info
    result = []
    for name in list(names)[:count]:
        domain_available = check_domain_availability(name.lower() + '.com')
        result.append({
            'name': name,
            'domain': name.lower() + '.com',
            'available': domain_available,
            'industry': industry
        })
    
    return result

@app.route('/')
def index():
    """Serve the main application"""
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/generate', methods=['POST'])
def generate_names():
    """API endpoint to generate business names"""
    try:
        data = request.get_json()
        keywords = data.get('keywords', '').strip()
        
        if not keywords:
            return jsonify({'error': 'Keywords are required'}), 400
        
        logger.info(f"Generating names for keywords: {keywords}")
        
        names = generate_business_names(keywords)
        
        return jsonify({
            'success': True,
            'names': names,
            'count': len(names),
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error generating names: {str(e)}")
        return jsonify({'error': 'Failed to generate names'}), 500

@app.route('/healthz')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

# HTML Template (embedded for simplicity)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Business Name Generator</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }

        .container {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            max-width: 800px;
            width: 100%;
        }

        h1 {
            text-align: center;
            margin-bottom: 30px;
            color: #333;
            font-size: 2.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }

        .input-section {
            margin-bottom: 30px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            color: #333;
            font-weight: 600;
            font-size: 1.1rem;
        }

        input[type="text"] {
            width: 100%;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.9);
        }

        input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        .generate-btn {
            width: 100%;
            padding: 15px;
            background: linear-gradient(45deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        .generate-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.3);
        }

        .generate-btn:disabled {
            opacity: 0.6;
            cursor: not-allowed;
            transform: none;
        }

        .results-section {
            margin-top: 30px;
            display: none;
        }

        .results-title {
            font-size: 1.5rem;
            color: #333;
            margin-bottom: 20px;
            font-weight: 600;
        }

        .name-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 15px;
        }

        .name-card {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 20px;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
            cursor: pointer;
        }

        .name-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 15px 30px rgba(0, 0, 0, 0.2);
        }

        .name-card.available {
            background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
        }

        .name-card.unavailable {
            background: linear-gradient(135deg, #FF9800 0%, #F57C00 100%);
        }

        .name-title {
            font-size: 1.3rem;
            font-weight: 700;
            margin-bottom: 10px;
        }

        .domain-info {
            font-size: 0.9rem;
            opacity: 0.9;
            margin-bottom: 5px;
        }

        .status {
            font-size: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }

        .spinner {
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 20px;
        }

        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        .error {
            background: #ff4444;
            color: white;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: center;
        }

        .tips {
            background: rgba(102, 126, 234, 0.1);
            padding: 20px;
            border-radius: 10px;
            margin-top: 30px;
            border-left: 4px solid #667eea;
        }

        .tips h3 {
            color: #333;
            margin-bottom: 10px;
        }

        .tips ul {
            color: #666;
            margin-left: 20px;
        }

        .tips li {
            margin-bottom: 5px;
        }

        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            h1 {
                font-size: 2rem;
            }
            .name-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 AI Business Name Generator</h1>
        
        <div class="input-section">
            <label for="keywords">Enter your business keywords or description:</label>
            <input type="text" id="keywords" placeholder="e.g., tech startup, coffee shop, fitness, creative agency..." />
            <button class="generate-btn" onclick="generateNames()">Generate Business Names</button>
        </div>

        <div class="results-section" id="results">
            <h2 class="results-title">Generated Business Names</h2>
            <div id="names-container"></div>
        </div>

        <div class="tips">
            <h3>💡 Tips for Better Results:</h3>
            <ul>
                <li>Be specific about your industry (tech, food, fitness, etc.)</li>
                <li>Include target audience or style preferences</li>
                <li>Mention key services or products</li>
                <li>Consider your brand personality</li>
                <li>Try different keyword combinations</li>
            </ul>
        </div>
    </div>

    <script>
        async function generateNames() {
            const keywords = document.getElementById('keywords').value.trim();
            
            if (!keywords) {
                alert('Please enter some keywords or description!');
                return;
            }

            const generateBtn = document.querySelector('.generate-btn');
            const resultsSection = document.getElementById('results');
            const namesContainer = document.getElementById('names-container');

            try {
                // Show loading
                generateBtn.disabled = true;
                generateBtn.textContent = 'Generating...';
                resultsSection.style.display = 'block';
                namesContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>Generating creative business names...</p></div>';

                // Call API
                const response = await fetch('/api/generate', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ keywords: keywords })
                });

                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                
                if (data.success) {
                    displayNames(data.names);
                } else {
                    throw new Error(data.error || 'Failed to generate names');
                }

            } catch (error) {
                console.error('Error:', error);
                namesContainer.innerHTML = `<div class="error">Error: ${error.message}</div>`;
            } finally {
                generateBtn.disabled = false;
                generateBtn.textContent = 'Generate Business Names';
            }
        }

        function displayNames(names) {
            const namesContainer = document.getElementById('names-container');
            
            let html = '<div class="name-grid">';
            names.forEach(nameData => {
                const statusClass = nameData.available ? 'available' : 'unavailable';
                const statusText = nameData.available ? 'Domain Available' : 'Check Domain';
                
                html += `
                    <div class="name-card ${statusClass}" onclick="copyToClipboard('${nameData.name}', this)">
                        <div class="name-title">${nameData.name}</div>
                        <div class="domain-info">${nameData.domain}</div>
                        <div class="status">${statusText}</div>
                    </div>
                `;
            });
            html += '</div>';
            
            namesContainer.innerHTML = html;
        }

        function copyToClipboard(text, element) {
            navigator.clipboard.writeText(text).then(() => {
                const originalHTML = element.innerHTML;
                element.innerHTML = `
                    <div class="name-title">✓ Copied!</div>
                    <div class="domain-info">Name copied to clipboard</div>
                    <div class="status">SUCCESS</div>
                `;
                
                setTimeout(() => {
                    element.innerHTML = originalHTML;
                }, 1500);
            }).catch(err => {
                console.error('Failed to copy:', err);
                alert('Failed to copy to clipboard');
            });
        }

        // Allow Enter key to trigger generation
        document.getElementById('keywords').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generateNames();
            }
        });
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)