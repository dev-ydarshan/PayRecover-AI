"""PayRecover AI — Explainable Revenue Recovery Agent.

The presentation layer is redesigned for a premium fintech command-center feel.
The recovery engine, Supabase access, intervention execution, audit trail and
payment outcome controls continue to use the existing project modules.
"""

import html
import math
import base64
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import streamlit as st

import config
import db
import decision_engine
import outcome_tracker

# Project identity marker — presentation layer only.
PAYRECOVER_PROJECT_NAME = "PayRecover AI — Explainable Revenue Recovery Agent"

st.set_page_config(
    page_title="PayRecover",
  page_icon=str(Path(__file__).with_name("razorpay-logo.svg")),
    layout="wide",
    initial_sidebar_state="expanded",
)

RAZORPAY_LOGO_DATA_URI = "data:image/svg+xml;base64," + base64.b64encode(
  Path(__file__).with_name("razorpay-logo.svg").read_bytes()
).decode("ascii")

# ---------------------------------------------------------------------------
# Visual system — intentionally scoped to presentation only.
# ---------------------------------------------------------------------------
PAGE_CSS = r"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Manrope:wght@600;700;800&display=swap');

:root{
  --navy:#061a4b;
  --navy-2:#0b2f80;
  --blue:#1769ff;
  --blue-2:#2ea7ff;
  --cyan:#18c9e8;
  --green:#10b981;
  --purple:#7447ff;
  --orange:#ff9d1f;
  --ink:#071b4f;
  --muted:#657793;
  --line:#d9e7f8;
  --page:#f4f8ff;
}

html,body,[class*="css"]{
  font-family:Inter,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;
}
.stApp{
  color:var(--ink);
  background:
    radial-gradient(circle at 78% 2%,rgba(38,133,255,.18),transparent 26%),
    radial-gradient(circle at 16% 30%,rgba(116,71,255,.08),transparent 24%),
    linear-gradient(135deg,#f8fbff 0%,#eef5ff 52%,#f8fbff 100%);
}
[data-testid="stHeader"]{background:transparent}
[data-testid="stToolbar"],footer{visibility:hidden}
[data-testid="stDecoration"]{display:none}
.main .block-container{position:relative}
.main .block-container:before{content:"";position:fixed;inset:74px 0 0 0;pointer-events:none;opacity:.28;background-image:radial-gradient(#9ab8df 0.65px,transparent 0.65px);background-size:18px 18px;mask-image:linear-gradient(to bottom,black 0%,transparent 88%);z-index:0}
.main .block-container>*{position:relative;z-index:1}
.block-container{max-width:1540px;margin-left:auto;margin-right:auto;padding:16px 18px 118px}.anchor-target{scroll-margin-top:18px;height:1px;width:1px;position:relative;top:-1px}.nav-section-label{margin:15px 8px 7px;color:#7fa7df!important;font-size:8px;font-weight:900;letter-spacing:1.2px;text-transform:uppercase}

/* ---------------- native sidebar ---------------- */
section[data-testid="stSidebar"]{
  min-width:258px!important; max-width:258px!important; width:258px!important;
  visibility:visible!important; transform:none!important;
  background:linear-gradient(180deg,#04133a 0%,#06235f 55%,#03163f 100%)!important;
  border-right:1px solid rgba(255,255,255,.10);
  box-shadow:18px 0 45px rgba(3,19,58,.14);
}
section[data-testid="stSidebar"]>div{padding:18px 14px 22px!important;}
section[data-testid="stSidebar"] [data-testid="stSidebarContent"],section[data-testid="stSidebar"]>div>div{padding-top:0!important;margin-top:0!important;}
section[data-testid="stSidebar"]>div{padding-top:8px!important;}
section[data-testid="stSidebar"]>div:first-child{margin-top:0!important;}
section[data-testid="stSidebar"] *{box-sizing:border-box;}
section[data-testid="stSidebar"] .sidebar-brand{padding:7px 8px 18px;border-bottom:1px solid rgba(255,255,255,.10);margin-bottom:13px;}
section[data-testid="stSidebar"] .sidebar-brand{transform:translateY(-35px);margin-bottom:-22px;}
section[data-testid="stSidebar"] .rp-logo-row{display:flex;align-items:center;gap:9px;}
section[data-testid="stSidebar"] .rp-mark{width:42px;height:42px;border-radius:12px;display:block;object-fit:contain;background:#fff;padding:4px;box-shadow:0 10px 25px rgba(22,105,255,.35),inset 0 1px 0 rgba(255,255,255,.35);}
section[data-testid="stSidebar"] .rp-word{font-family:Manrope,Inter,sans-serif;font-weight:800;font-size:23px;letter-spacing:-1.1px;color:#fff!important;}
section[data-testid="stSidebar"] .product-title{margin-top:15px;font-size:17px;font-weight:850;color:#fff!important;}
section[data-testid="stSidebar"] .product-copy{color:#a9c4ee!important;font-size:10px;margin-top:3px;}
section[data-testid="stSidebar"] .nav-section-label{margin:16px 8px 7px;color:#86a9dd!important;font-size:8px;font-weight:900;letter-spacing:1.2px;text-transform:uppercase;}
section[data-testid="stSidebar"] .nav-pill{display:flex;align-items:center;gap:10px;padding:10px 11px;margin:5px 0;border-radius:12px;color:#dbe9ff!important;text-decoration:none!important;font-size:12px;font-weight:700;border:1px solid transparent;cursor:pointer;transition:all .15s ease;}
section[data-testid="stSidebar"] .nav-pill:hover{background:rgba(255,255,255,.09);border-color:rgba(255,255,255,.10);transform:translateX(2px);}
section[data-testid="stSidebar"] .nav-pill.active{background:linear-gradient(100deg,#1267ff,#2d9cff);color:#fff!important;box-shadow:0 12px 26px rgba(18,103,255,.38),inset 0 1px 0 rgba(255,255,255,.24);}
section[data-testid="stSidebar"] .nav-icon{width:24px;height:24px;display:grid;place-items:center;border-radius:8px;background:rgba(255,255,255,.08);color:#b9d4ff!important;font-size:13px;}
section[data-testid="stSidebar"] .nav-pill.active .nav-icon{background:rgba(255,255,255,.18);color:#fff!important;}
section[data-testid="stSidebar"] .nav-pill.active{background:transparent;color:#dbe9ff!important;box-shadow:none;}
section[data-testid="stSidebar"] .nav-pill[href="#dashboard"]{background:linear-gradient(100deg,#1267ff,#2d9cff);color:#fff!important;box-shadow:0 12px 26px rgba(18,103,255,.38),inset 0 1px 0 rgba(255,255,255,.24);}
section[data-testid="stSidebar"] .nav-pill[href="#dashboard"] .nav-icon{background:rgba(255,255,255,.18);color:#fff!important;}
body:has(#failed-payments:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#recovery-actions:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#customers:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#analytics:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#ai-insights:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#audit-log:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"],body:has(#settings:target) section[data-testid="stSidebar"] .nav-pill[href="#dashboard"]{background:transparent;color:#dbe9ff!important;box-shadow:none;}
body:has(#failed-payments:target) section[data-testid="stSidebar"] .nav-pill[href="#failed-payments"],body:has(#recovery-actions:target) section[data-testid="stSidebar"] .nav-pill[href="#recovery-actions"],body:has(#customers:target) section[data-testid="stSidebar"] .nav-pill[href="#customers"],body:has(#analytics:target) section[data-testid="stSidebar"] .nav-pill[href="#analytics"],body:has(#ai-insights:target) section[data-testid="stSidebar"] .nav-pill[href="#ai-insights"],body:has(#audit-log:target) section[data-testid="stSidebar"] .nav-pill[href="#audit-log"],body:has(#settings:target) section[data-testid="stSidebar"] .nav-pill[href="#settings"]{background:linear-gradient(100deg,#1267ff,#2d9cff);color:#fff!important;box-shadow:0 12px 26px rgba(18,103,255,.38),inset 0 1px 0 rgba(255,255,255,.24);}
body:has(#failed-payments:target) section[data-testid="stSidebar"] .nav-pill[href="#failed-payments"] .nav-icon,body:has(#recovery-actions:target) section[data-testid="stSidebar"] .nav-pill[href="#recovery-actions"] .nav-icon,body:has(#customers:target) section[data-testid="stSidebar"] .nav-pill[href="#customers"] .nav-icon,body:has(#analytics:target) section[data-testid="stSidebar"] .nav-pill[href="#analytics"] .nav-icon,body:has(#ai-insights:target) section[data-testid="stSidebar"] .nav-pill[href="#ai-insights"] .nav-icon,body:has(#audit-log:target) section[data-testid="stSidebar"] .nav-pill[href="#audit-log"] .nav-icon,body:has(#settings:target) section[data-testid="stSidebar"] .nav-pill[href="#settings"] .nav-icon{background:rgba(255,255,255,.18);color:#fff!important;}
section[data-testid="stSidebar"] .side-feature{position:relative;overflow:hidden;margin-top:18px;padding:14px 12px 12px;border-radius:17px;background:radial-gradient(circle at 75% 80%,rgba(37,164,255,.34),transparent 34%),linear-gradient(145deg,rgba(24,108,255,.32),rgba(3,22,64,.94));border:1px solid rgba(84,159,255,.35);box-shadow:0 20px 42px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.10);}
section[data-testid="stSidebar"] .side-feature h4{margin:0;font-size:13px;color:#fff!important;}
section[data-testid="stSidebar"] .side-feature p{margin:5px 0 0;font-size:10px;line-height:1.5;color:#c5dcff!important;}
section[data-testid="stSidebar"] .feature-badge{display:inline-block;margin-bottom:7px;padding:4px 7px;border-radius:999px;background:rgba(255,255,255,.10);color:#a9d7ff!important;font-size:8px;font-weight:900;letter-spacing:.6px;}
section[data-testid="stSidebar"] .side-mini{margin-top:10px;padding:9px 10px;border-radius:11px;background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.10);color:#fff!important;font-size:10px;}
section[data-testid="stSidebar"] .side-mini b{font-size:15px;}
section[data-testid="stSidebar"] .side-footer{margin-top:11px;padding:10px 8px;border-radius:11px;color:#9fb9e5!important;font-size:9px!important;border:1px solid rgba(255,255,255,.08);background:rgba(255,255,255,.035);line-height:1.45;}
.site-footer{margin:70px 0 0;padding:22px 24px;border-radius:22px;background:linear-gradient(115deg,#061a4d,#0a347f 58%,#087eb8);border:1px solid rgba(100,184,255,.32);box-shadow:0 24px 52px rgba(4,24,68,.24),inset 0 1px 0 rgba(255,255,255,.16);color:#d7eaff;text-align:center}
.site-footer-title{font-size:13px;font-weight:850;color:#fff}.site-footer-copy{margin-top:5px;font-size:10px;color:#b9d3ef}.site-footer-version{margin-top:5px;font-size:9px;color:#86b0d9}
button[data-testid="stSidebarCollapseButton"],button[aria-label*="Collapse"],button[aria-label*="Expand"]{display:none!important;}
/* Clean section headers: expansion remains clickable, only the decorative chevron is hidden. */
details summary svg, [data-testid="stExpanderToggleIcon"]{display:none!important;}
details summary{padding-left:0!important;}
@media(max-width:900px){section[data-testid="stSidebar"]{min-width:220px!important;max-width:220px!important;width:220px!important;}.block-container{padding-left:12px;padding-right:12px;}}

/* ---------------- top chrome ---------------- */
.topbar{
  display:flex;justify-content:space-between;align-items:center;
  gap:12px;margin:0 2px 12px;
}
.top-group{display:flex;align-items:center;gap:9px}
.top-pill{
  display:inline-flex;align-items:center;gap:7px;
  min-height:34px;padding:7px 12px;border-radius:12px;
  background:rgba(255,255,255,.84);
  border:1px solid rgba(205,222,243,.9);
  box-shadow:0 9px 25px rgba(31,87,156,.09),inset 0 1px 0 #fff;
  color:#12366f;font-size:10px;font-weight:750;
  backdrop-filter:blur(14px);
}
.live-dot{
  width:8px;height:8px;border-radius:50%;
  background:#ffad1d;box-shadow:0 0 0 4px rgba(255,173,29,.12);
}
.calendar-mark{font-size:8px;font-weight:900;letter-spacing:.5px;color:#1769ff!important}.avatar{
  width:30px;height:26px;border-radius:50%;display:grid;place-items:center;
  background:linear-gradient(145deg,#7d47ff,#4b22db);color:white!important;font-size:9px;font-weight:800;
}

/* ---------------- hero ---------------- */
.hero{
  position:relative;overflow:hidden;
  min-height:252px;margin-bottom:14px;padding:22px 25px;
  border-radius:27px;
  background:
    radial-gradient(circle at 72% 30%,rgba(35,139,255,.18),transparent 25%),
    linear-gradient(112deg,rgba(255,255,255,.98),rgba(239,247,255,.97) 57%,rgba(225,239,255,.97));
  border:1px solid #d2e4fa;
  box-shadow:0 24px 58px rgba(24,82,150,.14),inset 0 1px 0 #fff;
}
.hero:before{
  content:"";position:absolute;right:-120px;top:-170px;width:560px;height:420px;
  border:72px solid rgba(30,119,255,.065);border-radius:50%;
}
.hero-left{position:relative;z-index:4;width:55%}
.kicker{
  display:inline-flex;align-items:center;gap:7px;
  padding:7px 11px;border-radius:999px;
  background:#eaf3ff;border:1px solid #d6e7fc;color:#165ac9;
  font-size:9px;font-weight:850;letter-spacing:.2px;
}
.hero h1{
  margin:13px 0 5px;
  font-family:Manrope,Inter,sans-serif;
  font-size:53px;line-height:.96;letter-spacing:-3.25px;color:#071944;
}
.hero h1 .grad{
  background:linear-gradient(90deg,#124bc8,#1769ff 55%,#34a9ff);
  -webkit-background-clip:text;background-clip:text;color:transparent;
}
.hero-desc{font-size:14px;line-height:1.48;color:#35547f}
.hero-desc strong{color:#092c69}
.hero-chips{display:flex;gap:9px;margin-top:16px;flex-wrap:wrap}
.hero-chip{
  display:flex;align-items:center;gap:7px;padding:8px 12px;border-radius:12px;
  background:rgba(255,255,255,.83);border:1px solid #d9e8f9;
  color:#123b77;font-size:10px;font-weight:800;
  box-shadow:0 8px 20px rgba(29,86,155,.08),inset 0 1px 0 #fff;
}
.hero-chip .chip-icon{
  width:23px;height:23px;border-radius:8px;display:grid;place-items:center;
  background:#e8f3ff;color:#1769ff;
}
.hero-chip:nth-child(2) .chip-icon{background:#e8f0ff;color:#345de6}
.hero-chip:nth-child(3) .chip-icon{background:#e7fbf4;color:#0ba876}
.hero-chip:nth-child(4) .chip-icon{background:#e8fafb;color:#09a6b8}

/* hero 3D illustration */
.hero-art{
  position:absolute;right:4px;top:7px;width:48%;height:240px;z-index:2;
}
.script{
  position:absolute;left:5px;top:17px;color:#0b55d1;
  font-family:"Comic Sans MS",cursive;font-style:italic;font-weight:700;
  font-size:25px;line-height:1.04;transform:rotate(-7deg);
}
.script:after{
  content:"";position:absolute;left:0;bottom:-16px;width:135px;height:12px;
  border-top:3px solid #0b6dff;border-radius:50%;transform:rotate(-4deg);
}
.card3d{
  position:absolute;right:73px;top:49px;width:198px;height:137px;
  border-radius:19px;
  background:linear-gradient(145deg,#0a3d9c,#176fff 56%,#1ac5e8);
  transform:rotate(-6deg);
  box-shadow:0 29px 48px rgba(8,72,175,.33),inset 0 1px 0 rgba(255,255,255,.48);
}
.card3d:before{
  content:"";position:absolute;inset:10px;border-radius:14px;
  border:1px solid rgba(255,255,255,.24);
}
.card-brand{position:absolute;left:17px;top:13px;color:white;font-weight:850;font-size:12px}
.card-copy{position:absolute;left:17px;bottom:13px;color:white;font-weight:800;font-size:11px;line-height:1.45}
.hero-quote{
  position:absolute;right:-2px;top:18px;width:120px;height:151px;padding:15px;
  border-radius:18px;background:linear-gradient(145deg,#e9f3ff,#cfe5ff);
  border:1px solid #c8def7;box-shadow:0 16px 33px rgba(29,83,153,.11);
  color:#0b3c83;font-size:10px;line-height:1.45;
}
.hero-quote b{display:block;font-size:24px;line-height:.7;margin-bottom:8px}

/* ---------------- KPI ---------------- */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin-bottom:14px}
.kpi{
  position:relative;overflow:hidden;min-height:112px;padding:14px 16px;
  border-radius:18px;background:linear-gradient(145deg,#fff,#f7fbff);
  border:1px solid #d9e7f7;
  box-shadow:0 17px 37px rgba(31,89,158,.10),inset 0 1px 0 #fff;
}
.kpi:hover{transform:translateY(-2px);box-shadow:0 22px 45px rgba(31,89,158,.14),inset 0 1px 0 #fff}
.kpi:after{
  content:"";position:absolute;right:-45px;bottom:-82px;width:175px;height:175px;border-radius:50%;
  background:var(--glow);opacity:.10;
}
.kpi-top{display:flex;align-items:center;justify-content:space-between;position:relative;z-index:1}
.kpi-icon{
  width:42px;height:42px;border-radius:13px;display:grid;place-items:center;
  font-size:19px;background:var(--iconbg);color:var(--icon);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.8);
}
.kpi-label{font-size:10px;font-weight:800;color:#60728e;margin-top:9px}
.kpi-value{
  font-family:Manrope,Inter,sans-serif;font-size:27px;font-weight:800;
  letter-spacing:-1.1px;color:#071944;margin-top:1px;
}
.kpi-sub{font-size:9px;color:#6d7f99;margin-top:3px}
.badge{
  display:inline-block;padding:4px 8px;border-radius:999px;
  background:#e8f2ff;color:#1763dc;font-size:9px;font-weight:850;
}
.badge.green{background:#e4faef;color:#099d69}
.badge.orange{background:#fff0dd;color:#dc7410}

/* ---------------- content panels ---------------- */
.panel{
  transition:transform .18s ease,box-shadow .18s ease;
  background:rgba(255,255,255,.92);
  border:1px solid #d9e7f7;border-radius:18px;
  box-shadow:0 15px 38px rgba(31,89,158,.09),inset 0 1px 0 #fff;
  padding:15px;margin-bottom:13px;
}
.panel:hover{transform:translateY(-1px);box-shadow:0 20px 44px rgba(31,89,158,.12),inset 0 1px 0 #fff}
.panel-head{display:flex;justify-content:space-between;gap:12px;align-items:flex-start}
.panel-title{font-size:14px;font-weight:850;color:#08275d}
.panel-sub{font-size:9px;color:#74859e;margin-top:3px}
.panel-link{font-size:9px;color:#1769ff;font-weight:800}.panel-link-btn{display:inline-flex;align-items:center;padding:5px 8px;border-radius:8px;background:#eef5ff;transition:background .15s ease,transform .15s ease}.panel-link-btn:hover{background:#dcecff;transform:translateY(-1px)}
.command-title{
  font-family:Manrope,Inter,sans-serif;font-size:19px;font-weight:850;
  margin:17px 0 4px;color:#061a4b;
}
.command-sub{font-size:10px;color:#71829c;margin-bottom:9px}

/* ---------------- chart ---------------- */
.chart{
  position:relative;height:212px;margin-top:8px;
  border-radius:13px;overflow:hidden;
  background:
    repeating-linear-gradient(to bottom,transparent 0,transparent 39px,#e9f0f8 40px),
    linear-gradient(180deg,#fbfdff,#f8fbff);
  border:1px solid #edf3fa;
}
.chart-y{position:absolute;left:8px;top:10px;bottom:34px;display:flex;flex-direction:column;justify-content:space-between;color:#7890ad;font-size:8px}
.chart-area{position:absolute;left:42px;right:10px;top:12px;bottom:34px}
.chart-grid{
  position:absolute;inset:0;
  background:repeating-linear-gradient(to right,transparent 0,transparent calc(14.285% - 1px),rgba(219,231,245,.75) calc(14.285% - 1px),rgba(219,231,245,.75) 14.285%);
}
.bar-wrap{position:absolute;inset:0;display:flex;align-items:flex-end;justify-content:space-around;padding:0 5px}
.bar-item{height:100%;flex:1;display:flex;align-items:flex-end;justify-content:center}
.bar-item .bar{
  width:54%;max-width:44px;min-height:0;border-radius:7px 7px 2px 2px;
  background:linear-gradient(180deg,#4aaeff,#1769ff);
  box-shadow:0 8px 17px rgba(23,105,255,.22);
}
.line-svg{position:absolute;inset:0;width:100%;height:100%;overflow:visible}
.chart-x{position:absolute;left:42px;right:10px;bottom:8px;display:flex;justify-content:space-around;color:#6f829e;font-size:8px}
.chart-legend{display:flex;justify-content:flex-end;gap:18px;margin:7px 4px 0;font-size:9px;color:#61748f}
.legend-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:5px}
.legend-square{width:8px;height:8px;border-radius:2px;display:inline-block;margin-right:5px}

/* ---------------- donut ---------------- */
.donut-layout{display:flex;align-items:center;gap:10px;min-height:205px}
.donut{
  width:140px;height:140px;flex:0 0 140px;border-radius:50%;display:grid;place-items:center;
  position:relative;background:conic-gradient(var(--segments));
  box-shadow:0 17px 32px rgba(27,84,150,.14);
}
.donut-svg{position:absolute;inset:0;width:100%;height:100%;transform:rotate(-90deg);overflow:visible}
.donut-segment{cursor:pointer;transition:filter .15s ease,stroke-width .15s ease}
.donut-segment:hover{filter:brightness(1.08);stroke-width:35}
.donut:after{
  content:"";position:absolute;width:88px;height:88px;border-radius:50%;background:white;
  box-shadow:inset 0 0 0 1px #edf3fa;
}
.donut-center{position:relative;z-index:2;text-align:center}
.donut-number{font-family:Manrope,Inter,sans-serif;font-size:25px;font-weight:850;color:#071944}
.donut-label{font-size:9px;color:#71839c}
.method-list{flex:1;min-width:0;overflow:visible}
.method-row{display:flex;align-items:center;gap:5px;margin:8px 0;font-size:10px;min-width:0;width:100%;box-sizing:border-box}
.method-name{flex:0 0 80px;min-width:80px;white-space:nowrap;color:#163d78;font-weight:750}
.method-count{font-weight:850;color:#071a4b}
.method-pct{flex:0 0 36px;width:36px;text-align:right;color:#71829b;font-size:8px}

/* ---------------- insights ---------------- */
.insight{
  display:flex;align-items:flex-start;gap:10px;padding:9px 10px;margin:7px 0;
  border-radius:12px;border:1px solid rgba(34,104,184,.10);
  box-shadow:inset 0 1px 0 rgba(255,255,255,.7);
}
.insight.green{background:linear-gradient(100deg,#e9faf3,#f8fffc)}
.insight.purple{background:linear-gradient(100deg,#f1ebff,#fbf9ff)}
.insight.blue{background:linear-gradient(100deg,#eaf4ff,#f9fcff)}
.insight.orange{background:linear-gradient(100deg,#fff3e2,#fffbf6)}
.insight-icon{width:28px;font-size:21px;line-height:1}
.insight-title{font-size:10px;font-weight:850;color:#08275d}
.insight-copy{font-size:8px;color:#6d7e97;margin-top:2px;line-height:1.42}

/* ---------------- V4 visual polish ---------------- */
.kicker-dot{display:grid;place-items:center;width:17px;height:17px;border-radius:6px;background:#fff;color:#1769ff;box-shadow:0 4px 10px rgba(23,105,255,.12)}
.hero:after{content:"";position:absolute;inset:0;pointer-events:none;background:linear-gradient(120deg,transparent 0%,rgba(255,255,255,.45) 42%,transparent 67%);transform:translateX(-110%);animation:heroSweep 7s ease-in-out infinite}
@keyframes heroSweep{0%,55%{transform:translateX(-110%)}75%,100%{transform:translateX(110%)}}
.hero-left{width:49%}
.hero h1{font-size:58px;line-height:.93;margin-top:14px}
.hero-desc{font-size:15px;max-width:610px}
.hero-chips{gap:10px}
.hero-chip{min-width:106px;padding:9px 11px;gap:8px}
.hero-chip span:last-child{display:flex;flex-direction:column}
.hero-chip b{font-size:10px}
.hero-chip small{font-size:7px;color:#7a8da8;margin-top:2px;font-weight:600}
.hero-proof{display:flex;gap:13px;flex-wrap:wrap;margin-top:14px;font-size:8px;font-weight:800;color:#55749e}
.hero-proof span{padding:5px 8px;border-radius:999px;background:rgba(255,255,255,.58);border:1px solid rgba(203,222,244,.8)}
.hero-art{width:53%;height:252px;top:0;right:0}
.hero-glow{position:absolute;border-radius:50%;filter:blur(3px);pointer-events:none}
.glow-one{width:190px;height:190px;right:110px;top:26px;background:radial-gradient(circle,rgba(39,143,255,.25),transparent 68%)}
.glow-two{width:150px;height:150px;right:5px;bottom:-10px;background:radial-gradient(circle,rgba(21,199,232,.22),transparent 68%)}
.script{left:2px;top:17px;font-size:23px;z-index:5;text-shadow:0 2px 0 #fff}
.script b{font-weight:800}
.hero-bars{position:absolute;right:4px;bottom:30px;height:100px;width:112px;display:flex;align-items:flex-end;justify-content:space-between;gap:8px;z-index:2}
.hero-bars i{display:block;width:16px;border-radius:7px 7px 2px 2px;background:linear-gradient(180deg,#35c9d8,#2388ff);box-shadow:0 12px 18px rgba(35,136,255,.22);transform:skewY(-8deg)}
.hero-bars i:nth-child(1){height:32px}.hero-bars i:nth-child(2){height:47px}.hero-bars i:nth-child(3){height:62px}.hero-bars i:nth-child(4){height:78px}.hero-bars i:nth-child(5){height:96px}
.card3d{right:73px;top:51px;width:205px;height:143px;z-index:4;transform:rotate(-7deg) perspective(600px) rotateY(-5deg);background:linear-gradient(145deg,#062f86 0%,#0e58c9 48%,#13bfe0 100%);border-radius:20px;box-shadow:0 31px 55px rgba(8,65,164,.36),0 7px 0 rgba(5,36,104,.35),inset 0 1px 0 rgba(255,255,255,.45)}
.card-shine{position:absolute;inset:-20%;background:linear-gradient(115deg,transparent 35%,rgba(255,255,255,.25) 47%,transparent 59%);transform:rotate(10deg);animation:cardShine 5s ease-in-out infinite}
@keyframes cardShine{0%,50%{transform:translateX(-45%) rotate(10deg)}75%,100%{transform:translateX(45%) rotate(10deg)}}
.card-brand{left:18px;top:15px;font-size:13px;z-index:2}.tiny-mark{display:inline-block;width:25px;height:25px;border-radius:6px;background:#fff;padding:3px;object-fit:contain;margin-right:5px;vertical-align:middle}
.card-copy{left:18px;bottom:18px;font-size:11px;z-index:2;letter-spacing:.2px}.card-copy b{font-size:15px}.card-chip{position:absolute;right:17px;top:51px;width:29px;height:23px;border-radius:7px;background:linear-gradient(145deg,#e7f5ff,#8dc8ff);color:#1769ff;display:grid;place-items:center;z-index:2;box-shadow:0 4px 8px rgba(0,0,0,.15)}
.hero-quote{right:0;top:20px;width:116px;height:157px;z-index:6;padding:14px;background:linear-gradient(145deg,rgba(239,248,255,.96),rgba(204,228,255,.96));box-shadow:0 20px 38px rgba(26,87,158,.16)}
.hero-quote b{font-size:28px;color:#1769ff}.hero-quote span{font-size:10px;font-weight:700}.hero-quote i{display:block;width:44px;border-top:3px solid #1769ff;margin-top:10px;border-radius:4px}
.floating-tile{position:absolute;z-index:7;display:flex;align-items:center;gap:6px;padding:7px 9px;border-radius:10px;background:rgba(255,255,255,.9);border:1px solid #d6e6f9;box-shadow:0 13px 25px rgba(26,87,158,.12);color:#0a2c68;backdrop-filter:blur(10px)}
.floating-tile span{width:20px;height:20px;border-radius:6px;background:#e8f5ff;color:#1769ff;display:grid;place-items:center;font-weight:900}.floating-tile b{font-size:9px}.floating-tile small{font-size:7px;color:#7b8ca5}.tile-one{right:178px;bottom:17px}.tile-two{right:28px;bottom:18px}
.feature-badge{display:inline-block;padding:4px 7px;border-radius:999px;background:rgba(49,154,255,.18);border:1px solid rgba(91,175,255,.3);color:#8bc8ff;font-size:7px;font-weight:900;letter-spacing:.6px;margin-bottom:6px}
.side-feature h4{font-size:15px}.side-feature{padding:14px 12px 12px}
.side-3d{height:150px;margin-top:11px;background:radial-gradient(circle at 65% 35%,rgba(36,170,255,.26),transparent 26%),linear-gradient(145deg,#0b3e9c,#031744);box-shadow:inset 0 1px 0 rgba(255,255,255,.12),0 14px 30px rgba(0,0,0,.2)}
.side-orb{position:absolute;border-radius:50%;filter:blur(1px)}.orb-a{width:28px;height:28px;right:17px;top:18px;background:#28c7ff;box-shadow:0 0 35px #28c7ff}.orb-b{width:18px;height:18px;right:52px;top:46px;background:#6b61ff;box-shadow:0 0 25px #6b61ff}
.side-bar{position:absolute;bottom:24px;width:26px;border-radius:6px 6px 2px 2px;background:linear-gradient(180deg,#58c9ff,#1d6eff);box-shadow:0 12px 15px rgba(0,0,0,.24);transform:skewY(-8deg)}.bar-a{left:22px;height:48px}.bar-b{left:54px;height:74px}.bar-c{left:86px;height:59px}
.side-card-mini{position:absolute;right:10px;bottom:20px;width:74px;padding:7px;border-radius:8px;background:linear-gradient(145deg,#0d57c6,#176eff);border:1px solid rgba(255,255,255,.18);box-shadow:0 15px 25px rgba(0,0,0,.28);color:#fff;font-size:9px}.side-card-mini b{font-size:12px}.side-card-mini small{display:block;font-size:7px;color:#b9dcff;margin-top:2px}
.kpi{min-height:120px;border-radius:20px;box-shadow:0 19px 42px rgba(31,89,158,.11),inset 0 1px 0 #fff;transition:all .22s ease}.kpi:before{content:"";position:absolute;inset:0;border-radius:20px;background:linear-gradient(120deg,rgba(255,255,255,.6),transparent 45%);pointer-events:none}.kpi:hover{transform:translateY(-4px) scale(1.005);box-shadow:0 25px 52px rgba(31,89,158,.16),inset 0 1px 0 #fff}
.kpi-value{font-size:29px}.kpi-icon{width:45px;height:45px;border-radius:14px;font-size:20px;box-shadow:0 9px 18px color-mix(in srgb,var(--icon) 18%,transparent),inset 0 1px 0 rgba(255,255,255,.85)}
.panel{border-radius:20px;padding:16px;background:linear-gradient(145deg,rgba(255,255,255,.97),rgba(248,252,255,.94));box-shadow:0 18px 43px rgba(31,89,158,.10),inset 0 1px 0 #fff}.panel-title{font-size:15px}.panel-sub{font-size:9px}
.chart{height:220px;border-radius:15px;box-shadow:inset 0 1px 0 #fff}.bar-item .bar{background:linear-gradient(180deg,#51b4ff,#238cff 70%,#1769ff);border-radius:8px 8px 2px 2px}
.donut{width:140px;height:140px;flex-basis:140px;background:conic-gradient(var(--segments));box-shadow:0 18px 36px rgba(27,84,150,.16)}
.donut:after{width:88px;height:88px}.method-row{padding:5px 0;border-radius:9px;transition:.18s}.method-row:hover{background:#f0f6ff;transform:translateX(2px)}
.insight{padding:10px 11px;margin:8px 0;border-radius:13px;box-shadow:0 7px 17px rgba(31,89,158,.06),inset 0 1px 0 rgba(255,255,255,.8)}
.insight:hover{transform:translateX(2px)}
.bottom-rail{left:calc(230px + 14px);right:14px;bottom:12px;padding:11px 15px;border-radius:19px;background:linear-gradient(110deg,#041747 0%,#073b9e 56%,#1168ea 100%);box-shadow:0 25px 58px rgba(4,24,68,.38),inset 0 1px 0 rgba(255,255,255,.16)}
.bottom-rail:before{content:"";position:absolute;right:140px;top:-1px;width:280px;height:100%;background:linear-gradient(135deg,transparent,rgba(64,180,255,.18),transparent);transform:skewX(-25deg);pointer-events:none}
.run-cta{padding:12px 19px;border-radius:13px;background:linear-gradient(135deg,#31a8ff,#1769ff);box-shadow:0 13px 27px rgba(0,0,0,.24),inset 0 1px 0 rgba(255,255,255,.3);font-size:10px}

/* ---------------- native controls ---------------- */
.stButton>button,.stDownloadButton>button{
  border-radius:11px!important;
  border:1px solid #cfe0f5!important;
  background:linear-gradient(180deg,#fff,#f1f7ff)!important;
  color:#0a2c68!important;
  font-weight:750!important;
  box-shadow:0 8px 18px rgba(31,89,158,.08)!important;
}
.stButton>button:hover,.stDownloadButton>button:hover{
  border-color:#8dbbff!important;transform:translateY(-1px);
}
.stButton>button[kind="primary"]{
  border:0!important;color:white!important;
  background:linear-gradient(135deg,#1769ff,#2b9eff)!important;
  box-shadow:0 13px 28px rgba(23,105,255,.28)!important;
}
.stSelectbox>div>div,.stTextInput>div>div,.stMultiSelect>div>div{
  border-radius:11px!important;border-color:#cfe0f5!important;background:white!important;
}
[data-testid="stExpander"]{
  border:1px solid #d9e7f7!important;border-radius:15px!important;
  background:rgba(255,255,255,.82)!important;
  box-shadow:0 10px 25px rgba(31,89,158,.06)!important;
}
[data-testid="stDataFrame"]{
  border:1px solid #d9e7f7!important;border-radius:13px!important;
  overflow:hidden;box-shadow:0 8px 22px rgba(31,89,158,.06);
}
hr{border-color:#dbe8f6!important}


.recent-table{width:100%;border-collapse:separate;border-spacing:0;overflow:hidden;border:1px solid #e0ebf8;border-radius:13px;font-size:9px;margin-top:10px;background:#fff}.recent-table th{padding:8px 9px;text-align:left;color:#6b7d97;background:#f4f8fd;font-size:8px;font-weight:850;border-bottom:1px solid #e2edf8}.recent-table td{padding:9px;border-bottom:1px solid #edf2f8;color:#163866;font-weight:650}.recent-table tr:last-child td{border-bottom:0}.recent-table tr:hover td{background:#f7fbff}.method-tag{display:inline-block;padding:4px 7px;border-radius:999px;font-size:7px;font-weight:900}.method-tag.whatsapp{background:#e5faef;color:#099d69}.method-tag.auto{background:#e8f2ff;color:#1769ff}.method-tag.voice{background:#fff0df;color:#db7610}.status-tag{display:inline-block;padding:4px 7px;border-radius:999px;background:#e6faee;color:#07955f;font-size:7px;font-weight:900}.status-tag.failed{background:#fff0f0;color:#d33}.status-tag.pending{background:#eef4ff;color:#3567bd}
/* ---------------- bottom command rail ---------------- */
.bottom-rail{
  position:fixed;left:calc(248px + 12px);right:14px;bottom:10px;z-index:999;
  display:flex;align-items:center;gap:20px;padding:10px 14px;
  border-radius:17px;
  background:
    linear-gradient(115deg,#061a4d 0%,#0a2f7d 54%,#0f55c8 100%);
  border:1px solid rgba(255,255,255,.14);
  color:white;
  box-shadow:0 24px 55px rgba(4,24,68,.34),inset 0 1px 0 rgba(255,255,255,.10);
}
.bottom-brand{display:flex;align-items:center;gap:12px;min-width:280px}
.bottom-mark{
  font-family:Manrope,Inter,sans-serif;font-size:22px;font-weight:850;
  color:#44b7ff;font-style:italic;
}
.bottom-brand-title{font-size:13px;font-weight:850}
.bottom-brand-copy{font-size:8px;color:#b9d3ff;margin-top:2px}
.bottom-actions{display:flex;flex:1;justify-content:center;gap:25px}
.bottom-action{display:flex;align-items:center;gap:8px;font-size:9px;color:#edf5ff}
.bottom-action .ba-icon{
  width:27px;height:27px;border-radius:50%;display:grid;place-items:center;
  background:rgba(255,255,255,.12);border:1px solid rgba(255,255,255,.12);
}
.run-cta{
  padding:11px 17px;border-radius:12px;
  background:linear-gradient(135deg,#2e9cff,#1769ff);
  font-size:10px;font-weight:850;
  box-shadow:0 11px 25px rgba(0,0,0,.22),inset 0 1px 0 rgba(255,255,255,.25);
  white-space:nowrap;
}
@media(max-width:1100px){.hero-left{width:70%}.hero-art{opacity:.45}.bottom-rail{left:12px}.bottom-actions{display:none}}
@media(max-width:760px){
  .hero-art{display:none}.hero-left{width:100%}.hero h1{font-size:38px}
  .kpi-grid{grid-template-columns:1fr 1fr}.top-group.right{display:none}
  .bottom-brand{min-width:auto}
}

/* ---------------- 3D command-center finish ---------------- */
.main .block-container{perspective:1400px}
.hero,.panel,.kpi,section[data-testid="stSidebar"] .side-feature{
  transform-style:preserve-3d;
  backface-visibility:hidden;
}
.hero{
  box-shadow:0 30px 70px rgba(25,78,145,.16),0 7px 0 rgba(20,78,157,.08),inset 0 1px 0 #fff;
}
.hero-art{perspective:900px;transform:translateZ(12px)}
.card3d{transform:rotate(-7deg) perspective(600px) rotateY(-7deg) translateZ(18px)}
.hero-quote,.floating-tile{transform:translateZ(22px)}
.panel{box-shadow:0 20px 48px rgba(31,89,158,.12),0 4px 0 rgba(30,100,190,.05),inset 0 1px 0 #fff}
.panel:hover{transform:translateY(-3px) rotateX(.35deg);box-shadow:0 28px 58px rgba(31,89,158,.16),0 5px 0 rgba(30,100,190,.07),inset 0 1px 0 #fff}
.kpi{box-shadow:0 22px 46px rgba(31,89,158,.13),0 5px 0 rgba(30,100,190,.06),inset 0 1px 0 #fff}
section[data-testid="stSidebar"] .side-feature{box-shadow:0 24px 46px rgba(0,0,0,.28),0 5px 0 rgba(24,106,219,.28),inset 0 1px 0 rgba(255,255,255,.13)}
.donut{filter:drop-shadow(0 18px 16px rgba(23,91,173,.16));transform:translateZ(8px)}
.donut-segment:hover{filter:brightness(1.08) drop-shadow(0 8px 8px rgba(21,92,180,.2))}

/* ---------------- scroll-driven depth ---------------- */
html{scroll-behavior:smooth}
.stApp{isolation:isolate;overflow:visible}
.stApp:before,.stApp:after{
  content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
}
.stApp:before{
  background:
    linear-gradient(115deg,transparent 0 28%,rgba(38,133,255,.055) 28.2%,transparent 28.6% 67%,rgba(24,201,232,.045) 67.3%,transparent 67.7%),
    repeating-linear-gradient(90deg,transparent 0,transparent 88px,rgba(111,157,213,.035) 89px,transparent 90px);
  transform:translateY(0) scale(1.08);
  animation:backgroundDrift linear both;
  animation-timeline:scroll(root);
  animation-range:0 100%;
}
.stApp:after{
  background:linear-gradient(180deg,rgba(255,255,255,.12),transparent 22%,rgba(27,103,190,.04) 78%,transparent);
  opacity:.55;
  animation:lightDrift linear both;
  animation-timeline:scroll(root);
  animation-range:0 100%;
}
.main .block-container>*{animation:sectionReveal .85s ease both;animation-timeline:view();animation-range:entry 0% cover 22%}
.hero-art{animation:heroParallax linear both;animation-timeline:scroll(root);animation-range:0 100%}
.side-feature{animation:none}
@keyframes backgroundDrift{to{transform:translateY(-9%) scale(1.14)}}
@keyframes lightDrift{to{transform:translateY(7%)}}
@keyframes sectionReveal{from{opacity:.35;transform:translateY(22px) scale(.985)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes heroParallax{to{transform:translate3d(0,-42px,12px)}}
@keyframes sideFloat{to{transform:translate3d(0,24px,0) rotateX(1deg)}}
@supports not (animation-timeline:scroll()){
  .main .block-container>*{animation:none}
  .hero-art,.side-feature{animation:none}
}

/* ---------------- premium product finish ---------------- */
.block-container{max-width:1380px;padding:10px 28px 96px}
.topbar{margin:0 4px 18px}
.top-pill{min-height:38px;padding:8px 14px;border-radius:14px;background:rgba(255,255,255,.72);border-color:rgba(190,211,238,.78);box-shadow:0 8px 24px rgba(36,83,143,.07),inset 0 1px 0 #fff}
.hero{min-height:340px;margin-bottom:20px;padding:34px 36px;border-radius:34px;background:linear-gradient(135deg,rgba(255,255,255,.98),rgba(239,247,255,.94) 62%,rgba(224,239,255,.9));border-color:rgba(190,215,244,.82);box-shadow:0 32px 80px rgba(24,82,150,.13),0 6px 0 rgba(20,78,157,.06),inset 0 1px 0 #fff}
.hero h1{font-size:68px;line-height:.94;margin:22px 0 10px}
.hero-desc{max-width:560px;font-size:16px;line-height:1.55;color:#496789}
.hero-chips{margin-top:22px;gap:11px}
.hero-chip{padding:10px 13px;border-radius:14px;background:rgba(255,255,255,.72);border-color:rgba(203,222,244,.9);box-shadow:0 10px 24px rgba(29,86,155,.07)}
.kpi-grid{gap:16px;margin-bottom:20px}
.kpi{min-height:132px;padding:18px 19px;border-radius:24px;background:rgba(255,255,255,.86);border-color:rgba(210,226,244,.94)}
.kpi-value{font-size:31px}
.command-title{font-size:24px;margin:28px 0 6px;letter-spacing:0}
.command-sub{font-size:11px;margin-bottom:12px;color:#7186a2}
.panel{padding:20px;border-radius:24px;background:rgba(255,255,255,.82);border-color:rgba(210,226,244,.94);box-shadow:0 22px 56px rgba(31,89,158,.10),0 4px 0 rgba(30,100,190,.045),inset 0 1px 0 #fff}
.panel-title{font-size:16px}
.chart{border-radius:18px;background:linear-gradient(180deg,rgba(251,253,255,.8),rgba(247,250,255,.95));border-color:#e2edf8}
.donut-layout{gap:14px}
section[data-testid="stSidebar"]>div{padding:22px 16px 26px!important}
section[data-testid="stSidebar"] .sidebar-brand{padding:9px 10px 21px;margin-bottom:17px}
section[data-testid="stSidebar"] .nav-pill{padding:11px 12px;margin:6px 0;border-radius:14px}
section[data-testid="stSidebar"] .side-feature{margin-top:22px;border-radius:22px}
@media(max-width:760px){
  .block-container{padding:18px 14px 80px}
  .hero{min-height:300px;padding:24px 22px;border-radius:26px}
  .hero h1{font-size:42px}
  .hero-desc{font-size:14px}
  .panel{padding:16px;border-radius:20px}
}

/* ---------------- signature visual direction ---------------- */
.hero{
  background:
    radial-gradient(circle at 82% 28%,rgba(66,187,255,.28),transparent 25%),
    radial-gradient(circle at 58% 100%,rgba(31,103,255,.28),transparent 30%),
    linear-gradient(120deg,#041541 0%,#082d76 48%,#087eb8 100%);
  border-color:rgba(99,181,255,.42);
  box-shadow:0 34px 90px rgba(4,28,86,.30),0 7px 0 rgba(16,76,169,.16),inset 0 1px 0 rgba(255,255,255,.24);
}
.hero:before{border-color:rgba(111,208,255,.14)}
.hero h1,.hero h1 .grad{color:#fff;background:none;-webkit-text-fill-color:#fff}
.hero-desc,.hero-desc strong{color:#d5e8ff}
.kicker{background:rgba(255,255,255,.10);border-color:rgba(156,213,255,.28);color:#c9e8ff}
.kicker-dot{background:rgba(255,255,255,.16);color:#7fd5ff;box-shadow:0 4px 16px rgba(64,188,255,.20)}
.hero-chip{background:rgba(255,255,255,.10);border-color:rgba(157,215,255,.25);color:#fff;box-shadow:0 13px 28px rgba(0,16,57,.18),inset 0 1px 0 rgba(255,255,255,.16)}
.hero-chip small{color:#b7d6f5}
.hero-chip .chip-icon{background:rgba(255,255,255,.14);color:#8cddff}
.hero-proof{color:#c6def8}
.hero-proof span{background:rgba(255,255,255,.08);border-color:rgba(159,215,255,.22)}
.hero-quote{background:rgba(239,248,255,.92);border-color:rgba(255,255,255,.58)}
.kpi-grid .kpi:nth-child(1){border-top:3px solid #2f9dff}
.kpi-grid .kpi:nth-child(2){border-top:3px solid #16c995}
.kpi-grid .kpi:nth-child(3){border-top:3px solid #8664ff}
.kpi-grid .kpi:nth-child(4){border-top:3px solid #ffad38}
.panel{background:linear-gradient(145deg,rgba(255,255,255,.96),rgba(242,248,255,.86));box-shadow:0 26px 64px rgba(31,89,158,.14),0 5px 0 rgba(30,100,190,.06),inset 0 1px 0 #fff}
.panel-head{padding-bottom:5px}
.panel-title{color:#071f55;font-size:17px}
.command-title{font-size:28px;color:#061a4b}
.top-pill{background:rgba(255,255,255,.88);box-shadow:0 12px 30px rgba(20,71,132,.11),inset 0 1px 0 #fff}
@media(max-width:760px){
  .hero h1{font-size:43px}
  .hero-art{opacity:1}
}
.script{color:#fff;opacity:1;text-shadow:0 3px 0 #0b55d1,0 8px 22px rgba(0,19,72,.42)}
.script:after{border-top-color:#43c9ff;box-shadow:0 2px 10px rgba(67,201,255,.35)}
.stApp{background:
  radial-gradient(circle at 8% 18%,rgba(42,151,255,.16),transparent 24%),
  radial-gradient(circle at 92% 46%,rgba(23,201,190,.12),transparent 22%),
  linear-gradient(135deg,#f7fbff 0%,#edf5ff 48%,#f8fcff 100%)}
.kpi{background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(239,247,255,.9))}
.kpi-grid .kpi:nth-child(2){background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(231,252,244,.9))}
.kpi-grid .kpi:nth-child(3){background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(243,238,255,.9))}
.kpi-grid .kpi:nth-child(4){background:linear-gradient(145deg,rgba(255,255,255,.98),rgba(255,246,229,.92))}
.panel{background:linear-gradient(145deg,rgba(255,255,255,.97),rgba(235,245,255,.9) 72%,rgba(228,248,255,.84));border-color:rgba(184,214,244,.92)}
.chart{background:linear-gradient(180deg,rgba(246,251,255,.88),rgba(232,245,255,.96));border-color:#d2e5f8}
.recent-table{background:rgba(255,255,255,.72);border-color:#cfe2f7}
.recent-table th{background:linear-gradient(100deg,#e9f3ff,#eefcff);color:#42668f}
[data-testid="stExpander"]{background:linear-gradient(145deg,rgba(255,255,255,.94),rgba(236,247,255,.9))!important;border-color:#c8def4!important}
.command-title{background:linear-gradient(90deg,#061a4b,#1769ff 45%,#0aa9a0);-webkit-background-clip:text;background-clip:text;color:transparent}
.settings-panel{display:flex;align-items:center;justify-content:space-between;gap:20px;margin:12px 0 10px;padding:18px 20px;border:1px solid #c8def4;border-radius:18px;background:linear-gradient(110deg,rgba(231,243,255,.92),rgba(237,252,250,.78));box-shadow:0 14px 30px rgba(31,89,158,.08),inset 0 1px 0 #fff}
.settings-status{display:flex;align-items:center;gap:10px;color:#164d88;font-size:12px;font-weight:750}
.settings-status-dot{width:10px;height:10px;border-radius:50%;background:#ffae24;box-shadow:0 0 0 5px rgba(255,174,36,.14)}
@media(max-width:760px){.settings-panel{align-items:flex-start;flex-direction:column;gap:10px}}
.hero{background-size:170% 170%;background-position:0% 50%;animation:heroAurora 14s ease-in-out infinite}
.hero .card3d{animation:cardFloat 6s ease-in-out infinite}
.hero .hero-quote{animation:quoteFloat 7s ease-in-out infinite}
.kpi-grid .kpi{animation:cardLiftIn .7s cubic-bezier(.2,.8,.2,1) both}
.kpi-grid .kpi:nth-child(2){animation-delay:.08s}
.kpi-grid .kpi:nth-child(3){animation-delay:.16s}
.kpi-grid .kpi:nth-child(4){animation-delay:.24s}
section[data-testid="stSidebar"] .side-feature{overflow:hidden}
section[data-testid="stSidebar"] .side-feature:after{
  content:"";position:absolute;inset:-60% -20%;pointer-events:none;
  background:linear-gradient(115deg,transparent 38%,rgba(117,211,255,.16) 48%,transparent 58%);
  transform:translateX(-55%) rotate(8deg);animation:featureSweep 8s ease-in-out infinite;
}
@keyframes heroAurora{0%,100%{background-position:0% 50%}50%{background-position:100% 50%}}
@keyframes cardFloat{0%,100%{transform:rotate(-7deg) perspective(600px) rotateY(-7deg) translate3d(0,0,18px)}50%{transform:rotate(-5deg) perspective(600px) rotateY(-4deg) translate3d(0,-9px,25px)}}
@keyframes quoteFloat{0%,100%{transform:translate3d(0,0,22px)}50%{transform:translate3d(0,-6px,28px)}}
@keyframes cardLiftIn{from{opacity:0;transform:translateY(18px) scale(.97)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes featureSweep{0%,55%{transform:translateX(-55%) rotate(8deg)}75%,100%{transform:translateX(55%) rotate(8deg)}}
@media(prefers-reduced-motion:reduce){
  .hero,.hero .card3d,.hero .hero-quote,.kpi-grid .kpi,section[data-testid="stSidebar"] .side-feature:after{animation:none}
}

/* ---------------- full-page demo motion system ---------------- */
section[data-testid="stSidebar"] .nav-pill{position:relative;overflow:hidden}
section[data-testid="stSidebar"] .nav-pill:after{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(105deg,transparent 25%,rgba(255,255,255,.18) 48%,transparent 72%);
  transform:translateX(-125%);transition:transform .55s ease;
}
section[data-testid="stSidebar"] .nav-pill:hover:after{transform:translateX(125%)}
section[data-testid="stSidebar"] .nav-pill.active:before{
  content:"";position:absolute;left:0;top:12%;bottom:12%;width:3px;border-radius:4px;background:#8ce4ff;
  box-shadow:0 0 16px #8ce4ff;animation:activeRail 2.4s ease-in-out infinite;
}
.kpi,.panel,.recent-table,[data-testid="stExpander"]{will-change:transform}
.kpi:hover{transform:translateY(-7px) rotateX(1.2deg) rotateY(-.8deg)}
.kpi-icon{animation:iconBreathe 4s ease-in-out infinite}
.kpi:nth-child(2) .kpi-icon{animation-delay:.7s}.kpi:nth-child(3) .kpi-icon{animation-delay:1.4s}.kpi:nth-child(4) .kpi-icon{animation-delay:2.1s}
.bar-item .bar{transform-origin:bottom;animation:barRise .9s cubic-bezier(.2,.8,.2,1) both}
.bar-item:nth-child(2) .bar{animation-delay:.08s}.bar-item:nth-child(3) .bar{animation-delay:.16s}.bar-item:nth-child(4) .bar{animation-delay:.24s}.bar-item:nth-child(5) .bar{animation-delay:.32s}.bar-item:nth-child(6) .bar{animation-delay:.40s}.bar-item:nth-child(7) .bar{animation-delay:.48s}
.chart-grid{animation:gridPulse 5s ease-in-out infinite}
.recent-table tbody tr{animation:rowReveal .65s ease both}
.recent-table tbody tr:nth-child(2){animation-delay:.06s}.recent-table tbody tr:nth-child(3){animation-delay:.12s}.recent-table tbody tr:nth-child(4){animation-delay:.18s}.recent-table tbody tr:nth-child(5){animation-delay:.24s}.recent-table tbody tr:nth-child(6){animation-delay:.30s}
.insight{animation:insightReveal .7s cubic-bezier(.2,.8,.2,1) both}
.insight:nth-of-type(2){animation-delay:.12s}.insight:nth-of-type(3){animation-delay:.24s}.insight:nth-of-type(4){animation-delay:.36s}
.method-row{transition:background .2s ease,transform .2s ease,box-shadow .2s ease}
.method-row:hover{box-shadow:0 8px 18px rgba(25,91,160,.10);transform:translateX(5px) scale(1.015)}
.run-cta,.stButton>button[kind="primary"]{position:relative;overflow:hidden}
.run-cta:after,.stButton>button[kind="primary"]:after{
  content:"";position:absolute;inset:0;background:linear-gradient(110deg,transparent 30%,rgba(255,255,255,.32) 50%,transparent 70%);
  transform:translateX(-120%);animation:buttonSweep 4.5s ease-in-out infinite;
}
@keyframes activeRail{0%,100%{opacity:.55;transform:scaleY(.72)}50%{opacity:1;transform:scaleY(1)}}
@keyframes iconBreathe{0%,100%{transform:translateY(0) rotate(0deg)}50%{transform:translateY(-2px) rotate(2deg)}}
@keyframes barRise{from{opacity:.25;transform:scaleY(0)}to{opacity:1;transform:scaleY(1)}}
@keyframes gridPulse{0%,100%{opacity:.55}50%{opacity:.82}}
@keyframes rowReveal{from{opacity:0;transform:translateX(-12px)}to{opacity:1;transform:translateX(0)}}
@keyframes insightReveal{from{opacity:0;transform:translateY(10px) scale(.98)}to{opacity:1;transform:translateY(0) scale(1)}}
@keyframes buttonSweep{0%,58%{transform:translateX(-120%)}78%,100%{transform:translateX(120%)}}
@media(prefers-reduced-motion:reduce){
  section[data-testid="stSidebar"] .nav-pill:after,.kpi-icon,.bar-item .bar,.chart-grid,.recent-table tbody tr,.insight,.run-cta:after,.stButton>button[kind="primary"]:after{animation:none}
}

/* Keep transformed decorative layers inside the page at the final scroll position. */
.stApp:before,.stApp:after{max-height:100vh;overflow:hidden}
section[data-testid="stSidebar"] .side-feature{transform:none!important}
[data-testid="stHeader"]{display:none!important;height:0!important;min-height:0!important}
.main .block-container{padding-top:0!important}
section[data-testid="stSidebar"]{top:0!important}

/* ---------------- highlighted expandable sections ---------------- */
[data-testid="stExpander"]{
  position:relative;overflow:hidden!important;border:1px solid #b9d3ef!important;
  border-radius:20px!important;background:linear-gradient(115deg,rgba(255,255,255,.96),rgba(232,244,255,.9))!important;
  box-shadow:0 14px 34px rgba(31,89,158,.10),inset 0 1px 0 #fff!important;
  transition:transform .2s ease,box-shadow .2s ease,border-color .2s ease;
}
[data-testid="stExpander"]:before{content:"";position:absolute;left:0;top:0;bottom:0;width:5px;border-radius:20px 0 0 20px;background:linear-gradient(180deg,#2d9cff,#18c9e8);box-shadow:0 0 18px rgba(45,156,255,.34);pointer-events:none}
[data-testid="stExpander"]:hover{transform:translateY(-3px);border-color:#7fb7ee!important;box-shadow:0 20px 42px rgba(31,89,158,.16),inset 0 1px 0 #fff!important}
[data-testid="stExpander"] details summary{min-height:54px!important;padding:14px 18px 14px 24px!important;background:linear-gradient(100deg,rgba(231,243,255,.72),rgba(248,252,255,.72));color:#0b2e6d!important;font-size:14px!important;font-weight:800!important;transition:background .2s ease,color .2s ease}
[data-testid="stExpander"] details summary p,[data-testid="stExpander"] details summary span{font-size:14px!important;font-weight:900!important;letter-spacing:.1px;color:inherit!important}
[data-testid="stExpander"] details summary svg{width:17px!important;height:17px!important;stroke-width:3!important;color:#1769ff!important}
[data-testid="stExpander"] details summary:hover{background:linear-gradient(100deg,rgba(211,234,255,.92),rgba(237,250,255,.9));color:#0757bf!important}
[data-testid="stExpander"] details[open] summary{background:linear-gradient(100deg,#dceeff,#e9fbfa);border-bottom:1px solid #c8def4;color:#064fa9!important}
[data-testid="stExpander"] details[open] summary:after{content:"ACTIVE";float:right;margin:2px 8px 0 12px;padding:4px 7px;border-radius:999px;background:#d4f8ef;color:#078d69;font-size:8px;font-weight:900;letter-spacing:.7px}
[data-testid="stExpander"] details>div{padding:14px 18px 18px 24px!important}
[data-testid="stDataFrame"] th,[data-testid="stDataFrame"] [role="columnheader"]{font-weight:850!important}
</style>
"""
st.markdown(PAGE_CSS, unsafe_allow_html=True)

TIER_LABELS = {"auto_retry": "Auto Retry", "whatsapp": "WhatsApp", "voice_call": "Voice Call"}
TIER_LABELS.update({"manual_review": "Manual Review", "skip": "Skipped"})
TIER_ORDER = ["auto_retry", "whatsapp", "voice_call"]
TIER_BLURB = {
    "auto_retry": "Silent gateway retry. No customer contact.",
    "whatsapp": "Templated nudge with a payment link.",
    "voice_call": "Hinglish call that captures a promise to pay.",
}
TIER_UNIT_COST = {"auto_retry": 0.0, "whatsapp": 0.35, "voice_call": 4.50}
OUTCOME_LABELS = {"success": "Executed", "failed": "Failed", "pending": "Waiting", "skipped": "Blocked by rule", "decision": "Decided"}
EVENT_GROUPS = {
    "Decisions": {"decision_made"},
    "Outreach": {"whatsapp_dry_run", "whatsapp_sent", "whatsapp_failed", "voice_dry_run", "voice_call_completed", "voice_call_failed", "auto_retry_dry_run", "auto_retry_attempted"},
    "Recoveries": {"payment_recovered", "recovery_reverted"},
    "Blocked by a rule": {"intervention_skipped"},
}

@st.cache_data(ttl=15, show_spinner="Loading recovery intelligence...")
def load_all():
    sb = db.get_supabase()
    return {
        "metrics": db.recovery_metrics(sb=sb),
        "transactions": sb.table("transactions").select("*, customers(name, segment)").order("amount", desc=True).execute().data,
        "interventions": sb.table("interventions").select("*").order("fired_at", desc=True).execute().data,
        "audit": sb.table("audit_log").select("*").order("created_at", desc=True).limit(1000).execute().data,
    }

def rupees(amount, decimals=0):
    return f"₹{float(amount):,.{decimals}f}"

def latest_intervention_by_txn(interventions):
    out = {}
    for iv in sorted(interventions, key=lambda i: i.get("fired_at") or ""):
        out[iv["transaction_id"]] = iv
    return out

def event_detail(event_type, payload):
    p = payload or {}
    if event_type in ("decision_made", "intervention_skipped"):
        return p.get("reason", "")
    if event_type in ("whatsapp_dry_run", "whatsapp_sent"):
        body = (p.get("body") or "").replace("\n", " ")
        return f"{'Would send' if event_type.endswith('dry_run') else 'Sent'} to {p.get('to', '?')} — {body[:100]}"
    if event_type == "whatsapp_failed":
        return f"Send failed: {p.get('error', '')}"
    if event_type in ("voice_dry_run", "voice_call_completed"):
        r = p.get("structured_result") or {}
        if r.get("promise_to_pay_date"):
            detail = f"promise to pay {r['promise_to_pay_date']}"
        elif not r.get("call_connected"):
            detail = "no answer"
        else:
            detail = "connected, no commitment"
        if r.get("reason_for_delay"):
            detail += f" ({r['reason_for_delay']})"
        return f"{p.get('provider', 'voice')} — {detail}"
    if event_type == "voice_call_failed":
        return f"Call failed: {p.get('error', '')}"
    if event_type in ("auto_retry_dry_run", "auto_retry_attempted"):
        return f"Silent retry captured {rupees(float(p.get('amount', 0)), 2)}" if p.get("captured") else p.get("decline_reason", "Retry declined")
    if event_type == "payment_recovered":
        return f"{rupees(float(p.get('amount', 0)), 2)} received — credited to {TIER_LABELS.get(p.get('attributed_tier'), 'no tier')}"
    if event_type == "recovery_reverted":
        return "Recovery reverted (demo reset)"
    return ""

def event_tier(event_type, payload):
    p = payload or {}
    for key in ("tier", "attributed_tier", "selected_tier", "chosen_tier"):
        if p.get(key):
            return p[key]
    for prefix, tier in (("whatsapp", "whatsapp"), ("voice", "voice_call"), ("auto_retry", "auto_retry")):
        if event_type.startswith(prefix):
            return tier
    return ""

    def decision_tier(payload):
      """Recover legacy decision labels when an older audit payload lacks tier."""
      p = payload or {}
      reason = str(p.get("reason", "")).lower()
      if "already resolved" in reason or "no longer failed" in reason:
        return "skip"
      if any(marker in reason for marker in ("manual review", "fraud", "stopping rule", "contact attempts")):
        return "manual_review"
      return ""

def build_audit_frame(audit_rows, interventions):
    outcomes = {(iv["transaction_id"], iv["tier"]): iv["outcome"] for iv in sorted(interventions, key=lambda i: i.get("fired_at") or "")}
    latest_by_txn = latest_intervention_by_txn(interventions)
    rows = []
    for a in audit_rows:
        payload = a.get("payload") or {}
        tier = event_tier(a["event_type"], payload)
        if a["event_type"] == "decision_made" and not tier:
          tier = decision_tier(payload)
        txn = a.get("transaction_id") or ""
        intervention = latest_by_txn.get(txn)
        if not tier and intervention:
            tier = intervention.get("tier", "")
        outcome = "decision" if a["event_type"] == "decision_made" else outcomes.get((txn, tier))
        if outcome is None and intervention and a["event_type"] != "decision_made":
            outcome = intervention.get("outcome")
        rows.append({
            "When": pd.to_datetime(a["created_at"]),
            "Payment": txn[:8],
            "Event": a["event_type"].replace("_", " "),
            "Tier": TIER_LABELS.get(tier, "—"),
            "What happened": event_detail(a["event_type"], payload),
            "Outcome": OUTCOME_LABELS.get(outcome, "—"),
            "_event_type": a["event_type"],
        })
    df = pd.DataFrame(rows)
    return df.sort_values("When", ascending=False) if not df.empty else df

def daily_recovery(transactions, days=7):
    today = pd.Timestamp.now(tz="Asia/Kolkata").normalize()
    dates = [today - pd.Timedelta(days=i) for i in range(days - 1, -1, -1)]
    vals = {d: 0.0 for d in dates}
    for transaction in transactions:
        if transaction.get("status") != "recovered":
            continue
        try:
            timestamp = transaction.get("updated_at") or transaction.get("created_at")
            d = pd.to_datetime(timestamp, utc=True).tz_convert("Asia/Kolkata").normalize()
            if d in vals:
                vals[d] += float(transaction.get("amount", 0) or 0)
        except Exception:
            pass
    return dates, [vals[d] for d in dates]

# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------
data = load_all()
metrics = data["metrics"]
interventions = data["interventions"]
transactions = data["transactions"]
recovered = float(metrics["total_recovered"])
at_risk = float(metrics["total_at_risk"])
value_rate = (recovered / at_risk * 100) if at_risk else 0.0
outreach_cost = sum(
    len([i for i in interventions if i["tier"] == t]) * TIER_UNIT_COST[t]
    for t in TIER_ORDER
)

# ---------------------------------------------------------------------------
# Sidebar — native Streamlit rail; every item is a real clickable anchor and cannot be hidden by the app state.
with st.sidebar:
    st.markdown(f"""
    <div class="sidebar-brand">
      <div class="rp-logo-row"><img class="rp-mark" src="{RAZORPAY_LOGO_DATA_URI}" alt="Razorpay logo"><div class="rp-word">Razorpay</div></div>
      <div class="product-title">PayRecover AI</div>
      <div class="product-copy">Recover more. Grow faster.</div>
    </div>
    <div class="nav-section-label">Workspace</div>
    <a href="#dashboard" class="nav-pill"><span class="nav-icon">⌂</span><span>Dashboard</span></a>
    <a href="#failed-payments" class="nav-pill"><span class="nav-icon">▣</span><span>Failed Payments</span></a>
    <a href="#recovery-actions" class="nav-pill"><span class="nav-icon">↗</span><span>Recovery Actions</span></a>
    <a href="#customers" class="nav-pill"><span class="nav-icon">♙</span><span>Customers</span></a>
    <a href="#analytics" class="nav-pill"><span class="nav-icon">▥</span><span>Analytics</span></a>
    <a href="#ai-insights" class="nav-pill"><span class="nav-icon">✦</span><span>AI Insights</span></a>
    <a href="#audit-log" class="nav-pill"><span class="nav-icon">▤</span><span>Audit Log</span></a>
    <a href="#settings" class="nav-pill"><span class="nav-icon">⚙</span><span>Settings</span></a>
    """, unsafe_allow_html=True)

st.markdown('<div id="dashboard" class="anchor-target"></div>', unsafe_allow_html=True)

# Top bar
# ---------------------------------------------------------------------------
now = datetime.now(ZoneInfo("Asia/Kolkata")).strftime("%a, %d %b %Y")
mode = "Simulation mode" if config.DRY_RUN else "Live recovery mode"
mode_copy = "Actions are logged, not sent" if config.DRY_RUN else "Messages and calls are enabled"
st.markdown(
    f'<div class="topbar"><div class="top-group"><div class="top-pill"><span class="live-dot"></span><span>{html.escape(mode)}</span><span style="color:#8191a8">·</span><span>{html.escape(mode_copy)}</span></div></div><div class="top-group right"><div class="top-pill">{now}</div><div class="top-pill"><span class="avatar">YD</span> Y DARSHAN</div></div></div>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Hero
# ---------------------------------------------------------------------------
st.markdown(
  f"""
<div class="hero">
  <div class="hero-left">
    <div class="kicker"><span class="kicker-dot">✦</span> RAZORPAY BUILDATHON 2026 <span>·</span> TRACK 3</div>
    <h1>AI Revenue <span class="grad">Recovery</span></h1>
    <div class="hero-desc"><strong>Smarter recovery. Stronger revenue.</strong><br>Using intelligent recovery workflows to turn failed payments into loyal customers.</div>
    <div class="hero-chips">
      <div class="hero-chip"><span class="chip-icon">↻</span><span><b>Recover</b><small>Reduce loss</small></span></div>
      <div class="hero-chip"><span class="chip-icon">◉</span><span><b>Engage</b><small>Reach smarter</small></span></div>
      <div class="hero-chip"><span class="chip-icon">◆</span><span><b>Retain</b><small>Build trust</small></span></div>
      <div class="hero-chip"><span class="chip-icon">↗</span><span><b>Grow</b><small>Increase revenue</small></span></div>
    </div>
    <div class="hero-proof"><span>✓ Explainable decisions</span><span>✓ Cost-aware outreach</span><span>✓ Full audit trail</span></div>
  </div>
  <div class="hero-art">
    <div class="script">Every payment has<br><b>a second chance.</b></div>
    <div class="hero-glow glow-one"></div><div class="hero-glow glow-two"></div>
    <div class="hero-bars"><i></i><i></i><i></i><i></i><i></i></div>
    <div class="floating-tile tile-one"><span>↗</span><b>203x</b><small>return</small></div>
    <div class="floating-tile tile-two"><span>✓</span><b>{rupees(recovered)}</b><small>recovered</small></div>
    <div class="card3d"><div class="card-shine"></div><div class="card-brand"><img class="tiny-mark" src="{RAZORPAY_LOGO_DATA_URI}" alt="Razorpay logo"> Razorpay</div><div class="card-copy"><b>PayRecover</b><br>Recover · Engage · Retain</div><div class="card-chip">◈</div></div>
    <div class="hero-quote"><b>“</b><span>Failed payments<br><strong>today.</strong><br>Loyal customers<br><strong>tomorrow.</strong></span><i></i></div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# KPI cards
# ---------------------------------------------------------------------------
wa_count = sum(1 for i in interventions if i.get("tier") == "whatsapp")
retry_count = sum(1 for i in interventions if i.get("tier") == "auto_retry")
voice_count = sum(1 for i in interventions if i.get("tier") == "voice_call")
kpis = [
    ("▥", "Total Amount at Risk", rupees(at_risk, 2), f'<span class="badge">{metrics["total_transactions"]} failed payments</span>', "#1769ff", "#e8f2ff"),
    ("▰", "Recovered Amount", rupees(recovered, 2), f'<span class="badge green">↑ {metrics["recovery_rate_pct"]:.1f}% recovery rate</span>', "#0aa36d", "#e5faef"),
    ("⚡", "Interventions Fired", str(len(interventions)), f"{wa_count} WhatsApp · {retry_count} Auto Retry · {voice_count} Voice Calls", "#7547ff", "#f0eaff"),
    ("◎", "Outreach Cost", rupees(outreach_cost, 2), f'<span class="badge orange">↑ {recovered / outreach_cost:,.0f}x return</span>' if outreach_cost and recovered else "No outreach spend", "#ff8a16", "#fff0df"),
]
kpi_html = ['<div class="kpi-grid">']
for icon, label, value, sub, icon_color, icon_bg in kpis:
    kpi_html.append(
        f'<div class="kpi" style="--glow:{icon_color};--icon:{icon_color};--iconbg:{icon_bg}"><div class="kpi-top"><div class="kpi-icon">{icon}</div></div><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'
    )
kpi_html.append("</div>")
st.markdown("".join(kpi_html), unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Recovery intelligence
# ---------------------------------------------------------------------------
st.markdown('<div id="analytics" class="anchor-target"></div>', unsafe_allow_html=True)
st.markdown(
    '<div class="command-title">Recovery intelligence</div><div class="command-sub">Live recovery performance across amount, channels and outcomes.</div>',
    unsafe_allow_html=True,
)

left, right = st.columns([1.72, 1], gap="medium")

with left:
    dates, vals = daily_recovery(transactions, 7)
    labels = [d.strftime("%b %d") for d in dates]
    maxv = max(max(vals), 1.0)
    bars = "".join(
      f'<div class="bar-item"><div class="bar" title="{html.escape(label)}: {html.escape(rupees(v, 2))} recovered" aria-label="{html.escape(label)}: {html.escape(rupees(v, 2))} recovered" style="height:{max(4,(v/maxv)*150) if v else 0:.0f}px"></div></div>'
      for label, v in zip(labels, vals)
    )
    xlabels = "".join(f"<span>{html.escape(lab)}</span>" for lab in labels)
    recovered_view = sum(vals)
    st.markdown(
        f"""
<div class="panel">
  <div class="panel-head">
    <div><div class="panel-title">Recovery Trend</div><div class="panel-sub">Recovered amount over time</div></div>
  </div>
  <div class="chart">
    <div class="chart-y"><span>10K</span><span>8K</span><span>6K</span><span>4K</span><span>2K</span><span>0</span></div>
    <div class="chart-area">
      <div class="chart-grid"></div>
      <div class="bar-wrap">{bars}</div>
    </div>
    <div class="chart-x">{xlabels}</div>
  </div>
  <div class="chart-legend">
    <span><i class="legend-square" style="background:#238cff"></i>Recovered Amount (₹)</span>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

with right:
    counts = {t: sum(1 for i in interventions if i.get("tier") == t) for t in TIER_ORDER}
    total = max(sum(counts.values()), 1)
    palette = {"whatsapp": "#10b981", "auto_retry": "#348ff2", "voice_call": "#ff9d1f"}
    segs = []
    start = 0.0
    for t in TIER_ORDER:
        pct = counts[t] / total * 100
        end = start + pct
        segs.append(f"{palette[t]} {start:.2f}% {end:.2f}%")
        start = end
    circumference = 2 * math.pi * 59
    donut_segments = []
    start = 0.0
    for t in TIER_ORDER:
      pct = counts[t] / total * 100
      segment_length = circumference * pct / 100
      tooltip = f"{TIER_LABELS[t]}: {counts[t]} actions ({pct:.1f}%)"
      donut_segments.append(
        f'<circle class="donut-segment" cx="83" cy="83" r="59" fill="none" stroke="{palette[t]}" stroke-width="32" stroke-dasharray="{segment_length:.3f} {circumference - segment_length:.3f}" stroke-dashoffset="{-circumference * start / 100:.3f}"><title>{html.escape(tooltip)}</title></circle>'
      )
      start += pct
    legend_rows = "".join(
      f'<div class="method-row" title="{html.escape(TIER_LABELS[t])}: {counts[t]} actions ({counts[t]/total*100:.1f}%)"><i class="legend-dot" style="background:{palette[t]}"></i><span class="method-name">{TIER_LABELS[t]}</span><span class="method-count">{counts[t]}</span><span class="method-pct">{counts[t]/total*100:.1f}%</span></div>'
        for t in TIER_ORDER
    )
    st.markdown(
        f"""
<div class="panel">
  <div class="panel-head"><div><div class="panel-title">Recovery by Method</div><div class="panel-sub">How the AI chose to reach out</div></div></div>
  <div class="donut-layout">
    <div class="donut" aria-label="Recovery by method"><svg class="donut-svg" viewBox="0 0 166 166" role="img">{"".join(donut_segments)}</svg><div class="donut-center"><div class="donut-number">{sum(counts.values())}</div><div class="donut-label">Total</div></div></div>
    <div class="method-list">{legend_rows}</div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------------------------
# Recent actions + AI insights
# ---------------------------------------------------------------------------
left, right = st.columns([1.62, 1], gap="medium")

with left:
    st.markdown('<div id="recovery-actions" class="anchor-target"></div>', unsafe_allow_html=True)
    by_txn = latest_intervention_by_txn(interventions)
    recent = []
    for t in transactions:
        iv = by_txn.get(t["id"])
        if iv:
            recent.append(
                {
                    "ID": t["id"][:8],
                    "Customer": (t.get("customers") or {}).get("name", "?"),
                    "Amount": float(t["amount"]),
                    "Method": TIER_LABELS.get(iv.get("tier"), iv.get("tier", "—")),
                    "Status": OUTCOME_LABELS.get(iv.get("outcome"), iv.get("outcome", "—")),
                    "Time": str(iv.get("fired_at", "") or "")[:10],
                }
            )
    st.markdown(
        '<div class="panel"><div class="panel-head"><div><div class="panel-title">Recent Recovery Actions</div><div class="panel-sub">Latest interventions and their current outcomes</div></div></div>',
        unsafe_allow_html=True,
    )
    if recent:
        table_rows=[]
        for r in recent[:6]:
            method_key = {"WhatsApp":"whatsapp","Auto Retry":"auto","Voice Call":"voice"}.get(r["Method"], "auto")
            outcome_key = str(r["Status"]).lower()
            status_class = "failed" if "fail" in outcome_key else ("pending" if "wait" in outcome_key else "")
            table_rows.append(f"<tr><td><b>{html.escape(r['ID'])}</b></td><td>{html.escape(str(r['Customer']))}</td><td><b>{rupees(r['Amount'],2)}</b></td><td><span class=\"method-tag {method_key}\">{html.escape(r['Method'])}</span></td><td><span class=\"status-tag {status_class}\">● {html.escape(r['Status'])}</span></td><td>{html.escape(r['Time'])}</td></tr>")
        st.markdown('<table class="recent-table"><thead><tr><th>ID</th><th>Customer</th><th>Amount</th><th>Method</th><th>Status</th><th>Date</th></tr></thead><tbody>'+''.join(table_rows)+'</tbody></table>', unsafe_allow_html=True)
    else:
        st.info("Run the recovery pipeline to populate interventions.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div id="ai-insights" class="anchor-target"></div>', unsafe_allow_html=True)
    high = sum(
        1
        for t in transactions
        if float(t.get("amount", 0)) > decision_engine.HIGH_VALUE_THRESHOLD
        and t.get("status") == "failed"
    )
    insights = [
        ("↗", "green", "Customers respond faster to timely outreach", f"{len(interventions)} interventions are logged and auditable."),
        ("♟", "purple", "High-value customers need personal outreach", f"Use voice calls for amounts above {rupees(decision_engine.HIGH_VALUE_THRESHOLD)}."),
        ("◷", "blue", "Retry automation protects margin", f"{retry_count} payments qualified for a no-contact retry."),
    ]
    st.markdown(
        '<div class="panel"><div class="panel-head"><div><div class="panel-title">AI Insights</div><div class="panel-sub">Explainable signals derived from current recovery data</div></div></div>',
        unsafe_allow_html=True,
    )
    for icon, kind, title, copy in insights:
        st.markdown(
            f'<div class="insight {kind}"><div class="insight-icon">{icon}</div><div><div class="insight-title">{html.escape(title)}</div><div class="insight-copy">{html.escape(copy)}</div></div></div>',
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Existing operational functionality — intentionally preserved.
# ---------------------------------------------------------------------------
st.markdown('<div id="failed-payments" class="anchor-target"></div>', unsafe_allow_html=True)
failed_payments = [t for t in transactions if t.get("status") == "failed"]
st.markdown(
  '<div class="command-title">Failed payments</div><div class="command-sub">Payments that need recovery action and are still unresolved.</div>',
  unsafe_allow_html=True,
)
failed_rows = []
for payment in failed_payments:
  customer = payment.get("customers") or {}
  failed_rows.append(
    {
      "Payment": payment.get("id", "")[:8],
      "Customer": customer.get("name", "Unknown"),
      "Segment": customer.get("segment", "—"),
      "Amount": float(payment.get("amount", 0) or 0),
            "Failure reason": (payment.get("failure_reason_code") or payment.get("failure_reason") or payment.get("failure_code") or "—").replace("_", " ").title(),
      "Status": "Failed",
    }
  )
if failed_rows:
  st.dataframe(
    pd.DataFrame(failed_rows),
    width="stretch",
    hide_index=True,
    column_config={"Amount": st.column_config.NumberColumn(format="₹%.2f")},
  )
else:
  st.success("No failed payments right now.")

st.markdown(
    '<div class="command-title">Recovery operations</div><div class="command-sub">Operate the same recovery workflow below — now inside the premium command center.</div>',
    unsafe_allow_html=True,
)

iv_df = pd.DataFrame(interventions)
if iv_df.empty:
    st.info("No interventions yet. Run the pipeline, then refresh.")
else:
    blocked = {}
    for a in data["audit"]:
        if a["event_type"] == "intervention_skipped":
            tier = (a.get("payload") or {}).get("tier", "")
            blocked[tier] = blocked.get(tier, 0) + 1
    rows = []
    for tier in TIER_ORDER:
        sub = iv_df[iv_df["tier"] == tier]
        if sub.empty:
            continue
        outcomes = sub["outcome"].value_counts().to_dict()
        rows.append(
            {
                "Tier": TIER_LABELS[tier],
                "What it is": TIER_BLURB[tier],
                "Fired": len(sub),
                "Share": len(sub) / len(iv_df),
                "Executed": outcomes.get("success", 0),
                "Blocked": blocked.get(tier, 0) + outcomes.get("skipped", 0),
                "Cost": len(sub) * TIER_UNIT_COST[tier],
            }
        )
    with st.expander("▦ Recovery strategy · three cost-ordered tiers", expanded=True):
        st.dataframe(
            pd.DataFrame(rows),
            width="stretch",
            hide_index=True,
            column_config={
                "Share": st.column_config.ProgressColumn("Share of batch", min_value=0, max_value=1, format="percent"),
                "Cost": st.column_config.NumberColumn(format="₹%.2f"),
            },
        )

promises = [i for i in interventions if i.get("promise_to_pay_date")]
if promises:
    with st.expander(f"☎ Promises to pay · {len(promises)} active commitment(s)", expanded=True):
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Payment": p["transaction_id"][:8],
                        "Promised for": p["promise_to_pay_date"],
                        "What they said": p.get("notes") or "—",
                    }
                    for p in sorted(promises, key=lambda x: x["promise_to_pay_date"])
                ]
            ),
            width="stretch",
            hide_index=True,
        )

by_txn = latest_intervention_by_txn(interventions)
open_payments = [t for t in transactions if t["status"] == "failed" and t["id"] in by_txn]
st.markdown('<div id="customers" class="anchor-target"></div>', unsafe_allow_html=True)
with st.expander("💳 Simulate a customer paying", expanded=False):
    st.caption("Uses the same recovery callback as the working dashboard. Metrics update after a payment is marked recovered.")
    if not open_payments:
        st.success("Every payment that had an intervention has been recovered.")
    else:
        def _label(t):
            tier = by_txn[t["id"]]["tier"]
            who = (t.get("customers") or {}).get("name", "?")
            return f"{t['id'][:8]} · {rupees(float(t['amount']))} · {who} · {TIER_LABELS.get(tier, tier)}"

        pick, act = st.columns([3, 1], vertical_alignment="bottom")
        with pick:
            choice = st.selectbox(
                "Payment to mark as paid",
                open_payments,
                format_func=_label,
                help="Pick a failed payment to simulate a successful recovery.",
            )
        with act:
            if st.button("Mark as paid", type="primary", width="stretch", icon="💳"):
                ok, msg = outcome_tracker.mark_recovered(choice["id"], source="dashboard")
                load_all.clear()
                st.toast(msg, icon="✅" if ok else "❌")
                st.rerun()

    recovered_rows = [t for t in transactions if t["status"] == "recovered"]
    if recovered_rows:
        st.markdown("#### Recovered payments")
        st.dataframe(
            pd.DataFrame(
                [
                    {
                        "Payment": t["id"][:8],
                        "Customer": (t.get("customers") or {}).get("name", "?"),
                        "Amount": float(t["amount"]),
                        "Credited to": TIER_LABELS.get((by_txn.get(t["id"]) or {}).get("tier"), "—"),
                    }
                    for t in recovered_rows
                ]
            ),
            width="stretch",
            hide_index=True,
            column_config={"Amount": st.column_config.NumberColumn(format="₹%.2f")},
        )
        undo = st.selectbox(
            "Put one back to failed",
            recovered_rows,
            format_func=lambda t: f"{t['id'][:8]} · {rupees(float(t['amount']))}",
            key="undo_pick",
        )
        if st.button("Revert to failed"):
            ok, msg = outcome_tracker.undo_recovered(undo["id"])
            load_all.clear()
            st.toast(msg, icon="✅" if ok else "❌")
            st.rerun()

with st.expander("🧠 How the recovery engine decides", expanded=False):
    st.caption("First-match-wins rules. The same decision_engine.py remains responsible for the actual decision.")
    st.dataframe(
        pd.DataFrame(
            [
                {"#": 1, "If": "payment is no longer failed", "Then": "skip", "Because": "already resolved"},
                {"#": 2, "If": "flagged as fraud risk", "Then": "manual review", "Because": "no automated contact"},
                {"#": 3, "If": f"{decision_engine.MAX_CONTACT_ATTEMPTS} contact attempts reached", "Then": "manual review", "Because": "stopping rule"},
                {"#": 4, "If": "failure is retryable + first attempt", "Then": "auto-retry", "Because": "silent retry costs nothing"},
                {"#": 5, "If": f"B2B invoice > {rupees(decision_engine.HIGH_VALUE_THRESHOLD)} or failed twice", "Then": "voice call", "Because": "high value / repeat failure"},
                {"#": 6, "If": f"customer must act + > {rupees(decision_engine.HIGH_VALUE_THRESHOLD)}", "Then": "voice call", "Because": "human touch is worthwhile"},
                {"#": 7, "If": "anything else", "Then": "WhatsApp", "Because": "low-cost default nudge"},
            ]
        ),
        width="stretch",
        hide_index=True,
    )
    st.markdown(
        f"**Stopping controls:** never contact a recovered customer · maximum {decision_engine.MAX_CONTACT_ATTEMPTS} contact attempts · calls only between {decision_engine.CALL_WINDOW_START:%H:%M} and {decision_engine.CALL_WINDOW_END:%H:%M} · fraud-flagged payments receive no automated contact."
    )

st.markdown('<div id="audit-log" class="anchor-target"></div>', unsafe_allow_html=True)
with st.expander("🧾 Audit trail · every decision, send, refusal and recovery", expanded=False):
    audit_df = build_audit_frame(data["audit"], interventions)
    if audit_df.empty:
        st.info("Audit trail is empty. Run the pipeline first.")
    else:
        f1, f2 = st.columns([2, 3])
        groups = f1.multiselect("Show", list(EVENT_GROUPS), default=[], placeholder="Everything")
        search = f2.text_input("Search", "", placeholder="Payment id or reason...")
        view = audit_df
        if groups:
            wanted = set().union(*(EVENT_GROUPS[g] for g in groups))
            view = view[view["_event_type"].isin(wanted)]
        if search:
            s = search.strip().lower()
            view = view[
                view["Payment"].str.lower().str.contains(s)
                | view["What happened"].str.lower().str.contains(s)
            ]
        st.caption(f"Showing {len(view)} of {len(audit_df)} events.")
        st.dataframe(view.drop(columns=["_event_type"]), width="stretch", hide_index=True, height=420)
        st.download_button(
            "Export audit CSV",
            view.drop(columns=["_event_type"]).to_csv(index=False).encode("utf-8"),
            file_name="payrecover_audit_trail.csv",
            mime="text/csv",
        )

st.markdown('<div id="settings" class="anchor-target"></div>', unsafe_allow_html=True)
st.markdown(
  '<div class="command-title">Settings</div><div class="command-sub">Control the dashboard refresh and review the current operating mode.</div>',
  unsafe_allow_html=True,
)
mode_text = "Simulation mode — actions are logged, not sent." if config.DRY_RUN else "Live recovery mode — configured providers may send messages and calls."
st.markdown(
  f'<div class="settings-panel"><div class="settings-status"><span class="settings-status-dot"></span><span>{html.escape(mode_text)}</span></div></div>',
  unsafe_allow_html=True,
)
if st.button("Refresh live data", type="primary"):
  st.session_state["data_refreshed"] = True
  load_all.clear()
  st.rerun()
if st.session_state.pop("data_refreshed", False):
  st.success("Data refreshed.")

st.markdown(
  '<div class="site-footer"><div class="site-footer-title">Built with ❤️ for resilient payment operations</div><div class="site-footer-copy">Razorpay · AI · Open Source</div><div class="site-footer-version">PayRecover AI · v1.0.0</div></div>',
  unsafe_allow_html=True,
)
