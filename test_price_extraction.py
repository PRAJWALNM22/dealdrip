#!/usr/bin/env python3
"""
Quick test script to debug price extraction patterns
"""

import re

def parse_price(price_text):
    """Parse price text into a float value"""
    if not price_text:
        return None
    
    # Convert to string and clean
    price_text = str(price_text).strip()
    
    # Remove currency symbols and extra characters, keep digits, dots, commas
    price_text = re.sub(r'[^0-9.,]', '', price_text)
    
    if not price_text:
        return None
    
    # Handle different decimal formats
    try:
        if ',' in price_text and '.' in price_text:
            # Check which comes last to determine format
            last_comma = price_text.rfind(',')
            last_dot = price_text.rfind('.')
            
            if last_dot > last_comma:
                # Format: 1,234.56 (comma as thousands separator)
                price_text = price_text.replace(',', '')
            else:
                # Format: 1.234,56 (European format)
                # Replace dots with empty, comma with dot
                price_text = price_text.replace('.', '').replace(',', '.')
        
        elif ',' in price_text:
            # Could be either 1,234 or 1,56
            parts = price_text.split(',')
            if len(parts) == 2 and len(parts[1]) <= 2:
                # Likely European decimal format: 1,56
                price_text = price_text.replace(',', '.')
            else:
                # Likely thousands separator: 1,234 or 12,34,567
                price_text = price_text.replace(',', '')
        
        # Convert to float
        price = float(price_text)
        
        # Reasonable bounds check
        if 0.01 <= price <= 10000000:  # Between 1 cent and 10 million
            return price
        else:
            return None
            
    except (ValueError, TypeError):
        return None

def test_regex_patterns():
    """Test regex patterns with sample content"""
    
    # Sample content that might contain prices
    test_content = """
    <div class="price-container">₹1,599</div>
    <span class="selling-price">Rs. 2,499</span>
    "sellingPrice": 3299,
    "currentPrice": "4999",
    data-price="1999"
    Price: ₹899 only
    MRP: ₹1299
    """
    
    patterns = [
        # Standard rupee patterns with flexible spacing and formatting
        r'₹\s*([1-9][0-9,]*(?:\.[0-9]{2})?)',
        r'Rs\.?\s*([1-9][0-9,]*(?:\.[0-9]{2})?)',
        r'INR\s*([1-9][0-9,]*(?:\.[0-9]{2})?)',
        r'₹([1-9][0-9,]{2,8})',
        
        # JSON/JavaScript patterns (most reliable for modern sites)
        r'"price"\s*:\s*"?([1-9][0-9,]*(?:\.[0-9]{2})?)"?',
        r'"sellingPrice"\s*:\s*"?([1-9][0-9,]*(?:\.[0-9]{2})?)"?',
        r'"currentPrice"\s*:\s*"?([1-9][0-9,]*(?:\.[0-9]{2})?)"?',
        
        # HTML data attributes
        r'data-price[=\s]*["\']([1-9][0-9,]*(?:\.[0-9]{2})?)["\']',
        
        # Context-based patterns
        r'([1-9][0-9,]*(?:\.[0-9]{2})?)\s*(?:only|OFF)',
        r'(?:MRP|marked|Price)\s*:?\s*₹?\s*([1-9][0-9,]*(?:\.[0-9]{2})?)',
    ]
    
    print("Testing regex patterns...")
    print(f"Content: {test_content}")
    print("-" * 50)
    
    all_prices = []
    
    for i, pattern in enumerate(patterns):
        matches = re.findall(pattern, test_content, re.IGNORECASE | re.MULTILINE)
        print(f"Pattern {i+1}: {pattern}")
        print(f"  Matches: {matches}")
        
        for match in matches:
            price = parse_price(match)
            if price and 10 <= price <= 100000:
                all_prices.append({'price': price, 'pattern': i, 'match': match})
                print(f"  -> Valid price: ₹{price}")
        print()
    
    print(f"Total valid prices found: {len(all_prices)}")
    for p in all_prices:
        print(f"  ₹{p['price']} from pattern {p['pattern']+1} (match: '{p['match']}')")

if __name__ == "__main__":
    test_regex_patterns()