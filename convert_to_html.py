import re

# Read the markdown file
with open('presentation.md', 'r', encoding='utf-8') as f:
    content = f.read()

# Extract YAML frontmatter
yaml_match = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
if yaml_match:
    content = content[yaml_match.end():]

# Split by slide separators
slides = content.split('\n---\n')

# Convert markdown to HTML
def md_to_html(text):
    # Headers
    text = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', text, flags=re.MULTILINE)
    text = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', text, flags=re.MULTILINE)
    text = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', text, flags=re.MULTILINE)
    
    # Bold
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    
    # Code blocks
    text = re.sub(r'`(.*?)`', r'<code>\1</code>', text)
    
    # Lists
    lines = text.split('\n')
    result = []
    in_list = False
    
    for line in lines:
        if line.strip().startswith('- '):
            if not in_list:
                result.append('<ul>')
                in_list = True
            item = line.strip()[2:]
            # Handle nested lists
            if line.startswith('  - '):
                item = line.strip()[2:]
                result.append(f'  <li style="margin-left: 20px;">{item}</li>')
            else:
                result.append(f'  <li>{item}</li>')
        else:
            if in_list:
                result.append('</ul>')
                in_list = False
            if line.strip() and not line.strip().startswith('<'):
                result.append(f'<p>{line}</p>')
            else:
                result.append(line)
    
    if in_list:
        result.append('</ul>')
    
    return '\n'.join(result)

# Generate HTML
html_content = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAP 연계 FTA 원산지 판정 시뮬레이터</title>
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
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .presentation-container {
            max-width: 1200px;
            width: 100%;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            overflow: hidden;
        }
        
        .slide {
            display: none;
            padding: 60px 80px;
            min-height: 600px;
            animation: fadeIn 0.5s;
        }
        
        .slide.active {
            display: block;
        }
        
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        
        .slide.lead.active {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            text-align: center;
        }
        
        h1 {
            font-size: 3em;
            margin-bottom: 20px;
            color: #2d3748;
        }
        
        .slide.lead h1 {
            color: white;
        }
        
        h2 {
            font-size: 2em;
            margin-bottom: 15px;
            color: #4a5568;
        }
        
        .slide.lead h2 {
            color: rgba(255, 255, 255, 0.9);
        }
        
        h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
            color: #718096;
        }
        
        .slide.lead h3 {
            color: rgba(255, 255, 255, 0.8);
        }
        
        p {
            font-size: 1.1em;
            line-height: 1.6;
            margin-bottom: 15px;
            color: #4a5568;
        }
        
        ul {
            margin-left: 30px;
            margin-bottom: 20px;
        }
        
        li {
            font-size: 1.1em;
            line-height: 1.8;
            margin-bottom: 10px;
            color: #4a5568;
        }
        
        strong {
            color: #667eea;
            font-weight: 600;
        }
        
        code {
            background: #f7fafc;
            padding: 2px 8px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e53e3e;
        }
        
        .controls {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 20px 40px;
            background: #f7fafc;
            border-top: 2px solid #e2e8f0;
        }
        
        .btn {
            padding: 12px 30px;
            background: #667eea;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1em;
            transition: all 0.3s;
        }
        
        .btn:hover {
            background: #5a67d8;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        
        .btn:disabled {
            background: #cbd5e0;
            cursor: not-allowed;
            transform: none;
        }
        
        .slide-counter {
            font-size: 1em;
            color: #718096;
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="presentation-container">
'''

# Add slides
for i, slide in enumerate(slides):
    slide = slide.strip()
    if not slide:
        continue
    
    is_lead = i == 0 or '<!-- _class: lead -->' in slide
    slide = slide.replace('<!-- _class: lead -->', '')
    
    class_name = 'slide lead' if is_lead else 'slide'
    active = 'active' if i == 0 else ''
    
    html_content += f'        <div class="{class_name} {active}" data-slide="{i}">\n'
    html_content += md_to_html(slide)
    html_content += '        </div>\n'

# Add controls and JavaScript
html_content += '''        <div class="controls">
            <button class="btn" id="prevBtn" onclick="changeSlide(-1)">← 이전</button>
            <span class="slide-counter">
                <span id="currentSlide">1</span> / <span id="totalSlides"></span>
            </span>
            <button class="btn" id="nextBtn" onclick="changeSlide(1)">다음 →</button>
        </div>
    </div>
    
    <script>
        let currentSlide = 0;
        const slides = document.querySelectorAll('.slide');
        const totalSlides = slides.length;
        
        document.getElementById('totalSlides').textContent = totalSlides;
        
        function showSlide(n) {
            slides[currentSlide].classList.remove('active');
            currentSlide = (n + totalSlides) % totalSlides;
            slides[currentSlide].classList.add('active');
            
            document.getElementById('currentSlide').textContent = currentSlide + 1;
            document.getElementById('prevBtn').disabled = currentSlide === 0;
            document.getElementById('nextBtn').disabled = currentSlide === totalSlides - 1;
        }
        
        function changeSlide(direction) {
            showSlide(currentSlide + direction);
        }
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') changeSlide(-1);
            if (e.key === 'ArrowRight') changeSlide(1);
        });
        
        // Initialize
        showSlide(0);
    </script>
</body>
</html>
'''

# Write HTML file
with open('presentation.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("✅ HTML 프레젠테이션이 성공적으로 생성되었습니다: presentation.html")
