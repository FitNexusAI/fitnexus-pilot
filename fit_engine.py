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
            self.catalog.columns = self.catalog.columns.str.strip()
        try:
            self.catalog = pd.read_csv(data_file)
            # Clean up column names
            self.catalog.columns = self.catalog.columns.str.strip()
            # Clean up data cells
            self.catalog = self.catalog.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            logging.info(f"Successfully loaded {len(self.catalog)} products.")
        except Exception as e:
            logging.error(f"Could not load data: {e}")
            self.catalog = pd.DataFrame()

    def retrieve_products(self, query):
<<<<<<< HEAD
        if self.catalog.empty: return []
        
        query = query.lower().translate(str.maketrans('', '', string.punctuation))
        
        # SYNONYMS (Context Mapping)
        synonyms = {
            "sweatshirt": "hoodie", "pullover": "hoodie", "jumper": "hoodie",
            "tshirt": "tee", "shirt": "tee", "t-shirt": "tee",
            "pants": "leggings", "tights": "leggings", "socks": "accessories"
        }
        for word, target in synonyms.items():
            query = query.replace(word, target)

        # STOP WORDS (Hallucination Prevention)
        stop_words = {
            'the', 'a', 'an', 'and', 'is', 'are', 'in', 'on', 'about', 'tell', 'me', 'show', 
            'i', 'need', 'want', 'do', 'you', 'have', 'fit', 'does', 'how', 'looking', 'for', 
            'find', 'search', 'get', 'buy', 'purchase', 'recommend', 'what', 'where', 'when', 'why'
        }
        query_words = [w for w in query.split() if w not in stop_words]
        
        if not query_words: return []

        scored_results = []
        for index, row in self.catalog.iterrows():
            searchable_text = f"{row['name']} {row['name']} {row['category']} {row['description']}".lower()
=======
        """
        Search logic:
        1. Try to find specific product matches.
        2. If NO matches found, return the top 5 items anyway (General Recommendation Mode).
        """
        if self.catalog.empty: return []
        
        # 1. Prepare Query
        clean_query = query.lower().translate(str.maketrans('', '', string.punctuation))
        
        # 2. Handle Synonyms
        synonyms = {
            "sweatshirt": "hoodie", "pullover": "hoodie", 
            "tshirt": "tee", "shirt": "tee", 
            "pants": "leggings", "tights": "leggings"
        }
        for word, target in synonyms.items():
            clean_query = clean_query.replace(word, target)

        query_words = clean_query.split()
        
        # 3. Score Products based on Keywords
        scored_results = []
        for index, row in self.catalog.iterrows():
            # Create a big string of text for this product
            searchable_text = f"{row.get('name', '')} {row.get('category', '')} {row.get('description', '')}".lower()
            
            # Count how many query words appear in the product text
>>>>>>> b2deeec (Final demo build with scroll fix)
            score = sum(1 for word in query_words if word in searchable_text)
            if score > 0:
                scored_results.append((score, row))
        
<<<<<<< HEAD
        scored_results.sort(key=lambda x: x[0], reverse=True)
        return [item[1] for item in scored_results]

    def generate_response(self, user_input, product_data, user_profile):
        # NEW: We extract challenges safely
        challenges = ", ".join(user_profile.get('challenges', ['None']))
        
        system_prompt = (
            "You are FitNexus, an elite personal stylist. "
            "Your goal is to recommend the best size based on the USER'S PROFILE. "
            "1. Compare the product's 'fit_advice' against the user's stats.\n"
            "2. CRITICAL: Check their 'Fit Challenges'. "
            "If they have 'Broad Shoulders', warn them if an item is 'Slim' or 'Non-stretch'. "
            "If they have 'Long Torso', warn them if an item is 'Cropped' or standard length.\n"
            "3. Be specific and helpful."
=======
        # 4. Sort by Score
        scored_results.sort(key=lambda x: x[0], reverse=True)
        results = [item[1] for item in scored_results]

        # 5. FAIL-SAFE: If results are empty, just return the first 5 items
        # This allows GPT-4 to handle broad questions like "What do you suggest?"
        if not results:
            return [row for index, row in self.catalog.iterrows()][:5]

        return results

    def generate_response(self, user_input, product_data_list, user_profile):
        challenges = ", ".join(user_profile.get('challenges', ['None']))
        
        # Create a text summary of the products for the AI to read
        products_context = ""
        for i, prod in enumerate(product_data_list[:5]): # Only send top 5 to avoid token limits
            products_context += f"\nPRODUCT {i+1}: {prod.get('name')} | Fit: {prod.get('fit_type')} | Advice: {prod.get('fit_advice')}"

        system_prompt = (
            "You are FitNexus, an elite personal stylist. "
            "The user will ask a question. Use the PRODUCT DATA below to answer. "
            "If the user asks for a recommendation (e.g., 'What should I buy?'), look at their FIT CHALLENGES "
            "and pick the single best item from the list that solves their problem. "
            "Explain WHY it fits their specific body type."
>>>>>>> b2deeec (Final demo build with scroll fix)
        )

        user_message = (
            f"User Question: {user_input}\n\n"
            f"USER PROFILE:\n"
            f"- Height: {user_profile.get('height', 'Unknown')}\n"
            f"- Usual Size: {user_profile.get('size', 'Unknown')}\n"
<<<<<<< HEAD
            f"- Fit Preference: {user_profile.get('preference', 'Unknown')}\n"
            f"- Fit Challenges: {challenges}\n\n"
            f"PRODUCT DATA:\n"
            f"- Name: {product_data['name']}\n"
            f"- Fit Type: {product_data['fit_type']}\n"
            f"- Stretch: {product_data['stretch']}\n"
            f"- Manufacturer Advice: {product_data['fit_advice']}\n"
=======
            f"- Preference: {user_profile.get('preference', 'Unknown')}\n"
            f"- Challenges: {challenges}\n\n"
            f"AVAILABLE PRODUCTS TO CHOOSE FROM:\n{products_context}"
>>>>>>> b2deeec (Final demo build with scroll fix)
        )

        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
<<<<<<< HEAD
                messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_message}],
=======
                messages=[
                    {"role": "system", "content": system_prompt}, 
                    {"role": "user", "content": user_message}
                ],
>>>>>>> b2deeec (Final demo build with scroll fix)
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
<<<<<<< HEAD
            return f"Error: {e}"

    def think(self, user_input, user_profile={"size": "Unknown", "preference": "Standard"}):
        logging.info(f"User asked: {user_input}")
=======
            return f"Error connecting to AI: {e}"

    def think(self, user_input, user_profile):
        logging.info(f"User asked: {user_input}")
        
        # Get products (Specific matches OR Top 5 randoms)
>>>>>>> b2deeec (Final demo build with scroll fix)
        matches = self.retrieve_products(user_input)
        
        result = {"text": "", "image": None, "product_name": None}

        if not matches:
<<<<<<< HEAD
            result["text"] = "I couldn't find a specific product matching that description. I can help you with Leggings, Shorts, Tees, Sports Bras, Hoodies, or Socks."
        else:
            best_match = matches[0]
            result["text"] = self.generate_response(user_input, best_match, user_profile)
            img_url = best_match.get("image_url", None)
            if pd.notna(img_url) and str(img_url).strip() != "":
                result["image"] = str(img_url).strip()
            result["product_name"] = best_match["name"]
        
        self.memory.append({"role": "user", "content": user_input})
        self.memory.append({"role": "assistant", "content": result["text"]})
        
=======
            # This should basically never happen now due to the Fail-Safe
            result["text"] = "I'm having trouble accessing the catalog. Please try again."
        else:
            # Generate the advice
            result["text"] = self.generate_response(user_input, matches, user_profile)
            
            # Decide which image to show
            # If we found specific matches, show the first one.
            # If we are in "General Mode" (many matches), show the first one just as a visual anchor.
            best_match = matches[0]
            img_url = best_match.get("image_url", None)
            
            if pd.notna(img_url) and str(img_url).strip() != "":
                result["image"] = str(img_url).strip()
                result["product_name"] = best_match.get("name", "Recommended Item")
            
>>>>>>> b2deeec (Final demo build with scroll fix)
        return result