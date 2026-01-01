import logging
import os
import string
import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

class FitNexusAgent:
    def __init__(self, data_file="fashion_products_mock.csv"):
        self.name = "FitNexus"
        self.memory = []
        try:
            self.catalog = pd.read_csv(data_file)
            # 1. CLEAN THE HEADERS
            self.catalog.columns = self.catalog.columns.str.strip()
            # 2. CLEAN THE DATA (This fixes the broken image bug!)
            # It removes invisible spaces from every cell in the database
            self.catalog = self.catalog.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            
            logging.info(f"Successfully loaded {len(self.catalog)} products.")
        except Exception as e:
            logging.error(f"Could not load data: {e}")
            self.catalog = pd.DataFrame()

    def retrieve_products(self, query):
        if self.catalog.empty: return []
        query = query.lower().translate(str.maketrans('', '', string.punctuation))
        stop_words = {'the', 'a', 'an', 'and', 'is', 'are', 'in', 'on', 'about', 'tell', 'me', 'show', 'i', 'need', 'want', 'do', 'you', 'have'}
        query_words = [w for w in query.split() if w not in stop_words]
        
        scored_results = []
        for index, row in self.catalog.iterrows():
            searchable_text = f"{row['name']} {row['category']} {row['description']} {row['fit_type']}".lower()
            score = sum(1 for word in query_words if word in searchable_text)
            if score > 0:
                scored_results.append((score, row))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_results]

    def generate_response(self, user_input, product_data):
        system_prompt = "You are FitNexus, an expert fashion fit consultant. Use the provided PRODUCT DATA to answer. Be conversational but concise. Highlight fit details specifically."
        user_message = (
            f"User Question: {user_input}\n\n"
            f"PRODUCT DATA FOUND:\n"
            f"Name: {product_data['name']}\n"
            f"Fit Type: {product_data['fit_type']}\n"
            f"Stretch: {product_data['stretch']}\n"
            f"Expert Advice: {product_data['fit_advice']}\n"
            f"Description: {product_data['description']}"
        )
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error: {e}"

    def think(self, user_input):
        logging.info(f"User asked: {user_input}")
        matches = self.retrieve_products(user_input)
        
        result = {
            "text": "",
            "image": None,
            "product_name": None
        }

        if not matches:
            result["text"] = "I couldn't find a specific product matching that description. Could you be more specific?"
        else:
            best_match = matches[0]
            result["text"] = self.generate_response(user_input, best_match)
            # Get the image and ensure it's a clean string
            img_url = best_match.get("image_url", None)
            if pd.notna(img_url) and str(img_url).strip() != "":
                result["image"] = str(img_url).strip()
            
            result["product_name"] = best_match["name"]
        
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": result["text"]})
        
        return result