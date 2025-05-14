import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load the same embedding model as in the backend
model = SentenceTransformer("all-MiniLM-L6-v2")

# Test questions
test_questions = [
    "What are the risks of investing in Bitcoin?",
    "Tell me about the interest rate set by the Federal Reserve.",
    "What is the current trend in Edmonton’s housing market?",
    "Can I invest in mutual funds for retirement?",
    "How does inflation affect my savings?",
    "What role does ATB Financial play in Alberta’s economy?",
    "Are ETFs a safe investment?",
    "What’s the TSX and what type of companies are listed?",
    "How much can I contribute to my RRSP in 2025?",
    "What initiatives support financial innovation in Edmonton?"
]

# FastAPI backend URL
API_URL = "http://localhost:8000/chat/"

# Knowledge base (same as backend)
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

# Function to call chatbot
def get_chatbot_response(query):
    try:
        response = requests.post(API_URL, json={"query": query})
        return response.json().get("response", "")
    except Exception as e:
        return f"Error: {e}"

# Evaluation loop
records = []
similarities = []

for q in test_questions:
    response = get_chatbot_response(q)
    resp_vec = model.encode(response).reshape(1, -1)

    kb_vecs = [model.encode(kb).reshape(1, -1) for kb in knowledge_base]
    sims = [cosine_similarity(resp_vec, kb_vec)[0][0] for kb_vec in kb_vecs]
    best_idx = int(np.argmax(sims))

    best_match = knowledge_base[best_idx]
    sim_score = round(float(sims[best_idx]), 4)

    records.append({
        "Question": q,
        "Chatbot Response": response,
        "Best Match": best_match,
        "Similarity": sim_score
    })
    similarities.append(sim_score)

# Save to CSV
df = pd.DataFrame(records)
df.to_csv("chatbot_eval_results.csv", index=False)

# 📊 Plot 1: Per-Question Similarity
plt.figure(figsize=(12, 6))
bars = plt.bar(range(len(test_questions)), similarities, tick_label=[f"Q{i+1}" for i in range(len(test_questions))])
plt.ylim(0, 1.05)
plt.xlabel("Test Questions")
plt.ylabel("Cosine Similarity Score")
plt.title("Chatbot Answer Accuracy vs Knowledge Base")

# Annotate similarity scores
for bar, score in zip(bars, similarities):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.01, f"{score:.2f}", ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.show()

# 📊 Plot 2: Average Similarity Score
average_score = round(np.mean(similarities), 4)

plt.figure(figsize=(6, 4))
bar = plt.bar(["Average Similarity"], [average_score], color="skyblue")
plt.ylim(0, 1.05)
plt.title("Average Similarity Score Across All Questions")
plt.ylabel("Cosine Similarity")

# Annotate the average
plt.text(0, average_score + 0.02, f"{average_score:.2f}", ha='center', va='bottom', fontsize=12, fontweight='bold')

plt.tight_layout()
plt.show()
