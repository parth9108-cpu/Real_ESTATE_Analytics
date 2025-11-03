# pages/Ask_real_estate_AI.py
import streamlit as st
import pandas as pd
import os
import tempfile
import base64
import io
import numpy as np
from groq import Groq
from dotenv import load_dotenv
from PIL import Image

# Import with fallback handling
try:
    import PyPDF2
except ImportError:
    st.error("Please install PyPDF2: pip install PyPDF2")
    PyPDF2 = None

try:
    from docx import Document
except ImportError:
    st.error("Please install python-docx: pip install python-docx")
    Document = None

# Load environment variables
load_dotenv()

# Configure Streamlit Page
st.set_page_config(
    page_title="Ask Real Estate AI", 
    layout="wide", 
    page_icon="🤖"
)

# Add modern CSS styling
st.markdown("""
<style>
    /* Import modern fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .main {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hero section styling */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        text-align: center;
        color: white;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }
    
    /* Analysis result styling */
    .analysis-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border-left: 4px solid #667eea;
    }
    
    .file-info-card {
        background: #e2e8f0;
        border-radius: 10px;
        padding: 1rem;
        margin: 0.5rem 0;
        border-left: 3px solid #48bb78;
    }
    
    /* Supported files styling */
    .supported-files {
        background: grey;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .file-type-badge {
        background: #667eea;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        margin: 0.2rem;
        font-size: 0.8rem;
        display: inline-block;
    }
    
    /* New file analysis button */
    .new-analysis-btn {
        background: linear-gradient(135deg, #ff4757 0%, #ff3742 100%);
        color: white;
        border: none;
        padding: 1rem 2rem;
        border-radius: 10px;
        font-size: 1.1rem;
        font-weight: 600;
        margin: 1rem 0;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(255, 71, 87, 0.3);
        transition: all 0.3s ease;
    }
    
    .new-analysis-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(255, 71, 87, 0.4);
    }
    
    /* Chat flow styling */
    .chat-flow {
        max-width: none;
        margin: 0;
    }
    
    .follow-up-section {
        background: #f8fafc;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        border-left: 4px solid #48bb78;
    }
    
    /* Success styling */
    .success-card {
        background: #c6f6d5;
        border: 1px solid #9ae6b4;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        color: #2f855a;
    }
</style>
""", unsafe_allow_html=True)

# Initialize Groq client
@st.cache_resource
def init_groq_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        st.error("Please set GROQ_API_KEY in your .env file")
        st.stop()
    return Groq(api_key=api_key)

client = init_groq_client()

# Function to encode image to base64
def encode_image_to_base64(image_file):
    """Encode image to base64 for API"""
    try:
        return base64.b64encode(image_file.getvalue()).decode('utf-8')
    except Exception as e:
        st.error(f"Error encoding image: {str(e)}")
        return None

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    """Extract text from PDF file"""
    if PyPDF2 is None:
        return "PyPDF2 not installed. Please run: pip install PyPDF2"
    
    try:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file.getvalue()))
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() + "\n"
        return text
    except Exception as e:
        return f"Error extracting PDF text: {str(e)}"

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    """Extract text from DOCX file"""
    if Document is None:
        return "python-docx not installed. Please run: pip install python-docx"
    
    try:
        doc = Document(io.BytesIO(docx_file.getvalue()))
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        return f"Error extracting DOCX text: {str(e)}"

# Function to analyze image with Groq Vision
def analyze_image_with_groq(image_file, user_question="Analyze this real estate related image in detail"):
    """Analyze image using Groq's vision model"""
    try:
        base64_image = encode_image_to_base64(image_file)
        if not base64_image:
            return "Failed to process image."
        
        response = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"""You are a senior real estate expert and analyst with 15+ years of experience. 
                            
                            User Question: {user_question}
                            
                            Please provide a comprehensive analysis of this image focusing on:
                            1. Property details and characteristics
                            2. Market insights and valuation indicators  
                            3. Investment potential and risks
                            4. Recommendations for buyers/investors
                            5. Any notable features or concerns
                            
                            Be specific, detailed, and actionable in your response."""
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing image: {str(e)}. Please try using a different image format or smaller file size."

# Function to analyze document with Groq
def analyze_document_with_groq(text_content, user_question, file_type):
    """Analyze document text using Groq"""
    try:
        prompt = f"""
        You are a senior real estate expert and analyst with 15+ years of experience. 
        
        A user has uploaded a {file_type} document and asked: "{user_question}"
        
        Document content:
        {text_content[:8000]}  # Limit content to prevent token overflow
        
        Please provide a comprehensive real estate analysis focusing on:
        1. Key insights and findings from the document
        2. Market implications and trends
        3. Investment opportunities and risks
        4. Financial analysis (if applicable)
        5. Strategic recommendations
        6. Next steps and action items
        
        Be specific, data-driven, and actionable in your response.
        """
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a senior real estate expert and market analyst with deep knowledge of property markets, investments, and industry trends."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"Error analyzing document: {str(e)}"

# Function to get AI response for follow-up questions
def get_ai_followup_response(question, context):
    """Get AI response for follow-up questions with context"""
    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": """You are a senior real estate expert and investment advisor with 20+ years of experience. 
                Provide comprehensive, actionable advice on all real estate topics. Be specific, practical, and data-driven."""},
                {"role": "assistant", "content": context},
                {"role": "user", "content": question}
            ],
            temperature=0.3,
            max_tokens=1200
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"I apologize, but I encountered an error: {str(e)}. Please try rephrasing your question."

# Function to clear all session states for new analysis
def clear_analysis_state():
    """Clear all analysis-related session states"""
    keys_to_clear = [
        'chat_mode',
        'current_analysis',
        'analysis_completed',
        'chat_history'
    ]
    
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]

# Sidebar for chat history
def create_sidebar_chat_history():
    """Create sidebar with chat history"""
    with st.sidebar:
        st.header("💬 Chat History")
        
        if "saved_analyses" not in st.session_state:
            st.session_state.saved_analyses = []
        
        if st.session_state.saved_analyses:
            st.markdown("Click on any analysis to resume the conversation:")
            
            for i, analysis in enumerate(st.session_state.saved_analyses):
                with st.container():
                    if st.button(
                        f"📄 {analysis['file_name']}", 
                        key=f"sidebar_chat_{i}",
                        help=f"Resume chat about {analysis['file_name']}"
                    ):
                        # Load the selected analysis
                        st.session_state.current_analysis = analysis
                        st.session_state.chat_mode = True
                        st.session_state.chat_history = analysis.get('chat_history', [])
                        st.rerun()
                    
                    st.caption(f"💬 {len(analysis.get('chat_history', []))} messages • {analysis['file_type'].upper()}")
                    
                st.markdown("---")
        else:
            st.info("🔍 No saved analyses yet. Upload and analyze files to start building your chat history!")
        
        # Clear all history button
        if st.session_state.saved_analyses:
            if st.button("🗑️ Clear All History", type="secondary"):
                st.session_state.saved_analyses = []
                clear_analysis_state()
                st.rerun()

# Main App
def main():
    # Initialize session states
    if "saved_analyses" not in st.session_state:
        st.session_state.saved_analyses = []
    if "chat_mode" not in st.session_state:
        st.session_state.chat_mode = False
    if "current_analysis" not in st.session_state:
        st.session_state.current_analysis = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "analysis_completed" not in st.session_state:
        st.session_state.analysis_completed = False

    # Hero Section
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">🤖 Ask Real Estate AI</div>
        <div class="hero-subtitle">Upload any file and get expert real estate analysis powered by advanced AI</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Check for missing dependencies
    missing_deps = []
    if PyPDF2 is None:
        missing_deps.append("PyPDF2")
    if Document is None:
        missing_deps.append("python-docx")
    
    if missing_deps:
        st.error(f"⚠️ Missing Dependencies: Please install {', '.join(missing_deps)}")

    # Show main interface or continue existing chat
    if not st.session_state.chat_mode:
        show_file_analysis_interface()
    else:
        show_combined_analysis_and_chat()

def show_file_analysis_interface():
    """Show the main file analysis interface"""
    
    # Supported file types info
    st.markdown("""
    <div class="supported-files">
        <h4>🗂️ Supported File Types</h4>
        <span class="file-type-badge">📸 Images (PNG, JPG, JPEG)</span>
        <span class="file-type-badge">📄 PDF Documents</span>
        <span class="file-type-badge">📝 Word Documents (DOCX)</span>
        <span class="file-type-badge">📊 CSV Files</span>
        <span class="file-type-badge">📋 Text Files</span>
        <span class="file-type-badge">📈 Excel Files</span>
    </div>
    """, unsafe_allow_html=True)
    
    # File upload section
    st.markdown("### 📁 Upload Your Files")
    
    # Use a key that changes when we want to reset the uploader
    uploader_key = f"file_uploader_{st.session_state.get('uploader_reset_counter', 0)}"
    
    uploaded_files = st.file_uploader(
        "Choose files to analyze",
        type=['pdf', 'docx', 'txt', 'csv', 'xlsx', 'xls', 'png', 'jpg', 'jpeg', 'gif', 'bmp'],
        accept_multiple_files=True,
        help="Upload real estate documents, images, or data files for expert AI analysis",
        key=uploader_key
    )
    
    user_question = st.text_area(
        "🤔 What would you like to know about your files?",
        placeholder="Examples:\n• Analyze this property listing and investment potential\n• What insights can you extract from this market report?\n• Evaluate this floor plan for space efficiency\n• What are the key trends in this data?",
        height=120,
        help="Be specific about what you want to know!",
        key=f"question_input_{st.session_state.get('uploader_reset_counter', 0)}"
    )
    
    # Only show analyze button
    if st.button("🔍 Analyze Files", type="primary", use_container_width=True):
        if uploaded_files and user_question:
            analyze_files(uploaded_files, user_question)
        elif not uploaded_files:
            st.warning("📁 Please upload at least one file to analyze.")
        elif not user_question:
            st.warning("🤔 Please enter a question about your files.")

def analyze_files(uploaded_files, user_question):
    """Analyze uploaded files and show results"""
    
    all_analyses = []
    
    for uploaded_file in uploaded_files:
        with st.spinner(f"🤖 Analyzing {uploaded_file.name}..."):
            
            # Display file info
            st.markdown(f"""
            <div class="file-info-card">
                <strong>📄 {uploaded_file.name}</strong> 
                <span style="color: #666;">({uploaded_file.size:,} bytes, {uploaded_file.type})</span>
            </div>
            """, unsafe_allow_html=True)
            
            file_extension = uploaded_file.name.split('.')[-1].lower()
            analysis_result = ""
            
            # Handle different file types (same as before)
            if file_extension in ['png', 'jpg', 'jpeg', 'gif', 'bmp']:
                st.image(uploaded_file, caption=f"📷 {uploaded_file.name}", width=400)
                analysis_result = analyze_image_with_groq(uploaded_file, user_question)
                
            elif file_extension == 'pdf':
                text_content = extract_text_from_pdf(uploaded_file)
                if text_content and not text_content.startswith("Error") and not text_content.startswith("PyPDF2"):
                    st.text_area("📄 Extracted Text Preview", text_content[:500] + "...", height=100, disabled=True)
                    analysis_result = analyze_document_with_groq(text_content, user_question, "PDF")
                else:
                    analysis_result = text_content or "Could not extract text from PDF file."
                    
            elif file_extension == 'docx':
                text_content = extract_text_from_docx(uploaded_file)
                if text_content and not text_content.startswith("Error") and not text_content.startswith("python-docx"):
                    st.text_area("📝 Extracted Text Preview", text_content[:500] + "...", height=100, disabled=True)
                    analysis_result = analyze_document_with_groq(text_content, user_question, "Word Document")
                else:
                    analysis_result = text_content or "Could not extract text from Word document."
                    
            elif file_extension == 'txt':
                try:
                    text_content = str(uploaded_file.getvalue(), "utf-8")
                    st.text_area("📋 Text Content Preview", text_content[:500] + "...", height=100, disabled=True)
                    analysis_result = analyze_document_with_groq(text_content, user_question, "Text File")
                except Exception as e:
                    analysis_result = f"Error reading text file: {str(e)}"
                
            elif file_extension in ['csv', 'xlsx', 'xls']:
                try:
                    if file_extension == 'csv':
                        df = pd.read_csv(uploaded_file)
                    else:
                        df = pd.read_excel(uploaded_file)
                    
                    st.markdown("**📊 Data Preview:**")
                    st.dataframe(df.head(10), use_container_width=True)
                    
                    data_summary = f"""
                    Dataset Information:
                    - Total Rows: {df.shape[0]:,}
                    - Total Columns: {df.shape[1]}
                    - Column Names: {', '.join(df.columns.tolist())}
                    - Data Types: {df.dtypes.to_dict()}
                    - Missing Values: {df.isnull().sum().to_dict()}
                    - Sample Records: {df.head(5).to_string()}
                    """
                    
                    numeric_df = df.select_dtypes(include=[np.number])
                    if not numeric_df.empty:
                        data_summary += f"\n- Numeric Statistics:\n{numeric_df.describe().to_string()}"
                    
                    analysis_result = analyze_document_with_groq(data_summary, user_question, f"{file_extension.upper()} Data File")
                    
                except Exception as e:
                    analysis_result = f"Error reading data file: {str(e)}"
            
            # Store analysis for each file
            if analysis_result:
                all_analyses.append({
                    "file_name": uploaded_file.name,
                    "file_type": file_extension,
                    "question": user_question,
                    "analysis": analysis_result
                })
    
    # Switch to combined view
    if all_analyses:
        # Store analysis and switch to chat mode
        combined_analysis = {
            "analyses": all_analyses,
            "chat_history": [
                {"role": "user", "content": user_question},
                {"role": "assistant", "content": "\n\n---\n\n".join([f"**Analysis of {a['file_name']}:**\n{a['analysis']}" for a in all_analyses])}
            ]
        }
        
        st.session_state.current_analysis = combined_analysis
        st.session_state.chat_history = combined_analysis['chat_history']
        st.session_state.chat_mode = True
        st.rerun()

def show_combined_analysis_and_chat():
    """Show file analysis and chat interface together"""
    
    if not st.session_state.current_analysis:
        st.error("No analysis found. Please upload and analyze files first.")
        if st.button("🔄 Start New Analysis"):
            st.session_state.chat_mode = False
            st.rerun()
        return
    
    st.markdown("### 💬 Real Estate Analysis & AI Assistant")
    
    # Display chat history (includes both initial analysis and follow-up questions)
    for message in st.session_state.chat_history:
        with st.chat_message(message['role']):
            st.write(message['content'])
    
    # Red "New File Analysis" button above chat input
    if st.button("🔄 New File Analysis", type="primary", use_container_width=True, key="new_analysis_top"):
        # Save current conversation to sidebar
        if st.session_state.current_analysis and 'analyses' in st.session_state.current_analysis:
            for analysis in st.session_state.current_analysis['analyses']:
                saved_analysis = {
                    "file_name": analysis['file_name'],
                    "file_type": analysis['file_type'],
                    "original_question": analysis['question'],
                    "initial_analysis": analysis['analysis'],
                    "chat_history": st.session_state.chat_history
                }
                st.session_state.saved_analyses.append(saved_analysis)
        
        # Clear states and go back to file analysis
        clear_analysis_state()
        st.session_state.chat_mode = False
        # Reset file uploader
        if 'uploader_reset_counter' not in st.session_state:
            st.session_state.uploader_reset_counter = 0
        st.session_state.uploader_reset_counter += 1
        st.rerun()
    
    # Chat input at the bottom
    user_input = st.chat_input("Ask follow-up questions about your analysis...")
    
    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        
        # Get AI response
        with st.spinner("🤖 Thinking..."):
            # Create context from the initial analysis
            context_parts = []
            if 'analyses' in st.session_state.current_analysis:
                for analysis in st.session_state.current_analysis['analyses']:
                    context_parts.append(f"Analysis of {analysis['file_name']}: {analysis['analysis']}")
            
            context = "\n\n".join(context_parts)
            ai_response = get_ai_followup_response(user_input, context)
            
            st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
        
        # Update current analysis with new chat
        st.session_state.current_analysis['chat_history'] = st.session_state.chat_history
        
        st.rerun()

if __name__ == "__main__":
    create_sidebar_chat_history()
    main()
