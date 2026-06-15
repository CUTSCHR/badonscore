"""
THE BATTLE AT BANDON — Tournament Scoring App
The 6th Annual Chubbs Peterson Invitational
"""

import streamlit as st
import pandas as pd
import json
import os
import math
import requests
import base64

# ─── Page Config ──────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Battle at Bandon 2026",
    page_icon="⛳",
    layout="wide",
    initial_sidebar_state="auto",
)

# ─── CSS: Bright / Masters-inspired with earth-tone accents ───────────────────

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:wght@700;900&family=Material+Symbols+Rounded&display=swap');

    /* === Base === */
    .stApp { background: #f5f0e8; }
    [data-testid="stSidebar"] {
        background: #1a3a1a;
        border-right: 2px solid #2a5a2a;
    }
    [data-testid="stSidebar"] * { color: #e8e0d4 !important; }
    [data-testid="stSidebar"] .stRadio label span { color: #e8e0d4 !important; }
    [data-testid="stSidebar"] .stRadio label:hover span { color: #fff !important; }
    [data-testid="stSidebar"] .sidebar-shooter { color: #1a6b9a !important; }
    [data-testid="stSidebar"] .sidebar-gilmore { color: #9a1a1a !important; }

    /* sidebar expand button (when sidebar is collapsed) - the button IS the testid element */
    button[data-testid="stExpandSidebarButton"] { display: flex !important; align-items: center !important; justify-content: center !important; visibility: visible !important; z-index: 999999 !important; position: fixed !important; top: 14px !important; left: 14px !important; background: #2a5a2a !important; color: transparent !important; border-radius: 6px !important; padding: 8px !important; font-size: 0 !important; width: 40px !important; height: 40px !important; cursor: pointer !important; border: 2px solid #f5f0e8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important; }
    button[data-testid="stExpandSidebarButton"] * { font-size: 0 !important; color: transparent !important; }
    button[data-testid="stExpandSidebarButton"]::after { content: '\\25B6'; font-size: 18px !important; color: #fff !important; }
    /* Also support older testid */
    [data-testid="collapsedControl"] { display: flex !important; visibility: visible !important; z-index: 999999 !important; position: fixed !important; top: 14px !important; left: 14px !important; }
    [data-testid="collapsedControl"] button { display: flex !important; align-items: center !important; justify-content: center !important; visibility: visible !important; background: #2a5a2a !important; color: transparent !important; border-radius: 6px !important; padding: 8px !important; font-size: 0 !important; width: 40px !important; height: 40px !important; cursor: pointer !important; border: 2px solid #f5f0e8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.3) !important; }
    [data-testid="collapsedControl"] button::after { content: '\\25B6'; font-size: 18px !important; color: #fff !important; }
    /* Hide collapse button material icon text */
    button[data-testid="stBaseButton-headerNoPadding"] { font-size: 0 !important; overflow: hidden !important; }
    [data-testid="stSidebarCollapseButton"] button { font-size: 0 !important; overflow: hidden !important; width: 32px !important; height: 32px !important; background: #2a5a2a !important; border-radius: 4px !important; color: transparent !important; display: flex !important; align-items: center !important; justify-content: center !important; }
    [data-testid="stSidebarCollapseButton"] button * { font-size: 0 !important; color: transparent !important; }
    [data-testid="stSidebarCollapseButton"] button::after { content: '\\25C0'; font-size: 14px !important; color: #fff !important; }

    h1, h2, h3 { font-family: 'Playfair Display', serif !important; color: #1a3a1a !important; }
    p, span, div, label, td, th { font-family: 'DM Sans', sans-serif !important; color: #1a3a1a; }

    /* remove watermark & footer */
    .viewerBadge_container__r5tak, footer, #MainMenu, .stDeployButton,
    div[data-testid="InputInstructions"], .stAppDeployButton,
    [data-testid="manage-app-button"], .styles_viewerBadge__CvC9N,
    ._profileContainer_gzau3_53, [class*="Keyboard"],
    div[class*="keyboard"], iframe[title*="keyboard"],
    div[data-testid="InputInstructions"] svg,
    div[data-testid="InputInstructions"] span,
    .stSelectbox div[data-testid="InputInstructions"],
    .stMultiSelect div[data-testid="InputInstructions"],
    div[data-baseweb="select"] + div[data-testid="InputInstructions"],
    [data-testid="stDecoration"],
    [data-testid="stStatusWidget"] { display: none !important; visibility: hidden !important; height: 0 !important; width: 0 !important; overflow: hidden !important; position: absolute !important; }
    /* Hide toolbar but keep expand button accessible (no display:none so fixed children render) */
    [data-testid="stToolbar"] { visibility: hidden !important; height: 0 !important; overflow: visible !important; position: absolute !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Multiselect chips - white text on green */
    [data-baseweb="tag"] { background-color: #2a5a2a !important; }
    [data-baseweb="tag"] span { color: #ffffff !important; }
    [data-baseweb="tag"] svg { fill: #ffffff !important; }
    [data-baseweb="tag"] [data-baseweb="tag-action"] { color: #ffffff !important; }

    /* === Hero === */
    .hero {
        background: linear-gradient(135deg, rgba(26,58,26,0.92), rgba(26,58,26,0.78)),
                    url('https://bandondunesgolf.com/wp-content/uploads/2024/06/HomePage_Header24_v2.jpg');
        background-size: cover; background-position: center;
        border-radius: 16px; padding: 56px 36px 44px; margin-bottom: 28px;
        border: 2px solid #2a5a2a; text-align: center;
    }
    .hero-title {
        font-family: 'Playfair Display', serif !important; font-size: 5rem !important; font-weight: 900 !important;
        color: #f5f0e8 !important; letter-spacing: 4px !important; margin: 0 !important;
        line-height: 1.1 !important;
    }
    .hero-sub {
        font-family: 'DM Sans', sans-serif; color: #c5b89a; font-size: 1.2rem;
        letter-spacing: 2px; text-transform: uppercase; margin-top: 8px;
    }

    /* === Cards === */
    .card {
        background: #ffffff; border: 1px solid #d4cfc5; border-radius: 12px;
        padding: 24px; margin-bottom: 16px; box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .card-title {
        font-size: 0.75rem; font-weight: 700; text-transform: uppercase;
        letter-spacing: 1.5px; color: #6b8f6b; margin-bottom: 8px;
    }

    /* === Section Headers === */
    .section-header {
        font-family: 'Playfair Display', serif; font-size: 1.8rem; font-weight: 900;
        color: #1a3a1a; text-align: center; margin: 24px 0 16px; padding: 12px 0;
        border-bottom: 2px solid #2a5a2a;
    }

    /* === Team colors === */
    .team-shooter { color: #1a6b9a; font-weight: 700; }
    .team-gilmore { color: #9a1a1a; font-weight: 700; }
    .team-shooter-bg {
        background: rgba(26,107,154,0.07); border-left: 3px solid #1a6b9a;
        padding: 12px; border-radius: 8px; margin: 8px 0;
    }
    .team-gilmore-bg {
        background: rgba(154,26,26,0.07); border-left: 3px solid #9a1a1a;
        padding: 12px; border-radius: 8px; margin: 8px 0;
    }

    /* === Team Score Card === */
    .team-score-box {
        text-align: center; padding: 24px; border-radius: 12px;
        background: #fff; border: 1px solid #d4cfc5;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .team-score-box h3 { margin: 0 0 8px; font-size: 1.2rem; }
    .team-score-box .score { font-family: 'Playfair Display', serif; font-size: 3rem; font-weight: 900; }

    /* === Scorecard table — white/Masters === */
    .sc-table {
        width: 100%; border-collapse: collapse;
        font-family: 'DM Sans', sans-serif; font-size: 0.8rem;
        background: #ffffff; border-radius: 8px; overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        table-layout: fixed;
    }
    .sc-table col:first-child { width: 90px; }
    .sc-table th {
        background: #2a5a2a; color: #f5f0e8;
        padding: 5px 4px; text-align: center;
        font-weight: 600; font-size: 0.7rem;
        text-transform: uppercase; letter-spacing: 0.3px;
    }
    .sc-table td {
        padding: 4px 3px; text-align: center;
        border-bottom: 1px solid #e8e4dc; color: #1a3a1a; font-size: 0.8rem;
    }
    .sc-table tr:nth-child(even) { background: #faf8f4; }
    .sc-table .par-row td { color: #4a7a4a; font-weight: 600; background: #f0ede5; }
    .sc-table .dot-row td { color: #c17a3a; font-size: 0.9rem; }
    .sc-table .net-row td { color: #6b8f6b; font-style: italic; }
    .sc-table .stab-row td { color: #2a5a2a; font-weight: 700; }
    .sc-table .player-header { text-align: left; font-weight: 700; padding: 6px 4px 2px; font-size: 0.75rem; white-space: nowrap; }
    .sc-table .player-header.team-shooter { color: #1a6b9a; }
    .sc-table .player-header.team-gilmore { color: #9a1a1a; }
    .sc-table .total-col { background: #1a4a1a !important; color: #ffffff !important; font-weight: 700; font-size: 0.75rem; }
    .sc-table .turn-col { background: #2a5a2a !important; color: #f5f0e8 !important; font-weight: 700; font-size: 0.75rem; }
    .sc-table thead .turn-col, .sc-table thead .total-col { background: #1a3a1a !important; color: #ffffff !important; font-size: 0.7rem; letter-spacing: 0.5px; }

    /* === Schedule table — white === */
    .sched-table {
        width: 100%; border-collapse: collapse;
        background: #ffffff; border-radius: 8px; overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        font-family: 'DM Sans', sans-serif; font-size: 0.85rem;
    }
    .sched-table th {
        background: #2a5a2a; color: #f5f0e8;
        padding: 10px 12px; text-align: left;
        font-weight: 600; text-transform: uppercase; font-size: 0.75rem; letter-spacing: 0.5px;
    }
    .sched-table td {
        padding: 8px 12px; color: #1a3a1a;
        border-bottom: 1px solid #e8e4dc;
    }
    .sched-table .row-a { background: #f5f2ea; }
    .sched-table .row-b { background: #ffffff; }
    .sched-table .result-t1 { color: #1a6b9a; font-weight: 700; }
    .sched-table .result-t2 { color: #9a1a1a; font-weight: 700; }
    .sched-table .result-h { color: #8a7a5a; font-weight: 600; }

    /* === Leaderboard table === */
    .lb-table {
        width: 100%; border-collapse: collapse;
        background: #ffffff; border-radius: 8px; overflow: hidden;
        box-shadow: 0 1px 4px rgba(0,0,0,0.08);
        font-family: 'DM Sans', sans-serif; font-size: 0.9rem;
    }
    .lb-table th {
        background: #2a5a2a; color: #f5f0e8;
        padding: 10px 12px; text-align: center;
        font-weight: 600; text-transform: uppercase; font-size: 0.75rem;
    }
    .lb-table th:first-child, .lb-table td:first-child { text-align: center; width: 40px; }
    .lb-table th:nth-child(2), .lb-table td:nth-child(2) { text-align: left; }
    .lb-table td {
        padding: 10px 12px; text-align: center;
        border-bottom: 1px solid #e8e4dc; color: #1a3a1a;
    }
    .lb-table .top-row td { background: #e8f5e9; font-weight: 600; }
    .lb-table .bottom-row td { background: #fff3e0; }

    /* === Leaderboard rows (card style) === */
    .lb-row { display: flex; align-items: center; padding: 12px 16px; border-bottom: 1px solid #e8e4dc; background: #fff; }
    .lb-row:nth-child(even) { background: #faf8f4; }
    .lb-row:hover { background: #f0ede5; }
    .lb-rank { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 900; color: #4a7a4a; width: 40px; }
    .lb-rank.top { color: #c17a3a; }
    .lb-name { flex: 1; font-weight: 500; color: #1a3a1a; }
    .lb-score { font-family: 'Playfair Display', serif; font-size: 1.4rem; font-weight: 700; color: #1a3a1a; }

    /* === Money display === */
    .money-big {
        font-family: 'Playfair Display', serif; font-size: 2.4rem; font-weight: 900;
        color: #2a5a2a; text-align: center; margin: 16px 0;
    }

    /* === Compact number inputs — hide spinner buttons === */
    div[data-testid="stNumberInput"] { min-width: 0 !important; max-width: 80px !important; }
    div[data-testid="stNumberInput"] input { padding: 4px 6px !important; font-size: 1rem !important; text-align: center !important; }
    div[data-testid="stNumberInput"] button { display: none !important; }

    /* === Metrics === */
    div[data-testid="stMetric"] { background: #ffffff; border: 1px solid #d4cfc5; border-radius: 12px; padding: 16px; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }
    div[data-testid="stMetricLabel"] { font-size: 0.7rem !important; text-transform: uppercase; letter-spacing: 1.5px; color: #6b8f6b !important; }
    div[data-testid="stMetricValue"] { font-family: 'Playfair Display', serif !important; color: #1a3a1a !important; }
    div[data-testid="stMetricLabel"] p { color: #6b8f6b !important; }
    div[data-testid="stMetricValue"] div { color: #1a3a1a !important; }

    /* === Expander === */
    details { background: #fff !important; border: 1px solid #d4cfc5 !important; border-radius: 8px !important; }
    details summary span { color: #1a3a1a !important; font-weight: 600 !important; }
    details summary svg { display: inline-block !important; }
    /* Hide material icon text fallback in expanders */
    .epifhcv2, span.st-emotion-cache-leahp2 { font-family: 'Material Symbols Rounded' !important; font-size: 20px !important; width: 20px !important; overflow: hidden !important; display: inline-block !important; }

    /* === Mobile Responsive === */
    @media (max-width: 768px) {
        .hero { padding: 28px 16px 24px !important; margin-bottom: 16px !important; border-radius: 10px !important; }
        .hero-title { font-size: 2.2rem !important; letter-spacing: 1px !important; }
        .hero-sub { font-size: 0.85rem !important; letter-spacing: 1px !important; }
        .section-header { font-size: 1.3rem !important; margin: 16px 0 10px !important; }
        .team-score-box { padding: 14px 10px !important; }
        .team-score-box h3 { font-size: 0.95rem !important; }
        .team-score-box .score { font-size: 2.2rem !important; }
        .card { padding: 14px !important; margin-bottom: 10px !important; }
        .lb-table th, .lb-table td { padding: 6px 4px !important; font-size: 0.75rem !important; }
        .sched-table th, .sched-table td { padding: 6px 6px !important; font-size: 0.75rem !important; }
        .sc-table th { padding: 4px 2px !important; font-size: 0.6rem !important; }
        .sc-table td { padding: 3px 2px !important; font-size: 0.7rem !important; }
        .sc-table .player-header { font-size: 0.7rem !important; }
        .money-big { font-size: 1.6rem !important; }
        div[data-testid="stNumberInput"] { max-width: 65px !important; }
        /* Stack columns on mobile */
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; gap: 8px !important; }
        [data-testid="stColumn"] { min-width: 100% !important; flex: 1 1 100% !important; }
        /* Tables scroll horizontally */
        .sc-table, .sched-table, .lb-table { display: block; overflow-x: auto; white-space: nowrap; -webkit-overflow-scrolling: touch; }
        /* Reduce main padding */
        .stMainBlockContainer { padding-left: 12px !important; padding-right: 12px !important; }
        section[data-testid="stMain"] > div { padding: 0 8px !important; }
    }
    @media (max-width: 480px) {
        .hero-title { font-size: 1.7rem !important; letter-spacing: 0.5px !important; }
        .hero-sub { font-size: 0.75rem !important; }
        .hero { padding: 20px 12px 18px !important; }
        .section-header { font-size: 1.1rem !important; }
        .team-score-box .score { font-size: 1.8rem !important; }
        .lb-table th, .lb-table td { padding: 5px 3px !important; font-size: 0.7rem !important; }
    }
</style>
""", unsafe_allow_html=True)

# ─── Tournament Data ──────────────────────────────────────────────────────────

TEAM_SHOOTER = ["Chris Cutshaw", "Ryan Phillips", "Pat Donoho", "Joe Donoho"]
TEAM_GILMORE = ["Mike Haynes", "Adam Hage", "James Hedges", "Adam Vandercar"]
ALL_PLAYERS = TEAM_SHOOTER + TEAM_GILMORE
OGS = ["Chris Cutshaw", "Joe Donoho", "Mike Haynes", "Adam Hage"]

COURSES = {
    "Sheep Ranch": {
        "par": [5,4,3,4,3,4,3,4,4, 4,5,4,5,4,4,3,4,5],
        "si":  [5,13,17,3,11,1,15,7,9, 6,4,2,10,8,14,16,12,18],
        "holes": 18,
        "slope": 130, "rating": 70.5,
    },
    "Pacific Dunes": {
        "par": [4,4,5,4,3,4,4,4,4, 3,3,5,4,3,5,4,3,5],
        "si":  [9,11,7,3,17,13,1,5,15, 14,18,6,2,16,10,12,8,4],
        "holes": 18,
        "slope": 131, "rating": 69.5,
    },
    "Old Macdonald": {
        "par": [4,3,4,4,3,5,4,3,4, 4,4,3,4,4,5,4,5,4],
        "si":  [11,15,9,1,17,3,5,13,7, 6,4,16,18,14,12,2,10,8],
        "holes": 18,
        "slope": 126, "rating": 69.3,
    },
    "Bandon Dunes": {
        "par": [4,3,5,4,4,3,4,4,5, 4,4,3,5,4,3,4,4,5],
        "si":  [13,15,3,5,1,17,7,11,9, 8,2,18,6,16,14,10,12,4],
        "holes": 18,
        "slope": 131, "rating": 70.2,
    },
    "Bandon Trails": {
        "par": [4,3,5,4,3,4,4,4,5, 4,4,3,4,4,4,5,3,4],
        "si":  [13,17,3,5,15,9,7,11,1, 10,4,18,12,14,8,2,16,6],
        "holes": 18,
        "slope": 131, "rating": 70.1,
    },
    "Shortys": {
        "par": [3,3,3,3,3,3,3,3,3, 3,3,3,3,3,3,3,3,3,3],
        "si":  [1,2,3,4,5,6,7,8,9, 10,11,12,13,14,15,16,17,18,19],
        "holes": 19,
        "no_handicap": True,
    },
    "Bandon Preserve": {
        "par": [3,3,3,3,3,3,3,3,3, 3,3,3,3],
        "si":  [9,11,2,4,1,12,5,8,7, 6,3,13,10],
        "holes": 13,
        "slope": 101, "rating": 34.5,
    },
}

SCHEDULE = [
    {"date": "June 17", "course": "Sheep Ranch",     "time": "8:40 AM",  "format": "2v2 Scramble Match Play",     "pts": 1, "stableford": False, "type": "scramble", "group": 1},
    {"date": "June 17", "course": "Sheep Ranch",     "time": "8:50 AM",  "format": "2v2 Scramble Match Play",     "pts": 1, "stableford": False, "type": "scramble", "group": 2},
    {"date": "June 17", "course": "Pacific Dunes",   "time": "2:40 PM",  "format": "2v2 Best Ball Stroke Play",   "pts": 1, "stableford": True,  "type": "bestball", "group": 1},
    {"date": "June 17", "course": "Pacific Dunes",   "time": "2:50 PM",  "format": "2v2 Best Ball Stroke Play",   "pts": 1, "stableford": True,  "type": "bestball", "group": 2},
    {"date": "June 18", "course": "Bandon Dunes",    "time": "9:30 AM",  "format": "2v2 Modified Alt Shot",       "pts": 1, "stableford": False, "type": "altshot",  "group": 1},
    {"date": "June 18", "course": "Bandon Dunes",    "time": "9:40 AM",  "format": "2v2 Modified Alt Shot",       "pts": 1, "stableford": False, "type": "altshot",  "group": 2},
    {"date": "June 18", "course": "Shortys",         "time": "3:45 PM",  "format": "2v2 Scramble Match Play",     "pts": 1, "stableford": False, "type": "scramble", "group": 1},
    {"date": "June 18", "course": "Shortys",         "time": "4:00 PM",  "format": "2v2 Scramble Match Play",     "pts": 1, "stableford": False, "type": "scramble", "group": 2},
    {"date": "June 19", "course": "Old Macdonald",   "time": "10:40 AM", "format": "2v2 Best Ball Stroke Play",   "pts": 1, "stableford": True,  "type": "bestball", "group": 1},
    {"date": "June 19", "course": "Old Macdonald",   "time": "10:50 AM", "format": "2v2 Best Ball Stroke Play",   "pts": 1, "stableford": True,  "type": "bestball", "group": 2},
    {"date": "June 19", "course": "Bandon Preserve",  "time": "5:00 PM",  "format": "2v2 Alt Shot Match Play",    "pts": 1, "stableford": False, "type": "altshot",  "group": 1},
    {"date": "June 19", "course": "Bandon Preserve",  "time": "5:15 PM",  "format": "2v2 Alt Shot Match Play",    "pts": 1, "stableford": False, "type": "altshot",  "group": 2},
    {"date": "June 20", "course": "Bandon Trails",   "time": "11:00 AM", "format": "Singles Match Play",          "pts": 1, "stableford": True,  "type": "singles",  "group": 1},
    {"date": "June 20", "course": "Bandon Trails",   "time": "11:00 AM", "format": "Singles Match Play",          "pts": 1, "stableford": True,  "type": "singles",  "group": 2},
    {"date": "June 20", "course": "Bandon Trails",   "time": "11:10 AM", "format": "Singles Match Play",          "pts": 1, "stableford": True,  "type": "singles",  "group": 3},
    {"date": "June 20", "course": "Bandon Trails",   "time": "11:10 AM", "format": "Singles Match Play",          "pts": 1, "stableford": True,  "type": "singles",  "group": 4},
]

TOTAL_TEAM_PTS = sum(s["pts"] for s in SCHEDULE)  # 16
WIN_THRESHOLD = 8.5
STABLEFORD_COURSES = ["Pacific Dunes", "Old Macdonald", "Bandon Trails"]

DEFAULT_PAIRINGS = {
    1: {"t1": [TEAM_SHOOTER[0], TEAM_SHOOTER[1]], "t2": [TEAM_GILMORE[0], TEAM_GILMORE[1]]},
    2: {"t1": [TEAM_SHOOTER[2], TEAM_SHOOTER[3]], "t2": [TEAM_GILMORE[2], TEAM_GILMORE[3]]},
    3: {"t1": [TEAM_SHOOTER[0]], "t2": [TEAM_GILMORE[0]]},
    4: {"t1": [TEAM_SHOOTER[1]], "t2": [TEAM_GILMORE[1]]},
}

DATA_FILE = "tournament_data.json"


def get_default_data():
    return {
        "handicaps": {p: {"index": 0.0, "main": 0.0, **{c: 0.0 for c in COURSES}} for p in ALL_PLAYERS},
        "scores": {},
        "team_scores": {},
        "team_results": [None] * len(SCHEDULE),
        "og_team_pts": {p: 0 for p in OGS},
        "pairings": {},
        "ledger": [],
    }


def load_data():
    if "data" not in st.session_state:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                st.session_state.data = json.load(f)
            default = get_default_data()
            for k in default:
                if k not in st.session_state.data:
                    st.session_state.data[k] = default[k]
            for p in ALL_PLAYERS:
                if p not in st.session_state.data["handicaps"]:
                    st.session_state.data["handicaps"][p] = {"index": 0.0, "main": 0.0, **{c: 0.0 for c in COURSES}}
                if "main" not in st.session_state.data["handicaps"][p]:
                    st.session_state.data["handicaps"][p]["main"] = 0.0
            # Pad team_results if schedule grew
            tr = st.session_state.data.get("team_results", [])
            while len(tr) < len(SCHEDULE):
                tr.append(None)
            st.session_state.data["team_results"] = tr
        else:
            st.session_state.data = get_default_data()
    return st.session_state.data


def save_data():
    with open(DATA_FILE, "w") as f:
        json.dump(st.session_state.data, f, indent=2)
    # Also commit to GitHub if token is available
    save_to_github()


def save_to_github():
    """Commit tournament_data.json to the GitHub repo."""
    try:
        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            try:
                token = st.secrets["GITHUB_TOKEN"]
            except (KeyError, FileNotFoundError):
                token = ""
        if not token:
            st.warning("No GITHUB_TOKEN configured — data saved locally only.")
            return
        repo = "CUTSCHR/badonscore"
        path = "tournament_data.json"
        url = f"https://api.github.com/repos/{repo}/contents/{path}"
        headers = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
        content = json.dumps(st.session_state.data, indent=2)
        encoded = base64.b64encode(content.encode()).decode()
        # Get current file SHA
        resp = requests.get(url, headers=headers, timeout=10)
        sha = resp.json().get("sha", "") if resp.status_code == 200 else ""
        payload = {"message": "Update scores", "content": encoded, "branch": "main"}
        if sha:
            payload["sha"] = sha
        put_resp = requests.put(url, headers=headers, json=payload, timeout=10)
        if put_resp.status_code not in (200, 201):
            st.error(f"GitHub save failed: {put_resp.status_code} — {put_resp.json().get('message', '')}")
    except Exception as e:
        st.error(f"GitHub save error: {e}")


def reset_data():
    """Reset tournament data to defaults."""
    st.session_state.data = get_default_data()
    save_data()
    st.rerun()


def calc_course_handicap(index, course_name):
    """Calculate Course Handicap from Handicap Index using slope/rating.
    Formula: Index × (Slope / 113) + (Course Rating − Par)
    """
    course = COURSES.get(course_name, {})
    slope = course.get("slope")
    rating = course.get("rating")
    if not slope or not rating:
        return index  # No slope data, use index directly
    par = sum(course["par"])
    return index * (slope / 113) + (rating - par)


def get_player_course_hdcp(data, player, course_name):
    """Return Course Handicap for this player/course.

    Priority: per-course manual override > auto-calculated from index + slope/rating.
    """
    h = data["handicaps"].get(player, {})
    course_val = h.get(course_name, 0)
    if course_val and float(course_val) != 0:
        return float(course_val)
    index = float(h.get("main", 0))
    return calc_course_handicap(index, course_name)


def round_half_up(value):
    """Round to nearest whole number with .5 rounding away from zero."""
    if value >= 0:
        return math.floor(value + 0.5)
    return math.ceil(value - 0.5)


# ─── Calc Helpers ─────────────────────────────────────────────────────────────

def get_strokes_on_hole(handicap, stroke_index, num_holes=18):
    hdcp = round_half_up(handicap)
    if hdcp <= 0:
        return 0
    strokes = 0
    if hdcp >= stroke_index:
        strokes += 1
    if hdcp >= stroke_index + num_holes:
        strokes += 1
    return strokes


def calc_net(gross, handicap, course_name, hole_idx):
    if not gross or gross == 0:
        return None
    data = COURSES[course_name]
    strokes = get_strokes_on_hole(handicap, data["si"][hole_idx], data["holes"])
    return gross - strokes


def calc_stableford(net_score, par):
    if net_score is None:
        return 0
    diff = net_score - par
    if diff <= -3: return 5
    elif diff == -2: return 4
    elif diff == -1: return 3
    elif diff == 0: return 2
    elif diff == 1: return 1
    return 0


def calc_scramble_hdcp(hdcp_a, hdcp_b):
    return round_half_up(0.35 * min(hdcp_a, hdcp_b) + 0.15 * max(hdcp_a, hdcp_b))


def calc_altshot_hdcp(hdcp_a, hdcp_b, modified=False):
    if modified:
        return round_half_up(0.6 * min(hdcp_a, hdcp_b) + 0.4 * max(hdcp_a, hdcp_b))
    return round_half_up((hdcp_a + hdcp_b) * 0.5)


def get_player_stableford(data, player, course):
    key = f"{course}|{player}"
    scores = data["scores"].get(key, [])
    hdcp = get_player_course_hdcp(data, player, course)
    total = 0
    for i, s in enumerate(scores):
        if s and s > 0:
            net = calc_net(s, hdcp, course, i)
            total += calc_stableford(net, COURSES[course]["par"][i])
    return total


def get_player_gross_stableford(data, player, course):
    key = f"{course}|{player}"
    scores = data["scores"].get(key, [])
    total = 0
    for i, s in enumerate(scores):
        if s and s > 0:
            diff = s - COURSES[course]["par"][i]
            if diff <= -3: total += 5
            elif diff == -2: total += 4
            elif diff == -1: total += 3
            elif diff == 0: total += 2
            elif diff == 1: total += 1
    return total


def calc_team_totals(data):
    t1_pts, t2_pts = 0.0, 0.0
    for i, result in enumerate(data["team_results"]):
        if i >= len(SCHEDULE):
            break
        pts = SCHEDULE[i]["pts"]
        if result == "T1": t1_pts += pts
        elif result == "T2": t2_pts += pts
        elif result == "H": t1_pts += pts/2; t2_pts += pts/2
    return t1_pts, t2_pts


def calc_og_rank_pts(og_scores):
    """Calculate OG rank points, splitting evenly when tied. Skip courses where nobody has scores."""
    rank_pts = {p: 0.0 for p in OGS}
    pts_pool = [4, 3, 2, 1]
    for course in STABLEFORD_COURSES:
        # Skip course if all players have 0 (not yet played)
        course_scores = [og_scores[p][course] for p in OGS]
        if all(s == 0 for s in course_scores):
            continue
        scores_list = [(p, og_scores[p][course]) for p in OGS]
        scores_list.sort(key=lambda x: x[1], reverse=True)
        i = 0
        while i < len(scores_list):
            # Find all tied at this score
            tied = [scores_list[i]]
            j = i + 1
            while j < len(scores_list) and scores_list[j][1] == scores_list[i][1]:
                tied.append(scores_list[j])
                j += 1
            # Split the points for tied positions
            shared_pts = sum(pts_pool[k] for k in range(i, min(j, len(pts_pool)))) / len(tied)
            for player, _ in tied:
                rank_pts[player] += shared_pts
            i = j
    return rank_pts


def calc_og_team_bonus(data):
    """Auto-calculate OG player team-point bonus from team_results."""
    # Count how many team matches each OG player participated in and won
    og_pts = {p: 0 for p in OGS}
    for i, result in enumerate(data["team_results"]):
        if result is None or i >= len(SCHEDULE):
            continue
        match = SCHEDULE[i]
        group = match["group"]
        custom_key = str(i)
        if "pairings" in data and custom_key in data["pairings"]:
            pairing = data["pairings"][custom_key]
        elif group in DEFAULT_PAIRINGS:
            pairing = DEFAULT_PAIRINGS[group]
        else:
            continue
        # Identify which OGs played in this match
        t1_players = pairing.get("t1", [])
        t2_players = pairing.get("t2", [])
        for player in OGS:
            if player in t1_players and result == "T1":
                og_pts[player] += 1
            elif player in t2_players and result == "T2":
                og_pts[player] += 1
    return og_pts


# ─── Scorecard HTML builder ──────────────────────────────────────────────────

def build_scorecard_html(course_name, players_data, show_stableford=True, match_play_data=None):
    """match_play_data: optional dict with 'hole_winners' list (1=T1 won, -1=T2 won, 0=tie/no data) and 'running_total' list of strings."""
    course = COURSES[course_name]
    pars = course["par"]
    si = course["si"]
    num_holes = course["holes"]

    if num_holes >= 18:
        sections = [(0, 9, "OUT"), (9, num_holes, "IN")]
    else:
        sections = [(0, num_holes, "TOT")]

    html_parts = []

    for sec_start, sec_end, sec_label in sections:
        num_cols = sec_end - sec_start
        # Total columns = 1 (label) + num_cols (holes) + 1 (turn) + (1 if 18-hole TOT)
        tot_cols = num_cols + 2 + (1 if num_holes >= 18 else 0)
        html = f'<table class="sc-table"><colgroup><col style="width:90px;">{"<col>" * (tot_cols - 1)}</colgroup>'
        html += '<thead><tr><th style="text-align:left;">HOLE</th>'
        for h in range(sec_start, sec_end):
            html += f'<th>{h+1}</th>'
        html += f'<th class="turn-col">{sec_label}</th>'
        if num_holes >= 18:
            html += '<th class="total-col">TOT</th>'
        html += '</tr></thead><tbody>'

        # Par row
        html += '<tr class="par-row"><td style="text-align:left;">PAR</td>'
        sec_par = sum(pars[sec_start:sec_end])
        for h in range(sec_start, sec_end):
            html += f'<td>{pars[h]}</td>'
        html += f'<td class="turn-col">{sec_par}</td>'
        if num_holes >= 18:
            if sec_label == "IN":
                html += f'<td class="total-col">{sum(pars)}</td>'
            else:
                html += '<td class="total-col"></td>'
        html += '</tr>'

        # S.I. row
        if not course.get("no_handicap"):
            html += '<tr class="par-row"><td style="text-align:left;font-size:0.65rem;">S.I.</td>'
            for h in range(sec_start, sec_end):
                html += f'<td style="font-size:0.65rem;">{si[h]}</td>'
            html += '<td class="turn-col"></td>'
            if num_holes >= 18:
                html += '<td class="total-col"></td>'
            html += '</tr>'

        # Each player
        for pd in players_data:
            hdcp = pd["handicap"]
            scores = pd["scores"]
            team_class = "team-shooter" if pd["team"] == 1 else "team-gilmore"

            # Dots row
            if not course.get("no_handicap"):
                html += f'<tr class="dot-row"><td class="player-header {team_class}">{pd["name"]}</td>'
                for h in range(sec_start, sec_end):
                    dots = get_strokes_on_hole(hdcp, si[h], num_holes)
                    html += f'<td>{"●" * dots}</td>'
                html += f'<td class="turn-col" style="font-size:0.7rem;color:#c17a3a;">{hdcp:.0f}</td>'
                if num_holes >= 18:
                    html += '<td class="total-col"></td>'
                html += '</tr>'
            else:
                html += f'<tr><td class="player-header {team_class}" colspan="{sec_end - sec_start + 2}">{pd["name"]}</td></tr>'

            # Gross row
            html += '<tr><td style="text-align:left;color:#6b8f6b;font-size:0.7rem;">GROSS</td>'
            sec_gross = 0
            total_gross = sum(s for s in scores if s and s > 0)
            for h in range(sec_start, sec_end):
                s = scores[h] if h < len(scores) else 0
                if s and s > 0:
                    diff = s - pars[h]
                    cls = ""
                    if diff <= -2: cls = ' style="color:#c17a3a;font-weight:700;"'
                    elif diff == -1: cls = ' style="color:#2a8a2a;font-weight:700;"'
                    elif diff >= 2: cls = ' style="color:#9a4a4a;"'
                    html += f'<td{cls}>{s}</td>'
                    sec_gross += s
                else:
                    html += '<td style="color:#ccc;">-</td>'
            html += f'<td class="turn-col">{sec_gross if sec_gross else "-"}</td>'
            if num_holes >= 18:
                if sec_label == "IN":
                    html += f'<td class="total-col">{total_gross if total_gross else "-"}</td>'
                else:
                    html += '<td class="total-col"></td>'
            html += '</tr>'

            # Net row
            if not course.get("no_handicap"):
                html += '<tr class="net-row"><td style="text-align:left;font-size:0.7rem;">NET</td>'
                sec_net = 0
                for h in range(sec_start, sec_end):
                    s = scores[h] if h < len(scores) else 0
                    if s and s > 0:
                        n = calc_net(s, hdcp, course_name, h)
                        # Highlight if this player/team won the hole in match play
                        cell_style = ""
                        if match_play_data and h < len(match_play_data.get("hole_winners", [])):
                            hw = match_play_data["hole_winners"][h]
                            if (pd["team"] == 1 and hw == 1) or (pd["team"] == 2 and hw == -1):
                                cell_style = ' style="background:#c8e6c9;font-weight:700;color:#1a5a1a;border:2px solid #2a8a2a;border-radius:4px;"'
                        html += f'<td{cell_style}>{n}</td>'
                        if n: sec_net += n
                    else:
                        html += '<td style="color:#ccc;">-</td>'
                html += f'<td class="turn-col">{sec_net if sec_net else "-"}</td>'
                if num_holes >= 18:
                    if sec_label == "IN":
                        front_net = sum(
                            calc_net(scores[h], hdcp, course_name, h)
                            for h in range(0, 9)
                            if h < len(scores) and scores[h] and scores[h] > 0 and calc_net(scores[h], hdcp, course_name, h)
                        )
                        html += f'<td class="total-col">{front_net + sec_net if (front_net + sec_net) else "-"}</td>'
                    else:
                        html += '<td class="total-col"></td>'
                html += '</tr>'

            # Stableford row (only if show_stableford and has handicap)
            if show_stableford and not course.get("no_handicap"):
                html += '<tr class="stab-row"><td style="text-align:left;font-size:0.7rem;">PTS</td>'
                sec_stab = 0
                for h in range(sec_start, sec_end):
                    s = scores[h] if h < len(scores) else 0
                    if s and s > 0:
                        n = calc_net(s, hdcp, course_name, h)
                        pts = calc_stableford(n, pars[h])
                        html += f'<td>{pts}</td>'
                        sec_stab += pts
                    else:
                        html += '<td style="color:#ccc;">-</td>'
                html += f'<td class="turn-col">{sec_stab if sec_stab else "-"}</td>'
                if num_holes >= 18:
                    if sec_label == "IN":
                        front_stab = sum(
                            calc_stableford(calc_net(scores[h], hdcp, course_name, h), pars[h])
                            for h in range(0, 9)
                            if h < len(scores) and scores[h] and scores[h] > 0
                        )
                        html += f'<td class="total-col">{front_stab + sec_stab if (front_stab + sec_stab) else "-"}</td>'
                    else:
                        html += '<td class="total-col"></td>'
                html += '</tr>'

        # Match play running total row (if match_play_data provided)
        if match_play_data:
            hole_winners = match_play_data.get("hole_winners", [])
            running = match_play_data.get("running_total", [])
            # Highlight hole winners row
            html += '<tr><td style="text-align:left;font-weight:700;font-size:0.7rem;color:#2a5a2a;">MATCH</td>'
            for h in range(sec_start, sec_end):
                if h < len(hole_winners):
                    w = hole_winners[h]
                    r = running[h] if h < len(running) else ""
                    if w == 1:
                        html += f'<td style="background:#c8e6c9;font-weight:700;color:#1a6b9a;border:2px solid #2a8a2a;border-radius:4px;font-size:0.7rem;">{r}</td>'
                    elif w == -1:
                        html += f'<td style="background:#ffcdd2;font-weight:700;color:#9a1a1a;border:2px solid #c62828;border-radius:4px;font-size:0.7rem;">{r}</td>'
                    else:
                        html += f'<td style="color:#6b8f6b;font-size:0.7rem;">{r}</td>'
                else:
                    html += '<td>-</td>'
            html += '<td class="turn-col"></td>'
            if num_holes >= 18:
                if sec_label == "IN":
                    # Show final match status
                    final_status = running[-1] if running else ""
                    html += f'<td class="total-col" style="font-size:0.7rem;font-weight:700;">{final_status}</td>'
                else:
                    html += '<td class="total-col"></td>'
            html += '</tr>'

        html += '</tbody></table>'
        html_parts.append(html)

    return html_parts


# ─── PAGES ────────────────────────────────────────────────────────────────────

def page_leaderboard(data):
    # Logo
    logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.png")
    if os.path.exists(logo_path):
        import base64
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f'<div style="text-align:center;margin-bottom:8px;"><img src="data:image/png;base64,{logo_b64}" style="width:240px;max-width:60vw;"></div>', unsafe_allow_html=True)

    # Hero
    st.markdown("""
    <div class="hero">
        <p class="hero-title">THE BATTLE AT BANDON</p>
        <p class="hero-sub">The 6th Annual Chubbs Peterson Invitational &middot; June 17&ndash;20, 2026</p>
    </div>
    """, unsafe_allow_html=True)

    # Team Championship summary
    st.markdown('<div class="section-header">Team Championship &middot; First to 8.5</div>', unsafe_allow_html=True)
    t1_pts, t2_pts = calc_team_totals(data)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown(f'''
        <div class="team-score-box">
            <h3 class="team-shooter">TEAM SHOOTER</h3>
            <div class="score" style="color:#1a6b9a;">{t1_pts:g}</div>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align:center;padding-top:30px;color:#4a7a4a;font-size:2rem;font-family:Playfair Display,serif;'>vs</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="team-score-box">
            <h3 class="team-gilmore">TEAM GILMORE</h3>
            <div class="score" style="color:#9a1a1a;">{t2_pts:g}</div>
        </div>''', unsafe_allow_html=True)

    played = sum(1 for r in data["team_results"] if r is not None)
    remaining = TOTAL_TEAM_PTS - t1_pts - t2_pts
    st.progress(played / len(SCHEDULE), text=f"{played}/{len(SCHEDULE)} matches · {remaining:g} pts remaining")

    # Individual Championship
    st.markdown('<div class="section-header">Individual NET Stableford</div>', unsafe_allow_html=True)
    stab_totals = [(p, sum(get_player_stableford(data, p, c) for c in STABLEFORD_COURSES)) for p in ALL_PLAYERS]
    stab_totals.sort(key=lambda x: x[1], reverse=True)

    lb_html = '<table class="lb-table"><thead><tr><th>Pos</th><th>Player</th>'
    for c in STABLEFORD_COURSES:
        lb_html += f'<th>{c}</th>'
    lb_html += '<th>Total</th></tr></thead><tbody>'
    for rank, (player, total) in enumerate(stab_totals, 1):
        team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
        row_class = "top-row" if rank <= 3 else ("bottom-row" if rank > 3 else "")
        course_cells = "".join(f'<td>{get_player_stableford(data, player, c)}</td>' for c in STABLEFORD_COURSES)
        lb_html += f'<tr class="{row_class}"><td>{rank}</td><td class="{team_class}">{player}</td>{course_cells}<td style="font-weight:700;">{total}</td></tr>'
    lb_html += '</tbody></table>'
    st.markdown(lb_html, unsafe_allow_html=True)

    # Schedule
    st.markdown("---")
    st.markdown("### Schedule")
    sched_html = '<table class="sched-table"><thead><tr><th>Date</th><th>Time</th><th>Course</th><th>Format</th><th>Pts</th><th>Result</th></tr></thead><tbody>'
    # Alternate color by course
    course_color_map = {}
    color_idx = 0
    for s in SCHEDULE:
        if s["course"] not in course_color_map:
            course_color_map[s["course"]] = color_idx % 2
            color_idx += 1

    for i, s in enumerate(SCHEDULE):
        row_class = "row-a" if course_color_map[s["course"]] == 0 else "row-b"
        r = data["team_results"][i]
        if r == "T1":
            result_html = '<span class="result-t1">Team Shooter</span>'
        elif r == "T2":
            result_html = '<span class="result-t2">Team Gilmore</span>'
        elif r == "H":
            result_html = '<span class="result-h">Halved</span>'
        else:
            result_html = '<span style="color:#bbb;">&mdash;</span>'
        sched_html += f'<tr class="{row_class}"><td>{s["date"]}</td><td>{s["time"]}</td><td>{s["course"]}</td><td>{s["format"]}</td><td style="text-align:center;">{s["pts"]}</td><td>{result_html}</td></tr>'
    sched_html += '</tbody></table>'
    st.markdown(sched_html, unsafe_allow_html=True)

    # OG Belt summary
    st.markdown('<div class="section-header">OG Belt Standings</div>', unsafe_allow_html=True)
    og_scores = {}
    for player in OGS:
        og_scores[player] = {}
        for course in STABLEFORD_COURSES:
            og_scores[player][course] = get_player_gross_stableford(data, player, course)
    rank_pts = calc_og_rank_pts(og_scores)
    og_team_pts = calc_og_team_bonus(data)
    og_final = []
    for player in OGS:
        bonus = og_team_pts[player] * 0.5
        og_final.append({"Player": player, "Total": rank_pts[player] + bonus})
    og_final.sort(key=lambda x: x["Total"], reverse=True)
    og_sum_html = '<table class="lb-table"><thead><tr><th>Pos</th><th>Player</th><th>Total</th></tr></thead><tbody>'
    for rank, r in enumerate(og_final, 1):
        team_class = "team-shooter" if r["Player"] in TEAM_SHOOTER else "team-gilmore"
        og_sum_html += f'<tr><td>{rank}</td><td class="{team_class}">{r["Player"]}</td><td style="font-weight:700;">{r["Total"]:.1f}</td></tr>'
    og_sum_html += '</tbody></table>'
    st.markdown(og_sum_html, unsafe_allow_html=True)

    # Skins summary
    st.markdown('<div class="section-header">Skins Summary</div>', unsafe_allow_html=True)
    total_skins_all = {p: 0 for p in ALL_PLAYERS}
    for course_name in STABLEFORD_COURSES:
        course = COURSES[course_name]
        pars = course["par"]
        num_holes = course["holes"]
        net_scores = {}
        for player in ALL_PLAYERS:
            key = f"{course_name}|{player}"
            scores = data["scores"].get(key, [0] * num_holes)
            hdcp = get_player_course_hdcp(data, player, course_name)
            net_scores[player] = [
                calc_net(scores[i], hdcp, course_name, i)
                if i < len(scores) and scores[i] and scores[i] > 0 else None
                for i in range(num_holes)
            ]
        for h in range(num_holes):
            hole_nets = {p: net_scores[p][h] for p in ALL_PLAYERS if net_scores[p][h] is not None}
            if hole_nets:
                min_net = min(hole_nets.values())
                leaders = [p for p, n in hole_nets.items() if n == min_net]
                if len(leaders) == 1:
                    next_h = (h + 1) % num_holes
                    nxt = net_scores[leaders[0]][next_h]
                    if nxt is not None and nxt <= pars[next_h]:
                        total_skins_all[leaders[0]] += 1
    pot_per_round = 100 * len(ALL_PLAYERS)
    total_all_skins = sum(total_skins_all.values())
    per_skin_all = pot_per_round / total_all_skins if total_all_skins > 0 else 0
    skins_winners = [(p, total_skins_all[p]) for p in ALL_PLAYERS if total_skins_all[p] > 0]
    skins_winners.sort(key=lambda x: x[1], reverse=True)
    if skins_winners:
        sk_html = '<table class="lb-table"><thead><tr><th>Player</th><th>Skins</th><th>Winnings</th></tr></thead><tbody>'
        for player, count in skins_winners:
            team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
            sk_html += f'<tr><td class="{team_class}">{player}</td><td>{count}</td><td style="font-weight:700;color:#2a5a2a;font-size:1.1rem;">${count * per_skin_all:,.0f}</td></tr>'
        sk_html += '</tbody></table>'
        st.markdown(sk_html, unsafe_allow_html=True)
    else:
        st.info("No skins won yet.")


def page_handicaps(data):
    st.markdown("### Handicaps")
    st.caption("Enter each player's Handicap Index. Course Handicaps are auto-calculated using slope/rating. Expand for manual per-course overrides.")

    for player in ALL_PLAYERS:
        team_label = "Team Shooter" if player in TEAM_SHOOTER else "Team Gilmore"
        team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"

        col1, col2 = st.columns([3, 1])
        with col1:
            main_hdcp = float(data["handicaps"][player].get("main", 0))
            st.markdown(f'<span class="{team_class}" style="font-size:1.1rem;">{player}</span> <span style="color:#8a8a7a;font-size:0.8rem;">({team_label})</span>', unsafe_allow_html=True)
        with col2:
            new_main = st.number_input(
                "Index", min_value=-5.0, max_value=54.0, step=0.1, value=main_hdcp,
                format="%.1f", key=f"main_hc_{player}", label_visibility="collapsed"
            )
            data["handicaps"][player]["main"] = new_main

        # Show auto-calculated course handicaps
        if new_main != 0:
            course_hdcps = []
            for course in COURSES:
                if COURSES[course].get("no_handicap"):
                    continue
                ch = calc_course_handicap(new_main, course)
                course_hdcps.append(f"{course[:8]}: {round_half_up(ch)}")
            st.caption(" · ".join(course_hdcps))

        with st.expander("Per-course overrides", expanded=False):
            cols = st.columns(len(COURSES))
            for i, course in enumerate(COURSES):
                current = float(data["handicaps"][player].get(course, 0))
                data["handicaps"][player][course] = cols[i].number_input(
                    course[:8], min_value=-5.0, max_value=54.0, step=0.1, value=current,
                    format="%.1f", key=f"hc_{player}_{course}"
                )
            st.caption("Leave at 0 to auto-calculate from index + slope/rating.")
        st.markdown("")


def page_scorecards(data):
    st.markdown("### Scorecards")

    match_options = [f"{s['date']} · {s['course']} · {s['format']} (G{s['group']})" for s in SCHEDULE]
    match_idx = st.selectbox("Select Match", range(len(SCHEDULE)), format_func=lambda i: match_options[i])

    match = SCHEDULE[match_idx]
    course_name = match["course"]
    course = COURSES[course_name]
    num_holes = course["holes"]
    match_type = match["type"]
    group = match["group"]
    # Use custom pairings if set, otherwise defaults
    custom_key = str(match_idx)
    if "pairings" in data and custom_key in data["pairings"]:
        pairing = data["pairings"][custom_key]
    elif group in DEFAULT_PAIRINGS:
        pairing = DEFAULT_PAIRINGS[group]
    else:
        pairing = {"t1": [TEAM_SHOOTER[0]], "t2": [TEAM_GILMORE[0]]}
    t1_players = pairing["t1"]
    t2_players = pairing["t2"]

    st.markdown(f"""
    <div style="margin:12px 0;">
        <span style="background:#2a5a2a;color:#f5f0e8;padding:4px 12px;border-radius:6px;font-size:0.8rem;font-weight:600;text-transform:uppercase;letter-spacing:0.5px;">{course_name} &middot; Par {sum(course['par'])}</span>
        <span style="color:#6b8f6b;font-size:0.85rem;margin-left:8px;">{match["format"]} &middot; {match["time"]}</span>
    </div>
    <div class="team-shooter-bg"><strong>Team Shooter:</strong> {' & '.join(t1_players)}</div>
    <div class="team-gilmore-bg"><strong>Team Gilmore:</strong> {' & '.join(t2_players)}</div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    if match_type in ("bestball", "singles"):
        if match_type == "singles":
            players_to_show = [t1_players[0], t2_players[0]]
        else:
            players_to_show = t1_players + t2_players

        for player in players_to_show:
            hdcp = get_player_course_hdcp(data, player, course_name)
            key = f"{course_name}|{player}"
            if key not in data["scores"]:
                data["scores"][key] = [0] * num_holes
            scores = data["scores"][key]
            if len(scores) < num_holes:
                scores.extend([0] * (num_holes - len(scores)))

            team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
            st.markdown(f'<span class="{team_class}" style="font-size:0.85rem;">{player} ({hdcp:.0f})</span>', unsafe_allow_html=True)

            # 18 holes on one line with OUT/IN/TOT
            if num_holes >= 18:
                back_count = num_holes - 9
                cols = st.columns([1]*9 + [1.3] + [1]*back_count + [1.3, 1.3])
                for h in range(9):
                    scores[h] = cols[h].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"s_{match_idx}_{player}_{h}", label_visibility="visible")
                out_val = sum(s for s in scores[:9] if s > 0)
                cols[9].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.85rem;color:#4a7a4a;'>{out_val if out_val else ''}</div>", unsafe_allow_html=True)
                for h in range(9, num_holes):
                    scores[h] = cols[10 + h - 9].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"s_{match_idx}_{player}_{h}", label_visibility="visible")
                in_val = sum(s for s in scores[9:num_holes] if s > 0)
                tot_val = out_val + in_val
                cols[-2].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.85rem;color:#4a7a4a;'>{in_val if in_val else ''}</div>", unsafe_allow_html=True)
                cols[-1].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.9rem;color:#1a3a1a;'>{tot_val if tot_val else ''}</div>", unsafe_allow_html=True)
            else:
                cols = st.columns([1]*num_holes + [1.3])
                for h in range(num_holes):
                    scores[h] = cols[h].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"s_{match_idx}_{player}_{h}", label_visibility="visible")
                tot_val = sum(s for s in scores if s > 0)
                cols[-1].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.9rem;color:#1a3a1a;'>{tot_val if tot_val else ''}</div>", unsafe_allow_html=True)

            data["scores"][key] = scores

        # Render scorecard
        players_data = [
            {"name": p, "team": 1 if p in TEAM_SHOOTER else 2,
             "handicap": get_player_course_hdcp(data, p, course_name),
             "scores": data["scores"].get(f"{course_name}|{p}", [0]*num_holes)}
            for p in players_to_show
        ]

        # For singles match play, compute hole-by-hole match data
        mp_data = None
        if match_type == "singles":
            p1, p2 = t1_players[0], t2_players[0]
            s1 = data["scores"].get(f"{course_name}|{p1}", [0]*num_holes)
            s2 = data["scores"].get(f"{course_name}|{p2}", [0]*num_holes)
            h1 = get_player_course_hdcp(data, p1, course_name)
            h2 = get_player_course_hdcp(data, p2, course_name)
            hole_winners = []
            running_total = []
            cum = 0
            for h in range(num_holes):
                sv1 = s1[h] if h < len(s1) else 0
                sv2 = s2[h] if h < len(s2) else 0
                if sv1 > 0 and sv2 > 0:
                    n1 = calc_net(sv1, h1, course_name, h)
                    n2 = calc_net(sv2, h2, course_name, h)
                    if n1 and n2:
                        if n1 < n2: cum += 1; hole_winners.append(1)
                        elif n2 < n1: cum -= 1; hole_winners.append(-1)
                        else: hole_winners.append(0)
                    else:
                        hole_winners.append(0)
                else:
                    hole_winners.append(0)
                if cum > 0: running_total.append(f"S+{cum}")
                elif cum < 0: running_total.append(f"G+{-cum}")
                else: running_total.append("AS")
            mp_data = {"hole_winners": hole_winners, "running_total": running_total}

        st.markdown("---")
        for html in build_scorecard_html(course_name, players_data, show_stableford=match["stableford"], match_play_data=mp_data):
            st.markdown(html, unsafe_allow_html=True)

        # Best Ball summary for bestball matches
        if match_type == "bestball":
            st.markdown("**Best Ball NET**")
            course_obj = COURSES[course_name]
            pars_bb = course_obj["par"]
            if num_holes >= 18:
                bb_sections = [(0, 9, "OUT"), (9, num_holes, "IN")]
            else:
                bb_sections = [(0, num_holes, "TOT")]
            for sec_start, sec_end, sec_label in bb_sections:
                bb_num_cols = sec_end - sec_start
                bb_tot_cols = bb_num_cols + 2 + (1 if num_holes >= 18 else 0)
                bb_html = f'<table class="sc-table"><colgroup><col style="width:90px;">{"<col>" * (bb_tot_cols - 1)}</colgroup>'
                bb_html += '<thead><tr><th style="text-align:left;">TEAM</th>'
                for h in range(sec_start, sec_end):
                    bb_html += f'<th>{h+1}</th>'
                bb_html += f'<th class="turn-col">{sec_label}</th>'
                if num_holes >= 18:
                    bb_html += '<th class="total-col">TOT</th>'
                bb_html += '</tr></thead><tbody>'
                # Par row
                bb_html += '<tr class="par-row"><td style="text-align:left;">PAR</td>'
                for h in range(sec_start, sec_end):
                    bb_html += f'<td>{pars_bb[h]}</td>'
                bb_html += f'<td class="turn-col">{sum(pars_bb[sec_start:sec_end])}</td>'
                if num_holes >= 18:
                    if sec_label == "IN":
                        bb_html += f'<td class="total-col">{sum(pars_bb)}</td>'
                    else:
                        bb_html += '<td class="total-col"></td>'
                bb_html += '</tr>'
                for team_name, team_players, team_class in [("Shooter", t1_players, "team-shooter"), ("Gilmore", t2_players, "team-gilmore")]:
                    bb_html += f'<tr><td class="player-header {team_class}">{team_name}</td>'
                    sec_bb = 0
                    total_bb = 0
                    for h in range(sec_start, sec_end):
                        best = None
                        for p in team_players:
                            s_key = f"{course_name}|{p}"
                            scores_p = data["scores"].get(s_key, [0]*num_holes)
                            sv = scores_p[h] if h < len(scores_p) else 0
                            if sv and sv > 0:
                                n = calc_net(sv, get_player_course_hdcp(data, p, course_name), course_name, h)
                                if n is not None and (best is None or n < best):
                                    best = n
                        if best is not None:
                            bb_html += f'<td style="font-weight:600;">{best}</td>'
                            sec_bb += best
                        else:
                            bb_html += '<td>-</td>'
                    # Compute full-round total for IN column
                    if sec_label == "IN":
                        for h in range(num_holes):
                            best = None
                            for p in team_players:
                                s_key = f"{course_name}|{p}"
                                scores_p = data["scores"].get(s_key, [0]*num_holes)
                                sv = scores_p[h] if h < len(scores_p) else 0
                                if sv and sv > 0:
                                    n = calc_net(sv, get_player_course_hdcp(data, p, course_name), course_name, h)
                                    if n is not None and (best is None or n < best):
                                        best = n
                            if best is not None:
                                total_bb += best
                    bb_html += f'<td class="turn-col" style="font-weight:700;">{sec_bb if sec_bb else "-"}</td>'
                    if num_holes >= 18:
                        if sec_label == "IN":
                            bb_html += f'<td class="total-col" style="font-weight:700;">{total_bb if total_bb else "-"}</td>'
                        else:
                            bb_html += '<td class="total-col"></td>'
                    bb_html += '</tr>'
                bb_html += '</tbody></table>'
                st.markdown(bb_html, unsafe_allow_html=True)

        auto_calc_individual_match(data, match_idx, match_type, course_name, num_holes, t1_players, t2_players)

    else:
        # Team formats (scramble / alt shot)
        t1_hdcps = [get_player_course_hdcp(data, p, course_name) for p in t1_players]
        t2_hdcps = [get_player_course_hdcp(data, p, course_name) for p in t2_players]

        if match_type == "scramble":
            t1_team_hdcp = calc_scramble_hdcp(*t1_hdcps)
            t2_team_hdcp = calc_scramble_hdcp(*t2_hdcps)
        else:
            modified = "Modified" in match["format"]
            t1_team_hdcp = calc_altshot_hdcp(*t1_hdcps, modified=modified)
            t2_team_hdcp = calc_altshot_hdcp(*t2_hdcps, modified=modified)

        strokes_diff = abs(t1_team_hdcp - t2_team_hdcp)
        receiving = "Team Shooter" if t1_team_hdcp > t2_team_hdcp else ("Team Gilmore" if t2_team_hdcp > t1_team_hdcp else "Even")
        st.caption(f"Shooter hdcp: {t1_team_hdcp} · Gilmore hdcp: {t2_team_hdcp} · {receiving} receives {strokes_diff}")

        for team_label, team_suffix, team_class in [("Team Shooter", "t1", "team-shooter"), ("Team Gilmore", "t2", "team-gilmore")]:
            st.markdown(f'<span class="{team_class}" style="font-size:0.85rem;">{team_label}</span>', unsafe_allow_html=True)
            key = f"{match_idx}|{team_suffix}"
            if key not in data["team_scores"]:
                data["team_scores"][key] = [0] * num_holes
            scores = data["team_scores"][key]
            if len(scores) < num_holes:
                scores.extend([0] * (num_holes - len(scores)))

            if num_holes >= 18:
                back_count = num_holes - 9
                cols = st.columns([1]*9 + [1.3] + [1]*back_count + [1.3, 1.3])
                for h in range(9):
                    scores[h] = cols[h].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"ts_{match_idx}_{team_suffix}_{h}", label_visibility="visible")
                out_val = sum(s for s in scores[:9] if s > 0)
                cols[9].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.85rem;color:#4a7a4a;'>{out_val if out_val else ''}</div>", unsafe_allow_html=True)
                for h in range(9, num_holes):
                    scores[h] = cols[10 + h - 9].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"ts_{match_idx}_{team_suffix}_{h}", label_visibility="visible")
                in_val = sum(s for s in scores[9:num_holes] if s > 0)
                tot_val = out_val + in_val
                cols[-2].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.85rem;color:#4a7a4a;'>{in_val if in_val else ''}</div>", unsafe_allow_html=True)
                cols[-1].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.9rem;color:#1a3a1a;'>{tot_val if tot_val else ''}</div>", unsafe_allow_html=True)
            else:
                cols = st.columns([1]*num_holes + [1.3])
                for h in range(num_holes):
                    scores[h] = cols[h].number_input(f"{h+1}", min_value=0, max_value=15, value=scores[h], key=f"ts_{match_idx}_{team_suffix}_{h}", label_visibility="visible")
                tot_val = sum(s for s in scores if s > 0)
                cols[-1].markdown(f"<div style='text-align:center;padding-top:26px;font-weight:700;font-size:0.9rem;color:#1a3a1a;'>{tot_val if tot_val else ''}</div>", unsafe_allow_html=True)
            data["team_scores"][key] = scores

        # Effective handicaps for scorecard
        t1_eff = strokes_diff if t1_team_hdcp > t2_team_hdcp else 0
        t2_eff = strokes_diff if t2_team_hdcp > t1_team_hdcp else 0

        # Compute match play hole-by-hole data
        t1s = data["team_scores"].get(f"{match_idx}|t1", [0]*num_holes)
        t2s = data["team_scores"].get(f"{match_idx}|t2", [0]*num_holes)
        hole_winners = []
        running_total = []
        cum = 0
        for h in range(num_holes):
            if t1s[h] > 0 and t2s[h] > 0:
                t1n = t1s[h] - get_strokes_on_hole(t1_eff, course["si"][h], num_holes)
                t2n = t2s[h] - get_strokes_on_hole(t2_eff, course["si"][h], num_holes)
                if t1n < t2n: cum += 1; hole_winners.append(1)
                elif t2n < t1n: cum -= 1; hole_winners.append(-1)
                else: hole_winners.append(0)
            else:
                hole_winners.append(0)
            if cum > 0: running_total.append(f"S+{cum}")
            elif cum < 0: running_total.append(f"G+{-cum}")
            else: running_total.append("AS")
        mp_data = {"hole_winners": hole_winners, "running_total": running_total}

        players_data = [
            {"name": "Team Shooter", "team": 1, "handicap": t1_eff, "scores": data["team_scores"].get(f"{match_idx}|t1", [0]*num_holes)},
            {"name": "Team Gilmore", "team": 2, "handicap": t2_eff, "scores": data["team_scores"].get(f"{match_idx}|t2", [0]*num_holes)},
        ]
        st.markdown("---")
        for html in build_scorecard_html(course_name, players_data, show_stableford=match["stableford"], match_play_data=mp_data):
            st.markdown(html, unsafe_allow_html=True)

        auto_calc_team_match(data, match_idx, course_name, num_holes, t1_eff, t2_eff)


def auto_calc_individual_match(data, match_idx, match_type, course_name, num_holes, t1_players, t2_players):
    if match_type == "bestball":
        all_done = True
        t1_total, t2_total = 0, 0
        for h in range(num_holes):
            t1_nets, t2_nets = [], []
            for p in t1_players:
                scores = data["scores"].get(f"{course_name}|{p}", [0]*num_holes)
                s = scores[h] if h < len(scores) else 0
                if s and s > 0:
                    t1_nets.append(calc_net(s, get_player_course_hdcp(data, p, course_name), course_name, h))
            for p in t2_players:
                scores = data["scores"].get(f"{course_name}|{p}", [0]*num_holes)
                s = scores[h] if h < len(scores) else 0
                if s and s > 0:
                    t2_nets.append(calc_net(s, get_player_course_hdcp(data, p, course_name), course_name, h))
            t1_valid = [n for n in t1_nets if n is not None]
            t2_valid = [n for n in t2_nets if n is not None]
            if not t1_valid or not t2_valid:
                all_done = False
            else:
                t1_total += min(t1_valid)
                t2_total += min(t2_valid)
        if all_done and t1_total > 0:
            if t1_total < t2_total: data["team_results"][match_idx] = "T1"
            elif t2_total < t1_total: data["team_results"][match_idx] = "T2"
            else: data["team_results"][match_idx] = "H"
            st.markdown(f"**Result:** Best Ball NET — Shooter: {t1_total} vs Gilmore: {t2_total}")
    elif match_type == "singles":
        p1, p2 = t1_players[0], t2_players[0]
        s1 = data["scores"].get(f"{course_name}|{p1}", [0]*num_holes)
        s2 = data["scores"].get(f"{course_name}|{p2}", [0]*num_holes)
        h1 = get_player_course_hdcp(data, p1, course_name)
        h2 = get_player_course_hdcp(data, p2, course_name)
        match_score = 0
        holes_done = 0
        for h in range(num_holes):
            sv1 = s1[h] if h < len(s1) else 0
            sv2 = s2[h] if h < len(s2) else 0
            if sv1 > 0 and sv2 > 0:
                n1 = calc_net(sv1, h1, course_name, h)
                n2 = calc_net(sv2, h2, course_name, h)
                if n1 and n2:
                    if n1 < n2: match_score += 1
                    elif n2 < n1: match_score -= 1
                holes_done += 1
        if holes_done == num_holes:
            if match_score > 0: data["team_results"][match_idx] = "T1"
            elif match_score < 0: data["team_results"][match_idx] = "T2"
            else: data["team_results"][match_idx] = "H"


def auto_calc_team_match(data, match_idx, course_name, num_holes, t1_eff, t2_eff):
    course = COURSES[course_name]
    si = course["si"]
    t1s = data["team_scores"].get(f"{match_idx}|t1", [0]*num_holes)
    t2s = data["team_scores"].get(f"{match_idx}|t2", [0]*num_holes)
    match_score = 0
    holes_done = 0
    for h in range(num_holes):
        if t1s[h] > 0 and t2s[h] > 0:
            t1n = t1s[h] - get_strokes_on_hole(t1_eff, si[h], num_holes)
            t2n = t2s[h] - get_strokes_on_hole(t2_eff, si[h], num_holes)
            if t1n < t2n: match_score += 1
            elif t2n < t1n: match_score -= 1
            holes_done += 1

    if holes_done == num_holes:
        if match_score > 0:
            data["team_results"][match_idx] = "T1"
            st.success(f"Team Shooter wins {match_score} up")
        elif match_score < 0:
            data["team_results"][match_idx] = "T2"
            st.error(f"Team Gilmore wins {-match_score} up")
        else:
            data["team_results"][match_idx] = "H"
            st.info("Halved")
    elif holes_done > 0:
        status = f"Shooter {match_score} up" if match_score > 0 else (f"Gilmore {-match_score} up" if match_score < 0 else "All Square")
        st.caption(f"Thru {holes_done} · {status}")


def page_pairings(data):
    st.markdown('<div class="section-header">Match Pairings</div>', unsafe_allow_html=True)
    st.caption("Set custom pairings for each match. Leave blank to use defaults.")

    if "pairings" not in data:
        data["pairings"] = {}

    changed = False
    for i, match in enumerate(SCHEDULE):
        with st.expander(f"Match {i+1}: {match['date']} – {match['course']} – {match['format']} (G{match['group']})"):
            custom_key = str(i)
            if match["type"] == "singles":
                existing = data["pairings"].get(custom_key, {})
                default_t1 = existing.get("t1", DEFAULT_PAIRINGS.get(match["group"], {}).get("t1", [TEAM_SHOOTER[0]]))
                default_t2 = existing.get("t2", DEFAULT_PAIRINGS.get(match["group"], {}).get("t2", [TEAM_GILMORE[0]]))
                t1_pick = st.selectbox(f"Team Shooter player", TEAM_SHOOTER, index=TEAM_SHOOTER.index(default_t1[0]) if default_t1[0] in TEAM_SHOOTER else 0, key=f"pair_t1_{i}")
                t2_pick = st.selectbox(f"Team Gilmore player", TEAM_GILMORE, index=TEAM_GILMORE.index(default_t2[0]) if default_t2[0] in TEAM_GILMORE else 0, key=f"pair_t2_{i}")
                new_pairing = {"t1": [t1_pick], "t2": [t2_pick]}
            else:
                existing = data["pairings"].get(custom_key, {})
                default_t1 = existing.get("t1", DEFAULT_PAIRINGS.get(match["group"], {}).get("t1", TEAM_SHOOTER[:2]))
                default_t2 = existing.get("t2", DEFAULT_PAIRINGS.get(match["group"], {}).get("t2", TEAM_GILMORE[:2]))
                t1_picks = st.multiselect(f"Team Shooter pair", TEAM_SHOOTER, default=default_t1, max_selections=2, key=f"pair_t1_{i}")
                t2_picks = st.multiselect(f"Team Gilmore pair", TEAM_GILMORE, default=default_t2, max_selections=2, key=f"pair_t2_{i}")
                new_pairing = {"t1": t1_picks if len(t1_picks) == 2 else default_t1, "t2": t2_picks if len(t2_picks) == 2 else default_t2}

            # Display current pairing with green background / white text
            st.markdown(
                f'<div style="background:#2a5a2a;padding:8px 12px;border-radius:6px;margin-top:8px;">'
                f'<span style="color:#ffffff;font-weight:600;">Shooter:</span> <span style="color:#ffffff;">{" & ".join(new_pairing["t1"])}</span>'
                f' &nbsp;vs&nbsp; '
                f'<span style="color:#ffffff;font-weight:600;">Gilmore:</span> <span style="color:#ffffff;">{" & ".join(new_pairing["t2"])}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

            if data["pairings"].get(custom_key) != new_pairing:
                data["pairings"][custom_key] = new_pairing
                changed = True

    if changed:
        save_data()
        st.success("Pairings updated!")


def page_team(data):
    st.markdown('<div class="section-header">Team Championship</div>', unsafe_allow_html=True)
    st.markdown('<p class="money-big">$500/player &middot; Winner Takes All</p>', unsafe_allow_html=True)
    st.caption(f"First to {WIN_THRESHOLD:g} of {TOTAL_TEAM_PTS}")

    t1_total, t2_total = calc_team_totals(data)

    col1, col2, col3 = st.columns([2, 1, 2])
    with col1:
        st.markdown(f'''
        <div class="team-score-box">
            <h3 class="team-shooter">TEAM SHOOTER</h3>
            <div class="score" style="color:#1a6b9a;">{t1_total:g}</div>
        </div>''', unsafe_allow_html=True)
    with col2:
        st.markdown("<div style='text-align:center;padding-top:30px;color:#4a7a4a;font-size:2rem;font-family:Playfair Display,serif;'>vs</div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f'''
        <div class="team-score-box">
            <h3 class="team-gilmore">TEAM GILMORE</h3>
            <div class="score" style="color:#9a1a1a;">{t2_total:g}</div>
        </div>''', unsafe_allow_html=True)

    if t1_total >= WIN_THRESHOLD:
        st.success("TEAM SHOOTER WINS!")
    elif t2_total >= WIN_THRESHOLD:
        st.success("TEAM GILMORE WINS!")
    elif t1_total == 8 and t2_total == 8:
        st.warning("DRAW — 8 to 8")

    st.markdown("---")
    st.caption("Results auto-calculated from scorecards. Expand to override.")

    for i, match in enumerate(SCHEDULE):
        r = data["team_results"][i]
        auto_label = {"T1": "Team Shooter", "T2": "Team Gilmore", "H": "Halved"}.get(r, "—")
        if r == "T1": color = "#1a6b9a"
        elif r == "T2": color = "#9a1a1a"
        elif r == "H": color = "#8a7a5a"
        else: color = "#bbb"

        st.markdown(
            f'<div style="display:flex;align-items:center;padding:8px 0;border-bottom:1px solid #e8e4dc;">'
            f'<span style="flex:3;font-size:0.85rem;">{match["course"]} · {match["format"]} · {match["date"]}</span>'
            f'<span style="flex:0 0 40px;text-align:center;font-size:0.85rem;">{match["pts"]} pt</span>'
            f'<span style="flex:1;text-align:right;font-weight:700;color:{color};font-size:0.85rem;">{auto_label}</span>'
            f'</div>',
            unsafe_allow_html=True
        )

        with st.expander("Override result", expanded=False):
            options = ["Auto", "Team Shooter", "Team Gilmore", "Halved", "—"]
            current = {"T1": "Team Shooter", "T2": "Team Gilmore", "H": "Halved"}.get(r, "—")
            idx = options.index(current) if current in options else 0
            result = st.selectbox("", options, index=idx, key=f"tr_{i}", label_visibility="collapsed")
            if result != "Auto":
                data["team_results"][i] = {"Team Shooter": "T1", "Team Gilmore": "T2", "Halved": "H", "—": None}[result]


def page_individual(data):
    st.markdown('<div class="section-header">Individual Championship</div>', unsafe_allow_html=True)
    st.markdown('<p class="money-big">$500 Entry &middot; 1st: $2,000 &middot; 2nd: $1,250 &middot; 3rd: $750</p>', unsafe_allow_html=True)
    st.caption("NET Stableford across 3 rounds (Albatross 5 · Eagle 4 · Birdie 3 · Par 2 · Bogey 1 · Double+ 0)")
    st.markdown("---")

    results = []
    for player in ALL_PLAYERS:
        row = {"Player": player}
        total = 0
        for course in STABLEFORD_COURSES:
            pts = get_player_stableford(data, player, course)
            row[course] = pts
            total += pts
        row["Total"] = total
        results.append(row)
    results.sort(key=lambda x: x["Total"], reverse=True)

    lb_html = '<table class="lb-table"><thead><tr><th>Pos</th><th>Player</th>'
    for c in STABLEFORD_COURSES:
        lb_html += f'<th>{c}</th>'
    lb_html += '<th>Total</th></tr></thead><tbody>'
    for rank, r in enumerate(results, 1):
        team_class = "team-shooter" if r["Player"] in TEAM_SHOOTER else "team-gilmore"
        row_class = "top-row" if rank <= 3 else ("bottom-row" if rank > 3 else "")
        course_cells = "".join(f'<td>{r[c]}</td>' for c in STABLEFORD_COURSES)
        lb_html += f'<tr class="{row_class}"><td>{rank}</td><td class="{team_class}">{r["Player"]}</td>{course_cells}<td style="font-weight:700;">{r["Total"]}</td></tr>'
    lb_html += '</tbody></table>'
    st.markdown(lb_html, unsafe_allow_html=True)


def page_og_belt(data):
    st.markdown('<div class="section-header">OG Belt</div>', unsafe_allow_html=True)
    st.markdown('<p class="money-big">$750 Buy-in &middot; 1st: $2,000 &middot; 2nd: $1,000</p>', unsafe_allow_html=True)
    st.caption("Gross Stableford rank (4/3/2/1) + 0.5 per team point")
    st.markdown("---")

    og_scores = {}
    for player in OGS:
        og_scores[player] = {}
        for course in STABLEFORD_COURSES:
            og_scores[player][course] = get_player_gross_stableford(data, player, course)

    # Gross stableford table
    og_html = '<table class="lb-table"><thead><tr><th style="min-width:130px;white-space:nowrap;">Player</th>'
    for c in STABLEFORD_COURSES:
        og_html += f'<th>{c}</th>'
    og_html += '<th>Total</th></tr></thead><tbody>'
    for player in OGS:
        team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
        total = sum(og_scores[player].values())
        cells = "".join(f'<td>{og_scores[player][c]}</td>' for c in STABLEFORD_COURSES)
        og_html += f'<tr><td class="{team_class}" style="white-space:nowrap;">{player}</td>{cells}<td style="font-weight:700;">{total}</td></tr>'
    og_html += '</tbody></table>'
    st.markdown("**Gross Stableford**")
    st.markdown(og_html, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("**Team Point Bonus (auto-calculated: +0.5 per team match win)**")
    og_team_pts = calc_og_team_bonus(data)
    cols = st.columns(4)
    for i, player in enumerate(OGS):
        cols[i].markdown(f"<div style='text-align:center;font-size:0.9rem;'><strong>{player.split()[0]}</strong><br>{og_team_pts[player]} wins = +{og_team_pts[player]*0.5:.1f}</div>", unsafe_allow_html=True)

    rank_pts = calc_og_rank_pts(og_scores)

    final = []
    for player in OGS:
        bonus = og_team_pts[player] * 0.5
        final.append({"Player": player, "Rank Pts": rank_pts[player], "Bonus": bonus, "Total": rank_pts[player] + bonus})
    final.sort(key=lambda x: x["Total"], reverse=True)

    st.markdown("---")
    st.markdown("**Standings**")
    stand_html = '<table class="lb-table"><thead><tr><th>Pos</th><th>Player</th><th>Rank Pts</th><th>Bonus</th><th>Total</th></tr></thead><tbody>'
    for rank, r in enumerate(final, 1):
        team_class = "team-shooter" if r["Player"] in TEAM_SHOOTER else "team-gilmore"
        row_class = "top-row" if rank == 1 else ""
        stand_html += f'<tr class="{row_class}"><td>{rank}</td><td class="{team_class}">{r["Player"]}</td><td>{r["Rank Pts"]}</td><td>{r["Bonus"]:.1f}</td><td style="font-weight:700;">{r["Total"]:.1f}</td></tr>'
    stand_html += '</tbody></table>'
    st.markdown(stand_html, unsafe_allow_html=True)


def page_skins(data):
    st.markdown('<div class="section-header">Skins</div>', unsafe_allow_html=True)
    pot_per_round = 100 * len(ALL_PLAYERS)
    st.markdown(f'<p class="money-big">${pot_per_round:,} Pot Per Round</p>', unsafe_allow_html=True)
    st.caption("$100/round · Must NET par on following hole to collect · H18 validates on H1")
    st.markdown("---")

    # Grand total across all rounds
    grand_skins = {p: 0 for p in ALL_PLAYERS}
    all_course_data = {}

    for course_name in STABLEFORD_COURSES:
        course = COURSES[course_name]
        pars = course["par"]
        num_holes = course["holes"]

        net_scores = {}
        for player in ALL_PLAYERS:
            key = f"{course_name}|{player}"
            scores = data["scores"].get(key, [0] * num_holes)
            hdcp = get_player_course_hdcp(data, player, course_name)
            net_scores[player] = [
                calc_net(scores[i], hdcp, course_name, i)
                if i < len(scores) and scores[i] and scores[i] > 0 else None
                for i in range(num_holes)
            ]

        skins_count = {p: 0 for p in ALL_PLAYERS}
        skin_holes = {}  # hole_idx -> winning player
        for h in range(num_holes):
            hole_nets = {p: net_scores[p][h] for p in ALL_PLAYERS if net_scores[p][h] is not None}
            if hole_nets:
                min_net = min(hole_nets.values())
                leaders = [p for p, n in hole_nets.items() if n == min_net]
                if len(leaders) == 1:
                    next_h = (h + 1) % num_holes
                    nxt = net_scores[leaders[0]][next_h]
                    if nxt is not None and nxt <= pars[next_h]:
                        skins_count[leaders[0]] += 1
                        skin_holes[h] = leaders[0]

        for p in ALL_PLAYERS:
            grand_skins[p] += skins_count[p]
        all_course_data[course_name] = {"net_scores": net_scores, "skins_count": skins_count, "skin_holes": skin_holes}

    # Grand summary table
    total_all_skins = sum(grand_skins.values())
    per_skin = pot_per_round / total_all_skins if total_all_skins > 0 else 0
    winners = [(p, grand_skins[p]) for p in ALL_PLAYERS if grand_skins[p] > 0]
    winners.sort(key=lambda x: x[1], reverse=True)

    st.markdown("**Overall Skins Standings**")
    if winners:
        win_html = '<table class="lb-table"><thead><tr><th>Player</th><th>Skins</th><th>Winnings</th></tr></thead><tbody>'
        for player, count in winners:
            team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
            win_html += f'<tr><td class="{team_class}">{player}</td><td style="font-size:1.1rem;">{count}</td><td style="font-weight:700;color:#2a5a2a;font-family:Playfair Display,serif;font-size:1.4rem;">${count * per_skin:,.0f}</td></tr>'
        win_html += '</tbody></table>'
        st.markdown(win_html, unsafe_allow_html=True)
    else:
        st.info("No skins won yet.")

    # Per-course scorecards with skin highlights
    for course_name in STABLEFORD_COURSES:
        st.markdown("---")
        st.markdown(f"**{course_name}**")
        course = COURSES[course_name]
        pars = course["par"]
        num_holes = course["holes"]
        cd = all_course_data[course_name]
        net_scores = cd["net_scores"]
        skin_holes = cd["skin_holes"]
        skins_count = cd["skins_count"]

        # Build scorecard with par row and skin highlights
        if num_holes >= 18:
            sections = [(0, 9, "OUT"), (9, num_holes, "IN")]
        else:
            sections = [(0, num_holes, "TOT")]

        for sec_start, sec_end, sec_label in sections:
            html = '<table class="sc-table"><thead><tr><th style="text-align:left;width:55px;">HOLE</th>'
            for h in range(sec_start, sec_end):
                html += f'<th>{h+1}</th>'
            html += f'<th class="turn-col">{sec_label}</th>'
            if sec_label == "IN":
                html += '<th class="total-col">TOT</th>'
            html += '</tr></thead><tbody>'

            # Par row
            html += '<tr class="par-row"><td style="text-align:left;">PAR</td>'
            sec_par = sum(pars[sec_start:sec_end])
            for h in range(sec_start, sec_end):
                html += f'<td>{pars[h]}</td>'
            html += f'<td class="turn-col">{sec_par}</td>'
            if sec_label == "IN":
                html += f'<td class="total-col">{sum(pars)}</td>'
            html += '</tr>'

            # Player net score rows
            for player in ALL_PLAYERS:
                team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
                html += f'<tr><td class="player-header {team_class}">{player.split()[0]}</td>'
                sec_total = 0
                for h in range(sec_start, sec_end):
                    v = net_scores[player][h]
                    is_skin = (h in skin_holes and skin_holes[h] == player)
                    style = ""
                    if is_skin:
                        style = ' style="background:#c8e6c9;font-weight:700;color:#1a5a1a;border:2px solid #2a8a2a;border-radius:4px;"'
                    cell_val = v if v is not None else "-"
                    if v is not None:
                        sec_total += v
                    html += f'<td{style}>{cell_val}</td>'
                total_net = sum(n for n in net_scores[player] if n is not None)
                html += f'<td class="turn-col">{sec_total if sec_total else "-"}</td>'
                if sec_label == "IN":
                    html += f'<td class="total-col">{total_net if total_net else "-"}</td>'
                html += '</tr>'

            html += '</tbody></table>'
            st.markdown(html, unsafe_allow_html=True)

        # Per-course skins count
        course_winners = [(p, skins_count[p]) for p in ALL_PLAYERS if skins_count[p] > 0]
        if course_winners:
            course_winners.sort(key=lambda x: x[1], reverse=True)
            txt = " · ".join(f"{p.split()[0]}: {c}" for p, c in course_winners)
            st.caption(f"Skins: {txt}")


def page_bets(data):
    st.markdown('<div class="section-header">Bets & Ledger</div>', unsafe_allow_html=True)

    # Initialize ledger in data if missing
    if "ledger" not in data:
        data["ledger"] = []

    # ─── Section 1: Winnings Calculator ─────────────────────────────────────
    st.markdown("""
    <div class="card">
        <div class="card-title">Tournament Winnings Summary</div>
    </div>
    """, unsafe_allow_html=True)

    # Entry fee
    entry_fee = st.number_input("Entry Fee per Player ($)", value=100, step=25, key="bet_entry_fee")
    total_pot = entry_fee * len(ALL_PLAYERS)

    # Pot allocation
    st.markdown("**Pot Allocation**")
    col1, col2, col3 = st.columns(3)
    with col1:
        skins_pct = st.number_input("Skins %", value=50, min_value=0, max_value=100, key="bet_skins_pct")
    with col2:
        indiv_pct = st.number_input("Individual Champ %", value=30, min_value=0, max_value=100, key="bet_indiv_pct")
    with col3:
        team_pct = st.number_input("Team Champ %", value=20, min_value=0, max_value=100, key="bet_team_pct")

    alloc_total = skins_pct + indiv_pct + team_pct
    if alloc_total != 100:
        st.warning(f"Allocation totals {alloc_total}% — should be 100%")

    skins_pot = total_pot * skins_pct / 100
    indiv_pot = total_pot * indiv_pct / 100
    team_pot = total_pot * team_pct / 100

    st.markdown(f"**Total Pot: ${total_pot:,.0f}** — Skins: ${skins_pot:,.0f} · Individual: ${indiv_pot:,.0f} · Team: ${team_pot:,.0f}")

    # Calculate skins winnings from data
    from collections import defaultdict
    STABLEFORD_COURSES_LIST = ["Pacific Dunes", "Old Macdonald", "Bandon Trails"]
    grand_skins = {p: 0 for p in ALL_PLAYERS}

    for course_name in STABLEFORD_COURSES_LIST:
        if course_name not in COURSES:
            continue
        course = COURSES[course_name]
        pars = course["par"]
        num_holes = course["holes"]
        net_scores = {}
        for player in ALL_PLAYERS:
            key = f"{course_name}|{player}"
            scores = data["scores"].get(key, [0] * num_holes)
            hdcp = get_player_course_hdcp(data, player, course_name)
            net_scores[player] = [
                calc_net(scores[i], hdcp, course_name, i)
                if i < len(scores) and scores[i] and scores[i] > 0 else None
                for i in range(num_holes)
            ]
        for h in range(num_holes):
            hole_nets = {p: net_scores[p][h] for p in ALL_PLAYERS if net_scores[p][h] is not None}
            if hole_nets:
                min_net = min(hole_nets.values())
                leaders = [p for p, n in hole_nets.items() if n == min_net]
                if len(leaders) == 1:
                    next_h = (h + 1) % num_holes
                    nxt = net_scores[leaders[0]][next_h]
                    if nxt is not None and nxt <= pars[next_h]:
                        grand_skins[leaders[0]] += 1

    total_skins = sum(grand_skins.values())
    per_skin_val = skins_pot / total_skins if total_skins > 0 else 0

    # Build winnings table
    winnings = {p: 0.0 for p in ALL_PLAYERS}
    for p in ALL_PLAYERS:
        winnings[p] += grand_skins[p] * per_skin_val

    # Show winnings summary
    win_data = [(p, grand_skins[p], winnings[p], winnings[p] - entry_fee) for p in ALL_PLAYERS]
    win_data.sort(key=lambda x: x[3], reverse=True)

    win_html = '<table class="lb-table"><thead><tr><th>Player</th><th>Skins</th><th>Winnings</th><th>Net (+/-)</th></tr></thead><tbody>'
    for player, skins, won, net in win_data:
        team_class = "team-shooter" if player in TEAM_SHOOTER else "team-gilmore"
        net_color = "#2a5a2a" if net >= 0 else "#9a1a1a"
        net_str = f"+${net:,.0f}" if net >= 0 else f"-${abs(net):,.0f}"
        win_html += f'<tr><td class="{team_class}">{player}</td><td>{skins}</td><td>${won:,.0f}</td><td style="color:{net_color};font-weight:700;">{net_str}</td></tr>'
    win_html += '</tbody></table>'
    st.markdown(win_html, unsafe_allow_html=True)

    # ─── Section 2: Side Bets Ledger ────────────────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <div class="card-title">Side Bets & Group Purchases</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("*Record side bets between players or group purchases (food, drinks, etc.)*")

    # Add new ledger entry
    with st.expander("➕ Add Ledger Entry", expanded=False):
        entry_type = st.radio("Type", ["Side Bet", "Group Purchase"], key="ledger_type", horizontal=True)

        if entry_type == "Side Bet":
            col1, col2 = st.columns(2)
            with col1:
                bet_from = st.selectbox("Loser (owes)", ALL_PLAYERS, key="bet_from")
            with col2:
                bet_to = st.selectbox("Winner (gets paid)", ALL_PLAYERS, key="bet_to")
            bet_amount = st.number_input("Amount ($)", value=10.0, min_value=0.0, step=5.0, key="bet_amount")
            bet_desc = st.text_input("Description", placeholder="e.g., Nassau press on hole 14", key="bet_desc")

            if st.button("Add Side Bet", key="add_bet"):
                if bet_from == bet_to:
                    st.error("Can't bet against yourself!")
                elif bet_amount <= 0:
                    st.error("Amount must be positive")
                else:
                    data["ledger"].append({
                        "type": "side_bet",
                        "from": bet_from,
                        "to": bet_to,
                        "amount": bet_amount,
                        "desc": bet_desc or "Side bet",
                    })
                    st.success(f"Added: {bet_from} owes {bet_to} ${bet_amount:.0f}")
                    st.rerun()

        else:  # Group Purchase
            purchaser = st.selectbox("Who paid?", ALL_PLAYERS, key="purchase_by")
            purchase_amount = st.number_input("Total Amount ($)", value=50.0, min_value=0.0, step=5.0, key="purchase_amount")
            purchase_desc = st.text_input("What was it?", placeholder="e.g., Beers at the turn", key="purchase_desc")
            split_among = st.multiselect("Split among", ALL_PLAYERS, default=ALL_PLAYERS, key="purchase_split")

            if st.button("Add Group Purchase", key="add_purchase"):
                if not split_among:
                    st.error("Select at least one person to split with")
                elif purchase_amount <= 0:
                    st.error("Amount must be positive")
                else:
                    data["ledger"].append({
                        "type": "group_purchase",
                        "paid_by": purchaser,
                        "amount": purchase_amount,
                        "desc": purchase_desc or "Group purchase",
                        "split_among": split_among,
                    })
                    st.success(f"Added: {purchaser} paid ${purchase_amount:.0f} split among {len(split_among)} people")
                    st.rerun()

    # Display current ledger
    if data["ledger"]:
        st.markdown("**Current Ledger**")
        ledger_html = '<table class="sched-table"><thead><tr><th>#</th><th>Type</th><th>Description</th><th>Details</th><th>Amount</th></tr></thead><tbody>'
        for i, entry in enumerate(data["ledger"]):
            row_class = "row-a" if i % 2 == 0 else "row-b"
            if entry["type"] == "side_bet":
                details = f"{entry['from']} → {entry['to']}"
                ledger_html += f'<tr class="{row_class}"><td>{i+1}</td><td>🎲 Bet</td><td>{entry["desc"]}</td><td>{details}</td><td>${entry["amount"]:.0f}</td></tr>'
            else:
                split_names = ", ".join(p.split()[0] for p in entry["split_among"])
                details = f"{entry['paid_by']} paid · split: {split_names}"
                ledger_html += f'<tr class="{row_class}"><td>{i+1}</td><td>🛒 Purchase</td><td>{entry["desc"]}</td><td>{details}</td><td>${entry["amount"]:.0f}</td></tr>'
        ledger_html += '</tbody></table>'
        st.markdown(ledger_html, unsafe_allow_html=True)

        # Delete entry
        with st.expander("🗑️ Remove Entry"):
            del_idx = st.number_input("Entry # to remove", min_value=1, max_value=len(data["ledger"]), value=1, key="del_ledger_idx")
            if st.button("Remove", key="del_ledger"):
                data["ledger"].pop(del_idx - 1)
                st.success("Removed!")
                st.rerun()

    # ─── Section 3: Settlement - Who Owes Who ───────────────────────────────
    st.markdown("---")
    st.markdown("""
    <div class="card">
        <div class="card-title">Settlement — Who Owes Who</div>
    </div>
    """, unsafe_allow_html=True)

    # Calculate net balances from ledger
    balances = {p: 0.0 for p in ALL_PLAYERS}

    for entry in data["ledger"]:
        if entry["type"] == "side_bet":
            balances[entry["from"]] -= entry["amount"]
            balances[entry["to"]] += entry["amount"]
        elif entry["type"] == "group_purchase":
            share = entry["amount"] / len(entry["split_among"])
            balances[entry["paid_by"]] += entry["amount"]  # they paid
            for p in entry["split_among"]:
                balances[p] -= share  # everyone owes their share

    # Simplify debts - greedy algorithm
    debtors = [(p, -balances[p]) for p in ALL_PLAYERS if balances[p] < -0.01]
    creditors = [(p, balances[p]) for p in ALL_PLAYERS if balances[p] > 0.01]
    debtors.sort(key=lambda x: x[1], reverse=True)
    creditors.sort(key=lambda x: x[1], reverse=True)

    settlements = []
    d_idx, c_idx = 0, 0
    d_amounts = [amt for _, amt in debtors]
    c_amounts = [amt for _, amt in creditors]

    while d_idx < len(debtors) and c_idx < len(creditors):
        pay = min(d_amounts[d_idx], c_amounts[c_idx])
        if pay > 0.01:
            settlements.append((debtors[d_idx][0], creditors[c_idx][0], pay))
        d_amounts[d_idx] -= pay
        c_amounts[c_idx] -= pay
        if d_amounts[d_idx] < 0.01:
            d_idx += 1
        if c_amounts[c_idx] < 0.01:
            c_idx += 1

    if settlements:
        settle_html = '<table class="lb-table"><thead><tr><th>From</th><th>To</th><th>Amount</th></tr></thead><tbody>'
        for payer, payee, amount in settlements:
            payer_class = "team-shooter" if payer in TEAM_SHOOTER else "team-gilmore"
            payee_class = "team-shooter" if payee in TEAM_SHOOTER else "team-gilmore"
            settle_html += f'<tr><td class="{payer_class}">{payer}</td><td class="{payee_class}">{payee}</td><td style="font-weight:700;color:#2a5a2a;font-size:1.2rem;">${amount:,.2f}</td></tr>'
        settle_html += '</tbody></table>'
        st.markdown(settle_html, unsafe_allow_html=True)
    else:
        st.info("No ledger entries yet — add side bets or purchases above.")


def page_rules():
    st.markdown('<div class="section-header">Rules & Scoring</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Team Championship (16 pts available · First to 8.5)</div>
        <p style="margin:8px 0;">16 matches across 4 days. Each match is worth <strong>1 point</strong>. Halved matches award 0.5 to each team. First team to 8.5 points wins the Team Championship.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Match Formats</div>
        <table class="sched-table">
            <thead><tr><th>Format</th><th>Scoring</th><th>Description</th></tr></thead>
            <tbody>
                <tr class="row-a"><td><strong>2v2 Scramble</strong></td><td>Match Play</td><td>Both players hit, pick the best ball, both play from there. Repeat until holed. Hole-by-hole winner.</td></tr>
                <tr class="row-b"><td><strong>2v2 Best Ball</strong></td><td>Stroke Play (NET)</td><td>All players play their own ball. Best NET score from each team counts per hole. Lowest total NET wins.</td></tr>
                <tr class="row-a"><td><strong>2v2 Modified Alt Shot</strong></td><td>Match Play</td><td>Both hit tee shots, pick one, then alternate from there. Hole-by-hole winner.</td></tr>
                <tr class="row-b"><td><strong>2v2 Alt Shot</strong></td><td>Match Play</td><td>One player tees off, then alternate shots until holed. Switch who tees off each hole. Hole-by-hole winner.</td></tr>
                <tr class="row-a"><td><strong>Singles</strong></td><td>Match Play (NET)</td><td>1v1 individual match play with handicap strokes applied. Hole-by-hole winner.</td></tr>
            </tbody>
        </table>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Handicap Calculations</div>
        <p style="margin:8px 0;"><strong>Course Handicap:</strong> Auto-calculated from your Handicap Index: Index &times; (Slope / 113) + (Course Rating &minus; Par), rounded. Per-course overrides on the Handicaps tab take priority.</p>
        <p style="margin:8px 0;"><strong>Stroke Allocation:</strong> Strokes are allocated by Stroke Index (S.I.). A 10-handicap receives 1 stroke on each of the 10 hardest holes (S.I. 1–10). An 18+ handicap receives 2 strokes on the hardest holes first.</p>
        <hr style="border-color:#e8e4dc;margin:12px 0;">
        <p style="margin:8px 0;font-weight:600;">Team Format Handicaps (calculated as a team, then difference applied):</p>
        <table class="sched-table" style="margin-top:8px;">
            <thead><tr><th>Format</th><th>Formula</th></tr></thead>
            <tbody>
                <tr class="row-a"><td>Scramble</td><td>35% of low handicap + 15% of high handicap</td></tr>
                <tr class="row-b"><td>Modified Alt Shot</td><td>60% of low handicap + 40% of high handicap</td></tr>
                <tr class="row-a"><td>Alt Shot</td><td>50% of combined Course Handicaps, rounded .5 up</td></tr>
                <tr class="row-b"><td>Best Ball / Singles</td><td>Full individual course handicap</td></tr>
            </tbody>
        </table>
        <p style="margin:8px 0;color:#6b8f6b;font-size:0.85rem;">In team match play, only the <em>difference</em> between team handicaps matters. The higher-handicap team receives that many strokes on the hardest S.I. holes.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Individual Championship (NET Stableford)</div>
        <p style="margin:8px 0;">Played on <strong>3 courses</strong>: Pacific Dunes, Old Macdonald, and Bandon Trails. Each player's NET score per hole is converted to Stableford points:</p>
        <table class="sched-table" style="margin-top:8px;">
            <thead><tr><th>Net vs Par</th><th>Points</th></tr></thead>
            <tbody>
                <tr class="row-a"><td>Albatross or better (≤ -3)</td><td><strong>5</strong></td></tr>
                <tr class="row-b"><td>Eagle (-2)</td><td><strong>4</strong></td></tr>
                <tr class="row-a"><td>Birdie (-1)</td><td><strong>3</strong></td></tr>
                <tr class="row-b"><td>Par (0)</td><td><strong>2</strong></td></tr>
                <tr class="row-a"><td>Bogey (+1)</td><td><strong>1</strong></td></tr>
                <tr class="row-b"><td>Double bogey or worse (≥ +2)</td><td><strong>0</strong></td></tr>
            </tbody>
        </table>
        <p style="margin:8px 0;">Total Stableford points across all 3 rounds determines the Individual Champion.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">OG Belt (Gross Stableford · OGs Only)</div>
        <p style="margin:8px 0;">Same 3 courses. Uses <strong>GROSS</strong> Stableford (no handicap adjustment). Players are ranked 1st–4th on each course with rank points:</p>
        <table class="sched-table" style="margin-top:8px;">
            <thead><tr><th>Rank</th><th>Points</th></tr></thead>
            <tbody>
                <tr class="row-a"><td>1st</td><td>4</td></tr>
                <tr class="row-b"><td>2nd</td><td>3</td></tr>
                <tr class="row-a"><td>3rd</td><td>2</td></tr>
                <tr class="row-b"><td>4th</td><td>1</td></tr>
            </tbody>
        </table>
        <p style="margin:8px 0;">Ties split the points evenly. A team bonus of +1 is added for each winning team match an OG participated in. Highest total wins the OG Belt.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Skins ($100/player/round · $800 pot per course)</div>
        <p style="margin:8px 0;">Played on Pacific Dunes, Old Macdonald, and Bandon Trails (same 3 stableford courses).</p>
        <p style="margin:8px 0;"><strong>How to win a skin:</strong></p>
        <ol style="margin:8px 0 8px 20px;line-height:1.8;">
            <li>Have the <strong>sole lowest NET score</strong> on a hole (no ties)</li>
            <li><strong>Validate it</strong> by scoring NET par or better on the <em>next</em> hole (hole 18 wraps to hole 1)</li>
        </ol>
        <p style="margin:8px 0;">Total skins per round split the $800 pot evenly. Example: 4 total skins = $200/skin.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">Scorecard Key</div>
        <p style="margin:8px 0;"><span style="color:#c17a3a;font-weight:700;">●</span> / <span style="color:#c17a3a;font-weight:700;">●●</span> = Handicap strokes received on that hole</p>
        <p style="margin:8px 0;"><span style="background:#c8e6c9;padding:2px 6px;border-radius:3px;border:2px solid #2a8a2a;font-weight:700;color:#1a5a1a;">4</span> = Won the hole (match play) or won a skin</p>
        <p style="margin:8px 0;"><span style="background:#ffcdd2;padding:2px 6px;border-radius:3px;border:2px solid #c62828;font-weight:700;color:#9a1a1a;">G+1</span> = Opponent leads by 1 (match status)</p>
        <p style="margin:8px 0;"><strong>AS</strong> = All Square &nbsp;|&nbsp; <strong>S+2</strong> = Shooter 2 up &nbsp;|&nbsp; <strong>G+1</strong> = Gilmore 1 up</p>
    </div>
    """, unsafe_allow_html=True)


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    data = load_data()

    with st.sidebar:
        st.markdown("""
        <div style="padding:16px 0;">
            <p style="font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:#f5f0e8;margin-bottom:2px;">
                THE BATTLE AT BANDON
            </p>
            <p style="font-size:0.65rem;color:#c5b89a;letter-spacing:1px;text-transform:uppercase;">
                6th Annual Chubbs Peterson Invitational
            </p>
        </div>
        """, unsafe_allow_html=True)

        page = st.radio("", [
            "Leaderboard & Schedule",
            "Handicaps",
            "Scorecards",
            "Pairings",
            "Team Championship",
            "Individual Championship",
            "OG Belt",
            "Skins",
            "Bets & Ledger",
            "Rules",
        ], label_visibility="collapsed")

        st.markdown("---")
        st.markdown(f"""
        <div style="font-size:1rem;">
            <p class="sidebar-shooter" style="font-weight:700;font-size:1.1rem;margin-bottom:6px;">TEAM SHOOTER</p>
            <p style="line-height:1.8;font-size:1rem;">{'<br>'.join(TEAM_SHOOTER)}</p>
            <p class="sidebar-gilmore" style="font-weight:700;font-size:1.1rem;margin-top:16px;margin-bottom:6px;">TEAM GILMORE</p>
            <p style="line-height:1.8;font-size:1rem;">{'<br>'.join(TEAM_GILMORE)}</p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        if st.button("Save", use_container_width=True, type="primary"):
            save_data()
            st.success("Saved!")
        if st.button("Reset All Scores", use_container_width=True):
            reset_data()

    if "Leaderboard" in page: page_leaderboard(data)
    elif "Handicaps" in page: page_handicaps(data)
    elif "Scorecards" in page: page_scorecards(data)
    elif "Pairings" in page: page_pairings(data)
    elif "Team Champ" in page: page_team(data)
    elif "Individual" in page: page_individual(data)
    elif "OG Belt" in page: page_og_belt(data)
    elif "Skins" in page: page_skins(data)
    elif "Bets" in page: page_bets(data)
    elif "Rules" in page: page_rules()

    st.session_state.data = data


if __name__ == "__main__":
    main()
