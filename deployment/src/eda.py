import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import nltk
nltk.download("punkt_tab")

def run_eda():
    st.subheader("Exploratory Data Analysis (EDA)")
    
    # Load data
    df = pd.read_csv("./src/data_cleaned.csv")
    ds = pd.read_csv("./src/review_data_labeled.csv")
    
    # Tabs
    tabs = st.tabs(["Dataset","EDA Product","EDA Review"])

    with tabs[0]:
        st.write("### Preview Dataset Product")
        st.dataframe(df.head(10))
        st.write(('### Preview Dataset Review'))
        st.dataframe(ds.head(10))
    
    with tabs[1]:
        # Standardize 'form_factor' entries
        df['form_factor'] = df['form_factor'].replace({
            'Open ear': 'Open Ear',
            'open ear': 'Open Ear',
            'Open Ear earbuds /Over the ear earbuds': 'Open/Over Ear Earbuds'})
        
        # Visualisasi distribusi tiap kolom numeric
        st.markdown("## 1. Numeric Columns Distribution")
        num_col = ('price', 'rating')

        fig, axes = plt.subplots(1, 2, figsize=(12, 6))
        plt.suptitle('Price and Rating Distribution', fontsize=20)
        axes = axes.flatten()

        for i, col in enumerate(num_col):
            sns.histplot(df[col], 
                        kde=True, 
                        ax=axes[i])
            axes[i].set_title(f"Distribution of {col}")
            
        plt.tight_layout()
        
        st.pyplot(fig)

        with st.expander("**Insight**"):
                st.markdown("""
                            Based on this plot, we can see how the distribution both of the features. Price has a skewed distribution where there are some outlier where headphone with a high price and small amount, usually a pricy headphone with high performance or even luxury.  
                            For Ratings, it is normally distributed where the median is around 4.25 score, where we can decide that it is a positive sentiments score review for bunch of the products that shows the group of these products has a good and decent performance based on review score alone.
                            """)
        
        st.markdown("## 2. Ear Placemenet Distribution")
        fig = plt.figure(figsize=(7, 7))
        plt.pie(
            df['ear_placement'].value_counts().values,
            labels=df['ear_placement'].value_counts().index,
            autopct='%1.1f%%',
            startangle=180,
            labeldistance=1.1,
            pctdistance=0.75,
            wedgeprops={'edgecolor': 'white', 'linewidth': 0.5},
            colors=sns.color_palette('Set2')
        )
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        plt.gca().add_artist(centre_circle)
        plt.title('Ear Placement Distribution')
        plt.axis('equal')
        st.pyplot(fig)

        with st.expander("**Insight**"):
                st.markdown("""
                            Based on this chart, most of the headphone product has the Ear Placement type as In Ear and small amount on any other type.  
                            Based on this we also find that most popular product with In Ear placement, as more its requested, more its produced and improved based on this type.
                            """)
        
        st.markdown("## 3. Form Factor Distribution")
        fig = plt.figure(figsize=(7, 7))
        plt.pie(
            df['form_factor'].value_counts().values,
            labels=df['form_factor'].value_counts().index,
            autopct='%1.1f%%',
            startangle=180,
            labeldistance=1.1,
            pctdistance=0.75,
            wedgeprops={'edgecolor': 'white', 'linewidth': 0.5},
            colors=sns.color_palette('Set2')
        )
        centre_circle = plt.Circle((0, 0), 0.50, fc='white')
        plt.gca().add_artist(centre_circle)
        plt.title('Form Factor Distribution')
        plt.axis('equal')
        st.pyplot(fig)

        with st.expander("**Insight**"):
                st.markdown("""
                            Based on this chart, the most form factor of this product also In Ear type, we can also assume that this type of product is the most popular and demanded product.  
                            In Ear form factor still uses wire also very light easy to carry, and with or without earbuds as comfort in ear.
                            """)
        
        st.markdown("## 4. Top Color Distribution")
        # Distribution by Top 10 Color

        top_colors = df['color'].value_counts().nlargest(10)
        top_colors_names = top_colors.index

        fig = plt.figure(figsize=(10, 6))
        sns.countplot(data=df[df['color'].isin(top_colors_names)],
                    x='color',
                    dodge=False,
                    order=top_colors_names,
                    edgecolor='black',
                    linewidth=0.5,
                    palette=['#120B0B', '#F2FAFA', '#224EDD', '#EB9D44', '#E3E3E3', 
                                '#8F21DE', '#1BB542', '#656C65', '#80D5E8', '#F2A2D7'])
        plt.title('Distribution by Color Popularity')
        plt.xlabel('Color')
        plt.ylabel('Count')
        plt.xticks(rotation=20)
        plt.grid(axis='y', linestyle='--', alpha=0.3)
        st.pyplot(fig)
        
        with st.expander("**Insight**"):
                st.markdown("""
                            Most of the product are colored Black and White, which is very common because these are neutral color which is very popular because less tied to fashion trends and universally acceptable, which is why manufacturer priotize to product to appeal to the mass and only small niche number of people to use colored ones.
                            """)
                
        st.markdown("## 5. Top 10 Brands by Average Price")
        # Top 10 Brands by Average Price
        average_price = (df
                        .groupby('brand')['price']
                        .mean()
                        .reset_index()
                        .sort_values(by='price', ascending=False)
                        .head(10))
        average_price.rename(columns={'price': 'average_price'}, inplace=True)

        # Visualization of Top 10 Brands by Average Price
        fig = plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=average_price,
                        x='average_price', 
                        y='brand', 
                        hue='brand', 
                        palette='Set3',
                        dodge=False)

        plt.title('Top 10 Brands by Average Price', fontsize=16)
        plt.xlabel('Average Price ($)')
        plt.ylabel('Brand')
        plt.grid(axis='x', linestyle='--', alpha=0.4)

        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f'{width:.2f}',
                        xy=(width - 0.05*width, p.get_y() + p.get_height()/2),
                        ha='right',
                        va='center',
                        color='black',
                        fontsize=10)
        st.pyplot(fig)
        with st.expander("**Insight**"):
                st.markdown("""
                            Bose and Sennheiser brands have a high average price doubling the average medium price, for a headphone shows that these are premium and high-end headphone product if compared with other product as these price reflects their brand equity and sound quality. Consumers might go for cheaper products as the common population of headphone buyers go for relatively cheaper with decent sound quality.
                            """)
        
        st.markdown("## 6. Top 10 Brands by Average Rating")
        # Top 10 Brands by Average Rating
        average_rating = (df
                        .groupby('brand')['rating']
                        .mean()
                        .reset_index()
                        .sort_values(by='rating', ascending=False)
                        .head(10))
        average_rating.rename(columns={'rating': 'average_rating'}, inplace=True)
        # Visualization of Top 10 Brands by Average Rating
        fig = plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=average_rating,
                        x='average_rating', 
                        y='brand', 
                        hue='brand', 
                        palette='Set3',
                        dodge=False)

        plt.title('Top 10 Brands by Average Rating', fontsize=16)
        plt.xlabel('Average Rating')
        plt.ylabel('Brand')
        plt.grid(axis='x', linestyle='--', alpha=0.4)

        for p in ax.patches:
            width = p.get_width()
            ax.annotate(f'{width:.2f}',
                        xy=(width - 0.05*width, p.get_y() + p.get_height()/2),
                        ha='right',
                        va='center',
                        color='black',
                        fontsize=10)
        st.pyplot(fig)
        with st.expander("**Insight**"):
                st.markdown("""
                            These top 10 brands have a relatively high average rating, with this consumer can get an insight on which brand that have best product they can based their decision on. While exploring these brands, consumer may find which product that suit their demand after exploring deeper the quality and the price of the choosen product.
                            """)
        
        st.markdown("## 7. Top 10 Brands by Average Price for In Ear Earphones")
        # Filter ear placement for 'In Ear' type
        df_in_ear = df[df['ear_placement'] == 'In Ear']

        avg_in_ear_price = (df_in_ear
                            .groupby('brand')['price']
                            .mean()
                            .reset_index()
                            .sort_values(by='price', ascending=False)
                            .head(10))

        fig = plt.figure(figsize=(10, 6))
        ax = sns.barplot(data=avg_in_ear_price,
                        x='brand',
                        y='price',
                        hue='brand',
                        palette='Set3')

        plt.xlabel('Brand')
        plt.ylabel('Average Price ($)')
        plt.title('Top 10 Brands by Average Price for In Ear Earphones', fontsize=16)
        plt.tight_layout()
        st.pyplot(fig)

        with st.expander("**Insight**"):
                st.markdown("""
                            Because most of the product Ear Placement is In Ear headphone type, this chart shows which brand that has the top quality In Ear headphones based on the pricing. Still, Bose, Sennheiser and Samsung has the top place, show these brand has high popularity and luxury for the average price of their headphone product. For high-end buyer may go for these brands, or for medium-level buyer may go for brand like Huawei, Realme and the other, as they offer relatively cheaper price and still has high quality sound based on those price.
                            """)
        
        st.markdown("## 8. Brand vs Form Factor Distribution")
        # Create pivot table
        pivot_form = pd.pivot_table(df, 
                                    index='brand',
                                    columns='form_factor',
                                    aggfunc='size',
                                    fill_value=0)

        fig = plt.figure(figsize=(12, 6))
        sns.heatmap(pivot_form,
                    annot=True,
                    linewidth=0.5,
                    linecolor='gray',
                    fmt='d',
                    cmap='Blues')
        plt.title('Brand vs Form Factor Distribution')
        plt.xlabel('Form Factor')
        plt.ylabel('Brand')
        plt.tight_layout()
        st.pyplot(fig)
        with st.expander("**Insight**"):
                st.markdown("""
                            This chart shows each brand and what type of Form Factor product they produce. Almost none of the brand produce Form Factor like On Ear, Open Ear, Open/Over Ear Earbuds, Over Ear except for Baseus, this shows that Baseus gives many choice of Form Factor type for consumer to choose.  
                            Most of the brand priotize focuse on producing In Ear type as we can assume it is mostly demanded product in market. Even though Baseus produce many type of Form Factor, but it doesn't produce True Wireless product, instead the other brands mostly produce In Ear and True Wireless type product. With this, consumer may get an insight if they want many variety of type, they may go for Basues or if they want True Wireless they may go for other brand, like Jbl that has multiple True Wireless product.
                            """)
                    
    with tabs[2]:
        # Check Label Distribution
        st.markdown('## 1. Sentiment Distribution')
        print(ds['label'].value_counts())
        fig, ax = plt.subplots(figsize=(12,5))
        sns.countplot(x = 'label',data= ds, palette='Set2')
        plt.title('Sentiment Distribution')
        st.pyplot(fig)

        st.markdown('## 2. Character Count')
        ds["char_count"] = ds["review_text"].apply(len)
        fig = plt.figure(figsize=(12, 5))
        sns.histplot(ds['char_count'], bins=50, kde=True, color='green')
        plt.title('Distribution of Character Count')
        plt.xlabel('Number of Character')
        plt.ylabel('Frequency')
        st.pyplot(fig)

        st.markdown('## 3. Character Count For All Labels')
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
        sns.histplot(data=ds[ds['label'] == 'Positive'], x='char_count', bins=50, kde=True, ax=axes[0], color='red')
        axes[0].set_title('Positive Review - Character Count')
        axes[0].set_xlabel('Number of Character')
        axes[0].set_ylabel('Frequency')

        sns.histplot(data=ds[ds['label'] == 'Negative'], x='char_count', bins=50, kde=True, ax=axes[1])
        axes[1].set_title('Negative Review - Character Count')
        axes[1].set_xlabel('Number of Character')

        sns.histplot(data=ds[ds['label'] == 'Neutral'], x='char_count', bins=50, kde=True, ax=axes[2], color ='yellow')
        axes[2].set_title('Neutral Review - Character Count')
        axes[2].set_xlabel('Number of Character')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("## 4. Words Count")
        ds['word_count'] = ds['review_text'].astype(str).apply(lambda x: len(nltk.word_tokenize(x)))
        fig = plt.figure(figsize=(15, 5))
        sns.histplot(ds['word_count'], bins=50, kde=True, color='green')
        plt.title('Distribution of Words Count')
        plt.xlabel('Number of Words')
        plt.ylabel('Frequency')
        st.pyplot(fig)

        st.markdown("## 5. Words Count for All Labels")
        fig, axes = plt.subplots(1, 3, figsize=(15, 5), sharey=True)
        sns.histplot(data=ds[ds['label'] == 'Positive'], x='word_count', bins=50, kde=True, ax=axes[0], color='red')
        axes[0].set_title('Positive Review - Words Count')
        axes[0].set_xlabel('Number of Words')
        axes[0].set_ylabel('Frequency')

        sns.histplot(data=ds[ds['label'] == 'Negative'], x='word_count', bins=50, kde=True, ax=axes[1])
        axes[1].set_title('Negative Review - Words Count')
        axes[1].set_xlabel('Number of Words')

        sns.histplot(data=ds[ds['label'] == 'Neutral'], x='word_count', bins=50, kde=True, ax=axes[2])
        axes[2].set_title('Neutral Review - Words Count')
        axes[2].set_xlabel('Number of Words')

        plt.tight_layout()
        st.pyplot(fig)

        st.markdown("## 6. WordCloud for Positive Label")
        # Membuat wordcloud
        text_positive = ds[ds['label'] == 'Positive'].review_text.values
        cloud_text_positive = WordCloud(background_color='black',colormap="cool",collocations=False,width=2000,height=1000).generate(" ".join(text_positive))

        # Menampilkan wordcloud
        fig = plt.figure(figsize=(15,10))
        plt.axis('off')
        plt.title("Positive Review Words",fontsize=20)
        plt.imshow(cloud_text_positive)
        st.pyplot(fig)

        st.markdown("## 7. WordCloud for Negative Label")
        # Membuat wordcloud
        text_negative = ds[ds['label'] == 'Negative'].review_text.values
        cloud_text_negative = WordCloud(background_color='black',colormap="cool",collocations=False,width=2000,height=1000).generate(" ".join(text_negative))

        # Menampilkan wordcloud
        fig = plt.figure(figsize=(15,10))
        plt.axis('off')
        plt.title("Negative Review Words",fontsize=20)
        plt.imshow(cloud_text_negative)
        st.pyplot(fig)
        
        st.markdown("## 7. WordCloud for Negative Label")          
        # Membuat wordcloud
        text_neutral = ds[ds['label'] == 'Neutral'].review_text.values
        cloud_text_neutral = WordCloud(background_color='black',colormap="cool",collocations=False,width=2000,height=1000).generate(" ".join(text_neutral))

        # Menampilkan wordcloud
        fig = plt.figure(figsize=(15,10))
        plt.axis('off')
        plt.title("Neutral Review Words",fontsize=20)
        plt.imshow(cloud_text_neutral)
        st.pyplot(fig)


if __name__=='__main__':
    run_eda()