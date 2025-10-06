import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pickle
import matplotlib.pyplot as plt
import seaborn as sns
import os
from groq import Groq
from dotenv import load_dotenv
import tempfile

# Load environment variables from .env file
load_dotenv()

# Configure Streamlit Page
st.set_page_config(page_title="Real Estate Analytics", layout="wide", page_icon="🏡")

# Initialize Groq client with environment variable
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set GROQ_API_KEY in your .env file")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# Function to transcribe audio using Groq Whisper
def transcribe_audio(audio_file):
    """Transcribe audio using Groq's Whisper model"""
    try:
        # Create a temporary file to store the audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            temp_file.write(audio_file.getvalue())
            temp_file_path = temp_file.name
        
        # Transcribe using Groq Whisper
        with open(temp_file_path, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(temp_file_path, file.read()),
                model="whisper-large-v3",
                prompt="Real estate analysis and property investment questions. Focus on sectors, prices, investments, market trends.",
                response_format="json",
                language="en",
                temperature=0.0
            )
        
        # Clean up the temporary file
        os.unlink(temp_file_path)
        
        return transcription.text
    
    except Exception as e:
        return f"Transcription error: {str(e)}"

# Function to get AI insights for graphs
def get_ai_insights(graph_type, data_description, user_question=None):
    """Generate AI insights for specific graphs"""
    try:
        if user_question:
            # Detailed analysis when user asks a question
            prompt = f"""
            You are a senior real estate data analyst and market research expert with 15+ years of experience in property market dynamics.
            
            CONTEXT: A user is examining a {graph_type} that displays {data_description}.
            USER QUESTION: "{user_question}"
            
            Provide a comprehensive, detailed analysis addressing:
            
            1. DIRECT ANSWER: Address the user's specific question clearly and thoroughly
            
            2. DETAILED VISUAL INTERPRETATION: 
               - What specific patterns, trends, clusters, or anomalies are visible
               - Statistical significance of observed patterns
               - Data distribution characteristics and outliers
            
            3. COMPREHENSIVE MARKET ANALYSIS:
               - Supply and demand dynamics revealed by this data
               - Market efficiency indicators and pricing patterns
               - Geographic or demographic insights (if applicable)
               - Seasonal or temporal trends (if applicable)
            
            4. INVESTMENT INTELLIGENCE:
               - Specific high-opportunity areas or segments
               - Risk assessment based on data patterns
               - Portfolio diversification strategies
               - Market timing considerations
               - Comparative value analysis
            
            5. STAKEHOLDER-SPECIFIC RECOMMENDATIONS:
               - First-time buyers: Entry strategies and budget considerations
               - Real estate investors: ROI opportunities and risk mitigation
               - Property developers: Market gaps and development opportunities
               - Market analysts: Key metrics and predictive indicators
            
            6. QUANTITATIVE INSIGHTS:
               - Reference specific data points, percentages, and ranges where relevant
               - Statistical correlations and their implications
               - Performance benchmarks and market comparisons
            
            7. RISK FACTORS & LIMITATIONS:
               - Potential risks or market vulnerabilities
               - Data limitations and what additional analysis is needed
               - External factors that could impact these trends
            
            8. ACTIONABLE NEXT STEPS:
               - Specific recommendations for immediate action
               - Due diligence focus areas
               - Market monitoring strategies
            
            Provide a professional, data-driven analysis with specific insights. Target 500-600 words for comprehensive coverage.
            Use concrete examples and quantitative references where possible.
            """
        else:
            # Simple initial analysis - keep existing brief format
            prompt = f"""
            You are a real estate data analyst. Explain this {graph_type} showing {data_description} in simple terms.
            
            Focus on:
            1. What this visualization reveals about the real estate market
            2. Key patterns or trends visible
            3. What buyers/investors should know from this data
            4. Any notable outliers or interesting findings
            
            Keep it under 150 words and user-friendly.
            """
        
        # Set different parameters based on response type
        if user_question:
            temperature = 0.2  # More focused for detailed analysis
            max_tokens = 700   # More tokens for comprehensive response
        else:
            temperature = 0.7  # Original setting for brief insights
            max_tokens = 200   # Original token limit for brief responses
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=temperature,
            max_tokens=max_tokens
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI analysis temporarily unavailable. Please try again. Error: {str(e)}"

# Enhanced function to create AI chat interface with voice support using st.audio_input
def create_graph_chat_with_voice(graph_id, graph_type, data_description):
    """Create a chat interface with voice input support for specific graph"""
    chat_key = f"chat_history_{graph_id}"
    
    # Initialize chat history for this graph
    if chat_key not in st.session_state:
        st.session_state[chat_key] = []
        # Add initial AI insight (brief format)
        initial_insight = get_ai_insights(graph_type, data_description)
        st.session_state[chat_key].append({"role": "assistant", "content": initial_insight})
    
    # Create expandable section for AI insights
    with st.expander(f"🤖 AI Insights for {graph_type.title()} (Voice & Text Enabled)", expanded=False):
        
        # Add helpful tips for better questions
        st.info("💡 **Ask questions via voice 🎤 or text ⌨️** for comprehensive analysis! Example: 'Which sectors offer the best ROI for investors?'")
        
        # Display chat history with enhanced formatting
        for i, message in enumerate(st.session_state[chat_key]):
            if message["role"] == "user":
                with st.chat_message("user", avatar="👤"):
                    st.write(f"**Question:** {message['content']}")
            else:
                with st.chat_message("assistant", avatar="🤖"):
                    if i == 0:  # First message is the brief overview
                        st.markdown("### 📊 Quick Overview")
                        st.write(message["content"])
                    else:  # Subsequent messages are detailed analysis
                        st.markdown("### 🔍 Detailed Analysis")
                        st.markdown(message["content"])
        
        st.markdown("---")
        
        # Create two columns for voice and text input
        voice_col, text_col = st.columns([1, 1])
        
        with voice_col:
            st.markdown("### 🎤 **Voice Input**")
            
            # Native Streamlit audio input
            audio_input = st.audio_input(
                "Record your question:",
                key=f"audio_input_{graph_id}",
                help="Click to record your question about this chart"
            )
            
            if audio_input is not None:
                # Display audio player
                st.audio(audio_input, format="audio/wav")
                
                # Transcribe button
                if st.button("🔄 Transcribe & Ask", key=f"transcribe_btn_{graph_id}", type="primary"):
                    with st.spinner("🎯 Transcribing your voice question..."):
                        transcribed_text = transcribe_audio(audio_input)
                        
                        if not transcribed_text.startswith("Transcription error"):
                            st.success(f"**Transcribed:** {transcribed_text}")
                            
                            # Add user message with voice indicator
                            st.session_state[chat_key].append({"role": "user", "content": f"🎤 {transcribed_text}"})
                            
                            # Get detailed AI response
                            with st.spinner("🤖 Analyzing your question..."):
                                ai_response = get_ai_insights(graph_type, data_description, transcribed_text)
                                st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
                            
                            # Rerun to show new messages
                            st.rerun()
                        else:
                            st.error("❌ " + transcribed_text)
        
        with text_col:
            st.markdown("### ⌨️ **Text Input**")
            
            # Text input section
            user_input = st.chat_input(f"Type your question about this {graph_type}...", key=f"text_input_{graph_id}")
            
            if user_input:
                # Add user message
                st.session_state[chat_key].append({"role": "user", "content": user_input})
                
                # Get detailed AI response
                ai_response = get_ai_insights(graph_type, data_description, user_input)
                st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
                
                # Rerun to show new messages
                st.rerun()
        
        # Quick question suggestions based on graph type
        suggestions = get_question_suggestions(graph_type)
        
        if suggestions:
            st.markdown("### 💭 **Suggested Questions**")
            cols = st.columns(len(suggestions) if len(suggestions) <= 3 else 3)
            for i, suggestion in enumerate(suggestions[:3]):  # Show max 3 suggestions
                with cols[i % 3]:
                    if st.button(suggestion, key=f"suggest_{graph_id}_{i}", help="Click for detailed analysis"):
                        # Add user message
                        st.session_state[chat_key].append({"role": "user", "content": suggestion})
                        
                        # Get detailed AI response
                        ai_response = get_ai_insights(graph_type, data_description, suggestion)
                        st.session_state[chat_key].append({"role": "assistant", "content": ai_response})
                        
                        # Rerun to show new messages
                        st.rerun()

def get_question_suggestions(graph_type):
    """Get relevant question suggestions based on graph type"""
    suggestions_map = {
        "geographical scatter plot": [
            "Which sectors offer the best value for money?",
            "What geographic patterns show opportunities?",
            "How should location influence buying strategy?"
        ],
        "bar chart": [
            "Which sectors have highest growth potential?",
            "What drives these price differences?",
            "How to diversify across sectors?"
        ],
        "3D scatter plot": [
            "What's optimal size-price-bedroom combo?",
            "Which configurations offer best value?",
            "How does bedroom count impact pricing?"
        ],
        "animated line chart": [
            "What seasonal patterns to monitor?",
            "Which sectors show consistent growth?",
            "When's optimal time to buy/sell?"
        ],
        "violin plot": [
            "Should I invest in houses or flats?",
            "What explains price distribution patterns?",
            "Where are the best property deals?"
        ],
        "heatmap": [
            "Which combinations are overvalued?",
            "Where are market inefficiencies?",
            "What's best ROI strategy?"
        ],
        "box plot": [
            "Which sectors offer price stability?",
            "How to identify overvalued properties?",
            "What are risk levels by sector?"
        ],
        "scatter plot": [
            "What drives price-area relationship?",
            "Are larger properties better investments?",
            "Where are pricing anomalies?"
        ],
        "bubble chart": [
            "Which clusters show best opportunities?",
            "How should size influence strategy?",
            "What are investment sweet spots?"
        ],
        "distribution histogram": [
            "How do houses vs flats compare?",
            "What do patterns reveal about market?",
            "Where should different investors focus?"
        ]
    }
    return suggestions_map.get(graph_type, [
        "What key insights should I know?",
        "What investment opportunities exist?",
        "How should this influence decisions?"
    ])

# Enhanced Global AI Assistant with Voice Support using st.audio_input
def create_global_voice_assistant():
    """Create enhanced global AI assistant with voice input using native Streamlit"""
    st.sidebar.markdown("---")
    st.sidebar.subheader("🧠 Expert AI Consultant")
    
    # Global chat history
    if "global_chat" not in st.session_state:
        st.session_state.global_chat = []
    
    # Voice input section in sidebar
    st.sidebar.markdown("#### 🎤 **Voice Questions**")
    
    # Native Streamlit audio input in sidebar
    sidebar_audio = st.sidebar.audio_input(
        "Record your real estate question:",
        key="sidebar_audio_input",
        help="Record a detailed question about real estate markets"
    )
    
    if sidebar_audio is not None:
        st.sidebar.audio(sidebar_audio, format="audio/wav")
        
        if st.sidebar.button("🎯 Transcribe & Analyze", key="sidebar_transcribe", type="primary"):
            with st.sidebar.spinner("🔄 Processing voice input..."):
                transcribed_question = transcribe_audio(sidebar_audio)
                
                if not transcribed_question.startswith("Transcription error"):
                    st.sidebar.success(f"**Transcribed:** {transcribed_question[:50]}...")
                    
                    # Add user message with voice indicator
                    st.session_state.global_chat.append({"role": "user", "content": f"🎤 {transcribed_question}"})
                    
                    # Get comprehensive AI response
                    try:
                        response = client.chat.completions.create(
                            model="llama-3.1-8b-instant",
                            messages=[
                                {"role": "system", "content": """You are a senior real estate market analyst and investment advisor with 20+ years of experience. 
                                Provide comprehensive, data-driven insights about real estate markets, trends, investment strategies, and market analysis. 
                                Always include specific actionable recommendations and consider different stakeholder perspectives (investors, buyers, developers).
                                Be detailed and thorough, focusing on practical insights and strategic recommendations."""},
                                {"role": "user", "content": transcribed_question}
                            ],
                            temperature=0.2,
                            max_tokens=500
                        )
                        ai_response = response.choices[0].message.content
                        st.session_state.global_chat.append({"role": "assistant", "content": ai_response})
                        st.rerun()
                    except Exception as e:
                        st.session_state.global_chat.append({"role": "assistant", "content": f"Expert consultation temporarily unavailable. Error: {str(e)}"})
                        st.rerun()
                else:
                    st.sidebar.error("❌ Transcription failed. Please try again.")
    
    # Text input section in sidebar
    st.sidebar.markdown("#### ⌨️ **Text Questions**")
    global_input = st.sidebar.text_area(
        "Or type your question:", 
        key="global_input",
        height=70,
        placeholder="e.g., What's the best investment strategy?"
    )
    
    if st.sidebar.button("📊 Get Expert Analysis", key="global_send", type="secondary") and global_input:
        # Add user message
        st.session_state.global_chat.append({"role": "user", "content": global_input})
        
        # Get comprehensive AI response
        try:
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": """You are a senior real estate market analyst and investment advisor with 20+ years of experience. 
                    Provide comprehensive, data-driven insights about real estate markets, trends, investment strategies, and market analysis. 
                    Always include specific actionable recommendations and consider different stakeholder perspectives (investors, buyers, developers).
                    Be detailed and thorough, focusing on practical insights and strategic recommendations."""},
                    {"role": "user", "content": global_input}
                ],
                temperature=0.2,
                max_tokens=500
            )
            ai_response = response.choices[0].message.content
            st.session_state.global_chat.append({"role": "assistant", "content": ai_response})
            st.rerun()
        except Exception as e:
            st.session_state.global_chat.append({"role": "assistant", "content": f"Expert consultation temporarily unavailable. Error: {str(e)}"})
            st.rerun()
    
    # Display enhanced global chat
    if st.session_state.global_chat:
        st.sidebar.markdown("#### 💬 **Recent Consultations**")
        for i, message in enumerate(st.session_state.global_chat[-2:]):  # Show last 2 messages
            if message["role"] == "user":
                # Show voice vs text indicator
                if message['content'].startswith("🎤"):
                    icon = "🎤 Voice"
                    content = message['content'].replace("🎤 ", "")
                else:
                    icon = "⌨️ Text"
                    content = message['content']
                
                st.sidebar.text_area(f"{icon}:", value=content[:60] + ("..." if len(content) > 60 else ""), height=50, disabled=True, key=f"q_{i}_{len(st.session_state.global_chat)}")
            else:
                st.sidebar.text_area("🤖 Response:", value=message['content'][:80] + ("..." if len(message['content']) > 80 else ""), height=60, disabled=True, key=f"a_{i}_{len(st.session_state.global_chat)}")
        
        if st.sidebar.button("🗑️ Clear Chat History", key="clear_global"):
            st.session_state.global_chat = []
            st.rerun()

# Sidebar Navigation
st.sidebar.header("🔍 Dashboard Navigation")
section = st.sidebar.radio("Go to", ["🏡 Overview", "📊 Data Visualization", "🔍 Insights"])

# Load Data
try:
    new_df = pd.read_csv('datasets/data_viz1.csv')
    feature_text = pickle.load(open('datasets/feature_text.pkl', 'rb'))
except FileNotFoundError as e:
    st.error(f"Data file not found: {e}")
    st.stop()

new_df['total_area'] = new_df['built_up_area']

# Group Data for Map Visualization
group_df = new_df.groupby('sector').mean(numeric_only=True)[['price', 'price_per_sqft', 'built_up_area', 'latitude', 'longitude']]

# --- Overview Section ---
if section == "🏡 Overview":
    st.title("🏡 Real Estate Analytics Dashboard")
    
    # Display Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏠 Total Properties", len(new_df))
    col2.metric("📍 Unique Sectors", new_df['sector'].nunique())
    col3.metric("💰 Avg Price (₹)", f"{new_df['price'].mean():,.0f}CR")
    col4.metric("📏 Avg Built-up Area", f"{new_df['built_up_area'].mean():,.0f} sq.ft")
    
    st.markdown("---")
    
    # Sector Price per Sqft Geomap
    st.subheader("🌍 Sector Price per Sqft Geomap")
    fig_map = px.scatter_mapbox(
        group_df, lat="latitude", lon="longitude", color="price_per_sqft", size='built_up_area',
        color_continuous_scale=px.colors.cyclical.IceFire, zoom=10,
        mapbox_style="carto-positron", width=1100, height=600, hover_name=group_df.index
    )
    st.plotly_chart(fig_map, use_container_width=True)
    
    # AI Chat with Voice for Map
    create_graph_chat_with_voice("geomap", "geographical scatter plot", "price per square foot across different sectors with built-up area as bubble size")
    
    st.markdown("---")
    
    # Avg Price per Sector Bar Chart
    st.subheader("📊 Average Price per Sector")
    fig_bar = px.bar(group_df, x=group_df.index, y='price', color='price', title='Average Price per Sector',
                     color_continuous_scale='Viridis')
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # AI Chat with Voice for Bar Chart
    create_graph_chat_with_voice("sector_bar", "bar chart", "average property prices across different sectors")
    
    st.markdown("---")

    # 3D Scatter Plot
    st.subheader("🔍 3D Scatter Plot: Price, Built-up Area & Bedrooms")
    fig_3d = px.scatter_3d(new_df, x='built_up_area', y='price', z='bedRoom',
                           color='property_type', title="Price vs Built-up Area vs Bedrooms",
                           color_continuous_scale='Viridis')
    
    fig_3d.update_layout(
        scene=dict(
            xaxis_title='Built-up Area (sq.ft)',
            yaxis_title='Price (₹)',
            zaxis_title='Bedrooms (BHK)'
        ),
        width=1000, height=700
    )
    
    st.plotly_chart(fig_3d, use_container_width=True)
    
    # AI Chat with Voice for 3D Plot
    create_graph_chat_with_voice("3d_scatter", "3D scatter plot", "relationship between property price, built-up area, and number of bedrooms, colored by property type")
    
    st.markdown("---")

    st.subheader("📈 Sector-wise Property Price Trend Over Time")
    new_df['month'] = (new_df.index % 12) + 1

    price_trend = new_df.groupby(['sector', 'month'], as_index=False)['price'].mean()

    fig_animated = px.line(
        price_trend, x="sector", y="price", color="sector",
        animation_frame="month", title="📈 Sector-wise Property Price Trend Over Time",
        labels={"price": "Avg Price (₹)", "sector": "Sector"},
        markers=True
    )

    st.plotly_chart(fig_animated, use_container_width=True)
    
    # AI Chat with Voice for Animated Line Chart
    create_graph_chat_with_voice("price_trend", "animated line chart", "sector-wise property price trends over months showing market dynamics")

# --- Data Visualization Section ---
elif section == "📊 Data Visualization":
    st.title("📊 Data Visualization")
    
    st.markdown("---")
    
    # Property Price Distribution by Property Type (Violin Plot)
    st.subheader("🏡 Property Price Distribution by Property Type")
    fig_violin = px.violin(new_df, x='property_type', y='price', box=True, points="all", title="Property Price Distribution by Property Type")
    st.plotly_chart(fig_violin, use_container_width=True)
    
    # AI Chat with Voice for Violin Plot
    create_graph_chat_with_voice("violin_plot", "violin plot", "property price distribution comparing houses vs flats with quartiles and data density")
    
    st.markdown("---")
    
    st.subheader("🏡 Price Distribution per Square Foot (Heatmap)")

    price_heatmap_data = new_df.pivot_table(values="price_per_sqft", index="sector", columns="property_type", aggfunc="mean")

    fig_heatmap = go.Figure(data=go.Heatmap(
        z=price_heatmap_data.values,
        x=price_heatmap_data.columns,
        y=price_heatmap_data.index,
        colorscale='Viridis',
        colorbar=dict(title='Price per Sqft'),
    ))

    fig_heatmap.update_layout(
        title="Price Distribution per Square Foot",
        xaxis_title="Property Type",
        yaxis_title="Sector",
        height=600,
        width=1000,
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # AI Chat with Voice for Heatmap
    create_graph_chat_with_voice("heatmap", "heatmap", "price per square foot across sectors and property types showing market heat zones")
    
    st.markdown("---")
    
    # Property Price Distribution by Sector
    st.subheader("📊 Price Distribution by Sector")
    fig_box = px.box(new_df, x='sector', y='price', color='sector', title='Price Distribution Across Sectors')
    st.plotly_chart(fig_box, use_container_width=True)
    
    # AI Chat with Voice for Box Plot
    create_graph_chat_with_voice("box_plot", "box plot", "price distribution across sectors showing medians, quartiles, and outliers")

    st.markdown("---")
    
    # Price vs Built-up Area Scatter Plot
    st.subheader("📉 Price vs Built-up Area")
    fig_scatter = px.scatter(new_df, x="built_up_area", y="price", color="property_type", title="Price vs Built-up Area", trendline="ols")
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # AI Chat with Voice for Scatter Plot
    create_graph_chat_with_voice("scatter_area", "scatter plot", "correlation between property price and built-up area with trend lines by property type")
    
    st.markdown("---")
    
    # Price vs Number of Bedrooms (BHK)
    st.subheader("🛏️ Price vs Number of Bedrooms")
    fig_bhk_scatter = px.scatter(new_df, x="bedRoom", y="price", color="property_type", title="Price vs Number of Bedrooms", trendline="ols")
    st.plotly_chart(fig_bhk_scatter, use_container_width=True)
    
    # AI Chat with Voice for BHK Scatter
    create_graph_chat_with_voice("scatter_bhk", "scatter plot", "relationship between property price and number of bedrooms with trend analysis")
    
    st.markdown("---")
    
    # Price per Sqft vs Latitude/Longitude (Location Scatter)
    st.subheader("📍 Price per Sqft vs Location")
    fig_loc_scatter = px.scatter(new_df, x="longitude", y="latitude", color="price_per_sqft", size='built_up_area', hover_name="sector",
                                 title="Price per Sqft vs Latitude/Longitude", color_continuous_scale=px.colors.cyclical.IceFire)
    st.plotly_chart(fig_loc_scatter, use_container_width=True)
    
    # AI Chat with Voice for Location Scatter
    create_graph_chat_with_voice("location_scatter", "location scatter plot", "geographical distribution of price per square foot showing location-based pricing patterns")

# --- Insights Section ---
elif section == "🔍 Insights":
    st.title("🔍 Insights")
    
    # BHK Price Comparison Box Plot
    st.subheader("💰 BHK Price Comparison")
    fig_bhk_price = px.box(new_df[new_df['bedRoom'] <= 4], x='bedRoom', y='price', title='BHK Price Range')
    st.plotly_chart(fig_bhk_price, use_container_width=True)
    
    # AI Chat with Voice for BHK Comparison
    create_graph_chat_with_voice("bhk_comparison", "box plot", "price comparison across different BHK configurations (1-4 bedrooms)")
    
    st.markdown("---")
    
    # Side by Side Property Type Price Distribution
    st.subheader("📈 Property Type Price Distribution")
    fig_distplot, ax = plt.subplots(figsize=(10, 4))
    sns.histplot(new_df[new_df['property_type'] == 'house']['price'], label='House', kde=True, color='blue', ax=ax)
    sns.histplot(new_df[new_df['property_type'] == 'flat']['price'], label='Flat', kde=True, color='red', ax=ax)
    ax.legend()
    st.pyplot(fig_distplot)
    
    # AI Chat with Voice for Distribution Plot
    create_graph_chat_with_voice("dist_plot", "distribution histogram", "price distribution comparison between houses and flats with density curves")
    
    st.markdown("---")
    
    # Average Price by Bedroom Count
    st.subheader("🏠 Average Price by BHK")
    avg_price_bhk = new_df.groupby('bedRoom')['price'].mean().reset_index()
    fig_avg_bhk = px.bar(avg_price_bhk, x='bedRoom', y='price', color='price', title='Average Price by BHK')
    st.plotly_chart(fig_avg_bhk, use_container_width=True)
    
    # AI Chat with Voice for Average Price BHK
    create_graph_chat_with_voice("avg_bhk", "bar chart", "average property prices by bedroom count showing pricing tiers")
    
    st.markdown("---")
    
    # Price per Sqft by Property Type
    st.subheader("🏡 Price per Sqft by Property Type")
    fig_price_sqft = px.box(new_df, x="property_type", y="price_per_sqft", color="property_type", title="Price per Sqft by Property Type")
    st.plotly_chart(fig_price_sqft, use_container_width=True)
    
    # AI Chat with Voice for Price per Sqft
    create_graph_chat_with_voice("price_sqft_type", "box plot", "price per square foot comparison between property types")
    
    st.markdown("---")

    st.subheader("💡 Cluster Analysis: Price vs. Built-up Area across Sectors")

    fig_bubble = px.scatter(
        new_df, x="built_up_area", y="price", size="price", color="sector",
        hover_name="sector", title="Property Price Clusters: Built-up Area vs. Price",
        labels={"built_up_area": "Built-up Area (sq.ft)", "price": "Price (₹)"},
        opacity=0.7, size_max=40
    )

    fig_bubble.update_layout(
        width=1000, height=600,
        xaxis_title="Built-up Area (sq.ft)",
        yaxis_title="Price (₹)",
        legend_title="Sector"
    )

    st.plotly_chart(fig_bubble, use_container_width=True)
    
    # AI Chat with Voice for Cluster Analysis
    create_graph_chat_with_voice("cluster_analysis", "bubble chart", "property price clusters showing relationship between built-up area and price across different sectors")

# Enhanced Global AI Assistant with Voice Support
create_global_voice_assistant()
