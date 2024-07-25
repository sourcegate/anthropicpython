from flask import Flask, request, render_template_string, jsonify
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

CLAUDE_API_KEY = os.getenv('CLAUDE_API_KEY')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Campaign Concept Generator</title>
    <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px; 
            background-color: #f0f0f0;
        }
        h1 { 
            color: #333; 
            text-align: center;
        }
        .form-container {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        input, button { 
            width: 100%;
            margin: 10px 0; 
            padding: 10px; 
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        button {
            background-color: #4CAF50;
            color: white;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s;
        }
        button:hover {
            background-color: #45a049;
        }
        #response { 
            white-space: pre-wrap; 
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <h1>DS Campaign Concept Generator alpha 1.0</h1>
    <div class="form-container">
        <input id="productService" placeholder="Enter product or service">
        <input id="targetAudience" placeholder="Enter target audience">
        <button onclick="generateConcept()">Generate Campaign Concept</button>
    </div>
    <div id="response"></div>

    <script>
    async function generateConcept() {
        const productService = document.getElementById('productService').value;
        const targetAudience = document.getElementById('targetAudience').value;
        const responseDiv = document.getElementById('response');
        responseDiv.innerHTML = 'Generating concept...';

        try {
            const response = await axios.post('/generate_concept', {
                productService: productService,
                targetAudience: targetAudience
            });
            responseDiv.innerHTML = response.data.concept;
        } catch (error) {
            responseDiv.innerHTML = 'An error occurred: ' + error.message;
        }
    }
    </script>
</body>
</html>
'''


@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)


@app.route('/generate_concept', methods=['POST'])
def generate_concept():
    data = request.json
    product_service = data['productService']
    target_audience = data['targetAudience']

    prompt = f'''
    You are a world-class ideation and creative director expert. You have won every possible award as an ad and creative agency. Your task is to generate a new campaign concept for a given product or service targeted at a specific audience. Your ideas should be groundbreaking and innovative, not trite or commonplace. Every time this prompt is run you generate a fresh and new idea and set of ideas that are never the same twice.

    You will be provided with a few key inputs and you should groq and understand them all:
    <Product_Service>
    {product_service}
    </Product_Service>
    <Target_Audience>
    {target_audience}
    </Target_Audience>

    Research and pull Relevant upcoming trends and things in the future to consider in your ideation process
    <research>
    [output your research here with stats, real citations, and why I should care]
    </research>

    In your idea consider our target audience and shift and tweak your vibe and language frame usage to consider them.

    Follow these steps to create your campaign concept:

    Insight Identification:
    - Identify a clear problem statement related to the product/service and target audience.
    - Describe the emotional and functional impacts of this problem.

    Concept Insight:
    - Create a relatable metaphor or analogy that connects emotionally with the audience.
    - Clearly state the key benefit or unique selling proposition of the product/service.

    Concept Write-Up:
    - Write a detailed narrative explaining how the product/service solves the problem.
    - Include vivid descriptions and relatable scenarios.
    - End with a clear call to action.

    How It Comes to Life:
    - Provide practical examples of how the concept can be implemented across different channels.
    - Suggest creative ways to execute the campaign.

    Next Steps:
    - Outline an action plan for executing the campaign.

    Instantiate multiple agents and top leaders competing to find the most creative and strategic hard hitting campaign that will not only be breakthrough advertising and creative but also drive impact and growth for the client. These agents will dialogue, ideate poke holes in each other's answer until they agree, which they all loathe to do. Each agent has unique skills and perspective and thinks about the problem from different vantage points. But ultimately they come up with the best idea that will help their clients GROW and deliver the most authentic value and truth for the end ICPs.

    - Agent 1: Top-down agent
    - Agent 2: Bottom-up agent

    Other agents:
    •  Pete Sena - Founder Digital Surgeons
    •  Colin Selikow - Executive Creative Director at DDB Chicago
    • Lorenz Langgartner - Executive Creative Director at Serviceplan Group
    • Franz Röppischer - Executive Creative Director at Serviceplan Group
    • Andrey Tyukavkin - Executive Creative Director at Publicis Italy
    • Daniel Fisher - Executive Creative Director at Ogilvy
    • David Lubars - Chief Creative Officer at BBDO New York
    • Greg Hahn - Chief Creative Officer at BBDO New York
    • Sean Bryan - Chief Creative Officer at McCann New York
    • Tom Murphy - Chief Creative Officer at McCann New York
    • Sam Shepherd - Executive Creative Director at Leo Burnett Chicago
    • Marie Claire Maalouf - Executive Creative Director at Impact BBDO
    • Christophe Everke - Executive Creative Director at Serviceplan
    • Jason LaFlore - Creative Director at 72andSunny
    • Daniel Correa - Creative Director at Alma
    • Bruno Trad - Creative Director at Alma
    • PG Aditiya - Creative Director at Talented
    • Liz Taylor - Global Chief Creative Officer at Ogilvy
    • Lucy Jameson - Consistently ranked as one of the top account planners
    • David Golding - Highly regarded in the industry, appearing in top rankings
    • Craig Mawdsley and Bridget Angear - Often mentioned as a duo, ranking highly in planner lists
    • Laurence Green - Recognized as a top account planner
    • Richard Huntington - Featured in top account planner rankings
    • Jason Gonsalves and Jonathan Bottomley - Another duo noted for their strategic expertise
    • John Lowery - Mentioned in top account planner lists
    • Dylan Williams - Recognized for his strategic planning skills
    • Charlie Snow - Noted as a top account planner
    • Giles Hedger - Featured in rankings of top planners

    All agents:
    - Excellent at the ability to think counterfactually, think step by step, think from first principles, think laterally, think about second-order implications, are highly skilled at simulating in their mental model and thinking critically before answering, having looked at the problem from many directions.

    Output that dialogue and discourse. Each agent must give their top 2 favorite headlines and pitch a creative idea.

    Output all the headlines in a single bulleted list.

    <scratchpad> </scratchpad>

    The group will then agree on the most creative and breakthrough idea that will grow the clients business and resonate with the core customer

    Generate a comprehensive campaign concept that includes:
    1. A catchy campaign slogan
    2. Key messaging points
    3. Proposed visual elements or imagery
    4. Suggested channels for promotion (e.g., social media, TV, print)
    5. A brief outline of the campaign story or narrative

    Be creative, bold, and make sure the concept resonates with the target audience while effectively promoting the product or service.
    '''

    try:
        response = requests.post(
            'https://api.anthropic.com/v1/messages',
            json={
                'model': 'claude-3-sonnet-20240229',
                'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 4000
            },
            headers={
                'Content-Type': 'application/json',
                'x-api-key': CLAUDE_API_KEY,
                'anthropic-version': '2023-06-01'
            }
        )
        response.raise_for_status()
        concept = response.json()['content'][0]['text']
        return jsonify({'concept': concept})
    except requests.RequestException as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
