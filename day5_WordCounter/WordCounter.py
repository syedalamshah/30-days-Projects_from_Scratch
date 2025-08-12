import re
import json
import string
from collections import Counter
from datetime import datetime

class TextAnalyzer:
    def __init__(self):
        self.stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'have', 'has', 'had', 
            'this', 'that', 'it', 'you', 'i', 'he', 'she', 'we', 'they'
        }
    
    def clean_text(self, text):
        return text.lower().translate(str.maketrans('', '', string.punctuation))
    
    def get_words(self, text, min_len=1, skip_common=False):
        words = self.clean_text(text).split()
        if skip_common:
            words = [w for w in words if w not in self.stop_words]
        if min_len > 1:
            words = [w for w in words if len(w) >= min_len]
        return words
    
    def analyze(self, text, options=None):
        opts = options or {'min_length': 1, 'skip_common': False, 'top_words': 10}
        words = self.get_words(text, opts.get('min_length', 1), opts.get('skip_common', False))
        
        if not words:
            return self._empty_analysis(text)
        
        word_count = Counter(words)
        total_words = len(words)
        unique_words = len(word_count)
        avg_len = sum(len(w) for w in words) / total_words
        
        return {
            'chars': len(text),
            'chars_no_space': len(text.replace(' ', '')),
            'words': total_words,
            'unique_words': unique_words,
            'sentences': len([s for s in re.split(r'[.!?]+', text) if s.strip()]),
            'paragraphs': len([p for p in text.split('\n\n') if p.strip()]),
            'avg_word_len': round(avg_len, 2),
            'reading_min': round(total_words / 200, 2),
            'diversity': round(unique_words / total_words, 3),
            'top_words': word_count.most_common(opts.get('top_words', 10))
        }
    
    def _empty_analysis(self, text):
        return {
            'chars': len(text), 'chars_no_space': len(text.replace(' ', '')),
            'words': 0, 'unique_words': 0, 'sentences': 0, 'paragraphs': 0,
            'avg_word_len': 0, 'reading_min': 0, 'diversity': 0, 'top_words': []
        }
    
    def find_word(self, text, word):
        words = self.get_words(text)
        count = words.count(word.lower())
        total = len(words)
        return {
            'word': word,
            'count': count,
            'percentage': round((count / total * 100) if total else 0, 2)
        }
    
    def compare(self, text1, text2):
        stats1, stats2 = self.analyze(text1), self.analyze(text2)
        return {
            key: {'text1': stats1[key], 'text2': stats2[key], 
                  'diff': stats2[key] - stats1[key] if isinstance(stats1[key], (int, float)) else 'N/A'}
            for key in stats1 if key != 'top_words'
        }
    
    def word_lengths(self, text):
        lengths = [len(w) for w in self.get_words(text)]
        if not lengths:
            return {}
        
        return {
            'min': min(lengths),
            'max': max(lengths),
            'avg': round(sum(lengths) / len(lengths), 2),
            'distribution': dict(sorted(Counter(lengths).items()))
        }
    
    def save(self, data, filename=None):
        filename = filename or f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump({'analysis': data, 'created': datetime.now().isoformat()}, f, indent=2)
        return filename

def load_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_input():
    print("Enter text (type 'END' when done):")
    lines = []
    while True:
        line = input()
        if line.upper() == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)

def show_results(stats):
    print(f"\n{'='*40}")
    print("ANALYSIS RESULTS")
    print(f"{'='*40}")
    print(f"Characters: {stats['chars']:,}")
    print(f"Words: {stats['words']:,}")
    print(f"Unique: {stats['unique_words']:,}")
    print(f"Sentences: {stats['sentences']:,}")
    print(f"Paragraphs: {stats['paragraphs']:,}")
    print(f"Avg word length: {stats['avg_word_len']}")
    print(f"Reading time: {stats['reading_min']} min")
    print(f"Diversity: {stats['diversity']}")
    
    if stats['top_words']:
        print("\nTop words:")
        for i, (word, count) in enumerate(stats['top_words'][:5], 1):
            print(f"  {i}. {word} ({count})")

def show_comparison(comp):
    print(f"\n{'='*50}")
    print("COMPARISON")
    print(f"{'='*50}")
    
    for metric, data in comp.items():
        name = metric.replace('_', ' ').title()
        diff = f" ({data['diff']:+})" if data['diff'] != 'N/A' and data['diff'] != 0 else ""
        print(f"{name}: {data['text1']} vs {data['text2']}{diff}")

def main():
    analyzer = TextAnalyzer()
    
    print("Text Analyzer")
    print("-" * 20)
    
    menu = {
        '1': 'Analyze text', '2': 'Analyze file', '3': 'Compare texts',
        '4': 'Find word', '5': 'Word lengths', '6': 'Custom options', '7': 'Exit'
    }
    
    while True:
        print("\n" + "\n".join(f"{k}. {v}" for k, v in menu.items()))
        choice = input("\nChoice: ")
        
        if choice == '1':
            text = get_input()
            if text:
                show_results(analyzer.analyze(text))
        
        elif choice == '2':
            path = input("File path: ")
            text = load_file(path)
            if text:
                results = analyzer.analyze(text)
                show_results(results)
                if input("\nSave results? (y/N): ").lower() == 'y':
                    print(f"Saved to {analyzer.save(results)}")
        
        elif choice == '3':
            print("Text 1:")
            text1 = get_input()
            print("Text 2:")
            text2 = get_input()
            if text1 and text2:
                show_comparison(analyzer.compare(text1, text2))
        
        elif choice == '4':
            text = get_input()
            word = input("Word to find: ")
            if text and word:
                result = analyzer.find_word(text, word)
                print(f"\n'{result['word']}' appears {result['count']} times ({result['percentage']}%)")
        
        elif choice == '5':
            text = get_input()
            if text:
                stats = analyzer.word_lengths(text)
                if stats:
                    print(f"\nWord Length Analysis:")
                    print(f"Range: {stats['min']}-{stats['max']} chars")
                    print(f"Average: {stats['avg']} chars")
                    print("Distribution:")
                    for length, count in stats['distribution'].items():
                        print(f"  {length}: {count}")
        
        elif choice == '6':
            text = get_input()
            if text:
                min_len = int(input("Min word length (1): ") or "1")
                skip_common = input("Skip common words? (y/N): ").lower() == 'y'
                top_n = int(input("Top N words (10): ") or "10")
                
                options = {'min_length': min_len, 'skip_common': skip_common, 'top_words': top_n}
                show_results(analyzer.analyze(text, options))
        
        elif choice == '7':
            print("Goodbye!")
            break
        
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()