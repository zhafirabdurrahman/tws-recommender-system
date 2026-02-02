<div align="center">
  <img src="img.png" alt="SoundScout Logo" width="200" style="margin-bottom: 0px;">
  <h1 style="margin-top: 0px;">SoundScout</h1>
  <p><i>Navigate the Noise, Find Your Perfect Sound</i></p>
</div>

[Find Your Perfect Sound Here!](https://huggingface.co/spaces/zikosetyawan/soundscout-app)  
---

## 📌 Program Description
**SoundScout** is a True Wireless Stereo (TWS) product recommendation system designed to help users discover the most suitable TWS based on their needs and preferences. This system leverages customer review analysis using Natural Language Processing (NLP) techniques to generate relevant, informative recommendations that support more efficient and confident purchasing decisions.

## 📖 Problem Background
The rapid adoption of True Wireless Stereo (TWS) devices has been driven by digital lifestyle changes that demand high mobility, along with smartphone manufacturers gradually removing physical audio jacks. As a result, TWS devices have become an essential necessity, offering cable-free convenience, voice assistant integration, and productivity-enhancing features such as noise cancellation—making them a top choice for both work and entertainment.

However, this surge in demand has led to an overwhelming number of models and brands in the market. Consumers often struggle to choose products that match their sound quality expectations and comfort preferences among thousands of available options.

To address this challenge, this project develops a recommendation system that focuses on extracting insights from user reviews using Natural Language Processing (NLP) techniques, specifically the Word2Vec model. Customer reviews are chosen as the primary data source because they capture real-world user experiences that go beyond technical specifications. Through word embedding, Word2Vec is able to understand semantic context and relationships between words, allowing the system to identify product similarities based on sentiment and experiential descriptions. This approach aims to deliver more accurate and personalized TWS recommendations, helping users navigate a saturated market using collective user experiences.

## 🎯 Project Objective
Based on the identified problems, the objectives of this project are:

- **Recommendation System Development**: To build a recommendation application that helps users select TWS products aligned with their usage needs, preferences, and desired specifications.
- **Personalization & Review Summarization**: To provide **Top 3** most relevant TWS recommendations, accompanied by summarized product reviews derived from previous purchasing and usage experiences.
- **Insights for Manufacturers**: To deliver actionable insights for TWS brands or manufacturers regarding potential product improvement opportunities based on sentiment and opinion analysis.
- **Marketing Strategy Efficiency**: To support more efficient marketing strategies by helping brands reduce *Cost Per Acquisition* (CPA) and accelerate consumer decision-making processes.

## 📊 Dataset Information
The dataset was collected through a *web scraping* process using **BeautifulSoup4**. Raw data was validated and cleaned to ensure high-quality features for modeling.

| Column Name | Data Type | Description |
| :--- | :--- | :--- |
| `product` | String | Full name of the TWS product |
| `feature` | String | Description of technical features |
| `brand` | String | Product brand or manufacturer |
| `price` | Float | Product price |
| `rating` | Float | User rating score |
| `color` | String | Available color variants |
| `ear_placement` | String | Ear-wearing style (e.g., In-Ear, Semi-In-Ear) |
| `form_factor` | String | Physical form factor (e.g., True Wireless) |
| `impedance` | String | Electrical resistance of the audio circuit (Ohm) |
| `image_url` | String | Link to product image for visualization |
| `reviews` | String | Aggregated user reviews for sentiment/context analysis |

## 🛠️ Technology Stack & Libraries
This project is built using **Python** as the primary language, supported by the following ecosystem of libraries:

| No | Library | Function |
| :--- | :--- | :--- |
| 1 | **Pandas** | Data manipulation and tabular processing |
| 2 | **NumPy** | Numerical computation and array operations |
| 3 | **Seaborn** | Statistical data visualization |
| 4 | **WordCloud** | Visualization of frequently occurring words |
| 5 | **NLTK** | Text preprocessing for NLP |
| 6 | **Scikit-learn** | Machine learning model development |
| 7 | **Gensim** | Word2Vec vectorization |
| 8 | **Streamlit** | Application interface and deployment |
| 9 | **ScraperAPI** | API integration to bypass scraping protection |
| 10 | **BeautifulSoup4** | Web scraping |

**Supporting Tools:**
- **VS Code**: Primary code editor
- **Hugging Face**: Platform for model deployment
- **Tableau**: Interactive and advanced data visualization

## 📊 Data Pipeline & Methodology
1. **Data Acquisition**: Scraping TWS product data from Amazon e-commerce.
2. **Data Cleaning & Validation**:
   - Standardizing product feature naming
   - Removing duplicate records
   - Creating a new `feature` column by splitting product names
   - Generating review datasets for modeling
   - Data validation using Great Expectations
3. **Exploratory Data Analysis (EDA)**: Analysis of price distribution, top brands, and average ratings.
4. **Modeling**:
   - Text representation of product features using **Word2Vec**
   - Measuring product similarity using *Cosine Similarity*
5. **Recommendation**: Displaying the top 3 most relevant products based on similarity to user preference inputs.

## 📊 Project Output
- [SoundScout Tableau Dashboard](https://public.tableau.com/app/profile/ivan.carlos.tambunan/viz/SoundScout/SoundScoutDashboard?publish=yes)  
- [SoundScout App](https://huggingface.co/spaces/zikosetyawan/soundscout-app)

## 📂 Project Structure
```text
├── deployment/               # Files for Hugging Face deployment
├── data_scraped/             # Scraped JSON data
├── scrape_and_cleaning/      # Data cleaning and validation scripts
├── EDA.ipynb                 # Exploratory Data Analysis notebook
├── modeling.ipynb            # Word2Vec & recommendation modeling
└── README.md                 # Project documentation
