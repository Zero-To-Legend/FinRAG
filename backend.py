from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import openai
import logging
import faiss
import numpy as np
import requests
import os

# Load environment variables from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Set it in the .env file.")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI
app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load sentence transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Enhanced financial knowledge base
knowledge_base = [
    "Stocks represent ownership in a company and provide potential for capital gains and dividends.",
    "Bonds are fixed-income investments that pay regular interest and return the principal at maturity.",
    "A mutual fund pools money from investors to purchase a diversified portfolio of stocks, bonds, or other assets.",
    "ETFs (Exchange-Traded Funds) trade like stocks but track an index, commodity, or sector, offering diversification and liquidity.",
    "The Federal Reserve influences interest rates to control inflation and stabilize the economy. As of March 2025, the Fed maintained the target range for the federal funds rate at 4.25% to 4.5%.",
    "Cryptocurrencies, such as Bitcoin and Ethereum, are highly volatile and speculative investments. As of April 7, 2025, Bitcoin is priced at approximately $78,000 USD, and Ethereum at approximately $1,540 USD. Risks include regulatory changes, security breaches, and market manipulation.",
    "Real estate investments can provide rental income and appreciation but require significant capital and carry risks like market fluctuations and property management challenges.",
    "Edmonton's real estate market has shown significant growth, with average residential prices reaching $460,685 in March 2025, reflecting a 2.5% increase from February and a 9.3% year-over-year rise.",
    "Diversification is a key strategy to reduce risk by spreading investments across different asset classes, sectors, and geographies.",
    "Inflation erodes purchasing power over time, making it important to invest in assets that outpace inflation, such as stocks or real estate.",
    "Retirement accounts like RRSPs (Registered Retirement Savings Plans) in Canada offer tax advantages for long-term savings. The RRSP contribution limit for 2025 is 18% of your 2024 earned income, up to a maximum of $32,490.",
    "The TSX (Toronto Stock Exchange) is Canada's primary stock exchange, featuring many energy and mining companies due to the country's resource-rich economy. In 2025, mining companies dominated the TSX Venture 50 list, with 31 out of 50 companies from the mining sector.",
    "Investors should assess their risk tolerance, investment horizon, and financial goals before making investment decisions.",
    "Cryptocurrency investments are not insured by government agencies like the Canada Deposit Insurance Corporation (CDIC), making them riskier than traditional bank deposits.",
    "Edmonton's economy is diversifying, with growth in sectors like technology, healthcare, and renewable energy, alongside its traditional oil and gas industry. The federal government announced over $6.7 million in investments for Edmonton companies in February 2025 to support this diversification.",
    "Edmonton's financial services sector is expanding, with a focus on fintech startups, credit unions, and sustainable finance. The city is seeing increased support for green bonds and ESG-focused investment funds.",
    "ATB Financial, headquartered in Edmonton, plays a major role in Alberta’s financial ecosystem, offering personal and business banking services, as well as investing heavily in AI and digital banking platforms.",
    "Credit unions like Servus Credit Union, also based in Edmonton, are providing more accessible financial products and services, contributing to local economic resilience.",
    "The Edmonton Metropolitan Region is promoting financial innovation through incubators like Startup Edmonton and Alberta Innovates, supporting early-stage ventures in finance, AI, and data analytics.",
    "Edmonton's financial literacy programs, supported by the City and nonprofits, aim to improve household budgeting, saving, and responsible investing, especially among young adults and newcomers."
]

# Dynamic Data Fetching Functions
def fetch_and_append_dynamic_data():
    dynamic_data = []

    def try_fetch(fetch_fn, label):
        try:
            result = fetch_fn()
            dynamic_data.append(f"{label}: \n{result}")
        except Exception as e:
            logger.error(f"Failed to fetch {label}: {e}")

    try_fetch(fetch_property_assessment_data, "Recent Edmonton Property Assessments")
    try_fetch(fetch_affordable_housing_data, "Affordable Housing Availability")
    try_fetch(fetch_senior_mgmt_expenses, "Senior Management Expenses")
    try_fetch(fetch_household_spending_survey, "Household Spending Trends")
    try_fetch(fetch_tax_perception_survey, "Tax Perception Insights")

    return dynamic_data

# Fetch and encode embeddings on startup
@app.on_event("startup")
def initialize_knowledge():
    logger.info("Initializing knowledge base with dynamic Edmonton data...")
    dynamic_entries = fetch_and_append_dynamic_data()
    knowledge_base.extend(dynamic_entries)

    global kb_embeddings, index
    kb_embeddings = np.array([model.encode(text) for text in knowledge_base])
    index = faiss.IndexFlatL2(kb_embeddings.shape[1])
    index.add(kb_embeddings)
    logger.info("Knowledge base and FAISS index initialized.")

# API Request Schema
class QueryRequest(BaseModel):
    query: str

# System prompt for OpenAI
SYSTEM_PROMPT = """
You are a financial assistant designed to provide reliable, accurate, and actionable financial advice. Your responses are based on a comprehensive financial knowledge base, which includes information on stocks, bonds, mutual funds, ETFs, cryptocurrencies, real estate, retirement planning, and economic trends relevant to regions like Edmonton, Canada.

**Guidelines:**
1. **Strictly Financial Focus**: Answer questions only related to finance, investments, and economic trends. If a question falls outside this scope, politely decline to answer.
2. **Knowledge-Based Responses**: Provide answers strictly based on the retrieved knowledge from the financial database. Do not speculate or provide opinions.
3. **Risk Awareness**: Highlight potential risks associated with investments, especially for volatile assets like cryptocurrencies.
4. **Local Context**: When relevant, include insights specific to regions like Edmonton, such as real estate trends or economic diversification.
5. **Developer Information**: If asked about the developers, provide the following details:
   - Developed by: Ruban Gino Singh A, Raja Priya M, and Raju B on behalf of MM802 Multimedia Communications project.

**Examples of Appropriate Questions:**
- "What are the risks of investing in cryptocurrencies?"
- "How does the Federal Reserve influence interest rates?"
- "What is the current trend in Edmonton's real estate market?"
- "How can I diversify my investment portfolio?"

**Examples of Inappropriate Questions:**
- "What is the best restaurant in Edmonton?" (Not financial-related)
- "Can you help me with my math homework?" (Outside the scope of finance)

**Note**: Always maintain a professional tone, and ensure your responses are clear, concise, and tailored to the user's query.
"""

# Chat Route
@app.post("/chat/")
async def chat(query_request: QueryRequest):
    query = query_request.query
    query_embedding = model.encode(query).reshape(1, -1)
    D, I = index.search(query_embedding, k=2)
    retrieved_texts = [knowledge_base[i] for i in I[0] if i >= 0]

    if not retrieved_texts:
        return {"response": "I'm sorry, I couldn't find any relevant financial information for your question."}

    prompt = f"{SYSTEM_PROMPT}\n\nRetrieved Information:\n" + "\n".join(retrieved_texts) + f"\n\nUser Question: {query}\nAnswer:"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=150,
            temperature=0.5,
        )
        answer = response['choices'][0]['message']['content'].strip()
        return {"response": answer}

    except openai.error.OpenAIError as e:
        logger.error(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")


# Dynamic Knowledge Fetchers
def fetch_property_assessment_data(limit=5):
    url = f"https://data.edmonton.ca/resource/q7d6-ambg.json?$limit={limit}"
    data = requests.get(url).json()
    return "\n".join([
        f"Address: {d.get('address', 'N/A')}, Assessed Value: ${d.get('assessed_value', 'N/A')}" for d in data
    ])

def fetch_affordable_housing_data(limit=5):
    url = f"https://data.edmonton.ca/resource/whar-nsyh.json?$limit={limit}"
    data = requests.get(url).json()
    return "\n".join([
        f"Neighbourhood: {d.get('neighbourhood', 'N/A')}, Type: {d.get('type_of_housing', 'N/A')}, Units: {d.get('number_of_units', 'N/A')}" for d in data
    ])

def fetch_senior_mgmt_expenses(limit=5):
    url = f"https://data.edmonton.ca/resource/ihuy-w3s8.json?$limit={limit}"
    data = requests.get(url).json()
    return "\n".join([
        f"{d.get('employee_name', 'N/A')} spent ${d.get('amount', 'N/A')} on {d.get('expense_category', 'N/A')} in {d.get('year', 'N/A')}" for d in data
    ])

def fetch_household_spending_survey(limit=5):
    url = f"https://data.edmonton.ca/resource/2crc-aced.json?$limit={limit}"
    data = requests.get(url).json()
    return "\n".join([
        f"{d.get('category', 'N/A')}: Average Spend = ${d.get('average_spend', 'N/A')}" for d in data
    ])

def fetch_tax_perception_survey(limit=5):
    url = f"https://data.edmonton.ca/resource/87u8-3yfv.json?$limit={limit}"
    data = requests.get(url).json()
    return "\n".join([
        f"{d.get('statement', 'N/A')}: {d.get('response', 'N/A')} ({d.get('percentage', 'N/A')}%)" for d in data
    ])
