#!/usr/bin/env python3#!/usr/bin/env python3
"""
FinLedger - Professional Accounting System
==========================================
Railway.app web deployment version.
"""

import http.server
import socketserver
import threading
import os
import json

PORT = int(os.environ.get("PORT", 8765))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FinLedger</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0f0f11;--surface:#16161a;--surface2:#1e1e24;--surface3:#26262e;
  --border:#2e2e38;--accent:#c8ff00;--text:#f0f0f4;--text2:#9090a8;--text3:#5a5a72;
  --green:#4ade80;--red:#f87171;--blue:#60a5fa;--purple:#a78bfa;--yellow:#ffd93d;
  --radius:10px;
}
/* LIGHT MODE */
body.light-mode{
  --bg:#f4f5f7;--surface:#ffffff;--surface2:#f0f1f3;--surface3:#e8e9eb;
  --border:#dde0e4;--accent:#0057ff;--text:#1a1d23;--text2:#5c6070;--text3:#9198a6;
  --green:#16a34a;--red:#dc2626;--blue:#2563eb;--purple:#7c3aed;--yellow:#d97706;
}
body.light-mode .sidebar{background:#ffffff;border-right:1px solid var(--border);}
body.light-mode .topbar{background:#ffffff;}
body.light-mode .nav-item.active{background:rgba(0,87,255,.06);}
body.light-mode input,body.light-mode select,body.light-mode textarea{background:#f8f9fa;color:var(--text);}
body.light-mode .modal{background:#ffffff;}
body.light-mode .kpi-card,body.light-mode .card,body.light-mode .chart-area{background:#ffffff;}
body.light-mode .btn-ghost{background:#f0f1f3;color:var(--text2);}
body.light-mode .user-card{background:#f4f5f7;}
body.light-mode .date-filter-bar{background:#f0f1f3;}
body.light-mode .totbar{background:#f0f1f3;}
body.light-mode .rtbl tr.rh td{background:#f0f1f3;}
body.light-mode .autocomplete-list{background:#ffffff;}
body.light-mode th{color:var(--text3);}
body.light-mode td{color:var(--text2);}
body.light-mode tr:hover td{background:#f4f5f7;color:var(--text);}
/* Theme toggle button */
.theme-toggle{display:flex;align-items:center;gap:8px;background:var(--surface2);border:1px solid var(--border);border-radius:20px;padding:4px 6px;cursor:pointer;transition:all .2s;}
.theme-toggle-track{width:36px;height:20px;background:var(--surface3);border-radius:10px;position:relative;transition:background .2s;}
.theme-toggle-track.on{background:var(--accent);}
.theme-toggle-thumb{width:16px;height:16px;background:#fff;border-radius:50%;position:absolute;top:2px;left:2px;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3);}
.theme-toggle-track.on .theme-toggle-thumb{transform:translateX(16px);}
.theme-toggle-label{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;min-height:100vh;display:flex;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:232px;min-width:232px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:0;}
.logo-area{padding:22px 20px 18px;border-bottom:1px solid var(--border);}
.logo-title{font-family:'DM Serif Display',serif;font-size:22px;color:var(--accent);letter-spacing:-.5px;}
.logo-sub{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;margin-top:2px;}
.nav{padding:16px 0;flex:1;overflow-y:auto;}
.nav-sec{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;padding:10px 20px 5px;}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 20px;cursor:pointer;color:var(--text2);border-left:2px solid transparent;transition:all .15s;font-size:13px;font-weight:500;user-select:none;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);border-left-color:var(--accent);background:rgba(200,255,0,.06);}
.nav-icon{font-size:14px;width:18px;text-align:center;flex-shrink:0;}

/* ── USER PROFILE CARD (sidebar bottom) ── */
.sidebar-foot{padding:14px 14px;border-top:1px solid var(--border);}
.user-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:12px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:border-color .15s;}
.user-card:hover{border-color:var(--accent);}
.user-avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:14px;font-weight:600;color:#0f0f11;flex-shrink:0;background:var(--accent);}
.user-info{flex:1;min-width:0;}
.user-name{font-weight:600;font-size:12px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-role{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-co{font-size:10px;color:var(--text3);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-gear{color:var(--text3);font-size:13px;flex-shrink:0;}

/* ── MAIN ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);padding:0 28px;height:56px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.topbar-left{}
.page-title{font-family:'DM Serif Display',serif;font-size:20px;}
.breadcrumb{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;}
.topbar-right{display:flex;align-items:center;gap:10px;}
.greeting{font-size:13px;color:var(--text2);}
.greeting strong{color:var(--text);font-weight:600;}
.server-badge{background:rgba(200,255,0,.1);border:1px solid rgba(200,255,0,.3);color:var(--accent);padding:4px 12px;border-radius:20px;font-size:11px;font-family:'DM Mono',monospace;}

/* ── BUTTONS ── */
.btn{padding:7px 16px;border-radius:7px;border:none;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;transition:all .16s;}
.btn-primary{background:var(--accent);color:#0f0f11;}
.btn-primary:hover{background:#d4ff26;transform:translateY(-1px);}
.btn-ghost{background:var(--surface2);color:var(--text2);border:1px solid var(--border);}
.btn-ghost:hover{color:var(--text);}
.btn-danger{background:rgba(248,113,113,.15);color:var(--red);border:1px solid rgba(248,113,113,.3);}
.btn-sm{padding:5px 11px;font-size:12px;}

/* ── CONTENT ── */
.content{flex:1;overflow-y:auto;padding:28px;}
.content::-webkit-scrollbar{width:6px;}
.content::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
.page{display:none;}
.page.active{display:block;animation:fadeIn .2s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* ── KPI CARDS ── */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;position:relative;overflow:hidden;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.kpi-card.g::before{background:var(--green);}
.kpi-card.r::before{background:var(--red);}
.kpi-card.b::before{background:var(--blue);}
.kpi-card.a::before{background:var(--accent);}
.card-title{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;}
.card-value{font-family:'DM Serif Display',serif;font-size:28px;}
.card-delta{font-size:12px;margin-top:4px;color:var(--text3);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}

/* ── TABLES ── */
.tbl-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;}
th{padding:10px 14px;text-align:left;font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.2px;border-bottom:1px solid var(--border);white-space:nowrap;}
td{padding:11px 14px;border-bottom:1px solid rgba(46,46,56,.5);font-size:13px;color:var(--text2);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);color:var(--text);}
.amt{font-family:'DM Mono',monospace;text-align:right;}
.pos{color:var(--green)!important;}
.neg{color:var(--red)!important;}

/* ── BADGES ── */
.badge{display:inline-flex;align-items:center;padding:2px 9px;border-radius:20px;font-size:10px;font-weight:600;font-family:'DM Mono',monospace;text-transform:uppercase;}
.bg{background:rgba(74,222,128,.12);color:var(--green);}
.br{background:rgba(248,113,113,.12);color:var(--red);}
.bb{background:rgba(96,165,250,.12);color:var(--blue);}
.by{background:rgba(255,217,61,.12);color:var(--yellow);}
.ba{background:rgba(200,255,0,.12);color:var(--accent);}
.bp{background:rgba(167,139,250,.12);color:var(--purple);}

/* ── FORMS ── */
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.fgrid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;}
.fg{display:flex;flex-direction:column;gap:5px;}
.fg.full{grid-column:1/-1;}
label{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;}
input,select,textarea{background:var(--surface2);border:1px solid var(--border);border-radius:7px;padding:9px 12px;color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;transition:border .15s;width:100%;outline:none;}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 2px rgba(200,255,0,.1);}
select option{background:var(--surface2);}
textarea{resize:vertical;min-height:72px;}

/* ── LAYOUT HELPERS ── */
.row{display:flex;gap:16px;}
.col{flex:1;}
.col2{flex:2;}
.divider{height:1px;background:var(--border);margin:20px 0;}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;}
.sec-title{font-family:'DM Serif Display',serif;font-size:17px;}
.sec-sub{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;}
.tabs{display:flex;gap:2px;background:var(--surface2);border-radius:8px;padding:3px;width:fit-content;margin-bottom:20px;}
.tab{padding:7px 18px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);transition:all .15s;}
.tab.active{background:var(--surface3);color:var(--text);}
.totbar{display:flex;gap:24px;padding:14px 20px;background:var(--surface2);border-radius:8px;border:1px solid var(--border);margin-bottom:16px;flex-wrap:wrap;}
.tot-item label{display:block;font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
.tot-item span{font-family:'DM Serif Display',serif;font-size:18px;}

/* ── CHART ── */
.chart-area{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}
.chart-bars{display:flex;align-items:flex-end;gap:8px;height:160px;}
.bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end;}
.bar{width:100%;border-radius:4px 4px 0 0;min-height:4px;transition:all .3s;}
.bar:hover{filter:brightness(1.2);}
.bar-lbl{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;}

/* ── REPORT TABLES ── */
.rtbl{width:100%;border-collapse:collapse;}
.rtbl tr.rh td{background:var(--surface2);color:var(--text);font-weight:600;font-size:12px;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;padding:8px 14px;}
.rtbl tr.rd td{padding:8px 14px;color:var(--text2);font-size:13px;border-bottom:1px solid rgba(46,46,56,.4);}
.rtbl tr.rd:hover td{background:rgba(255,255,255,.02);}
.rtbl tr.rs td{padding:9px 14px;font-weight:600;color:var(--text);border-top:1px solid var(--border);}
.rtbl tr.rt td{padding:11px 14px;font-family:'DM Serif Display',serif;font-size:16px;color:var(--accent);border-top:2px solid var(--accent);background:rgba(200,255,0,.04);}
.rtbl .ind{padding-left:30px!important;}
.rtbl .num{font-family:'DM Mono',monospace;text-align:right;}

/* ── JE LINES ── */
.je-line{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:10px;align-items:center;margin-bottom:8px;}

/* ── OVERLAYS / MODALS ── */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:100;display:none;align-items:center;justify-content:center;backdrop-filter:blur(5px);}
.overlay.open{display:flex;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;width:min(620px,95vw);max-height:90vh;overflow-y:auto;box-shadow:0 8px 50px rgba(0,0,0,.6);}
.modal.wide{width:min(740px,95vw);}
.modal.xwide{width:min(820px,95vw);}
.mhdr{padding:22px 26px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.mtitle{font-family:'DM Serif Display',serif;font-size:20px;}
.mclose{width:30px;height:30px;border-radius:7px;background:var(--surface2);border:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:15px;}
.mclose:hover{color:var(--text);}
.mbody{padding:26px;}
.mfoot{padding:16px 26px;border-top:1px solid var(--border);display:flex;justify-content:flex-end;gap:10px;}
.modal::-webkit-scrollbar{width:4px;}
.modal::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}

/* ── SETTINGS TABS ── */
.set-tabs{display:flex;border-bottom:1px solid var(--border);margin-bottom:22px;gap:0;}
.set-tab{padding:10px 20px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);border-bottom:2px solid transparent;transition:all .15s;margin-bottom:-1px;}
.set-tab:hover{color:var(--text);}
.set-tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.set-panel{display:none;}
.set-panel.active{display:block;}

/* ── AVATAR PICKER ── */
.avatar-row{display:flex;align-items:center;gap:16px;margin-bottom:6px;}
.avatar-big{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:24px;font-weight:700;color:#0f0f11;background:var(--accent);flex-shrink:0;}
.color-swatches{display:flex;gap:8px;flex-wrap:wrap;}
.swatch{width:26px;height:26px;border-radius:50%;cursor:pointer;border:2px solid transparent;transition:all .15s;}
.swatch:hover,.swatch.sel{border-color:var(--text);transform:scale(1.15);}

/* ── SECTION DIVIDER LABEL ── */
.set-section-label{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;margin-top:4px;}

/* ── INFO ROW ── */
.info-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(46,46,56,.5);}
.info-row:last-child{border-bottom:none;}
.info-label{font-size:12px;color:var(--text3);}
.info-val{font-size:13px;color:var(--text);font-family:'DM Mono',monospace;}

/* ── EXPORT ICON BUTTONS ── */
.btn-xls{background:rgba(74,222,128,.12);color:#4ade80;border:1px solid rgba(74,222,128,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-xls:hover{background:rgba(74,222,128,.28);transform:translateY(-1px);}
.btn-pdf2{background:rgba(248,113,113,.12);color:#f87171;border:1px solid rgba(248,113,113,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-pdf2:hover{background:rgba(248,113,113,.28);transform:translateY(-1px);}
/* contacts */
.contact-type-toggle{display:flex;gap:4px;background:var(--surface3);border-radius:7px;padding:3px;}
.ct-btn{padding:5px 14px;border-radius:5px;cursor:pointer;font-size:12px;font-weight:600;color:var(--text2);border:none;background:transparent;font-family:'DM Sans',sans-serif;transition:all .15s;}
.ct-btn.active{background:var(--surface);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.3);}
.contact-tabs{display:flex;border-bottom:1px solid var(--border);margin-bottom:18px;}
.contact-tab{padding:9px 18px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);border-bottom:2px solid transparent;transition:all .15s;margin-bottom:-1px;}
.contact-tab:hover{color:var(--text);}
.contact-tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.contact-panel{display:none;}
.contact-panel.active{display:block;}
.contact-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;display:flex;align-items:center;gap:14px;cursor:pointer;transition:all .15s;margin-bottom:8px;}
.contact-card:hover{border-color:var(--accent);background:var(--surface2);}
.contact-avatar{width:40px;height:40px;border-radius:50%;background:var(--surface3);display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:15px;font-weight:700;color:var(--accent);flex-shrink:0;border:1px solid var(--border);}
.contact-name{font-weight:600;font-size:14px;color:var(--text);}
.contact-meta{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:2px;}
.contact-badge{margin-left:auto;flex-shrink:0;}
.contacts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}
/* autocomplete dropdown */
.autocomplete-wrap{position:relative;}
.autocomplete-list{position:absolute;top:100%;left:0;right:0;background:var(--surface);border:1px solid var(--accent);border-top:none;border-radius:0 0 7px 7px;z-index:200;max-height:200px;overflow-y:auto;display:none;}
.autocomplete-list.open{display:block;}
.autocomplete-item{padding:9px 12px;cursor:pointer;font-size:13px;color:var(--text2);border-bottom:1px solid rgba(46,46,56,.4);}
.autocomplete-item:hover{background:var(--surface2);color:var(--text);}
.autocomplete-item:last-child{border-bottom:none;}
.autocomplete-item .ac-meta{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:1px;}
/* date filter bar */
.date-filter-bar{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;margin-bottom:16px;flex-wrap:wrap;}
.date-filter-bar label{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin:0;}
.date-filter-bar input{width:140px;padding:6px 10px;font-size:12px;background:var(--surface3);border:1px solid var(--border);border-radius:6px;color:var(--text);}
.date-filter-bar input:focus{border-color:var(--accent);}
.filter-active-badge{background:rgba(200,255,0,.15);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:3px 10px;border-radius:20px;font-size:10px;font-family:'DM Mono',monospace;font-weight:600;}
/* reconcile button */
.btn-reconcile{background:rgba(200,255,0,.12);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;transition:all .15s;}
.btn-reconcile:hover{background:rgba(200,255,0,.22);}
.btn-reconcile.done{background:rgba(74,222,128,.1);color:#4ade80;border-color:rgba(74,222,128,.3);cursor:default;}
/* pending badge on sales/purch rows */
.needs-coll{background:rgba(255,217,61,.1);border-left:3px solid var(--yellow);}
.fully-coll{background:rgba(74,222,128,.05);border-left:3px solid rgba(74,222,128,.3);}
@media print{
  .sidebar,.topbar,.overlay,.export-bar,.btn,.btn-primary,.btn-danger,.btn-ghost{display:none!important;}
  .main{overflow:visible!important;}
  .content{overflow:visible!important;padding:0!important;}
  .page{display:block!important;}
  body{background:#fff!important;color:#000!important;}
  table{border-collapse:collapse!important;}
  th,td{border:1px solid #ccc!important;color:#000!important;background:#fff!important;font-size:11px!important;}
  .rtbl tr.rh td{background:#f0f0f0!important;color:#000!important;}
  .rtbl tr.rt td{background:#e8ffe8!important;color:#000!important;}
  .pos{color:#008000!important;}
  .neg{color:#cc0000!important;}
  .amt{font-family:monospace!important;}
}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════ SIDEBAR ═══ -->
<nav class="sidebar">
  <div class="logo-area">
    <div class="logo-title">FinLedger</div>
    <div class="logo-sub">Accounting System</div>
  </div>

  <div class="nav">
    <div class="nav-sec">Overview</div>
    <div class="nav-item active" onclick="nav('dashboard')"><span class="nav-icon">▦</span>Dashboard</div>

    <div class="nav-sec">Operations</div>
    <div class="nav-item" onclick="nav('contacts')"><span class="nav-icon">👥</span>Contacts</div>
    <div class="nav-item" onclick="nav('sales')"><span class="nav-icon">↑</span>Sales</div>
    <div class="nav-item" onclick="nav('purchases')"><span class="nav-icon">↓</span>Purchases</div>
    <div class="nav-item" onclick="nav('collections')"><span class="nav-icon">◎</span>Collections</div>
    <div class="nav-item" onclick="nav('payments')"><span class="nav-icon">◉</span>Payments</div>
    <div class="nav-item" onclick="nav('journal')"><span class="nav-icon">≡</span>Journal Entries</div>

    <div class="nav-sec">Reports</div>
    <div class="nav-item" onclick="nav('pl')"><span class="nav-icon">◈</span>P&amp;L Statement</div>
    <div class="nav-item" onclick="nav('bs')"><span class="nav-icon">⊞</span>Balance Sheet</div>
    <div class="nav-item" onclick="nav('cf')"><span class="nav-icon">⟳</span>Cash Flow</div>
  </div>

  <!-- USER CARD -->
  <div class="sidebar-foot">
    <div class="user-card" onclick="openSettings('user')" title="Open Settings">
      <div class="user-avatar" id="sideAvatarBg"><span id="sideAvatarInitials">PK</span></div>
      <div class="user-info">
        <div class="user-name" id="sideUserName">Previt Ketsia</div>
        <div class="user-role" id="sideUserRole">Chief Accountant</div>
        <div class="user-co" id="sideUserCo">My Company Ltd.</div>
      </div>
      <div class="user-gear">⚙</div>
    </div>
  </div>
</nav>

<!-- ═══════════════════════════════════════════ MAIN ═══════ -->
<div class="main">
  <!-- TOPBAR -->
  <div class="topbar">
    <div class="topbar-left">
      <div class="page-title" id="pgTitle">Dashboard</div>
      <div class="breadcrumb" id="pgCrumb">FinLedger / Overview</div>
    </div>
    <div class="topbar-right">
      <div class="greeting">Welcome back, <strong id="topGreeting">Previt Ketsia</strong></div>
      <div class="server-badge">● localhost:8765</div>
      <div class="theme-toggle" onclick="toggleTheme()" title="Toggle Dark/Light mode">
        <div class="theme-toggle-track" id="themeTrack"><div class="theme-toggle-thumb"></div></div>
        <span class="theme-toggle-label" id="themeLabel">Dark</span>
      </div>
      <button class="btn btn-ghost" onclick="openSettings('company')">⚙ Settings</button>
    </div>
  </div>

  <!-- CONTENT -->
  <div class="content">

    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="kpi-grid">
        <div class="kpi-card g"><div class="card-title">Total Revenue</div><div class="card-value" id="kpi-rev">€0</div><div class="card-delta">Net sales + adjustments</div></div>
        <div class="kpi-card r"><div class="card-title">Total Expenses</div><div class="card-value" id="kpi-exp">€0</div><div class="card-delta">COGS + OpEx</div></div>
        <div class="kpi-card a"><div class="card-title">Net Income</div><div class="card-value" id="kpi-ni">€0</div><div class="card-delta">Revenue − Expenses</div></div>
        <div class="kpi-card b"><div class="card-title">Cash Position</div><div class="card-value" id="kpi-cash">€0</div><div class="card-delta">Collections − Payments</div></div>
      </div>
      <div class="row">
        <div class="col2">
          <div class="chart-area">
            <div class="sec-hdr"><div><div class="sec-title">Revenue vs Expenses</div><div class="sec-sub">Monthly overview</div></div></div>
            <div class="chart-bars" id="chartBars"><div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:'DM Mono',monospace;">Add transactions to see chart</div></div>
            <div style="display:flex;gap:16px;margin-top:12px;">
              <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text3);"><span style="width:10px;height:10px;background:var(--green);border-radius:2px;display:inline-block;"></span>Revenue</div>
              <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text3);"><span style="width:10px;height:10px;background:var(--red);border-radius:2px;display:inline-block;"></span>Expenses</div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="chart-area" style="height:100%;">
            <div class="card-title">Quick Stats</div>
            <div style="margin-top:16px;display:flex;flex-direction:column;gap:14px;">
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Accounts Receivable</span><span class="badge bb" id="qs-ar">€0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Accounts Payable</span><span class="badge by" id="qs-ap">€0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Sales Invoices</span><span class="badge bg" id="qs-sc">0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Purchase Invoices</span><span class="badge br" id="qs-pc">0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Journal Entries</span><span class="badge ba" id="qs-jec">0</span></div>
              <div style="height:1px;background:var(--border);"></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Net Margin</span><span style="font-family:'DM Mono',monospace;" id="qs-mg">—</span></div>
            </div>
          </div>
        </div>
      </div>
      <div style="margin-top:16px;">
        <div class="chart-area">
          <div class="sec-hdr"><div class="sec-title">Recent Transactions</div><div class="sec-sub">Last 10 entries</div></div>
          <div class="tbl-wrap"><table><thead><tr><th>Date</th><th>Type</th><th>Description</th><th>Party</th><th>Amount</th><th>Status</th></tr></thead><tbody id="recentTx"><tr><td colspan="6" style="text-align:center;color:var(--text3);padding:24px;">No transactions yet.</td></tr></tbody></table></div>
        </div>
      </div>
    </div>

    <!-- ══ CONTACTS ══ -->
    <div class="page" id="page-contacts">
      <div class="sec-hdr">
        <div><div class="sec-title">Contacts</div><div class="sec-sub">Clients &amp; Suppliers directory</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('contacts')" title="Export Excel">📊</button>
          <button class="btn btn-primary" onclick="openContactModal()">+ New Contact</button>
        </div>
      </div>
      <!-- Filter bar -->
      <div style="display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;">
        <input type="text" id="ct-search" placeholder="🔍  Search by name, NIF, email..." style="max-width:300px;" oninput="rContacts()">
        <div class="contact-type-toggle">
          <button class="ct-btn active" id="ctf-all"    onclick="setCtFilter('all')">All</button>
          <button class="ct-btn"        id="ctf-client" onclick="setCtFilter('client')">Clients</button>
          <button class="ct-btn"        id="ctf-supplier" onclick="setCtFilter('supplier')">Suppliers</button>
          <button class="ct-btn"        id="ctf-both"   onclick="setCtFilter('both')">Both</button>
        </div>
        <span id="ct-count" style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;"></span>
      </div>
      <!-- Contacts grid -->
      <div class="contacts-grid" id="contactsGrid">
        <div style="color:var(--text3);font-size:13px;font-family:'DM Mono',monospace;padding:32px;text-align:center;grid-column:1/-1;">
          No contacts yet. Click "+ New Contact" to add your first client or supplier.
        </div>
      </div>
    </div>

    <!-- ══ SALES ══ -->
    <div class="page" id="page-sales">
      <div class="sec-hdr"><div><div class="sec-title">Sales Invoices</div><div class="sec-sub">Record customer invoices</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('sales')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('sales','Sales Invoices')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-sale')">+ New Invoice</button></div></div>
      <div class="totbar">
        <div class="tot-item"><label>Invoiced</label><span id="s-tot" style="color:var(--green);">€0.00</span></div>
        <div class="tot-item"><label>Collected</label><span id="s-coll" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/R</label><span id="s-ar" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>Count</label><span id="s-cnt" style="color:var(--text2);">0</span></div>
      </div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Customer</th><th>Description</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="salesTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ PURCHASES ══ -->
    <div class="page" id="page-purchases">
      <div class="sec-hdr"><div><div class="sec-title">Purchase Invoices</div><div class="sec-sub">Record supplier invoices</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('purchases')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('purchases','Purchase Invoices')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-purch')">+ New Purchase</button></div></div>
      <div class="totbar">
        <div class="tot-item"><label>Purchased</label><span id="p-tot" style="color:var(--red);">€0.00</span></div>
        <div class="tot-item"><label>Paid</label><span id="p-paid" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/P</label><span id="p-ap" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>Count</label><span id="p-cnt" style="color:var(--text2);">0</span></div>
      </div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Supplier</th><th>Description</th><th>Category</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="purchTbl"><tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ COLLECTIONS ══ -->
    <div class="page" id="page-collections">
      <div class="sec-hdr">
        <div><div class="sec-title">Collections</div><div class="sec-sub">Reconcile payments from customers</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('collections')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('collections','Collections')" title="Export PDF">📄</button>
          <button class="btn btn-ghost btn-sm" onclick="openOverlay('ov-coll')">+ Manual Collection</button>
        </div>
      </div>
      <div class="totbar">
        <div class="tot-item"><label>Total Invoiced</label><span id="c-invoiced" style="color:var(--text2);">€0.00</span></div>
        <div class="tot-item"><label>Total Collected</label><span id="c-tot" style="color:var(--green);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/R</label><span id="c-pending" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>This Month</label><span id="c-mth" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Collected</label><span id="c-cnt" style="color:var(--text2);">0</span></div>
      </div>

      <!-- PENDING SALES TO COLLECT -->
      <div style="margin-bottom:16px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Collection — From Sales Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Customer</th><th>Description</th><th>Total</th><th>Collected</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingCollTbl"><tr><td colspan="9" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- COLLECTION HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Collection History</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Date</th><th>Customer</th><th>Invoice Ref</th><th>Method</th><th>Amount</th><th>Notes</th><th></th></tr></thead>
          <tbody id="collTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No collections yet.</td></tr></tbody>
        </table></div></div>
      </div>
    </div>

    <!-- ══ PAYMENTS ══ -->
    <div class="page" id="page-payments">
      <div class="sec-hdr">
        <div><div class="sec-title">Payments</div><div class="sec-sub">Reconcile payments to suppliers</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('payments')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('payments','Payments')" title="Export PDF">📄</button>
          <button class="btn btn-ghost btn-sm" onclick="openOverlay('ov-pay')">+ Manual Payment</button>
        </div>
      </div>
      <div class="totbar">
        <div class="tot-item"><label>Total Purchased</label><span id="py-purchased" style="color:var(--text2);">€0.00</span></div>
        <div class="tot-item"><label>Total Paid</label><span id="py-tot" style="color:var(--red);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/P</label><span id="py-pending" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>This Month</label><span id="py-mth" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Paid</label><span id="py-cnt" style="color:var(--text2);">0</span></div>
      </div>

      <!-- PENDING PURCHASES TO PAY -->
      <div style="margin-bottom:16px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Payment — From Purchase Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Supplier</th><th>Description</th><th>Category</th><th>Total</th><th>Paid</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingPayTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- PAYMENT HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Payment History</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Date</th><th>Supplier</th><th>Invoice Ref</th><th>Method</th><th>Amount</th><th>Notes</th><th></th></tr></thead>
          <tbody id="payTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No payments yet.</td></tr></tbody>
        </table></div></div>
      </div>
    </div>

    <!-- ══ JOURNAL ══ -->
    <div class="page" id="page-journal">
      <div class="sec-hdr"><div><div class="sec-title">Journal Entries</div><div class="sec-sub">Double-entry bookkeeping</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('journal')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('journal','Journal Entries')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-je')">+ New Entry</button></div></div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>Entry #</th><th>Date</th><th>Type</th><th>Description</th><th>Debit Account</th><th>Credit Account</th><th>Amount</th><th></th></tr></thead><tbody id="jeTbl"><tr><td colspan="7" style="text-align:center;color:var(--text3);padding:24px;">No journal entries yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ P&L ══ -->
    <div class="page" id="page-pl">
      <div class="sec-hdr">
        <div><div class="sec-title">Profit &amp; Loss Statement</div><div class="sec-sub">Income statement for the period</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('pl')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('pl','P&amp;L Statement')" title="Export PDF">📄</button>
          <div class="tabs" style="margin-bottom:0;"><div class="tab active" id="pl-det" onclick="plTab('detail')">Detailed</div><div class="tab" id="pl-sum" onclick="plTab('summary')">Summary</div></div>
        </div>
      </div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from" onchange="setDateFilter(this.value, document.getElementById('df-to').value)">
        <label>To</label>
        <input type="date" id="df-to" onchange="setDateFilter(document.getElementById('df-from').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from').value='';document.getElementById('df-to').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="card"><div class="tbl-wrap"><table class="rtbl"><colgroup><col style="width:60%"><col style="width:40%"></colgroup><tbody id="plBody"></tbody></table></div></div>
    </div>

    <!-- ══ BALANCE SHEET ══ -->
    <div class="page" id="page-bs">
      <div class="sec-hdr"><div><div class="sec-title">Balance Sheet</div><div class="sec-sub">Assets, Liabilities &amp; Equity</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('bs')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('bs','Balance Sheet')" title="Export PDF">📄</button></div></div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from2" onchange="setDateFilter(this.value, document.getElementById('df-to2').value)">
        <label>To</label>
        <input type="date" id="df-to2" onchange="setDateFilter(document.getElementById('df-from2').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from2').value='';document.getElementById('df-to2').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge2" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="row">
        <div class="col"><div class="card"><div class="card-title" style="margin-bottom:16px;">Assets</div><table class="rtbl"><tbody id="bsA"></tbody></table></div></div>
        <div class="col"><div class="card"><div class="card-title" style="margin-bottom:16px;">Liabilities &amp; Equity</div><table class="rtbl"><tbody id="bsLE"></tbody></table></div></div>
      </div>
      <div style="margin-top:14px;padding:14px 20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);display:flex;justify-content:space-between;align-items:center;">
        <span style="font-family:'DM Serif Display',serif;font-size:16px;">Balance Check</span>
        <span id="bsChk" style="font-family:'DM Mono',monospace;font-size:13px;"></span>
      </div>
    </div>

    <!-- ══ CASH FLOW ══ -->
    <div class="page" id="page-cf">
      <div class="sec-hdr"><div><div class="sec-title">Cash Flow Statement</div><div class="sec-sub">Cash movements by activity</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('cashflow')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('cf','Cash Flow')" title="Export PDF">📄</button></div></div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from3" onchange="setDateFilter(this.value, document.getElementById('df-to3').value)">
        <label>To</label>
        <input type="date" id="df-to3" onchange="setDateFilter(document.getElementById('df-from3').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from3').value='';document.getElementById('df-to3').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge3" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="card"><table class="rtbl"><tbody id="cfBody"></tbody></table></div>
    </div>

  </div><!-- /content -->
</div><!-- /main -->


<!-- ═══════════════════════ OPERATION MODALS ═══════════════════════ -->

<!-- SALE -->
<div class="overlay" id="ov-sale">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">New Sales Invoice</div><div class="mclose" onclick="closeOverlay('ov-sale')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="s-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="s-num" placeholder="INV-001"></div>
        <div class="fg full"><label>Customer</label>
          <div class="autocomplete-wrap">
            <div style="display:flex;gap:6px;">
              <input type="text" id="s-cust" placeholder="Type to search contacts..." autocomplete="off" oninput="acSearch('s-cust','s-cust-list','client')" onfocus="acSearch('s-cust','s-cust-list','client')" onblur="setTimeout(function(){closeAC('s-cust-list')},200)" style="flex:1;">
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('client')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="s-cust-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="s-desc" placeholder="e.g. Consulting services Q1"></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="s-net" placeholder="0.00" step="0.01" oninput="calcS()"></div>
        <div class="fg"><label>VAT Rate</label><select id="s-vat" onchange="calcS()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="s-va" readonly style="background:var(--surface3);"></div>
        <div class="fg"><label>Total (€)</label><input type="text" id="s-tot2" readonly style="background:var(--surface3);color:var(--accent);font-family:'DM Mono',monospace;font-weight:600;"></div>
        <div class="fg"><label>Status</label><select id="s-stat"><option value="pending">Pending</option><option value="paid">Paid</option><option value="partial">Partial</option></select></div>
        <div class="fg"><label>Payment Method</label><select id="s-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-sale')">Cancel</button><button class="btn btn-primary" onclick="saveSale()">Save Invoice</button></div>
  </div>
</div>

<!-- PURCHASE -->
<div class="overlay" id="ov-purch">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">New Purchase Invoice</div><div class="mclose" onclick="closeOverlay('ov-purch')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="p-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="p-num" placeholder="PINV-001"></div>
        <div class="fg full"><label>Supplier</label>
          <div class="autocomplete-wrap">
            <div style="display:flex;gap:6px;">
              <input type="text" id="p-sup" placeholder="Type to search contacts..." autocomplete="off" oninput="acSearch('p-sup','p-sup-list','supplier')" onfocus="acSearch('p-sup','p-sup-list','supplier')" onblur="setTimeout(function(){closeAC('p-sup-list')},200)" style="flex:1;">
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('supplier')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="p-sup-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="p-desc" placeholder="e.g. Office rent March"></div>
        <div class="fg"><label>Category</label><select id="p-cat"><option value="COGS">Cost of Goods Sold</option><option value="Rent">Rent</option><option value="Salaries">Salaries</option><option value="Utilities">Utilities</option><option value="Marketing">Marketing</option><option value="Professional">Professional Services</option><option value="Depreciation">Depreciation</option><option value="Other OpEx">Other OpEx</option></select></div>
        <div class="fg"><label>VAT Rate</label><select id="p-vat" onchange="calcP()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="p-net" placeholder="0.00" step="0.01" oninput="calcP()"></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="p-va" readonly style="background:var(--surface3);"></div>
        <div class="fg full"><label>Total (€)</label><input type="text" id="p-tot2" readonly style="background:var(--surface3);color:var(--red);font-family:'DM Mono',monospace;font-weight:600;"></div>
        <div class="fg"><label>Status</label><select id="p-stat"><option value="pending">Pending</option><option value="paid">Paid</option></select></div>
        <div class="fg"><label>Payment Method</label><select id="p-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-purch')">Cancel</button><button class="btn btn-primary" onclick="savePurch()">Save Purchase</button></div>
  </div>
</div>

<!-- COLLECTION -->
<div class="overlay" id="ov-coll">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Collection</div><div class="mclose" onclick="closeOverlay('ov-coll')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="c-date"></div>
        <div class="fg"><label>Customer</label><input type="text" id="c-cust" placeholder="Customer name"></div>
        <div class="fg"><label>Invoice Ref</label><input type="text" id="c-ref" placeholder="INV-001"></div>
        <div class="fg"><label>Method</label><select id="c-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
        <div class="fg full"><label>Amount Received (€)</label><input type="number" id="c-amt" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><textarea id="c-notes" placeholder="Optional..."></textarea></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-coll')">Cancel</button><button class="btn btn-primary" onclick="saveColl()">Save</button></div>
  </div>
</div>

<!-- PAYMENT -->
<div class="overlay" id="ov-pay">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Payment</div><div class="mclose" onclick="closeOverlay('ov-pay')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="py-date"></div>
        <div class="fg"><label>Supplier</label><input type="text" id="py-sup" placeholder="Supplier name"></div>
        <div class="fg"><label>Invoice Ref</label><input type="text" id="py-ref" placeholder="PINV-001"></div>
        <div class="fg"><label>Method</label><select id="py-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
        <div class="fg full"><label>Amount Paid (€)</label><input type="number" id="py-amt" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><textarea id="py-notes" placeholder="Optional..."></textarea></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-pay')">Cancel</button><button class="btn btn-primary" onclick="savePay()">Save</button></div>
  </div>
</div>

<!-- JOURNAL ENTRY -->
<div class="overlay" id="ov-je">
  <div class="modal wide">
    <div class="mhdr"><div class="mtitle">New Journal Entry</div><div class="mclose" onclick="closeOverlay('ov-je')">✕</div></div>
    <div class="mbody">
      <div class="fgrid" style="margin-bottom:20px;">
        <div class="fg"><label>Date</label><input type="date" id="j-date"></div>
        <div class="fg full"><label>Description</label><input type="text" id="j-desc" placeholder="e.g. Depreciation charge Q1"></div>
      </div>
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:10px;margin-bottom:6px;">
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Account</span>
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Debit (€)</span>
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Credit (€)</span>
        <span></span>
      </div>
      <div id="jeLines"></div>
      <button class="btn btn-ghost btn-sm" style="margin-top:8px;" onclick="addJELine()">+ Add Line</button>
      <div style="display:flex;gap:20px;padding:12px 14px;background:var(--surface2);border-radius:7px;margin-top:12px;">
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">DEBIT</span><span id="je-td" style="font-family:'DM Mono',monospace;color:var(--green);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">CREDIT</span><span id="je-tc" style="font-family:'DM Mono',monospace;color:var(--red);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">STATUS</span><span id="je-st" style="font-family:'DM Mono',monospace;">—</span></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-je')">Cancel</button><button class="btn btn-primary" onclick="saveJE()">Post Entry</button></div>
  </div>
</div>


<!-- ═══════════════════════ SETTINGS MODAL ═══════════════════════════ -->
<div class="overlay" id="ov-settings">
  <div class="modal xwide">
    <div class="mhdr">
      <div class="mtitle">Settings &amp; Parametrization</div>
      <div class="mclose" onclick="closeOverlay('ov-settings')">✕</div>
    </div>
    <div class="mbody">
      <!-- SETTINGS TABS -->
      <div class="set-tabs">
        <div class="set-tab active" id="stab-user" onclick="setTab('user')">👤 User Profile</div>
        <div class="set-tab" id="stab-company" onclick="setTab('company')">🏢 Company</div>
        <div class="set-tab" id="stab-prefs" onclick="setTab('prefs')">🎨 Preferences</div>
        <div class="set-tab" id="stab-data" onclick="setTab('data')">🗃 Data</div>
      </div>

      <!-- ── USER PROFILE PANEL ── -->
      <div class="set-panel active" id="spanel-user">
        <div class="set-section-label">Profile Photo &amp; Name</div>
        <div class="avatar-row">
          <div class="avatar-big" id="previewAvatar" style="background:#c8ff00;">PK</div>
          <div>
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Avatar Color</div>
            <div class="color-swatches" id="colorSwatches"></div>
          </div>
        </div>
        <div class="fgrid" style="margin-top:18px;">
          <div class="fg"><label>First Name</label><input type="text" id="u-fname" placeholder="Previt" oninput="livePreviewUser()"></div>
          <div class="fg"><label>Last Name</label><input type="text" id="u-lname" placeholder="Ketsia" oninput="livePreviewUser()"></div>
          <div class="fg full"><label>Job Title / Role</label><input type="text" id="u-role" placeholder="e.g. Chief Accountant, CFO, Finance Manager"></div>
          <div class="fg full"><label>Email Address</label><input type="email" id="u-email" placeholder="previt.ketsia@company.com"></div>
          <div class="fg full"><label>Phone (optional)</label><input type="text" id="u-phone" placeholder="+1 234 567 890"></div>
        </div>
      </div>

      <!-- ── COMPANY PANEL ── -->
      <div class="set-panel" id="spanel-company">
        <div class="set-section-label">Company Information</div>
        <div class="fgrid">
          <div class="fg full"><label>Company Name</label><input type="text" id="set-co" placeholder="My Company Ltd."></div>
          <div class="fg"><label>Tax ID / VAT Number</label><input type="text" id="set-taxid" placeholder="ES-B12345678"></div>
          <div class="fg"><label>Industry</label><select id="set-industry"><option value="">— Select —</option><option>Consulting</option><option>Retail</option><option>Manufacturing</option><option>Technology</option><option>Healthcare</option><option>Real Estate</option><option>Finance</option><option>Other</option></select></div>
          <div class="fg full"><label>Address</label><input type="text" id="set-addr" placeholder="123 Main Street, City, Country"></div>
          <div class="fg"><label>Fiscal Year Start</label><select id="set-fystart"><option value="Jan">January</option><option value="Apr">April</option><option value="Jul">July</option><option value="Oct">October</option></select></div>
          <div class="fg"><label>Fiscal Year</label><input type="text" id="set-fy" placeholder="2025"></div>
          <div class="fg"><label>Currency Symbol</label><input type="text" id="set-cur" placeholder="€" maxlength="3"></div>
          <div class="fg"><label>Default VAT Rate (%)</label><select id="set-defvat"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        </div>
      </div>

      <!-- ── PREFERENCES PANEL ── -->
      <div class="set-panel" id="spanel-prefs">
        <div class="set-section-label">Display &amp; Interface</div>
        <div class="fgrid">
          <div class="fg"><label>Date Format</label><select id="set-datefmt"><option value="DD/MM/YYYY">DD/MM/YYYY</option><option value="MM/DD/YYYY">MM/DD/YYYY</option><option value="YYYY-MM-DD">YYYY-MM-DD</option></select></div>
          <div class="fg"><label>Number Format</label><select id="set-numfmt"><option value="eu">1.234,56 (European)</option><option value="us">1,234.56 (US/UK)</option></select></div>
          <div class="fg"><label>Language</label><select id="set-lang"><option value="en">English</option><option value="fr">Français</option><option value="es">Español</option><option value="de">Deutsch</option><option value="it">Italiano</option></select></div>
          <div class="fg"><label>Theme Mode</label>
            <select id="set-theme">
              <option value="dark">🌙 Dark Mode (default)</option>
              <option value="light">☀️ Light Mode</option>
            </select>
          </div>
        </div>
        <div class="divider"></div>
        <div class="set-section-label">Invoice Defaults</div>
        <div class="fgrid">
          <div class="fg full"><label>Default Invoice Notes / Footer</label><textarea id="set-invnotes" placeholder="e.g. Payment due within 30 days. Thank you for your business."></textarea></div>
          <div class="fg"><label>Invoice Prefix</label><input type="text" id="set-invpfx" placeholder="INV-" maxlength="10"></div>
          <div class="fg"><label>Purchase Prefix</label><input type="text" id="set-purpfx" placeholder="PINV-" maxlength="10"></div>
        </div>
      </div>

      <!-- ── DATA PANEL ── -->
      <div class="set-panel" id="spanel-data">
        <div class="set-section-label">Session Summary</div>
        <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:20px;">
          <div class="info-row"><span class="info-label">Sales Invoices</span><span class="info-val" id="di-sales">0</span></div>
          <div class="info-row"><span class="info-label">Purchase Invoices</span><span class="info-val" id="di-purch">0</span></div>
          <div class="info-row"><span class="info-label">Collections</span><span class="info-val" id="di-coll">0</span></div>
          <div class="info-row"><span class="info-label">Payments</span><span class="info-val" id="di-pay">0</span></div>
          <div class="info-row"><span class="info-label">Journal Entries</span><span class="info-val" id="di-je">0</span></div>
          <div class="info-row"><span class="info-label">Storage Used</span><span class="info-val" id="di-size">—</span></div>
        </div>
        <div class="set-section-label">Danger Zone</div>
        <div style="background:rgba(248,113,113,.06);border:1px solid rgba(248,113,113,.2);border-radius:8px;padding:16px;display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-weight:600;font-size:13px;color:var(--red);margin-bottom:4px;">Clear All Transaction Data</div>
            <div style="font-size:12px;color:var(--text3);">Permanently deletes all invoices, payments, and journal entries. Settings are preserved.</div>
          </div>
          <button class="btn btn-danger btn-sm" onclick="clearAll()" style="flex-shrink:0;margin-left:16px;">Clear Data</button>
        </div>
      </div>

    </div><!-- /mbody -->
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-settings')">Cancel</button>
      <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════ JAVASCRIPT ═══════════════════════ -->
<script>
// ── STATE ──────────────────────────────────────────────────────────────────
var DB={
  user:{fname:'Previt',lname:'Ketsia',role:'Chief Accountant',email:'',phone:'',avatarColor:'#c8ff00'},
  co:{name:'My Company Ltd.',taxid:'',industry:'',addr:'',fy:'2025',fystart:'Jan',cur:'€',defvat:'21'},
  prefs:{datefmt:'DD/MM/YYYY',numfmt:'us',lang:'en',accent:'#c8ff00',invnotes:'',invpfx:'INV-',purpfx:'PINV-'},
  sales:[],purch:[],coll:[],pay:[],je:[],
  contacts:[],
  ids:{s:1,p:1,c:1,py:1,j:1,ct:1}
};
var plMode='detail';
var AVATAR_COLORS=['#c8ff00','#00d4ff','#a78bfa','#fb923c','#f472b6','#34d399','#ffd93d','#f87171','#60a5fa'];
var COA=[
  {c:'1000',n:'Cash & Bank',t:'asset'},{c:'1100',n:'Accounts Receivable',t:'asset'},
  {c:'1200',n:'Inventory',t:'asset'},{c:'1300',n:'Prepaid Expenses',t:'asset'},
  {c:'1500',n:'Fixed Assets',t:'asset'},{c:'1510',n:'Accum. Depreciation',t:'asset'},
  {c:'2000',n:'Accounts Payable',t:'liability'},{c:'2100',n:'VAT Payable',t:'liability'},
  {c:'2200',n:'Accrued Liabilities',t:'liability'},{c:'2500',n:'Long-term Debt',t:'liability'},
  {c:'3000',n:'Share Capital',t:'equity'},{c:'3100',n:'Retained Earnings',t:'equity'},
  {c:'4000',n:'Sales Revenue',t:'revenue'},{c:'4100',n:'Other Revenue',t:'revenue'},
  {c:'5000',n:'Cost of Goods Sold',t:'expense'},{c:'6000',n:'Salaries & Wages',t:'expense'},
  {c:'6100',n:'Rent',t:'expense'},{c:'6200',n:'Utilities',t:'expense'},
  {c:'6300',n:'Marketing',t:'expense'},{c:'6400',n:'Professional Services',t:'expense'},
  {c:'6500',n:'Depreciation',t:'expense'},{c:'6900',n:'Other OpEx',t:'expense'},
  {c:'7000',n:'Interest Expense',t:'expense'},{c:'7100',n:'Tax Expense',t:'expense'}
];

// ── PERSISTENCE  (saves to disk via Python server) ──────────────────────────
function sv(){
  try{
    fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)});
  }catch(e){}
  // fallback: also keep in localStorage
  try{localStorage.setItem('fl_v4',JSON.stringify(DB));}catch(e){}
}
function ld(){
  var xhr=new XMLHttpRequest();
  xhr.open('GET','/load',false);
  xhr.send();
  if(xhr.status===200){
    try{
      var parsed=JSON.parse(xhr.responseText);
      if(parsed && parsed.ids) DB=parsed;
    }catch(e){}
  } else {
    try{var r=localStorage.getItem('fl_v4');if(r){var p=JSON.parse(r);if(p&&p.ids)DB=p;}}catch(e){}
  }
  // Ensure new fields exist for backward compatibility
  if(!DB.contacts)  DB.contacts = [];
  if(!DB.ids.ct)    DB.ids.ct   = 1;
}

// ── FORMAT ─────────────────────────────────────────────────────────────────
function f(n){return(DB.co.cur||'€')+Number(n||0).toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2});}
function td(){return new Date().toISOString().split('T')[0];}
function ym(){var n=new Date();return n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0');}
function initials(fn,ln){return((fn||'?')[0]+(ln||'?')[0]).toUpperCase();}
function fullName(){return((DB.user.fname||'')+' '+(DB.user.lname||'')).trim()||'User';}

// ── INIT ───────────────────────────────────────────────────────────────────
function init(){
  ld();
  buildColorSwatches();
  applyAccent();
  applyTranslations();
  updateUserUI();
  setDates();
  initJE();
  renderAll();
}
function setDates(){var t=td();['s-date','p-date','c-date','py-date','j-date'].forEach(function(id){var e=document.getElementById(id);if(e)e.value=t;});}

// ── ACCENT COLOR ───────────────────────────────────────────────────────────
function applyAccent(){
  // Apply theme (dark/light)
  var theme = DB.prefs.theme || 'dark';
  document.body.classList.toggle('light-mode', theme === 'light');
  var track = document.getElementById('themeTrack');
  var label = document.getElementById('themeLabel');
  if(track) track.classList.toggle('on', theme === 'light');
  if(label) label.textContent = theme === 'light' ? 'Light' : 'Dark';
  // Accent color
  var acc = theme === 'light' ? '#0057ff' : (DB.prefs.accent||'#c8ff00');
  document.documentElement.style.setProperty('--accent', acc);
  var r=parseInt(acc.slice(1,3),16),g=parseInt(acc.slice(3,5),16),b=parseInt(acc.slice(5,7),16);
  var lum=(0.299*r+0.587*g+0.114*b)/255;
  var fgColor=lum>0.5?'#0f0f11':'#f0f0f4';
  document.querySelectorAll('.user-avatar,.avatar-big').forEach(function(el){el.style.color=fgColor;});
}

function toggleTheme(){
  DB.prefs.theme = (DB.prefs.theme === 'light') ? 'dark' : 'light';
  sv(); applyAccent();
}

// ── USER UI ────────────────────────────────────────────────────────────────
function updateUserUI(){
  var fn=fullName(),ini=initials(DB.user.fname,DB.user.lname);
  var ac=DB.user.avatarColor||DB.prefs.accent||'#c8ff00';
  // Sidebar
  document.getElementById('sideAvatarInitials').textContent=ini;
  document.getElementById('sideAvatarBg').style.background=ac;
  document.getElementById('sideUserName').textContent=fn;
  document.getElementById('sideUserRole').textContent=DB.user.role||'Accountant';
  document.getElementById('sideUserCo').textContent=DB.co.name||'My Company';
  // Topbar
  document.getElementById('topGreeting').textContent=DB.user.fname||fn;
  // Title
  document.title='FinLedger — '+fn;
}

// ── COLOUR SWATCHES ────────────────────────────────────────────────────────
function buildColorSwatches(){
  var wrap=document.getElementById('colorSwatches');
  wrap.innerHTML='';
  AVATAR_COLORS.forEach(function(col){
    var d=document.createElement('div');
    d.className='swatch'+(col===(DB.user.avatarColor||'#c8ff00')?' sel':'');
    d.style.background=col;
    d.title=col;
    d.onclick=function(){
      document.querySelectorAll('.swatch').forEach(function(s){s.classList.remove('sel');});
      d.classList.add('sel');
      DB.user.avatarColor=col;
      var pv=document.getElementById('previewAvatar');
      pv.style.background=col;
      var r2=parseInt(col.slice(1,3),16),g2=parseInt(col.slice(3,5),16),b2=parseInt(col.slice(5,7),16);
      var l=(0.299*r2+0.587*g2+0.114*b2)/255;
      pv.style.color=l>0.5?'#0f0f11':'#f0f0f4';
      livePreviewUser();
    };
    wrap.appendChild(d);
  });
}

function livePreviewUser(){
  var fn=document.getElementById('u-fname').value||'?';
  var ln=document.getElementById('u-lname').value||'?';
  document.getElementById('previewAvatar').textContent=initials(fn,ln);
}

// ── NAVIGATION ─────────────────────────────────────────────────────────────
var titles={dashboard:'Dashboard',contacts:'Contacts',sales:'Sales Invoices',purchases:'Purchase Invoices',collections:'Collections',payments:'Payments',journal:'Journal Entries',pl:'P&L Statement',bs:'Balance Sheet',cf:'Cash Flow Statement'};
var crumbs={dashboard:'FinLedger / Overview',contacts:'FinLedger / Operations / Contacts',sales:'FinLedger / Operations / Sales',purchases:'FinLedger / Operations / Purchases',collections:'FinLedger / Operations / Collections',payments:'FinLedger / Operations / Payments',journal:'FinLedger / Operations / Journal',pl:'FinLedger / Reports / P&L',bs:'FinLedger / Reports / Balance Sheet',cf:'FinLedger / Reports / Cash Flow'};
function nav(p){
  document.querySelectorAll('.page').forEach(function(e){e.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(e){e.classList.remove('active');});
  document.getElementById('page-'+p).classList.add('active');
  var ni=document.querySelector('[onclick="nav(\''+p+'\')"]');if(ni)ni.classList.add('active');
  document.getElementById('pgTitle').textContent=titles[p]||p;
  document.getElementById('pgCrumb').textContent=crumbs[p]||'';
  renderAll();
}

// ── OVERLAYS ───────────────────────────────────────────────────────────────
function openOverlay(id){document.getElementById(id).classList.add('open');setDates();}
function closeOverlay(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.overlay').forEach(function(ov){
  ov.addEventListener('click',function(e){if(e.target===ov)ov.classList.remove('open');});
});

// ── SETTINGS TABS ──────────────────────────────────────────────────────────
function openSettings(tab){
  // Populate fields before opening
  document.getElementById('u-fname').value=DB.user.fname||'';
  document.getElementById('u-lname').value=DB.user.lname||'';
  document.getElementById('u-role').value=DB.user.role||'';
  document.getElementById('u-email').value=DB.user.email||'';
  document.getElementById('u-phone').value=DB.user.phone||'';
  var pv=document.getElementById('previewAvatar');
  var ac=DB.user.avatarColor||'#c8ff00';
  pv.style.background=ac;pv.textContent=initials(DB.user.fname,DB.user.lname);
  var r2=parseInt(ac.slice(1,3),16),g2=parseInt(ac.slice(3,5),16),b2=parseInt(ac.slice(5,7),16);
  pv.style.color=((0.299*r2+0.587*g2+0.114*b2)/255)>0.5?'#0f0f11':'#f0f0f4';
  buildColorSwatches();
  // Company
  document.getElementById('set-co').value=DB.co.name||'';
  document.getElementById('set-taxid').value=DB.co.taxid||'';
  document.getElementById('set-industry').value=DB.co.industry||'';
  document.getElementById('set-addr').value=DB.co.addr||'';
  document.getElementById('set-fy').value=DB.co.fy||'2025';
  document.getElementById('set-fystart').value=DB.co.fystart||'Jan';
  document.getElementById('set-cur').value=DB.co.cur||'€';
  document.getElementById('set-defvat').value=DB.co.defvat||'21';
  // Prefs
  document.getElementById('set-datefmt').value=DB.prefs.datefmt||'DD/MM/YYYY';
  document.getElementById('set-numfmt').value=DB.prefs.numfmt||'us';
  document.getElementById('set-lang').value=DB.prefs.lang||'en';
  document.getElementById('set-theme').value=DB.prefs.theme||'dark';
  document.getElementById('set-invnotes').value=DB.prefs.invnotes||'';
  document.getElementById('set-invpfx').value=DB.prefs.invpfx||'INV-';
  document.getElementById('set-purpfx').value=DB.prefs.purpfx||'PINV-';
  // Data stats
  document.getElementById('di-sales').textContent=DB.sales.length;
  document.getElementById('di-purch').textContent=DB.purch.length;
  document.getElementById('di-coll').textContent=DB.coll.length;
  document.getElementById('di-pay').textContent=DB.pay.length;
  document.getElementById('di-je').textContent=DB.je.length;
  var raw=localStorage.getItem('fl_v4')||'';
  document.getElementById('di-size').textContent=(raw.length/1024).toFixed(1)+' KB';
  setTab(tab||'user');
  openOverlay('ov-settings');
}

function setTab(t){
  ['user','company','prefs','data'].forEach(function(n){
    document.getElementById('stab-'+n).classList.toggle('active',n===t);
    document.getElementById('spanel-'+n).classList.toggle('active',n===t);
  });
}

function saveSettings(){
  // User
  DB.user.fname=document.getElementById('u-fname').value||'User';
  DB.user.lname=document.getElementById('u-lname').value||'';
  DB.user.role=document.getElementById('u-role').value||'Accountant';
  DB.user.email=document.getElementById('u-email').value||'';
  DB.user.phone=document.getElementById('u-phone').value||'';
  // Company
  DB.co.name=document.getElementById('set-co').value||'My Company Ltd.';
  DB.co.taxid=document.getElementById('set-taxid').value||'';
  DB.co.industry=document.getElementById('set-industry').value||'';
  DB.co.addr=document.getElementById('set-addr').value||'';
  DB.co.fy=document.getElementById('set-fy').value||'2025';
  DB.co.fystart=document.getElementById('set-fystart').value||'Jan';
  DB.co.cur=document.getElementById('set-cur').value||'€';
  DB.co.defvat=document.getElementById('set-defvat').value||'21';
  // Prefs
  DB.prefs.datefmt=document.getElementById('set-datefmt').value;
  DB.prefs.numfmt=document.getElementById('set-numfmt').value;
  DB.prefs.lang=document.getElementById('set-lang').value;
  DB.prefs.theme=document.getElementById('set-theme').value;
  DB.prefs.invnotes=document.getElementById('set-invnotes').value;
  DB.prefs.invpfx=document.getElementById('set-invpfx').value||'INV-';
  DB.prefs.purpfx=document.getElementById('set-purpfx').value||'PINV-';
  sv();applyAccent();applyTranslations();updateUserUI();closeOverlay('ov-settings');renderAll();
}

function clearAll(){
  if(!confirm('Delete ALL transaction data?\n\nThis action is permanent and cannot be undone.\nYour settings and user profile will be preserved.'))return;
  DB.sales=[];DB.purch=[];DB.coll=[];DB.pay=[];DB.je=[];DB.ids={s:1,p:1,c:1,py:1,j:1};
  sv();closeOverlay('ov-settings');renderAll();
}

// ── CALC HELPERS ───────────────────────────────────────────────────────────
function calcS(){var n=parseFloat(document.getElementById('s-net').value)||0,v=parseFloat(document.getElementById('s-vat').value)||0,va=n*v/100;document.getElementById('s-va').value=va.toFixed(2);document.getElementById('s-tot2').value=(n+va).toFixed(2);}
function calcP(){var n=parseFloat(document.getElementById('p-net').value)||0,v=parseFloat(document.getElementById('p-vat').value)||0,va=n*v/100;document.getElementById('p-va').value=va.toFixed(2);document.getElementById('p-tot2').value=(n+va).toFixed(2);}

// ── SAVE OPERATIONS ────────────────────────────────────────────────────────
function saveSale(){
  var net=parseFloat(document.getElementById('s-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('s-vat').value)||0,va=net*vat/100,stat=document.getElementById('s-stat').value,meth=document.getElementById('s-meth').value,dt=document.getElementById('s-date').value;
  var pfx=DB.prefs.invpfx||'INV-';
  var num=document.getElementById('s-num').value||(pfx+String(DB.ids.s).padStart(3,'0'));
  var cust=document.getElementById('s-cust').value||'Unknown',desc=document.getElementById('s-desc').value;
  var rec={id:DB.ids.s++,date:dt,num:num,customer:cust,desc:desc,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth};
  DB.sales.push(rec);
  // Auto JE: Dr Accounts Receivable / Cr Sales Revenue (+ VAT Payable if applicable)
  var saleLines = [
    {account:'1100', debit:rec.total, credit:0},   // Dr Accounts Receivable (total incl VAT)
    {account:'4000', debit:0, credit:net}            // Cr Sales Revenue (net)
  ];
  if(va > 0) saleLines.push({account:'2100', debit:0, credit:va}); // Cr VAT Payable
  DB.je.push({id:DB.ids.j++,date:dt,desc:'Sale — '+cust+' / '+num,lines:saleLines,amount:rec.total,auto:true,sourceType:'sale',sourceId:rec.id});
  // If paid immediately, also create collection + cash JE
  if(stat==='paid'){
    DB.coll.push({id:DB.ids.c++,date:dt,customer:cust,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Collection — '+cust+' / '+num,lines:[{account:'1000',debit:rec.total,credit:0},{account:'1100',debit:0,credit:rec.total}],amount:rec.total,auto:true,sourceType:'collection'});
  }
  sv();closeOverlay('ov-sale');['s-num','s-cust','s-desc','s-net','s-va','s-tot2'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function savePurch(){
  var net=parseFloat(document.getElementById('p-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('p-vat').value)||0,va=net*vat/100,stat=document.getElementById('p-stat').value,meth=document.getElementById('p-meth').value,dt=document.getElementById('p-date').value;
  var pfx=DB.prefs.purpfx||'PINV-';
  var num=document.getElementById('p-num').value||(pfx+String(DB.ids.p).padStart(3,'0'));
  var sup=document.getElementById('p-sup').value||'Unknown',desc=document.getElementById('p-desc').value,cat=document.getElementById('p-cat').value;
  var rec={id:DB.ids.p++,date:dt,num:num,supplier:sup,desc:desc,cat:cat,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth};
  DB.purch.push(rec);
  // Auto JE: Dr Expense / Cr Accounts Payable (+ VAT deductible)
  var catAccMap={'COGS':'5000','Rent':'6100','Salaries':'6000','Utilities':'6200','Marketing':'6300','Professional':'6400','Depreciation':'6500','Other OpEx':'6900'};
  var expAcc = catAccMap[cat] || '6900';
  var purchLines = [
    {account:expAcc, debit:net,  credit:0},         // Dr Expense account (net)
    {account:'2000', debit:0,    credit:rec.total}   // Cr Accounts Payable (total incl VAT)
  ];
  if(va > 0) purchLines.splice(1, 0, {account:'2100', debit:va, credit:0}); // Dr VAT deductible
  DB.je.push({id:DB.ids.j++,date:dt,desc:'Purchase — '+sup+' / '+num,lines:purchLines,amount:rec.total,auto:true,sourceType:'purchase',sourceId:rec.id});
  // If paid immediately
  if(stat==='paid'){
    DB.pay.push({id:DB.ids.py++,date:dt,supplier:sup,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Payment — '+sup+' / '+num,lines:[{account:'2000',debit:rec.total,credit:0},{account:'1000',debit:0,credit:rec.total}],amount:rec.total,auto:true,sourceType:'payment'});
  }
  sv();closeOverlay('ov-purch');['p-num','p-sup','p-desc','p-net','p-va','p-tot2'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function saveColl(){
  var amt=parseFloat(document.getElementById('c-amt').value)||0;if(!amt){alert('Enter amount.');return;}
  DB.coll.push({id:DB.ids.c++,date:document.getElementById('c-date').value,customer:document.getElementById('c-cust').value||'Unknown',ref:document.getElementById('c-ref').value,method:document.getElementById('c-meth').value,amount:amt,notes:document.getElementById('c-notes').value});
  sv();closeOverlay('ov-coll');['c-cust','c-ref','c-amt','c-notes'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function savePay(){
  var amt=parseFloat(document.getElementById('py-amt').value)||0;if(!amt){alert('Enter amount.');return;}
  DB.pay.push({id:DB.ids.py++,date:document.getElementById('py-date').value,supplier:document.getElementById('py-sup').value||'Unknown',ref:document.getElementById('py-ref').value,method:document.getElementById('py-meth').value,amount:amt,notes:document.getElementById('py-notes').value});
  sv();closeOverlay('ov-pay');['py-sup','py-ref','py-amt','py-notes'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}

// ── JOURNAL ────────────────────────────────────────────────────────────────
function coaOpts(){return COA.map(function(a){return '<option value="'+a.c+'">'+a.c+' – '+a.n+'</option>';}).join('');}
function initJE(){document.getElementById('jeLines').innerHTML='';addJELine();addJELine();}
function addJELine(){
  var d=document.createElement('div');d.className='je-line';
  d.innerHTML='<select class="je-ac"><option value="">-- Account --</option>'+coaOpts()+'</select><input type="number" class="je-dr" placeholder="0.00" step="0.01" oninput="calcJEB()"><input type="number" class="je-cr" placeholder="0.00" step="0.01" oninput="calcJEB()"><button class="btn btn-ghost btn-sm" onclick="rmJELine(this)">✕</button>';
  document.getElementById('jeLines').appendChild(d);
}
function rmJELine(b){if(document.querySelectorAll('.je-line').length<=2)return;b.parentElement.remove();calcJEB();}
function calcJEB(){
  var d=0,c=0;
  document.querySelectorAll('.je-dr').forEach(function(i){d+=parseFloat(i.value)||0;});
  document.querySelectorAll('.je-cr').forEach(function(i){c+=parseFloat(i.value)||0;});
  document.getElementById('je-td').textContent=f(d);document.getElementById('je-tc').textContent=f(c);
  var st=document.getElementById('je-st');
  if(Math.abs(d-c)<0.01&&d>0){st.textContent='✓ Balanced';st.style.color='var(--green)';}
  else{st.textContent='Δ '+f(Math.abs(d-c));st.style.color='var(--red)';}
}
function saveJE(){
  var lines=[],td2=0,tc2=0;
  document.querySelectorAll('#jeLines .je-line').forEach(function(row){
    var a=row.querySelector('.je-ac').value,d=parseFloat(row.querySelector('.je-dr').value)||0,c=parseFloat(row.querySelector('.je-cr').value)||0;
    if(a){lines.push({account:a,debit:d,credit:c});td2+=d;tc2+=c;}
  });
  if(lines.length<2){alert('Enter at least 2 lines.');return;}
  if(Math.abs(td2-tc2)>0.01){alert('Not balanced. Debits must equal Credits.');return;}
  DB.je.push({id:DB.ids.j++,date:document.getElementById('j-date').value,desc:document.getElementById('j-desc').value||'Journal Entry',lines:lines,amount:td2});
  sv();closeOverlay('ov-je');document.getElementById('j-desc').value='';initJE();renderAll();
}

// ── DELETE ─────────────────────────────────────────────────────────────────
function delS(id){if(!confirm('Delete this invoice?'))return;DB.sales=DB.sales.filter(function(x){return x.id!==id;});sv();renderAll();}
function delP(id){if(!confirm('Delete this invoice?'))return;DB.purch=DB.purch.filter(function(x){return x.id!==id;});sv();renderAll();}
function delC(id){if(!confirm('Delete?'))return;DB.coll=DB.coll.filter(function(x){return x.id!==id;});sv();renderAll();}
function delPy(id){if(!confirm('Delete?'))return;DB.pay=DB.pay.filter(function(x){return x.id!==id;});sv();renderAll();}
function delJ(id){if(!confirm('Delete entry?'))return;DB.je=DB.je.filter(function(x){return x.id!==id;});sv();renderAll();}

// ── HELPERS ────────────────────────────────────────────────────────────────
function bdg(s){var m={paid:'bg',pending:'by',partial:'bb',received:'bg',posted:'bp'};return '<span class="badge '+(m[s]||'bb')+'">'+s+'</span>';}
function mth(m){return{bank:'🏦 Bank',cash:'💵 Cash',card:'💳 Card',other:'📋 Other'}[m]||m;}

// ── COMPUTE FINANCIALS ─────────────────────────────────────────────────────
// Active date filter state
var _dateFrom = '', _dateTo = '';

// ── TRANSLATIONS ────────────────────────────────────────────────────────────
var T = {
  en:{
    dashboard:'Dashboard',contacts:'Contacts',sales:'Sales',purchases:'Purchases',
    collections:'Collections',payments:'Payments',journal:'Journal Entries',
    pl:'P&L Statement',bs:'Balance Sheet',cf:'Cash Flow',settings:'Settings',
    newInvoice:'+ New Invoice',newPurchase:'+ New Purchase',newCollection:'+ Record Collection',
    newPayment:'+ Record Payment',newEntry:'+ New Entry',newContact:'+ New Contact',
    overview:'Overview',operations:'Operations',reports:'Reports',
    totalRevenue:'Total Revenue',totalExpenses:'Total Expenses',netIncome:'Net Income',
    cashPosition:'Cash Position',accountsReceivable:'Accounts Receivable',
    accountsPayable:'Accounts Payable',salesInvoices:'Sales Invoices',
    purchaseInvoices:'Purchase Invoices',netMargin:'Net Margin',
    recentTransactions:'Recent Transactions',invoiced:'Invoiced',collected:'Collected',
    pendingAR:'Pending A/R',count:'Count',purchased:'Purchased',paid:'Paid',
    pendingAP:'Pending A/P',totalCollected:'Total Collected',thisMonth:'This Month',
    totalPaid:'Total Paid',grossProfit:'Gross Profit',operatingExpenses:'Operating Expenses',
    totalAssets:'Total Assets',totalLiabilities:'Total Liabilities',totalEquity:'Total Equity',
    currentAssets:'Current Assets',nonCurrentAssets:'Non-Current Assets',
    currentLiabilities:'Current Liabilities',nonCurrentLiabilities:'Non-Current Liabilities',
    equity:'Equity',operatingActivities:'Operating Activities',investingActivities:'Investing Activities',
    financingActivities:'Financing Activities',netChangeInCash:'Net Change in Cash',
    closingBalance:'Closing Balance',openingBalance:'Opening Balance',
    welcomeBack:'Welcome back,',date:'Date',customer:'Customer',supplier:'Supplier',
    description:'Description',total:'Total',status:'Status',method:'Method',
    pending:'Pending',paid2:'Paid',partial:'Partial',del:'Del',cancel:'Cancel',save:'Save',
    postEntry:'Post Entry',saveInvoice:'Save Invoice',savePurchase:'Save Purchase',
    balanced:'Balanced',unbalanced:'Unbalanced',collect:'Collect',pay:'Pay',
    exportExcel:'Export Excel',exportPDF:'Export PDF',
    noDataYet:'No data yet.',addTransactions:'Add transactions to see chart'
  },
  es:{
    dashboard:'Panel',contacts:'Contactos',sales:'Ventas',purchases:'Compras',
    collections:'Cobros',payments:'Pagos',journal:'Asientos Contables',
    pl:'Cuenta de PyG',bs:'Balance de Situación',cf:'Flujo de Caja',settings:'Configuración',
    newInvoice:'+ Nueva Factura',newPurchase:'+ Nueva Compra',newCollection:'+ Registrar Cobro',
    newPayment:'+ Registrar Pago',newEntry:'+ Nuevo Asiento',newContact:'+ Nuevo Contacto',
    overview:'Resumen',operations:'Operaciones',reports:'Informes',
    totalRevenue:'Ingresos Totales',totalExpenses:'Gastos Totales',netIncome:'Beneficio Neto',
    cashPosition:'Posición de Caja',accountsReceivable:'Clientes (deudores)',
    accountsPayable:'Proveedores (acreed.)',salesInvoices:'Facturas de Venta',
    purchaseInvoices:'Facturas de Compra',netMargin:'Margen Neto',
    recentTransactions:'Movimientos Recientes',invoiced:'Facturado',collected:'Cobrado',
    pendingAR:'Pendiente Cobro',count:'Nº',purchased:'Comprado',paid:'Pagado',
    pendingAP:'Pendiente Pago',totalCollected:'Total Cobrado',thisMonth:'Este Mes',
    totalPaid:'Total Pagado',grossProfit:'Margen Bruto',operatingExpenses:'Gastos Operativos',
    totalAssets:'Total Activo',totalLiabilities:'Total Pasivo',totalEquity:'Patrimonio Neto',
    currentAssets:'Activo Corriente',nonCurrentAssets:'Activo No Corriente',
    currentLiabilities:'Pasivo Corriente',nonCurrentLiabilities:'Pasivo No Corriente',
    equity:'Patrimonio Neto',operatingActivities:'Actividades de Explotación',
    investingActivities:'Actividades de Inversión',financingActivities:'Actividades de Financiación',
    netChangeInCash:'Variación Neta de Caja',closingBalance:'Saldo Final',openingBalance:'Saldo Inicial',
    welcomeBack:'Bienvenido,',date:'Fecha',customer:'Cliente',supplier:'Proveedor',
    description:'Descripción',total:'Total',status:'Estado',method:'Método',
    pending:'Pendiente',paid2:'Pagado',partial:'Parcial',del:'Elim.',cancel:'Cancelar',save:'Guardar',
    postEntry:'Publicar Asiento',saveInvoice:'Guardar Factura',savePurchase:'Guardar Compra',
    balanced:'Cuadrado',unbalanced:'Descuadrado',collect:'Cobrar',pay:'Pagar',
    exportExcel:'Exportar Excel',exportPDF:'Exportar PDF',
    noDataYet:'Sin datos aún.',addTransactions:'Añade transacciones para ver el gráfico'
  },
  fr:{
    dashboard:'Tableau de bord',contacts:'Contacts',sales:'Ventes',purchases:'Achats',
    collections:'Encaissements',payments:'Paiements',journal:'Journal Comptable',
    pl:'Compte de Résultat',bs:'Bilan',cf:'Flux de Trésorerie',settings:'Paramètres',
    newInvoice:'+ Nouvelle Facture',newPurchase:'+ Nouvel Achat',newCollection:'+ Enregistrer',
    newPayment:'+ Enregistrer',newEntry:'+ Nouvelle Écriture',newContact:'+ Nouveau Contact',
    overview:'Vue ensemble',operations:'Opérations',reports:'Rapports',
    totalRevenue:'Revenus Totaux',totalExpenses:'Dépenses Totales',netIncome:'Résultat Net',
    cashPosition:'Trésorerie',accountsReceivable:'Clients',accountsPayable:'Fournisseurs',
    salesInvoices:'Factures de Vente',purchaseInvoices:'Factures Achat',netMargin:'Marge Nette',
    recentTransactions:'Transactions Récentes',invoiced:'Facturé',collected:'Encaissé',
    pendingAR:'En attente',count:'Nbre',purchased:'Acheté',paid:'Payé',pendingAP:'À payer',
    totalCollected:'Total Encaissé',thisMonth:'Ce Mois',totalPaid:'Total Payé',
    grossProfit:'Marge Brute',operatingExpenses:'Charges exploitation',
    totalAssets:'Total Actif',totalLiabilities:'Total Passif',totalEquity:'Capitaux Propres',
    currentAssets:'Actif Courant',nonCurrentAssets:'Actif Non Courant',
    currentLiabilities:'Passif Courant',nonCurrentLiabilities:'Passif Non Courant',
    equity:'Capitaux Propres',operatingActivities:'Activités Opérationnelles',
    investingActivities:'Activites Investissement',financingActivities:'Activites Financement',
    netChangeInCash:'Variation Nette de Trésorerie',closingBalance:'Solde Final',
    openingBalance:'Solde Initial',welcomeBack:'Bienvenue,',date:'Date',customer:'Client',
    supplier:'Fournisseur',description:'Description',total:'Total',status:'Statut',method:'Méthode',
    pending:'En attente',paid2:'Payé',partial:'Partiel',del:'Suppr.',cancel:'Annuler',save:'Sauvegarder',
    postEntry:'Valider',saveInvoice:'Enregistrer',savePurchase:'Enregistrer',
    balanced:'Équilibré',unbalanced:'Déséquilibré',collect:'Encaisser',pay:'Payer',
    exportExcel:'Exporter Excel',exportPDF:'Exporter PDF',
    noDataYet:'Pas encore de données.',addTransactions:'Ajoutez des transactions pour voir le graphique'
  },
  de:{
    dashboard:'Dashboard',contacts:'Kontakte',sales:'Verkäufe',purchases:'Einkäufe',
    collections:'Zahlungseingänge',payments:'Zahlungen',journal:'Buchungsjournal',
    pl:'GuV-Rechnung',bs:'Bilanz',cf:'Kapitalflussrechnung',settings:'Einstellungen',
    newInvoice:'+ Neue Rechnung',newPurchase:'+ Neuer Kauf',newCollection:'+ Eingang',
    newPayment:'+ Zahlung',newEntry:'+ Neuer Eintrag',newContact:'+ Neuer Kontakt',
    overview:'Übersicht',operations:'Operationen',reports:'Berichte',
    totalRevenue:'Gesamtumsatz',totalExpenses:'Gesamtkosten',netIncome:'Nettoergebnis',
    cashPosition:'Kassenbestand',accountsReceivable:'Forderungen',accountsPayable:'Verbindlichkeiten',
    salesInvoices:'Verkaufsrechnungen',purchaseInvoices:'Einkaufsrechnungen',netMargin:'Nettomarge',
    recentTransactions:'Letzte Transaktionen',invoiced:'Fakturiert',collected:'Eingegangen',
    pendingAR:'Ausstehend',count:'Anz.',purchased:'Eingekauft',paid:'Bezahlt',pendingAP:'Zu zahlen',
    totalCollected:'Gesamt Eingegangen',thisMonth:'Diesen Monat',totalPaid:'Gesamt Bezahlt',
    grossProfit:'Bruttogewinn',operatingExpenses:'Betriebskosten',
    totalAssets:'Gesamtvermögen',totalLiabilities:'Gesamtverbindlichkeiten',totalEquity:'Eigenkapital',
    currentAssets:'Umlaufvermögen',nonCurrentAssets:'Anlagevermögen',
    currentLiabilities:'Kurzfristige Verbindlichkeiten',nonCurrentLiabilities:'Langfristige Verbindlichkeiten',
    equity:'Eigenkapital',operatingActivities:'Betriebliche Tätigkeit',
    investingActivities:'Investitionstätigkeit',financingActivities:'Finanzierungstätigkeit',
    netChangeInCash:'Nettoveränderung Kassenbestand',closingBalance:'Abschlusssaldo',
    openingBalance:'Eröffnungssaldo',welcomeBack:'Willkommen,',date:'Datum',customer:'Kunde',
    supplier:'Lieferant',description:'Beschreibung',total:'Gesamt',status:'Status',method:'Methode',
    pending:'Ausstehend',paid2:'Bezahlt',partial:'Teilweise',del:'Löschen',cancel:'Abbrechen',save:'Speichern',
    postEntry:'Buchen',saveInvoice:'Rechnung speichern',savePurchase:'Kauf speichern',
    balanced:'Ausgeglichen',unbalanced:'Nicht ausgeglichen',collect:'Einziehen',pay:'Bezahlen',
    exportExcel:'Excel exportieren',exportPDF:'PDF exportieren',
    noDataYet:'Noch keine Daten.',addTransactions:'Transaktionen hinzufügen um Diagramm zu sehen'
  }
};

function t(key){ return (T[DB.prefs.lang||'en']||T.en)[key] || (T.en[key]) || key; }

function applyTranslations(){
  var lang = DB.prefs.lang || 'en';
  // Nav items
  var navMap = {
    'dashboard':'dashboard','contacts':'contacts','sales':'sales','purchases':'purchases',
    'collections':'collections','payments':'payments','journal':'journal',
    'pl':'pl','bs':'bs','cf':'cf'
  };
  document.querySelectorAll('.nav-item').forEach(function(el){
    var match = el.getAttribute('onclick')||'';
    var pg = match.replace("nav('","").replace("')","");
    if(T[lang] && T[lang][pg]) el.childNodes[1] && (el.childNodes[1].textContent = T[lang][pg]);
  });
  // Nav sections
  var secs = document.querySelectorAll('.nav-sec');
  var secLabels = [t('overview'), t('operations'), t('reports')];
  secs.forEach(function(s,i){ if(secLabels[i]) s.textContent = secLabels[i]; });
  // Topbar greeting
  var greetEl = document.querySelector('.greeting');
  if(greetEl) greetEl.childNodes[0].textContent = t('welcomeBack') + ' ';
  // Settings button
    // settings btn
  if(settBtn) settBtn.textContent = '⚙ ' + t('settings');
  // Chart placeholder
  var chartPh = document.querySelector('#chartBars div');
  if(chartPh && chartPh.textContent.indexOf('Add') >= 0) chartPh.textContent = t('addTransactions');
}

function setDateFilter(from, to) {
  _dateFrom = from || '';
  _dateTo   = to   || '';
  // Sync all date inputs across pages
  ['df-from','df-from2','df-from3'].forEach(function(id){
    var el=document.getElementById(id); if(el)el.value=_dateFrom;
  });
  ['df-to','df-to2','df-to3'].forEach(function(id){
    var el=document.getElementById(id); if(el)el.value=_dateTo;
  });
  // Toggle filter badge
  var active = _dateFrom || _dateTo;
  document.querySelectorAll('#df-badge,#df-badge2,#df-badge3').forEach(function(b){
    if(b) b.style.display = active ? 'inline-flex' : 'none';
  });
  renderAll();
}

function inRange(date) {
  if (!date) return true;
  if (_dateFrom && date < _dateFrom) return false;
  if (_dateTo   && date > _dateTo)   return false;
  return true;
}

function cF(){
  // ══════════════════════════════════════════════════════════════════════════
  // SINGLE SOURCE OF TRUTH: Journal Entries drive ALL financial statements.
  // DB.sales / DB.purch are used only for operational views (lists, A/R, A/P).
  // ══════════════════════════════════════════════════════════════════════════

  // Date-filtered JEs for P&L and CF
  var jes = DB.je.filter(function(x){ return inRange(x.date); });

  // Account classification
  var CASH_ACCTS    = ['1000'];
  var AR_ACCTS      = ['1100'];
  var AP_ACCTS      = ['2000'];
  var INVEST_ACCTS  = ['1500','1510'];
  var FINANCE_ACCTS = ['2500','3000','3100','2200'];
  var REV_ACCTS     = ['4000','4100'];
  var COGS_ACCTS    = ['5000'];
  var OPEX_ACCTS    = ['6000','6100','6200','6300','6400','6500','6900'];
  var FINEXP_ACCTS  = ['7000','7100'];

  // ── P&L — read directly from JE account balances ─────────────────────────
  var plBalances = {};
  jes.forEach(function(je){
    je.lines.forEach(function(l){
      if(!plBalances[l.account]) plBalances[l.account]={dr:0,cr:0};
      plBalances[l.account].dr += (l.debit  || 0);
      plBalances[l.account].cr += (l.credit || 0);
    });
  });

  function plBal(acc){
    var b = plBalances[acc]; if(!b) return 0;
    var acct = COA.find(function(a){return a.c===acc;});
    if(!acct) return b.dr - b.cr;
    if(acct.t==='revenue') return b.cr - b.dr;  // revenue: Cr positive
    return b.dr - b.cr;                           // expense/asset: Dr positive
  }

  // Revenue
  var rev = REV_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);

  // COGS
  var cogs = COGS_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);

  // OpEx by category name
  var opex = {};
  OPEX_ACCTS.forEach(function(acc){
    var bal = plBal(acc);
    if(bal !== 0){
      var acct = COA.find(function(a){return a.c===acc;});
      var name = acct ? acct.n : acc;
      opex[name] = (opex[name]||0) + bal;
    }
  });
  var toOpEx = Object.values(opex).reduce(function(a,v){return a+v;},0);
  var ebit   = rev - cogs - toOpEx;

  // Financial expenses (interest, tax)
  var finExp = FINEXP_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);
  var ni     = ebit - finExp;

  // ── CASH FLOW — read from 1000 Cash movements in JEs ─────────────────────
  var jeOCF=0, jeICF=0, jeFCF=0;
  var jeOCFLines=[], jeICFLines=[], jeFCFLines=[];

  jes.forEach(function(je){
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account) < 0) return;
      var cashMove = (l.debit||0) - (l.credit||0); // Dr=in, Cr=out
      var others = je.lines.filter(function(o){return o!==l;});
      var toInvest  = others.some(function(o){return INVEST_ACCTS.indexOf(o.account)>=0;});
      var toFinance = others.some(function(o){return FINANCE_ACCTS.indexOf(o.account)>=0;});
      var toAR      = others.some(function(o){return AR_ACCTS.indexOf(o.account)>=0;});
      var toAP      = others.some(function(o){return AP_ACCTS.indexOf(o.account)>=0;});
      if(toInvest){
        jeICF += cashMove;
        if(cashMove!==0) jeICFLines.push({desc:je.desc,amt:cashMove});
      } else if(toFinance){
        jeFCF += cashMove;
        if(cashMove!==0) jeFCFLines.push({desc:je.desc,amt:cashMove});
      } else {
        // Operating: includes collections (Dr Cash/Cr AR) and payments (Dr AP/Cr Cash)
        jeOCF += cashMove;
        if(cashMove!==0) jeOCFLines.push({desc:je.desc,amt:cashMove});
      }
    });
  });

  var totColl = jes.reduce(function(a,je){
    // Cash IN from operations = Dr 1000 where other side is AR or revenue
    var cashIn=0;
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account)>=0 && l.debit>0){
        var others=je.lines.filter(function(o){return o!==l;});
        var fromAR=others.some(function(o){return AR_ACCTS.indexOf(o.account)>=0;});
        var fromRev=others.some(function(o){return REV_ACCTS.indexOf(o.account)>=0;});
        if(fromAR||fromRev) cashIn+=l.debit;
      }
    });
    return a+cashIn;
  },0);

  var totPay = jes.reduce(function(a,je){
    // Cash OUT from operations = Cr 1000 where other side is AP or expense
    var cashOut=0;
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account)>=0 && l.credit>0){
        var others=je.lines.filter(function(o){return o!==l;});
        var toAP=others.some(function(o){return AP_ACCTS.indexOf(o.account)>=0;});
        var toExp=others.some(function(o){
          var ac=COA.find(function(a){return a.c===o.account;});
          return ac&&ac.t==='expense';
        });
        if(toAP||toExp) cashOut+=l.credit;
      }
    });
    return a+cashOut;
  },0);

  // Cash position = net of all Cash account movements
  var cash = jeOCF + jeICF + jeFCF;

  // ── A/R and A/P for operational views (from sales/purch lists) ───────────
  // These are still useful for Collections/Payments reconciliation
  var salesTotal  = DB.sales.reduce(function(a,x){return a+x.total;},0);
  var purchTotal  = DB.purch.reduce(function(a,x){return a+x.total;},0);
  var collTotal   = DB.coll.reduce(function(a,x){return a+x.amount;},0);
  var payTotal    = DB.pay.reduce(function(a,x){return a+x.amount;},0);
  var ar = Math.max(0, salesTotal - collTotal);
  var ap = Math.max(0, purchTotal - payTotal);

  // ── Balance Sheet — all account balances from ALL JEs (no date filter) ────
  var bsBalances = {};
  DB.je.forEach(function(je){
    je.lines.forEach(function(l){
      if(!bsBalances[l.account]) bsBalances[l.account]={dr:0,cr:0};
      bsBalances[l.account].dr += (l.debit  || 0);
      bsBalances[l.account].cr += (l.credit || 0);
    });
  });
  function jeBal(acc){
    var b=bsBalances[acc]; if(!b) return 0;
    var acct=COA.find(function(a){return a.c===acc;});
    if(!acct) return b.dr-b.cr;
    if(acct.t==='asset'||acct.t==='expense') return b.dr-b.cr;
    return b.cr-b.dr;
  }
  var jeFixedAssets  = jeBal('1500') - jeBal('1510');
  var jeLTDebt       = jeBal('2500');
  var jeShareCapital = jeBal('3000');
  var jeRetained     = jeBal('3100');
  var jeAccrued      = jeBal('2200');
  // Cash from BS = net of all 1000 movements
  var bsCash = jeBal('1000');
  // AR from BS = net of 1100
  var bsAR   = jeBal('1100');
  // AP from BS = net of 2000
  var bsAP   = jeBal('2000');
  // VAT = net of 2100
  var vatP   = jeBal('2100');

  return{
    rev:rev, cogs:cogs, opex:opex, toOpEx:toOpEx, ebit:ebit, ni:ni,
    finExp:finExp,
    totColl:totColl, totPay:totPay, cash:cash,
    ar:ar, ap:ap, vatP:vatP,
    totRev:rev, totExp:cogs+toOpEx+finExp,
    jeOCF:jeOCF, jeICF:jeICF, jeFCF:jeFCF,
    jeOCFLines:jeOCFLines, jeICFLines:jeICFLines, jeFCFLines:jeFCFLines,
    jeFixedAssets:jeFixedAssets, jeLTDebt:jeLTDebt,
    jeShareCapital:jeShareCapital, jeRetained:jeRetained, jeAccrued:jeAccrued,
    bsCash:bsCash, bsAR:bsAR, bsAP:bsAP,
    jeCashAdj:0
  };
}

// ── RENDERERS ──────────────────────────────────────────────────────────────
function rDash(){
  var F=cF();
  document.getElementById('kpi-rev').textContent=f(F.rev);
  document.getElementById('kpi-exp').textContent=f(F.cogs+F.toOpEx+F.finExp);
  var ni=document.getElementById('kpi-ni');ni.textContent=f(F.ni);ni.style.color=F.ni>=0?'var(--green)':'var(--red)';
  document.getElementById('kpi-cash').textContent=f(F.cash);
  document.getElementById('qs-ar').textContent=f(F.ar);document.getElementById('qs-ap').textContent=f(F.ap);
  document.getElementById('qs-sc').textContent=DB.sales.length;document.getElementById('qs-pc').textContent=DB.purch.length;document.getElementById('qs-jec').textContent=DB.je.length;
  var mg=document.getElementById('qs-mg');
  if(F.totRev){var p=(F.ni/F.totRev*100).toFixed(1);mg.textContent=p+'%';mg.style.color=p>=0?'var(--green)':'var(--red)';}else mg.textContent='—';
  if(DB.sales.length||DB.purch.length){
    var mo={};
    DB.sales.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].r+=x.net;});
    DB.purch.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].e+=x.net;});
    var ks=Object.keys(mo).sort().slice(-8),mv=Math.max.apply(null,ks.map(function(k){return Math.max(mo[k].r,mo[k].e);}));mv=Math.max(mv,1);
    var MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    document.getElementById('chartBars').innerHTML=ks.map(function(k){var d=mo[k],rh=Math.max(4,d.r/mv*140),eh=Math.max(4,d.e/mv*140),ml=k.substring(5,7),mn=MN[parseInt(ml)-1]||ml;return '<div class="bar-wrap"><div style="display:flex;gap:3px;align-items:flex-end;height:140px;"><div class="bar" style="background:var(--green);height:'+rh+'px;width:14px;" title="'+f(d.r)+'"></div><div class="bar" style="background:var(--red);height:'+eh+'px;width:14px;" title="'+f(d.e)+'"></div></div><div class="bar-lbl">'+mn+'</div></div>';}).join('');
  }else document.getElementById('chartBars').innerHTML='<div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:\'DM Mono\',monospace;">Add transactions to see chart</div>';
  var tmap={Sale:'bg',Purchase:'br',Collection:'bb',Payment:'by',Journal:'ba'};
  var all=[].concat(DB.sales.map(function(x){return{date:x.date,type:'Sale',desc:x.desc||'Sale',party:x.customer,amount:x.total,status:x.status};}),DB.purch.map(function(x){return{date:x.date,type:'Purchase',desc:x.desc||'Purchase',party:x.supplier,amount:-x.total,status:x.status};}),DB.coll.map(function(x){return{date:x.date,type:'Collection',desc:'Cash received',party:x.customer,amount:x.amount,status:'received'};}),DB.pay.map(function(x){return{date:x.date,type:'Payment',desc:'Cash paid',party:x.supplier,amount:-x.amount,status:'paid'};}),DB.je.map(function(x){return{date:x.date,type:'Journal',desc:x.desc,party:'Manual',amount:x.amount,status:'posted'};})).sort(function(a,b){return b.date<a.date?-1:1;}).slice(0,10);
  var rb=document.getElementById('recentTx');
  if(!all.length){rb.innerHTML='<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:24px;">No transactions yet. Start by adding a sale or purchase.</td></tr>';return;}
  rb.innerHTML=all.map(function(t){return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;">'+t.date+'</td><td><span class="badge '+(tmap[t.type]||'bb')+'">'+t.type+'</span></td><td>'+t.desc+'</td><td style="color:var(--text3);">'+t.party+'</td><td class="amt '+(t.amount>=0?'pos':'neg')+'">'+f(Math.abs(t.amount))+'</td><td>'+bdg(t.status)+'</td></tr>';}).join('');
}
function rSales(){
  var tot=DB.sales.reduce(function(a,x){return a+x.total;},0),coll=DB.coll.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('s-tot').textContent=f(tot);document.getElementById('s-coll').textContent=f(coll);document.getElementById('s-ar').textContent=f(Math.max(0,tot-coll));document.getElementById('s-cnt').textContent=DB.sales.length;
  var b=document.getElementById('salesTbl');
  if(!DB.sales.length){b.innerHTML='<tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr>';return;}
  b.innerHTML=DB.sales.slice().sort(function(a,c){return c.id-a.id;}).map(function(s){return '<tr><td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--accent);">'+s.num+'</span></td><td>'+s.date+'</td><td style="font-weight:500;color:var(--text);">'+s.customer+'</td><td style="color:var(--text3);">'+(s.desc||'—')+'</td><td class="amt">'+s.vatRate+'%</td><td class="amt">'+f(s.net)+'</td><td class="amt" style="color:var(--text3);">'+f(s.vatAmt)+'</td><td class="amt pos">'+f(s.total)+'</td><td>'+bdg(s.status)+'</td><td><button class="btn btn-danger btn-sm" onclick="delS('+s.id+')">Del</button></td></tr>';}).join('');
}
function rPurch(){
  var tot=DB.purch.reduce(function(a,x){return a+x.total;},0),paid=DB.pay.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('p-tot').textContent=f(tot);document.getElementById('p-paid').textContent=f(paid);document.getElementById('p-ap').textContent=f(Math.max(0,tot-paid));document.getElementById('p-cnt').textContent=DB.purch.length;
  var b=document.getElementById('purchTbl');
  if(!DB.purch.length){b.innerHTML='<tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr>';return;}
  b.innerHTML=DB.purch.slice().sort(function(a,c){return c.id-a.id;}).map(function(p){return '<tr><td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td><td>'+p.date+'</td><td style="font-weight:500;color:var(--text);">'+p.supplier+'</td><td style="color:var(--text3);">'+(p.desc||'—')+'</td><td><span class="badge bb">'+p.cat+'</span></td><td class="amt">'+p.vatRate+'%</td><td class="amt">'+f(p.net)+'</td><td class="amt" style="color:var(--text3);">'+f(p.vatAmt)+'</td><td class="amt neg">'+f(p.total)+'</td><td>'+bdg(p.status)+'</td><td><button class="btn btn-danger btn-sm" onclick="delP('+p.id+')">Del</button></td></tr>';}).join('');
}
// Current sale being reconciled
var _rcSaleId = null;

function openReconcileColl(saleId) {
  _rcSaleId = saleId;
  var s = DB.sales.find(function(x){return x.id===saleId;});
  if (!s) return;
  var collected = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
  var remaining = Math.max(0, s.total - collected);
  document.getElementById('rc-invoice-info').innerHTML =
    '<strong>' + s.num + '</strong> &nbsp;·&nbsp; ' + s.customer +
    ' &nbsp;·&nbsp; Total: <span style="color:var(--green);">' + f(s.total) + '</span>' +
    ' &nbsp;·&nbsp; Remaining: <span style="color:var(--yellow);">' + f(remaining) + '</span>';
  document.getElementById('rc-date').value = td();
  document.getElementById('rc-amount').value = remaining.toFixed(2);
  document.getElementById('rc-notes').value = '';
  openOverlay('ov-reconcile-coll');
}

function confirmCollect() {
  var s = DB.sales.find(function(x){return x.id===_rcSaleId;});
  if (!s) return;
  var amt = parseFloat(document.getElementById('rc-amount').value)||0;
  if (!amt) { alert('Enter an amount.'); return; }
  var dt  = document.getElementById('rc-date').value;
  var mth2 = document.getElementById('rc-method').value;
  var notes = document.getElementById('rc-notes').value;

  // 1. Create collection record
  DB.coll.push({id:DB.ids.c++, date:dt, customer:s.customer, ref:s.num, method:mth2, amount:amt, notes:notes||'Reconciled from '+s.num});

  // 2. Auto journal entry: Dr Cash / Cr Accounts Receivable
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Collection — ' + s.customer + ' / ' + s.num,
    lines: [
      {account:'1000', debit:amt,  credit:0},   // Dr Cash & Bank
      {account:'1100', debit:0,    credit:amt}   // Cr Accounts Receivable
    ],
    amount: amt,
    auto: true
  });

  // 3. Update sale status
  var collected2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
  if (collected2 >= s.total - 0.01) s.status = 'paid';
  else if (collected2 > 0) s.status = 'partial';

  sv(); closeOverlay('ov-reconcile-coll'); renderAll();
}

function rColl(){
  var totalInvoiced = DB.sales.reduce(function(a,x){return a+x.total;},0);
  var tot=DB.coll.reduce(function(a,x){return a+x.amount;},0);
  var curym=ym(), mth2=DB.coll.filter(function(x){return x.date&&x.date.startsWith(curym);}).reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('c-invoiced').textContent=f(totalInvoiced);
  document.getElementById('c-tot').textContent=f(tot);
  document.getElementById('c-pending').textContent=f(Math.max(0,totalInvoiced-tot));
  document.getElementById('c-mth').textContent=f(mth2);
  document.getElementById('c-cnt').textContent=DB.coll.length;

  // ── Pending table (sales not fully collected) ──
  var pb = document.getElementById('pendingCollTbl');
  var pending = DB.sales.filter(function(s){
    var coll2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
    return coll2 < s.total - 0.01;
  });
  if (!pending.length) {
    pb.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--text3);padding:20px;">✅ All invoices collected!</td></tr>';
  } else {
    pb.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(s){
      var coll2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem = s.total - coll2;
      return '<tr class="needs-coll">' +
        '<td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--accent);">'+s.num+'</span></td>' +
        '<td>'+s.date+'</td>' +
        '<td style="font-weight:600;color:var(--text);">'+s.customer+'</td>' +
        '<td style="color:var(--text3);">'+(s.desc||'—')+'</td>' +
        '<td class="amt">'+f(s.total)+'</td>' +
        '<td class="amt pos">'+f(coll2)+'</td>' +
        '<td class="amt" style="color:var(--yellow);">'+f(rem)+'</td>' +
        '<td><select onchange="this.dataset.v=this.value" data-v="bank" style="padding:4px 8px;font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:5px;color:var(--text);"><option value=\'bank\'>🏦 Bank</option><option value=\'cash\'>💵 Cash</option><option value=\'card\'>💳 Card</option><option value=\'other\'>📋 Other</option></select></td>' +
        '<td><button class="btn-reconcile" onclick="openReconcileColl('+s.id+')">⚡ Collect</button></td>' +
        '</tr>';
    }).join('');
  }

  // ── Collection history ──
  var b=document.getElementById('collTbl');
  if(!DB.coll.length){b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:20px;">No collections yet.</td></tr>';return;}
  b.innerHTML=DB.coll.slice().sort(function(a,c){return c.id-a.id;}).map(function(c){
    return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text3);">#'+c.id+'</td><td>'+c.date+'</td><td style="font-weight:500;color:var(--text);">'+c.customer+'</td><td style="color:var(--text3);">'+(c.ref||'—')+'</td><td>'+mth(c.method)+'</td><td class="amt pos">'+f(c.amount)+'</td><td style="color:var(--text3);">'+(c.notes||'—')+'</td><td><button class="btn btn-danger btn-sm" onclick="delC('+c.id+')">Del</button></td></tr>';
  }).join('');
}
var _rpPurchId = null;

function openReconcilePay(purchId) {
  _rpPurchId = purchId;
  var p = DB.purch.find(function(x){return x.id===purchId;});
  if (!p) return;
  var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
  var remaining = Math.max(0, p.total - paid);
  document.getElementById('rp-invoice-info').innerHTML =
    '<strong>' + p.num + '</strong> &nbsp;·&nbsp; ' + p.supplier +
    ' &nbsp;·&nbsp; <span class="badge bb">' + p.cat + '</span>' +
    ' &nbsp;·&nbsp; Total: <span style="color:var(--red);">' + f(p.total) + '</span>' +
    ' &nbsp;·&nbsp; Remaining: <span style="color:var(--yellow);">' + f(remaining) + '</span>';
  document.getElementById('rp-date').value = td();
  document.getElementById('rp-amount').value = remaining.toFixed(2);
  document.getElementById('rp-notes').value = '';
  openOverlay('ov-reconcile-pay');
}

function confirmPay() {
  var p = DB.purch.find(function(x){return x.id===_rpPurchId;});
  if (!p) return;
  var amt = parseFloat(document.getElementById('rp-amount').value)||0;
  if (!amt) { alert('Enter an amount.'); return; }
  var dt   = document.getElementById('rp-date').value;
  var mth2 = document.getElementById('rp-method').value;
  var notes = document.getElementById('rp-notes').value;

  // 1. Create payment record
  DB.pay.push({id:DB.ids.py++, date:dt, supplier:p.supplier, ref:p.num, method:mth2, amount:amt, notes:notes||'Reconciled from '+p.num});

  // 2. Auto journal entry: Dr Accounts Payable / Cr Cash
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Payment — ' + p.supplier + ' / ' + p.num,
    lines: [
      {account:'2000', debit:amt, credit:0},   // Dr Accounts Payable
      {account:'1000', debit:0,   credit:amt}   // Cr Cash & Bank
    ],
    amount: amt,
    auto: true
  });

  // 3. Update purchase status
  var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
  if (paid2 >= p.total - 0.01) p.status = 'paid';

  sv(); closeOverlay('ov-reconcile-pay'); renderAll();
}

function rPay(){
  var totalPurch = DB.purch.reduce(function(a,x){return a+x.total;},0);
  var tot=DB.pay.reduce(function(a,x){return a+x.amount;},0);
  var curym=ym(), mth2=DB.pay.filter(function(x){return x.date&&x.date.startsWith(curym);}).reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('py-purchased').textContent=f(totalPurch);
  document.getElementById('py-tot').textContent=f(tot);
  document.getElementById('py-pending').textContent=f(Math.max(0,totalPurch-tot));
  document.getElementById('py-mth').textContent=f(mth2);
  document.getElementById('py-cnt').textContent=DB.pay.length;

  // ── Pending table (purchases not fully paid) ──
  var pb = document.getElementById('pendingPayTbl');
  var pending = DB.purch.filter(function(p){
    var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
    return paid2 < p.total - 0.01;
  });
  if (!pending.length) {
    pb.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text3);padding:20px;">✅ All invoices paid!</td></tr>';
  } else {
    pb.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(p){
      var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem = p.total - paid2;
      return '<tr class="needs-coll">' +
        '<td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td>' +
        '<td>'+p.date+'</td>' +
        '<td style="font-weight:600;color:var(--text);">'+p.supplier+'</td>' +
        '<td style="color:var(--text3);">'+(p.desc||'—')+'</td>' +
        '<td><span class="badge bb">'+p.cat+'</span></td>' +
        '<td class="amt">'+f(p.total)+'</td>' +
        '<td class="amt pos">'+f(paid2)+'</td>' +
        '<td class="amt" style="color:var(--yellow);">'+f(rem)+'</td>' +
        '<td><select style="padding:4px 8px;font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:5px;color:var(--text);"><option value=\'bank\'>🏦 Bank</option><option value=\'cash\'>💵 Cash</option><option value=\'card\'>💳 Card</option><option value=\'other\'>📋 Other</option></select></td>' +
        '<td><button class="btn-reconcile" onclick="openReconcilePay('+p.id+')">⚡ Pay</button></td>' +
        '</tr>';
    }).join('');
  }

  // ── Payment history ──
  var b=document.getElementById('payTbl');
  if(!DB.pay.length){b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:20px;">No payments yet.</td></tr>';return;}
  b.innerHTML=DB.pay.slice().sort(function(a,c){return c.id-a.id;}).map(function(p){
    return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text3);">#'+p.id+'</td><td>'+p.date+'</td><td style="font-weight:500;color:var(--text);">'+p.supplier+'</td><td style="color:var(--text3);">'+(p.ref||'—')+'</td><td>'+mth(p.method)+'</td><td class="amt neg">'+f(p.amount)+'</td><td style="color:var(--text3);">'+(p.notes||'—')+'</td><td><button class="btn btn-danger btn-sm" onclick="delPy('+p.id+')">Del</button></td></tr>';
  }).join('');
}
function rJE(){
  var b=document.getElementById('jeTbl');
  if(!DB.je.length){
    b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No journal entries yet.</td></tr>';
    return;
  }
  var srcColors={sale:'var(--green)',purchase:'var(--red)',collection:'var(--blue)',payment:'var(--yellow)',manual:'var(--purple)'};
  var srcLabels={sale:'SALE',purchase:'PURCH',collection:'COLL',payment:'PAY',manual:'MANUAL'};
  var rows = DB.je.slice().sort(function(a,z){return z.id-a.id;});
  b.innerHTML = '';
  rows.forEach(function(je){
    var dl = je.lines.find(function(l){return l.debit>0;});
    var cl = je.lines.find(function(l){return l.credit>0;});
    function acName(l){
      if(!l) return '—';
      var a = COA.find(function(ac){return ac.c===l.account;});
      return a ? a.n : l.account;
    }
    var stype  = je.sourceType || 'manual';
    var scolor = srcColors[stype] || 'var(--purple)';
    var slabel = srcLabels[stype] || 'MANUAL';
    var allLines = je.lines.map(function(l){
      var a = COA.find(function(ac){return ac.c===l.account;});
      return (l.debit>0?'Dr ':'Cr ')+(a?a.n:l.account)+' '+f(l.debit||l.credit);
    }).join(' | ');

    var tr = document.createElement('tr');
    tr.title = allLines;

    var td1 = document.createElement('td');
    td1.style.cssText = 'font-size:11px;color:var(--purple);font-family:monospace;';
    td1.textContent = 'JE-'+String(je.id).padStart(3,'0');

    var td2 = document.createElement('td');
    td2.textContent = je.date;

    var td3 = document.createElement('td');
    var badge = document.createElement('span');
    badge.className = 'badge';
    badge.style.cssText = 'background:transparent;color:'+scolor+';border:1px solid '+scolor+';';
    badge.textContent = slabel;
    td3.appendChild(badge);

    var td4 = document.createElement('td');
    td4.style.cssText = 'font-weight:500;color:var(--text);';
    td4.textContent = je.desc;

    var td5 = document.createElement('td');
    td5.style.cssText = 'color:var(--green);font-size:12px;';
    td5.textContent = acName(dl);

    var td6 = document.createElement('td');
    td6.style.cssText = 'color:var(--red);font-size:12px;';
    td6.textContent = acName(cl);

    var td7 = document.createElement('td');
    td7.className = 'amt';
    td7.style.color = 'var(--purple)';
    td7.textContent = f(je.amount);

    var td8 = document.createElement('td');
    var btn = document.createElement('button');
    btn.className = 'btn btn-danger btn-sm';
    btn.textContent = 'Del';
    btn.onclick = (function(jid){return function(){delJ(jid);};})(je.id);
    td8.appendChild(btn);

    [td1,td2,td3,td4,td5,td6,td7,td8].forEach(function(td){tr.appendChild(td);});
    b.appendChild(tr);
  });
}
function plTab(m){plMode=m;document.getElementById('pl-det').classList.toggle('active',m==='detail');document.getElementById('pl-sum').classList.toggle('active',m==='summary');rPL();}
function rPL(){
  var F=cF(),b=document.getElementById('plBody'),gp=F.rev-F.cogs;
  var gmp=F.totRev?(gp/F.totRev*100).toFixed(1):0,npp=F.totRev?(F.ni/F.totRev*100).toFixed(1):0;
  if(plMode==='summary'){b.innerHTML='<tr class="rh"><td colspan="2">Summary P&L</td></tr><tr class="rd"><td>Total Revenue</td><td class="num pos">'+f(F.totRev)+'</td></tr><tr class="rd"><td>Cost of Goods Sold</td><td class="num neg">('+f(F.cogs)+')</td></tr><tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num">'+f(gp)+'</td></tr><tr class="rd"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx)+')</td></tr><tr class="rs"><td>EBIT</td><td class="num">'+f(F.ebit)+'</td></tr><tr class="rd"><td>Journal Adjustments (net)</td><td class="num">'+f(F.jeR-F.jeE)+'</td></tr><tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';return;}
  var rows='<tr class="rh"><td colspan="2">Revenue</td></tr><tr class="rd"><td class="ind">Sales Revenue</td><td class="num pos">'+f(F.rev)+'</td></tr>';
  // Revenue already fully from JE accounts - no separate adjustment line needed
  rows+='<tr class="rs"><td>Total Revenue</td><td class="num">'+f(F.totRev)+'</td></tr><tr class="rh"><td colspan="2">Cost of Goods Sold</td></tr><tr class="rd"><td class="ind">COGS – Direct Purchases</td><td class="num neg">('+f(F.cogs)+')</td></tr><tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num '+(gp>=0?'pos':'neg')+'">'+f(gp)+'</td></tr><tr class="rh"><td colspan="2">Operating Expenses</td></tr>';
  Object.entries(F.opex).forEach(function(e){rows+='<tr class="rd"><td class="ind">'+e[0]+'</td><td class="num neg">('+f(e[1])+')</td></tr>';});
  // Expenses already fully from JE accounts - no separate adjustment line needed
  if(!F.toOpEx&&!F.jeE)rows+='<tr class="rd"><td class="ind" style="color:var(--text3);">No expenses recorded</td><td class="num">—</td></tr>';
  rows+='<tr class="rs"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx+F.jeE)+')</td></tr><tr class="rs"><td>EBIT (Operating Income)</td><td class="num">'+f(F.ebit)+'</td></tr><tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';
  b.innerHTML=rows;
}
function rBS(){
  var F = cF();

  // ── ASSETS ────────────────────────────────────────────────────────────────
  // Cash = operating cash + JE cash movements
  var cash    = F.bsCash;  // from JE account 1000 balance
  var ar      = F.bsAR;    // from JE account 1100 balance
  var tca     = cash + ar;
  // Non-current: Fixed Assets net from JEs
  var fixedA  = F.jeFixedAssets;
  var ta      = tca + (fixedA > 0 ? fixedA : 0);

  // ── LIABILITIES ───────────────────────────────────────────────────────────
  var ap      = F.bsAP;    // from JE account 2000 balance
  var vatp    = Math.max(0, F.vatP); // from JE account 2100 balance
  var accrued = F.jeAccrued;
  var tcl     = ap + vatp + accrued;
  var ltDebt  = F.jeLTDebt;
  var tl      = tcl + ltDebt;

  // ── EQUITY ────────────────────────────────────────────────────────────────
  var shareC  = F.jeShareCapital;
  var retained= F.jeRetained;
  var netInc  = F.ni;
  var te      = shareC + retained + netInc;
  var tle     = tl + te;

  // ── ASSETS SIDE ───────────────────────────────────────────────────────────
  var aRows = '<tr class="rh"><td colspan="2">Current Assets</td></tr>';
  aRows += '<tr class="rd"><td class="ind">Cash &amp; Bank</td><td class="num">'+f(cash)+'</td></tr>';
  aRows += '<tr class="rd"><td class="ind">Accounts Receivable</td><td class="num">'+f(ar)+'</td></tr>';
  aRows += '<tr class="rs"><td>Total Current Assets</td><td class="num">'+f(tca)+'</td></tr>';
  aRows += '<tr class="rh"><td colspan="2">Non-Current Assets</td></tr>';
  if(fixedA > 0){
    aRows += '<tr class="rd"><td class="ind">Fixed Assets (net)</td><td class="num">'+f(fixedA)+'</td></tr>';
  } else {
    aRows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — use Journal Entries</td><td class="num">—</td></tr>';
  }
  aRows += '<tr class="rt"><td>TOTAL ASSETS</td><td class="num">'+f(ta)+'</td></tr>';

  // ── LIABILITIES & EQUITY SIDE ─────────────────────────────────────────────
  var lRows = '<tr class="rh"><td colspan="2">Current Liabilities</td></tr>';
  lRows += '<tr class="rd"><td class="ind">Accounts Payable</td><td class="num">'+f(ap)+'</td></tr>';
  lRows += '<tr class="rd"><td class="ind">VAT Payable (net)</td><td class="num">'+f(vatp)+'</td></tr>';
  if(accrued !== 0) lRows += '<tr class="rd"><td class="ind">Accrued Liabilities</td><td class="num">'+f(accrued)+'</td></tr>';
  lRows += '<tr class="rs"><td>Total Current Liabilities</td><td class="num">'+f(tcl)+'</td></tr>';
  lRows += '<tr class="rh"><td colspan="2">Non-Current Liabilities</td></tr>';
  if(ltDebt > 0){
    lRows += '<tr class="rd"><td class="ind">Long-term Debt</td><td class="num">'+f(ltDebt)+'</td></tr>';
  } else {
    lRows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded</td><td class="num">—</td></tr>';
  }
  lRows += '<tr class="rs"><td>Total Liabilities</td><td class="num">'+f(tl)+'</td></tr>';
  lRows += '<tr class="rh"><td colspan="2">Equity</td></tr>';
  if(shareC !== 0) lRows += '<tr class="rd"><td class="ind">Share Capital</td><td class="num">'+f(shareC)+'</td></tr>';
  if(retained !== 0) lRows += '<tr class="rd"><td class="ind">Retained Earnings</td><td class="num">'+f(retained)+'</td></tr>';
  lRows += '<tr class="rd"><td class="ind">Net Income (Period)</td><td class="num '+(netInc>=0?'pos':'neg')+'">'+f(netInc)+'</td></tr>';
  lRows += '<tr class="rs"><td>Total Equity</td><td class="num">'+f(te)+'</td></tr>';
  lRows += '<tr class="rt"><td>TOTAL LIAB. &amp; EQUITY</td><td class="num">'+f(tle)+'</td></tr>';

  document.getElementById('bsA').innerHTML  = aRows;
  document.getElementById('bsLE').innerHTML = lRows;

  var diff = Math.abs(ta - tle);
  var ck   = document.getElementById('bsChk');
  if(diff < 0.01){
    ck.textContent = '✓ Balanced — Assets = Liabilities + Equity';
    ck.style.color = 'var(--green)';
  } else {
    ck.textContent = '⚠ Unbalanced by ' + f(diff) + ' — check your Journal Entries';
    ck.style.color = 'var(--yellow)';
  }
}
function rCF(){
  var F=cF();
  // Operating: cash in from customers + cash out to suppliers (all from JE account 1000)
  // jeOCF already included in totColl/totPay via JE reading — do NOT add again
  var ocf    = F.totColl - F.totPay;
  var icf    = F.jeICF;
  var fcf    = F.jeFCF;
  var netCF  = ocf + icf + fcf;

  function jeDetailLines(lines) {
    // Only show detail for Investing and Financing — NOT for Operating (avoids duplication)
    if(!lines || !lines.length) return '';
    return lines.map(function(l){
      var cls  = l.amt >= 0 ? 'pos' : 'neg';
      var disp = l.amt >= 0 ? f(l.amt) : '('+f(Math.abs(l.amt))+')';
      return '<tr class="rd"><td class="ind" style="color:var(--text2);">↳ '+l.desc+'</td><td class="num '+cls+'">'+disp+'</td></tr>';
    }).join('');
  }

  var rows = '';

  // ── OPERATING ─────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Operating Activities</td></tr>';
  rows += '<tr class="rd"><td class="ind">Cash received from customers</td><td class="num pos">'+f(F.totColl)+'</td></tr>';
  rows += '<tr class="rd"><td class="ind">Cash paid to suppliers</td><td class="num '+(F.totPay>0?'neg':'')+'">'+(F.totPay>0?'('+f(F.totPay)+')':f(0))+'</td></tr>';
  rows += '<tr class="rs"><td>Net Cash from Operating Activities</td><td class="num '+(ocf>=0?'pos':'neg')+'">'+f(ocf)+'</td></tr>';

  // ── INVESTING ─────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Investing Activities</td></tr>';
  if(F.jeICFLines && F.jeICFLines.length) {
    rows += jeDetailLines(F.jeICFLines);
  } else {
    rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — Dr. Fixed Assets / Cr. Cash in Journal Entries</td><td class="num">—</td></tr>';
  }
  rows += '<tr class="rs"><td>Net Cash from Investing Activities</td><td class="num '+(icf>=0?'pos':'neg')+'">'+f(icf)+'</td></tr>';

  // ── FINANCING ─────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Financing Activities</td></tr>';
  if(F.jeFCFLines && F.jeFCFLines.length) {
    rows += jeDetailLines(F.jeFCFLines);
  } else {
    rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — Dr. Cash / Cr. Long-term Debt or Share Capital in Journal Entries</td><td class="num">—</td></tr>';
  }
  rows += '<tr class="rs"><td>Net Cash from Financing Activities</td><td class="num '+(fcf>=0?'pos':'neg')+'">'+f(fcf)+'</td></tr>';

  // ── TOTALS ────────────────────────────────────────────────────────────────
  rows += '<tr class="rt"><td>NET CHANGE IN CASH</td><td class="num '+(netCF>=0?'pos':'neg')+'">'+f(netCF)+'</td></tr>';
  rows += '<tr class="rd" style="border-top:1px solid var(--border);"><td style="color:var(--text3);">Opening Cash Balance</td><td class="num" style="color:var(--text3);">'+f(0)+'</td></tr>';
  rows += '<tr class="rs"><td>Closing Cash Balance</td><td class="num" style="color:var(--accent);">'+f(netCF)+'</td></tr>';

  document.getElementById('cfBody').innerHTML = rows;
}

// ══════════════════════════════════════════════════════════════════
// CONTACTS MODULE
// ══════════════════════════════════════════════════════════════════

var _ctFilter = 'all';
var _ctEditId = null;
var _ctType   = 'client';
var _ctTab    = 'basic';

function setCtFilter(f) {
  _ctFilter = f;
  ['all','client','supplier','both'].forEach(function(x){
    var el = document.getElementById('ctf-'+x);
    if(el) el.classList.toggle('active', x===f);
  });
  rContacts();
}

function openContactModal(type, id) {
  _ctEditId = id || null;
  _ctType   = type || 'client';
  _ctTab    = 'basic';

  // Reset all tabs
  document.querySelectorAll('.contact-tab').forEach(function(t,i){
    t.classList.toggle('active', i===0);
  });
  document.querySelectorAll('.contact-panel').forEach(function(p,i){
    p.classList.toggle('active', i===0);
  });

  // Set type buttons
  setCtType(_ctType);

  var deleteBtn = document.getElementById('ct-delete-btn');

  if(id) {
    var ct = DB.contacts.find(function(x){return x.id===id;});
    if(!ct) return;
    document.getElementById('ct-modal-title').textContent = 'Edit Contact';
    deleteBtn.style.display = 'inline-flex';
    // Fill fields
    setCtType(ct.type||'client');
    document.getElementById('ct-name').value       = ct.name||'';
    document.getElementById('ct-nif').value        = ct.nif||'';
    document.getElementById('ct-tradename').value  = ct.tradename||'';
    document.getElementById('ct-addr').value       = ct.addr||'';
    document.getElementById('ct-city').value       = ct.city||'';
    document.getElementById('ct-postal').value     = ct.postal||'';
    document.getElementById('ct-province').value   = ct.province||'';
    document.getElementById('ct-country').value    = ct.country||'';
    document.getElementById('ct-email').value      = ct.email||'';
    document.getElementById('ct-phone').value      = ct.phone||'';
    document.getElementById('ct-mobile').value     = ct.mobile||'';
    document.getElementById('ct-web').value        = ct.web||'';
    document.getElementById('ct-iban').value       = ct.iban||'';
    document.getElementById('ct-bic').value        = ct.bic||'';
    document.getElementById('ct-bank').value       = ct.bank||'';
    document.getElementById('ct-payterms').value   = ct.payterms||'30days';
    document.getElementById('ct-creditlimit').value= ct.creditlimit||'';
    document.getElementById('ct-currency').value   = ct.currency||'EUR';
    document.getElementById('ct-salesvat').value   = ct.salesvat||'21';
    document.getElementById('ct-purchvat').value   = ct.purchvat||'21';
    document.getElementById('ct-lang').value       = ct.lang||'en';
    document.getElementById('ct-invoiceby').value  = ct.invoiceby||'email';
    document.getElementById('ct-notes').value      = ct.notes||'';
    document.getElementById('ct-debtacc').value    = ct.debtacc||'';
    document.getElementById('ct-credacc').value    = ct.credacc||'';
    document.getElementById('ct-salestax').value   = ct.salestax||'IVA21';
    document.getElementById('ct-purchtax').value   = ct.purchtax||'IVA21';
    document.getElementById('ct-acccode').value    = ct.acccode||'';
  } else {
    document.getElementById('ct-modal-title').textContent = 'New Contact';
    deleteBtn.style.display = 'none';
    // Clear fields
    ['ct-name','ct-nif','ct-tradename','ct-addr','ct-city','ct-postal','ct-province',
     'ct-country','ct-email','ct-phone','ct-mobile','ct-web','ct-iban','ct-bic',
     'ct-bank','ct-creditlimit','ct-notes','ct-acccode'].forEach(function(id){
      document.getElementById(id).value='';
    });
    document.getElementById('ct-payterms').value  = '30days';
    document.getElementById('ct-currency').value  = 'EUR';
    document.getElementById('ct-salesvat').value  = '21';
    document.getElementById('ct-purchvat').value  = '21';
    document.getElementById('ct-lang').value      = 'en';
    document.getElementById('ct-invoiceby').value = 'email';
    document.getElementById('ct-debtacc').value   = '';
    document.getElementById('ct-credacc').value   = '';
    document.getElementById('ct-salestax').value  = 'IVA21';
    document.getElementById('ct-purchtax').value  = 'IVA21';
  }
  openOverlay('ov-contact');
}

function setCtType(t) {
  _ctType = t;
  ['client','supplier','both'].forEach(function(x){
    var el = document.getElementById('ct-type-'+x);
    if(el) el.classList.toggle('active', x===t);
  });
}

function ctTab(name) {
  var panels = ['basic','accounts','preferences','accounting'];
  var tabs   = document.querySelectorAll('.contact-tab');
  panels.forEach(function(p, i){
    var panel = document.getElementById('ctpanel-'+p);
    if(panel) panel.classList.toggle('active', p===name);
    if(tabs[i]) tabs[i].classList.toggle('active', p===name);
  });
}

function saveContact() {
  var name = document.getElementById('ct-name').value.trim();
  if(!name){ alert('Please enter a contact name.'); return; }

  var ct = {
    id:          _ctEditId || DB.ids.ct++,
    type:        _ctType,
    name:        name,
    nif:         document.getElementById('ct-nif').value,
    tradename:   document.getElementById('ct-tradename').value,
    addr:        document.getElementById('ct-addr').value,
    city:        document.getElementById('ct-city').value,
    postal:      document.getElementById('ct-postal').value,
    province:    document.getElementById('ct-province').value,
    country:     document.getElementById('ct-country').value,
    email:       document.getElementById('ct-email').value,
    phone:       document.getElementById('ct-phone').value,
    mobile:      document.getElementById('ct-mobile').value,
    web:         document.getElementById('ct-web').value,
    iban:        document.getElementById('ct-iban').value,
    bic:         document.getElementById('ct-bic').value,
    bank:        document.getElementById('ct-bank').value,
    payterms:    document.getElementById('ct-payterms').value,
    creditlimit: parseFloat(document.getElementById('ct-creditlimit').value)||0,
    currency:    document.getElementById('ct-currency').value,
    salesvat:    document.getElementById('ct-salesvat').value,
    purchvat:    document.getElementById('ct-purchvat').value,
    lang:        document.getElementById('ct-lang').value,
    invoiceby:   document.getElementById('ct-invoiceby').value,
    notes:       document.getElementById('ct-notes').value,
    debtacc:     document.getElementById('ct-debtacc').value,
    credacc:     document.getElementById('ct-credacc').value,
    salestax:    document.getElementById('ct-salestax').value,
    purchtax:    document.getElementById('ct-purchtax').value,
    acccode:     document.getElementById('ct-acccode').value,
    createdAt:   _ctEditId ? (DB.contacts.find(function(x){return x.id===_ctEditId;})||{}).createdAt : new Date().toISOString().slice(0,10)
  };

  if(_ctEditId) {
    var idx = DB.contacts.findIndex(function(x){return x.id===_ctEditId;});
    if(idx>=0) DB.contacts[idx] = ct;
  } else {
    DB.contacts.push(ct);
  }

  sv(); closeOverlay('ov-contact'); rContacts();
  showToast('✅ Contact saved: ' + name);
}

function deleteContact() {
  if(!_ctEditId) return;
  var ct = DB.contacts.find(function(x){return x.id===_ctEditId;});
  if(!confirm('Delete contact: ' + (ct?ct.name:'') + '?')) return;
  DB.contacts = DB.contacts.filter(function(x){return x.id!==_ctEditId;});
  sv(); closeOverlay('ov-contact'); rContacts();
  showToast('🗑 Contact deleted');
}

// ── Render contacts grid ──────────────────────────────────────
function rContacts() {
  if(!DB.contacts) DB.contacts = [];
  var search = (document.getElementById('ct-search')||{}).value||'';
  search = search.toLowerCase();
  var grid = document.getElementById('contactsGrid');
  if(!grid) return;

  var filtered = DB.contacts.filter(function(ct){
    var matchType = _ctFilter==='all' || ct.type===_ctFilter || ct.type==='both' ||
                    (_ctFilter==='both' && ct.type==='both');
    if(_ctFilter !== 'all' && ct.type !== _ctFilter && ct.type !== 'both') matchType = false;
    if(_ctFilter === 'all') matchType = true;
    var matchSearch = !search ||
      (ct.name||'').toLowerCase().indexOf(search)>=0 ||
      (ct.nif||'').toLowerCase().indexOf(search)>=0 ||
      (ct.email||'').toLowerCase().indexOf(search)>=0 ||
      (ct.city||'').toLowerCase().indexOf(search)>=0;
    return matchType && matchSearch;
  });

  var countEl = document.getElementById('ct-count');
  if(countEl) countEl.textContent = filtered.length + ' contact' + (filtered.length!==1?'s':'');

  if(!filtered.length){
    grid.innerHTML = '<div style="color:var(--text3);font-size:13px;font-family:monospace;padding:32px;text-align:center;grid-column:1/-1;">' +
      (DB.contacts.length ? 'No contacts match your search.' : 'No contacts yet. Click &quot;+ New Contact&quot; to add your first client or supplier.') +
      '</div>';
    return;
  }

  var typeBadge = {client:'<span class="badge bb">Client</span>',supplier:'<span class="badge by">Supplier</span>',both:'<span class="badge ba">Client &amp; Supplier</span>'};

  grid.innerHTML = filtered.sort(function(a,b){return a.name.localeCompare(b.name);}).map(function(ct){
    var initials = ct.name.split(' ').map(function(w){return w[0];}).slice(0,2).join('').toUpperCase();
    var meta = [ct.nif, ct.city, ct.email].filter(Boolean).join(' · ');
    return '<div class="contact-card" onclick="openContactModal(\''+ct.type+'\','+ct.id+')">' +
      '<div class="contact-avatar">'+initials+'</div>' +
      '<div style="flex:1;min-width:0;">' +
        '<div class="contact-name">'+ct.name+'</div>' +
        '<div class="contact-meta">'+(meta||'No details added')+'</div>' +
      '</div>' +
      '<div class="contact-badge">'+(typeBadge[ct.type]||'')+'</div>' +
    '</div>';
  }).join('');
}

// ── Autocomplete for Sales/Purchase modals ────────────────────
function acSearch(inputId, listId, typeFilter) {
  var input = document.getElementById(inputId);
  var list  = document.getElementById(listId);
  if(!input || !list) return;
  var q = input.value.toLowerCase();

  if(!DB.contacts) DB.contacts = [];
  var matches = DB.contacts.filter(function(ct){
    var typeOk = typeFilter==='client'
      ? (ct.type==='client'||ct.type==='both')
      : typeFilter==='supplier'
      ? (ct.type==='supplier'||ct.type==='both')
      : true;
    var nameOk = !q || (ct.name||'').toLowerCase().indexOf(q)>=0 ||
                 (ct.nif||'').toLowerCase().indexOf(q)>=0;
    return typeOk && nameOk;
  }).slice(0, 8);

  if(!matches.length) { list.classList.remove('open'); return; }

  list.innerHTML = matches.map(function(ct){
    var meta = [ct.nif, ct.city].filter(Boolean).join(' · ');
    return '<div class="autocomplete-item" onmousedown="acSelect(\''+inputId+'\',\''+listId+'\',\''+ct.name.replace(/'/g,"\\'")+'\','+ct.id+')">' +
      '<div>'+ct.name+'</div>' +
      '<div class="ac-meta">'+(meta||ct.type)+'</div>' +
    '</div>';
  }).join('');
  list.classList.add('open');
}

function acSelect(inputId, listId, name, ctId) {
  var input = document.getElementById(inputId);
  if(input) input.value = name;
  closeAC(listId);
  // Auto-fill VAT if contact has preference
  var ct = DB.contacts.find(function(x){return x.id===ctId;});
  if(ct) {
    if(inputId==='s-cust' && ct.salesvat) {
      var vatEl = document.getElementById('s-vat');
      if(vatEl){ vatEl.value=ct.salesvat; calcS(); }
    }
    if(inputId==='p-sup' && ct.purchvat) {
      var vatEl2 = document.getElementById('p-vat');
      if(vatEl2){ vatEl2.value=ct.purchvat; calcP(); }
    }
  }
}

function closeAC(listId) {
  var list = document.getElementById(listId);
  if(list) list.classList.remove('open');
}

// contacts export handled inside getRows directly (see getRows function)

function renderAll(){rDash();rContacts();rSales();rPurch();rColl();rPay();rJE();rPL();rBS();rCF();}

init();

// ══════════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ══════════════════════════════════════════════════════════════════

// ── PDF EXPORT ────────────────────────────────────────────────────
function exportPDF(sectionId, title) {
  // Hide all pages, show only the target
  document.querySelectorAll('.page').forEach(function(p){p.style.display='none';});
  var target = document.getElementById('page-' + sectionId);
  target.style.display = 'block';
  // Set print title
  var oldTitle = document.title;
  document.title = 'FinLedger — ' + title + ' — ' + new Date().toLocaleDateString('en-GB');
  window.print();
  // Restore
  document.title = oldTitle;
  document.querySelectorAll('.page').forEach(function(p){p.style.display='';});
  target.classList.add('active');
}

// ── EXCEL EXPORT ──────────────────────────────────────────────────
// ── EXCEL/CSV EXPORT — via Python server (works in pywebview) ────
function getRows(type) {
  var rows=[], F;
  if(type==='sales'){
    rows.push(['Invoice #','Date','Customer','Description','VAT %','Net','VAT Amount','Total','Status','Method']);
    DB.sales.forEach(function(s){rows.push([s.num,s.date,s.customer,s.desc||'',s.vatRate,s.net,s.vatAmt,s.total,s.status,s.method]);});
  } else if(type==='purchases'){
    rows.push(['Invoice #','Date','Supplier','Description','Category','VAT %','Net','VAT Amount','Total','Status','Method']);
    DB.purch.forEach(function(p){rows.push([p.num,p.date,p.supplier,p.desc||'',p.cat,p.vatRate,p.net,p.vatAmt,p.total,p.status,p.method]);});
  } else if(type==='collections'){
    rows.push(['#','Date','Customer','Invoice Ref','Method','Amount','Notes']);
    DB.coll.forEach(function(c){rows.push([c.id,c.date,c.customer,c.ref||'',c.method,c.amount,c.notes||'']);});
  } else if(type==='payments'){
    rows.push(['#','Date','Supplier','Invoice Ref','Method','Amount','Notes']);
    DB.pay.forEach(function(p){rows.push([p.id,p.date,p.supplier,p.ref||'',p.method,p.amount,p.notes||'']);});
  } else if(type==='journal'){
    rows.push(['Entry #','Date','Type','Description','Account','Debit','Credit']);
    DB.je.forEach(function(je){je.lines.forEach(function(l,i){var acct=COA.find(function(a){return a.c===l.account;});rows.push([i===0?'JE-'+String(je.id).padStart(3,'0'):'',i===0?je.date:'',i===0?(je.sourceType||'manual').toUpperCase():'',i===0?je.desc:'',acct?acct.c+' - '+acct.n:l.account,l.debit||'',l.credit||'']);});});
  } else if(type==='pl'){
    F=cF();rows.push(['P&L — '+DB.co.name,''],['FY: '+DB.co.fy,''],['',''],['REVENUE',''],['Sales Revenue',F.rev]);
    if(F.jeR)rows.push(['Journal Revenue Adj.',F.jeR]);
    rows.push(['Total Revenue',F.totRev],['',''],['COGS',''],['Cost of Goods Sold',-F.cogs],['Gross Profit',F.rev-F.cogs],['',''],['OPERATING EXPENSES','']);
    Object.entries(F.opex).forEach(function(e){rows.push([e[0],-e[1]]);});
    rows.push(['Total OpEx',-F.toOpEx],['',''],['EBIT',F.ebit],['Journal Adj.',F.jeR-F.jeE],['NET INCOME',F.ni]);
  } else if(type==='bs'){
    F=cF();rows.push(['Balance Sheet — '+DB.co.name,''],['',''],['ASSETS',''],['Cash & Bank',F.cash],['Accounts Receivable',F.ar],['Total Assets',F.cash+F.ar],['',''],['LIABILITIES',''],['Accounts Payable',F.ap],['VAT Payable',Math.max(0,F.vatP)],['Total Liabilities',F.ap+Math.max(0,F.vatP)],['',''],['EQUITY',''],['Net Income',F.ni],['Total Equity',F.ni],['',''],['TOTAL LIAB. & EQUITY',F.ap+Math.max(0,F.vatP)+F.ni]);
  } else if(type==='cashflow'){
    F=cF();rows.push(['Cash Flow — '+DB.co.name,''],['',''],['OPERATING ACTIVITIES',''],['Cash received',F.totColl],['Cash paid',-F.totPay],['Net Operating CF',F.totColl-F.totPay],['',''],['INVESTING',''],['Net Investing CF',0],['',''],['FINANCING',''],['Net Financing CF',0],['',''],['NET CHANGE IN CASH',F.totColl-F.totPay],['Opening Balance',0],['Closing Balance',F.totColl-F.totPay]);
  } else if(type==='contacts'){
    rows.push(['Name','Type','NIF','Email','Phone','City','Country','IBAN','Payment Terms','VAT Sales','VAT Purchase','Notes']);
    (DB.contacts||[]).forEach(function(ct){
      rows.push([ct.name,ct.type,ct.nif||'',ct.email||'',ct.phone||'',ct.city||'',ct.country||'',ct.iban||'',ct.payterms||'',ct.salesvat||'',ct.purchvat||'',ct.notes||'']);
    });
  }
  return rows;
}

function rowsToCSV(rows) {
  // UTF-8 BOM so Excel opens it correctly
  return '\uFEFF' + rows.map(function(row){
    return row.map(function(v){
      var s = String(v===null||v===undefined?'':v);
      if(s.indexOf(',')>=0||s.indexOf('"')>=0||s.indexOf('\n')>=0) s='"'+s.replace(/"/g,'""')+'"';
      return s;
    }).join(',');
  }).join('\r\n');
}

function exportExcel(type) {
  var names={sales:'Sales_Invoices',purchases:'Purchase_Invoices',collections:'Collections',
    payments:'Payments',journal:'Journal_Entries',pl:'PL_Statement',bs:'Balance_Sheet',cashflow:'Cash_Flow'};
  var rows = getRows(type);
  if(!rows.length){alert('No data to export.');return;}
  var fname = 'FinLedger_'+(names[type]||type)+'_'+new Date().toISOString().slice(0,10)+'.csv';
  var csv   = rowsToCSV(rows);

  // ── Method 1: Standard browser download (works in Chrome/Firefox/Edge) ──
  // Try this first — works perfectly when accessed via http://localhost:8765
  try {
    var blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement('a');
    a.href        = url;
    a.download    = fname;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    // Check if download actually triggered (pywebview blocks it silently)
    var triggered = true;
    setTimeout(function(){
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
    // Give pywebview fallback after short delay
    setTimeout(function(){
      // If we are inside pywebview, the download won't have worked
      // so we also send to Python server as backup
      fetch('/export', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({filename: fname, content: csv})
      })
      .then(function(r){return r.json();})
      .then(function(res){
        if(res.ok){
          showToast('✅ Descargado: ' + fname);
        }
      })
      .catch(function(){
        // In real browser this will fail (no server needed) — that's fine
      });
    }, 400);
    showToast('✅ Descargando: ' + fname);
  } catch(e) {
    showToast('❌ Error al descargar: ' + e);
  }
}

// ── Toast notification ─────────────────────────────────────────────
function showToast(msg) {
  var t = document.getElementById('fl-toast');
  if(!t){
    t = document.createElement('div');
    t.id = 'fl-toast';
    t.style.cssText = 'position:fixed;bottom:28px;right:28px;background:#1e1e24;border:1px solid #2e2e38;color:#f0f0f4;padding:12px 20px;border-radius:10px;font-family:DM Sans,sans-serif;font-size:13px;z-index:9999;box-shadow:0 4px 24px rgba(0,0,0,.5);transition:opacity .3s;max-width:400px;';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._timer);
  t._timer = setTimeout(function(){t.style.opacity='0';}, 3500);
}
</script>

<!-- RECONCILE COLLECTION MODAL -->
<div class="overlay" id="ov-reconcile-coll">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Collect Payment</div><div class="mclose" onclick="closeOverlay('ov-reconcile-coll')">✕</div></div>
    <div class="mbody">
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
        <div id="rc-invoice-info" style="font-size:14px;color:var(--text);font-weight:500;"></div>
      </div>
      <div class="fgrid">
        <div class="fg"><label>Collection Date</label><input type="date" id="rc-date"></div>
        <div class="fg"><label>Payment Method</label>
          <select id="rc-method"><option value="bank">🏦 Bank Transfer</option><option value="cash">💵 Cash</option><option value="card">💳 Card</option><option value="other">📋 Other</option></select>
        </div>
        <div class="fg full"><label>Amount to Collect (€)</label><input type="number" id="rc-amount" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><input type="text" id="rc-notes" placeholder="Optional notes..."></div>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.06);border:1px solid rgba(200,255,0,.2);border-radius:7px;font-size:12px;color:var(--text3);">
        🔖 This will automatically create a <strong style="color:var(--accent);">Journal Entry</strong>: Dr. Cash / Cr. Accounts Receivable
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-reconcile-coll')">Cancel</button><button class="btn btn-primary" onclick="confirmCollect()">✓ Collect & Post</button></div>
  </div>
</div>

<!-- RECONCILE PAYMENT MODAL -->
<div class="overlay" id="ov-reconcile-pay">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Payment</div><div class="mclose" onclick="closeOverlay('ov-reconcile-pay')">✕</div></div>
    <div class="mbody">
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
        <div id="rp-invoice-info" style="font-size:14px;color:var(--text);font-weight:500;"></div>
      </div>
      <div class="fgrid">
        <div class="fg"><label>Payment Date</label><input type="date" id="rp-date"></div>
        <div class="fg"><label>Payment Method</label>
          <select id="rp-method"><option value="bank">🏦 Bank Transfer</option><option value="cash">💵 Cash</option><option value="card">💳 Card</option><option value="other">📋 Other</option></select>
        </div>
        <div class="fg full"><label>Amount to Pay (€)</label><input type="number" id="rp-amount" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><input type="text" id="rp-notes" placeholder="Optional notes..."></div>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.06);border:1px solid rgba(200,255,0,.2);border-radius:7px;font-size:12px;color:var(--text3);">
        🔖 This will automatically create a <strong style="color:var(--accent);">Journal Entry</strong>: Dr. Accounts Payable / Cr. Cash
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-reconcile-pay')">Cancel</button><button class="btn btn-primary" onclick="confirmPay()">✓ Pay & Post</button></div>
  </div>
</div>

<!-- ═══════════════════ CONTACT MODAL ═══════════════════ -->
<div class="overlay" id="ov-contact">
  <div class="modal" style="width:min(700px,95vw);">
    <div class="mhdr">
      <div>
        <div class="mtitle" id="ct-modal-title">New Contact</div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:2px;">
          <div class="contact-type-toggle" style="margin-top:8px;">
            <button class="ct-btn active" id="ct-type-client"   onclick="setCtType('client')">Client</button>
            <button class="ct-btn"        id="ct-type-supplier" onclick="setCtType('supplier')">Supplier</button>
            <button class="ct-btn"        id="ct-type-both"     onclick="setCtType('both')">Both</button>
          </div>
        </div>
      </div>
      <div class="mclose" onclick="closeOverlay('ov-contact')">✕</div>
    </div>
    <div class="mbody">
      <!-- Contact tabs -->
      <div class="contact-tabs">
        <div class="contact-tab active" onclick="ctTab('basic')">📋 Basic</div>
        <div class="contact-tab" onclick="ctTab('accounts')">🏦 Accounts</div>
        <div class="contact-tab" onclick="ctTab('preferences')">⚙ Preferences</div>
        <div class="contact-tab" onclick="ctTab('accounting')">📊 Accounting</div>
      </div>

      <!-- BASIC -->
      <div class="contact-panel active" id="ctpanel-basic">
        <div class="fgrid">
          <div class="fg full"><label>Full Name / Company Name</label><input type="text" id="ct-name" placeholder="e.g. Balenciaga Spain SL."></div>
          <div class="fg"><label>NIF / VAT Number</label><input type="text" id="ct-nif" placeholder="e.g. B66408139"></div>
          <div class="fg"><label>Trade Name (optional)</label><input type="text" id="ct-tradename" placeholder="Trade name"></div>
          <div class="fg full"><label>Address</label><input type="text" id="ct-addr" placeholder="e.g. Paseo Gracia 56, Module B Floor 6"></div>
          <div class="fg"><label>City</label><input type="text" id="ct-city" placeholder="Barcelona"></div>
          <div class="fg"><label>Postal Code</label><input type="text" id="ct-postal" placeholder="08007"></div>
          <div class="fg"><label>Province / State</label><input type="text" id="ct-province" placeholder="Barcelona"></div>
          <div class="fg"><label>Country</label><input type="text" id="ct-country" placeholder="Spain"></div>
          <div class="fg"><label>Email</label><input type="email" id="ct-email" placeholder="invoices@company.com"></div>
          <div class="fg"><label>Phone</label><input type="text" id="ct-phone" placeholder="+34 932 956 184"></div>
          <div class="fg"><label>Mobile</label><input type="text" id="ct-mobile" placeholder="+34 616 519 247"></div>
          <div class="fg"><label>Website</label><input type="text" id="ct-web" placeholder="www.company.com"></div>
        </div>
      </div>

      <!-- ACCOUNTS -->
      <div class="contact-panel" id="ctpanel-accounts">
        <div class="fgrid">
          <div class="fg full"><label>IBAN</label><input type="text" id="ct-iban" placeholder="ES91 2100 0418 4502 0005 1332"></div>
          <div class="fg"><label>BIC / SWIFT</label><input type="text" id="ct-bic" placeholder="CAIXESBBXXX"></div>
          <div class="fg"><label>Bank Name</label><input type="text" id="ct-bank" placeholder="CaixaBank"></div>
          <div class="fg full"><label>Payment Terms</label>
            <select id="ct-payterms">
              <option value="immediate">Immediate</option>
              <option value="15days">15 days</option>
              <option value="30days" selected>30 days</option>
              <option value="45days">45 days</option>
              <option value="60days">60 days</option>
              <option value="90days">90 days</option>
            </select>
          </div>
          <div class="fg"><label>Credit Limit (€)</label><input type="number" id="ct-creditlimit" placeholder="0.00" step="0.01"></div>
          <div class="fg"><label>Currency</label>
            <select id="ct-currency">
              <option value="EUR" selected>EUR — Euro</option>
              <option value="USD">USD — US Dollar</option>
              <option value="GBP">GBP — British Pound</option>
              <option value="CHF">CHF — Swiss Franc</option>
            </select>
          </div>
        </div>
      </div>

      <!-- PREFERENCES -->
      <div class="contact-panel" id="ctpanel-preferences">
        <div class="fgrid">
          <div class="fg"><label>Default Sales VAT (%)</label>
            <select id="ct-salesvat">
              <option value="0">0%</option>
              <option value="4">4% (Reduced)</option>
              <option value="10">10% (Reduced)</option>
              <option value="21" selected>21% (General)</option>
            </select>
          </div>
          <div class="fg"><label>Default Purchase VAT (%)</label>
            <select id="ct-purchvat">
              <option value="0">0%</option>
              <option value="4">4% (Reduced)</option>
              <option value="10">10% (Reduced)</option>
              <option value="21" selected>21% (General)</option>
            </select>
          </div>
          <div class="fg"><label>Invoice Language</label>
            <select id="ct-lang">
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
          <div class="fg"><label>Send Invoices By</label>
            <select id="ct-invoiceby">
              <option value="email">Email</option>
              <option value="post">Post</option>
              <option value="both">Email &amp; Post</option>
            </select>
          </div>
          <div class="fg full"><label>Notes / Tags</label><textarea id="ct-notes" placeholder="Internal notes about this contact..."></textarea></div>
        </div>
      </div>

      <!-- ACCOUNTING -->
      <div class="contact-panel" id="ctpanel-accounting">
        <div class="fgrid">
          <div class="fg full">
            <label>Client / Debtor Account</label>
            <select id="ct-debtacc">
              <option value="">— Select account —</option>
              <option value="43000001">43000001 — Clients (General)</option>
              <option value="43000002">43000002 — Clients (EU)</option>
              <option value="43000003">43000003 — Clients (Non-EU)</option>
              <option value="1100">1100 — Accounts Receivable</option>
            </select>
          </div>
          <div class="fg full">
            <label>Supplier / Creditor Account</label>
            <select id="ct-credacc">
              <option value="">— Select account —</option>
              <option value="41000001">41000001 — Suppliers (General)</option>
              <option value="41000002">41000002 — Suppliers (EU)</option>
              <option value="41000003">41000003 — Suppliers (Non-EU)</option>
              <option value="2000">2000 — Accounts Payable</option>
            </select>
          </div>
          <div class="fg"><label>Sales Tax Rate</label>
            <select id="ct-salestax">
              <option value="IVA21">IVA 21% (General)</option>
              <option value="IVA10">IVA 10% (Reduced)</option>
              <option value="IVA4">IVA 4% (Super-reduced)</option>
              <option value="IVA0">IVA 0% (Exempt)</option>
            </select>
          </div>
          <div class="fg"><label>Purchase Tax Rate</label>
            <select id="ct-purchtax">
              <option value="IVA21">IVA 21% (General)</option>
              <option value="IVA10">IVA 10% (Reduced)</option>
              <option value="IVA4">IVA 4% (Super-reduced)</option>
              <option value="IVA0">IVA 0% (Exempt)</option>
            </select>
          </div>
          <div class="fg full"><label>Custom Accounting Code (optional)</label><input type="text" id="ct-acccode" placeholder="e.g. 43000168"></div>
        </div>
        <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.05);border:1px solid rgba(200,255,0,.15);border-radius:7px;font-size:12px;color:var(--text3);">
          💡 These accounting codes will be used automatically when generating Journal Entries for this contact.
        </div>
      </div>

    </div>
    <div class="mfoot">
      <button class="btn btn-danger btn-sm" id="ct-delete-btn" onclick="deleteContact()" style="margin-right:auto;display:none;">🗑 Delete</button>
      <button class="btn btn-ghost" onclick="closeOverlay('ov-contact')">Cancel</button>
      <button class="btn btn-primary" onclick="saveContact()">Save Contact</button>
    </div>
  </div>
</div>
</body>
</html>"""

_store = {}
_lock  = threading.Lock()


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/load":
            self._load()
        elif self.path == "/health":
            self._text("ok")
        else:
            self._app()

    def do_POST(self):
        if self.path == "/save":
            self._save()
        elif self.path == "/export":
            self._export()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _app(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self._cors()
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def _text(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self._cors()
        self.end_headers()
        self.wfile.write(msg.encode())

    def _load(self):
        with _lock:
            data = _store.get("db")
        if data:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(204)
            self._cors()
            self.end_headers()

    def _save(self):
        try:
            n    = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            data = json.loads(body)
            with _lock:
                _store["db"] = data
            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _export(self):
        try:
            n       = int(self.headers.get("Content-Length", 0))
            body    = self.rfile.read(n)
            payload = json.loads(body)
            fname   = payload.get("filename", "export.csv")
            content = payload.get("content", "")
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
            self._cors()
            self.end_headers()
            self.wfile.write(content.encode("utf-8-sig"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, fmt, *args):
        if args:
            print(f"[{self.client_address[0]}] {args[0]}")


def main():
    socketserver.TCPServer.allow_reuse_address = True
    print(f"\n  FinLedger ready on port {PORT}")
    print(f"  Open: http://localhost:{PORT}\n")
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()

"""
FinLedger - Professional Accounting System
==========================================
Railway.app web deployment version.
Run locally:  python main.py
Deploy:       Push to GitHub, connect to Railway.app
"""

import http.server
import socketserver
import threading
import os
import json

PORT = int(os.environ.get("PORT", 8765))

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>FinLedger</title>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500;600&display=swap" rel="stylesheet">
<style>
:root{
  --bg:#0f0f11;--surface:#16161a;--surface2:#1e1e24;--surface3:#26262e;
  --border:#2e2e38;--accent:#c8ff00;--text:#f0f0f4;--text2:#9090a8;--text3:#5a5a72;
  --green:#4ade80;--red:#f87171;--blue:#60a5fa;--purple:#a78bfa;--yellow:#ffd93d;
  --radius:10px;
}
/* LIGHT MODE */
body.light-mode{
  --bg:#f4f5f7;--surface:#ffffff;--surface2:#f0f1f3;--surface3:#e8e9eb;
  --border:#dde0e4;--accent:#0057ff;--text:#1a1d23;--text2:#5c6070;--text3:#9198a6;
  --green:#16a34a;--red:#dc2626;--blue:#2563eb;--purple:#7c3aed;--yellow:#d97706;
}
body.light-mode .sidebar{background:#ffffff;border-right:1px solid var(--border);}
body.light-mode .topbar{background:#ffffff;}
body.light-mode .nav-item.active{background:rgba(0,87,255,.06);}
body.light-mode input,body.light-mode select,body.light-mode textarea{background:#f8f9fa;color:var(--text);}
body.light-mode .modal{background:#ffffff;}
body.light-mode .kpi-card,body.light-mode .card,body.light-mode .chart-area{background:#ffffff;}
body.light-mode .btn-ghost{background:#f0f1f3;color:var(--text2);}
body.light-mode .user-card{background:#f4f5f7;}
body.light-mode .date-filter-bar{background:#f0f1f3;}
body.light-mode .totbar{background:#f0f1f3;}
body.light-mode .rtbl tr.rh td{background:#f0f1f3;}
body.light-mode .autocomplete-list{background:#ffffff;}
body.light-mode th{color:var(--text3);}
body.light-mode td{color:var(--text2);}
body.light-mode tr:hover td{background:#f4f5f7;color:var(--text);}
/* Theme toggle button */
.theme-toggle{display:flex;align-items:center;gap:8px;background:var(--surface2);border:1px solid var(--border);border-radius:20px;padding:4px 6px;cursor:pointer;transition:all .2s;}
.theme-toggle-track{width:36px;height:20px;background:var(--surface3);border-radius:10px;position:relative;transition:background .2s;}
.theme-toggle-track.on{background:var(--accent);}
.theme-toggle-thumb{width:16px;height:16px;background:#fff;border-radius:50%;position:absolute;top:2px;left:2px;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3);}
.theme-toggle-track.on .theme-toggle-thumb{transform:translateX(16px);}
.theme-toggle-label{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;min-height:100vh;display:flex;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:232px;min-width:232px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:0;}
.logo-area{padding:22px 20px 18px;border-bottom:1px solid var(--border);}
.logo-title{font-family:'DM Serif Display',serif;font-size:22px;color:var(--accent);letter-spacing:-.5px;}
.logo-sub{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;margin-top:2px;}
.nav{padding:16px 0;flex:1;overflow-y:auto;}
.nav-sec{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;padding:10px 20px 5px;}
.nav-item{display:flex;align-items:center;gap:10px;padding:9px 20px;cursor:pointer;color:var(--text2);border-left:2px solid transparent;transition:all .15s;font-size:13px;font-weight:500;user-select:none;}
.nav-item:hover{color:var(--text);background:var(--surface2);}
.nav-item.active{color:var(--accent);border-left-color:var(--accent);background:rgba(200,255,0,.06);}
.nav-icon{font-size:14px;width:18px;text-align:center;flex-shrink:0;}

/* ── USER PROFILE CARD (sidebar bottom) ── */
.sidebar-foot{padding:14px 14px;border-top:1px solid var(--border);}
.user-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:12px;display:flex;align-items:center;gap:10px;cursor:pointer;transition:border-color .15s;}
.user-card:hover{border-color:var(--accent);}
.user-avatar{width:36px;height:36px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:14px;font-weight:600;color:#0f0f11;flex-shrink:0;background:var(--accent);}
.user-info{flex:1;min-width:0;}
.user-name{font-weight:600;font-size:12px;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-role{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-co{font-size:10px;color:var(--text3);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-gear{color:var(--text3);font-size:13px;flex-shrink:0;}

/* ── MAIN ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);padding:0 28px;height:56px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.topbar-left{}
.page-title{font-family:'DM Serif Display',serif;font-size:20px;}
.breadcrumb{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;}
.topbar-right{display:flex;align-items:center;gap:10px;}
.greeting{font-size:13px;color:var(--text2);}
.greeting strong{color:var(--text);font-weight:600;}
.server-badge{background:rgba(200,255,0,.1);border:1px solid rgba(200,255,0,.3);color:var(--accent);padding:4px 12px;border-radius:20px;font-size:11px;font-family:'DM Mono',monospace;}

/* ── BUTTONS ── */
.btn{padding:7px 16px;border-radius:7px;border:none;cursor:pointer;font-family:'DM Sans',sans-serif;font-size:13px;font-weight:500;transition:all .16s;}
.btn-primary{background:var(--accent);color:#0f0f11;}
.btn-primary:hover{background:#d4ff26;transform:translateY(-1px);}
.btn-ghost{background:var(--surface2);color:var(--text2);border:1px solid var(--border);}
.btn-ghost:hover{color:var(--text);}
.btn-danger{background:rgba(248,113,113,.15);color:var(--red);border:1px solid rgba(248,113,113,.3);}
.btn-sm{padding:5px 11px;font-size:12px;}

/* ── CONTENT ── */
.content{flex:1;overflow-y:auto;padding:28px;}
.content::-webkit-scrollbar{width:6px;}
.content::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
.page{display:none;}
.page.active{display:block;animation:fadeIn .2s ease;}
@keyframes fadeIn{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

/* ── KPI CARDS ── */
.kpi-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;}
.kpi-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:18px 20px;position:relative;overflow:hidden;}
.kpi-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;}
.kpi-card.g::before{background:var(--green);}
.kpi-card.r::before{background:var(--red);}
.kpi-card.b::before{background:var(--blue);}
.kpi-card.a::before{background:var(--accent);}
.card-title{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;}
.card-value{font-family:'DM Serif Display',serif;font-size:28px;}
.card-delta{font-size:12px;margin-top:4px;color:var(--text3);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}

/* ── TABLES ── */
.tbl-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;}
th{padding:10px 14px;text-align:left;font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.2px;border-bottom:1px solid var(--border);white-space:nowrap;}
td{padding:11px 14px;border-bottom:1px solid rgba(46,46,56,.5);font-size:13px;color:var(--text2);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);color:var(--text);}
.amt{font-family:'DM Mono',monospace;text-align:right;}
.pos{color:var(--green)!important;}
.neg{color:var(--red)!important;}

/* ── BADGES ── */
.badge{display:inline-flex;align-items:center;padding:2px 9px;border-radius:20px;font-size:10px;font-weight:600;font-family:'DM Mono',monospace;text-transform:uppercase;}
.bg{background:rgba(74,222,128,.12);color:var(--green);}
.br{background:rgba(248,113,113,.12);color:var(--red);}
.bb{background:rgba(96,165,250,.12);color:var(--blue);}
.by{background:rgba(255,217,61,.12);color:var(--yellow);}
.ba{background:rgba(200,255,0,.12);color:var(--accent);}
.bp{background:rgba(167,139,250,.12);color:var(--purple);}

/* ── FORMS ── */
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:14px;}
.fgrid3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:14px;}
.fg{display:flex;flex-direction:column;gap:5px;}
.fg.full{grid-column:1/-1;}
label{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;}
input,select,textarea{background:var(--surface2);border:1px solid var(--border);border-radius:7px;padding:9px 12px;color:var(--text);font-family:'DM Sans',sans-serif;font-size:13px;transition:border .15s;width:100%;outline:none;}
input:focus,select:focus,textarea:focus{border-color:var(--accent);box-shadow:0 0 0 2px rgba(200,255,0,.1);}
select option{background:var(--surface2);}
textarea{resize:vertical;min-height:72px;}

/* ── LAYOUT HELPERS ── */
.row{display:flex;gap:16px;}
.col{flex:1;}
.col2{flex:2;}
.divider{height:1px;background:var(--border);margin:20px 0;}
.sec-hdr{display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;}
.sec-title{font-family:'DM Serif Display',serif;font-size:17px;}
.sec-sub{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;}
.tabs{display:flex;gap:2px;background:var(--surface2);border-radius:8px;padding:3px;width:fit-content;margin-bottom:20px;}
.tab{padding:7px 18px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);transition:all .15s;}
.tab.active{background:var(--surface3);color:var(--text);}
.totbar{display:flex;gap:24px;padding:14px 20px;background:var(--surface2);border-radius:8px;border:1px solid var(--border);margin-bottom:16px;flex-wrap:wrap;}
.tot-item label{display:block;font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
.tot-item span{font-family:'DM Serif Display',serif;font-size:18px;}

/* ── CHART ── */
.chart-area{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}
.chart-bars{display:flex;align-items:flex-end;gap:8px;height:160px;}
.bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end;}
.bar{width:100%;border-radius:4px 4px 0 0;min-height:4px;transition:all .3s;}
.bar:hover{filter:brightness(1.2);}
.bar-lbl{font-size:9px;color:var(--text3);font-family:'DM Mono',monospace;}

/* ── REPORT TABLES ── */
.rtbl{width:100%;border-collapse:collapse;}
.rtbl tr.rh td{background:var(--surface2);color:var(--text);font-weight:600;font-size:12px;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;padding:8px 14px;}
.rtbl tr.rd td{padding:8px 14px;color:var(--text2);font-size:13px;border-bottom:1px solid rgba(46,46,56,.4);}
.rtbl tr.rd:hover td{background:rgba(255,255,255,.02);}
.rtbl tr.rs td{padding:9px 14px;font-weight:600;color:var(--text);border-top:1px solid var(--border);}
.rtbl tr.rt td{padding:11px 14px;font-family:'DM Serif Display',serif;font-size:16px;color:var(--accent);border-top:2px solid var(--accent);background:rgba(200,255,0,.04);}
.rtbl .ind{padding-left:30px!important;}
.rtbl .num{font-family:'DM Mono',monospace;text-align:right;}

/* ── JE LINES ── */
.je-line{display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:10px;align-items:center;margin-bottom:8px;}

/* ── OVERLAYS / MODALS ── */
.overlay{position:fixed;inset:0;background:rgba(0,0,0,.72);z-index:100;display:none;align-items:center;justify-content:center;backdrop-filter:blur(5px);}
.overlay.open{display:flex;}
.modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;width:min(620px,95vw);max-height:90vh;overflow-y:auto;box-shadow:0 8px 50px rgba(0,0,0,.6);}
.modal.wide{width:min(740px,95vw);}
.modal.xwide{width:min(820px,95vw);}
.mhdr{padding:22px 26px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.mtitle{font-family:'DM Serif Display',serif;font-size:20px;}
.mclose{width:30px;height:30px;border-radius:7px;background:var(--surface2);border:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:15px;}
.mclose:hover{color:var(--text);}
.mbody{padding:26px;}
.mfoot{padding:16px 26px;border-top:1px solid var(--border);display:flex;justify-content:flex-end;gap:10px;}
.modal::-webkit-scrollbar{width:4px;}
.modal::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}

/* ── SETTINGS TABS ── */
.set-tabs{display:flex;border-bottom:1px solid var(--border);margin-bottom:22px;gap:0;}
.set-tab{padding:10px 20px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);border-bottom:2px solid transparent;transition:all .15s;margin-bottom:-1px;}
.set-tab:hover{color:var(--text);}
.set-tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.set-panel{display:none;}
.set-panel.active{display:block;}

/* ── AVATAR PICKER ── */
.avatar-row{display:flex;align-items:center;gap:16px;margin-bottom:6px;}
.avatar-big{width:64px;height:64px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:24px;font-weight:700;color:#0f0f11;background:var(--accent);flex-shrink:0;}
.color-swatches{display:flex;gap:8px;flex-wrap:wrap;}
.swatch{width:26px;height:26px;border-radius:50%;cursor:pointer;border:2px solid transparent;transition:all .15s;}
.swatch:hover,.swatch.sel{border-color:var(--text);transform:scale(1.15);}

/* ── SECTION DIVIDER LABEL ── */
.set-section-label{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;margin-top:4px;}

/* ── INFO ROW ── */
.info-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(46,46,56,.5);}
.info-row:last-child{border-bottom:none;}
.info-label{font-size:12px;color:var(--text3);}
.info-val{font-size:13px;color:var(--text);font-family:'DM Mono',monospace;}

/* ── EXPORT ICON BUTTONS ── */
.btn-xls{background:rgba(74,222,128,.12);color:#4ade80;border:1px solid rgba(74,222,128,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-xls:hover{background:rgba(74,222,128,.28);transform:translateY(-1px);}
.btn-pdf2{background:rgba(248,113,113,.12);color:#f87171;border:1px solid rgba(248,113,113,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-pdf2:hover{background:rgba(248,113,113,.28);transform:translateY(-1px);}
/* contacts */
.contact-type-toggle{display:flex;gap:4px;background:var(--surface3);border-radius:7px;padding:3px;}
.ct-btn{padding:5px 14px;border-radius:5px;cursor:pointer;font-size:12px;font-weight:600;color:var(--text2);border:none;background:transparent;font-family:'DM Sans',sans-serif;transition:all .15s;}
.ct-btn.active{background:var(--surface);color:var(--text);box-shadow:0 1px 4px rgba(0,0,0,.3);}
.contact-tabs{display:flex;border-bottom:1px solid var(--border);margin-bottom:18px;}
.contact-tab{padding:9px 18px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);border-bottom:2px solid transparent;transition:all .15s;margin-bottom:-1px;}
.contact-tab:hover{color:var(--text);}
.contact-tab.active{color:var(--accent);border-bottom-color:var(--accent);}
.contact-panel{display:none;}
.contact-panel.active{display:block;}
.contact-card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:16px 18px;display:flex;align-items:center;gap:14px;cursor:pointer;transition:all .15s;margin-bottom:8px;}
.contact-card:hover{border-color:var(--accent);background:var(--surface2);}
.contact-avatar{width:40px;height:40px;border-radius:50%;background:var(--surface3);display:flex;align-items:center;justify-content:center;font-family:'DM Serif Display',serif;font-size:15px;font-weight:700;color:var(--accent);flex-shrink:0;border:1px solid var(--border);}
.contact-name{font-weight:600;font-size:14px;color:var(--text);}
.contact-meta{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:2px;}
.contact-badge{margin-left:auto;flex-shrink:0;}
.contacts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}
/* autocomplete dropdown */
.autocomplete-wrap{position:relative;}
.autocomplete-list{position:absolute;top:100%;left:0;right:0;background:var(--surface);border:1px solid var(--accent);border-top:none;border-radius:0 0 7px 7px;z-index:200;max-height:200px;overflow-y:auto;display:none;}
.autocomplete-list.open{display:block;}
.autocomplete-item{padding:9px 12px;cursor:pointer;font-size:13px;color:var(--text2);border-bottom:1px solid rgba(46,46,56,.4);}
.autocomplete-item:hover{background:var(--surface2);color:var(--text);}
.autocomplete-item:last-child{border-bottom:none;}
.autocomplete-item .ac-meta{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:1px;}
/* date filter bar */
.date-filter-bar{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;margin-bottom:16px;flex-wrap:wrap;}
.date-filter-bar label{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin:0;}
.date-filter-bar input{width:140px;padding:6px 10px;font-size:12px;background:var(--surface3);border:1px solid var(--border);border-radius:6px;color:var(--text);}
.date-filter-bar input:focus{border-color:var(--accent);}
.filter-active-badge{background:rgba(200,255,0,.15);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:3px 10px;border-radius:20px;font-size:10px;font-family:'DM Mono',monospace;font-weight:600;}
/* reconcile button */
.btn-reconcile{background:rgba(200,255,0,.12);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;transition:all .15s;}
.btn-reconcile:hover{background:rgba(200,255,0,.22);}
.btn-reconcile.done{background:rgba(74,222,128,.1);color:#4ade80;border-color:rgba(74,222,128,.3);cursor:default;}
/* pending badge on sales/purch rows */
.needs-coll{background:rgba(255,217,61,.1);border-left:3px solid var(--yellow);}
.fully-coll{background:rgba(74,222,128,.05);border-left:3px solid rgba(74,222,128,.3);}
@media print{
  .sidebar,.topbar,.overlay,.export-bar,.btn,.btn-primary,.btn-danger,.btn-ghost{display:none!important;}
  .main{overflow:visible!important;}
  .content{overflow:visible!important;padding:0!important;}
  .page{display:block!important;}
  body{background:#fff!important;color:#000!important;}
  table{border-collapse:collapse!important;}
  th,td{border:1px solid #ccc!important;color:#000!important;background:#fff!important;font-size:11px!important;}
  .rtbl tr.rh td{background:#f0f0f0!important;color:#000!important;}
  .rtbl tr.rt td{background:#e8ffe8!important;color:#000!important;}
  .pos{color:#008000!important;}
  .neg{color:#cc0000!important;}
  .amt{font-family:monospace!important;}
}
</style>
</head>
<body>

<!-- ═══════════════════════════════════════════ SIDEBAR ═══ -->
<nav class="sidebar">
  <div class="logo-area">
    <div class="logo-title">FinLedger</div>
    <div class="logo-sub">Accounting System</div>
  </div>

  <div class="nav">
    <div class="nav-sec">Overview</div>
    <div class="nav-item active" onclick="nav('dashboard')"><span class="nav-icon">▦</span>Dashboard</div>

    <div class="nav-sec">Operations</div>
    <div class="nav-item" onclick="nav('contacts')"><span class="nav-icon">👥</span>Contacts</div>
    <div class="nav-item" onclick="nav('sales')"><span class="nav-icon">↑</span>Sales</div>
    <div class="nav-item" onclick="nav('purchases')"><span class="nav-icon">↓</span>Purchases</div>
    <div class="nav-item" onclick="nav('collections')"><span class="nav-icon">◎</span>Collections</div>
    <div class="nav-item" onclick="nav('payments')"><span class="nav-icon">◉</span>Payments</div>
    <div class="nav-item" onclick="nav('journal')"><span class="nav-icon">≡</span>Journal Entries</div>

    <div class="nav-sec">Reports</div>
    <div class="nav-item" onclick="nav('pl')"><span class="nav-icon">◈</span>P&amp;L Statement</div>
    <div class="nav-item" onclick="nav('bs')"><span class="nav-icon">⊞</span>Balance Sheet</div>
    <div class="nav-item" onclick="nav('cf')"><span class="nav-icon">⟳</span>Cash Flow</div>
  </div>

  <!-- USER CARD -->
  <div class="sidebar-foot">
    <div class="user-card" onclick="openSettings('user')" title="Open Settings">
      <div class="user-avatar" id="sideAvatarBg"><span id="sideAvatarInitials">PK</span></div>
      <div class="user-info">
        <div class="user-name" id="sideUserName">Previt Ketsia</div>
        <div class="user-role" id="sideUserRole">Chief Accountant</div>
        <div class="user-co" id="sideUserCo">My Company Ltd.</div>
      </div>
      <div class="user-gear">⚙</div>
    </div>
  </div>
</nav>

<!-- ═══════════════════════════════════════════ MAIN ═══════ -->
<div class="main">
  <!-- TOPBAR -->
  <div class="topbar">
    <div class="topbar-left">
      <div class="page-title" id="pgTitle">Dashboard</div>
      <div class="breadcrumb" id="pgCrumb">FinLedger / Overview</div>
    </div>
    <div class="topbar-right">
      <div class="greeting">Welcome back, <strong id="topGreeting">Previt Ketsia</strong></div>
      <div class="server-badge">● localhost:8765</div>
      <div class="theme-toggle" onclick="toggleTheme()" title="Toggle Dark/Light mode">
        <div class="theme-toggle-track" id="themeTrack"><div class="theme-toggle-thumb"></div></div>
        <span class="theme-toggle-label" id="themeLabel">Dark</span>
      </div>
      <button class="btn btn-ghost" onclick="openSettings('company')">⚙ Settings</button>
    </div>
  </div>

  <!-- CONTENT -->
  <div class="content">

    <!-- ══ DASHBOARD ══ -->
    <div class="page active" id="page-dashboard">
      <div class="kpi-grid">
        <div class="kpi-card g"><div class="card-title">Total Revenue</div><div class="card-value" id="kpi-rev">€0</div><div class="card-delta">Net sales + adjustments</div></div>
        <div class="kpi-card r"><div class="card-title">Total Expenses</div><div class="card-value" id="kpi-exp">€0</div><div class="card-delta">COGS + OpEx</div></div>
        <div class="kpi-card a"><div class="card-title">Net Income</div><div class="card-value" id="kpi-ni">€0</div><div class="card-delta">Revenue − Expenses</div></div>
        <div class="kpi-card b"><div class="card-title">Cash Position</div><div class="card-value" id="kpi-cash">€0</div><div class="card-delta">Collections − Payments</div></div>
      </div>
      <div class="row">
        <div class="col2">
          <div class="chart-area">
            <div class="sec-hdr"><div><div class="sec-title">Revenue vs Expenses</div><div class="sec-sub">Monthly overview</div></div></div>
            <div class="chart-bars" id="chartBars"><div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:'DM Mono',monospace;">Add transactions to see chart</div></div>
            <div style="display:flex;gap:16px;margin-top:12px;">
              <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text3);"><span style="width:10px;height:10px;background:var(--green);border-radius:2px;display:inline-block;"></span>Revenue</div>
              <div style="display:flex;align-items:center;gap:6px;font-size:11px;color:var(--text3);"><span style="width:10px;height:10px;background:var(--red);border-radius:2px;display:inline-block;"></span>Expenses</div>
            </div>
          </div>
        </div>
        <div class="col">
          <div class="chart-area" style="height:100%;">
            <div class="card-title">Quick Stats</div>
            <div style="margin-top:16px;display:flex;flex-direction:column;gap:14px;">
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Accounts Receivable</span><span class="badge bb" id="qs-ar">€0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Accounts Payable</span><span class="badge by" id="qs-ap">€0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Sales Invoices</span><span class="badge bg" id="qs-sc">0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Purchase Invoices</span><span class="badge br" id="qs-pc">0</span></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Journal Entries</span><span class="badge ba" id="qs-jec">0</span></div>
              <div style="height:1px;background:var(--border);"></div>
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Net Margin</span><span style="font-family:'DM Mono',monospace;" id="qs-mg">—</span></div>
            </div>
          </div>
        </div>
      </div>
      <div style="margin-top:16px;">
        <div class="chart-area">
          <div class="sec-hdr"><div class="sec-title">Recent Transactions</div><div class="sec-sub">Last 10 entries</div></div>
          <div class="tbl-wrap"><table><thead><tr><th>Date</th><th>Type</th><th>Description</th><th>Party</th><th>Amount</th><th>Status</th></tr></thead><tbody id="recentTx"><tr><td colspan="6" style="text-align:center;color:var(--text3);padding:24px;">No transactions yet.</td></tr></tbody></table></div>
        </div>
      </div>
    </div>

    <!-- ══ CONTACTS ══ -->
    <div class="page" id="page-contacts">
      <div class="sec-hdr">
        <div><div class="sec-title">Contacts</div><div class="sec-sub">Clients &amp; Suppliers directory</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('contacts')" title="Export Excel">📊</button>
          <button class="btn btn-primary" onclick="openContactModal()">+ New Contact</button>
        </div>
      </div>
      <!-- Filter bar -->
      <div style="display:flex;gap:10px;margin-bottom:16px;align-items:center;flex-wrap:wrap;">
        <input type="text" id="ct-search" placeholder="🔍  Search by name, NIF, email..." style="max-width:300px;" oninput="rContacts()">
        <div class="contact-type-toggle">
          <button class="ct-btn active" id="ctf-all"    onclick="setCtFilter('all')">All</button>
          <button class="ct-btn"        id="ctf-client" onclick="setCtFilter('client')">Clients</button>
          <button class="ct-btn"        id="ctf-supplier" onclick="setCtFilter('supplier')">Suppliers</button>
          <button class="ct-btn"        id="ctf-both"   onclick="setCtFilter('both')">Both</button>
        </div>
        <span id="ct-count" style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;"></span>
      </div>
      <!-- Contacts grid -->
      <div class="contacts-grid" id="contactsGrid">
        <div style="color:var(--text3);font-size:13px;font-family:'DM Mono',monospace;padding:32px;text-align:center;grid-column:1/-1;">
          No contacts yet. Click "+ New Contact" to add your first client or supplier.
        </div>
      </div>
    </div>

    <!-- ══ SALES ══ -->
    <div class="page" id="page-sales">
      <div class="sec-hdr"><div><div class="sec-title">Sales Invoices</div><div class="sec-sub">Record customer invoices</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('sales')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('sales','Sales Invoices')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-sale')">+ New Invoice</button></div></div>
      <div class="totbar">
        <div class="tot-item"><label>Invoiced</label><span id="s-tot" style="color:var(--green);">€0.00</span></div>
        <div class="tot-item"><label>Collected</label><span id="s-coll" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/R</label><span id="s-ar" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>Count</label><span id="s-cnt" style="color:var(--text2);">0</span></div>
      </div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Customer</th><th>Description</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="salesTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ PURCHASES ══ -->
    <div class="page" id="page-purchases">
      <div class="sec-hdr"><div><div class="sec-title">Purchase Invoices</div><div class="sec-sub">Record supplier invoices</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('purchases')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('purchases','Purchase Invoices')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-purch')">+ New Purchase</button></div></div>
      <div class="totbar">
        <div class="tot-item"><label>Purchased</label><span id="p-tot" style="color:var(--red);">€0.00</span></div>
        <div class="tot-item"><label>Paid</label><span id="p-paid" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/P</label><span id="p-ap" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>Count</label><span id="p-cnt" style="color:var(--text2);">0</span></div>
      </div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Supplier</th><th>Description</th><th>Category</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="purchTbl"><tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ COLLECTIONS ══ -->
    <div class="page" id="page-collections">
      <div class="sec-hdr">
        <div><div class="sec-title">Collections</div><div class="sec-sub">Reconcile payments from customers</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('collections')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('collections','Collections')" title="Export PDF">📄</button>
          <button class="btn btn-ghost btn-sm" onclick="openOverlay('ov-coll')">+ Manual Collection</button>
        </div>
      </div>
      <div class="totbar">
        <div class="tot-item"><label>Total Invoiced</label><span id="c-invoiced" style="color:var(--text2);">€0.00</span></div>
        <div class="tot-item"><label>Total Collected</label><span id="c-tot" style="color:var(--green);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/R</label><span id="c-pending" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>This Month</label><span id="c-mth" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Collected</label><span id="c-cnt" style="color:var(--text2);">0</span></div>
      </div>

      <!-- PENDING SALES TO COLLECT -->
      <div style="margin-bottom:16px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Collection — From Sales Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Customer</th><th>Description</th><th>Total</th><th>Collected</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingCollTbl"><tr><td colspan="9" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- COLLECTION HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Collection History</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Date</th><th>Customer</th><th>Invoice Ref</th><th>Method</th><th>Amount</th><th>Notes</th><th></th></tr></thead>
          <tbody id="collTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No collections yet.</td></tr></tbody>
        </table></div></div>
      </div>
    </div>

    <!-- ══ PAYMENTS ══ -->
    <div class="page" id="page-payments">
      <div class="sec-hdr">
        <div><div class="sec-title">Payments</div><div class="sec-sub">Reconcile payments to suppliers</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('payments')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('payments','Payments')" title="Export PDF">📄</button>
          <button class="btn btn-ghost btn-sm" onclick="openOverlay('ov-pay')">+ Manual Payment</button>
        </div>
      </div>
      <div class="totbar">
        <div class="tot-item"><label>Total Purchased</label><span id="py-purchased" style="color:var(--text2);">€0.00</span></div>
        <div class="tot-item"><label>Total Paid</label><span id="py-tot" style="color:var(--red);">€0.00</span></div>
        <div class="tot-item"><label>Pending A/P</label><span id="py-pending" style="color:var(--yellow);">€0.00</span></div>
        <div class="tot-item"><label>This Month</label><span id="py-mth" style="color:var(--blue);">€0.00</span></div>
        <div class="tot-item"><label>Paid</label><span id="py-cnt" style="color:var(--text2);">0</span></div>
      </div>

      <!-- PENDING PURCHASES TO PAY -->
      <div style="margin-bottom:16px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Payment — From Purchase Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Supplier</th><th>Description</th><th>Category</th><th>Total</th><th>Paid</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingPayTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- PAYMENT HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Payment History</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Date</th><th>Supplier</th><th>Invoice Ref</th><th>Method</th><th>Amount</th><th>Notes</th><th></th></tr></thead>
          <tbody id="payTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No payments yet.</td></tr></tbody>
        </table></div></div>
      </div>
    </div>

    <!-- ══ JOURNAL ══ -->
    <div class="page" id="page-journal">
      <div class="sec-hdr"><div><div class="sec-title">Journal Entries</div><div class="sec-sub">Double-entry bookkeeping</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('journal')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('journal','Journal Entries')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openOverlay('ov-je')">+ New Entry</button></div></div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>Entry #</th><th>Date</th><th>Type</th><th>Description</th><th>Debit Account</th><th>Credit Account</th><th>Amount</th><th></th></tr></thead><tbody id="jeTbl"><tr><td colspan="7" style="text-align:center;color:var(--text3);padding:24px;">No journal entries yet.</td></tr></tbody></table></div></div>
    </div>

    <!-- ══ P&L ══ -->
    <div class="page" id="page-pl">
      <div class="sec-hdr">
        <div><div class="sec-title">Profit &amp; Loss Statement</div><div class="sec-sub">Income statement for the period</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('pl')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('pl','P&amp;L Statement')" title="Export PDF">📄</button>
          <div class="tabs" style="margin-bottom:0;"><div class="tab active" id="pl-det" onclick="plTab('detail')">Detailed</div><div class="tab" id="pl-sum" onclick="plTab('summary')">Summary</div></div>
        </div>
      </div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from" onchange="setDateFilter(this.value, document.getElementById('df-to').value)">
        <label>To</label>
        <input type="date" id="df-to" onchange="setDateFilter(document.getElementById('df-from').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from').value='';document.getElementById('df-to').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="card"><div class="tbl-wrap"><table class="rtbl"><colgroup><col style="width:60%"><col style="width:40%"></colgroup><tbody id="plBody"></tbody></table></div></div>
    </div>

    <!-- ══ BALANCE SHEET ══ -->
    <div class="page" id="page-bs">
      <div class="sec-hdr"><div><div class="sec-title">Balance Sheet</div><div class="sec-sub">Assets, Liabilities &amp; Equity</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('bs')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('bs','Balance Sheet')" title="Export PDF">📄</button></div></div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from2" onchange="setDateFilter(this.value, document.getElementById('df-to2').value)">
        <label>To</label>
        <input type="date" id="df-to2" onchange="setDateFilter(document.getElementById('df-from2').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from2').value='';document.getElementById('df-to2').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge2" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="row">
        <div class="col"><div class="card"><div class="card-title" style="margin-bottom:16px;">Assets</div><table class="rtbl"><tbody id="bsA"></tbody></table></div></div>
        <div class="col"><div class="card"><div class="card-title" style="margin-bottom:16px;">Liabilities &amp; Equity</div><table class="rtbl"><tbody id="bsLE"></tbody></table></div></div>
      </div>
      <div style="margin-top:14px;padding:14px 20px;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);display:flex;justify-content:space-between;align-items:center;">
        <span style="font-family:'DM Serif Display',serif;font-size:16px;">Balance Check</span>
        <span id="bsChk" style="font-family:'DM Mono',monospace;font-size:13px;"></span>
      </div>
    </div>

    <!-- ══ CASH FLOW ══ -->
    <div class="page" id="page-cf">
      <div class="sec-hdr"><div><div class="sec-title">Cash Flow Statement</div><div class="sec-sub">Cash movements by activity</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('cashflow')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('cf','Cash Flow')" title="Export PDF">📄</button></div></div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from3" onchange="setDateFilter(this.value, document.getElementById('df-to3').value)">
        <label>To</label>
        <input type="date" id="df-to3" onchange="setDateFilter(document.getElementById('df-from3').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from3').value='';document.getElementById('df-to3').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge3" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="card"><table class="rtbl"><tbody id="cfBody"></tbody></table></div>
    </div>

  </div><!-- /content -->
</div><!-- /main -->


<!-- ═══════════════════════ OPERATION MODALS ═══════════════════════ -->

<!-- SALE -->
<div class="overlay" id="ov-sale">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">New Sales Invoice</div><div class="mclose" onclick="closeOverlay('ov-sale')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="s-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="s-num" placeholder="INV-001"></div>
        <div class="fg full"><label>Customer</label>
          <div class="autocomplete-wrap">
            <div style="display:flex;gap:6px;">
              <input type="text" id="s-cust" placeholder="Type to search contacts..." autocomplete="off" oninput="acSearch('s-cust','s-cust-list','client')" onfocus="acSearch('s-cust','s-cust-list','client')" onblur="setTimeout(function(){closeAC('s-cust-list')},200)" style="flex:1;">
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('client')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="s-cust-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="s-desc" placeholder="e.g. Consulting services Q1"></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="s-net" placeholder="0.00" step="0.01" oninput="calcS()"></div>
        <div class="fg"><label>VAT Rate</label><select id="s-vat" onchange="calcS()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="s-va" readonly style="background:var(--surface3);"></div>
        <div class="fg"><label>Total (€)</label><input type="text" id="s-tot2" readonly style="background:var(--surface3);color:var(--accent);font-family:'DM Mono',monospace;font-weight:600;"></div>
        <div class="fg"><label>Status</label><select id="s-stat"><option value="pending">Pending</option><option value="paid">Paid</option><option value="partial">Partial</option></select></div>
        <div class="fg"><label>Payment Method</label><select id="s-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-sale')">Cancel</button><button class="btn btn-primary" onclick="saveSale()">Save Invoice</button></div>
  </div>
</div>

<!-- PURCHASE -->
<div class="overlay" id="ov-purch">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">New Purchase Invoice</div><div class="mclose" onclick="closeOverlay('ov-purch')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="p-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="p-num" placeholder="PINV-001"></div>
        <div class="fg full"><label>Supplier</label>
          <div class="autocomplete-wrap">
            <div style="display:flex;gap:6px;">
              <input type="text" id="p-sup" placeholder="Type to search contacts..." autocomplete="off" oninput="acSearch('p-sup','p-sup-list','supplier')" onfocus="acSearch('p-sup','p-sup-list','supplier')" onblur="setTimeout(function(){closeAC('p-sup-list')},200)" style="flex:1;">
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('supplier')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="p-sup-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="p-desc" placeholder="e.g. Office rent March"></div>
        <div class="fg"><label>Category</label><select id="p-cat"><option value="COGS">Cost of Goods Sold</option><option value="Rent">Rent</option><option value="Salaries">Salaries</option><option value="Utilities">Utilities</option><option value="Marketing">Marketing</option><option value="Professional">Professional Services</option><option value="Depreciation">Depreciation</option><option value="Other OpEx">Other OpEx</option></select></div>
        <div class="fg"><label>VAT Rate</label><select id="p-vat" onchange="calcP()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="p-net" placeholder="0.00" step="0.01" oninput="calcP()"></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="p-va" readonly style="background:var(--surface3);"></div>
        <div class="fg full"><label>Total (€)</label><input type="text" id="p-tot2" readonly style="background:var(--surface3);color:var(--red);font-family:'DM Mono',monospace;font-weight:600;"></div>
        <div class="fg"><label>Status</label><select id="p-stat"><option value="pending">Pending</option><option value="paid">Paid</option></select></div>
        <div class="fg"><label>Payment Method</label><select id="p-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-purch')">Cancel</button><button class="btn btn-primary" onclick="savePurch()">Save Purchase</button></div>
  </div>
</div>

<!-- COLLECTION -->
<div class="overlay" id="ov-coll">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Collection</div><div class="mclose" onclick="closeOverlay('ov-coll')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="c-date"></div>
        <div class="fg"><label>Customer</label><input type="text" id="c-cust" placeholder="Customer name"></div>
        <div class="fg"><label>Invoice Ref</label><input type="text" id="c-ref" placeholder="INV-001"></div>
        <div class="fg"><label>Method</label><select id="c-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
        <div class="fg full"><label>Amount Received (€)</label><input type="number" id="c-amt" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><textarea id="c-notes" placeholder="Optional..."></textarea></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-coll')">Cancel</button><button class="btn btn-primary" onclick="saveColl()">Save</button></div>
  </div>
</div>

<!-- PAYMENT -->
<div class="overlay" id="ov-pay">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Payment</div><div class="mclose" onclick="closeOverlay('ov-pay')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="py-date"></div>
        <div class="fg"><label>Supplier</label><input type="text" id="py-sup" placeholder="Supplier name"></div>
        <div class="fg"><label>Invoice Ref</label><input type="text" id="py-ref" placeholder="PINV-001"></div>
        <div class="fg"><label>Method</label><select id="py-meth"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select></div>
        <div class="fg full"><label>Amount Paid (€)</label><input type="number" id="py-amt" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><textarea id="py-notes" placeholder="Optional..."></textarea></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-pay')">Cancel</button><button class="btn btn-primary" onclick="savePay()">Save</button></div>
  </div>
</div>

<!-- JOURNAL ENTRY -->
<div class="overlay" id="ov-je">
  <div class="modal wide">
    <div class="mhdr"><div class="mtitle">New Journal Entry</div><div class="mclose" onclick="closeOverlay('ov-je')">✕</div></div>
    <div class="mbody">
      <div class="fgrid" style="margin-bottom:20px;">
        <div class="fg"><label>Date</label><input type="date" id="j-date"></div>
        <div class="fg full"><label>Description</label><input type="text" id="j-desc" placeholder="e.g. Depreciation charge Q1"></div>
      </div>
      <div style="display:grid;grid-template-columns:2fr 1fr 1fr auto;gap:10px;margin-bottom:6px;">
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Account</span>
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Debit (€)</span>
        <span style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Credit (€)</span>
        <span></span>
      </div>
      <div id="jeLines"></div>
      <button class="btn btn-ghost btn-sm" style="margin-top:8px;" onclick="addJELine()">+ Add Line</button>
      <div style="display:flex;gap:20px;padding:12px 14px;background:var(--surface2);border-radius:7px;margin-top:12px;">
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">DEBIT</span><span id="je-td" style="font-family:'DM Mono',monospace;color:var(--green);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">CREDIT</span><span id="je-tc" style="font-family:'DM Mono',monospace;color:var(--red);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:'DM Mono',monospace;margin-bottom:2px;">STATUS</span><span id="je-st" style="font-family:'DM Mono',monospace;">—</span></div>
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-je')">Cancel</button><button class="btn btn-primary" onclick="saveJE()">Post Entry</button></div>
  </div>
</div>


<!-- ═══════════════════════ SETTINGS MODAL ═══════════════════════════ -->
<div class="overlay" id="ov-settings">
  <div class="modal xwide">
    <div class="mhdr">
      <div class="mtitle">Settings &amp; Parametrization</div>
      <div class="mclose" onclick="closeOverlay('ov-settings')">✕</div>
    </div>
    <div class="mbody">
      <!-- SETTINGS TABS -->
      <div class="set-tabs">
        <div class="set-tab active" id="stab-user" onclick="setTab('user')">👤 User Profile</div>
        <div class="set-tab" id="stab-company" onclick="setTab('company')">🏢 Company</div>
        <div class="set-tab" id="stab-prefs" onclick="setTab('prefs')">🎨 Preferences</div>
        <div class="set-tab" id="stab-data" onclick="setTab('data')">🗃 Data</div>
      </div>

      <!-- ── USER PROFILE PANEL ── -->
      <div class="set-panel active" id="spanel-user">
        <div class="set-section-label">Profile Photo &amp; Name</div>
        <div class="avatar-row">
          <div class="avatar-big" id="previewAvatar" style="background:#c8ff00;">PK</div>
          <div>
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;">Avatar Color</div>
            <div class="color-swatches" id="colorSwatches"></div>
          </div>
        </div>
        <div class="fgrid" style="margin-top:18px;">
          <div class="fg"><label>First Name</label><input type="text" id="u-fname" placeholder="Previt" oninput="livePreviewUser()"></div>
          <div class="fg"><label>Last Name</label><input type="text" id="u-lname" placeholder="Ketsia" oninput="livePreviewUser()"></div>
          <div class="fg full"><label>Job Title / Role</label><input type="text" id="u-role" placeholder="e.g. Chief Accountant, CFO, Finance Manager"></div>
          <div class="fg full"><label>Email Address</label><input type="email" id="u-email" placeholder="previt.ketsia@company.com"></div>
          <div class="fg full"><label>Phone (optional)</label><input type="text" id="u-phone" placeholder="+1 234 567 890"></div>
        </div>
      </div>

      <!-- ── COMPANY PANEL ── -->
      <div class="set-panel" id="spanel-company">
        <div class="set-section-label">Company Information</div>
        <div class="fgrid">
          <div class="fg full"><label>Company Name</label><input type="text" id="set-co" placeholder="My Company Ltd."></div>
          <div class="fg"><label>Tax ID / VAT Number</label><input type="text" id="set-taxid" placeholder="ES-B12345678"></div>
          <div class="fg"><label>Industry</label><select id="set-industry"><option value="">— Select —</option><option>Consulting</option><option>Retail</option><option>Manufacturing</option><option>Technology</option><option>Healthcare</option><option>Real Estate</option><option>Finance</option><option>Other</option></select></div>
          <div class="fg full"><label>Address</label><input type="text" id="set-addr" placeholder="123 Main Street, City, Country"></div>
          <div class="fg"><label>Fiscal Year Start</label><select id="set-fystart"><option value="Jan">January</option><option value="Apr">April</option><option value="Jul">July</option><option value="Oct">October</option></select></div>
          <div class="fg"><label>Fiscal Year</label><input type="text" id="set-fy" placeholder="2025"></div>
          <div class="fg"><label>Currency Symbol</label><input type="text" id="set-cur" placeholder="€" maxlength="3"></div>
          <div class="fg"><label>Default VAT Rate (%)</label><select id="set-defvat"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        </div>
      </div>

      <!-- ── PREFERENCES PANEL ── -->
      <div class="set-panel" id="spanel-prefs">
        <div class="set-section-label">Display &amp; Interface</div>
        <div class="fgrid">
          <div class="fg"><label>Date Format</label><select id="set-datefmt"><option value="DD/MM/YYYY">DD/MM/YYYY</option><option value="MM/DD/YYYY">MM/DD/YYYY</option><option value="YYYY-MM-DD">YYYY-MM-DD</option></select></div>
          <div class="fg"><label>Number Format</label><select id="set-numfmt"><option value="eu">1.234,56 (European)</option><option value="us">1,234.56 (US/UK)</option></select></div>
          <div class="fg"><label>Language</label><select id="set-lang"><option value="en">English</option><option value="fr">Français</option><option value="es">Español</option><option value="de">Deutsch</option><option value="it">Italiano</option></select></div>
          <div class="fg"><label>Theme Mode</label>
            <select id="set-theme">
              <option value="dark">🌙 Dark Mode (default)</option>
              <option value="light">☀️ Light Mode</option>
            </select>
          </div>
        </div>
        <div class="divider"></div>
        <div class="set-section-label">Invoice Defaults</div>
        <div class="fgrid">
          <div class="fg full"><label>Default Invoice Notes / Footer</label><textarea id="set-invnotes" placeholder="e.g. Payment due within 30 days. Thank you for your business."></textarea></div>
          <div class="fg"><label>Invoice Prefix</label><input type="text" id="set-invpfx" placeholder="INV-" maxlength="10"></div>
          <div class="fg"><label>Purchase Prefix</label><input type="text" id="set-purpfx" placeholder="PINV-" maxlength="10"></div>
        </div>
      </div>

      <!-- ── DATA PANEL ── -->
      <div class="set-panel" id="spanel-data">
        <div class="set-section-label">Session Summary</div>
        <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:20px;">
          <div class="info-row"><span class="info-label">Sales Invoices</span><span class="info-val" id="di-sales">0</span></div>
          <div class="info-row"><span class="info-label">Purchase Invoices</span><span class="info-val" id="di-purch">0</span></div>
          <div class="info-row"><span class="info-label">Collections</span><span class="info-val" id="di-coll">0</span></div>
          <div class="info-row"><span class="info-label">Payments</span><span class="info-val" id="di-pay">0</span></div>
          <div class="info-row"><span class="info-label">Journal Entries</span><span class="info-val" id="di-je">0</span></div>
          <div class="info-row"><span class="info-label">Storage Used</span><span class="info-val" id="di-size">—</span></div>
        </div>
        <div class="set-section-label">Danger Zone</div>
        <div style="background:rgba(248,113,113,.06);border:1px solid rgba(248,113,113,.2);border-radius:8px;padding:16px;display:flex;justify-content:space-between;align-items:center;">
          <div>
            <div style="font-weight:600;font-size:13px;color:var(--red);margin-bottom:4px;">Clear All Transaction Data</div>
            <div style="font-size:12px;color:var(--text3);">Permanently deletes all invoices, payments, and journal entries. Settings are preserved.</div>
          </div>
          <button class="btn btn-danger btn-sm" onclick="clearAll()" style="flex-shrink:0;margin-left:16px;">Clear Data</button>
        </div>
      </div>

    </div><!-- /mbody -->
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-settings')">Cancel</button>
      <button class="btn btn-primary" onclick="saveSettings()">Save Settings</button>
    </div>
  </div>
</div>


<!-- ═══════════════════════════════ JAVASCRIPT ═══════════════════════ -->
<script>
// ── STATE ──────────────────────────────────────────────────────────────────
var DB={
  user:{fname:'Previt',lname:'Ketsia',role:'Chief Accountant',email:'',phone:'',avatarColor:'#c8ff00'},
  co:{name:'My Company Ltd.',taxid:'',industry:'',addr:'',fy:'2025',fystart:'Jan',cur:'€',defvat:'21'},
  prefs:{datefmt:'DD/MM/YYYY',numfmt:'us',lang:'en',accent:'#c8ff00',invnotes:'',invpfx:'INV-',purpfx:'PINV-'},
  sales:[],purch:[],coll:[],pay:[],je:[],
  contacts:[],
  ids:{s:1,p:1,c:1,py:1,j:1,ct:1}
};
var plMode='detail';
var AVATAR_COLORS=['#c8ff00','#00d4ff','#a78bfa','#fb923c','#f472b6','#34d399','#ffd93d','#f87171','#60a5fa'];
var COA=[
  {c:'1000',n:'Cash & Bank',t:'asset'},{c:'1100',n:'Accounts Receivable',t:'asset'},
  {c:'1200',n:'Inventory',t:'asset'},{c:'1300',n:'Prepaid Expenses',t:'asset'},
  {c:'1500',n:'Fixed Assets',t:'asset'},{c:'1510',n:'Accum. Depreciation',t:'asset'},
  {c:'2000',n:'Accounts Payable',t:'liability'},{c:'2100',n:'VAT Payable',t:'liability'},
  {c:'2200',n:'Accrued Liabilities',t:'liability'},{c:'2500',n:'Long-term Debt',t:'liability'},
  {c:'3000',n:'Share Capital',t:'equity'},{c:'3100',n:'Retained Earnings',t:'equity'},
  {c:'4000',n:'Sales Revenue',t:'revenue'},{c:'4100',n:'Other Revenue',t:'revenue'},
  {c:'5000',n:'Cost of Goods Sold',t:'expense'},{c:'6000',n:'Salaries & Wages',t:'expense'},
  {c:'6100',n:'Rent',t:'expense'},{c:'6200',n:'Utilities',t:'expense'},
  {c:'6300',n:'Marketing',t:'expense'},{c:'6400',n:'Professional Services',t:'expense'},
  {c:'6500',n:'Depreciation',t:'expense'},{c:'6900',n:'Other OpEx',t:'expense'},
  {c:'7000',n:'Interest Expense',t:'expense'},{c:'7100',n:'Tax Expense',t:'expense'}
];

// ── PERSISTENCE  (saves to disk via Python server) ──────────────────────────
function sv(){
  try{
    fetch('/save',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(DB)});
  }catch(e){}
  // fallback: also keep in localStorage
  try{localStorage.setItem('fl_v4',JSON.stringify(DB));}catch(e){}
}
function ld(){
  var xhr=new XMLHttpRequest();
  xhr.open('GET','/load',false);
  xhr.send();
  if(xhr.status===200){
    try{
      var parsed=JSON.parse(xhr.responseText);
      if(parsed && parsed.ids) DB=parsed;
    }catch(e){}
  } else {
    try{var r=localStorage.getItem('fl_v4');if(r){var p=JSON.parse(r);if(p&&p.ids)DB=p;}}catch(e){}
  }
  // Ensure new fields exist for backward compatibility
  if(!DB.contacts)  DB.contacts = [];
  if(!DB.ids.ct)    DB.ids.ct   = 1;
}

// ── FORMAT ─────────────────────────────────────────────────────────────────
function f(n){return(DB.co.cur||'€')+Number(n||0).toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2});}
function td(){return new Date().toISOString().split('T')[0];}
function ym(){var n=new Date();return n.getFullYear()+'-'+String(n.getMonth()+1).padStart(2,'0');}
function initials(fn,ln){return((fn||'?')[0]+(ln||'?')[0]).toUpperCase();}
function fullName(){return((DB.user.fname||'')+' '+(DB.user.lname||'')).trim()||'User';}

// ── INIT ───────────────────────────────────────────────────────────────────
function init(){
  ld();
  buildColorSwatches();
  applyAccent();
  applyTranslations();
  updateUserUI();
  setDates();
  initJE();
  renderAll();
}
function setDates(){var t=td();['s-date','p-date','c-date','py-date','j-date'].forEach(function(id){var e=document.getElementById(id);if(e)e.value=t;});}

// ── ACCENT COLOR ───────────────────────────────────────────────────────────
function applyAccent(){
  // Apply theme (dark/light)
  var theme = DB.prefs.theme || 'dark';
  document.body.classList.toggle('light-mode', theme === 'light');
  var track = document.getElementById('themeTrack');
  var label = document.getElementById('themeLabel');
  if(track) track.classList.toggle('on', theme === 'light');
  if(label) label.textContent = theme === 'light' ? 'Light' : 'Dark';
  // Accent color
  var acc = theme === 'light' ? '#0057ff' : (DB.prefs.accent||'#c8ff00');
  document.documentElement.style.setProperty('--accent', acc);
  var r=parseInt(acc.slice(1,3),16),g=parseInt(acc.slice(3,5),16),b=parseInt(acc.slice(5,7),16);
  var lum=(0.299*r+0.587*g+0.114*b)/255;
  var fgColor=lum>0.5?'#0f0f11':'#f0f0f4';
  document.querySelectorAll('.user-avatar,.avatar-big').forEach(function(el){el.style.color=fgColor;});
}

function toggleTheme(){
  DB.prefs.theme = (DB.prefs.theme === 'light') ? 'dark' : 'light';
  sv(); applyAccent();
}

// ── USER UI ────────────────────────────────────────────────────────────────
function updateUserUI(){
  var fn=fullName(),ini=initials(DB.user.fname,DB.user.lname);
  var ac=DB.user.avatarColor||DB.prefs.accent||'#c8ff00';
  // Sidebar
  document.getElementById('sideAvatarInitials').textContent=ini;
  document.getElementById('sideAvatarBg').style.background=ac;
  document.getElementById('sideUserName').textContent=fn;
  document.getElementById('sideUserRole').textContent=DB.user.role||'Accountant';
  document.getElementById('sideUserCo').textContent=DB.co.name||'My Company';
  // Topbar
  document.getElementById('topGreeting').textContent=DB.user.fname||fn;
  // Title
  document.title='FinLedger — '+fn;
}

// ── COLOUR SWATCHES ────────────────────────────────────────────────────────
function buildColorSwatches(){
  var wrap=document.getElementById('colorSwatches');
  wrap.innerHTML='';
  AVATAR_COLORS.forEach(function(col){
    var d=document.createElement('div');
    d.className='swatch'+(col===(DB.user.avatarColor||'#c8ff00')?' sel':'');
    d.style.background=col;
    d.title=col;
    d.onclick=function(){
      document.querySelectorAll('.swatch').forEach(function(s){s.classList.remove('sel');});
      d.classList.add('sel');
      DB.user.avatarColor=col;
      var pv=document.getElementById('previewAvatar');
      pv.style.background=col;
      var r2=parseInt(col.slice(1,3),16),g2=parseInt(col.slice(3,5),16),b2=parseInt(col.slice(5,7),16);
      var l=(0.299*r2+0.587*g2+0.114*b2)/255;
      pv.style.color=l>0.5?'#0f0f11':'#f0f0f4';
      livePreviewUser();
    };
    wrap.appendChild(d);
  });
}

function livePreviewUser(){
  var fn=document.getElementById('u-fname').value||'?';
  var ln=document.getElementById('u-lname').value||'?';
  document.getElementById('previewAvatar').textContent=initials(fn,ln);
}

// ── NAVIGATION ─────────────────────────────────────────────────────────────
var titles={dashboard:'Dashboard',contacts:'Contacts',sales:'Sales Invoices',purchases:'Purchase Invoices',collections:'Collections',payments:'Payments',journal:'Journal Entries',pl:'P&L Statement',bs:'Balance Sheet',cf:'Cash Flow Statement'};
var crumbs={dashboard:'FinLedger / Overview',contacts:'FinLedger / Operations / Contacts',sales:'FinLedger / Operations / Sales',purchases:'FinLedger / Operations / Purchases',collections:'FinLedger / Operations / Collections',payments:'FinLedger / Operations / Payments',journal:'FinLedger / Operations / Journal',pl:'FinLedger / Reports / P&L',bs:'FinLedger / Reports / Balance Sheet',cf:'FinLedger / Reports / Cash Flow'};
function nav(p){
  document.querySelectorAll('.page').forEach(function(e){e.classList.remove('active');});
  document.querySelectorAll('.nav-item').forEach(function(e){e.classList.remove('active');});
  document.getElementById('page-'+p).classList.add('active');
  var ni=document.querySelector('[onclick="nav(\''+p+'\')"]');if(ni)ni.classList.add('active');
  document.getElementById('pgTitle').textContent=titles[p]||p;
  document.getElementById('pgCrumb').textContent=crumbs[p]||'';
  renderAll();
}

// ── OVERLAYS ───────────────────────────────────────────────────────────────
function openOverlay(id){document.getElementById(id).classList.add('open');setDates();}
function closeOverlay(id){document.getElementById(id).classList.remove('open');}
document.querySelectorAll('.overlay').forEach(function(ov){
  ov.addEventListener('click',function(e){if(e.target===ov)ov.classList.remove('open');});
});

// ── SETTINGS TABS ──────────────────────────────────────────────────────────
function openSettings(tab){
  // Populate fields before opening
  document.getElementById('u-fname').value=DB.user.fname||'';
  document.getElementById('u-lname').value=DB.user.lname||'';
  document.getElementById('u-role').value=DB.user.role||'';
  document.getElementById('u-email').value=DB.user.email||'';
  document.getElementById('u-phone').value=DB.user.phone||'';
  var pv=document.getElementById('previewAvatar');
  var ac=DB.user.avatarColor||'#c8ff00';
  pv.style.background=ac;pv.textContent=initials(DB.user.fname,DB.user.lname);
  var r2=parseInt(ac.slice(1,3),16),g2=parseInt(ac.slice(3,5),16),b2=parseInt(ac.slice(5,7),16);
  pv.style.color=((0.299*r2+0.587*g2+0.114*b2)/255)>0.5?'#0f0f11':'#f0f0f4';
  buildColorSwatches();
  // Company
  document.getElementById('set-co').value=DB.co.name||'';
  document.getElementById('set-taxid').value=DB.co.taxid||'';
  document.getElementById('set-industry').value=DB.co.industry||'';
  document.getElementById('set-addr').value=DB.co.addr||'';
  document.getElementById('set-fy').value=DB.co.fy||'2025';
  document.getElementById('set-fystart').value=DB.co.fystart||'Jan';
  document.getElementById('set-cur').value=DB.co.cur||'€';
  document.getElementById('set-defvat').value=DB.co.defvat||'21';
  // Prefs
  document.getElementById('set-datefmt').value=DB.prefs.datefmt||'DD/MM/YYYY';
  document.getElementById('set-numfmt').value=DB.prefs.numfmt||'us';
  document.getElementById('set-lang').value=DB.prefs.lang||'en';
  document.getElementById('set-theme').value=DB.prefs.theme||'dark';
  document.getElementById('set-invnotes').value=DB.prefs.invnotes||'';
  document.getElementById('set-invpfx').value=DB.prefs.invpfx||'INV-';
  document.getElementById('set-purpfx').value=DB.prefs.purpfx||'PINV-';
  // Data stats
  document.getElementById('di-sales').textContent=DB.sales.length;
  document.getElementById('di-purch').textContent=DB.purch.length;
  document.getElementById('di-coll').textContent=DB.coll.length;
  document.getElementById('di-pay').textContent=DB.pay.length;
  document.getElementById('di-je').textContent=DB.je.length;
  var raw=localStorage.getItem('fl_v4')||'';
  document.getElementById('di-size').textContent=(raw.length/1024).toFixed(1)+' KB';
  setTab(tab||'user');
  openOverlay('ov-settings');
}

function setTab(t){
  ['user','company','prefs','data'].forEach(function(n){
    document.getElementById('stab-'+n).classList.toggle('active',n===t);
    document.getElementById('spanel-'+n).classList.toggle('active',n===t);
  });
}

function saveSettings(){
  // User
  DB.user.fname=document.getElementById('u-fname').value||'User';
  DB.user.lname=document.getElementById('u-lname').value||'';
  DB.user.role=document.getElementById('u-role').value||'Accountant';
  DB.user.email=document.getElementById('u-email').value||'';
  DB.user.phone=document.getElementById('u-phone').value||'';
  // Company
  DB.co.name=document.getElementById('set-co').value||'My Company Ltd.';
  DB.co.taxid=document.getElementById('set-taxid').value||'';
  DB.co.industry=document.getElementById('set-industry').value||'';
  DB.co.addr=document.getElementById('set-addr').value||'';
  DB.co.fy=document.getElementById('set-fy').value||'2025';
  DB.co.fystart=document.getElementById('set-fystart').value||'Jan';
  DB.co.cur=document.getElementById('set-cur').value||'€';
  DB.co.defvat=document.getElementById('set-defvat').value||'21';
  // Prefs
  DB.prefs.datefmt=document.getElementById('set-datefmt').value;
  DB.prefs.numfmt=document.getElementById('set-numfmt').value;
  DB.prefs.lang=document.getElementById('set-lang').value;
  DB.prefs.theme=document.getElementById('set-theme').value;
  DB.prefs.invnotes=document.getElementById('set-invnotes').value;
  DB.prefs.invpfx=document.getElementById('set-invpfx').value||'INV-';
  DB.prefs.purpfx=document.getElementById('set-purpfx').value||'PINV-';
  sv();applyAccent();applyTranslations();updateUserUI();closeOverlay('ov-settings');renderAll();
}

function clearAll(){
  if(!confirm('Delete ALL transaction data?\n\nThis action is permanent and cannot be undone.\nYour settings and user profile will be preserved.'))return;
  DB.sales=[];DB.purch=[];DB.coll=[];DB.pay=[];DB.je=[];DB.ids={s:1,p:1,c:1,py:1,j:1};
  sv();closeOverlay('ov-settings');renderAll();
}

// ── CALC HELPERS ───────────────────────────────────────────────────────────
function calcS(){var n=parseFloat(document.getElementById('s-net').value)||0,v=parseFloat(document.getElementById('s-vat').value)||0,va=n*v/100;document.getElementById('s-va').value=va.toFixed(2);document.getElementById('s-tot2').value=(n+va).toFixed(2);}
function calcP(){var n=parseFloat(document.getElementById('p-net').value)||0,v=parseFloat(document.getElementById('p-vat').value)||0,va=n*v/100;document.getElementById('p-va').value=va.toFixed(2);document.getElementById('p-tot2').value=(n+va).toFixed(2);}

// ── SAVE OPERATIONS ────────────────────────────────────────────────────────
function saveSale(){
  var net=parseFloat(document.getElementById('s-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('s-vat').value)||0,va=net*vat/100,stat=document.getElementById('s-stat').value,meth=document.getElementById('s-meth').value,dt=document.getElementById('s-date').value;
  var pfx=DB.prefs.invpfx||'INV-';
  var num=document.getElementById('s-num').value||(pfx+String(DB.ids.s).padStart(3,'0'));
  var cust=document.getElementById('s-cust').value||'Unknown',desc=document.getElementById('s-desc').value;
  var rec={id:DB.ids.s++,date:dt,num:num,customer:cust,desc:desc,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth};
  DB.sales.push(rec);
  // Auto JE: Dr Accounts Receivable / Cr Sales Revenue (+ VAT Payable if applicable)
  var saleLines = [
    {account:'1100', debit:rec.total, credit:0},   // Dr Accounts Receivable (total incl VAT)
    {account:'4000', debit:0, credit:net}            // Cr Sales Revenue (net)
  ];
  if(va > 0) saleLines.push({account:'2100', debit:0, credit:va}); // Cr VAT Payable
  DB.je.push({id:DB.ids.j++,date:dt,desc:'Sale — '+cust+' / '+num,lines:saleLines,amount:rec.total,auto:true,sourceType:'sale',sourceId:rec.id});
  // If paid immediately, also create collection + cash JE
  if(stat==='paid'){
    DB.coll.push({id:DB.ids.c++,date:dt,customer:cust,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Collection — '+cust+' / '+num,lines:[{account:'1000',debit:rec.total,credit:0},{account:'1100',debit:0,credit:rec.total}],amount:rec.total,auto:true,sourceType:'collection'});
  }
  sv();closeOverlay('ov-sale');['s-num','s-cust','s-desc','s-net','s-va','s-tot2'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function savePurch(){
  var net=parseFloat(document.getElementById('p-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('p-vat').value)||0,va=net*vat/100,stat=document.getElementById('p-stat').value,meth=document.getElementById('p-meth').value,dt=document.getElementById('p-date').value;
  var pfx=DB.prefs.purpfx||'PINV-';
  var num=document.getElementById('p-num').value||(pfx+String(DB.ids.p).padStart(3,'0'));
  var sup=document.getElementById('p-sup').value||'Unknown',desc=document.getElementById('p-desc').value,cat=document.getElementById('p-cat').value;
  var rec={id:DB.ids.p++,date:dt,num:num,supplier:sup,desc:desc,cat:cat,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth};
  DB.purch.push(rec);
  // Auto JE: Dr Expense / Cr Accounts Payable (+ VAT deductible)
  var catAccMap={'COGS':'5000','Rent':'6100','Salaries':'6000','Utilities':'6200','Marketing':'6300','Professional':'6400','Depreciation':'6500','Other OpEx':'6900'};
  var expAcc = catAccMap[cat] || '6900';
  var purchLines = [
    {account:expAcc, debit:net,  credit:0},         // Dr Expense account (net)
    {account:'2000', debit:0,    credit:rec.total}   // Cr Accounts Payable (total incl VAT)
  ];
  if(va > 0) purchLines.splice(1, 0, {account:'2100', debit:va, credit:0}); // Dr VAT deductible
  DB.je.push({id:DB.ids.j++,date:dt,desc:'Purchase — '+sup+' / '+num,lines:purchLines,amount:rec.total,auto:true,sourceType:'purchase',sourceId:rec.id});
  // If paid immediately
  if(stat==='paid'){
    DB.pay.push({id:DB.ids.py++,date:dt,supplier:sup,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Payment — '+sup+' / '+num,lines:[{account:'2000',debit:rec.total,credit:0},{account:'1000',debit:0,credit:rec.total}],amount:rec.total,auto:true,sourceType:'payment'});
  }
  sv();closeOverlay('ov-purch');['p-num','p-sup','p-desc','p-net','p-va','p-tot2'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function saveColl(){
  var amt=parseFloat(document.getElementById('c-amt').value)||0;if(!amt){alert('Enter amount.');return;}
  DB.coll.push({id:DB.ids.c++,date:document.getElementById('c-date').value,customer:document.getElementById('c-cust').value||'Unknown',ref:document.getElementById('c-ref').value,method:document.getElementById('c-meth').value,amount:amt,notes:document.getElementById('c-notes').value});
  sv();closeOverlay('ov-coll');['c-cust','c-ref','c-amt','c-notes'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function savePay(){
  var amt=parseFloat(document.getElementById('py-amt').value)||0;if(!amt){alert('Enter amount.');return;}
  DB.pay.push({id:DB.ids.py++,date:document.getElementById('py-date').value,supplier:document.getElementById('py-sup').value||'Unknown',ref:document.getElementById('py-ref').value,method:document.getElementById('py-meth').value,amount:amt,notes:document.getElementById('py-notes').value});
  sv();closeOverlay('ov-pay');['py-sup','py-ref','py-amt','py-notes'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}

// ── JOURNAL ────────────────────────────────────────────────────────────────
function coaOpts(){return COA.map(function(a){return '<option value="'+a.c+'">'+a.c+' – '+a.n+'</option>';}).join('');}
function initJE(){document.getElementById('jeLines').innerHTML='';addJELine();addJELine();}
function addJELine(){
  var d=document.createElement('div');d.className='je-line';
  d.innerHTML='<select class="je-ac"><option value="">-- Account --</option>'+coaOpts()+'</select><input type="number" class="je-dr" placeholder="0.00" step="0.01" oninput="calcJEB()"><input type="number" class="je-cr" placeholder="0.00" step="0.01" oninput="calcJEB()"><button class="btn btn-ghost btn-sm" onclick="rmJELine(this)">✕</button>';
  document.getElementById('jeLines').appendChild(d);
}
function rmJELine(b){if(document.querySelectorAll('.je-line').length<=2)return;b.parentElement.remove();calcJEB();}
function calcJEB(){
  var d=0,c=0;
  document.querySelectorAll('.je-dr').forEach(function(i){d+=parseFloat(i.value)||0;});
  document.querySelectorAll('.je-cr').forEach(function(i){c+=parseFloat(i.value)||0;});
  document.getElementById('je-td').textContent=f(d);document.getElementById('je-tc').textContent=f(c);
  var st=document.getElementById('je-st');
  if(Math.abs(d-c)<0.01&&d>0){st.textContent='✓ Balanced';st.style.color='var(--green)';}
  else{st.textContent='Δ '+f(Math.abs(d-c));st.style.color='var(--red)';}
}
function saveJE(){
  var lines=[],td2=0,tc2=0;
  document.querySelectorAll('#jeLines .je-line').forEach(function(row){
    var a=row.querySelector('.je-ac').value,d=parseFloat(row.querySelector('.je-dr').value)||0,c=parseFloat(row.querySelector('.je-cr').value)||0;
    if(a){lines.push({account:a,debit:d,credit:c});td2+=d;tc2+=c;}
  });
  if(lines.length<2){alert('Enter at least 2 lines.');return;}
  if(Math.abs(td2-tc2)>0.01){alert('Not balanced. Debits must equal Credits.');return;}
  DB.je.push({id:DB.ids.j++,date:document.getElementById('j-date').value,desc:document.getElementById('j-desc').value||'Journal Entry',lines:lines,amount:td2});
  sv();closeOverlay('ov-je');document.getElementById('j-desc').value='';initJE();renderAll();
}

// ── DELETE ─────────────────────────────────────────────────────────────────
function delS(id){if(!confirm('Delete this invoice?'))return;DB.sales=DB.sales.filter(function(x){return x.id!==id;});sv();renderAll();}
function delP(id){if(!confirm('Delete this invoice?'))return;DB.purch=DB.purch.filter(function(x){return x.id!==id;});sv();renderAll();}
function delC(id){if(!confirm('Delete?'))return;DB.coll=DB.coll.filter(function(x){return x.id!==id;});sv();renderAll();}
function delPy(id){if(!confirm('Delete?'))return;DB.pay=DB.pay.filter(function(x){return x.id!==id;});sv();renderAll();}
function delJ(id){if(!confirm('Delete entry?'))return;DB.je=DB.je.filter(function(x){return x.id!==id;});sv();renderAll();}

// ── HELPERS ────────────────────────────────────────────────────────────────
function bdg(s){var m={paid:'bg',pending:'by',partial:'bb',received:'bg',posted:'bp'};return '<span class="badge '+(m[s]||'bb')+'">'+s+'</span>';}
function mth(m){return{bank:'🏦 Bank',cash:'💵 Cash',card:'💳 Card',other:'📋 Other'}[m]||m;}

// ── COMPUTE FINANCIALS ─────────────────────────────────────────────────────
// Active date filter state
var _dateFrom = '', _dateTo = '';

// ── TRANSLATIONS ────────────────────────────────────────────────────────────
var T = {
  en:{
    dashboard:'Dashboard',contacts:'Contacts',sales:'Sales',purchases:'Purchases',
    collections:'Collections',payments:'Payments',journal:'Journal Entries',
    pl:'P&L Statement',bs:'Balance Sheet',cf:'Cash Flow',settings:'Settings',
    newInvoice:'+ New Invoice',newPurchase:'+ New Purchase',newCollection:'+ Record Collection',
    newPayment:'+ Record Payment',newEntry:'+ New Entry',newContact:'+ New Contact',
    overview:'Overview',operations:'Operations',reports:'Reports',
    totalRevenue:'Total Revenue',totalExpenses:'Total Expenses',netIncome:'Net Income',
    cashPosition:'Cash Position',accountsReceivable:'Accounts Receivable',
    accountsPayable:'Accounts Payable',salesInvoices:'Sales Invoices',
    purchaseInvoices:'Purchase Invoices',netMargin:'Net Margin',
    recentTransactions:'Recent Transactions',invoiced:'Invoiced',collected:'Collected',
    pendingAR:'Pending A/R',count:'Count',purchased:'Purchased',paid:'Paid',
    pendingAP:'Pending A/P',totalCollected:'Total Collected',thisMonth:'This Month',
    totalPaid:'Total Paid',grossProfit:'Gross Profit',operatingExpenses:'Operating Expenses',
    totalAssets:'Total Assets',totalLiabilities:'Total Liabilities',totalEquity:'Total Equity',
    currentAssets:'Current Assets',nonCurrentAssets:'Non-Current Assets',
    currentLiabilities:'Current Liabilities',nonCurrentLiabilities:'Non-Current Liabilities',
    equity:'Equity',operatingActivities:'Operating Activities',investingActivities:'Investing Activities',
    financingActivities:'Financing Activities',netChangeInCash:'Net Change in Cash',
    closingBalance:'Closing Balance',openingBalance:'Opening Balance',
    welcomeBack:'Welcome back,',date:'Date',customer:'Customer',supplier:'Supplier',
    description:'Description',total:'Total',status:'Status',method:'Method',
    pending:'Pending',paid2:'Paid',partial:'Partial',del:'Del',cancel:'Cancel',save:'Save',
    postEntry:'Post Entry',saveInvoice:'Save Invoice',savePurchase:'Save Purchase',
    balanced:'Balanced',unbalanced:'Unbalanced',collect:'Collect',pay:'Pay',
    exportExcel:'Export Excel',exportPDF:'Export PDF',
    noDataYet:'No data yet.',addTransactions:'Add transactions to see chart'
  },
  es:{
    dashboard:'Panel',contacts:'Contactos',sales:'Ventas',purchases:'Compras',
    collections:'Cobros',payments:'Pagos',journal:'Asientos Contables',
    pl:'Cuenta de PyG',bs:'Balance de Situación',cf:'Flujo de Caja',settings:'Configuración',
    newInvoice:'+ Nueva Factura',newPurchase:'+ Nueva Compra',newCollection:'+ Registrar Cobro',
    newPayment:'+ Registrar Pago',newEntry:'+ Nuevo Asiento',newContact:'+ Nuevo Contacto',
    overview:'Resumen',operations:'Operaciones',reports:'Informes',
    totalRevenue:'Ingresos Totales',totalExpenses:'Gastos Totales',netIncome:'Beneficio Neto',
    cashPosition:'Posición de Caja',accountsReceivable:'Clientes (deudores)',
    accountsPayable:'Proveedores (acreed.)',salesInvoices:'Facturas de Venta',
    purchaseInvoices:'Facturas de Compra',netMargin:'Margen Neto',
    recentTransactions:'Movimientos Recientes',invoiced:'Facturado',collected:'Cobrado',
    pendingAR:'Pendiente Cobro',count:'Nº',purchased:'Comprado',paid:'Pagado',
    pendingAP:'Pendiente Pago',totalCollected:'Total Cobrado',thisMonth:'Este Mes',
    totalPaid:'Total Pagado',grossProfit:'Margen Bruto',operatingExpenses:'Gastos Operativos',
    totalAssets:'Total Activo',totalLiabilities:'Total Pasivo',totalEquity:'Patrimonio Neto',
    currentAssets:'Activo Corriente',nonCurrentAssets:'Activo No Corriente',
    currentLiabilities:'Pasivo Corriente',nonCurrentLiabilities:'Pasivo No Corriente',
    equity:'Patrimonio Neto',operatingActivities:'Actividades de Explotación',
    investingActivities:'Actividades de Inversión',financingActivities:'Actividades de Financiación',
    netChangeInCash:'Variación Neta de Caja',closingBalance:'Saldo Final',openingBalance:'Saldo Inicial',
    welcomeBack:'Bienvenido,',date:'Fecha',customer:'Cliente',supplier:'Proveedor',
    description:'Descripción',total:'Total',status:'Estado',method:'Método',
    pending:'Pendiente',paid2:'Pagado',partial:'Parcial',del:'Elim.',cancel:'Cancelar',save:'Guardar',
    postEntry:'Publicar Asiento',saveInvoice:'Guardar Factura',savePurchase:'Guardar Compra',
    balanced:'Cuadrado',unbalanced:'Descuadrado',collect:'Cobrar',pay:'Pagar',
    exportExcel:'Exportar Excel',exportPDF:'Exportar PDF',
    noDataYet:'Sin datos aún.',addTransactions:'Añade transacciones para ver el gráfico'
  },
  fr:{
    dashboard:'Tableau de bord',contacts:'Contacts',sales:'Ventes',purchases:'Achats',
    collections:'Encaissements',payments:'Paiements',journal:'Journal Comptable',
    pl:'Compte de Résultat',bs:'Bilan',cf:'Flux de Trésorerie',settings:'Paramètres',
    newInvoice:'+ Nouvelle Facture',newPurchase:'+ Nouvel Achat',newCollection:'+ Enregistrer',
    newPayment:'+ Enregistrer',newEntry:'+ Nouvelle Écriture',newContact:'+ Nouveau Contact',
    overview:'Vue ensemble',operations:'Opérations',reports:'Rapports',
    totalRevenue:'Revenus Totaux',totalExpenses:'Dépenses Totales',netIncome:'Résultat Net',
    cashPosition:'Trésorerie',accountsReceivable:'Clients',accountsPayable:'Fournisseurs',
    salesInvoices:'Factures de Vente',purchaseInvoices:'Factures Achat',netMargin:'Marge Nette',
    recentTransactions:'Transactions Récentes',invoiced:'Facturé',collected:'Encaissé',
    pendingAR:'En attente',count:'Nbre',purchased:'Acheté',paid:'Payé',pendingAP:'À payer',
    totalCollected:'Total Encaissé',thisMonth:'Ce Mois',totalPaid:'Total Payé',
    grossProfit:'Marge Brute',operatingExpenses:'Charges exploitation',
    totalAssets:'Total Actif',totalLiabilities:'Total Passif',totalEquity:'Capitaux Propres',
    currentAssets:'Actif Courant',nonCurrentAssets:'Actif Non Courant',
    currentLiabilities:'Passif Courant',nonCurrentLiabilities:'Passif Non Courant',
    equity:'Capitaux Propres',operatingActivities:'Activités Opérationnelles',
    investingActivities:'Activites Investissement',financingActivities:'Activites Financement',
    netChangeInCash:'Variation Nette de Trésorerie',closingBalance:'Solde Final',
    openingBalance:'Solde Initial',welcomeBack:'Bienvenue,',date:'Date',customer:'Client',
    supplier:'Fournisseur',description:'Description',total:'Total',status:'Statut',method:'Méthode',
    pending:'En attente',paid2:'Payé',partial:'Partiel',del:'Suppr.',cancel:'Annuler',save:'Sauvegarder',
    postEntry:'Valider',saveInvoice:'Enregistrer',savePurchase:'Enregistrer',
    balanced:'Équilibré',unbalanced:'Déséquilibré',collect:'Encaisser',pay:'Payer',
    exportExcel:'Exporter Excel',exportPDF:'Exporter PDF',
    noDataYet:'Pas encore de données.',addTransactions:'Ajoutez des transactions pour voir le graphique'
  },
  de:{
    dashboard:'Dashboard',contacts:'Kontakte',sales:'Verkäufe',purchases:'Einkäufe',
    collections:'Zahlungseingänge',payments:'Zahlungen',journal:'Buchungsjournal',
    pl:'GuV-Rechnung',bs:'Bilanz',cf:'Kapitalflussrechnung',settings:'Einstellungen',
    newInvoice:'+ Neue Rechnung',newPurchase:'+ Neuer Kauf',newCollection:'+ Eingang',
    newPayment:'+ Zahlung',newEntry:'+ Neuer Eintrag',newContact:'+ Neuer Kontakt',
    overview:'Übersicht',operations:'Operationen',reports:'Berichte',
    totalRevenue:'Gesamtumsatz',totalExpenses:'Gesamtkosten',netIncome:'Nettoergebnis',
    cashPosition:'Kassenbestand',accountsReceivable:'Forderungen',accountsPayable:'Verbindlichkeiten',
    salesInvoices:'Verkaufsrechnungen',purchaseInvoices:'Einkaufsrechnungen',netMargin:'Nettomarge',
    recentTransactions:'Letzte Transaktionen',invoiced:'Fakturiert',collected:'Eingegangen',
    pendingAR:'Ausstehend',count:'Anz.',purchased:'Eingekauft',paid:'Bezahlt',pendingAP:'Zu zahlen',
    totalCollected:'Gesamt Eingegangen',thisMonth:'Diesen Monat',totalPaid:'Gesamt Bezahlt',
    grossProfit:'Bruttogewinn',operatingExpenses:'Betriebskosten',
    totalAssets:'Gesamtvermögen',totalLiabilities:'Gesamtverbindlichkeiten',totalEquity:'Eigenkapital',
    currentAssets:'Umlaufvermögen',nonCurrentAssets:'Anlagevermögen',
    currentLiabilities:'Kurzfristige Verbindlichkeiten',nonCurrentLiabilities:'Langfristige Verbindlichkeiten',
    equity:'Eigenkapital',operatingActivities:'Betriebliche Tätigkeit',
    investingActivities:'Investitionstätigkeit',financingActivities:'Finanzierungstätigkeit',
    netChangeInCash:'Nettoveränderung Kassenbestand',closingBalance:'Abschlusssaldo',
    openingBalance:'Eröffnungssaldo',welcomeBack:'Willkommen,',date:'Datum',customer:'Kunde',
    supplier:'Lieferant',description:'Beschreibung',total:'Gesamt',status:'Status',method:'Methode',
    pending:'Ausstehend',paid2:'Bezahlt',partial:'Teilweise',del:'Löschen',cancel:'Abbrechen',save:'Speichern',
    postEntry:'Buchen',saveInvoice:'Rechnung speichern',savePurchase:'Kauf speichern',
    balanced:'Ausgeglichen',unbalanced:'Nicht ausgeglichen',collect:'Einziehen',pay:'Bezahlen',
    exportExcel:'Excel exportieren',exportPDF:'PDF exportieren',
    noDataYet:'Noch keine Daten.',addTransactions:'Transaktionen hinzufügen um Diagramm zu sehen'
  }
};

function t(key){ return (T[DB.prefs.lang||'en']||T.en)[key] || (T.en[key]) || key; }

function applyTranslations(){
  var lang = DB.prefs.lang || 'en';
  // Nav items
  var navMap = {
    'dashboard':'dashboard','contacts':'contacts','sales':'sales','purchases':'purchases',
    'collections':'collections','payments':'payments','journal':'journal',
    'pl':'pl','bs':'bs','cf':'cf'
  };
  document.querySelectorAll('.nav-item').forEach(function(el){
    var match = el.getAttribute('onclick')||'';
    var pg = match.replace("nav('","").replace("')","");
    if(T[lang] && T[lang][pg]) el.childNodes[1] && (el.childNodes[1].textContent = T[lang][pg]);
  });
  // Nav sections
  var secs = document.querySelectorAll('.nav-sec');
  var secLabels = [t('overview'), t('operations'), t('reports')];
  secs.forEach(function(s,i){ if(secLabels[i]) s.textContent = secLabels[i]; });
  // Topbar greeting
  var greetEl = document.querySelector('.greeting');
  if(greetEl) greetEl.childNodes[0].textContent = t('welcomeBack') + ' ';
  // Settings button
    // settings btn
  if(settBtn) settBtn.textContent = '⚙ ' + t('settings');
  // Chart placeholder
  var chartPh = document.querySelector('#chartBars div');
  if(chartPh && chartPh.textContent.indexOf('Add') >= 0) chartPh.textContent = t('addTransactions');
}

function setDateFilter(from, to) {
  _dateFrom = from || '';
  _dateTo   = to   || '';
  // Sync all date inputs across pages
  ['df-from','df-from2','df-from3'].forEach(function(id){
    var el=document.getElementById(id); if(el)el.value=_dateFrom;
  });
  ['df-to','df-to2','df-to3'].forEach(function(id){
    var el=document.getElementById(id); if(el)el.value=_dateTo;
  });
  // Toggle filter badge
  var active = _dateFrom || _dateTo;
  document.querySelectorAll('#df-badge,#df-badge2,#df-badge3').forEach(function(b){
    if(b) b.style.display = active ? 'inline-flex' : 'none';
  });
  renderAll();
}

function inRange(date) {
  if (!date) return true;
  if (_dateFrom && date < _dateFrom) return false;
  if (_dateTo   && date > _dateTo)   return false;
  return true;
}

function cF(){
  // ══════════════════════════════════════════════════════════════════════════
  // SINGLE SOURCE OF TRUTH: Journal Entries drive ALL financial statements.
  // DB.sales / DB.purch are used only for operational views (lists, A/R, A/P).
  // ══════════════════════════════════════════════════════════════════════════

  // Date-filtered JEs for P&L and CF
  var jes = DB.je.filter(function(x){ return inRange(x.date); });

  // Account classification
  var CASH_ACCTS    = ['1000'];
  var AR_ACCTS      = ['1100'];
  var AP_ACCTS      = ['2000'];
  var INVEST_ACCTS  = ['1500','1510'];
  var FINANCE_ACCTS = ['2500','3000','3100','2200'];
  var REV_ACCTS     = ['4000','4100'];
  var COGS_ACCTS    = ['5000'];
  var OPEX_ACCTS    = ['6000','6100','6200','6300','6400','6500','6900'];
  var FINEXP_ACCTS  = ['7000','7100'];

  // ── P&L — read directly from JE account balances ─────────────────────────
  var plBalances = {};
  jes.forEach(function(je){
    je.lines.forEach(function(l){
      if(!plBalances[l.account]) plBalances[l.account]={dr:0,cr:0};
      plBalances[l.account].dr += (l.debit  || 0);
      plBalances[l.account].cr += (l.credit || 0);
    });
  });

  function plBal(acc){
    var b = plBalances[acc]; if(!b) return 0;
    var acct = COA.find(function(a){return a.c===acc;});
    if(!acct) return b.dr - b.cr;
    if(acct.t==='revenue') return b.cr - b.dr;  // revenue: Cr positive
    return b.dr - b.cr;                           // expense/asset: Dr positive
  }

  // Revenue
  var rev = REV_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);

  // COGS
  var cogs = COGS_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);

  // OpEx by category name
  var opex = {};
  OPEX_ACCTS.forEach(function(acc){
    var bal = plBal(acc);
    if(bal !== 0){
      var acct = COA.find(function(a){return a.c===acc;});
      var name = acct ? acct.n : acc;
      opex[name] = (opex[name]||0) + bal;
    }
  });
  var toOpEx = Object.values(opex).reduce(function(a,v){return a+v;},0);
  var ebit   = rev - cogs - toOpEx;

  // Financial expenses (interest, tax)
  var finExp = FINEXP_ACCTS.reduce(function(a,acc){return a+plBal(acc);},0);
  var ni     = ebit - finExp;

  // ── CASH FLOW — read from 1000 Cash movements in JEs ─────────────────────
  var jeOCF=0, jeICF=0, jeFCF=0;
  var jeOCFLines=[], jeICFLines=[], jeFCFLines=[];

  jes.forEach(function(je){
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account) < 0) return;
      var cashMove = (l.debit||0) - (l.credit||0); // Dr=in, Cr=out
      var others = je.lines.filter(function(o){return o!==l;});
      var toInvest  = others.some(function(o){return INVEST_ACCTS.indexOf(o.account)>=0;});
      var toFinance = others.some(function(o){return FINANCE_ACCTS.indexOf(o.account)>=0;});
      var toAR      = others.some(function(o){return AR_ACCTS.indexOf(o.account)>=0;});
      var toAP      = others.some(function(o){return AP_ACCTS.indexOf(o.account)>=0;});
      if(toInvest){
        jeICF += cashMove;
        if(cashMove!==0) jeICFLines.push({desc:je.desc,amt:cashMove});
      } else if(toFinance){
        jeFCF += cashMove;
        if(cashMove!==0) jeFCFLines.push({desc:je.desc,amt:cashMove});
      } else {
        // Operating: includes collections (Dr Cash/Cr AR) and payments (Dr AP/Cr Cash)
        jeOCF += cashMove;
        if(cashMove!==0) jeOCFLines.push({desc:je.desc,amt:cashMove});
      }
    });
  });

  var totColl = jes.reduce(function(a,je){
    // Cash IN from operations = Dr 1000 where other side is AR or revenue
    var cashIn=0;
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account)>=0 && l.debit>0){
        var others=je.lines.filter(function(o){return o!==l;});
        var fromAR=others.some(function(o){return AR_ACCTS.indexOf(o.account)>=0;});
        var fromRev=others.some(function(o){return REV_ACCTS.indexOf(o.account)>=0;});
        if(fromAR||fromRev) cashIn+=l.debit;
      }
    });
    return a+cashIn;
  },0);

  var totPay = jes.reduce(function(a,je){
    // Cash OUT from operations = Cr 1000 where other side is AP or expense
    var cashOut=0;
    je.lines.forEach(function(l){
      if(CASH_ACCTS.indexOf(l.account)>=0 && l.credit>0){
        var others=je.lines.filter(function(o){return o!==l;});
        var toAP=others.some(function(o){return AP_ACCTS.indexOf(o.account)>=0;});
        var toExp=others.some(function(o){
          var ac=COA.find(function(a){return a.c===o.account;});
          return ac&&ac.t==='expense';
        });
        if(toAP||toExp) cashOut+=l.credit;
      }
    });
    return a+cashOut;
  },0);

  // Cash position = net of all Cash account movements
  var cash = jeOCF + jeICF + jeFCF;

  // ── A/R and A/P for operational views (from sales/purch lists) ───────────
  // These are still useful for Collections/Payments reconciliation
  var salesTotal  = DB.sales.reduce(function(a,x){return a+x.total;},0);
  var purchTotal  = DB.purch.reduce(function(a,x){return a+x.total;},0);
  var collTotal   = DB.coll.reduce(function(a,x){return a+x.amount;},0);
  var payTotal    = DB.pay.reduce(function(a,x){return a+x.amount;},0);
  var ar = Math.max(0, salesTotal - collTotal);
  var ap = Math.max(0, purchTotal - payTotal);

  // ── Balance Sheet — all account balances from ALL JEs (no date filter) ────
  var bsBalances = {};
  DB.je.forEach(function(je){
    je.lines.forEach(function(l){
      if(!bsBalances[l.account]) bsBalances[l.account]={dr:0,cr:0};
      bsBalances[l.account].dr += (l.debit  || 0);
      bsBalances[l.account].cr += (l.credit || 0);
    });
  });
  function jeBal(acc){
    var b=bsBalances[acc]; if(!b) return 0;
    var acct=COA.find(function(a){return a.c===acc;});
    if(!acct) return b.dr-b.cr;
    if(acct.t==='asset'||acct.t==='expense') return b.dr-b.cr;
    return b.cr-b.dr;
  }
  var jeFixedAssets  = jeBal('1500') - jeBal('1510');
  var jeLTDebt       = jeBal('2500');
  var jeShareCapital = jeBal('3000');
  var jeRetained     = jeBal('3100');
  var jeAccrued      = jeBal('2200');
  // Cash from BS = net of all 1000 movements
  var bsCash = jeBal('1000');
  // AR from BS = net of 1100
  var bsAR   = jeBal('1100');
  // AP from BS = net of 2000
  var bsAP   = jeBal('2000');
  // VAT = net of 2100
  var vatP   = jeBal('2100');

  return{
    rev:rev, cogs:cogs, opex:opex, toOpEx:toOpEx, ebit:ebit, ni:ni,
    finExp:finExp,
    totColl:totColl, totPay:totPay, cash:cash,
    ar:ar, ap:ap, vatP:vatP,
    totRev:rev, totExp:cogs+toOpEx+finExp,
    jeOCF:jeOCF, jeICF:jeICF, jeFCF:jeFCF,
    jeOCFLines:jeOCFLines, jeICFLines:jeICFLines, jeFCFLines:jeFCFLines,
    jeFixedAssets:jeFixedAssets, jeLTDebt:jeLTDebt,
    jeShareCapital:jeShareCapital, jeRetained:jeRetained, jeAccrued:jeAccrued,
    bsCash:bsCash, bsAR:bsAR, bsAP:bsAP,
    jeCashAdj:0
  };
}

// ── RENDERERS ──────────────────────────────────────────────────────────────
function rDash(){
  var F=cF();
  document.getElementById('kpi-rev').textContent=f(F.rev);
  document.getElementById('kpi-exp').textContent=f(F.cogs+F.toOpEx+F.finExp);
  var ni=document.getElementById('kpi-ni');ni.textContent=f(F.ni);ni.style.color=F.ni>=0?'var(--green)':'var(--red)';
  document.getElementById('kpi-cash').textContent=f(F.cash);
  document.getElementById('qs-ar').textContent=f(F.ar);document.getElementById('qs-ap').textContent=f(F.ap);
  document.getElementById('qs-sc').textContent=DB.sales.length;document.getElementById('qs-pc').textContent=DB.purch.length;document.getElementById('qs-jec').textContent=DB.je.length;
  var mg=document.getElementById('qs-mg');
  if(F.totRev){var p=(F.ni/F.totRev*100).toFixed(1);mg.textContent=p+'%';mg.style.color=p>=0?'var(--green)':'var(--red)';}else mg.textContent='—';
  if(DB.sales.length||DB.purch.length){
    var mo={};
    DB.sales.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].r+=x.net;});
    DB.purch.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].e+=x.net;});
    var ks=Object.keys(mo).sort().slice(-8),mv=Math.max.apply(null,ks.map(function(k){return Math.max(mo[k].r,mo[k].e);}));mv=Math.max(mv,1);
    var MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    document.getElementById('chartBars').innerHTML=ks.map(function(k){var d=mo[k],rh=Math.max(4,d.r/mv*140),eh=Math.max(4,d.e/mv*140),ml=k.substring(5,7),mn=MN[parseInt(ml)-1]||ml;return '<div class="bar-wrap"><div style="display:flex;gap:3px;align-items:flex-end;height:140px;"><div class="bar" style="background:var(--green);height:'+rh+'px;width:14px;" title="'+f(d.r)+'"></div><div class="bar" style="background:var(--red);height:'+eh+'px;width:14px;" title="'+f(d.e)+'"></div></div><div class="bar-lbl">'+mn+'</div></div>';}).join('');
  }else document.getElementById('chartBars').innerHTML='<div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:\'DM Mono\',monospace;">Add transactions to see chart</div>';
  var tmap={Sale:'bg',Purchase:'br',Collection:'bb',Payment:'by',Journal:'ba'};
  var all=[].concat(DB.sales.map(function(x){return{date:x.date,type:'Sale',desc:x.desc||'Sale',party:x.customer,amount:x.total,status:x.status};}),DB.purch.map(function(x){return{date:x.date,type:'Purchase',desc:x.desc||'Purchase',party:x.supplier,amount:-x.total,status:x.status};}),DB.coll.map(function(x){return{date:x.date,type:'Collection',desc:'Cash received',party:x.customer,amount:x.amount,status:'received'};}),DB.pay.map(function(x){return{date:x.date,type:'Payment',desc:'Cash paid',party:x.supplier,amount:-x.amount,status:'paid'};}),DB.je.map(function(x){return{date:x.date,type:'Journal',desc:x.desc,party:'Manual',amount:x.amount,status:'posted'};})).sort(function(a,b){return b.date<a.date?-1:1;}).slice(0,10);
  var rb=document.getElementById('recentTx');
  if(!all.length){rb.innerHTML='<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:24px;">No transactions yet. Start by adding a sale or purchase.</td></tr>';return;}
  rb.innerHTML=all.map(function(t){return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;">'+t.date+'</td><td><span class="badge '+(tmap[t.type]||'bb')+'">'+t.type+'</span></td><td>'+t.desc+'</td><td style="color:var(--text3);">'+t.party+'</td><td class="amt '+(t.amount>=0?'pos':'neg')+'">'+f(Math.abs(t.amount))+'</td><td>'+bdg(t.status)+'</td></tr>';}).join('');
}
function rSales(){
  var tot=DB.sales.reduce(function(a,x){return a+x.total;},0),coll=DB.coll.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('s-tot').textContent=f(tot);document.getElementById('s-coll').textContent=f(coll);document.getElementById('s-ar').textContent=f(Math.max(0,tot-coll));document.getElementById('s-cnt').textContent=DB.sales.length;
  var b=document.getElementById('salesTbl');
  if(!DB.sales.length){b.innerHTML='<tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr>';return;}
  b.innerHTML=DB.sales.slice().sort(function(a,c){return c.id-a.id;}).map(function(s){return '<tr><td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--accent);">'+s.num+'</span></td><td>'+s.date+'</td><td style="font-weight:500;color:var(--text);">'+s.customer+'</td><td style="color:var(--text3);">'+(s.desc||'—')+'</td><td class="amt">'+s.vatRate+'%</td><td class="amt">'+f(s.net)+'</td><td class="amt" style="color:var(--text3);">'+f(s.vatAmt)+'</td><td class="amt pos">'+f(s.total)+'</td><td>'+bdg(s.status)+'</td><td><button class="btn btn-danger btn-sm" onclick="delS('+s.id+')">Del</button></td></tr>';}).join('');
}
function rPurch(){
  var tot=DB.purch.reduce(function(a,x){return a+x.total;},0),paid=DB.pay.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('p-tot').textContent=f(tot);document.getElementById('p-paid').textContent=f(paid);document.getElementById('p-ap').textContent=f(Math.max(0,tot-paid));document.getElementById('p-cnt').textContent=DB.purch.length;
  var b=document.getElementById('purchTbl');
  if(!DB.purch.length){b.innerHTML='<tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr>';return;}
  b.innerHTML=DB.purch.slice().sort(function(a,c){return c.id-a.id;}).map(function(p){return '<tr><td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td><td>'+p.date+'</td><td style="font-weight:500;color:var(--text);">'+p.supplier+'</td><td style="color:var(--text3);">'+(p.desc||'—')+'</td><td><span class="badge bb">'+p.cat+'</span></td><td class="amt">'+p.vatRate+'%</td><td class="amt">'+f(p.net)+'</td><td class="amt" style="color:var(--text3);">'+f(p.vatAmt)+'</td><td class="amt neg">'+f(p.total)+'</td><td>'+bdg(p.status)+'</td><td><button class="btn btn-danger btn-sm" onclick="delP('+p.id+')">Del</button></td></tr>';}).join('');
}
// Current sale being reconciled
var _rcSaleId = null;

function openReconcileColl(saleId) {
  _rcSaleId = saleId;
  var s = DB.sales.find(function(x){return x.id===saleId;});
  if (!s) return;
  var collected = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
  var remaining = Math.max(0, s.total - collected);
  document.getElementById('rc-invoice-info').innerHTML =
    '<strong>' + s.num + '</strong> &nbsp;·&nbsp; ' + s.customer +
    ' &nbsp;·&nbsp; Total: <span style="color:var(--green);">' + f(s.total) + '</span>' +
    ' &nbsp;·&nbsp; Remaining: <span style="color:var(--yellow);">' + f(remaining) + '</span>';
  document.getElementById('rc-date').value = td();
  document.getElementById('rc-amount').value = remaining.toFixed(2);
  document.getElementById('rc-notes').value = '';
  openOverlay('ov-reconcile-coll');
}

function confirmCollect() {
  var s = DB.sales.find(function(x){return x.id===_rcSaleId;});
  if (!s) return;
  var amt = parseFloat(document.getElementById('rc-amount').value)||0;
  if (!amt) { alert('Enter an amount.'); return; }
  var dt  = document.getElementById('rc-date').value;
  var mth2 = document.getElementById('rc-method').value;
  var notes = document.getElementById('rc-notes').value;

  // 1. Create collection record
  DB.coll.push({id:DB.ids.c++, date:dt, customer:s.customer, ref:s.num, method:mth2, amount:amt, notes:notes||'Reconciled from '+s.num});

  // 2. Auto journal entry: Dr Cash / Cr Accounts Receivable
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Collection — ' + s.customer + ' / ' + s.num,
    lines: [
      {account:'1000', debit:amt,  credit:0},   // Dr Cash & Bank
      {account:'1100', debit:0,    credit:amt}   // Cr Accounts Receivable
    ],
    amount: amt,
    auto: true
  });

  // 3. Update sale status
  var collected2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
  if (collected2 >= s.total - 0.01) s.status = 'paid';
  else if (collected2 > 0) s.status = 'partial';

  sv(); closeOverlay('ov-reconcile-coll'); renderAll();
}

function rColl(){
  var totalInvoiced = DB.sales.reduce(function(a,x){return a+x.total;},0);
  var tot=DB.coll.reduce(function(a,x){return a+x.amount;},0);
  var curym=ym(), mth2=DB.coll.filter(function(x){return x.date&&x.date.startsWith(curym);}).reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('c-invoiced').textContent=f(totalInvoiced);
  document.getElementById('c-tot').textContent=f(tot);
  document.getElementById('c-pending').textContent=f(Math.max(0,totalInvoiced-tot));
  document.getElementById('c-mth').textContent=f(mth2);
  document.getElementById('c-cnt').textContent=DB.coll.length;

  // ── Pending table (sales not fully collected) ──
  var pb = document.getElementById('pendingCollTbl');
  var pending = DB.sales.filter(function(s){
    var coll2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
    return coll2 < s.total - 0.01;
  });
  if (!pending.length) {
    pb.innerHTML = '<tr><td colspan="9" style="text-align:center;color:var(--text3);padding:20px;">✅ All invoices collected!</td></tr>';
  } else {
    pb.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(s){
      var coll2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem = s.total - coll2;
      return '<tr class="needs-coll">' +
        '<td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--accent);">'+s.num+'</span></td>' +
        '<td>'+s.date+'</td>' +
        '<td style="font-weight:600;color:var(--text);">'+s.customer+'</td>' +
        '<td style="color:var(--text3);">'+(s.desc||'—')+'</td>' +
        '<td class="amt">'+f(s.total)+'</td>' +
        '<td class="amt pos">'+f(coll2)+'</td>' +
        '<td class="amt" style="color:var(--yellow);">'+f(rem)+'</td>' +
        '<td><select onchange="this.dataset.v=this.value" data-v="bank" style="padding:4px 8px;font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:5px;color:var(--text);"><option value=\'bank\'>🏦 Bank</option><option value=\'cash\'>💵 Cash</option><option value=\'card\'>💳 Card</option><option value=\'other\'>📋 Other</option></select></td>' +
        '<td><button class="btn-reconcile" onclick="openReconcileColl('+s.id+')">⚡ Collect</button></td>' +
        '</tr>';
    }).join('');
  }

  // ── Collection history ──
  var b=document.getElementById('collTbl');
  if(!DB.coll.length){b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:20px;">No collections yet.</td></tr>';return;}
  b.innerHTML=DB.coll.slice().sort(function(a,c){return c.id-a.id;}).map(function(c){
    return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text3);">#'+c.id+'</td><td>'+c.date+'</td><td style="font-weight:500;color:var(--text);">'+c.customer+'</td><td style="color:var(--text3);">'+(c.ref||'—')+'</td><td>'+mth(c.method)+'</td><td class="amt pos">'+f(c.amount)+'</td><td style="color:var(--text3);">'+(c.notes||'—')+'</td><td><button class="btn btn-danger btn-sm" onclick="delC('+c.id+')">Del</button></td></tr>';
  }).join('');
}
var _rpPurchId = null;

function openReconcilePay(purchId) {
  _rpPurchId = purchId;
  var p = DB.purch.find(function(x){return x.id===purchId;});
  if (!p) return;
  var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
  var remaining = Math.max(0, p.total - paid);
  document.getElementById('rp-invoice-info').innerHTML =
    '<strong>' + p.num + '</strong> &nbsp;·&nbsp; ' + p.supplier +
    ' &nbsp;·&nbsp; <span class="badge bb">' + p.cat + '</span>' +
    ' &nbsp;·&nbsp; Total: <span style="color:var(--red);">' + f(p.total) + '</span>' +
    ' &nbsp;·&nbsp; Remaining: <span style="color:var(--yellow);">' + f(remaining) + '</span>';
  document.getElementById('rp-date').value = td();
  document.getElementById('rp-amount').value = remaining.toFixed(2);
  document.getElementById('rp-notes').value = '';
  openOverlay('ov-reconcile-pay');
}

function confirmPay() {
  var p = DB.purch.find(function(x){return x.id===_rpPurchId;});
  if (!p) return;
  var amt = parseFloat(document.getElementById('rp-amount').value)||0;
  if (!amt) { alert('Enter an amount.'); return; }
  var dt   = document.getElementById('rp-date').value;
  var mth2 = document.getElementById('rp-method').value;
  var notes = document.getElementById('rp-notes').value;

  // 1. Create payment record
  DB.pay.push({id:DB.ids.py++, date:dt, supplier:p.supplier, ref:p.num, method:mth2, amount:amt, notes:notes||'Reconciled from '+p.num});

  // 2. Auto journal entry: Dr Accounts Payable / Cr Cash
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Payment — ' + p.supplier + ' / ' + p.num,
    lines: [
      {account:'2000', debit:amt, credit:0},   // Dr Accounts Payable
      {account:'1000', debit:0,   credit:amt}   // Cr Cash & Bank
    ],
    amount: amt,
    auto: true
  });

  // 3. Update purchase status
  var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
  if (paid2 >= p.total - 0.01) p.status = 'paid';

  sv(); closeOverlay('ov-reconcile-pay'); renderAll();
}

function rPay(){
  var totalPurch = DB.purch.reduce(function(a,x){return a+x.total;},0);
  var tot=DB.pay.reduce(function(a,x){return a+x.amount;},0);
  var curym=ym(), mth2=DB.pay.filter(function(x){return x.date&&x.date.startsWith(curym);}).reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('py-purchased').textContent=f(totalPurch);
  document.getElementById('py-tot').textContent=f(tot);
  document.getElementById('py-pending').textContent=f(Math.max(0,totalPurch-tot));
  document.getElementById('py-mth').textContent=f(mth2);
  document.getElementById('py-cnt').textContent=DB.pay.length;

  // ── Pending table (purchases not fully paid) ──
  var pb = document.getElementById('pendingPayTbl');
  var pending = DB.purch.filter(function(p){
    var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
    return paid2 < p.total - 0.01;
  });
  if (!pending.length) {
    pb.innerHTML = '<tr><td colspan="10" style="text-align:center;color:var(--text3);padding:20px;">✅ All invoices paid!</td></tr>';
  } else {
    pb.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(p){
      var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem = p.total - paid2;
      return '<tr class="needs-coll">' +
        '<td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td>' +
        '<td>'+p.date+'</td>' +
        '<td style="font-weight:600;color:var(--text);">'+p.supplier+'</td>' +
        '<td style="color:var(--text3);">'+(p.desc||'—')+'</td>' +
        '<td><span class="badge bb">'+p.cat+'</span></td>' +
        '<td class="amt">'+f(p.total)+'</td>' +
        '<td class="amt pos">'+f(paid2)+'</td>' +
        '<td class="amt" style="color:var(--yellow);">'+f(rem)+'</td>' +
        '<td><select style="padding:4px 8px;font-size:11px;background:var(--surface2);border:1px solid var(--border);border-radius:5px;color:var(--text);"><option value=\'bank\'>🏦 Bank</option><option value=\'cash\'>💵 Cash</option><option value=\'card\'>💳 Card</option><option value=\'other\'>📋 Other</option></select></td>' +
        '<td><button class="btn-reconcile" onclick="openReconcilePay('+p.id+')">⚡ Pay</button></td>' +
        '</tr>';
    }).join('');
  }

  // ── Payment history ──
  var b=document.getElementById('payTbl');
  if(!DB.pay.length){b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:20px;">No payments yet.</td></tr>';return;}
  b.innerHTML=DB.pay.slice().sort(function(a,c){return c.id-a.id;}).map(function(p){
    return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--text3);">#'+p.id+'</td><td>'+p.date+'</td><td style="font-weight:500;color:var(--text);">'+p.supplier+'</td><td style="color:var(--text3);">'+(p.ref||'—')+'</td><td>'+mth(p.method)+'</td><td class="amt neg">'+f(p.amount)+'</td><td style="color:var(--text3);">'+(p.notes||'—')+'</td><td><button class="btn btn-danger btn-sm" onclick="delPy('+p.id+')">Del</button></td></tr>';
  }).join('');
}
function rJE(){
  var b=document.getElementById('jeTbl');
  if(!DB.je.length){
    b.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No journal entries yet.</td></tr>';
    return;
  }
  var srcColors={sale:'var(--green)',purchase:'var(--red)',collection:'var(--blue)',payment:'var(--yellow)',manual:'var(--purple)'};
  var srcLabels={sale:'SALE',purchase:'PURCH',collection:'COLL',payment:'PAY',manual:'MANUAL'};
  var rows = DB.je.slice().sort(function(a,z){return z.id-a.id;});
  b.innerHTML = '';
  rows.forEach(function(je){
    var dl = je.lines.find(function(l){return l.debit>0;});
    var cl = je.lines.find(function(l){return l.credit>0;});
    function acName(l){
      if(!l) return '—';
      var a = COA.find(function(ac){return ac.c===l.account;});
      return a ? a.n : l.account;
    }
    var stype  = je.sourceType || 'manual';
    var scolor = srcColors[stype] || 'var(--purple)';
    var slabel = srcLabels[stype] || 'MANUAL';
    var allLines = je.lines.map(function(l){
      var a = COA.find(function(ac){return ac.c===l.account;});
      return (l.debit>0?'Dr ':'Cr ')+(a?a.n:l.account)+' '+f(l.debit||l.credit);
    }).join(' | ');

    var tr = document.createElement('tr');
    tr.title = allLines;

    var td1 = document.createElement('td');
    td1.style.cssText = 'font-size:11px;color:var(--purple);font-family:monospace;';
    td1.textContent = 'JE-'+String(je.id).padStart(3,'0');

    var td2 = document.createElement('td');
    td2.textContent = je.date;

    var td3 = document.createElement('td');
    var badge = document.createElement('span');
    badge.className = 'badge';
    badge.style.cssText = 'background:transparent;color:'+scolor+';border:1px solid '+scolor+';';
    badge.textContent = slabel;
    td3.appendChild(badge);

    var td4 = document.createElement('td');
    td4.style.cssText = 'font-weight:500;color:var(--text);';
    td4.textContent = je.desc;

    var td5 = document.createElement('td');
    td5.style.cssText = 'color:var(--green);font-size:12px;';
    td5.textContent = acName(dl);

    var td6 = document.createElement('td');
    td6.style.cssText = 'color:var(--red);font-size:12px;';
    td6.textContent = acName(cl);

    var td7 = document.createElement('td');
    td7.className = 'amt';
    td7.style.color = 'var(--purple)';
    td7.textContent = f(je.amount);

    var td8 = document.createElement('td');
    var btn = document.createElement('button');
    btn.className = 'btn btn-danger btn-sm';
    btn.textContent = 'Del';
    btn.onclick = (function(jid){return function(){delJ(jid);};})(je.id);
    td8.appendChild(btn);

    [td1,td2,td3,td4,td5,td6,td7,td8].forEach(function(td){tr.appendChild(td);});
    b.appendChild(tr);
  });
}
function plTab(m){plMode=m;document.getElementById('pl-det').classList.toggle('active',m==='detail');document.getElementById('pl-sum').classList.toggle('active',m==='summary');rPL();}
function rPL(){
  var F=cF(),b=document.getElementById('plBody'),gp=F.rev-F.cogs;
  var gmp=F.totRev?(gp/F.totRev*100).toFixed(1):0,npp=F.totRev?(F.ni/F.totRev*100).toFixed(1):0;
  if(plMode==='summary'){b.innerHTML='<tr class="rh"><td colspan="2">Summary P&L</td></tr><tr class="rd"><td>Total Revenue</td><td class="num pos">'+f(F.totRev)+'</td></tr><tr class="rd"><td>Cost of Goods Sold</td><td class="num neg">('+f(F.cogs)+')</td></tr><tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num">'+f(gp)+'</td></tr><tr class="rd"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx)+')</td></tr><tr class="rs"><td>EBIT</td><td class="num">'+f(F.ebit)+'</td></tr><tr class="rd"><td>Journal Adjustments (net)</td><td class="num">'+f(F.jeR-F.jeE)+'</td></tr><tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';return;}
  var rows='<tr class="rh"><td colspan="2">Revenue</td></tr><tr class="rd"><td class="ind">Sales Revenue</td><td class="num pos">'+f(F.rev)+'</td></tr>';
  // Revenue already fully from JE accounts - no separate adjustment line needed
  rows+='<tr class="rs"><td>Total Revenue</td><td class="num">'+f(F.totRev)+'</td></tr><tr class="rh"><td colspan="2">Cost of Goods Sold</td></tr><tr class="rd"><td class="ind">COGS – Direct Purchases</td><td class="num neg">('+f(F.cogs)+')</td></tr><tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num '+(gp>=0?'pos':'neg')+'">'+f(gp)+'</td></tr><tr class="rh"><td colspan="2">Operating Expenses</td></tr>';
  Object.entries(F.opex).forEach(function(e){rows+='<tr class="rd"><td class="ind">'+e[0]+'</td><td class="num neg">('+f(e[1])+')</td></tr>';});
  // Expenses already fully from JE accounts - no separate adjustment line needed
  if(!F.toOpEx&&!F.jeE)rows+='<tr class="rd"><td class="ind" style="color:var(--text3);">No expenses recorded</td><td class="num">—</td></tr>';
  rows+='<tr class="rs"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx+F.jeE)+')</td></tr><tr class="rs"><td>EBIT (Operating Income)</td><td class="num">'+f(F.ebit)+'</td></tr><tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';
  b.innerHTML=rows;
}
function rBS(){
  var F = cF();

  // ── ASSETS ────────────────────────────────────────────────────────────────
  // Cash = operating cash + JE cash movements
  var cash    = F.bsCash;  // from JE account 1000 balance
  var ar      = F.bsAR;    // from JE account 1100 balance
  var tca     = cash + ar;
  // Non-current: Fixed Assets net from JEs
  var fixedA  = F.jeFixedAssets;
  var ta      = tca + (fixedA > 0 ? fixedA : 0);

  // ── LIABILITIES ───────────────────────────────────────────────────────────
  var ap      = F.bsAP;    // from JE account 2000 balance
  var vatp    = Math.max(0, F.vatP); // from JE account 2100 balance
  var accrued = F.jeAccrued;
  var tcl     = ap + vatp + accrued;
  var ltDebt  = F.jeLTDebt;
  var tl      = tcl + ltDebt;

  // ── EQUITY ────────────────────────────────────────────────────────────────
  var shareC  = F.jeShareCapital;
  var retained= F.jeRetained;
  var netInc  = F.ni;
  var te      = shareC + retained + netInc;
  var tle     = tl + te;

  // ── ASSETS SIDE ───────────────────────────────────────────────────────────
  var aRows = '<tr class="rh"><td colspan="2">Current Assets</td></tr>';
  aRows += '<tr class="rd"><td class="ind">Cash &amp; Bank</td><td class="num">'+f(cash)+'</td></tr>';
  aRows += '<tr class="rd"><td class="ind">Accounts Receivable</td><td class="num">'+f(ar)+'</td></tr>';
  aRows += '<tr class="rs"><td>Total Current Assets</td><td class="num">'+f(tca)+'</td></tr>';
  aRows += '<tr class="rh"><td colspan="2">Non-Current Assets</td></tr>';
  if(fixedA > 0){
    aRows += '<tr class="rd"><td class="ind">Fixed Assets (net)</td><td class="num">'+f(fixedA)+'</td></tr>';
  } else {
    aRows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — use Journal Entries</td><td class="num">—</td></tr>';
  }
  aRows += '<tr class="rt"><td>TOTAL ASSETS</td><td class="num">'+f(ta)+'</td></tr>';

  // ── LIABILITIES & EQUITY SIDE ─────────────────────────────────────────────
  var lRows = '<tr class="rh"><td colspan="2">Current Liabilities</td></tr>';
  lRows += '<tr class="rd"><td class="ind">Accounts Payable</td><td class="num">'+f(ap)+'</td></tr>';
  lRows += '<tr class="rd"><td class="ind">VAT Payable (net)</td><td class="num">'+f(vatp)+'</td></tr>';
  if(accrued !== 0) lRows += '<tr class="rd"><td class="ind">Accrued Liabilities</td><td class="num">'+f(accrued)+'</td></tr>';
  lRows += '<tr class="rs"><td>Total Current Liabilities</td><td class="num">'+f(tcl)+'</td></tr>';
  lRows += '<tr class="rh"><td colspan="2">Non-Current Liabilities</td></tr>';
  if(ltDebt > 0){
    lRows += '<tr class="rd"><td class="ind">Long-term Debt</td><td class="num">'+f(ltDebt)+'</td></tr>';
  } else {
    lRows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded</td><td class="num">—</td></tr>';
  }
  lRows += '<tr class="rs"><td>Total Liabilities</td><td class="num">'+f(tl)+'</td></tr>';
  lRows += '<tr class="rh"><td colspan="2">Equity</td></tr>';
  if(shareC !== 0) lRows += '<tr class="rd"><td class="ind">Share Capital</td><td class="num">'+f(shareC)+'</td></tr>';
  if(retained !== 0) lRows += '<tr class="rd"><td class="ind">Retained Earnings</td><td class="num">'+f(retained)+'</td></tr>';
  lRows += '<tr class="rd"><td class="ind">Net Income (Period)</td><td class="num '+(netInc>=0?'pos':'neg')+'">'+f(netInc)+'</td></tr>';
  lRows += '<tr class="rs"><td>Total Equity</td><td class="num">'+f(te)+'</td></tr>';
  lRows += '<tr class="rt"><td>TOTAL LIAB. &amp; EQUITY</td><td class="num">'+f(tle)+'</td></tr>';

  document.getElementById('bsA').innerHTML  = aRows;
  document.getElementById('bsLE').innerHTML = lRows;

  var diff = Math.abs(ta - tle);
  var ck   = document.getElementById('bsChk');
  if(diff < 0.01){
    ck.textContent = '✓ Balanced — Assets = Liabilities + Equity';
    ck.style.color = 'var(--green)';
  } else {
    ck.textContent = '⚠ Unbalanced by ' + f(diff) + ' — check your Journal Entries';
    ck.style.color = 'var(--yellow)';
  }
}
function rCF(){
  var F=cF();
  var ocf = F.totColl - F.totPay + F.jeOCF;
  var icf = F.jeICF;
  var fcf = F.jeFCF;
  var netCF = ocf + icf + fcf;

  function jeLines(lines, sign) {
    if(!lines || !lines.length) return '';
    return lines.map(function(l){
      var amt = l.amt;
      var cls = amt >= 0 ? 'pos' : 'neg';
      var disp = amt >= 0 ? f(amt) : '('+f(Math.abs(amt))+')';
      return '<tr class="rd"><td class="ind" style="color:var(--text2);">↳ '+l.desc+'</td><td class="num '+cls+'">'+disp+'</td></tr>';
    }).join('');
  }

  var rows = '';

  // ── OPERATING ────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Operating Activities</td></tr>';
  rows += '<tr class="rd"><td class="ind">Cash received from customers</td><td class="num pos">'+f(F.totColl)+'</td></tr>';
  rows += '<tr class="rd"><td class="ind">Cash paid to suppliers</td><td class="num neg">('+f(F.totPay)+')</td></tr>';
  rows += jeLines(F.jeOCFLines);
  if(!F.jeOCFLines.length && F.jeOCF === 0) {
    // no extra lines
  }
  rows += '<tr class="rs"><td>Net Cash from Operating Activities</td><td class="num '+(ocf>=0?'pos':'neg')+'">'+f(ocf)+'</td></tr>';

  // ── INVESTING ────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Investing Activities</td></tr>';
  if(F.jeICFLines && F.jeICFLines.length) {
    rows += jeLines(F.jeICFLines);
  } else {
    rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — Dr. Fixed Assets / Cr. Cash in Journal Entries</td><td class="num">—</td></tr>';
  }
  rows += '<tr class="rs"><td>Net Cash from Investing Activities</td><td class="num '+(icf>=0?'pos':'neg')+'">'+f(icf)+'</td></tr>';

  // ── FINANCING ────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">Financing Activities</td></tr>';
  if(F.jeFCFLines && F.jeFCFLines.length) {
    rows += jeLines(F.jeFCFLines);
  } else {
    rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — Dr. Cash / Cr. Long-term Debt or Share Capital in Journal Entries</td><td class="num">—</td></tr>';
  }
  rows += '<tr class="rs"><td>Net Cash from Financing Activities</td><td class="num '+(fcf>=0?'pos':'neg')+'">'+f(fcf)+'</td></tr>';

  // ── TOTALS ───────────────────────────────────────────────────────────────
  rows += '<tr class="rt"><td>NET CHANGE IN CASH</td><td class="num '+(netCF>=0?'pos':'neg')+'">'+f(netCF)+'</td></tr>';
  rows += '<tr class="rd" style="border-top:1px solid var(--border);"><td style="color:var(--text3);">Opening Cash Balance</td><td class="num" style="color:var(--text3);">'+f(0)+'</td></tr>';
  rows += '<tr class="rs"><td>Closing Cash Balance</td><td class="num" style="color:var(--accent);">'+f(netCF)+'</td></tr>';

  document.getElementById('cfBody').innerHTML = rows;
}

// ══════════════════════════════════════════════════════════════════
// CONTACTS MODULE
// ══════════════════════════════════════════════════════════════════

var _ctFilter = 'all';
var _ctEditId = null;
var _ctType   = 'client';
var _ctTab    = 'basic';

function setCtFilter(f) {
  _ctFilter = f;
  ['all','client','supplier','both'].forEach(function(x){
    var el = document.getElementById('ctf-'+x);
    if(el) el.classList.toggle('active', x===f);
  });
  rContacts();
}

function openContactModal(type, id) {
  _ctEditId = id || null;
  _ctType   = type || 'client';
  _ctTab    = 'basic';

  // Reset all tabs
  document.querySelectorAll('.contact-tab').forEach(function(t,i){
    t.classList.toggle('active', i===0);
  });
  document.querySelectorAll('.contact-panel').forEach(function(p,i){
    p.classList.toggle('active', i===0);
  });

  // Set type buttons
  setCtType(_ctType);

  var deleteBtn = document.getElementById('ct-delete-btn');

  if(id) {
    var ct = DB.contacts.find(function(x){return x.id===id;});
    if(!ct) return;
    document.getElementById('ct-modal-title').textContent = 'Edit Contact';
    deleteBtn.style.display = 'inline-flex';
    // Fill fields
    setCtType(ct.type||'client');
    document.getElementById('ct-name').value       = ct.name||'';
    document.getElementById('ct-nif').value        = ct.nif||'';
    document.getElementById('ct-tradename').value  = ct.tradename||'';
    document.getElementById('ct-addr').value       = ct.addr||'';
    document.getElementById('ct-city').value       = ct.city||'';
    document.getElementById('ct-postal').value     = ct.postal||'';
    document.getElementById('ct-province').value   = ct.province||'';
    document.getElementById('ct-country').value    = ct.country||'';
    document.getElementById('ct-email').value      = ct.email||'';
    document.getElementById('ct-phone').value      = ct.phone||'';
    document.getElementById('ct-mobile').value     = ct.mobile||'';
    document.getElementById('ct-web').value        = ct.web||'';
    document.getElementById('ct-iban').value       = ct.iban||'';
    document.getElementById('ct-bic').value        = ct.bic||'';
    document.getElementById('ct-bank').value       = ct.bank||'';
    document.getElementById('ct-payterms').value   = ct.payterms||'30days';
    document.getElementById('ct-creditlimit').value= ct.creditlimit||'';
    document.getElementById('ct-currency').value   = ct.currency||'EUR';
    document.getElementById('ct-salesvat').value   = ct.salesvat||'21';
    document.getElementById('ct-purchvat').value   = ct.purchvat||'21';
    document.getElementById('ct-lang').value       = ct.lang||'en';
    document.getElementById('ct-invoiceby').value  = ct.invoiceby||'email';
    document.getElementById('ct-notes').value      = ct.notes||'';
    document.getElementById('ct-debtacc').value    = ct.debtacc||'';
    document.getElementById('ct-credacc').value    = ct.credacc||'';
    document.getElementById('ct-salestax').value   = ct.salestax||'IVA21';
    document.getElementById('ct-purchtax').value   = ct.purchtax||'IVA21';
    document.getElementById('ct-acccode').value    = ct.acccode||'';
  } else {
    document.getElementById('ct-modal-title').textContent = 'New Contact';
    deleteBtn.style.display = 'none';
    // Clear fields
    ['ct-name','ct-nif','ct-tradename','ct-addr','ct-city','ct-postal','ct-province',
     'ct-country','ct-email','ct-phone','ct-mobile','ct-web','ct-iban','ct-bic',
     'ct-bank','ct-creditlimit','ct-notes','ct-acccode'].forEach(function(id){
      document.getElementById(id).value='';
    });
    document.getElementById('ct-payterms').value  = '30days';
    document.getElementById('ct-currency').value  = 'EUR';
    document.getElementById('ct-salesvat').value  = '21';
    document.getElementById('ct-purchvat').value  = '21';
    document.getElementById('ct-lang').value      = 'en';
    document.getElementById('ct-invoiceby').value = 'email';
    document.getElementById('ct-debtacc').value   = '';
    document.getElementById('ct-credacc').value   = '';
    document.getElementById('ct-salestax').value  = 'IVA21';
    document.getElementById('ct-purchtax').value  = 'IVA21';
  }
  openOverlay('ov-contact');
}

function setCtType(t) {
  _ctType = t;
  ['client','supplier','both'].forEach(function(x){
    var el = document.getElementById('ct-type-'+x);
    if(el) el.classList.toggle('active', x===t);
  });
}

function ctTab(name) {
  var panels = ['basic','accounts','preferences','accounting'];
  var tabs   = document.querySelectorAll('.contact-tab');
  panels.forEach(function(p, i){
    var panel = document.getElementById('ctpanel-'+p);
    if(panel) panel.classList.toggle('active', p===name);
    if(tabs[i]) tabs[i].classList.toggle('active', p===name);
  });
}

function saveContact() {
  var name = document.getElementById('ct-name').value.trim();
  if(!name){ alert('Please enter a contact name.'); return; }

  var ct = {
    id:          _ctEditId || DB.ids.ct++,
    type:        _ctType,
    name:        name,
    nif:         document.getElementById('ct-nif').value,
    tradename:   document.getElementById('ct-tradename').value,
    addr:        document.getElementById('ct-addr').value,
    city:        document.getElementById('ct-city').value,
    postal:      document.getElementById('ct-postal').value,
    province:    document.getElementById('ct-province').value,
    country:     document.getElementById('ct-country').value,
    email:       document.getElementById('ct-email').value,
    phone:       document.getElementById('ct-phone').value,
    mobile:      document.getElementById('ct-mobile').value,
    web:         document.getElementById('ct-web').value,
    iban:        document.getElementById('ct-iban').value,
    bic:         document.getElementById('ct-bic').value,
    bank:        document.getElementById('ct-bank').value,
    payterms:    document.getElementById('ct-payterms').value,
    creditlimit: parseFloat(document.getElementById('ct-creditlimit').value)||0,
    currency:    document.getElementById('ct-currency').value,
    salesvat:    document.getElementById('ct-salesvat').value,
    purchvat:    document.getElementById('ct-purchvat').value,
    lang:        document.getElementById('ct-lang').value,
    invoiceby:   document.getElementById('ct-invoiceby').value,
    notes:       document.getElementById('ct-notes').value,
    debtacc:     document.getElementById('ct-debtacc').value,
    credacc:     document.getElementById('ct-credacc').value,
    salestax:    document.getElementById('ct-salestax').value,
    purchtax:    document.getElementById('ct-purchtax').value,
    acccode:     document.getElementById('ct-acccode').value,
    createdAt:   _ctEditId ? (DB.contacts.find(function(x){return x.id===_ctEditId;})||{}).createdAt : new Date().toISOString().slice(0,10)
  };

  if(_ctEditId) {
    var idx = DB.contacts.findIndex(function(x){return x.id===_ctEditId;});
    if(idx>=0) DB.contacts[idx] = ct;
  } else {
    DB.contacts.push(ct);
  }

  sv(); closeOverlay('ov-contact'); rContacts();
  showToast('✅ Contact saved: ' + name);
}

function deleteContact() {
  if(!_ctEditId) return;
  var ct = DB.contacts.find(function(x){return x.id===_ctEditId;});
  if(!confirm('Delete contact: ' + (ct?ct.name:'') + '?')) return;
  DB.contacts = DB.contacts.filter(function(x){return x.id!==_ctEditId;});
  sv(); closeOverlay('ov-contact'); rContacts();
  showToast('🗑 Contact deleted');
}

// ── Render contacts grid ──────────────────────────────────────
function rContacts() {
  if(!DB.contacts) DB.contacts = [];
  var search = (document.getElementById('ct-search')||{}).value||'';
  search = search.toLowerCase();
  var grid = document.getElementById('contactsGrid');
  if(!grid) return;

  var filtered = DB.contacts.filter(function(ct){
    var matchType = _ctFilter==='all' || ct.type===_ctFilter || ct.type==='both' ||
                    (_ctFilter==='both' && ct.type==='both');
    if(_ctFilter !== 'all' && ct.type !== _ctFilter && ct.type !== 'both') matchType = false;
    if(_ctFilter === 'all') matchType = true;
    var matchSearch = !search ||
      (ct.name||'').toLowerCase().indexOf(search)>=0 ||
      (ct.nif||'').toLowerCase().indexOf(search)>=0 ||
      (ct.email||'').toLowerCase().indexOf(search)>=0 ||
      (ct.city||'').toLowerCase().indexOf(search)>=0;
    return matchType && matchSearch;
  });

  var countEl = document.getElementById('ct-count');
  if(countEl) countEl.textContent = filtered.length + ' contact' + (filtered.length!==1?'s':'');

  if(!filtered.length){
    grid.innerHTML = '<div style="color:var(--text3);font-size:13px;font-family:monospace;padding:32px;text-align:center;grid-column:1/-1;">' +
      (DB.contacts.length ? 'No contacts match your search.' : 'No contacts yet. Click &quot;+ New Contact&quot; to add your first client or supplier.') +
      '</div>';
    return;
  }

  var typeBadge = {client:'<span class="badge bb">Client</span>',supplier:'<span class="badge by">Supplier</span>',both:'<span class="badge ba">Client &amp; Supplier</span>'};

  grid.innerHTML = filtered.sort(function(a,b){return a.name.localeCompare(b.name);}).map(function(ct){
    var initials = ct.name.split(' ').map(function(w){return w[0];}).slice(0,2).join('').toUpperCase();
    var meta = [ct.nif, ct.city, ct.email].filter(Boolean).join(' · ');
    return '<div class="contact-card" onclick="openContactModal(\''+ct.type+'\','+ct.id+')">' +
      '<div class="contact-avatar">'+initials+'</div>' +
      '<div style="flex:1;min-width:0;">' +
        '<div class="contact-name">'+ct.name+'</div>' +
        '<div class="contact-meta">'+(meta||'No details added')+'</div>' +
      '</div>' +
      '<div class="contact-badge">'+(typeBadge[ct.type]||'')+'</div>' +
    '</div>';
  }).join('');
}

// ── Autocomplete for Sales/Purchase modals ────────────────────
function acSearch(inputId, listId, typeFilter) {
  var input = document.getElementById(inputId);
  var list  = document.getElementById(listId);
  if(!input || !list) return;
  var q = input.value.toLowerCase();

  if(!DB.contacts) DB.contacts = [];
  var matches = DB.contacts.filter(function(ct){
    var typeOk = typeFilter==='client'
      ? (ct.type==='client'||ct.type==='both')
      : typeFilter==='supplier'
      ? (ct.type==='supplier'||ct.type==='both')
      : true;
    var nameOk = !q || (ct.name||'').toLowerCase().indexOf(q)>=0 ||
                 (ct.nif||'').toLowerCase().indexOf(q)>=0;
    return typeOk && nameOk;
  }).slice(0, 8);

  if(!matches.length) { list.classList.remove('open'); return; }

  list.innerHTML = matches.map(function(ct){
    var meta = [ct.nif, ct.city].filter(Boolean).join(' · ');
    return '<div class="autocomplete-item" onmousedown="acSelect(\''+inputId+'\',\''+listId+'\',\''+ct.name.replace(/'/g,"\\'")+'\','+ct.id+')">' +
      '<div>'+ct.name+'</div>' +
      '<div class="ac-meta">'+(meta||ct.type)+'</div>' +
    '</div>';
  }).join('');
  list.classList.add('open');
}

function acSelect(inputId, listId, name, ctId) {
  var input = document.getElementById(inputId);
  if(input) input.value = name;
  closeAC(listId);
  // Auto-fill VAT if contact has preference
  var ct = DB.contacts.find(function(x){return x.id===ctId;});
  if(ct) {
    if(inputId==='s-cust' && ct.salesvat) {
      var vatEl = document.getElementById('s-vat');
      if(vatEl){ vatEl.value=ct.salesvat; calcS(); }
    }
    if(inputId==='p-sup' && ct.purchvat) {
      var vatEl2 = document.getElementById('p-vat');
      if(vatEl2){ vatEl2.value=ct.purchvat; calcP(); }
    }
  }
}

function closeAC(listId) {
  var list = document.getElementById(listId);
  if(list) list.classList.remove('open');
}

// contacts export handled inside getRows directly (see getRows function)

function renderAll(){rDash();rContacts();rSales();rPurch();rColl();rPay();rJE();rPL();rBS();rCF();}

init();

// ══════════════════════════════════════════════════════════════════
// EXPORT FUNCTIONS
// ══════════════════════════════════════════════════════════════════

// ── PDF EXPORT ────────────────────────────────────────────────────
function exportPDF(sectionId, title) {
  // Hide all pages, show only the target
  document.querySelectorAll('.page').forEach(function(p){p.style.display='none';});
  var target = document.getElementById('page-' + sectionId);
  target.style.display = 'block';
  // Set print title
  var oldTitle = document.title;
  document.title = 'FinLedger — ' + title + ' — ' + new Date().toLocaleDateString('en-GB');
  window.print();
  // Restore
  document.title = oldTitle;
  document.querySelectorAll('.page').forEach(function(p){p.style.display='';});
  target.classList.add('active');
}

// ── EXCEL EXPORT ──────────────────────────────────────────────────
// ── EXCEL/CSV EXPORT — via Python server (works in pywebview) ────
function getRows(type) {
  var rows=[], F;
  if(type==='sales'){
    rows.push(['Invoice #','Date','Customer','Description','VAT %','Net','VAT Amount','Total','Status','Method']);
    DB.sales.forEach(function(s){rows.push([s.num,s.date,s.customer,s.desc||'',s.vatRate,s.net,s.vatAmt,s.total,s.status,s.method]);});
  } else if(type==='purchases'){
    rows.push(['Invoice #','Date','Supplier','Description','Category','VAT %','Net','VAT Amount','Total','Status','Method']);
    DB.purch.forEach(function(p){rows.push([p.num,p.date,p.supplier,p.desc||'',p.cat,p.vatRate,p.net,p.vatAmt,p.total,p.status,p.method]);});
  } else if(type==='collections'){
    rows.push(['#','Date','Customer','Invoice Ref','Method','Amount','Notes']);
    DB.coll.forEach(function(c){rows.push([c.id,c.date,c.customer,c.ref||'',c.method,c.amount,c.notes||'']);});
  } else if(type==='payments'){
    rows.push(['#','Date','Supplier','Invoice Ref','Method','Amount','Notes']);
    DB.pay.forEach(function(p){rows.push([p.id,p.date,p.supplier,p.ref||'',p.method,p.amount,p.notes||'']);});
  } else if(type==='journal'){
    rows.push(['Entry #','Date','Type','Description','Account','Debit','Credit']);
    DB.je.forEach(function(je){je.lines.forEach(function(l,i){var acct=COA.find(function(a){return a.c===l.account;});rows.push([i===0?'JE-'+String(je.id).padStart(3,'0'):'',i===0?je.date:'',i===0?(je.sourceType||'manual').toUpperCase():'',i===0?je.desc:'',acct?acct.c+' - '+acct.n:l.account,l.debit||'',l.credit||'']);});});
  } else if(type==='pl'){
    F=cF();rows.push(['P&L — '+DB.co.name,''],['FY: '+DB.co.fy,''],['',''],['REVENUE',''],['Sales Revenue',F.rev]);
    if(F.jeR)rows.push(['Journal Revenue Adj.',F.jeR]);
    rows.push(['Total Revenue',F.totRev],['',''],['COGS',''],['Cost of Goods Sold',-F.cogs],['Gross Profit',F.rev-F.cogs],['',''],['OPERATING EXPENSES','']);
    Object.entries(F.opex).forEach(function(e){rows.push([e[0],-e[1]]);});
    rows.push(['Total OpEx',-F.toOpEx],['',''],['EBIT',F.ebit],['Journal Adj.',F.jeR-F.jeE],['NET INCOME',F.ni]);
  } else if(type==='bs'){
    F=cF();rows.push(['Balance Sheet — '+DB.co.name,''],['',''],['ASSETS',''],['Cash & Bank',F.cash],['Accounts Receivable',F.ar],['Total Assets',F.cash+F.ar],['',''],['LIABILITIES',''],['Accounts Payable',F.ap],['VAT Payable',Math.max(0,F.vatP)],['Total Liabilities',F.ap+Math.max(0,F.vatP)],['',''],['EQUITY',''],['Net Income',F.ni],['Total Equity',F.ni],['',''],['TOTAL LIAB. & EQUITY',F.ap+Math.max(0,F.vatP)+F.ni]);
  } else if(type==='cashflow'){
    F=cF();rows.push(['Cash Flow — '+DB.co.name,''],['',''],['OPERATING ACTIVITIES',''],['Cash received',F.totColl],['Cash paid',-F.totPay],['Net Operating CF',F.totColl-F.totPay],['',''],['INVESTING',''],['Net Investing CF',0],['',''],['FINANCING',''],['Net Financing CF',0],['',''],['NET CHANGE IN CASH',F.totColl-F.totPay],['Opening Balance',0],['Closing Balance',F.totColl-F.totPay]);
  } else if(type==='contacts'){
    rows.push(['Name','Type','NIF','Email','Phone','City','Country','IBAN','Payment Terms','VAT Sales','VAT Purchase','Notes']);
    (DB.contacts||[]).forEach(function(ct){
      rows.push([ct.name,ct.type,ct.nif||'',ct.email||'',ct.phone||'',ct.city||'',ct.country||'',ct.iban||'',ct.payterms||'',ct.salesvat||'',ct.purchvat||'',ct.notes||'']);
    });
  }
  return rows;
}

function rowsToCSV(rows) {
  // UTF-8 BOM so Excel opens it correctly
  return '\uFEFF' + rows.map(function(row){
    return row.map(function(v){
      var s = String(v===null||v===undefined?'':v);
      if(s.indexOf(',')>=0||s.indexOf('"')>=0||s.indexOf('\n')>=0) s='"'+s.replace(/"/g,'""')+'"';
      return s;
    }).join(',');
  }).join('\r\n');
}

function exportExcel(type) {
  var names={sales:'Sales_Invoices',purchases:'Purchase_Invoices',collections:'Collections',
    payments:'Payments',journal:'Journal_Entries',pl:'PL_Statement',bs:'Balance_Sheet',cashflow:'Cash_Flow'};
  var rows = getRows(type);
  if(!rows.length){alert('No data to export.');return;}
  var fname = 'FinLedger_'+(names[type]||type)+'_'+new Date().toISOString().slice(0,10)+'.csv';
  var csv   = rowsToCSV(rows);

  // ── Method 1: Standard browser download (works in Chrome/Firefox/Edge) ──
  // Try this first — works perfectly when accessed via http://localhost:8765
  try {
    var blob = new Blob([csv], {type:'text/csv;charset=utf-8;'});
    var url  = URL.createObjectURL(blob);
    var a    = document.createElement('a');
    a.href        = url;
    a.download    = fname;
    a.style.display = 'none';
    document.body.appendChild(a);
    a.click();
    // Check if download actually triggered (pywebview blocks it silently)
    var triggered = true;
    setTimeout(function(){
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
    }, 1000);
    // Give pywebview fallback after short delay
    setTimeout(function(){
      // If we are inside pywebview, the download won't have worked
      // so we also send to Python server as backup
      fetch('/export', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body: JSON.stringify({filename: fname, content: csv})
      })
      .then(function(r){return r.json();})
      .then(function(res){
        if(res.ok){
          showToast('✅ Descargado: ' + fname);
        }
      })
      .catch(function(){
        // In real browser this will fail (no server needed) — that's fine
      });
    }, 400);
    showToast('✅ Descargando: ' + fname);
  } catch(e) {
    showToast('❌ Error al descargar: ' + e);
  }
}

// ── Toast notification ─────────────────────────────────────────────
function showToast(msg) {
  var t = document.getElementById('fl-toast');
  if(!t){
    t = document.createElement('div');
    t.id = 'fl-toast';
    t.style.cssText = 'position:fixed;bottom:28px;right:28px;background:#1e1e24;border:1px solid #2e2e38;color:#f0f0f4;padding:12px 20px;border-radius:10px;font-family:DM Sans,sans-serif;font-size:13px;z-index:9999;box-shadow:0 4px 24px rgba(0,0,0,.5);transition:opacity .3s;max-width:400px;';
    document.body.appendChild(t);
  }
  t.textContent = msg;
  t.style.opacity = '1';
  clearTimeout(t._timer);
  t._timer = setTimeout(function(){t.style.opacity='0';}, 3500);
}
</script>

<!-- RECONCILE COLLECTION MODAL -->
<div class="overlay" id="ov-reconcile-coll">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Collect Payment</div><div class="mclose" onclick="closeOverlay('ov-reconcile-coll')">✕</div></div>
    <div class="mbody">
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
        <div id="rc-invoice-info" style="font-size:14px;color:var(--text);font-weight:500;"></div>
      </div>
      <div class="fgrid">
        <div class="fg"><label>Collection Date</label><input type="date" id="rc-date"></div>
        <div class="fg"><label>Payment Method</label>
          <select id="rc-method"><option value="bank">🏦 Bank Transfer</option><option value="cash">💵 Cash</option><option value="card">💳 Card</option><option value="other">📋 Other</option></select>
        </div>
        <div class="fg full"><label>Amount to Collect (€)</label><input type="number" id="rc-amount" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><input type="text" id="rc-notes" placeholder="Optional notes..."></div>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.06);border:1px solid rgba(200,255,0,.2);border-radius:7px;font-size:12px;color:var(--text3);">
        🔖 This will automatically create a <strong style="color:var(--accent);">Journal Entry</strong>: Dr. Cash / Cr. Accounts Receivable
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-reconcile-coll')">Cancel</button><button class="btn btn-primary" onclick="confirmCollect()">✓ Collect & Post</button></div>
  </div>
</div>

<!-- RECONCILE PAYMENT MODAL -->
<div class="overlay" id="ov-reconcile-pay">
  <div class="modal">
    <div class="mhdr"><div class="mtitle">Record Payment</div><div class="mclose" onclick="closeOverlay('ov-reconcile-pay')">✕</div></div>
    <div class="mbody">
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
        <div id="rp-invoice-info" style="font-size:14px;color:var(--text);font-weight:500;"></div>
      </div>
      <div class="fgrid">
        <div class="fg"><label>Payment Date</label><input type="date" id="rp-date"></div>
        <div class="fg"><label>Payment Method</label>
          <select id="rp-method"><option value="bank">🏦 Bank Transfer</option><option value="cash">💵 Cash</option><option value="card">💳 Card</option><option value="other">📋 Other</option></select>
        </div>
        <div class="fg full"><label>Amount to Pay (€)</label><input type="number" id="rp-amount" placeholder="0.00" step="0.01"></div>
        <div class="fg full"><label>Notes</label><input type="text" id="rp-notes" placeholder="Optional notes..."></div>
      </div>
      <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.06);border:1px solid rgba(200,255,0,.2);border-radius:7px;font-size:12px;color:var(--text3);">
        🔖 This will automatically create a <strong style="color:var(--accent);">Journal Entry</strong>: Dr. Accounts Payable / Cr. Cash
      </div>
    </div>
    <div class="mfoot"><button class="btn btn-ghost" onclick="closeOverlay('ov-reconcile-pay')">Cancel</button><button class="btn btn-primary" onclick="confirmPay()">✓ Pay & Post</button></div>
  </div>
</div>

<!-- ═══════════════════ CONTACT MODAL ═══════════════════ -->
<div class="overlay" id="ov-contact">
  <div class="modal" style="width:min(700px,95vw);">
    <div class="mhdr">
      <div>
        <div class="mtitle" id="ct-modal-title">New Contact</div>
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;margin-top:2px;">
          <div class="contact-type-toggle" style="margin-top:8px;">
            <button class="ct-btn active" id="ct-type-client"   onclick="setCtType('client')">Client</button>
            <button class="ct-btn"        id="ct-type-supplier" onclick="setCtType('supplier')">Supplier</button>
            <button class="ct-btn"        id="ct-type-both"     onclick="setCtType('both')">Both</button>
          </div>
        </div>
      </div>
      <div class="mclose" onclick="closeOverlay('ov-contact')">✕</div>
    </div>
    <div class="mbody">
      <!-- Contact tabs -->
      <div class="contact-tabs">
        <div class="contact-tab active" onclick="ctTab('basic')">📋 Basic</div>
        <div class="contact-tab" onclick="ctTab('accounts')">🏦 Accounts</div>
        <div class="contact-tab" onclick="ctTab('preferences')">⚙ Preferences</div>
        <div class="contact-tab" onclick="ctTab('accounting')">📊 Accounting</div>
      </div>

      <!-- BASIC -->
      <div class="contact-panel active" id="ctpanel-basic">
        <div class="fgrid">
          <div class="fg full"><label>Full Name / Company Name</label><input type="text" id="ct-name" placeholder="e.g. Balenciaga Spain SL."></div>
          <div class="fg"><label>NIF / VAT Number</label><input type="text" id="ct-nif" placeholder="e.g. B66408139"></div>
          <div class="fg"><label>Trade Name (optional)</label><input type="text" id="ct-tradename" placeholder="Trade name"></div>
          <div class="fg full"><label>Address</label><input type="text" id="ct-addr" placeholder="e.g. Paseo Gracia 56, Module B Floor 6"></div>
          <div class="fg"><label>City</label><input type="text" id="ct-city" placeholder="Barcelona"></div>
          <div class="fg"><label>Postal Code</label><input type="text" id="ct-postal" placeholder="08007"></div>
          <div class="fg"><label>Province / State</label><input type="text" id="ct-province" placeholder="Barcelona"></div>
          <div class="fg"><label>Country</label><input type="text" id="ct-country" placeholder="Spain"></div>
          <div class="fg"><label>Email</label><input type="email" id="ct-email" placeholder="invoices@company.com"></div>
          <div class="fg"><label>Phone</label><input type="text" id="ct-phone" placeholder="+34 932 956 184"></div>
          <div class="fg"><label>Mobile</label><input type="text" id="ct-mobile" placeholder="+34 616 519 247"></div>
          <div class="fg"><label>Website</label><input type="text" id="ct-web" placeholder="www.company.com"></div>
        </div>
      </div>

      <!-- ACCOUNTS -->
      <div class="contact-panel" id="ctpanel-accounts">
        <div class="fgrid">
          <div class="fg full"><label>IBAN</label><input type="text" id="ct-iban" placeholder="ES91 2100 0418 4502 0005 1332"></div>
          <div class="fg"><label>BIC / SWIFT</label><input type="text" id="ct-bic" placeholder="CAIXESBBXXX"></div>
          <div class="fg"><label>Bank Name</label><input type="text" id="ct-bank" placeholder="CaixaBank"></div>
          <div class="fg full"><label>Payment Terms</label>
            <select id="ct-payterms">
              <option value="immediate">Immediate</option>
              <option value="15days">15 days</option>
              <option value="30days" selected>30 days</option>
              <option value="45days">45 days</option>
              <option value="60days">60 days</option>
              <option value="90days">90 days</option>
            </select>
          </div>
          <div class="fg"><label>Credit Limit (€)</label><input type="number" id="ct-creditlimit" placeholder="0.00" step="0.01"></div>
          <div class="fg"><label>Currency</label>
            <select id="ct-currency">
              <option value="EUR" selected>EUR — Euro</option>
              <option value="USD">USD — US Dollar</option>
              <option value="GBP">GBP — British Pound</option>
              <option value="CHF">CHF — Swiss Franc</option>
            </select>
          </div>
        </div>
      </div>

      <!-- PREFERENCES -->
      <div class="contact-panel" id="ctpanel-preferences">
        <div class="fgrid">
          <div class="fg"><label>Default Sales VAT (%)</label>
            <select id="ct-salesvat">
              <option value="0">0%</option>
              <option value="4">4% (Reduced)</option>
              <option value="10">10% (Reduced)</option>
              <option value="21" selected>21% (General)</option>
            </select>
          </div>
          <div class="fg"><label>Default Purchase VAT (%)</label>
            <select id="ct-purchvat">
              <option value="0">0%</option>
              <option value="4">4% (Reduced)</option>
              <option value="10">10% (Reduced)</option>
              <option value="21" selected>21% (General)</option>
            </select>
          </div>
          <div class="fg"><label>Invoice Language</label>
            <select id="ct-lang">
              <option value="en">English</option>
              <option value="es">Español</option>
              <option value="fr">Français</option>
              <option value="de">Deutsch</option>
            </select>
          </div>
          <div class="fg"><label>Send Invoices By</label>
            <select id="ct-invoiceby">
              <option value="email">Email</option>
              <option value="post">Post</option>
              <option value="both">Email &amp; Post</option>
            </select>
          </div>
          <div class="fg full"><label>Notes / Tags</label><textarea id="ct-notes" placeholder="Internal notes about this contact..."></textarea></div>
        </div>
      </div>

      <!-- ACCOUNTING -->
      <div class="contact-panel" id="ctpanel-accounting">
        <div class="fgrid">
          <div class="fg full">
            <label>Client / Debtor Account</label>
            <select id="ct-debtacc">
              <option value="">— Select account —</option>
              <option value="43000001">43000001 — Clients (General)</option>
              <option value="43000002">43000002 — Clients (EU)</option>
              <option value="43000003">43000003 — Clients (Non-EU)</option>
              <option value="1100">1100 — Accounts Receivable</option>
            </select>
          </div>
          <div class="fg full">
            <label>Supplier / Creditor Account</label>
            <select id="ct-credacc">
              <option value="">— Select account —</option>
              <option value="41000001">41000001 — Suppliers (General)</option>
              <option value="41000002">41000002 — Suppliers (EU)</option>
              <option value="41000003">41000003 — Suppliers (Non-EU)</option>
              <option value="2000">2000 — Accounts Payable</option>
            </select>
          </div>
          <div class="fg"><label>Sales Tax Rate</label>
            <select id="ct-salestax">
              <option value="IVA21">IVA 21% (General)</option>
              <option value="IVA10">IVA 10% (Reduced)</option>
              <option value="IVA4">IVA 4% (Super-reduced)</option>
              <option value="IVA0">IVA 0% (Exempt)</option>
            </select>
          </div>
          <div class="fg"><label>Purchase Tax Rate</label>
            <select id="ct-purchtax">
              <option value="IVA21">IVA 21% (General)</option>
              <option value="IVA10">IVA 10% (Reduced)</option>
              <option value="IVA4">IVA 4% (Super-reduced)</option>
              <option value="IVA0">IVA 0% (Exempt)</option>
            </select>
          </div>
          <div class="fg full"><label>Custom Accounting Code (optional)</label><input type="text" id="ct-acccode" placeholder="e.g. 43000168"></div>
        </div>
        <div style="margin-top:14px;padding:10px 14px;background:rgba(200,255,0,.05);border:1px solid rgba(200,255,0,.15);border-radius:7px;font-size:12px;color:var(--text3);">
          💡 These accounting codes will be used automatically when generating Journal Entries for this contact.
        </div>
      </div>

    </div>
    <div class="mfoot">
      <button class="btn btn-danger btn-sm" id="ct-delete-btn" onclick="deleteContact()" style="margin-right:auto;display:none;">🗑 Delete</button>
      <button class="btn btn-ghost" onclick="closeOverlay('ov-contact')">Cancel</button>
      <button class="btn btn-primary" onclick="saveContact()">Save Contact</button>
    </div>
  </div>
</div>
</body>
</html>"""

# In-memory store (resets on server restart)
# For persistent data, add a PostgreSQL database on Railway
_store = {}
_lock  = threading.Lock()


class Handler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/load":
            self._load()
        elif self.path == "/health":
            self._text("ok")
        else:
            self._app()

    def do_POST(self):
        if self.path == "/save":
            self._save()
        elif self.path == "/export":
            self._export()
        else:
            self.send_response(404)
            self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self._cors()
        self.end_headers()

    # ── helpers ──────────────────────────────────────────────────────────────

    def _cors(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _app(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.send_header("Cache-Control", "no-cache")
        self._cors()
        self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))

    def _text(self, msg):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self._cors()
        self.end_headers()
        self.wfile.write(msg.encode())

    def _load(self):
        with _lock:
            data = _store.get("db")
        if data:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self._cors()
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        else:
            self.send_response(204)
            self._cors()
            self.end_headers()

    def _save(self):
        try:
            n    = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(n)
            data = json.loads(body)
            with _lock:
                _store["db"] = data
            self.send_response(200)
            self._cors()
            self.end_headers()
            self.wfile.write(b"ok")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def _export(self):
        try:
            n       = int(self.headers.get("Content-Length", 0))
            body    = self.rfile.read(n)
            payload = json.loads(body)
            fname   = payload.get("filename", "export.csv")
            content = payload.get("content", "")
            # Return the file as a browser download
            self.send_response(200)
            self.send_header("Content-Type", "text/csv; charset=utf-8")
            self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
            self._cors()
            self.end_headers()
            self.wfile.write(content.encode("utf-8-sig"))
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(str(e).encode())

    def log_message(self, fmt, *args):
        if args:
            print(f"[{self.client_address[0]}] {args[0]}")


def main():
    socketserver.TCPServer.allow_reuse_address = True
    print(f"\n  FinLedger ready on port {PORT}")
    print(f"  Open: http://localhost:{PORT}\n")
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as srv:
        srv.serve_forever()


if __name__ == "__main__":
    main()
