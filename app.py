# =====================================
# PART 1
# CONFIGURATION & UI FOUNDATION
# =====================================


import streamlit as st
import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go

from pathlib import Path



# -----------------------------
# Page Configuration
# -----------------------------


st.set_page_config(

    page_title=
    "Digikala Content Intelligence",

    page_icon="🛒",

    layout="wide",

    initial_sidebar_state="expanded"

)



# -----------------------------
# Custom CSS
# -----------------------------


st.markdown(

"""

<style>


.main-header {

font-size:35px;

font-weight:800;

}



.metric-card {


background:#ffffff;

padding:20px;

border-radius:15px;

box-shadow:0 4px 15px rgba(0,0,0,0.08);

}



.section-title{

font-size:25px;

font-weight:700;

margin-top:20px;

}



</style>


""",

unsafe_allow_html=True

)



# -----------------------------
# Logo
# -----------------------------


logo_path = Path(
"assets/digikala_logo.png"
)


if logo_path.exists():

    st.sidebar.image(

        str(logo_path),

        width=180

    )

else:

    st.sidebar.markdown(

        "🛒 **Digikala Content Analytics**"

    )



# -----------------------------
# Header
# -----------------------------


st.markdown(

"""

<div class="main-header">

🛒 Digikala Content Intelligence Platform

</div>


""",

unsafe_allow_html=True

)



st.caption(

"AI Powered Content Analytics Dashboard | Data Driven Decision System"

)
# =====================================
# PART 2
# DATA LOADING & DATA QUALITY ENGINE
# =====================================


from pathlib import Path
import streamlit as st
import pandas as pd



# -------------------------------------
# Project Paths
# -------------------------------------


BASE_DIR = Path(__file__).resolve().parent


DATA_PATH = (

    BASE_DIR

    / "data"

    / "processed"

    / "content_analytics_dataset.csv"

)



# -------------------------------------
# Data Loading Function
# -------------------------------------


@st.cache_data(
    ttl=3600
)

def load_content_data():

    """
    Load Digikala Content Analytics Dataset

    Features:

    - Product information
    - Customer reviews
    - Content quality metrics
    - AI opportunity scores

    """


    try:


        df = pd.read_csv(

            DATA_PATH,

            encoding="utf-8"

        )


        return df



    except FileNotFoundError:


        st.error(

        """
        ❌ فایل داده پیدا نشد.

        مسیر مورد انتظار:

        data/processed/content_analytics_dataset.csv

        """

        )


        st.stop()



    except Exception as e:


        st.error(

            f"خطا در بارگذاری داده: {e}"

        )


        st.stop()




# -------------------------------------
# Load Dataset
# -------------------------------------


data = load_content_data()



# -------------------------------------
# Data Validation Engine
# -------------------------------------



def data_quality_report(df):


    report = {


        "تعداد رکوردها":

        len(df),



        "تعداد ستون‌ها":

        df.shape[1],



        "مقادیر خالی":

        int(

            df.isnull()

            .sum()

            .sum()

        ),



        "تعداد محصولات":

        df["product_id"]

        .nunique()

        if "product_id" in df.columns

        else 0,


        "تاریخ بررسی":

        pd.Timestamp.now()

    }



    return pd.DataFrame(

        report,

        index=[0]

    )




# -------------------------------------
# Generate Quality Report
# -------------------------------------


quality_report = data_quality_report(data)



# -------------------------------------
# Sidebar Data Status
# -------------------------------------


st.sidebar.markdown(

"---"

)


st.sidebar.subheader(

"📂 وضعیت داده"

)



st.sidebar.success(

"Dataset Loaded Successfully"

)



st.sidebar.metric(

"تعداد رکورد",

f"{len(data):,}"

)



st.sidebar.metric(

"تعداد ویژگی",

f"{data.shape[1]:,}"

)



# -------------------------------------
# Internal Data Preparation
# -------------------------------------



required_columns = [


"product_id",

"title_fa",

"Category1",

"Brand",

"rate",

"Content_Completeness",

"Customer_Satisfaction",

"Engagement_Score",

"Opportunity_Score"


]



available_columns = [

col

for col in required_columns

if col in data.columns

]



analytics_data = data[

    available_columns

].copy()


# =====================================
# PART 3
# SIDEBAR CONTROL CENTER
# ADVANCED FILTER SYSTEM
# =====================================



# -------------------------------------
# Sidebar Title
# -------------------------------------


st.sidebar.markdown(

"""
## 🎛 مرکز کنترل تحلیل

فیلترهای زیر روی تمام نمودارها
و گزارش‌ها اعمال می‌شوند.

"""

)



# -------------------------------------
# Category Filter
# -------------------------------------


if "Category1" in analytics_data.columns:


    category_options = (

        analytics_data["Category1"]

        .dropna()

        .unique()

    )


    selected_categories = st.sidebar.multiselect(

        "📂 انتخاب دسته‌بندی",

        options=sorted(category_options),

        default=[]

    )


else:

    selected_categories = []




# -------------------------------------
# Brand Filter
# -------------------------------------


if "Brand" in analytics_data.columns:


    brand_options = (

        analytics_data["Brand"]

        .dropna()

        .unique()

    )


    selected_brands = st.sidebar.multiselect(

        "🏷 انتخاب برند",

        options=sorted(brand_options)[:200],

        default=[]

    )


else:

    selected_brands = []





# -------------------------------------
# Seller Filter
# -------------------------------------


if "Seller" in data.columns:


    seller_options = (

        data["Seller"]

        .dropna()

        .unique()

    )


    selected_sellers = st.sidebar.multiselect(

        "🏪 انتخاب فروشنده",

        options=sorted(seller_options)[:100],

        default=[]

    )


else:

    selected_sellers = []





# -------------------------------------
# Price Range
# -------------------------------------


if "Price" in data.columns:


    min_price = int(

        data["Price"]

        .min()

    )


    max_price = int(

        data["Price"]

        .max()

    )


    price_range = st.sidebar.slider(

        "💰 بازه قیمت",

        min_value=min_price,

        max_value=max_price,

        value=(min_price,max_price)

    )


else:

    price_range = None





# -------------------------------------
# Opportunity Filter
# -------------------------------------


show_only_opportunity = st.sidebar.checkbox(

    "🤖 فقط محصولات نیازمند بهبود",

    value=False

)





# -------------------------------------
# Apply Filters Function
# -------------------------------------


def apply_filters(df):


    filtered = df.copy()



    # Category

    if selected_categories:


        filtered = filtered[

            filtered["Category1"]

            .isin(selected_categories)

        ]



    # Brand

    if selected_brands:


        filtered = filtered[

            filtered["Brand"]

            .isin(selected_brands)

        ]



    # Seller

    if selected_sellers and "Seller" in filtered.columns:


        filtered = filtered[

            filtered["Seller"]

            .isin(selected_sellers)

        ]



    # Price

    if price_range and "Price" in filtered.columns:


        filtered = filtered[

            (filtered["Price"] >= price_range[0])

            &

            (filtered["Price"] <= price_range[1])

        ]



    # AI Opportunity

    if show_only_opportunity:


        filtered = filtered[

            filtered["Opportunity_Score"]

            >

            filtered["Opportunity_Score"]

            .quantile(0.75)

        ]



    return filtered





# -------------------------------------
# Final Filtered Dataset
# -------------------------------------


filtered_data = apply_filters(data)





# -------------------------------------
# Filter Summary
# -------------------------------------


st.sidebar.markdown("---")


st.sidebar.subheader(

"📌 وضعیت فیلتر"

)



st.sidebar.info(

f"""

تعداد محصولات:

{filtered_data['product_id'].nunique():,}


تعداد رکوردها:

{len(filtered_data):,}

"""

)
# =====================================
# PART 4
# EXECUTIVE OVERVIEW DASHBOARD
# =====================================



st.markdown(
"""
<div class="section-title">

📊 نمای کلی عملکرد محتوا

</div>

""",

unsafe_allow_html=True

)



# -------------------------------------
# KPI Calculation Layer
# -------------------------------------


total_products = (

    filtered_data["product_id"]

    .nunique()

)



total_reviews = len(filtered_data)



avg_rating = (

    filtered_data["rate"]

    .mean()

)



content_quality = (

    filtered_data["Content_Completeness"]

    .mean()

    *

    100

)



customer_satisfaction = (

    filtered_data["Customer_Satisfaction"]

    .mean()

    *

    100

)



engagement_score = (

    filtered_data["Engagement_Score"]

    .mean()

    *

    100

)



opportunity_index = (

    filtered_data["Opportunity_Score"]

    .mean()

    *

    100

)



# -------------------------------------
# KPI Cards
# -------------------------------------


col1,col2,col3,col4 = st.columns(4)



with col1:

    st.metric(

        label="🛒 تعداد محصولات",

        value=f"{total_products:,}",

        help="تعداد محصولات تحلیل شده"

    )



with col2:

    st.metric(

        label="💬 تعداد نظرات",

        value=f"{total_reviews:,}",

        help="تعداد Review های کاربران"

    )



with col3:

    st.metric(

        label="⭐ میانگین امتیاز",

        value=f"{avg_rating:.2f}",

        help="Average Customer Rating"

    )



with col4:

    st.metric(

        label="📈 کیفیت محتوا",

        value=f"{content_quality:.1f}%",

        help="Content Completeness Score"

    )





# -------------------------------------
# Second KPI Row
# -------------------------------------



st.write("")



col5,col6,col7,col8 = st.columns(4)



with col5:


    st.metric(

        "😊 رضایت مشتری",

        f"{customer_satisfaction:.1f}%"

    )



with col6:


    st.metric(

        "🔥 تعامل کاربران",

        f"{engagement_score:.1f}%"

    )



with col7:


    st.metric(

        "🤖 فرصت بهبود AI",

        f"{opportunity_index:.1f}%"

    )



with col8:


    st.metric(

        "📦 دسته‌بندی‌ها",

        filtered_data["Category1"]

        .nunique()

    )



# -------------------------------------
# Business Health Score
# -------------------------------------



st.subheader(

"🏥 شاخص سلامت محتوای فروشگاه"

)



health_score = (

    content_quality * 0.4

    +

    customer_satisfaction * 0.3

    +

    engagement_score * 0.3

)



fig_health = go.Figure(

    go.Indicator(

        mode="gauge+number",

        value=health_score,

        title={

            "text":

            "Content Health Score"

        },

        gauge={

            "axis":

            {

            "range":[0,100]

            }

        }

    )

)



st.plotly_chart(

    fig_health,

    use_container_width=True

)




# -------------------------------------
# Category Performance
# -------------------------------------



st.subheader(

"📂 عملکرد دسته‌بندی‌ها"

)



category_summary = (

    filtered_data

    .groupby("Category1")

    .agg(

        products=(

            "product_id",

            "nunique"

        ),

        avg_rating=(

            "rate",

            "mean"

        ),

        content_quality=(

            "Content_Completeness",

            "mean"

        ),

        satisfaction=(

            "Customer_Satisfaction",

            "mean"

        )

    )

    .reset_index()

)



category_summary[

"content_quality"

] *= 100



category_summary[

"satisfaction"

] *= 100



fig_category = px.scatter(

    category_summary,

    x="content_quality",

    y="satisfaction",

    size="products",

    color="avg_rating",

    hover_name="Category1",

    title=

    "رابطه کیفیت محتوا و رضایت مشتری"

)



st.plotly_chart(

    fig_category,

    use_container_width=True

)



# -------------------------------------
# Top Opportunity Categories
# -------------------------------------



st.subheader(

"🚨 دسته‌بندی‌های دارای بیشترین فرصت بهبود"

)



opportunity_categories = (

    filtered_data

    .groupby("Category1")

    ["Opportunity_Score"]

    .mean()

    .sort_values(

        ascending=False

    )

    .head(10)

    .reset_index()

)



fig_opportunity = px.bar(

    opportunity_categories,

    x="Category1",

    y="Opportunity_Score",

    title=

    "AI Opportunity Ranking"

)



st.plotly_chart(

    fig_opportunity,

    use_container_width=True

)
# =====================================
# PART 5
# CONTENT PERFORMANCE ANALYTICS
# =====================================



st.markdown(
"""
<div class="section-title">

📦 تحلیل عملکرد محتوا

</div>

""",
unsafe_allow_html=True
)



# -------------------------------------
# Product Performance Table
# -------------------------------------


st.subheader(
"🏆 محصولات برتر از نظر کیفیت محتوا"
)



product_performance = (

    filtered_data

    .groupby(
        [
            "product_id",
            "title_fa",
            "Brand",
            "Category1"
        ]
    )

    .agg(

        rating=(

            "rate",

            "mean"

        ),


        content_quality=(

            "Content_Completeness",

            "mean"

        ),


        satisfaction=(

            "Customer_Satisfaction",

            "mean"

        ),


        engagement=(

            "Engagement_Score",

            "mean"

        )

    )


    .reset_index()

)



product_performance["Content Score"] = (

    product_performance["content_quality"]

    *

    100

)



top_products = (

    product_performance

    .sort_values(

        "Content Score",

        ascending=False

    )

    .head(10)

)



st.dataframe(

    top_products[

        [

            "title_fa",

            "Brand",

            "Category1",

            "rating",

            "Content Score"

        ]

    ],

    use_container_width=True

)





# -------------------------------------
# Weak Content Detection
# -------------------------------------


st.subheader(

"🚨 محصولات دارای محتوای ضعیف"

)



weak_products = (

    product_performance

    .sort_values(

        "Content Score",

        ascending=True

    )

    .head(20)

)



st.dataframe(

    weak_products[

        [

            "title_fa",

            "Brand",

            "Category1",

            "Content Score",

            "rating"

        ]

    ],

    use_container_width=True

)





# -------------------------------------
# Content Quality Distribution
# -------------------------------------


st.subheader(

"📊 توزیع کیفیت محتوا"

)



fig_quality = px.histogram(

    product_performance,

    x="Content Score",

    nbins=30,

    title=

    "Content Completeness Distribution"

)



st.plotly_chart(

    fig_quality,

    use_container_width=True

)





# -------------------------------------
# Brand Analysis
# -------------------------------------


st.subheader(

"🏷 تحلیل عملکرد برندها"

)



brand_analysis = (

    filtered_data

    .groupby("Brand")

    .agg(

        products=(

            "product_id",

            "nunique"

        ),


        avg_rating=(

            "rate",

            "mean"

        ),


        content_quality=(

            "Content_Completeness",

            "mean"

        ),


        customer_satisfaction=(

            "Customer_Satisfaction",

            "mean"

        )

    )

    .reset_index()

)



brand_analysis["Content Quality %"] = (

    brand_analysis["content_quality"]

    *

    100

)



fig_brand = px.scatter(

    brand_analysis,

    x="Content Quality %",

    y="avg_rating",

    size="products",

    hover_name="Brand",

    title=

    "Brand Content Quality vs Rating"

)



st.plotly_chart(

    fig_brand,

    use_container_width=True

)





# -------------------------------------
# Seller Content Analysis
# -------------------------------------


if "Seller" in filtered_data.columns:


    st.subheader(

    "🏪 تحلیل فروشندگان"

    )


    seller_analysis = (

        filtered_data

        .groupby("Seller")

        .agg(

            products=(

                "product_id",

                "nunique"

            ),


            avg_rating=(

                "rate",

                "mean"

            ),


            content_quality=(

                "Content_Completeness",

                "mean"

            )

        )

        .reset_index()

    )


    seller_analysis["Quality %"] = (

        seller_analysis["content_quality"]

        *

        100

    )


    st.dataframe(

        seller_analysis

        .sort_values(

            "Quality %",

            ascending=False

        )

        .head(20),

        use_container_width=True

    )





# -------------------------------------
# Opportunity Matrix
# -------------------------------------


st.subheader(

"🎯 ماتریس فرصت بهبود محتوا"

)



opportunity_matrix = (

    product_performance

    .copy()

)



fig_matrix = px.scatter(

    opportunity_matrix,

    x="rating",

    y="Content Score",

    size="engagement",

    color="satisfaction",

    hover_name="title_fa",

    title=

    "Content Quality Opportunity Matrix"

)



st.plotly_chart(

    fig_matrix,

    use_container_width=True

)
# =====================================
# PART 6
# NLP + CUSTOMER FEEDBACK INTELLIGENCE
# =====================================


import re
from collections import Counter



st.markdown(

"""
<div class="section-title">

🤖 هوش مصنوعی تحلیل بازخورد مشتری

</div>

""",

unsafe_allow_html=True

)



# -------------------------------------
# Sentiment Overview
# -------------------------------------


st.subheader(

"😊 تحلیل احساسات مشتریان"

)



if "recommendation_status" in filtered_data.columns:


    sentiment_count = (

        filtered_data

        ["recommendation_status"]

        .value_counts()

        .reset_index()

    )


    sentiment_count.columns = [

        "Sentiment",

        "Count"

    ]



    fig_sentiment = px.pie(

        sentiment_count,

        names="Sentiment",

        values="Count",

        title=

        "Customer Sentiment Distribution"

    )


    st.plotly_chart(

        fig_sentiment,

        use_container_width=True

    )


else:


    st.info(

        "ستون تحلیل احساسات در داده موجود نیست"

    )





# -------------------------------------
# Text Preparation
# -------------------------------------


def clean_persian_text(text):


    if pd.isna(text):

        return ""


    text = str(text)



    text = re.sub(

        r'[^\w\s\u0600-\u06FF]',

        '',

        text

    )


    return text





# -------------------------------------
# Positive / Negative Keywords
# -------------------------------------



st.subheader(

"🔎 استخراج نکات پرتکرار مشتریان"

)



if "body" in filtered_data.columns:


    comments = (

        filtered_data["body"]

        .dropna()

        .apply(clean_persian_text)

    )



    all_words = []



    for comment in comments:


        all_words.extend(

            comment.split()

        )



    word_frequency = (

        Counter(all_words)

        .most_common(20)

    )



    word_df = pd.DataFrame(

        word_frequency,

        columns=[

            "کلمه",

            "تعداد"

        ]

    )



    fig_words = px.bar(

        word_df,

        x="تعداد",

        y="کلمه",

        orientation="h",

        title=

        "کلمات پرتکرار در نظرات"

    )



    st.plotly_chart(

        fig_words,

        use_container_width=True

    )



else:


    st.warning(

        "داده کامنت برای NLP موجود نیست"

    )





# -------------------------------------
# Advantages Analysis
# -------------------------------------


if "advantages" in filtered_data.columns:


    st.subheader(

    "👍 مهم‌ترین نقاط قوت محصولات"

    )


    advantages = (

        filtered_data

        ["advantages"]

        .dropna()

    )


    advantage_words = []



    for item in advantages:


        advantage_words.extend(

            clean_persian_text(item)

            .split()

        )



    adv_df = pd.DataFrame(

        Counter(

            advantage_words

        )

        .most_common(15),

        columns=[

            "ویژگی مثبت",

            "تعداد"

        ]

    )



    fig_adv = px.bar(

        adv_df,

        x="تعداد",

        y="ویژگی مثبت",

        orientation="h",

        title=

        "Customer Positive Signals"

    )



    st.plotly_chart(

        fig_adv,

        use_container_width=True

    )





# -------------------------------------
# Disadvantages Analysis
# -------------------------------------


if "disadvantages" in filtered_data.columns:


    st.subheader(

    "⚠️ مشکلات پرتکرار مشتریان"

    )



    disadvantages = (

        filtered_data

        ["disadvantages"]

        .dropna()

    )



    negative_words = []



    for item in disadvantages:


        negative_words.extend(

            clean_persian_text(item)

            .split()

        )



    neg_df = pd.DataFrame(

        Counter(

            negative_words

        )

        .most_common(15),

        columns=[

            "مشکل",

            "تعداد"

        ]

    )



    fig_neg = px.bar(

        neg_df,

        x="تعداد",

        y="مشکل",

        orientation="h",

        title=

        "Customer Pain Points"

    )


    st.plotly_chart(

        fig_neg,

        use_container_width=True

    )





# -------------------------------------
# AI Insight Generator
# -------------------------------------


st.subheader(

"🧠 پیشنهاد هوشمند AI"

)



def generate_ai_insight(df):


    insights=[]



    avg_quality = (

        df["Content_Completeness"]

        .mean()

    )



    if avg_quality < 0.7:


        insights.append(

        "کیفیت محتوای محصولات پایین است؛ پیشنهاد می‌شود مشخصات فنی، تصاویر و توضیحات تکمیل شوند."

        )


    if (

        df["Customer_Satisfaction"]

        .mean()

        <

        0.7

    ):


        insights.append(

        "رضایت مشتری پایین است؛ بررسی نقاط ضعف محصولات و بازنویسی محتوا پیشنهاد می‌شود."

        )


    if not insights:


        insights.append(

        "وضعیت محتوا مناسب است اما بهینه‌سازی مستمر پیشنهاد می‌شود."

        )



    return insights





for insight in generate_ai_insight(filtered_data):


    st.success(

        insight

    )
# =====================================
# PART 7
# REPORTING CENTER
# AI RECOMMENDATION ENGINE
# EXPORT SYSTEM
# =====================================



st.markdown(

"""
<div class="section-title">

🚀 مرکز تصمیم‌گیری هوشمند محتوا

</div>

""",

unsafe_allow_html=True

)




# -------------------------------------
# Opportunity Ranking Engine
# -------------------------------------


st.subheader(

"🎯 اولویت‌بندی محصولات برای بهبود محتوا"

)



recommendation_df = filtered_data.copy()



recommendation_df["AI_Priority_Score"] = (

    (

    100 -

    recommendation_df["Content_Completeness"] * 100

    )

    *

    0.4


    +

    

    (

    100 -

    recommendation_df["Customer_Satisfaction"] * 100

    )

    *

    0.3


    +


    (

    recommendation_df["Opportunity_Score"]

    *

    100

    )

    *

    0.3

)



priority_products = (

    recommendation_df

    .sort_values(

        "AI_Priority_Score",

        ascending=False

    )

    .head(20)

)



st.dataframe(

    priority_products[

        [

        "title_fa",

        "Brand",

        "Category1",

        "AI_Priority_Score",

        "Content_Completeness",

        "Customer_Satisfaction"

        ]

    ],

    use_container_width=True

)




# -------------------------------------
# AI Action Recommendation
# -------------------------------------


st.subheader(

"🧠 پیشنهاد اقدام برای تیم محتوا"

)



def generate_actions(row):


    actions=[]



    if row["Content_Completeness"] < 0.6:


        actions.append(

        "تکمیل مشخصات فنی و توضیحات محصول"

        )



    if row["Customer_Satisfaction"] < 0.7:


        actions.append(

        "بررسی مشکلات مطرح شده توسط کاربران"

        )



    if row["Engagement_Score"] < 0.5:


        actions.append(

        "بهبود تصاویر، عنوان و ساختار محتوا"

        )



    return " | ".join(actions)




priority_products["AI_Action"] = (

    priority_products

    .apply(

        generate_actions,

        axis=1

    )

)



st.dataframe(

    priority_products[

        [

        "title_fa",

        "AI_Action"

        ]

    ],

    use_container_width=True

)




# -------------------------------------
# Executive Summary
# -------------------------------------


st.subheader(

"📌 خلاصه مدیریتی"

)



summary_text = f"""

### گزارش وضعیت محتوا

🔹 تعداد محصولات بررسی شده:

{filtered_data['product_id'].nunique():,}


🔹 میانگین کیفیت محتوا:

{filtered_data['Content_Completeness'].mean()*100:.1f}%


🔹 رضایت مشتری:

{filtered_data['Customer_Satisfaction'].mean()*100:.1f}%


🔹 تعداد محصولات نیازمند اقدام:

{len(priority_products):,}



بر اساس تحلیل داده، پیشنهاد می‌شود تیم محتوا ابتدا
محصولات با بیشترین AI Priority Score را بررسی کند.

"""



st.info(summary_text)





# -------------------------------------
# Export Excel
# -------------------------------------


st.subheader(

"📥 خروجی گزارش"

)



@st.cache_data

def convert_csv(df):


    return df.to_csv(

        index=False,

        encoding="utf-8-sig"

    )




csv_data = convert_csv(

    priority_products

)



st.download_button(

    label=

    "⬇ دانلود گزارش CSV",

    data=

    csv_data,

    file_name=

    "digikala_content_ai_report.csv",

    mime=

    "text/csv"

)





# -------------------------------------
# Final Dashboard Footer
# -------------------------------------


st.markdown(

"""

---

<center>

<b>

Digikala Content Intelligence Platform

</b>

<br>

AI Powered Analytics System

</center>

""",

unsafe_allow_html=True

)