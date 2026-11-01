"""
Custom CSS for Streamlit UI
"""


def load_css():
    return """
<style>

/* =====================================
   Hide Streamlit Elements
===================================== */

#MainMenu{
    visibility:hidden;
}

footer{
    visibility:hidden;
}

/* Keep header visible for Streamlit widgets */

header{
    background:transparent;
}

/* =====================================
   Main Layout
===================================== */

.block-container{
    max-width:1400px;
    padding-top:1.2rem;
    padding-bottom:2rem;
}

/* =====================================
   Metrics
===================================== */

div[data-testid="stMetric"]{
    border:1px solid #30363d;
    border-radius:12px;
    padding:12px;
}

div[data-testid="stMetricLabel"]{
    font-size:14px;
    font-weight:500;
}

div[data-testid="stMetricValue"]{
    font-weight:700;
}

/* =====================================
   Buttons
===================================== */

.stButton > button{
    width:100%;
    border-radius:8px;
    font-weight:600;
}

/* =====================================
   File Uploader
===================================== */

[data-testid="stFileUploader"]{
    border:2px dashed #4b5563;
    border-radius:10px;
    padding:8px;
}

[data-testid="stFileUploader"] section{
    border:none !important;
    background:transparent !important;
}

[data-testid="stFileUploader"] button{
    border-radius:8px;
}

/* =====================================
   Chat Messages
===================================== */

div[data-testid="stChatMessage"]{
    border:1px solid #30363d;
    border-radius:12px;
    padding:12px;
    margin-bottom:12px;
}

/* =====================================
   Chat Input
===================================== */

[data-testid="stChatInput"]{
    border-top:1px solid #30363d;
    padding-top:8px;
}

/* =====================================
   Source Cards
===================================== */

.source-card{
    border-left:4px solid #3b82f6;
    padding:10px;
    border-radius:8px;
    margin-bottom:8px;
}

/* =====================================
   Document Cards
===================================== */

.doc-card{
    border:1px solid #30363d;
    border-radius:8px;
    padding:10px 12px;
    margin-bottom:8px;
}

/* =====================================
   Divider
===================================== */

hr{
    margin:1rem 0;
}

/* =====================================
   Success / Error
===================================== */

[data-testid="stSuccess"]{
    border-radius:8px;
}

[data-testid="stError"]{
    border-radius:8px;
}

/* =====================================
   Scrollbar
===================================== */

::-webkit-scrollbar{
    width:8px;
}

::-webkit-scrollbar-thumb{
    background:#666;
    border-radius:10px;
}

::-webkit-scrollbar-track{
    background:transparent;
}

</style>
"""