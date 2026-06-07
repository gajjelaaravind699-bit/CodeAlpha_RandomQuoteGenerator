"""
╔══════════════════════════════════════════════════════════════╗
║          CodeAlpha Random Quote Generator                    ║
║          Author  : Your Name                                 ║
║          Project : CodeAlpha Python Internship               ║
║          Version : 1.0.0                                     ║
╚══════════════════════════════════════════════════════════════╝

A professional Random Quote Generator built with Python & Streamlit.
Features: Categories, Search, Dark/Light Mode, Favorites, Statistics,
Copy-to-Clipboard, and a responsive modern UI.
"""

import json
import random
import streamlit as st
from pathlib import Path

# ─────────────────────────────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="QuoteAlpha | Random Quote Generator",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

QUOTES_FILE = Path(__file__).parent / "quotes.json"
CATEGORIES = ["All", "Motivation", "Success", "Life", "Study"]
CATEGORY_ICONS = {
    "All": "✦",
    "Motivation": "🔥",
    "Success": "🏆",
    "Life": "🌿",
    "Study": "📚",
}


# ─────────────────────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────────────────────
@st.cache_data
def load_quotes() -> list[dict]:
    """Load quotes from the JSON file. Returns a list of quote dicts."""
    try:
        with open(QUOTES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error("❌ quotes.json not found. Please ensure it is in the project directory.")
        return []
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse quotes.json: {e}")
        return []


def filter_quotes(quotes: list[dict], category: str, search_term: str) -> list[dict]:
    """
    Filter quotes based on selected category and search term.

    Args:
        quotes: Full list of quote dictionaries.
        category: Selected category string ("All" returns every quote).
        search_term: Text to search within quote body and author name.

    Returns:
        Filtered list of quote dictionaries.
    """
    filtered = quotes

    # Apply category filter
    if category != "All":
        filtered = [q for q in filtered if q.get("category") == category]

    # Apply search filter (case-insensitive)
    if search_term.strip():
        term = search_term.strip().lower()
        filtered = [
            q for q in filtered
            if term in q.get("quote", "").lower() or term in q.get("author", "").lower()
        ]

    return filtered


# ─────────────────────────────────────────────────────────────
# SESSION STATE INITIALISATION
# ─────────────────────────────────────────────────────────────
def init_session_state(quotes: list[dict]) -> None:
    """
    Initialise all Streamlit session-state keys on first run.

    Args:
        quotes: Full list of loaded quotes.
    """
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True

    if "favorites" not in st.session_state:
        st.session_state.favorites = []   # list of quote dicts

    if "current_quote" not in st.session_state and quotes:
        st.session_state.current_quote = random.choice(quotes)

    if "page" not in st.session_state:
        st.session_state.page = "Home"

    if "copy_feedback" not in st.session_state:
        st.session_state.copy_feedback = False


# ─────────────────────────────────────────────────────────────
# THEMING  (CSS)
# ─────────────────────────────────────────────────────────────
def inject_css(dark: bool) -> None:
    """
    Inject custom CSS for Dark / Light mode and all UI styling.

    Args:
        dark: True = dark mode, False = light mode.
    """
    if dark:
        bg          = "#0e1117"
        card_bg     = "#1a1d27"
        card_border = "#2e3148"
        text_main   = "#f0f2ff"
        text_sub    = "#9ba3c7"
        accent      = "#7c6af7"
        accent2     = "#5eb8ff"
        btn_bg      = "#7c6af7"
        btn_hover   = "#6a59e0"
        sidebar_bg  = "#12151f"
        tag_bg      = "#2a2d42"
        shadow      = "0 8px 40px rgba(124,106,247,0.18)"
        fav_btn     = "#ff6b8a"
        fav_btn_h   = "#e85577"
    else:
        bg          = "#f5f6fa"
        card_bg     = "#ffffff"
        card_border = "#e2e6f0"
        text_main   = "#1a1d2e"
        text_sub    = "#6b728e"
        accent      = "#6c5ce7"
        accent2     = "#0984e3"
        btn_bg      = "#6c5ce7"
        btn_hover   = "#5a4bd1"
        sidebar_bg  = "#eef0f8"
        tag_bg      = "#e8eaf6"
        shadow      = "0 8px 40px rgba(108,92,231,0.12)"
        fav_btn     = "#e84393"
        fav_btn_h   = "#c9316f"

    css = f"""
    <style>
    /* ── Google Fonts ── */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,600;1,400&family=DM+Sans:wght@300;400;500;600&display=swap');

    /* ── Global Reset ── */
    html, body, [class*="css"] {{
        font-family: 'DM Sans', sans-serif;
        background-color: {bg} !important;
        color: {text_main} !important;
    }}

    /* ── Hide default Streamlit chrome ── */
    #MainMenu, footer, header {{ visibility: hidden; }}
    .stDeployButton {{ display: none; }}
    [data-testid="stToolbar"] {{ display: none; }}

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {{
        background-color: {sidebar_bg} !important;
        border-right: 1px solid {card_border};
    }}
    [data-testid="stSidebar"] * {{ color: {text_main} !important; }}

    /* ── Main content padding ── */
    .main .block-container {{
        padding: 2rem 2.5rem 4rem;
        max-width: 900px;
    }}

    /* ── App Title ── */
    .app-title {{
        font-family: 'Playfair Display', serif;
        font-size: 2.6rem;
        font-weight: 600;
        color: {accent};
        letter-spacing: -0.5px;
        line-height: 1.2;
        margin-bottom: 0.2rem;
    }}
    .app-subtitle {{
        color: {text_sub};
        font-size: 0.95rem;
        margin-bottom: 2rem;
        letter-spacing: 0.04em;
    }}

    /* ── Quote Card ── */
    .quote-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 20px;
        padding: 2.8rem 3rem;
        box-shadow: {shadow};
        position: relative;
        overflow: hidden;
        transition: transform 0.25s ease, box-shadow 0.25s ease;
        animation: fadeSlide 0.45s ease;
    }}
    .quote-card:hover {{
        transform: translateY(-4px);
        box-shadow: 0 16px 60px rgba(124,106,247,0.22);
    }}
    @keyframes fadeSlide {{
        from {{ opacity: 0; transform: translateY(18px); }}
        to   {{ opacity: 1; transform: translateY(0); }}
    }}

    /* Accent stripe */
    .quote-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 5px; height: 100%;
        background: linear-gradient(180deg, {accent}, {accent2});
        border-radius: 20px 0 0 20px;
    }}

    /* Big quotation mark */
    .quote-card::after {{
        content: '\\201C';
        font-family: 'Playfair Display', serif;
        font-size: 11rem;
        color: {accent};
        opacity: 0.07;
        position: absolute;
        top: -2.5rem; left: 1.5rem;
        line-height: 1;
        pointer-events: none;
    }}

    .quote-text {{
        font-family: 'Playfair Display', serif;
        font-size: 1.45rem;
        font-style: italic;
        line-height: 1.75;
        color: {text_main};
        margin-bottom: 1.5rem;
        position: relative;
        z-index: 1;
    }}
    .quote-author {{
        font-size: 0.95rem;
        font-weight: 600;
        color: {accent};
        letter-spacing: 0.06em;
        text-transform: uppercase;
    }}
    .quote-category-tag {{
        display: inline-block;
        background: {tag_bg};
        color: {text_sub};
        font-size: 0.78rem;
        font-weight: 500;
        padding: 0.25rem 0.75rem;
        border-radius: 99px;
        margin-top: 0.9rem;
        letter-spacing: 0.05em;
    }}

    /* ── Buttons ── */
    .stButton > button {{
        background: {btn_bg} !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.55rem 1.6rem !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        letter-spacing: 0.03em;
        cursor: pointer;
        transition: background 0.2s ease, transform 0.15s ease !important;
    }}
    .stButton > button:hover {{
        background: {btn_hover} !important;
        transform: translateY(-2px) !important;
    }}
    .stButton > button:active {{
        transform: translateY(0) !important;
    }}

    /* ── Favourite button ── */
    .fav-btn > button {{
        background: {fav_btn} !important;
    }}
    .fav-btn > button:hover {{
        background: {fav_btn_h} !important;
    }}

    /* ── Stat Card ── */
    .stat-card {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        text-align: center;
        box-shadow: {shadow};
        transition: transform 0.2s ease;
    }}
    .stat-card:hover {{ transform: translateY(-3px); }}
    .stat-number {{
        font-family: 'Playfair Display', serif;
        font-size: 2.4rem;
        font-weight: 600;
        color: {accent};
        line-height: 1;
    }}
    .stat-label {{
        font-size: 0.8rem;
        color: {text_sub};
        margin-top: 0.4rem;
        letter-spacing: 0.07em;
        text-transform: uppercase;
    }}

    /* ── Divider ── */
    .section-divider {{
        border: none;
        border-top: 1px solid {card_border};
        margin: 2rem 0;
    }}

    /* ── Search & Select ── */
    .stTextInput > div > div > input,
    .stSelectbox > div > div {{
        background: {card_bg} !important;
        border-color: {card_border} !important;
        color: {text_main} !important;
        border-radius: 12px !important;
    }}

    /* ── Counter badge ── */
    .counter-badge {{
        display: inline-block;
        background: linear-gradient(135deg, {accent}, {accent2});
        color: #fff;
        font-size: 0.82rem;
        font-weight: 700;
        padding: 0.28rem 0.85rem;
        border-radius: 99px;
        letter-spacing: 0.04em;
    }}

    /* ── Fav item card ── */
    .fav-item {{
        background: {card_bg};
        border: 1px solid {card_border};
        border-radius: 14px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.9rem;
        transition: transform 0.2s ease;
    }}
    .fav-item:hover {{ transform: translateX(4px); }}

    /* ── Footer ── */
    .footer {{
        margin-top: 4rem;
        padding-top: 1.5rem;
        border-top: 1px solid {card_border};
        text-align: center;
        color: {text_sub};
        font-size: 0.82rem;
        line-height: 1.9;
    }}
    .footer a {{
        color: {accent};
        text-decoration: none;
    }}
    .footer a:hover {{ text-decoration: underline; }}

    /* ── Sidebar nav button ── */
    .nav-btn > button {{
        width: 100% !important;
        text-align: left !important;
        background: transparent !important;
        color: {text_main} !important;
        border-radius: 10px !important;
        padding: 0.55rem 1rem !important;
        font-size: 0.92rem !important;
        font-weight: 500 !important;
        border: none !important;
        margin-bottom: 0.25rem;
    }}
    .nav-btn > button:hover {{
        background: {tag_bg} !important;
        color: {accent} !important;
    }}
    .nav-btn-active > button {{
        background: {tag_bg} !important;
        color: {accent} !important;
        font-weight: 700 !important;
    }}

    /* ── Scrollbar ── */
    ::-webkit-scrollbar {{ width: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: {card_border}; border-radius: 99px; }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────
# COMPONENTS
# ─────────────────────────────────────────────────────────────
def render_quote_card(quote: dict) -> None:
    """
    Render a styled HTML quote card for the given quote dict.

    Args:
        quote: Dictionary with keys 'quote', 'author', 'category'.
    """
    icon = CATEGORY_ICONS.get(quote.get("category", ""), "✦")
    html = f"""
    <div class="quote-card">
        <div class="quote-text">
            {quote.get('quote', '')}
        </div>
        <div class="quote-author">— {quote.get('author', 'Unknown')}</div>
        <div class="quote-category-tag">{icon} {quote.get('category', '')}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


def render_stat_card(number: int | str, label: str) -> str:
    """Return HTML string for a statistics card."""
    return f"""
    <div class="stat-card">
        <div class="stat-number">{number}</div>
        <div class="stat-label">{label}</div>
    </div>
    """


def is_favorite(quote: dict) -> bool:
    """Return True if the given quote is already in favorites."""
    return any(
        f.get("quote") == quote.get("quote") and f.get("author") == quote.get("author")
        for f in st.session_state.favorites
    )


def add_favorite(quote: dict) -> None:
    """Add a quote to session-state favorites if not already present."""
    if not is_favorite(quote):
        st.session_state.favorites.append(quote)


def remove_favorite(quote: dict) -> None:
    """Remove a quote from session-state favorites."""
    st.session_state.favorites = [
        f for f in st.session_state.favorites
        if not (f.get("quote") == quote.get("quote") and f.get("author") == quote.get("author"))
    ]


# ─────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────
def render_sidebar(all_quotes: list[dict]) -> None:
    """
    Render the left sidebar with navigation, mode toggle, and mini-stats.

    Args:
        all_quotes: Full list of quotes (used for stats).
    """
    with st.sidebar:
        # Logo / brand
        st.markdown(
            "<div style='font-family:Playfair Display,serif;font-size:1.6rem;"
            "font-weight:600;margin-bottom:0.3rem;'>✦ QuoteAlpha</div>"
            "<div style='font-size:0.78rem;opacity:0.55;margin-bottom:1.5rem;"
            "letter-spacing:0.06em;text-transform:uppercase;'>CodeAlpha Internship</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")

        # Navigation
        st.markdown(
            "<div style='font-size:0.75rem;font-weight:700;letter-spacing:0.1em;"
            "text-transform:uppercase;opacity:0.5;margin-bottom:0.5rem;'>Navigation</div>",
            unsafe_allow_html=True,
        )

        pages = [("🏠  Home", "Home"), ("⭐  Favorites", "Favorites"), ("📊  Statistics", "Statistics")]
        for label, key in pages:
            is_active = st.session_state.page == key
            css_class = "nav-btn-active" if is_active else "nav-btn"
            st.markdown(f"<div class='{css_class}'>", unsafe_allow_html=True)
            if st.button(label, key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # Dark / Light mode toggle
        mode_label = "☀️  Switch to Light Mode" if st.session_state.dark_mode else "🌙  Switch to Dark Mode"
        if st.button(mode_label, use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()

        st.markdown("---")

        # Quick stats in sidebar
        total  = len(all_quotes)
        favs   = len(st.session_state.favorites)
        cats   = len(CATEGORIES) - 1   # exclude "All"
        st.markdown(
            f"<div style='font-size:0.78rem;opacity:0.55;letter-spacing:0.08em;"
            f"text-transform:uppercase;font-weight:700;margin-bottom:0.6rem;'>Quick Stats</div>"
            f"<div style='font-size:0.88rem;line-height:2.1;'>"
            f"📝 &nbsp;{total} Total Quotes<br>"
            f"🗂  &nbsp;{cats} Categories<br>"
            f"⭐ &nbsp;{favs} Favourites"
            f"</div>",
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.markdown(
            "<div style='font-size:0.72rem;opacity:0.4;text-align:center;line-height:1.7;'>"
            "Built with ❤️ using Python & Streamlit<br>"
            "CodeAlpha Python Internship 2024"
            "</div>",
            unsafe_allow_html=True,
        )


# ─────────────────────────────────────────────────────────────
# PAGES
# ─────────────────────────────────────────────────────────────
def page_home(all_quotes: list[dict]) -> None:
    """
    Render the Home page: filters, quote card, action buttons.

    Args:
        all_quotes: Full list of loaded quotes.
    """
    # Header
    st.markdown(
        "<div class='app-title'>Random Quote Generator</div>"
        "<div class='app-subtitle'>✦ Discover wisdom, one quote at a time</div>",
        unsafe_allow_html=True,
    )

    # ── Filters row ──
    col_cat, col_search = st.columns([1, 2])
    with col_cat:
        category = st.selectbox(
            "Category",
            CATEGORIES,
            format_func=lambda c: f"{CATEGORY_ICONS[c]}  {c}",
            key="selected_category",
        )
    with col_search:
        search_term = st.text_input("🔍  Search by quote or author", key="search_term", placeholder="e.g. Einstein, success…")

    # Filter quotes
    visible = filter_quotes(all_quotes, category, search_term)

    # Quote counter badge
    count_label = "quote" if len(visible) == 1 else "quotes"
    st.markdown(
        f"<div style='margin:0.4rem 0 1.2rem;'>"
        f"<span class='counter-badge'>{len(visible)} {count_label} available</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    if not visible:
        st.warning("No quotes found for the current filters. Try adjusting your search or category.")
        return

    # Ensure current_quote is in the visible pool; if not, pick a new one
    if st.session_state.current_quote not in visible:
        st.session_state.current_quote = random.choice(visible)

    # ── Quote Card ──
    render_quote_card(st.session_state.current_quote)

    st.markdown("<div style='height:1rem;'></div>", unsafe_allow_html=True)

    # ── Action Buttons ──
    col_new, col_fav, col_copy = st.columns([1, 1, 1])

    with col_new:
        if st.button("✦  New Quote", use_container_width=True, key="new_quote_btn"):
            # Ensure the new quote is different from the current one
            pool = [q for q in visible if q != st.session_state.current_quote]
            if pool:
                st.session_state.current_quote = random.choice(pool)
            else:
                st.session_state.current_quote = random.choice(visible)
            st.session_state.copy_feedback = False
            st.rerun()

    with col_fav:
        already_fav = is_favorite(st.session_state.current_quote)
        fav_label   = "★  Remove Favourite" if already_fav else "☆  Add to Favourites"
        st.markdown("<div class='fav-btn'>", unsafe_allow_html=True)
        if st.button(fav_label, use_container_width=True, key="fav_btn"):
            if already_fav:
                remove_favorite(st.session_state.current_quote)
                st.toast("Removed from Favourites", icon="🗑️")
            else:
                add_favorite(st.session_state.current_quote)
                st.toast("Added to Favourites!", icon="⭐")
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

    with col_copy:
        q  = st.session_state.current_quote
        clipboard_text = f'"{q.get("quote", "")}" — {q.get("author", "Unknown")}'
        # Streamlit's st.code with clipboard is the best native approach
        if st.button("📋  Copy Quote", use_container_width=True, key="copy_btn"):
            st.session_state.copy_feedback = True
            st.rerun()

    # Inline copy-text display (native clipboard-friendly)
    if st.session_state.get("copy_feedback"):
        q = st.session_state.current_quote
        copy_str = f'"{q.get("quote", "")}" — {q.get("author", "Unknown")}'
        st.code(copy_str, language=None)
        st.caption("☝️ Click the copy icon on the top-right of the box above.")


def page_favorites() -> None:
    """Render the Favourites page with all saved quotes and remove buttons."""
    st.markdown(
        "<div class='app-title'>⭐ Favourites</div>"
        "<div class='app-subtitle'>Quotes you've saved for inspiration</div>",
        unsafe_allow_html=True,
    )

    favs = st.session_state.favorites

    if not favs:
        st.info("You haven't added any favourites yet. Head to Home, discover a quote you love, and tap **☆ Add to Favourites**!")
        return

    count_label = "quote" if len(favs) == 1 else "quotes"
    st.markdown(
        f"<div style='margin-bottom:1.4rem;'>"
        f"<span class='counter-badge'>⭐  {len(favs)} saved {count_label}</span>"
        f"</div>",
        unsafe_allow_html=True,
    )

    for idx, quote in enumerate(favs):
        icon = CATEGORY_ICONS.get(quote.get("category", ""), "✦")
        st.markdown(
            f"<div class='fav-item'>"
            f"<div style='font-family:Playfair Display,serif;font-style:italic;"
            f"font-size:1.05rem;line-height:1.7;margin-bottom:0.5rem;'>"
            f"&ldquo;{quote.get('quote', '')}&rdquo;</div>"
            f"<div style='font-size:0.85rem;font-weight:600;opacity:0.7;'>"
            f"— {quote.get('author', 'Unknown')} &nbsp;|&nbsp; {icon} {quote.get('category', '')}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )

        col_remove, _ = st.columns([1, 4])
        with col_remove:
            if st.button("🗑️ Remove", key=f"remove_{idx}", use_container_width=True):
                remove_favorite(quote)
                st.toast("Removed from Favourites.", icon="🗑️")
                st.rerun()


def page_statistics(all_quotes: list[dict]) -> None:
    """
    Render the Statistics page with total counts and category breakdown.

    Args:
        all_quotes: Full list of loaded quotes.
    """
    st.markdown(
        "<div class='app-title'>📊 Statistics</div>"
        "<div class='app-subtitle'>A breakdown of your quote library</div>",
        unsafe_allow_html=True,
    )

    total = len(all_quotes)
    favs  = len(st.session_state.favorites)

    # Top stats row
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(render_stat_card(total, "Total Quotes"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_stat_card(favs, "Favourites"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_stat_card(len(CATEGORIES) - 1, "Categories"), unsafe_allow_html=True)

    st.markdown("<div style='height:1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Per-category breakdown
    st.markdown(
        "<div style='font-size:1.15rem;font-weight:700;margin-bottom:1rem;'>"
        "Quotes per Category</div>",
        unsafe_allow_html=True,
    )

    real_cats = [c for c in CATEGORIES if c != "All"]
    cols = st.columns(len(real_cats))

    for col, cat in zip(cols, real_cats):
        count = len([q for q in all_quotes if q.get("category") == cat])
        pct   = round(count / total * 100) if total else 0
        icon  = CATEGORY_ICONS.get(cat, "")
        with col:
            st.markdown(
                render_stat_card(f"{count}", f"{icon} {cat} ({pct}%)"),
                unsafe_allow_html=True,
            )

    st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

    # Favourite breakdown by category
    if favs:
        st.markdown(
            "<div style='font-size:1.15rem;font-weight:700;margin-bottom:1rem;'>"
            "Favourites by Category</div>",
            unsafe_allow_html=True,
        )
        fav_cats: dict[str, int] = {}
        for q in st.session_state.favorites:
            cat = q.get("category", "Unknown")
            fav_cats[cat] = fav_cats.get(cat, 0) + 1

        f_cols = st.columns(max(len(fav_cats), 1))
        for col, (cat, cnt) in zip(f_cols, fav_cats.items()):
            icon = CATEGORY_ICONS.get(cat, "")
            with col:
                st.markdown(
                    render_stat_card(cnt, f"{icon} {cat}"),
                    unsafe_allow_html=True,
                )
    else:
        st.info("Add some quotes to Favourites to see your personal breakdown here.")


def render_footer() -> None:
    """Render the app footer with project and author information."""
    st.markdown(
        "<div class='footer'>"
        "✦ <strong>QuoteAlpha — Random Quote Generator</strong><br>"
        "CodeAlpha Python Internship Project &nbsp;|&nbsp; Built with "
        "<a href='https://streamlit.io' target='_blank'>Streamlit</a> &amp; Python 3<br>"
        "<span style='opacity:0.5;font-size:0.78rem;'>"
        "© 2024 · Your Name · "
        "<a href='https://github.com/yourusername/CodeAlpha_RandomQuoteGenerator' target='_blank'>"
        "GitHub Repository</a>"
        "</span>"
        "</div>",
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────────────────────
# MAIN ENTRY POINT
# ─────────────────────────────────────────────────────────────
def main() -> None:
    """
    Main application entry point.
    Orchestrates loading, state init, CSS injection, and page routing.
    """
    # 1. Load quote data
    all_quotes = load_quotes()
    if not all_quotes:
        st.stop()

    # 2. Initialise session state
    init_session_state(all_quotes)

    # 3. Apply theme CSS
    inject_css(dark=st.session_state.dark_mode)

    # 4. Render sidebar
    render_sidebar(all_quotes)

    # 5. Route to correct page
    page = st.session_state.get("page", "Home")

    if page == "Home":
        page_home(all_quotes)
    elif page == "Favorites":
        page_favorites()
    elif page == "Statistics":
        page_statistics(all_quotes)

    # 6. Footer (shown on every page)
    render_footer()


# ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    main()
