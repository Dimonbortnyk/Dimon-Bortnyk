#!/usr/bin/env python3
"""FinLedger — Railway + Supabase auth deployment."""
import http.server, socketserver, os
import json as _json

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
.theme-toggle-label{font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;}
*{margin:0;padding:0;box-sizing:border-box;}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;font-size:14px;min-height:100vh;display:flex;overflow:hidden;}

/* ── SIDEBAR ── */
.sidebar{width:232px;min-width:232px;background:var(--surface);border-right:1px solid var(--border);display:flex;flex-direction:column;padding:0;}
.logo-area{padding:22px 20px 18px;border-bottom:1px solid var(--border);}
.logo-title{font-family:'DM Serif Display',serif;font-size:22px;color:var(--accent);letter-spacing:-.5px;}
.logo-sub{font-size:9px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:2px;margin-top:2px;}
.nav{padding:16px 0;flex:1;overflow-y:auto;}
.nav-sec{font-size:9px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:2px;padding:10px 20px 5px;}
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
.user-role{font-size:10px;color:var(--text3);font-family:monospace;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-co{font-size:10px;color:var(--text3);margin-top:1px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.user-gear{color:var(--text3);font-size:13px;flex-shrink:0;}

/* ── MAIN ── */
.main{flex:1;display:flex;flex-direction:column;overflow:hidden;}
.topbar{background:var(--surface);border-bottom:1px solid var(--border);padding:0 28px;height:56px;display:flex;align-items:center;justify-content:space-between;gap:16px;}
.topbar-left{}
.page-title{font-family:'DM Serif Display',serif;font-size:20px;}
.breadcrumb{font-size:11px;color:var(--text3);font-family:monospace;}
.topbar-right{display:flex;align-items:center;gap:10px;}
.greeting{font-size:13px;color:var(--text2);}
.greeting strong{color:var(--text);font-weight:600;}
.server-badge{background:rgba(200,255,0,.1);border:1px solid rgba(200,255,0,.3);color:var(--accent);padding:4px 12px;border-radius:20px;font-size:11px;font-family:monospace;}

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
.card-title{font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:8px;}
.card-value{font-family:'DM Serif Display',serif;font-size:28px;}
.card-delta{font-size:12px;margin-top:4px;color:var(--text3);}
.card{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}

/* ── TABLES ── */
.tbl-wrap{overflow-x:auto;}
table{width:100%;border-collapse:collapse;}
th{padding:10px 14px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.2px;border-bottom:1px solid var(--border);white-space:nowrap;}
td{padding:11px 14px;border-bottom:1px solid rgba(46,46,56,.5);font-size:13px;color:var(--text2);}
tr:last-child td{border-bottom:none;}
tr:hover td{background:var(--surface2);color:var(--text);}
.amt{font-family:monospace;text-align:right;}
.pos{color:var(--green)!important;}
.neg{color:var(--red)!important;}

/* ── BADGES ── */
.badge{display:inline-flex;align-items:center;padding:2px 9px;border-radius:20px;font-size:10px;font-weight:600;font-family:monospace;text-transform:uppercase;}
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
label{font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;}
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
.sec-sub{font-size:11px;color:var(--text3);font-family:monospace;}
.tabs{display:flex;gap:2px;background:var(--surface2);border-radius:8px;padding:3px;width:fit-content;margin-bottom:20px;}
.tab{padding:7px 18px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:500;color:var(--text2);transition:all .15s;}
.tab.active{background:var(--surface3);color:var(--text);}
.totbar{display:flex;gap:24px;padding:14px 20px;background:var(--surface2);border-radius:8px;border:1px solid var(--border);margin-bottom:16px;flex-wrap:wrap;}
.tot-item label{display:block;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
.tot-item span{font-family:'DM Serif Display',serif;font-size:18px;}

/* ── CHART ── */
.chart-area{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:20px;}
.chart-bars{display:flex;align-items:flex-end;gap:8px;height:160px;}
.bar-wrap{flex:1;display:flex;flex-direction:column;align-items:center;gap:6px;height:100%;justify-content:flex-end;}
.bar{width:100%;border-radius:4px 4px 0 0;min-height:4px;transition:all .3s;}
.bar:hover{filter:brightness(1.2);}
.bar-lbl{font-size:9px;color:var(--text3);font-family:monospace;}

/* ── REPORT TABLES ── */
.rtbl{width:100%;border-collapse:collapse;}
.rtbl tr.rh td{background:var(--surface2);color:var(--text);font-weight:600;font-size:12px;font-family:monospace;text-transform:uppercase;letter-spacing:1px;padding:8px 14px;}
.rtbl tr.rd td{padding:8px 14px;color:var(--text2);font-size:13px;border-bottom:1px solid rgba(46,46,56,.4);}
.rtbl tr.rd:hover td{background:rgba(255,255,255,.02);}
.rtbl tr.rs td{padding:9px 14px;font-weight:600;color:var(--text);border-top:1px solid var(--border);}
.rtbl tr.rt td{padding:11px 14px;font-family:'DM Serif Display',serif;font-size:16px;color:var(--accent);border-top:2px solid var(--accent);background:rgba(200,255,0,.04);}
.rtbl .ind{padding-left:30px!important;}
.rtbl .num{font-family:monospace;text-align:right;}

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
.set-section-label{font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;margin-top:4px;}

/* ── INFO ROW ── */
.info-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid rgba(46,46,56,.5);}
.info-row:last-child{border-bottom:none;}
.info-label{font-size:12px;color:var(--text3);}
.info-val{font-size:13px;color:var(--text);font-family:monospace;}

/* ── EXPORT ICON BUTTONS ── */
.btn-xls{background:rgba(74,222,128,.12);color:#4ade80;border:1px solid rgba(74,222,128,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-xls:hover{background:rgba(74,222,128,.28);transform:translateY(-1px);}
.btn-pdf2{background:rgba(248,113,113,.12);color:#f87171;border:1px solid rgba(248,113,113,.3);padding:6px 10px;border-radius:7px;font-size:15px;cursor:pointer;transition:all .15s;line-height:1;}
.btn-pdf2:hover{background:rgba(248,113,113,.28);transform:translateY(-1px);}
/* asset type badge */
.inv-type-badge{display:inline-flex;align-items:center;gap:5px;padding:3px 10px;border-radius:10px;font-size:10px;font-weight:700;font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;}
.inv-type-expense{background:rgba(251,146,60,.12);color:var(--yellow);border:1px solid rgba(251,146,60,.3);}
.inv-type-asset{background:rgba(99,102,241,.15);color:#818cf8;border:1px solid rgba(99,102,241,.3);}
.depr-plan-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:10px;}
.depr-plan-card:hover{border-color:var(--accent);}
.depr-schedule-row{display:flex;align-items:center;justify-content:space-between;padding:5px 0;border-bottom:1px solid var(--border);font-size:12px;}
.depr-schedule-row:last-child{border-bottom:none;}
/* recurring side panel */
.rc-layout{display:flex;gap:0;height:100%;}
.rc-list-col{flex:1;min-width:0;overflow:auto;}
.rc-panel{width:340px;flex-shrink:0;background:var(--surface);border-left:1px solid var(--border);display:none;flex-direction:column;overflow-y:auto;position:sticky;top:0;max-height:calc(100vh - 200px);}
.rc-panel.open{display:flex;}
.rc-panel-hdr{padding:16px 18px 12px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;}
.rc-panel-title{font-size:14px;font-weight:700;color:var(--text);}
.rc-panel-body{padding:16px 18px;flex:1;}
.rc-panel-section{font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin:14px 0 6px;}
.rc-field{margin-bottom:12px;}
.rc-field label{display:block;font-size:11px;color:var(--text3);margin-bottom:4px;text-transform:uppercase;letter-spacing:.5px;}
.rc-field input,.rc-field select{width:100%;padding:7px 10px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:13px;}
.rc-field input:focus,.rc-field select:focus{border-color:var(--accent);}
/* toggle switch */
.rc-toggle-row{display:flex;align-items:center;justify-content:space-between;padding:10px 0;border-bottom:1px solid var(--border);}
.rc-toggle-row:last-child{border-bottom:none;}
.rc-toggle-label{font-size:13px;color:var(--text2);}
.rc-toggle-sub{font-size:11px;color:var(--text3);margin-top:2px;}
.toggle-sw{position:relative;width:44px;height:24px;flex-shrink:0;}
.toggle-sw input{opacity:0;width:0;height:0;}
.toggle-sw-track{position:absolute;inset:0;background:var(--surface3);border-radius:12px;cursor:pointer;transition:background .2s;}
.toggle-sw input:checked+.toggle-sw-track{background:var(--accent);}
.toggle-sw-thumb{position:absolute;width:18px;height:18px;background:#fff;border-radius:50%;top:3px;left:3px;transition:transform .2s;box-shadow:0 1px 3px rgba(0,0,0,.3);}
.toggle-sw input:checked+.toggle-sw-track .toggle-sw-thumb{transform:translateX(20px);}
/* cascade timeline */
.rc-cascade{margin-top:8px;}
.rc-cascade-item{display:flex;align-items:center;gap:10px;padding:8px 0;border-bottom:1px solid var(--border);}
.rc-cascade-item:last-child{border-bottom:none;}
.rc-month-pill{width:56px;text-align:center;flex-shrink:0;}
.rc-month-pill .month{font-size:11px;font-weight:700;color:var(--text);text-transform:uppercase;}
.rc-month-pill .year{font-size:10px;color:var(--text3);}
.rc-cascade-qty{width:20px;text-align:center;font-size:12px;color:var(--text3);}
.rc-cascade-amt{flex:1;font-size:13px;font-weight:600;color:var(--text);}
.rc-cascade-badge{font-size:10px;font-weight:700;padding:3px 8px;border-radius:10px;text-transform:uppercase;letter-spacing:.5px;}
.rc-cascade-badge.converted{background:rgba(74,222,128,.15);color:var(--green);border:1px solid rgba(74,222,128,.3);}
.rc-cascade-badge.pending{background:rgba(251,191,36,.12);color:var(--yellow);border:1px solid rgba(251,191,36,.3);}
.rc-cascade-inv{font-size:10px;color:var(--accent);font-family:monospace;cursor:pointer;text-decoration:underline dotted;}
/* 3-dot context menu */
.rc-dots-btn{background:none;border:none;cursor:pointer;padding:4px 8px;border-radius:6px;color:var(--text3);font-size:18px;line-height:1;transition:all .15s;}
.rc-dots-btn:hover{background:var(--surface2);color:var(--text);}
.rc-ctx-menu{position:absolute;right:8px;top:100%;background:var(--surface);border:1px solid var(--border);border-radius:10px;min-width:160px;z-index:500;box-shadow:0 4px 24px rgba(0,0,0,.3);padding:4px;display:none;}
.rc-ctx-menu.open{display:block;}
.rc-ctx-item{padding:9px 14px;cursor:pointer;font-size:13px;color:var(--text2);border-radius:7px;display:flex;align-items:center;gap:9px;transition:background .12s;}
.rc-ctx-item:hover{background:var(--surface2);color:var(--text);}
.rc-ctx-item.danger{color:var(--red);}
.rc-ctx-item.danger:hover{background:rgba(248,113,113,.08);}
/* import / export */
.import-zone{border:2px dashed var(--border);border-radius:12px;padding:32px;text-align:center;transition:all .2s;cursor:pointer;background:var(--surface2);}
.import-zone:hover,.import-zone.drag-over{border-color:var(--accent);background:rgba(200,255,0,.04);}
.import-zone-icon{font-size:36px;margin-bottom:8px;}
.import-zone-title{font-size:15px;font-weight:600;color:var(--text);margin-bottom:4px;}
.import-zone-sub{font-size:12px;color:var(--text3);}
.import-preview{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-top:14px;max-height:280px;overflow-y:auto;}
.import-preview table{width:100%;border-collapse:collapse;font-size:11px;}
.import-preview th{background:var(--surface3);padding:5px 8px;text-align:left;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:.5px;position:sticky;top:0;}
.import-preview td{padding:5px 8px;border-bottom:1px solid var(--border);color:var(--text2);}
.import-preview tr:last-child td{border-bottom:none;}
.import-result{padding:10px 14px;border-radius:8px;font-size:12px;margin-top:10px;font-weight:500;}
.import-result.ok{background:rgba(74,222,128,.12);color:var(--green);border:1px solid rgba(74,222,128,.3);}
.import-result.warn{background:rgba(251,191,36,.12);color:var(--yellow);border:1px solid rgba(251,191,36,.3);}
.import-result.err{background:rgba(248,113,113,.12);color:var(--red);border:1px solid rgba(248,113,113,.3);}
.export-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:10px;margin-top:12px;}
.export-btn-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:14px 10px;text-align:center;cursor:pointer;transition:all .15s;}
.export-btn-card:hover{border-color:var(--accent);background:var(--surface3);}
.export-btn-card .ebc-icon{font-size:24px;margin-bottom:6px;}
.export-btn-card .ebc-label{font-size:11px;font-weight:600;color:var(--text2);}
.export-btn-card .ebc-fmt{font-size:10px;color:var(--text3);font-family:monospace;margin-top:2px;}
.template-btn{display:inline-flex;align-items:center;gap:6px;padding:7px 14px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;cursor:pointer;font-size:12px;color:var(--text2);transition:all .15s;}
.template-btn:hover{border-color:var(--accent);color:var(--accent);}
/* drill-down from P&L / BS */
.drilldown-link{cursor:pointer;text-decoration:underline dotted;text-underline-offset:3px;transition:color .15s;}
.drilldown-link:hover{color:var(--accent)!important;}
.je-filter-bar{display:flex;align-items:center;gap:10px;padding:10px 14px;background:var(--surface2);border:1px solid var(--accent);border-radius:8px;margin-bottom:14px;flex-wrap:wrap;}
.je-filter-bar .filter-label{font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;}
.je-filter-bar .filter-val{font-size:13px;color:var(--accent);font-weight:700;}
/* journal ledger rows */
.je-header-row td{background:var(--surface2);border-top:2px solid var(--border);}
.je-header-row:first-child td{border-top:none;}
.je-line-row td{background:var(--surface);border-bottom:1px solid rgba(46,46,56,.3);}
.je-line-row:last-of-type td{border-bottom:2px solid var(--border);}
.je-line-row:hover td{background:var(--surface2);}
.je-acc-code{font-family:monospace;font-size:11px;color:var(--text3);padding:2px 6px;background:var(--surface3);border-radius:4px;display:inline-block;}
.je-dr{color:var(--green);font-family:monospace;font-size:12px;font-weight:600;}
.je-cr{color:var(--red);font-family:monospace;font-size:12px;font-weight:600;}
.je-acc-name{font-size:13px;color:var(--text2);padding-left:20px;}
/* numbering series */
.series-card{background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px 16px;display:flex;align-items:center;gap:12px;margin-bottom:8px;transition:border-color .15s;}
.series-card:hover{border-color:var(--accent);}
.series-code{font-family:monospace;font-size:13px;font-weight:700;color:var(--accent);min-width:60px;}
.series-info{flex:1;}
.series-name{font-size:13px;font-weight:600;color:var(--text);}
.series-format{font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;}
.series-actions{display:flex;gap:6px;align-items:center;}
.series-lastnum{font-size:11px;color:var(--text3);font-family:monospace;text-align:right;}
/* sales/purchases view tabs */
.view-tabs{display:flex;gap:4px;padding:0 0 16px 0;}
.view-tab{padding:8px 20px;border-radius:8px 8px 0 0;cursor:pointer;font-size:13px;font-weight:600;color:var(--text2);border:1px solid transparent;border-bottom:none;transition:all .15s;background:var(--surface2);}
.view-tab:hover{color:var(--text);}
.view-tab.active{background:var(--surface);color:var(--accent);border-color:var(--border);position:relative;top:1px;}
.recur-badge{display:inline-flex;align-items:center;gap:4px;padding:3px 10px;border-radius:12px;font-size:10px;font-weight:700;font-family:monospace;letter-spacing:.5px;text-transform:uppercase;}
.recur-badge.active{background:rgba(74,222,128,.15);color:var(--green);border:1px solid rgba(74,222,128,.3);}
.recur-badge.paused{background:rgba(251,146,60,.15);color:var(--yellow);border:1px solid rgba(251,146,60,.3);}
.recur-badge.ended{background:rgba(144,144,168,.15);color:var(--text3);border:1px solid var(--border);}
/* invoice preview */
.inv-modal{background:var(--surface);border:1px solid var(--border);border-radius:14px;width:min(860px,96vw);max-height:95vh;overflow-y:auto;box-shadow:0 8px 50px rgba(0,0,0,.6);display:flex;flex-direction:column;}
.inv-modal::-webkit-scrollbar{width:4px;}
.inv-modal::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px;}
.inv-toolbar{padding:14px 20px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:10px;background:var(--surface);border-radius:14px 14px 0 0;}
.inv-toolbar-left{display:flex;align-items:center;gap:10px;}
.inv-toolbar-right{display:flex;align-items:center;gap:8px;}
/* Invoice paper */
.inv-paper{background:#ffffff;color:#1a1a2e;margin:20px;border-radius:8px;padding:48px 52px;font-family:'DM Sans',sans-serif;box-shadow:0 2px 20px rgba(0,0,0,.15);min-height:900px;position:relative;}
.inv-paper *{box-sizing:border-box;}
.inv-header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:40px;}
.inv-logo-area{flex:1;}
.inv-company-name{font-family:'DM Serif Display',serif;font-size:26px;color:#0f0f11;letter-spacing:-.5px;margin-bottom:4px;}
.inv-company-details{font-size:12px;color:#555;line-height:1.6;}
.inv-title-area{text-align:right;}
.inv-title{font-family:'DM Serif Display',serif;font-size:36px;color:#0f0f11;letter-spacing:-1px;text-transform:uppercase;}
.inv-num{font-size:14px;color:#666;margin-top:4px;font-family:monospace;}
.inv-meta-row{display:flex;justify-content:space-between;margin-bottom:36px;gap:24px;}
.inv-bill-to{flex:1;}
.inv-bill-label{font-size:10px;text-transform:uppercase;letter-spacing:2px;color:#999;font-family:monospace;margin-bottom:8px;}
.inv-bill-name{font-size:16px;font-weight:700;color:#0f0f11;margin-bottom:4px;}
.inv-bill-detail{font-size:12px;color:#555;line-height:1.5;}
.inv-dates{text-align:right;}
.inv-date-row{display:flex;justify-content:flex-end;gap:16px;margin-bottom:6px;font-size:13px;}
.inv-date-label{color:#999;font-family:monospace;font-size:11px;text-transform:uppercase;letter-spacing:1px;}
.inv-date-val{color:#0f0f11;font-weight:600;}
.inv-table{width:100%;border-collapse:collapse;margin-bottom:32px;}
.inv-table thead tr{background:#0f0f11;color:#fff;}
.inv-table thead th{padding:12px 16px;text-align:left;font-size:11px;font-family:monospace;text-transform:uppercase;letter-spacing:1px;font-weight:500;}
.inv-table thead th:last-child{text-align:right;}
.inv-table tbody tr{border-bottom:1px solid #f0f0f0;}
.inv-table tbody tr:last-child{border-bottom:none;}
.inv-table tbody td{padding:14px 16px;font-size:13px;color:#333;vertical-align:top;}
.inv-table tbody td:last-child{text-align:right;font-weight:600;color:#0f0f11;}
.inv-table tfoot tr{border-top:2px solid #e8e8e8;}
.inv-table tfoot td{padding:10px 16px;font-size:13px;}
.inv-table tfoot td:last-child{text-align:right;font-weight:700;}
.inv-total-row td{font-size:16px!important;font-weight:800!important;color:#0f0f11!important;padding-top:14px!important;border-top:2px solid #0f0f11!important;}
.inv-summary{display:flex;justify-content:flex-end;margin-bottom:36px;}
.inv-summary-box{min-width:280px;}
.inv-summary-line{display:flex;justify-content:space-between;padding:8px 0;font-size:13px;border-bottom:1px solid #f0f0f0;}
.inv-summary-line:last-child{border-bottom:none;font-size:16px;font-weight:800;padding-top:12px;color:#0f0f11;}
.inv-summary-label{color:#666;}
.inv-summary-val{font-weight:600;color:#0f0f11;}
.inv-footer{border-top:1px solid #e8e8e8;padding-top:20px;margin-top:auto;}
.inv-footer-notes{font-size:12px;color:#666;line-height:1.6;margin-bottom:12px;}
.inv-footer-status{display:inline-flex;align-items:center;gap:6px;padding:6px 16px;border-radius:20px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:1px;font-family:monospace;}
.inv-footer-status.paid{background:#dcfce7;color:#16a34a;}
.inv-footer-status.pending{background:#fef9c3;color:#ca8a04;}
.inv-footer-status.partial{background:#dbeafe;color:#2563eb;}
.inv-accent-bar{position:absolute;top:0;left:0;right:0;height:5px;background:#0f0f11;border-radius:8px 8px 0 0;}
@media print{
  body *{visibility:hidden!important;}
  .inv-paper,.inv-paper *{visibility:visible!important;}
  .inv-paper{position:fixed!important;top:0!important;left:0!important;right:0!important;margin:0!important;border-radius:0!important;box-shadow:none!important;padding:32px 40px!important;}
  .inv-accent-bar{display:none!important;}
}
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
.contact-meta{font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;}
.contact-badge{margin-left:auto;flex-shrink:0;}
.contacts-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:12px;}
/* autocomplete dropdown */
.autocomplete-wrap{position:relative;}
.autocomplete-list{position:absolute;top:100%;left:0;right:0;background:var(--surface);border:1px solid var(--accent);border-top:none;border-radius:0 0 7px 7px;z-index:200;max-height:200px;overflow-y:auto;display:none;}
.autocomplete-list.open{display:block;}
.autocomplete-item{padding:9px 12px;cursor:pointer;font-size:13px;color:var(--text2);border-bottom:1px solid rgba(46,46,56,.4);}
.autocomplete-item:hover{background:var(--surface2);color:var(--text);}
.autocomplete-item:last-child{border-bottom:none;}
.autocomplete-item .ac-meta{font-size:10px;color:var(--text3);font-family:monospace;margin-top:1px;}
/* ── TESORERÍA NAV GROUP ── */
.nav-group-toggle{cursor:pointer;user-select:none;}
.nav-group-toggle:hover{color:var(--text);background:var(--surface2);}
.nav-subitem{padding:7px 14px 7px 10px !important;font-size:12px !important;}
.nav-subitem.active{color:var(--accent);border-left-color:var(--accent);background:rgba(200,255,0,.06);}

/* ── WIRE TRANSFERS OVERLAY ── */
.wt-overlay{position:fixed;inset:0;background:rgba(0,0,0,.78);z-index:200;display:none;align-items:flex-start;justify-content:center;padding-top:40px;backdrop-filter:blur(6px);}
.wt-overlay.open{display:flex;}
.wt-modal{background:var(--surface);border:1px solid var(--border);border-radius:16px;width:min(1100px,97vw);max-height:88vh;display:flex;flex-direction:column;box-shadow:0 12px 60px rgba(0,0,0,.6);}
.wt-header{padding:18px 24px;border-bottom:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;flex-shrink:0;}
.wt-title{font-family:'DM Serif Display',serif;font-size:20px;display:flex;align-items:center;gap:10px;}
.wt-tabs{display:flex;gap:0;background:var(--surface2);border-radius:8px;padding:3px;margin:0 24px 0 0;}
.wt-tab{padding:7px 20px;border-radius:6px;cursor:pointer;font-size:13px;font-weight:600;color:var(--text2);transition:all .15s;}
.wt-tab.active{background:var(--surface3);color:var(--text);}
.wt-body{display:flex;flex:1;overflow:hidden;}
.wt-list{flex:1;overflow-y:auto;padding:20px 24px;}
.wt-list::-webkit-scrollbar{width:5px;}
.wt-list::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
.wt-sidebar{width:300px;flex-shrink:0;background:var(--surface2);border-left:1px solid var(--border);padding:22px 20px;overflow-y:auto;display:flex;flex-direction:column;gap:14px;}
.wt-field label{display:block;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:5px;}
.wt-field input,.wt-field select{width:100%;padding:8px 10px;background:var(--surface3);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:13px;font-family:'DM Sans',sans-serif;}
.wt-field input:focus,.wt-field select:focus{border-color:var(--accent);outline:none;}
.wt-total-box{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:14px;text-align:center;}
.wt-total-label{font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;}
.wt-total-val{font-family:'DM Serif Display',serif;font-size:30px;color:var(--accent);}
.wt-history-row{display:flex;align-items:center;justify-content:space-between;padding:10px 14px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;margin-bottom:8px;cursor:pointer;transition:border-color .15s;}
.wt-history-row:hover{border-color:var(--accent);}
.wt-badge-out{background:rgba(248,113,113,.12);color:var(--red);border:1px solid rgba(248,113,113,.3);padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;font-family:monospace;}
.wt-badge-in{background:rgba(74,222,128,.12);color:var(--green);border:1px solid rgba(74,222,128,.3);padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;font-family:monospace;}
.wt-badge-pend{background:rgba(255,217,61,.12);color:var(--yellow);border:1px solid rgba(255,217,61,.3);padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;font-family:monospace;}

/* ── BANK ACCOUNTS MODULE ────────────────────────────────────── */
.ba-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:16px;margin-top:20px;}
.ba-card{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px 22px;position:relative;cursor:pointer;transition:all .15s;}
.ba-card:hover{border-color:var(--accent);transform:translateY(-2px);box-shadow:0 6px 24px rgba(0,0,0,.2);}
.ba-card-header{display:flex;align-items:center;gap:12px;margin-bottom:14px;}
.ba-bank-icon{width:42px;height:42px;border-radius:10px;background:var(--surface2);border:1px solid var(--border);display:flex;align-items:center;justify-content:center;font-size:20px;flex-shrink:0;}
.ba-bank-name{font-weight:700;font-size:14px;color:var(--text);}
.ba-bank-iban{font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;}
.ba-balance{font-family:'DM Serif Display',serif;font-size:26px;color:var(--text);margin-bottom:4px;}
.ba-balance.neg{color:var(--red);}
.ba-stats{display:flex;gap:16px;margin-top:10px;padding-top:10px;border-top:1px solid var(--border);}
.ba-stat label{display:block;font-size:9px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;}
.ba-stat span{font-size:12px;font-weight:600;font-family:monospace;}
.ba-card-actions{position:absolute;top:14px;right:14px;display:flex;gap:6px;opacity:0;transition:opacity .15s;}
.ba-card:hover .ba-card-actions{opacity:1;}
.ba-action-btn{width:28px;height:28px;border-radius:7px;background:var(--surface2);border:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center;font-size:13px;color:var(--text3);transition:all .15s;}
.ba-action-btn:hover{color:var(--text);border-color:var(--accent);}
.ba-add-card{background:transparent;border:2px dashed var(--border);border-radius:14px;padding:20px 22px;cursor:pointer;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:10px;min-height:140px;transition:all .15s;color:var(--text3);}
.ba-add-card:hover{border-color:var(--accent);color:var(--accent);background:rgba(200,255,0,.03);}
.ba-add-icon{font-size:28px;}
.ba-add-label{font-size:13px;font-weight:600;}
.ba-chart-wrap{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px 24px;margin-bottom:20px;}
.ba-chart-header{display:flex;align-items:center;justify-content:space-between;margin-bottom:20px;}
.ba-chart-kpis{display:flex;gap:32px;}
.ba-kpi-item label{display:block;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:3px;}
.ba-kpi-item span{font-family:'DM Serif Display',serif;font-size:22px;}
.ba-mov-row{display:flex;align-items:center;padding:12px 14px;border-bottom:1px solid rgba(46,46,56,.4);gap:12px;cursor:pointer;transition:background .12s;}
.ba-mov-row:hover{background:var(--surface2);}
.ba-mov-row:last-child{border-bottom:none;}
.ba-mov-sign{width:34px;height:34px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:14px;flex-shrink:0;}
.ba-mov-sign.in{background:rgba(74,222,128,.12);color:var(--green);}
.ba-mov-sign.out{background:rgba(248,113,113,.12);color:var(--red);}
.ba-mov-desc{flex:1;min-width:0;}
.ba-mov-concept{font-size:13px;font-weight:500;color:var(--text);white-space:nowrap;overflow:hidden;text-overflow:ellipsis;}
.ba-mov-date{font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;}
.ba-mov-amount{font-family:monospace;font-size:14px;font-weight:700;flex-shrink:0;}
.ba-mov-amount.pos{color:var(--green);}
.ba-mov-amount.neg{color:var(--red);}
.ba-reconcile-badge{display:inline-flex;align-items:center;gap:4px;padding:2px 8px;border-radius:10px;font-size:10px;font-weight:700;font-family:monospace;}
.ba-reconcile-badge.done{background:rgba(74,222,128,.12);color:var(--green);border:1px solid rgba(74,222,128,.3);}
.ba-reconcile-badge.pending{background:rgba(255,217,61,.1);color:var(--yellow);border:1px solid rgba(255,217,61,.3);}
.ba-import-zone{border:2px dashed var(--border);border-radius:12px;padding:32px;text-align:center;transition:all .2s;cursor:pointer;background:var(--surface2);}
.ba-import-zone:hover,.ba-import-zone.drag-over{border-color:var(--accent);background:rgba(200,255,0,.04);}
.ba-import-zone-icon{font-size:36px;margin-bottom:8px;}
.ba-import-zone-title{font-size:14px;font-weight:600;color:var(--text);margin-bottom:4px;}
.ba-import-zone-sub{font-size:12px;color:var(--text3);}
/* ── CFO MODULE ─────────────────────────────────────────── */
.cfo-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-bottom:24px;}
.cfo-grid-2{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-bottom:24px;}
.cfo-grid-3{display:grid;grid-template-columns:2fr 1fr;gap:20px;margin-bottom:24px;}
.cfo-kpi{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:20px 22px;position:relative;overflow:hidden;transition:transform .15s,box-shadow .15s;}
.cfo-kpi:hover{transform:translateY(-2px);box-shadow:0 8px 32px rgba(0,0,0,.25);}
.cfo-kpi-accent{position:absolute;top:0;left:0;right:0;height:3px;}
.cfo-kpi-label{font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;}
.cfo-kpi-value{font-size:32px;font-weight:800;color:var(--text);line-height:1;margin-bottom:6px;}
.cfo-kpi-sub{font-size:12px;color:var(--text3);}
.cfo-kpi-badge{display:inline-flex;align-items:center;gap:4px;padding:3px 9px;border-radius:10px;font-size:11px;font-weight:600;margin-top:8px;}
.cfo-kpi-badge.up{background:rgba(74,222,128,.12);color:var(--green);}
.cfo-kpi-badge.down{background:rgba(248,113,113,.12);color:var(--red);}
.cfo-kpi-badge.neu{background:rgba(148,163,184,.12);color:var(--text3);}
.cfo-panel{background:var(--surface);border:1px solid var(--border);border-radius:14px;padding:22px 24px;}
.cfo-panel-title{font-size:13px;font-weight:700;color:var(--text);margin-bottom:4px;display:flex;align-items:center;gap:8px;}
.cfo-panel-sub{font-size:11px;color:var(--text3);margin-bottom:18px;}
.cfo-chart-wrap{position:relative;width:100%;overflow:hidden;}
/* Cohort table */
.cohort-tbl{width:100%;border-collapse:collapse;font-size:12px;}
.cohort-tbl th{padding:8px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;border-bottom:1px solid var(--border);}
.cohort-tbl td{padding:9px 12px;border-bottom:1px solid rgba(46,46,56,.3);color:var(--text2);}
.cohort-tbl tr:last-child td{border-bottom:none;}
.cohort-tbl tr:hover td{background:var(--surface2);}
.cohort-dot{width:8px;height:8px;border-radius:50%;display:inline-block;margin-right:6px;}
/* Ratio cards */
.ratio-grid{display:grid;grid-template-columns:1fr 1fr;gap:12px;}
.ratio-card{background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:14px 16px;}
.ratio-name{font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:.5px;margin-bottom:6px;}
.ratio-val{font-size:24px;font-weight:800;margin-bottom:4px;}
.ratio-formula{font-size:10px;color:var(--text3);font-style:italic;}
.ratio-status{display:inline-flex;align-items:center;gap:4px;font-size:10px;font-weight:600;padding:2px 7px;border-radius:6px;margin-top:6px;}
/* SVG bar chart */
.bar-chart-svg{width:100%;overflow:visible;}
/* period quick selector */
.period-bar{display:flex;align-items:center;gap:8px;margin-bottom:10px;flex-wrap:wrap;}
.period-select{padding:7px 12px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;color:var(--text);font-size:13px;font-family:'DM Sans',sans-serif;cursor:pointer;min-width:140px;}
.period-select:focus{border-color:var(--accent);outline:none;}
.period-nav{display:flex;gap:4px;}
.period-nav-btn{width:28px;height:28px;background:var(--surface2);border:1px solid var(--border);border-radius:6px;cursor:pointer;color:var(--text2);font-size:14px;display:flex;align-items:center;justify-content:center;transition:all .15s;}
.period-nav-btn:hover{border-color:var(--accent);color:var(--accent);}
.period-label{font-size:13px;font-weight:600;color:var(--text);min-width:120px;text-align:center;}
/* date filter bar */
.date-filter-bar{display:flex;align-items:center;gap:10px;padding:12px 16px;background:var(--surface2);border:1px solid var(--border);border-radius:8px;margin-bottom:16px;flex-wrap:wrap;}
.date-filter-bar label{font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin:0;}
.date-filter-bar input{width:140px;padding:6px 10px;font-size:12px;background:var(--surface3);border:1px solid var(--border);border-radius:6px;color:var(--text);}
.date-filter-bar input:focus{border-color:var(--accent);}
.filter-active-badge{background:rgba(200,255,0,.15);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:3px 10px;border-radius:20px;font-size:10px;font-family:monospace;font-weight:600;}
/* reconcile button */
.btn-reconcile{background:rgba(200,255,0,.12);color:var(--accent);border:1px solid rgba(200,255,0,.3);padding:5px 12px;border-radius:6px;font-size:11px;font-weight:700;cursor:pointer;font-family:monospace;text-transform:uppercase;letter-spacing:.5px;transition:all .15s;}
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
    <!-- TESORERÍA GROUP -->
    <div class="nav-item nav-group-toggle" id="nav-tesoreria" onclick="toggleTesoreriaNav()" style="justify-content:space-between;">
      <div style="display:flex;align-items:center;gap:10px;"><span class="nav-icon">🏦</span><span>Treasury</span></div>
      <span id="nav-tesoreria-arrow" style="font-size:10px;color:var(--text3);transition:transform .2s;">▶</span>
    </div>
    <div id="nav-tesoreria-sub" style="display:none;padding-left:14px;">
      <div class="nav-item nav-subitem" onclick="navTesoreria('bankaccounts')"><span class="nav-icon" style="font-size:11px;">🏛</span>Bank Accounts</div>
      <div class="nav-item nav-subitem" onclick="navTesoreria('collections')"><span class="nav-icon" style="font-size:11px;">◎</span>Collections</div>
      <div class="nav-item nav-subitem" onclick="navTesoreria('payments')"><span class="nav-icon" style="font-size:11px;">◉</span>Payments</div>
      <div class="nav-item nav-subitem" onclick="openWireTransfers()"><span class="nav-icon" style="font-size:11px;">⇄</span>Wire Transfers</div>
    </div>
    <div class="nav-item" onclick="nav('journal')"><span class="nav-icon">≡</span>Journal Entries</div>

    <div class="nav-sec">Reports</div>
    <div class="nav-item" onclick="nav('pl')"><span class="nav-icon">◈</span>P&amp;L Statement</div>
    <div class="nav-item" onclick="nav('bs')"><span class="nav-icon">⊞</span>Balance Sheet</div>
    <div class="nav-item" onclick="nav('cf')"><span class="nav-icon">⟳</span>Cash Flow</div>
    <div class="nav-item" onclick="nav('cfo')" style="margin-top:8px;background:linear-gradient(135deg,rgba(200,255,0,.1),rgba(14,154,167,.1));border:1px solid rgba(200,255,0,.2);border-radius:8px;"><span class="nav-icon">★</span><span style="font-weight:700;background:linear-gradient(90deg,var(--accent),var(--teal,#0E9AA7));-webkit-background-clip:text;-webkit-text-fill-color:transparent;">CFO Module</span></div>
  </div>

  <!-- USER CARD -->
  <div class="sidebar-foot">
    <div style="position:relative;">
      <!-- Dropdown menu -->
      <div id="user-dropdown" style="display:none;position:absolute;bottom:calc(100% + 6px);left:0;right:0;background:var(--surface);border:1px solid var(--border);border-radius:10px;box-shadow:0 4px 24px rgba(0,0,0,.4);overflow:hidden;z-index:500;">
        <div onclick="openSettings('user');closeUserDropdown()" style="display:flex;align-items:center;gap:10px;padding:11px 16px;cursor:pointer;color:var(--text2);font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background=''">
          <span style="font-size:15px;">⚙</span> Settings
        </div>
        <div style="height:1px;background:var(--border);margin:0 10px;"></div>
        <div onclick="signOut()" style="display:flex;align-items:center;gap:10px;padding:11px 16px;cursor:pointer;color:var(--red);font-size:13px;font-weight:500;transition:background .12s;" onmouseover="this.style.background='rgba(248,113,113,.08)'" onmouseout="this.style.background=''">
          <span style="font-size:15px;">→</span> Sign Out
        </div>
      </div>
      <!-- User card -->
      <div class="user-card" onclick="toggleUserDropdown(event)" title="Account options">
        <div class="user-avatar" id="sideAvatarBg"><span id="sideAvatarInitials">PK</span></div>
        <div class="user-info">
          <div class="user-name" id="sideUserName">Previt Ketsia</div>
          <div class="user-role" id="sideUserRole">Chief Accountant</div>
          <div class="user-co" id="sideUserCo">My Company Ltd.</div>
        </div>
        <div class="user-gear" style="font-size:16px;">⋯</div>
      </div>
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
        <div class="kpi-card g"><div class="card-title">Total Revenue</div><div class="card-value" id="kpi-rev">€0</div><div class="card-delta">From journal entries</div></div>
        <div class="kpi-card r"><div class="card-title">Total Expenses</div><div class="card-value" id="kpi-exp">€0</div><div class="card-delta" id="kpi-exp-delta">COGS + OpEx + Financial</div></div>
        <div class="kpi-card a"><div class="card-title">Net Income</div><div class="card-value" id="kpi-ni">€0</div><div class="card-delta">Revenue − Expenses</div></div>
        <div class="kpi-card b"><div class="card-title">Cash Position</div><div class="card-value" id="kpi-cash">€0</div><div class="card-delta">Net cash from JE movements</div></div>
      </div>
      <div class="row">
        <div class="col2">
          <div class="chart-area">
            <div class="sec-hdr"><div><div class="sec-title">Revenue vs Expenses</div><div class="sec-sub">Monthly overview</div></div></div>
            <div class="chart-bars" id="chartBars"><div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:monospace;">Add transactions to see chart</div></div>
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
              <div style="display:flex;justify-content:space-between;align-items:center;"><span style="color:var(--text2);">Net Margin</span><span style="font-family:monospace;" id="qs-mg">—</span></div>
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
        <span id="ct-count" style="font-size:11px;color:var(--text3);font-family:monospace;"></span>
      </div>
      <!-- Contacts grid -->
      <div class="contacts-grid" id="contactsGrid">
        <div style="color:var(--text3);font-size:13px;font-family:monospace;padding:32px;text-align:center;grid-column:1/-1;">
          No contacts yet. Click "+ New Contact" to add your first client or supplier.
        </div>
      </div>
    </div>

    <!-- ══ SALES ══ -->
    <div class="page" id="page-sales">
      <div class="sec-hdr">
        <div><div class="sec-title">Sales Invoices</div><div class="sec-sub">Record customer invoices</div></div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn-xls" onclick="exportExcel('sales')" title="Export Excel">📊</button>
          <button class="btn-pdf2" onclick="exportPDF('sales','Sales Invoices')" title="Export PDF">📄</button>
          <button class="btn btn-primary" id="sales-new-btn" onclick="openOverlay('ov-sale')">+ New Invoice</button>
        </div>
      </div>
      <!-- View tabs -->
      <div class="view-tabs">
        <div class="view-tab active" id="stab-invoices" onclick="setSalesTab('invoices')">📄 Invoices</div>
        <div class="view-tab" id="stab-recurring" onclick="setSalesTab('recurring')">🔁 Recurring <span id="rc-count-badge" style="margin-left:4px;background:var(--accent);color:#0f0f11;border-radius:10px;padding:1px 7px;font-size:10px;font-weight:700;"></span></div>
      </div>
      <!-- Invoices view -->
      <div id="sales-view-invoices">
        <div class="totbar">
          <div class="tot-item"><label>Invoiced</label><span id="s-tot" style="color:var(--green);">€0.00</span></div>
          <div class="tot-item"><label>Collected</label><span id="s-coll" style="color:var(--blue);">€0.00</span></div>
          <div class="tot-item"><label>Pending A/R</label><span id="s-ar" style="color:var(--yellow);">€0.00</span></div>
          <div class="tot-item"><label>Count</label><span id="s-cnt" style="color:var(--text2);">0</span></div>
        </div>
        <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Customer</th><th>Description</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="salesTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr></tbody></table></div></div>
      </div>
      <!-- Recurring view -->
      <div id="sales-view-recurring" style="display:none;">
        <div class="totbar">
          <div class="tot-item"><label>Active</label><span id="rc-active" style="color:var(--green);">0</span></div>
          <div class="tot-item"><label>Monthly Revenue</label><span id="rc-mrr" style="color:var(--accent);">€0.00</span></div>
          <div class="tot-item"><label>Paused</label><span id="rc-paused" style="color:var(--yellow);">0</span></div>
          <div class="tot-item"><label>Total</label><span id="rc-total" style="color:var(--text2);">0</span></div>
        </div>
        <div style="display:flex;gap:0;border:1px solid var(--border);border-radius:var(--radius);overflow:hidden;background:var(--surface);">
          <!-- List -->
          <div style="flex:1;min-width:0;overflow:auto;">
            <table style="width:100%;border-collapse:collapse;">
              <thead><tr>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Contact</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Interval</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Start</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Next</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">End</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Status</th>
                <th style="padding:10px 12px;text-align:left;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Description</th>
                <th style="padding:10px 12px;text-align:right;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:var(--surface2);border-bottom:1px solid var(--border);">Amount</th>

              </tr></thead>
              <tbody id="recurringTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:32px;">No recurring invoices yet. Open any invoice and click ⇄ Convert → Recurring Invoice.</td></tr></tbody>
            </table>
          </div>
          <!-- Side panel -->
          <div class="rc-panel" id="rc-side-panel">
            <div class="rc-panel-hdr">
              <div class="rc-panel-title" id="rcp-title">Recurring Invoice</div>
              <div style="display:flex;align-items:center;gap:6px;position:relative;">
                <div style="position:relative;">
                  <button class="rc-dots-btn" id="rcp-dots-btn" onclick="toggleRCPanelMenu(event)" title="Options" style="font-size:20px;padding:2px 8px;">⋯</button>
                  <div id="rcp-ctx-menu" class="rc-ctx-menu" style="right:0;top:110%;">
                    <div class="rc-ctx-item" onclick="openRCEditPage(_rcPanelId)">✏️ Edit</div>
                    <div class="rc-ctx-item" onclick="duplicateRC(_rcPanelId);document.getElementById('rcp-ctx-menu').classList.remove('open')">⧉ Duplicate</div>
                    <div class="rc-ctx-item danger" onclick="deleteRC(_rcPanelId);document.getElementById('rcp-ctx-menu').classList.remove('open')">🗑 Delete</div>
                    <div class="rc-ctx-item" onclick="closeRCPanel();document.getElementById('rcp-ctx-menu').classList.remove('open')">✕ Close</div>
                  </div>
                </div>
              </div>
            </div>
            <div class="rc-panel-body">
              <!-- Description -->
              <div class="rc-panel-section">Description</div>
              <div id="rcp-desc" style="font-size:13px;color:var(--text2);margin-bottom:4px;"></div>
              <!-- Contact info -->
              <div style="display:flex;align-items:center;gap:10px;padding:10px 0;border-bottom:1px solid var(--border);margin-bottom:4px;">
                <div id="rcp-avatar" style="width:36px;height:36px;border-radius:50%;background:var(--teal,#0E9AA7);display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:14px;flex-shrink:0;"></div>
                <div>
                  <div id="rcp-customer" style="font-size:14px;font-weight:700;color:var(--text);"></div>
                  <div id="rcp-customer-email" style="font-size:11px;color:var(--text3);"></div>
                </div>
              </div>

              <!-- Dates info -->
              <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin:12px 0;">
                <div style="text-align:center;">
                  <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px;">Interval</div>
                  <div id="rcp-interval" style="font-size:12px;font-weight:600;color:var(--accent);"></div>
                </div>
                <div style="text-align:center;">
                  <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px;">Start</div>
                  <div id="rcp-start" style="font-size:12px;font-weight:600;color:var(--text);"></div>
                </div>
                <div style="text-align:center;">
                  <div style="font-size:10px;color:var(--text3);text-transform:uppercase;letter-spacing:.5px;margin-bottom:3px;">End</div>
                  <div id="rcp-end" style="font-size:12px;font-weight:600;color:var(--text);"></div>
                </div>
              </div>

              <!-- Auto create & send toggles -->
              <div class="rc-panel-section">Auto Create &amp; Send</div>
              <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:12px 14px;margin-bottom:14px;">
                <div class="rc-toggle-row">
                  <div>
                    <div class="rc-toggle-label">Create invoices automatically</div>
                    <div class="rc-toggle-sub">Generate on each due date</div>
                  </div>
                  <label class="toggle-sw">
                    <input type="checkbox" id="rcp-autocreate" onchange="saveRCPSettings()">
                    <div class="toggle-sw-track"><div class="toggle-sw-thumb"></div></div>
                  </label>
                </div>
                <div class="rc-toggle-row">
                  <div>
                    <div class="rc-toggle-label">Send invoices automatically</div>
                    <div class="rc-toggle-sub">Email to contact on creation</div>
                  </div>
                  <label class="toggle-sw">
                    <input type="checkbox" id="rcp-autosend" onchange="saveRCPSettings()">
                    <div class="toggle-sw-track"><div class="toggle-sw-thumb"></div></div>
                  </label>
                </div>
              </div>

              <!-- Edit fields -->
              <div class="rc-panel-section">Edit Settings</div>
              <div class="rc-field">
                <label>Amount (net €)</label>
                <input type="number" id="rcp-net" step="0.01" oninput="recalcRCP()">
              </div>
              <div class="rc-field">
                <label>VAT Rate (%)</label>
                <select id="rcp-vat" onchange="recalcRCP()">
                  <option value="0">0%</option><option value="4">4%</option>
                  <option value="10">10%</option><option value="21">21%</option>
                </select>
              </div>
              <div class="rc-field">
                <label>Total (incl. VAT)</label>
                <input type="text" id="rcp-total-display" readonly style="background:var(--surface3);color:var(--accent);font-weight:700;">
              </div>
              <div class="rc-field">
                <label>End Date (blank = indefinite)</label>
                <input type="date" id="rcp-enddate">
              </div>
              <div style="display:flex;gap:8px;margin-top:4px;">
                <button class="btn btn-primary btn-sm" style="flex:1;" onclick="saveRCPanel()">💾 Save Changes</button>
                <button class="btn btn-danger btn-sm" onclick="stopRecurring(_rcPanelId)">⏹ Stop</button>
              </div>

              <!-- Cascade timeline -->
              <div class="rc-panel-section" style="margin-top:18px;">Invoice History &amp; Upcoming</div>
              <div style="font-size:11px;color:var(--text3);margin-bottom:8px;" id="rcp-daterange"></div>
              <div class="rc-cascade" id="rcp-cascade"></div>
            </div>
          </div>
        </div>
      </div>
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
      <div class="card"><div class="tbl-wrap"><table><thead><tr><th>#</th><th>Date</th><th>Type</th><th>Supplier</th><th>Description</th><th>Category</th><th>VAT%</th><th>Net</th><th>VAT</th><th>Total</th><th>Status</th><th></th></tr></thead><tbody id="purchTbl"><tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr></tbody></table></div></div>
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
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Collection — From Sales Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Customer</th><th>Description</th><th>Total</th><th>Collected</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingCollTbl"><tr><td colspan="9" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- COLLECTION HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Collection History</div>
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
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">⏳ Pending Payment — From Purchase Invoices</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>Invoice #</th><th>Date</th><th>Supplier</th><th>Description</th><th>Category</th><th>Total</th><th>Paid</th><th>Remaining</th><th>Method</th><th>Action</th></tr></thead>
          <tbody id="pendingPayTbl"><tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No pending invoices.</td></tr></tbody>
        </table></div></div>
      </div>

      <!-- PAYMENT HISTORY -->
      <div>
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:10px;">✅ Payment History</div>
        <div class="card"><div class="tbl-wrap"><table>
          <thead><tr><th>#</th><th>Date</th><th>Supplier</th><th>Invoice Ref</th><th>Method</th><th>Amount</th><th>Notes</th><th></th></tr></thead>
          <tbody id="payTbl"><tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No payments yet.</td></tr></tbody>
        </table></div></div>
      </div>
    </div>

    <!-- ══ JOURNAL ══ -->
    <div class="page" id="page-journal">
      <div class="sec-hdr"><div><div class="sec-title">Journal Entries</div><div class="sec-sub">Double-entry bookkeeping</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('journal')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('journal','Journal Entries')" title="Export PDF">📄</button><button class="btn btn-primary" onclick="openNewJE()">+ New Entry</button></div></div>
      <div id="je-filter-bar" class="je-filter-bar" style="display:none;">
        <span class="filter-label">Filtered by:</span>
        <span class="filter-val" id="je-filter-label"></span>
        <span class="je-acc-code" id="je-filter-acc" style="font-size:11px;"></span>
        <span style="font-size:11px;color:var(--text3);" id="je-filter-count"></span>
        <button class="btn btn-ghost btn-sm" onclick="clearJEFilter()" style="margin-left:auto;">✕ Clear filter</button>
      </div>
      <div class="card"><div class="tbl-wrap"><table><thead><tr>
  <th style="width:90px;">Entry #</th>
  <th style="width:100px;">Date</th>
  <th style="width:70px;">Type</th>
  <th>Description / Account</th>
  <th style="width:80px;">Acc. Code</th>
  <th style="width:130px;text-align:right;">Debit (€)</th>
  <th style="width:130px;text-align:right;">Credit (€)</th>
  <th style="width:80px;"></th>
</tr></thead><tbody id="jeTbl"><tr><td colspan="7" style="text-align:center;color:var(--text3);padding:24px;">No journal entries yet.</td></tr></tbody></table></div></div>
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
      <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
        <select id="pl-view-mode" class="period-select" style="min-width:160px;" onchange="setViewMode(this.value)">
          <option value="total">— View as —</option>
          <option value="monthly">Monthly (Jan–Dec)</option>
          <option value="quarterly">Quarterly (Q1–Q4)</option>
          <option value="annual">Annual</option>
        </select>
        <select id="pl-view-year" class="period-select" style="min-width:90px;" onchange="setViewMode(document.getElementById('pl-view-mode').value)">
        </select>
        <button class="btn btn-ghost btn-sm" onclick="resetViewMode()" id="pl-view-reset" style="display:none;">✕ Reset</button>
      </div>
      <div class="date-filter-bar">
        <label>From</label>
        <input type="date" id="df-from" onchange="setDateFilter(this.value, document.getElementById('df-to').value)">
        <label>To</label>
        <input type="date" id="df-to" onchange="setDateFilter(document.getElementById('df-from').value, this.value)">
        <button class="btn btn-ghost btn-sm" onclick="document.getElementById('df-from').value='';document.getElementById('df-to').value='';setDateFilter('','');">✕ Clear</button>
        <span id="df-badge" style="display:none;" class="filter-active-badge">● Filtered</span>
      </div>
      <div class="card"><div class="tbl-wrap"><table class="rtbl" id="plTable"><colgroup id="plColgroup"><col style="width:55%"><col style="width:45%"></colgroup><thead id="plHead"></thead><tbody id="plBody"></tbody></table></div></div>
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
        <span id="bsChk" style="font-family:monospace;font-size:13px;"></span>
      </div>
    </div>

    <!-- ══ CASH FLOW ══ -->
    <div class="page" id="page-cf">
      <div class="sec-hdr"><div><div class="sec-title">Cash Flow Statement</div><div class="sec-sub">Cash movements by activity</div></div><div style="display:flex;align-items:center;gap:8px;"><button class="btn-xls" onclick="exportExcel('cashflow')" title="Export Excel">📊</button><button class="btn-pdf2" onclick="exportPDF('cf','Cash Flow')" title="Export PDF">📄</button></div></div>
      <div class="period-bar">
        <select class="period-select" id="period-select3" onchange="applyPeriodPreset(this.value)">
          <option value="">— Select period —</option>
          <optgroup label="Quick Select">
            <option value="this_month">This Month</option>
            <option value="last_month">Last Month</option>
            <option value="this_quarter">This Quarter</option>
            <option value="last_quarter">Last Quarter</option>
            <option value="this_year">This Year (Annual)</option>
            <option value="last_year">Last Year</option>
          </optgroup>
          <optgroup label="Quarters">
            <option value="q1">Q1 (Jan–Mar)</option>
            <option value="q2">Q2 (Apr–Jun)</option>
            <option value="q3">Q3 (Jul–Sep)</option>
            <option value="q4">Q4 (Oct–Dec)</option>
          </optgroup>
          <optgroup label="Months">
            <option value="m1">January</option>
            <option value="m2">February</option>
            <option value="m3">March</option>
            <option value="m4">April</option>
            <option value="m5">May</option>
            <option value="m6">June</option>
            <option value="m7">July</option>
            <option value="m8">August</option>
            <option value="m9">September</option>
            <option value="m10">October</option>
            <option value="m11">November</option>
            <option value="m12">December</option>
          </optgroup>
        </select>
        <div class="period-nav">
          <button class="period-nav-btn" onclick="shiftPeriod(-1)" title="Previous period">‹</button>
          <div class="period-label" id="period-label3">All time</div>
          <button class="period-nav-btn" onclick="shiftPeriod(1)" title="Next period">›</button>
        </div>
        <button class="btn btn-ghost btn-sm" onclick="clearPeriod()" title="Clear period filter">✕ All</button>
      </div>
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
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('client',null,'s-cust')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="s-cust-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="s-desc" placeholder="e.g. Consulting services Q1"></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="s-net" placeholder="0.00" step="0.01" oninput="calcS()"></div>
        <div class="fg"><label>VAT Rate</label><select id="s-vat" onchange="calcS()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="s-va" readonly style="background:var(--surface3);"></div>
        <div class="fg"><label>Total (€)</label><input type="text" id="s-tot2" readonly style="background:var(--surface3);color:var(--accent);font-family:monospace;font-weight:600;"></div>
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
        <div class="fg full">
          <label>Type of Invoice</label>
          <select id="p-invtype" onchange="onPurchTypeChange(this.value)" style="font-weight:600;">
            <option value="expense">📋 Expense — goes to P&L as operating cost</option>
            <option value="asset">🏗 Asset — goes to Balance Sheet as non-current asset</option>
          </select>
        </div>
        <!-- Asset name field (only shown when type=asset) -->
        <div class="fg full" id="p-asset-name-row" style="display:none;">
          <label>Asset Name / Description</label>
          <input type="text" id="p-asset-name" placeholder="e.g. MacBook Pro 16 · Office equipment">
        </div>
        <div class="fg full"><label>Supplier</label>
          <div class="autocomplete-wrap">
            <div style="display:flex;gap:6px;">
              <input type="text" id="p-sup" placeholder="Type to search contacts..." autocomplete="off" oninput="acSearch('p-sup','p-sup-list','supplier')" onfocus="acSearch('p-sup','p-sup-list','supplier')" onblur="setTimeout(function(){closeAC('p-sup-list')},200)" style="flex:1;">
              <button class="btn btn-ghost btn-sm" onclick="openContactModal('supplier',null,'p-sup')" title="Add new contact" style="flex-shrink:0;padding:8px 10px;">+</button>
            </div>
            <div class="autocomplete-list" id="p-sup-list"></div>
          </div>
        </div>
        <div class="fg full"><label>Description</label><input type="text" id="p-desc" placeholder="e.g. Office rent March"></div>
        <div class="fg"><label>Category</label><select id="p-cat"><option value="COGS">Cost of Goods Sold</option><option value="Rent">Rent</option><option value="Salaries">Salaries</option><option value="Utilities">Utilities</option><option value="Marketing">Marketing</option><option value="Professional">Professional Services</option><option value="Depreciation">Depreciation</option><option value="Other OpEx">Other OpEx</option></select></div>
        <div class="fg"><label>VAT Rate</label><select id="p-vat" onchange="calcP()"><option value="0">0%</option><option value="4">4%</option><option value="10">10%</option><option value="21" selected>21%</option></select></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="p-net" placeholder="0.00" step="0.01" oninput="calcP()"></div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="p-va" readonly style="background:var(--surface3);"></div>
        <div class="fg full"><label>Total (€)</label><input type="text" id="p-tot2" readonly style="background:var(--surface3);color:var(--red);font-family:monospace;font-weight:600;"></div>
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
        <span style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">Account</span>
        <span style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">Debit (€)</span>
        <span style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">Credit (€)</span>
        <span></span>
      </div>
      <div id="jeLines"></div>
      <button class="btn btn-ghost btn-sm" style="margin-top:8px;" onclick="addJELine()">+ Add Line</button>
      <div style="display:flex;gap:20px;padding:12px 14px;background:var(--surface2);border-radius:7px;margin-top:12px;">
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:monospace;margin-bottom:2px;">DEBIT</span><span id="je-td" style="font-family:monospace;color:var(--green);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:monospace;margin-bottom:2px;">CREDIT</span><span id="je-tc" style="font-family:monospace;color:var(--red);">€0.00</span></div>
        <div><span style="font-size:11px;color:var(--text3);display:block;font-family:monospace;margin-bottom:2px;">STATUS</span><span id="je-st" style="font-family:monospace;">—</span></div>
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
            <div style="font-size:12px;color:var(--text3);margin-bottom:8px;font-family:monospace;text-transform:uppercase;letter-spacing:1px;">Avatar Color</div>
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
          <div class="fg full" style="background:var(--surface2);border:1px solid var(--accent);border-radius:8px;padding:14px;margin-bottom:4px;">
            <label style="font-size:11px;color:var(--accent);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;display:block;margin-bottom:8px;">📋 Accounting Plan / Chart of Accounts</label>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;">
              <div onclick="selectAccountPlan('usgaap')" id="plan-card-usgaap" style="border:2px solid var(--accent);border-radius:8px;padding:12px;cursor:pointer;background:var(--surface3);">
                <div style="font-weight:700;font-size:13px;color:var(--text);margin-bottom:4px;">🇺🇸 US GAAP / Simplified</div>
                <div style="font-size:11px;color:var(--text3);">Accounts 1000–7100. English labels. Standard for international use.</div>
                <div id="plan-active-usgaap" style="margin-top:8px;font-size:10px;font-weight:700;color:var(--accent);font-family:'DM Mono',monospace;">✓ ACTIVE</div>
              </div>
              <div onclick="selectAccountPlan('pgc')" id="plan-card-pgc" style="border:2px solid var(--border);border-radius:8px;padding:12px;cursor:pointer;">
                <div style="font-weight:700;font-size:13px;color:var(--text);margin-bottom:4px;">🇪🇸 PGC España</div>
                <div style="font-size:11px;color:var(--text3);">Cuentas 100–778. PGC 2007 adaptado. Obligatorio para empresas españolas.</div>
                <div id="plan-active-pgc" style="margin-top:8px;font-size:10px;font-weight:700;color:var(--text3);font-family:'DM Mono',monospace;display:none;">✓ ACTIVE</div>
              </div>
            </div>
            <div id="plan-warning" style="display:none;margin-top:10px;padding:8px 12px;background:rgba(251,146,60,.1);border:1px solid rgba(251,146,60,.3);border-radius:6px;font-size:12px;color:var(--yellow);">
              ⚠️ Changing the accounting plan affects how new Journal Entries are generated. Existing JEs are preserved. The financial statements will reflect the new account structure immediately.
            </div>
          </div>
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
          <div class="fg"><label>Invoice Prefix (legacy)</label><input type="text" id="set-invpfx" placeholder="INV-" maxlength="10"></div>
          <div class="fg"><label>Purchase Prefix (legacy)</label><input type="text" id="set-purpfx" placeholder="PINV-" maxlength="10"></div>
        </div>
        <!-- ── INVOICE NUMBERING SERIES ── -->
        <div class="set-section-label" style="margin-top:20px;">📋 Invoice Numbering Series</div>
        <div style="font-size:12px;color:var(--text3);margin-bottom:12px;">
          Format tokens: <code style="background:var(--surface3);padding:2px 6px;border-radius:4px;">[YY]</code> = 2-digit year &nbsp;
          <code style="background:var(--surface3);padding:2px 6px;border-radius:4px;">[YYYY]</code> = 4-digit year &nbsp;
          <code style="background:var(--surface3);padding:2px 6px;border-radius:4px;">%</code> = sequential digit
        </div>
        <div id="series-list"></div>
        <button class="btn btn-ghost btn-sm" onclick="openSeriesModal()" style="margin-top:8px;">+ Add Series</button>
      </div>

      <!-- ── DATA PANEL ── -->
      <div class="set-panel" id="spanel-data">
        <!-- ── Session Summary ── -->
        <div class="set-section-label">Session Summary</div>
        <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:16px;margin-bottom:20px;display:grid;grid-template-columns:1fr 1fr;gap:6px 20px;">
          <div class="info-row"><span class="info-label">Sales Invoices</span><span class="info-val" id="di-sales">0</span></div>
          <div class="info-row"><span class="info-label">Purchase Invoices</span><span class="info-val" id="di-purch">0</span></div>
          <div class="info-row"><span class="info-label">Collections</span><span class="info-val" id="di-coll">0</span></div>
          <div class="info-row"><span class="info-label">Payments</span><span class="info-val" id="di-pay">0</span></div>
          <div class="info-row"><span class="info-label">Journal Entries</span><span class="info-val" id="di-je">0</span></div>
          <div class="info-row"><span class="info-label">Storage Used</span><span class="info-val" id="di-size">—</span></div>
        </div>

        <!-- ── EXPORT ── -->
        <div class="set-section-label">📤 Export Data</div>
        <div style="font-size:12px;color:var(--text3);margin-bottom:10px;">Download your data as CSV. Each file can be opened in Excel, Google Sheets or imported into Power BI.</div>
        <div class="export-grid">
          <div class="export-btn-card" onclick="exportExcel('sales')">
            <div class="ebc-icon">🧾</div>
            <div class="ebc-label">Sales</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportExcel('purchases')">
            <div class="ebc-icon">🛒</div>
            <div class="ebc-label">Purchases</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportExcel('collections')">
            <div class="ebc-icon">💰</div>
            <div class="ebc-label">Collections</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportExcel('payments')">
            <div class="ebc-icon">💸</div>
            <div class="ebc-label">Payments</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportExcel('journal')">
            <div class="ebc-icon">📒</div>
            <div class="ebc-label">Journal</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportExcel('contacts')">
            <div class="ebc-icon">👥</div>
            <div class="ebc-label">Contacts</div>
            <div class="ebc-fmt">CSV</div>
          </div>
          <div class="export-btn-card" onclick="exportFullBackup()">
            <div class="ebc-icon">💾</div>
            <div class="ebc-label">Full Backup</div>
            <div class="ebc-fmt">JSON</div>
          </div>
        </div>

        <!-- ── IMPORT ── -->
        <div class="set-section-label" style="margin-top:24px;">📥 Import Data</div>
        <div style="font-size:12px;color:var(--text3);margin-bottom:10px;">
          Import Sales, Purchases, Contacts or a full backup. FinLedger will automatically generate Journal Entries and update all financial statements.
          &nbsp;<span class="template-btn" onclick="downloadImportTemplate()">⬇ Download template</span>
        </div>

        <!-- Drag & drop zone -->
        <div class="import-zone" id="import-drop-zone"
          ondragover="event.preventDefault();this.classList.add('drag-over')"
          ondragleave="this.classList.remove('drag-over')"
          ondrop="handleImportDrop(event)"
          onclick="document.getElementById('import-file-input').click()">
          <div class="import-zone-icon">📂</div>
          <div class="import-zone-title">Drop a CSV or JSON file here</div>
          <div class="import-zone-sub">or click to browse · Supported: Sales CSV, Purchases CSV, Contacts CSV, Full Backup JSON</div>
          <input type="file" id="import-file-input" accept=".csv,.json" style="display:none" onchange="handleImportFile(this)">
        </div>

        <!-- Preview / result area -->
        <div id="import-result-area" style="display:none;">
          <div id="import-result-msg" class="import-result ok"></div>
          <div class="import-preview" id="import-preview-table"></div>
          <div style="display:flex;gap:10px;margin-top:12px;justify-content:flex-end;">
            <button class="btn btn-ghost btn-sm" onclick="clearImport()">Cancel</button>
            <button class="btn btn-primary" id="import-confirm-btn" onclick="confirmImport()">✅ Import &amp; Process</button>
          </div>
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
  series:[
    {id:1, name:'Sales Invoices',    code:'INV',  format:'INV[YY]-%%%%%', lastNum:0, type:'sale',   active:true},
    {id:2, name:'Credit Notes',      code:'CN',   format:'CN[YY]-%%%%%',  lastNum:0, type:'credit', active:true},
    {id:3, name:'Purchase Invoices', code:'PINV', format:'PINV[YY]-%%%%', lastNum:0, type:'purchase',active:true}
  ],
  sales:[],purch:[],coll:[],pay:[],je:[],
  contacts:[],recurring:[],
  assets:[], deprPlans:[],
  ids:{s:1,p:1,c:1,py:1,j:1,ct:1,rc:1,ast:1,dp:1}
};
var plMode='detail';
var AVATAR_COLORS=['#c8ff00','#00d4ff','#a78bfa','#fb923c','#f472b6','#34d399','#ffd93d','#f87171','#60a5fa'];
// ── US GAAP / Simplified Chart of Accounts ──────────────────────
var COA_USGAAP = [
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

// ── PGC España (Plan General Contable) ───────────────────────────
var COA_PGC = [
  // Grupo 1 — Financiación Básica
  {c:'100',n:'Capital social',t:'equity'},{c:'110',n:'Prima de emisión',t:'equity'},
  {c:'112',n:'Reserva legal',t:'equity'},{c:'113',n:'Reservas voluntarias',t:'equity'},
  {c:'129',n:'Resultado del ejercicio',t:'equity'},
  {c:'170',n:'Deudas LP con entidades de crédito',t:'liability'},
  {c:'171',n:'Deudas a largo plazo',t:'liability'},
  {c:'174',n:'Acreedores por arrendamiento financiero LP',t:'liability'},
  // Grupo 2 — Inmovilizado
  {c:'210',n:'Terrenos y bienes naturales',t:'asset'},
  {c:'211',n:'Construcciones',t:'asset'},
  {c:'213',n:'Maquinaria',t:'asset'},
  {c:'216',n:'Mobiliario',t:'asset'},
  {c:'217',n:'Equipos para procesos de información',t:'asset'},
  {c:'280',n:'Amort. acum. inmovilizado intangible',t:'asset'},
  {c:'281',n:'Amort. acum. inmovilizado material',t:'asset'},
  // Grupo 3 — Existencias
  {c:'300',n:'Mercaderías',t:'asset'},
  {c:'310',n:'Materias primas',t:'asset'},
  {c:'350',n:'Productos terminados',t:'asset'},
  // Grupo 4 — Acreedores y deudores comerciales
  {c:'400',n:'Proveedores',t:'liability'},
  {c:'410',n:'Acreedores por prestaciones de servicios',t:'liability'},
  {c:'430',n:'Clientes',t:'asset'},
  {c:'431',n:'Clientes, efectos comerciales a cobrar',t:'asset'},
  {c:'460',n:'Anticipos de remuneraciones',t:'asset'},
  {c:'470',n:'HP deudora por IVA',t:'asset'},
  {c:'472',n:'HP, IVA soportado',t:'asset'},
  {c:'475',n:'HP acreedora por conceptos fiscales',t:'liability'},
  {c:'476',n:'Organismos SS, acreedores',t:'liability'},
  {c:'477',n:'HP, IVA repercutido',t:'liability'},
  {c:'480',n:'Gastos anticipados',t:'asset'},
  {c:'485',n:'Ingresos anticipados',t:'liability'},
  // Grupo 5 — Cuentas financieras
  {c:'520',n:'Deudas CP con entidades de crédito',t:'liability'},
  {c:'521',n:'Deudas a corto plazo',t:'liability'},
  {c:'551',n:'Cuenta corriente con socios y administradores',t:'liability'},
  {c:'570',n:'Caja, euros',t:'asset'},
  {c:'572',n:'Bancos c/c vista, euros',t:'asset'},
  {c:'573',n:'Bancos c/c vista, moneda extranjera',t:'asset'},
  // Grupo 6 — Compras y Gastos
  {c:'600',n:'Compras de mercaderías',t:'expense'},
  {c:'601',n:'Compras de materias primas',t:'expense'},
  {c:'602',n:'Compras otros aprovisionamientos',t:'expense'},
  {c:'607',n:'Trabajos realizados por otras empresas',t:'expense'},
  {c:'621',n:'Arrendamientos y cánones',t:'expense'},
  {c:'622',n:'Reparaciones y conservación',t:'expense'},
  {c:'623',n:'Servicios de profesionales independientes',t:'expense'},
  {c:'624',n:'Transportes',t:'expense'},
  {c:'625',n:'Primas de seguros',t:'expense'},
  {c:'626',n:'Servicios bancarios y similares',t:'expense'},
  {c:'627',n:'Publicidad, propaganda y RRPP',t:'expense'},
  {c:'628',n:'Suministros',t:'expense'},
  {c:'629',n:'Otros servicios',t:'expense'},
  {c:'640',n:'Sueldos y salarios',t:'expense'},
  {c:'641',n:'Indemnizaciones',t:'expense'},
  {c:'642',n:'Seguridad Social a cargo de la empresa',t:'expense'},
  {c:'649',n:'Otros gastos sociales',t:'expense'},
  {c:'660',n:'Gastos financieros por actualización de provisiones',t:'expense'},
  {c:'662',n:'Intereses de deudas',t:'expense'},
  {c:'665',n:'Intereses por descuento de efectos',t:'expense'},
  {c:'668',n:'Diferencias negativas de cambio',t:'expense'},
  {c:'669',n:'Otros gastos financieros',t:'expense'},
  {c:'671',n:'Pérdidas procedentes de activos no corrientes',t:'expense'},
  {c:'678',n:'Gastos excepcionales',t:'expense'},
  {c:'680',n:'Amortización inmovilizado intangible',t:'expense'},
  {c:'681',n:'Amortización inmovilizado material',t:'expense'},
  {c:'690',n:'Pérdidas por deterioro de existencias',t:'expense'},
  {c:'694',n:'Pérdidas por deterioro de créditos',t:'expense'},
  {c:'698',n:'Dotación provisión para otras responsabilidades',t:'expense'},
  // Grupo 7 — Ventas e Ingresos
  {c:'700',n:'Ventas de mercaderías',t:'revenue'},
  {c:'701',n:'Ventas de productos terminados',t:'revenue'},
  {c:'705',n:'Prestaciones de servicios',t:'revenue'},
  {c:'708',n:'Devoluciones de ventas',t:'revenue'},
  {c:'710',n:'Variación de existencias de mercaderías',t:'revenue'},
  {c:'740',n:'Subvenciones a la explotación',t:'revenue'},
  {c:'751',n:'Resultados de operaciones en común',t:'revenue'},
  {c:'752',n:'Ingresos por arrendamientos',t:'revenue'},
  {c:'754',n:'Ingresos por comisiones',t:'revenue'},
  {c:'759',n:'Ingresos por servicios diversos',t:'revenue'},
  {c:'760',n:'Ingresos de participaciones en instrumentos de patrimonio',t:'revenue'},
  {c:'762',n:'Ingresos de créditos',t:'revenue'},
  {c:'768',n:'Diferencias positivas de cambio',t:'revenue'},
  {c:'769',n:'Otros ingresos financieros',t:'revenue'},
  {c:'771',n:'Beneficios procedentes de activos no corrientes',t:'revenue'},
  {c:'778',n:'Ingresos excepcionales',t:'revenue'}
];

// ── Account plan definitions (metadata + JE mappings) ────────────
var ACCOUNT_PLANS = {
  usgaap: {
    id: 'usgaap',
    name: 'US GAAP / Simplified',
    coa: COA_USGAAP,
    // JE account codes for auto-entries
    cash:     '1000',
    ar:       '1100',
    ap:       '2000',
    vatIn:    '2100',  // VAT collected (output)
    vatOut:   '2100',  // VAT paid (input) — combined in simplified
    revenue:  '4000',
    cogs:     '5000',
    ltDebt:   '2500',
    capital:  '3000',
    // P&L account groups
    revAccts:  ['4000','4100'],
    cogsAccts: ['5000'],
    opexAccts: ['6000','6100','6200','6300','6400','6500','6900'],
    finExpAccts:['7000','7100'],
    // BS account groups
    cashAccts:    ['1000'],
    arAccts:      ['1100'],
    apAccts:      ['2000'],
    vatAccts:     ['2100'],
    fixedAccts:   ['1500','1510'],
    ltDebtAccts:  ['2500'],
    capitalAccts: ['3000','3100'],
    financeAccts: ['2500','3000','3100','2200'],
    investAccts:  ['1500','1510'],
    // Expense category → account map
    expCatMap: {
      'Cost of Goods Sold':'5000','Salaries':'6000','Salaries & Wages':'6000',
      'Rent':'6100','Utilities':'6200','Marketing':'6300',
      'Professional Services':'6400','Depreciation':'6500','Other OpEx':'6900'
    },
    // Labels for financial statements
    labels: {
      revenue:'Sales Revenue', cogs:'COGS – Direct Purchases',
      ar:'Accounts Receivable', ap:'Accounts Payable',
      cash:'Cash & Bank', vat:'VAT Payable',
      capital:'Share Capital', ltDebt:'Long-term Debt',
      opCash:'Cash received from customers', opPay:'Cash paid to suppliers'
    }
  },
  pgc: {
    id: 'pgc',
    name: 'PGC España',
    coa: COA_PGC,
    // JE account codes
    cash:     '572',
    ar:       '430',
    ap:       '400',
    vatIn:    '477',   // HP IVA repercutido (output VAT)
    vatOut:   '472',   // HP IVA soportado (input VAT)
    revenue:  '705',
    cogs:     '600',
    ltDebt:   '170',
    capital:  '100',
    // P&L account groups
    revAccts:   ['700','701','702','703','704','705','740','751','752','754','759'],
    cogsAccts:  ['600','601','602','607'],
    opexAccts:  ['621','622','623','624','625','626','627','628','629',
                 '640','641','642','649','680','681'],
    finExpAccts:['660','662','665','668','669'],
    // BS account groups
    cashAccts:    ['570','572','573'],
    arAccts:      ['430','431'],
    apAccts:      ['400','410'],
    vatAccts:     ['477'],  // IVA repercutido liability
    fixedAccts:   ['210','211','213','216','217','280','281'],
    ltDebtAccts:  ['170','171','174'],
    capitalAccts: ['100','110','112','113','129'],
    financeAccts: ['170','171','174','100','110','112','113'],
    investAccts:  ['210','211','213','216','217'],
    // Expense category → account map
    expCatMap: {
      'Compras de mercaderías':'600','Materias primas':'601',
      'Arrendamientos':'621','Reparaciones':'622',
      'Servicios profesionales':'623','Transportes':'624',
      'Seguros':'625','Publicidad':'627','Suministros':'628',
      'Otros servicios':'629','Sueldos y salarios':'640',
      'Seguridad Social':'642','Amortización':'681','Otros gastos':'629'
    },
    // Labels for financial statements (Spanish)
    labels: {
      revenue:'Ventas / Prestaciones de servicios',
      cogs:'Compras y aprovisionamientos',
      ar:'Clientes (430)', ap:'Proveedores (400)',
      cash:'Bancos y Caja (570/572)', vat:'HP IVA repercutido (477)',
      capital:'Capital social (100)', ltDebt:'Deudas LP (170)',
      opCash:'Cobros de clientes', opPay:'Pagos a proveedores'
    }
  }
};

// Active plan — read from DB.co.accountPlan, default 'usgaap'
function getActivePlan() {
  var planId = (DB.co && DB.co.accountPlan) || 'usgaap';
  return ACCOUNT_PLANS[planId] || ACCOUNT_PLANS.usgaap;
}

// COA is always the active plan's accounts
var COA = COA_USGAAP; // will be reassigned after DB loads
function refreshCOA() {
  COA = getActivePlan().coa;
}

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
  if(!DB.contacts)  DB.contacts  = [];
  if(!DB.ids.ct)    DB.ids.ct    = 1;
  if(!DB.recurring) DB.recurring = [];
  if(!DB.ids.rc)    DB.ids.rc    = 1;
  if(!DB.assets)    DB.assets    = [];
  if(!DB.deprPlans) DB.deprPlans = [];
  if(!DB.ids.ast)   DB.ids.ast   = 1;
  if(!DB.ids.dp)    DB.ids.dp    = 1;
  // Refresh COA based on saved plan
  refreshCOA();
  if(!DB.series) DB.series = [
    {id:1,name:'Sales Invoices',   code:'INV', format:'INV[YY]-%%%%%',lastNum:0,type:'sale',   active:true},
    {id:2,name:'Credit Notes',     code:'CN',  format:'CN[YY]-%%%%%', lastNum:0,type:'credit', active:true},
    {id:3,name:'Purchase Invoices',code:'PINV',format:'PINV[YY]-%%%%',lastNum:0,type:'purchase',active:true}
  ];
  if(!DB.ids.ser) DB.ids.ser = 4;
  if(!DB.wires)   DB.wires   = [];
  if(!DB.ids.wt)  DB.ids.wt  = 1;
  if(!DB.bankAccounts)  DB.bankAccounts  = [];
  if(!DB.bankMovements) DB.bankMovements = [];
  if(!DB.ids.ba)  DB.ids.ba  = 1;
  if(!DB.ids.bm)  DB.ids.bm  = 1;
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
  initViewYears();
  refreshCOA();
  refreshPlanUI();
  // Process any pending recurring invoices
  var newOnes = processRecurringInvoices();
  if(newOnes > 0){ sv(); showToast('🔁 '+newOnes+' recurring invoice'+(newOnes>1?'s':'')+' generated'); }
  var newDepr = processDeprPlans();
  if(newDepr > 0){ sv(); showToast('📉 '+newDepr+' depreciation entry'+(newDepr>1?'ies':'y')+' posted'); }
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
  // Sidebar user card
  document.getElementById('sideAvatarInitials').textContent=ini;
  document.getElementById('sideAvatarBg').style.background=ac;
  document.getElementById('sideUserName').textContent=fn;
  document.getElementById('sideUserRole').textContent=DB.user.role||'Accountant';
  document.getElementById('sideUserCo').textContent=DB.co.name||'My Company';
  // Topbar greeting — show first name for brevity
  var greetEl=document.getElementById('topGreeting');
  if(greetEl) greetEl.textContent=(DB.user.fname||fn);
  // Page title
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
  var ini=initials(fn,ln);
  // Update modal avatar preview
  document.getElementById('previewAvatar').textContent=ini;
  // Also update sidebar immediately (live preview)
  var sideIni=document.getElementById('sideAvatarInitials');
  var sideName=document.getElementById('sideUserName');
  var topGreet=document.getElementById('topGreeting');
  if(sideIni)  sideIni.textContent=ini;
  if(sideName) sideName.textContent=((fn==='?'?'':fn)+' '+(ln==='?'?'':ln)).trim()||fn;
  if(topGreet) topGreet.textContent=fn==='?'?'':fn;
}

// ── NAVIGATION ─────────────────────────────────────────────────────────────
var titles={dashboard:'Dashboard',contacts:'Contacts',sales:'Sales Invoices',purchases:'Purchase Invoices',collections:'Collections',payments:'Payments',journal:'Journal Entries',pl:'P&L Statement',bs:'Balance Sheet',cf:'Cash Flow Statement', cfo:'CFO Intelligence', tesoreria:'Tesorería', bankaccounts:'Bank Accounts', badetail:'Account Detail'};
var crumbs={dashboard:'FinLedger / Overview',contacts:'FinLedger / Operations / Contacts',sales:'FinLedger / Operations / Sales',purchases:'FinLedger / Operations / Purchases',collections:'FinLedger / Tesorería / Collections',payments:'FinLedger / Tesorería / Payments',journal:'FinLedger / Operations / Journal',pl:'FinLedger / Reports / P&L',bs:'FinLedger / Reports / Balance Sheet',cf:'FinLedger / Reports / Cash Flow',
    cfo:'FinLedger / CFO Module', tesoreria:'FinLedger / Tesorería', bankaccounts:'FinLedger / Tesorería / Bank Accounts', badetail:'FinLedger / Tesorería / Bank Accounts / Detail'};
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
  DB.user.fname=document.getElementById('u-fname').value.trim()||'User';
  DB.user.lname=document.getElementById('u-lname').value.trim()||'';
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
  // 1. Save & close first
  sv();
  closeOverlay('ov-settings');
  // 2. Update sidebar user card immediately
  updateUserUI();
  // 3. Apply visual changes, refresh COA & re-render
  applyAccent();
  applyTranslations();
  refreshCOA();
  initJE();
  renderAll();
  showToast('✅ Settings saved.');
}

function clearAll(){
  if(!confirm('Delete ALL data?\n\nThis will delete ALL transactions, contacts, journal entries, assets and recurring invoices.\n\nYour company settings and preferences will be preserved.\n\nThis cannot be undone.'))return;
  DB.sales=[];DB.purch=[];DB.coll=[];DB.pay=[];DB.je=[];
  DB.contacts=[];DB.recurring=[];DB.assets=[];DB.deprPlans=[];DB.series=DB.series||[];DB.wires=[];
  DB.bankAccounts=[];DB.bankMovements=[];
  DB.ids={s:1,p:1,c:1,py:1,j:1,ct:1,rc:1,ast:1,dp:1,wt:1,ba:1,bm:1,
          sub_430:1,sub_431:1,sub_400:1,sub_410:1,sub_1100:1,sub_2000:1};
  sv();closeOverlay('ov-settings');renderAll();
  showToast('✅ All data cleared. Settings preserved.');
}

// ── CALC HELPERS ───────────────────────────────────────────────────────────
function calcS(){var n=parseFloat(document.getElementById('s-net').value)||0,v=parseFloat(document.getElementById('s-vat').value)||0,va=n*v/100;document.getElementById('s-va').value=va.toFixed(2);document.getElementById('s-tot2').value=(n+va).toFixed(2);}
function calcP(){var n=parseFloat(document.getElementById('p-net').value)||0,v=parseFloat(document.getElementById('p-vat').value)||0,va=n*v/100;document.getElementById('p-va').value=va.toFixed(2);document.getElementById('p-tot2').value=(n+va).toFixed(2);}

// ── SAVE OPERATIONS ────────────────────────────────────────────────────────
function saveSale(){
  var net=parseFloat(document.getElementById('s-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('s-vat').value)||0,va=net*vat/100,stat=document.getElementById('s-stat').value,meth=document.getElementById('s-meth').value,dt=document.getElementById('s-date').value;
  // Use series numbering if available, fallback to legacy prefix
  var _manualNum = document.getElementById('s-num').value;
  var num;
  if(_manualNum) {
    num = _manualNum;
  } else {
    var _defSer = getDefaultSeriesForType('sale');
    if(_defSer) {
      num = getNextSeriesNum(_defSer.id);
    } else {
      var pfx = DB.prefs.invpfx||'INV-';
      num = pfx + String(DB.ids.s).padStart(6,'0');
    }
  }
  var cust=document.getElementById('s-cust').value||'Unknown',desc=document.getElementById('s-desc').value;
  var rec={id:DB.ids.s++,date:dt,num:num,customer:cust,desc:desc,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth};
  DB.sales.push(rec);
  // Auto JE using active plan accounts
  var _sp = getActivePlan();
  var saleLines = [
    {account:_sp.ar,      debit:rec.total, credit:0},
    {account:_sp.revenue, debit:0,         credit:net}
  ];
  if(va > 0) saleLines.push({account:_sp.vatIn, debit:0, credit:va});
  DB.je.push({id:DB.ids.j++,date:dt,desc:'Sale — '+cust+' / '+num,lines:saleLines,amount:rec.total,auto:true,sourceType:'sale',sourceId:rec.id});
  if(stat==='paid'){
    DB.coll.push({id:DB.ids.c++,date:dt,customer:cust,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Collection — '+cust+' / '+num,
      lines:[{account:_sp.cash,debit:rec.total,credit:0},{account:_sp.ar,debit:0,credit:rec.total}],
      amount:rec.total,auto:true,sourceType:'collection'});
  }
  sv();closeOverlay('ov-sale');['s-num','s-cust','s-desc','s-net','s-va','s-tot2'].forEach(function(id){document.getElementById(id).value='';});renderAll();
}
function savePurch(){
  var net=parseFloat(document.getElementById('p-net').value)||0;if(!net){alert('Enter net amount.');return;}
  var vat=parseFloat(document.getElementById('p-vat').value)||0,va=net*vat/100,stat=document.getElementById('p-stat').value,meth=document.getElementById('p-meth').value,dt=document.getElementById('p-date').value;
  var invType = (document.getElementById('p-invtype')||{value:'expense'}).value || 'expense';
  var assetName = invType==='asset' ? (document.getElementById('p-asset-name')||{value:''}).value : '';
  var _manualPNum = document.getElementById('p-num').value;
  var num;
  if(_manualPNum) {
    num = _manualPNum;
  } else {
    var _defPurSer = getDefaultSeriesForType('purchase');
    if(_defPurSer) {
      num = getNextSeriesNum(_defPurSer.id);
    } else {
      var pfx = DB.prefs.purpfx||'PINV-';
      num = pfx + String(DB.ids.p).padStart(6,'0');
    }
  }
  var sup=document.getElementById('p-sup').value||'Unknown',desc=document.getElementById('p-desc').value,cat=document.getElementById('p-cat').value;
  var rec={id:DB.ids.p++,date:dt,num:num,supplier:sup,desc:desc,cat:cat,vatRate:vat,net:net,vatAmt:va,total:net+va,status:stat,method:meth,invType:invType,assetName:assetName};
  DB.purch.push(rec);

  // ── JE depends on invoice type ────────────────────────────────
  var _pp = getActivePlan();
  // catAccMap covers BOTH plans: English keys (form values) mapped per plan
  var catAccMap;
  if(_pp.id === 'pgc') {
    catAccMap = {
      'COGS':'600','Cost of Goods Sold':'600','Compras de mercaderías':'600',
      'Materias primas':'601','Raw Materials':'601',
      'Rent':'621','Arrendamientos':'621','Renting':'621',
      'Salaries':'640','Salaries & Wages':'640','Sueldos y salarios':'640',
      'Utilities':'628','Suministros':'628',
      'Marketing':'627','Publicidad':'627',
      'Professional':'623','Professional Services':'623','Servicios profesionales':'623',
      'Depreciation':'681','Amortización':'681',
      'Financial':'662','Gastos financieros':'662',
      'Other OpEx':'629','Otros':'629'
    };
  } else {
    catAccMap = {'COGS':'5000','Cost of Goods Sold':'5000','Rent':'6100','Salaries':'6000',
      'Salaries & Wages':'6000','Utilities':'6200','Marketing':'6300',
      'Professional':'6400','Professional Services':'6400',
      'Depreciation':'6500','Other OpEx':'6900'};
  }

  var purchLines;
  if(invType === 'asset') {
    // ASSET: Dr Fixed Asset account / Dr VAT / Cr AP
    var planId   = (DB.co && DB.co.accountPlan) || 'usgaap';
    // Use category value as the asset account code (selected from asset dropdown)
    var assetAcc = cat || (planId === 'pgc' ? '213' : '1500');
    purchLines = [
      {account:assetAcc, debit:net, credit:0},
      {account:_pp.ap,   debit:0,   credit:rec.total}
    ];
    if(va > 0) purchLines.splice(1, 0, {account:_pp.vatOut, debit:va, credit:0});
    // Register in assets[]
    if(!DB.assets) DB.assets = [];
    if(!DB.ids.ast) DB.ids.ast = 1;
    DB.assets.push({
      id:DB.ids.ast++, purchaseId:rec.id,
      name:assetName||desc, date:dt, num:num, supplier:sup,
      cost:net, bookValue:net, accumulated:0, status:'active'
    });
  } else {
    // EXPENSE: normal flow
    var _fallbackExp = _pp.id === 'pgc' ? '629' : '6900';
    var expAcc = (_pp.expCatMap && _pp.expCatMap[cat]) || catAccMap[cat] || _fallbackExp;
    purchLines = [
      {account:expAcc, debit:net,  credit:0},
      {account:_pp.ap, debit:0,    credit:rec.total}
    ];
    if(va > 0) purchLines.splice(1, 0, {account:_pp.vatOut, debit:va, credit:0});
  }
  DB.je.push({id:DB.ids.j++,date:dt,desc:(invType==='asset'?'Asset purchase':'Purchase')+' — '+sup+' / '+num,lines:purchLines,amount:rec.total,auto:true,sourceType:'purchase',sourceId:rec.id});
  // If paid immediately
  if(stat==='paid'){
    DB.pay.push({id:DB.ids.py++,date:dt,supplier:sup,ref:num,method:meth,amount:rec.total,notes:'Auto from invoice'});
    var _ppaid = getActivePlan();
    DB.je.push({id:DB.ids.j++,date:dt,desc:'Payment — '+sup+' / '+num,lines:[{account:_ppaid.ap,debit:rec.total,credit:0},{account:_ppaid.cash,debit:0,credit:rec.total}],amount:rec.total,auto:true,sourceType:'payment'});
  }
  sv();
  closeOverlay('ov-purch');
  ['p-num','p-sup','p-desc','p-net','p-va','p-tot2','p-asset-name'].forEach(function(id){var el=document.getElementById(id);if(el)el.value='';});
  // Reset type
  var ptEl = document.getElementById('p-invtype');
  if(ptEl) ptEl.value = 'expense';
  onPurchTypeChange('expense');
  renderAll();
  // If asset — ask about depreciation plan
  if(invType === 'asset') {
    setTimeout(function(){
      if(confirm('🏗 Asset registered: ' + (assetName||desc) + '\n\nDo you want to create a Depreciation Plan?')) {
        openDeprModal(rec.id);
      }
    }, 200);
  }
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
// Always reads from current active plan — never stale
function coaOpts(){
  var coa = getActivePlan().coa;
  return coa.map(function(a){
    return '<option value="'+a.c+'">'+a.c+' – '+a.n+'</option>';
  }).join('');
}

// Open JE modal — always rebuild lines with current COA first
function openNewJE(){
  refreshCOA();   // ensure COA global is up to date
  initJE();       // rebuild lines with fresh COA options
  openOverlay('ov-je');
}

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

  // Account classification — from active plan
  var _plan = getActivePlan();
  var CASH_ACCTS    = _plan.cashAccts;
  var AR_ACCTS      = _plan.arAccts;
  var AP_ACCTS      = _plan.apAccts;
  var INVEST_ACCTS  = _plan.investAccts;
  var FINANCE_ACCTS = _plan.financeAccts;
  var REV_ACCTS     = _plan.revAccts;
  var COGS_ACCTS    = _plan.cogsAccts;
  var OPEX_ACCTS    = _plan.opexAccts;
  var FINEXP_ACCTS  = _plan.finExpAccts;

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
  // Use active plan for these too
  var _cfp2 = getActivePlan();
  var jeFixedAssets  = _cfp2.id==='pgc'
    ? (_cfp2.fixedAccts.filter(function(a){return parseInt(a)>=200&&parseInt(a)<=221;})
        .reduce(function(s,a){return s+jeBal(a);},0))
    : jeBal('1500') - jeBal('1510');
  var jeLTDebt = _cfp2.ltDebtAccts
    ? _cfp2.ltDebtAccts.reduce(function(s,a){return s+jeBal(a);},0)
    : jeBal('2500');
  var jeShareCapital = _cfp2.capitalAccts
    ? _cfp2.capitalAccts.reduce(function(s,a){return s+jeBal(a);},0)
    : jeBal('3000');
  var jeRetained     = 0; // included in capitalAccts for PGC (129)
  var jeAccrued      = _cfp2.id==='pgc' ? 0 : jeBal('2200');
  // Use active plan account codes for BS balances
  var _cfPlan = getActivePlan();
  // Cash
  var bsCash = _cfPlan.cashAccts.reduce(function(a,acc){return a+jeBal(acc);}, 0);
  // AR (clients)
  var bsAR   = _cfPlan.arAccts.reduce(function(a,acc){return a+jeBal(acc);}, 0);
  // AP (suppliers)
  var bsAP   = _cfPlan.apAccts.reduce(function(a,acc){return a+jeBal(acc);}, 0);
  // VAT payable (output VAT collected)
  var vatP   = _cfPlan.vatAccts.reduce(function(a,acc){return a+jeBal(acc);}, 0);
  // VAT receivable (input VAT paid on purchases — 472 PGC / same 2100 USGAAP)
  var vatRec = 0;
  if(_cfPlan.id === 'pgc') {
    vatRec = jeBal('472'); // HP IVA soportado
  }

  return{
    rev:rev, cogs:cogs, opex:opex, toOpEx:toOpEx, ebit:ebit, ni:ni,
    finExp:finExp,
    totColl:totColl, totPay:totPay, cash:cash,
    ar:ar, ap:ap, vatP:vatP, vatRec:vatRec||0,
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
  var _dp = getActivePlan();
  // Total expenses = COGS + OpEx + Financial — all from JE account balances
  var totExp = F.cogs + F.toOpEx + (F.finExp||0);
  document.getElementById('kpi-rev').textContent=f(F.rev);
  document.getElementById('kpi-exp').textContent=f(totExp);
  // Delta shows breakdown
  var expDelta = document.getElementById('kpi-exp-delta');
  if(expDelta) {
    var parts = [];
    if(F.cogs>0)   parts.push('COGS: '+f(F.cogs));
    if(F.toOpEx>0) parts.push('OpEx: '+f(F.toOpEx));
    if((F.finExp||0)>0) parts.push('Financial: '+f(F.finExp));
    expDelta.textContent = parts.length ? parts.join(' · ') : (_dp.id==='pgc'?'Compras + Gastos':'COGS + OpEx');
  }
  var ni=document.getElementById('kpi-ni');
  ni.textContent=f(F.ni);
  ni.style.color=F.ni>=0?'var(--green)':'var(--red)';
  document.getElementById('kpi-cash').textContent=f(F.cash);
  document.getElementById('qs-ar').textContent=f(F.ar);
  document.getElementById('qs-ap').textContent=f(F.ap);
  document.getElementById('qs-sc').textContent=DB.sales.length;
  document.getElementById('qs-pc').textContent=DB.purch.length;
  document.getElementById('qs-jec').textContent=DB.je.length;
  var mg=document.getElementById('qs-mg');
  if(F.totRev){var p=(F.ni/F.totRev*100).toFixed(1);mg.textContent=p+'%';mg.style.color=p>=0?'var(--green)':'var(--red)';}
  else mg.textContent='—';
  // Chart: use JE-derived monthly rev/exp for accuracy
  if(DB.sales.length||DB.purch.length){
    var mo={};
    DB.sales.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].r+=x.net;});
    DB.purch.forEach(function(x){var m=x.date?x.date.substring(0,7):'?';mo[m]=mo[m]||{r:0,e:0};mo[m].e+=x.net;});
    var ks=Object.keys(mo).sort().slice(-8),mv=Math.max.apply(null,ks.map(function(k){return Math.max(mo[k].r,mo[k].e);}));mv=Math.max(mv,1);
    var MN=['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    document.getElementById('chartBars').innerHTML=ks.map(function(k){var d=mo[k],rh=Math.max(4,d.r/mv*140),eh=Math.max(4,d.e/mv*140),ml=k.substring(5,7),mn=MN[parseInt(ml)-1]||ml;return '<div class="bar-wrap"><div style="display:flex;gap:3px;align-items:flex-end;height:140px;"><div class="bar" style="background:var(--green);height:'+rh+'px;width:14px;" title="'+f(d.r)+'"></div><div class="bar" style="background:var(--red);height:'+eh+'px;width:14px;" title="'+f(d.e)+'"></div></div><div class="bar-lbl">'+mn+'</div></div>';}).join('');
  } else {
    document.getElementById('chartBars').innerHTML='<div style="color:var(--text3);font-size:12px;align-self:center;margin:auto;font-family:\'DM Mono\',monospace;">Add transactions to see chart</div>';
  }
  var tmap={Sale:'bg',Purchase:'br',Collection:'bb',Payment:'by',Journal:'ba'};
  var all=[].concat(
    DB.sales.map(function(x){return{date:x.date,type:'Sale',desc:x.desc||'Sale',party:x.customer,amount:x.total,status:x.status};}),
    DB.purch.map(function(x){return{date:x.date,type:'Purchase',desc:x.desc||'Purchase',party:x.supplier,amount:x.total,status:x.status};}),
    DB.coll.map(function(x){return{date:x.date,type:'Collection',desc:'Cash received',party:x.customer,amount:x.amount,status:'received'};}),
    DB.pay.map(function(x){return{date:x.date,type:'Payment',desc:'Cash paid',party:x.supplier,amount:x.amount,status:'paid'};}),
    DB.je.filter(function(x){return !x.auto;}).map(function(x){return{date:x.date,type:'Journal',desc:x.desc,party:'Manual',amount:x.amount,status:'posted'};}))
    .sort(function(a,b){return b.date<a.date?-1:1;}).slice(0,10);
  var rb=document.getElementById('recentTx');
  if(!all.length){rb.innerHTML='<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:24px;">No transactions yet. Start by adding a sale or purchase.</td></tr>';return;}
  rb.innerHTML=all.map(function(t){return '<tr><td style="font-family:\'DM Mono\',monospace;font-size:11px;">'+t.date+'</td><td><span class="badge '+(tmap[t.type]||'bb')+'">'+t.type+'</span></td><td>'+t.desc+'</td><td style="color:var(--text3);">'+t.party+'</td><td class="amt pos">'+f(Math.abs(t.amount))+'</td><td>'+bdg(t.status)+'</td></tr>';}).join('');
}
function rSales(){
  var tot=DB.sales.reduce(function(a,x){return a+x.total;},0),coll=DB.coll.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('s-tot').textContent=f(tot);document.getElementById('s-coll').textContent=f(coll);document.getElementById('s-ar').textContent=f(Math.max(0,tot-coll));document.getElementById('s-cnt').textContent=DB.sales.length;
  var b=document.getElementById('salesTbl');
  if(!DB.sales.length){b.innerHTML='<tr><td colspan="10" style="text-align:center;color:var(--text3);padding:24px;">No sales invoices yet.</td></tr>';return;}
  b.innerHTML='';
  DB.sales.slice().sort(function(a,z){return z.id-a.id;}).forEach(function(s){
    var tr = document.createElement('tr');
    tr.style.cursor = 'pointer';
    tr.title = 'Click to view invoice';
    tr.onclick = function(e){
      if(e.target.tagName==='BUTTON') return;
      openInvoicePreview(s.id);
    };
    tr.innerHTML =
      '<td><span style="font-size:11px;color:var(--accent);font-family:monospace;">'+s.num+'</span></td>'+
      '<td>'+s.date+'</td>'+
      '<td style="font-weight:500;color:var(--text);">'+s.customer+'</td>'+
      '<td style="color:var(--text3);">'+(s.desc||'—')+'</td>'+
      '<td class="amt">'+s.vatRate+'%</td>'+
      '<td class="amt">'+f(s.net)+'</td>'+
      '<td class="amt" style="color:var(--text3);">'+f(s.vatAmt)+'</td>'+
      '<td class="amt pos">'+f(s.total)+'</td>'+
      '<td>'+bdg(s.status)+'</td>'+
      '<td><button class="btn btn-danger btn-sm" onclick="delS('+s.id+')">Del</button>'+
      ' <button class="btn btn-ghost btn-sm" onclick="openInvoicePreview('+s.id+')">📄</button></td>';
    b.appendChild(tr);
  });
}
function rPurch(){
  var tot=DB.purch.reduce(function(a,x){return a+x.total;},0),paid=DB.pay.reduce(function(a,x){return a+x.amount;},0);
  document.getElementById('p-tot').textContent=f(tot);document.getElementById('p-paid').textContent=f(paid);document.getElementById('p-ap').textContent=f(Math.max(0,tot-paid));document.getElementById('p-cnt').textContent=DB.purch.length;
  var b=document.getElementById('purchTbl');
  if(!DB.purch.length){b.innerHTML='<tr><td colspan="11" style="text-align:center;color:var(--text3);padding:24px;">No purchase invoices yet.</td></tr>';return;}
  b.innerHTML=DB.purch.slice().sort(function(a,c){return c.id-a.id;}).map(function(p){return '<tr><td><span style="font-family:\'DM Mono\',monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td><td>'+p.date+'</td><td>'+(p.invType==='asset'?'<span class="inv-type-badge inv-type-asset">🏗 Asset</span>':'<span class="inv-type-badge inv-type-expense">📋 Expense</span>')+'</td><td style="font-weight:500;color:var(--text);">'+p.supplier+'</td><td style="color:var(--text3);">'+(p.desc||'—')+'</td><td><span class="badge bb">'+p.cat+'</span></td><td class="amt">'+p.vatRate+'%</td><td class="amt">'+f(p.net)+'</td><td class="amt" style="color:var(--text3);">'+f(p.vatAmt)+'</td><td class="amt neg">'+f(p.total)+'</td><td>'+bdg(p.status)+'</td><td style="display:flex;gap:4px;">'+(p.invType==='asset'?'<button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();openDeprModal('+p.id+')">📉</button>':'')+'<button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();openEditPurch('+p.id+')">✏️</button><button class="btn btn-danger btn-sm" onclick="event.stopPropagation();delP('+p.id+')">Del</button></td></tr>';}).join('');
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

  // 2. Auto journal entry: Dr Cash / Cr AR (active plan)
  var _cpp = getActivePlan();
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Collection — ' + s.customer + ' / ' + s.num,
    lines: [
      {account:_cpp.cash, debit:amt, credit:0},
      {account:_cpp.ar,   debit:0,   credit:amt}
    ],
    amount: amt,
    auto: true,
    sourceType: 'collection'
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

  // 2. Auto journal entry: Dr AP / Cr Cash (active plan)
  var _payp = getActivePlan();
  DB.je.push({
    id: DB.ids.j++,
    date: dt,
    desc: 'Payment — ' + p.supplier + ' / ' + p.num,
    lines: [
      {account:_payp.ap,   debit:amt, credit:0},
      {account:_payp.cash, debit:0,   credit:amt}
    ],
    amount: amt,
    auto: true,
    sourceType: 'payment'
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
  var b = document.getElementById('jeTbl');

  // ── Apply drill-down filter if active ────────────────────────────────────
  var filterBar = document.getElementById('je-filter-bar');
  var visibleJE = DB.je;
  if(_jeFilter) {
    visibleJE = DB.je.filter(function(je){
      return je.lines.some(function(l){ return l.account === _jeFilter.account; });
    });
    if(filterBar) {
      filterBar.style.display = 'flex';
      document.getElementById('je-filter-label').textContent = _jeFilter.label;
      document.getElementById('je-filter-acc').textContent   = _jeFilter.account;
      document.getElementById('je-filter-count').textContent = visibleJE.length + ' entries';
    }
  } else {
    if(filterBar) filterBar.style.display = 'none';
  }

  if(!visibleJE.length){
    b.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:32px;">'+(
      _jeFilter ? 'No journal entries found for account '+_jeFilter.account+' — '+_jeFilter.label+'.'
                : 'No journal entries yet.'
    )+'</td></tr>';
    return;
  }

  var srcColors = {sale:'var(--green)',purchase:'var(--red)',collection:'var(--blue)',payment:'var(--yellow)',manual:'var(--purple)'};
  var srcLabels = {sale:'SALE',purchase:'PURCH',collection:'COLL',payment:'PAY',manual:'MANUAL'};

  b.innerHTML = '';
  var sorted = visibleJE.slice().sort(function(a,z){return z.id-a.id;});

  sorted.forEach(function(je){
    var stype  = je.sourceType || 'manual';
    var scolor = srcColors[stype] || 'var(--purple)';
    var slabel = srcLabels[stype] || 'MANUAL';

    // ── Header row: Entry#, Date, Type badge, Description, empty cols, Total, Del button ──
    var htr = document.createElement('tr');
    htr.className = 'je-header-row';

    // Col 1: Entry #
    var h1 = document.createElement('td');
    h1.style.cssText = 'font-size:11px;color:var(--purple);font-family:monospace;font-weight:700;padding:10px 12px 4px;';
    h1.textContent = 'JE-'+String(je.id).padStart(3,'0');

    // Col 2: Date
    var h2 = document.createElement('td');
    h2.style.cssText = 'font-size:12px;color:var(--text3);padding:10px 12px 4px;';
    h2.textContent = je.date;

    // Col 3: Type badge
    var h3 = document.createElement('td');
    h3.style.cssText = 'padding:10px 12px 4px;';
    var badge = document.createElement('span');
    badge.className = 'badge';
    badge.style.cssText = 'background:transparent;color:'+scolor+';border:1px solid '+scolor+';font-size:10px;';
    badge.textContent = slabel;
    h3.appendChild(badge);

    // Col 4: Description (spans conceptually)
    var h4 = document.createElement('td');
    h4.style.cssText = 'font-weight:600;color:var(--text);font-size:13px;padding:10px 12px 4px;';
    h4.textContent = je.desc;

    // Col 5: empty (acc code col)
    var h5 = document.createElement('td');
    h5.style.cssText = 'padding:4px;';

    // Col 6: Total debit (sum of all debits)
    var totalDr = je.lines.reduce(function(a,l){return a+(l.debit||0);},0);
    var h6 = document.createElement('td');
    h6.style.cssText = 'text-align:right;font-size:11px;color:var(--text3);padding:10px 12px 4px;font-family:monospace;';
    h6.textContent = totalDr > 0 ? f(totalDr) : '';

    // Col 7: Total credit
    var totalCr = je.lines.reduce(function(a,l){return a+(l.credit||0);},0);
    var h7 = document.createElement('td');
    h7.style.cssText = 'text-align:right;font-size:11px;color:var(--text3);padding:10px 12px 4px;font-family:monospace;';
    h7.textContent = totalCr > 0 ? f(totalCr) : '';

    // Col 8: Del button
    var h8 = document.createElement('td');
    h8.style.cssText = 'padding:10px 12px 4px;';
    var btn = document.createElement('button');
    btn.className = 'btn btn-danger btn-sm';
    btn.textContent = 'Del';
    btn.onclick = (function(jid){return function(){delJ(jid);};})(je.id);
    h8.appendChild(btn);

    [h1,h2,h3,h4,h5,h6,h7,h8].forEach(function(td){htr.appendChild(td);});
    b.appendChild(htr);

    // ── Line rows: one row per account line ───────────────────────────────
    je.lines.forEach(function(l, li){
      var acct = COA.find(function(ac){return ac.c===l.account;});
      var accName = acct ? acct.n : l.account;
      var accCode = l.account;
      var isDr = (l.debit||0) > 0;

      var ltr = document.createElement('tr');
      ltr.className = 'je-line-row';

      // Col 1: empty (entry # space)
      var l1 = document.createElement('td');
      l1.style.cssText = 'padding:5px 12px;border-left:3px solid '+(isDr?'var(--green)':'var(--red)')+';';

      // Col 2: empty (date space)
      var l2 = document.createElement('td');
      l2.style.cssText = 'padding:5px 12px;';

      // Col 3: empty (type space)
      var l3 = document.createElement('td');

      // Col 4: Account name (indented)
      var l4 = document.createElement('td');
      l4.style.cssText = 'padding:5px 12px;';
      l4.innerHTML = '<span class="je-acc-name">'+(isDr?'↳ Dr. ':'↳ Cr. ')+accName+'</span>';

      // Col 5: Account code
      var l5 = document.createElement('td');
      l5.style.cssText = 'padding:5px 12px;';
      l5.innerHTML = '<span class="je-acc-code">'+accCode+'</span>';

      // Col 6: Debit amount
      var l6 = document.createElement('td');
      l6.style.cssText = 'text-align:right;padding:5px 12px;';
      if(isDr){
        l6.innerHTML = '<span class="je-dr">'+f(l.debit)+'</span>';
      }

      // Col 7: Credit amount
      var l7 = document.createElement('td');
      l7.style.cssText = 'text-align:right;padding:5px 12px;';
      if(!isDr){
        l7.innerHTML = '<span class="je-cr">'+f(l.credit)+'</span>';
      }

      // Col 8: empty
      var l8 = document.createElement('td');

      [l1,l2,l3,l4,l5,l6,l7,l8].forEach(function(td){ltr.appendChild(td);});
      b.appendChild(ltr);
    });
  });
}

function plTab(m){plMode=m;document.getElementById('pl-det').classList.toggle('active',m==='detail');document.getElementById('pl-sum').classList.toggle('active',m==='summary');rPL();}
function rPL(){
  var F=cF(), b=document.getElementById('plBody'), gp=F.rev-F.cogs;
  var _pl = getActivePlan();
  var gmp = F.totRev ? (gp/F.totRev*100).toFixed(1) : 0;
  var npp = F.totRev ? (F.ni/F.totRev*100).toFixed(1) : 0;
  // Plan-aware COGS drill account
  var cogsDrill = _pl.cogsAccts ? _pl.cogsAccts[0] : (_pl.id==='pgc'?'600':'5000');
  var cogsLabel = _pl.labels ? _pl.labels.cogs : 'COGS – Direct Purchases';
  // Plan-aware revenue drill
  var revDrill  = _pl.revAccts ? _pl.revAccts[0] : (_pl.id==='pgc'?'705':'4000');
  var revLabel  = _pl.labels ? _pl.labels.revenue : 'Sales Revenue';

  if(plMode==='summary'){
    b.innerHTML=
      '<tr class="rh"><td colspan="2">Summary P&L</td></tr>'+
      '<tr class="rd"><td>Total Revenue</td><td class="num pos">'+f(F.totRev)+'</td></tr>'+
      '<tr class="rd"><td>Cost of Goods Sold</td><td class="num neg">('+f(F.cogs)+')</td></tr>'+
      '<tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num">'+f(gp)+'</td></tr>'+
      '<tr class="rd"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx)+')</td></tr>'+
      '<tr class="rs"><td>EBIT</td><td class="num">'+f(F.ebit)+'</td></tr>'+
      '<tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';
    return;
  }

  // ── Detailed mode ─────────────────────────────────────────────────────────
  var rows = '<tr class="rh"><td colspan="2">'+(_pl.id==='pgc'?'INGRESOS':'REVENUE')+'</td></tr>';

  // Revenue: one row per revenue account that has a balance
  _pl.revAccts.forEach(function(acc){
    var bal = F.revDetail ? (F.revDetail[acc]||0) : 0;
    // Fall back: compute from cF plBalances directly via the opex structure approach
    // We need per-account detail — get it from re-reading JEs
    if(!F.revDetail) bal = 0; // will be fixed below
  });
  // Since cF() doesn't expose per-rev-account detail, compute inline:
  var jes2 = DB.je.filter(function(x){ return inRange(x.date); });
  var accBals = {};
  jes2.forEach(function(je){ je.lines.forEach(function(l){
    if(!accBals[l.account]) accBals[l.account]={dr:0,cr:0};
    accBals[l.account].dr += (l.debit||0);
    accBals[l.account].cr += (l.credit||0);
  });});
  function accBal(acc) {
    var b2=accBals[acc]; if(!b2) return 0;
    var a=COA.find(function(x){return x.c===acc;});
    if(!a) return b2.dr-b2.cr;
    return a.t==='revenue' ? b2.cr-b2.dr : b2.dr-b2.cr;
  }

  var revTotal = 0;
  _pl.revAccts.forEach(function(acc){
    var bal = accBal(acc);
    if(bal === 0) return;
    var a = COA.find(function(x){return x.c===acc;});
    var name = a ? a.n : acc;
    revTotal += bal;
    rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+acc+'" data-label="'+name+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+name+' ↗</td><td class="num pos">'+f(bal)+'</td></tr>';
  });
  if(revTotal === 0) rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">No revenue recorded</td><td class="num">—</td></tr>';
  rows += '<tr class="rs"><td>'+(_pl.id==='pgc'?'Total Ingresos':'Total Revenue')+'</td><td class="num">'+f(F.totRev)+'</td></tr>';

  // ── COGS ─────────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">'+(_pl.id==='pgc'?'COMPRAS Y APROVISIONAMIENTOS':'COST OF GOODS SOLD')+'</td></tr>';
  var cogsTotal = 0;
  _pl.cogsAccts.forEach(function(acc){
    var bal = accBal(acc);
    if(bal === 0) return;
    var a = COA.find(function(x){return x.c===acc;});
    var name = a ? a.n : acc;
    cogsTotal += bal;
    rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+acc+'" data-label="'+name+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+name+' ↗</td><td class="num neg">('+f(bal)+')</td></tr>';
  });
  if(cogsTotal === 0) rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">'+(_pl.id==='pgc'?'Sin compras registradas':'No COGS recorded')+'</td><td class="num">—</td></tr>';
  rows += '<tr class="rs"><td>'+(_pl.id==='pgc'?'Margen bruto':'Gross Profit')+' <span style="font-size:11px;color:var(--text3);font-family:\'DM Mono\',monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num '+(gp>=0?'pos':'neg')+'">'+f(gp)+'</td></tr>';

  // ── OpEx ─────────────────────────────────────────────────────────────────
  rows += '<tr class="rh"><td colspan="2">'+(_pl.id==='pgc'?'GASTOS DE EXPLOTACIÓN':'OPERATING EXPENSES')+'</td></tr>';
  var opexTotal = 0;
  _pl.opexAccts.forEach(function(acc){
    var bal = accBal(acc);
    if(bal === 0) return;
    var a = COA.find(function(x){return x.c===acc;});
    var name = a ? a.n : acc;
    opexTotal += bal;
    rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+acc+'" data-label="'+name+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click">'+name+' ↗</td><td class="num neg">('+f(bal)+')</td></tr>';
  });
  if(opexTotal === 0) rows += '<tr class="rd"><td class="ind" style="color:var(--text3);">'+(_pl.id==='pgc'?'Sin gastos registrados':'No expenses recorded')+'</td><td class="num">—</td></tr>';
  rows += '<tr class="rs"><td>'+(_pl.id==='pgc'?'Total Gastos Explotación':'Total Operating Expenses')+'</td><td class="num neg">('+f(F.toOpEx)+')</td></tr>';
  rows += '<tr class="rs"><td>EBIT ('+(_pl.id==='pgc'?'Resultado Explotación':'Operating Income')+')</td><td class="num">'+f(F.ebit)+'</td></tr>';

  // ── Financial expenses ────────────────────────────────────────────────────
  if(F.finExp > 0) {
    rows += '<tr class="rh"><td colspan="2">'+(_pl.id==='pgc'?'GASTOS FINANCIEROS':'FINANCIAL EXPENSES')+'</td></tr>';
    if(_pl.finExpAccts) _pl.finExpAccts.forEach(function(acc){
      var bal = accBal(acc);
      if(bal === 0) return;
      var a = COA.find(function(x){return x.c===acc;});
      rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+acc+'" data-label="'+(a?a.n:acc)+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)">'+( a?a.n:acc)+' ↗</td><td class="num neg">('+f(bal)+')</td></tr>';
    });
  }

  rows += '<tr class="rt"><td>'+(_pl.id==='pgc'?'RESULTADO DEL EJERCICIO':'NET INCOME')+' <span style="font-size:11px;font-family:\'DM Mono\',monospace;opacity:.7;margin-left:8px;">'+npp+'% margen</span></td><td class="num">'+f(F.ni)+'</td></tr>';
  b.innerHTML = rows;
}
function rBS(){
  var F = cF();

  // ── ASSETS ────────────────────────────────────────────────────────────────
  // Cash = operating cash + JE cash movements
  var cash    = F.bsCash;
  var ar      = F.bsAR;
  var vatRec  = F.vatRec || 0;
  var tca     = cash + ar + vatRec;
  // Non-current assets — gross fixed + accumulated depreciation from ALL JEs
  var _bsp2 = getActivePlan();
  var grossFixed = 0, accumDepr = 0;
  DB.je.forEach(function(je){
    je.lines.forEach(function(l){
      var acc = String(l.account);
      var n   = parseInt(acc);
      var isFixed    = false;
      var isAccumDep = false;
      if(_bsp2.id === 'pgc') {
        isFixed    = (n >= 200 && n <= 221);
        isAccumDep = (n >= 280 && n <= 289) || (String(n).startsWith('28'));
      } else {
        isFixed    = (n >= 1500 && n <= 1570) && acc !== '1510';
        isAccumDep = (acc === '1510');
      }
      if(isFixed && !isAccumDep) grossFixed += (l.debit||0) - (l.credit||0);
      if(isAccumDep)             accumDepr  += (l.credit||0) - (l.debit||0);
    });
  });
  var fixedA = Math.max(0, grossFixed - accumDepr);
  var ta      = tca + (fixedA > 0 ? fixedA : 0);

  // ── LIABILITIES ───────────────────────────────────────────────────────────
  var ap      = F.bsAP;
  var accrued = F.jeAccrued;
  var vatRec2 = F.vatRec || 0;

  // In PGC: show 477 (IVA repercutido) and 472 (IVA soportado) independently
  // In US GAAP: show net VAT payable
  var vatp, vatNet, vatRepercutido, vatSoportado;
  if(_bsp2.id === 'pgc') {
    // 477 — HP IVA repercutido (liability, Cr balance)
    vatRepercutido = Math.max(0, F.vatP);   // F.vatP = sum of vatAccts = [477]
    // 472 — HP IVA soportado (asset, Dr balance) — already shown on asset side
    vatSoportado   = vatRec2;               // already in vatRec
    vatp   = vatRepercutido;
    vatNet = vatp;  // Show gross, not net — they are separate accounts
  } else {
    vatp   = Math.max(0, F.vatP);
    vatNet = vatp - vatRec2;
  }

  var tcl     = ap + Math.max(0, vatNet) + accrued;
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
  var _bsp = getActivePlan();
  aRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+_bsp.cashAccts[0]+'" data-label="'+_bsp.labels.cash+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+_bsp.labels.cash+' ↗</td><td class="num">'+f(cash)+'</td></tr>';
  aRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+_bsp.arAccts[0]+'" data-label="'+_bsp.labels.ar+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+_bsp.labels.ar+' ↗</td><td class="num">'+f(ar)+'</td></tr>';
  if(vatRec > 0) {
    var vatRecLabel = _bsp.id==='pgc' ? 'HP IVA soportado (472)' : 'VAT Recoverable';
    aRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+(
      _bsp.id==='pgc'?'472':'2100'
    )+'" data-label="'+vatRecLabel+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+vatRecLabel+' ↗</td><td class="num pos">'+f(vatRec)+'</td></tr>';
  }
  aRows += '<tr class="rs"><td>Total Current Assets</td><td class="num">'+f(tca)+'</td></tr>';
  aRows += '<tr class="rh"><td colspan="2">Non-Current Assets</td></tr>';
  if(fixedA > 0){
    aRows += '<tr class="rd"><td class="ind">Fixed Assets — Gross: '+f(grossFixed)+'</td><td class="num">'+f(grossFixed)+'</td></tr>';
    aRows += '<tr class="rd"><td class="ind" style="color:var(--red);">&nbsp;&nbsp;&nbsp;Accumulated Depreciation</td><td class="num" style="color:var(--red);">('+f(accumDepr)+')</td></tr>';
    aRows += '<tr class="rs"><td>Net Book Value (Non-Current Assets)</td><td class="num">'+f(fixedA)+'</td></tr>';
  } else {
    aRows += '<tr class="rd"><td class="ind" style="color:var(--text3);">None recorded — create a Purchase of type Asset</td><td class="num">—</td></tr>';
  }
  aRows += '<tr class="rt"><td>TOTAL ASSETS</td><td class="num">'+f(ta)+'</td></tr>';

  // ── LIABILITIES & EQUITY SIDE ─────────────────────────────────────────────
  var lRows = '<tr class="rh"><td colspan="2">Current Liabilities</td></tr>';
  lRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+_bsp.apAccts[0]+'" data-label="'+_bsp.labels.ap+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+_bsp.labels.ap+' ↗</td><td class="num">'+f(ap)+'</td></tr>';
  // VAT liabilities
  if(_bsp.id === 'pgc') {
    // PGC: show 477 IVA repercutido independently (it's separate from 472 on asset side)
    if(vatRepercutido > 0) {
      lRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="477" data-label="HP, IVA repercutido (477)" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">HP, IVA repercutido (477) ↗</td><td class="num">'+f(vatRepercutido)+'</td></tr>';
    }
  } else {
    // US GAAP: show net VAT payable
    if(Math.max(0, vatNet) > 0) {
      lRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="'+_bsp.vatAccts[0]+'" data-label="'+_bsp.labels.vat+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">'+_bsp.labels.vat+' (net) ↗</td><td class="num">'+f(Math.max(0,vatNet))+'</td></tr>';
    }
  }
  if(accrued !== 0) lRows += '<tr class="rd"><td class="ind">Accrued Liabilities</td><td class="num">'+f(accrued)+'</td></tr>';
  lRows += '<tr class="rs"><td>Total Current Liabilities</td><td class="num">'+f(tcl)+'</td></tr>';
  lRows += '<tr class="rh"><td colspan="2">Non-Current Liabilities</td></tr>';
  if(ltDebt > 0){
    lRows += '<tr class="rd"><td class="ind drilldown-link" data-drill="2500" data-label="Long-term Debt" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click to see Journal Entries">Long-term Debt ↗</td><td class="num">'+f(ltDebt)+'</td></tr>';
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
  rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="1100" data-label="Cash received from customers" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">Cash received from customers ↗</td><td class="num pos">'+f(F.totColl)+'</td></tr>';
  rows += '<tr class="rd"><td class="ind drilldown-link" data-drill="2000" data-label="Cash paid to suppliers" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">Cash paid to suppliers ↗</td><td class="num '+(F.totPay>0?'neg':'')+'">'+(F.totPay>0?'('+f(F.totPay)+')':f(0))+'</td></tr>';
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
var _ctReturnTarget = null; // 's-cust' | 'p-sup' | null
var _ctTab    = 'basic';

function setCtFilter(f) {
  _ctFilter = f;
  ['all','client','supplier','both'].forEach(function(x){
    var el = document.getElementById('ctf-'+x);
    if(el) el.classList.toggle('active', x===f);
  });
  rContacts();
}

function openContactModal(type, id, returnTarget) {
  // Use String comparison — works for both legacy int IDs and new string UIDs
  var _sid = (id !== undefined && id !== null && id !== '') ? String(id) : null;
  _ctEditId = _sid;
  _ctReturnTarget = returnTarget || null;
  _ctTab    = 'basic';

  // Always get type from DB when editing
  if(_sid) {
    var _existCt = DB.contacts.find(function(x){ return String(x.id) === _sid; });
    _ctType = _existCt ? (_existCt.type || 'client') : (type || 'client');
  } else {
    _ctType = type || 'client';
  }

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

  if(_sid) {
    var ct = DB.contacts.find(function(x){ return String(x.id) === _sid; });
    if(!ct) { showToast('⚠️ Contact not found (ID: '+_sid+')'); return; }
    document.getElementById('ct-modal-title').textContent = 'Edit Contact';
    if(deleteBtn) deleteBtn.style.display = 'inline-flex';
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
    document.getElementById('ct-salestax').value   = ct.salestax||'IVA21';
    document.getElementById('ct-purchtax').value   = ct.purchtax||'IVA21';
    document.getElementById('ct-acccode').value    = ct.acccode||'';
    buildCtAccSelects(ct.debtacc||'', ct.credacc||'');
  } else {
    document.getElementById('ct-modal-title').textContent = 'New Contact';
    if(deleteBtn) deleteBtn.style.display = 'none';
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
    document.getElementById('ct-salestax').value  = 'IVA21';
    document.getElementById('ct-purchtax').value  = 'IVA21';
    buildCtAccSelects('', '');
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

// ══════════════════════════════════════════════════════════════════
// SUBCUENTA CORRELATIVA — Contact Accounting Tab
// ══════════════════════════════════════════════════════════════════

// Base accounts that support auto-subcuenta per active plan
function getSubcuentaBases() {
  var plan = getActivePlan();
  if (plan.id === 'pgc') {
    return {
      debt: [
        { base:'430', name:'Clientes',                          digits:8 },
        { base:'431', name:'Clientes, efectos comerciales',     digits:8 }
      ],
      cred: [
        { base:'400', name:'Proveedores',                       digits:8 },
        { base:'410', name:'Acreedores por prestaciones',       digits:8 }
      ]
    };
  } else {
    // US GAAP
    return {
      debt: [
        { base:'1100', name:'Accounts Receivable', digits:8 }
      ],
      cred: [
        { base:'2000', name:'Accounts Payable',    digits:8 }
      ]
    };
  }
}

// Build the next subcuenta number for a given base (e.g. '430' → '43000001')
function getNextSubcuenta(base, digits) {
  // Init counter in DB.ids if not present
  var key = 'sub_' + base;
  if (!DB.ids[key]) DB.ids[key] = 1;
  var seq  = DB.ids[key];
  // Pad: base + zeros to fill up to `digits` total length
  var padLen = digits - base.length;
  return base + String(seq).padStart(padLen, '0');
}

// Peek (don't consume) next subcuenta for preview display
function peekNextSubcuenta(base, digits) {
  var key = 'sub_' + base;
  var seq  = (DB.ids[key] || 1);
  var padLen = digits - base.length;
  return base + String(seq).padStart(padLen, '0');
}

// Consume next subcuenta (increment counter)
function consumeSubcuenta(base) {
  var key = 'sub_' + base;
  if (!DB.ids[key]) DB.ids[key] = 1;
  return DB.ids[key]++;
}

// Populate ct-debtacc and ct-credacc selects dynamically
function buildCtAccSelects(currentDebt, currentCred) {
  var bases = getSubcuentaBases();
  var plan  = getActivePlan();

  function buildOpts(bList, dir, currentVal) {
    var html = '<option value="">— Select account —</option>';
    // Existing assigned subcuentas from all contacts for this dir
    var usedKey = dir === 'debt' ? 'debtacc' : 'credacc';
    var usedCodes = DB.contacts
      .filter(function(c){ return c[usedKey] && c[usedKey] !== ''; })
      .map(function(c){ return c[usedKey]; });

    bList.forEach(function(b) {
      // Option group header
      html += '<optgroup label="' + b.base + ' — ' + b.name + '">';
      // ✦ NEW subcuenta option
      var next = peekNextSubcuenta(b.base, b.digits);
      html += '<option value="__new__' + b.base + '__' + b.digits + '">' +
              '✦ Nueva subcuenta → ' + next + ' (' + b.name + ')</option>';
      // Already assigned subcuentas for this base
      usedCodes
        .filter(function(code){ return code.startsWith(b.base) && code.length === b.digits; })
        .sort()
        .forEach(function(code){
          var ct = DB.contacts.find(function(x){ return x[usedKey] === code; });
          var label = ct ? ct.name : '';
          html += '<option value="' + code + '">' + code + ' — ' + (label||'(assigned)') + '</option>';
        });
      // The base account itself as a manual fallback
      html += '<option value="' + b.base + '">' + b.base + ' — ' + b.name + ' (cuenta general)</option>';
      html += '</optgroup>';
    });

    // For PGC also show the general COA accounts that aren't in the bases
    var planAccs = plan.id === 'pgc'
      ? (dir === 'debt'
          ? [{c:'460',n:'Anticipos de remuneraciones'},{c:'431',n:'Clientes, efectos a cobrar'}]
          : [{c:'475',n:'HP acreedora por conceptos fiscales'},{c:'476',n:'Organismos SS, acreedores'}])
      : [];

    return html;
  }

  var dSel = document.getElementById('ct-debtacc');
  var cSel = document.getElementById('ct-credacc');
  if (!dSel || !cSel) return;

  dSel.innerHTML = buildOpts(bases.debt, 'debt', currentDebt);
  cSel.innerHTML = buildOpts(bases.cred, 'cred', currentCred);

  // Restore saved values if editing
  if (currentDebt) {
    // Check if it matches a real option
    var found = Array.from(dSel.options).some(function(o){ return o.value === currentDebt; });
    if (found) dSel.value = currentDebt;
    updateCtAccPreview('debt', currentDebt);
  }
  if (currentCred) {
    var found2 = Array.from(cSel.options).some(function(o){ return o.value === currentCred; });
    if (found2) cSel.value = currentCred;
    updateCtAccPreview('cred', currentCred);
  }
}

// Handle select change — if "__new__" chosen, show preview but don't consume yet
function onCtAccChange(dir, val) {
  updateCtAccPreview(dir, val);
}

function updateCtAccPreview(dir, val) {
  var previewEl = document.getElementById('ct-' + (dir==='debt'?'debtacc':'credacc') + '-preview');
  if (!previewEl) return;

  if (!val || val === '') {
    previewEl.textContent = '';
    return;
  }
  if (val.startsWith('__new__')) {
    var parts   = val.split('__');  // ['', 'new', base, digits, '']
    var base    = parts[2];
    var digits  = parseInt(parts[3]);
    var preview = peekNextSubcuenta(base, digits);
    previewEl.innerHTML = '→ Se asignará: <strong>' + preview + '</strong> (próximo número correlativo)';
  } else {
    previewEl.textContent = '✓ Cuenta: ' + val;
  }
}

// Called on saveContact to resolve __new__ values → real subcuenta numbers
function resolveCtAccCode(val) {
  if (!val || !val.startsWith('__new__')) return val || '';
  var parts  = val.split('__');
  var base   = parts[2];
  var digits = parseInt(parts[3]);
  // Consume next number
  consumeSubcuenta(base);
  return peekNextSubcuenta(base, digits);  // peekNextSubcuenta reflects state BEFORE increment
}

// ── Patch resolveCtAccCode to use BEFORE incrementing ─────────────
// Re-define so we consume and return the correct value
function resolveCtAccCode(val) {
  if (!val || !val.startsWith('__new__')) return val || '';
  var parts  = val.split('__');
  var base   = parts[2];
  var digits = parseInt(parts[3]);
  var key    = 'sub_' + base;
  if (!DB.ids[key]) DB.ids[key] = 1;
  var seq    = DB.ids[key];
  DB.ids[key]++;   // consume
  var padLen = digits - base.length;
  return base + String(seq).padStart(padLen, '0');
}

function saveContact() {
  var name = document.getElementById('ct-name').value.trim();
  if(!name){ alert('Please enter a contact name.'); return; }

  // Determine if editing or creating
  var isEdit = (_ctEditId !== null && _ctEditId !== undefined);
  var existingCt = isEdit ? DB.contacts.find(function(x){ return String(x.id) === String(_ctEditId); }) : null;

  var ct = {
    id:          isEdit ? _ctEditId : ('CT' + Date.now() + (DB.ids.ct++)),
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
    debtacc:     resolveCtAccCode(document.getElementById('ct-debtacc').value),
    credacc:     resolveCtAccCode(document.getElementById('ct-credacc').value),
    salestax:    document.getElementById('ct-salestax').value,
    purchtax:    document.getElementById('ct-purchtax').value,
    acccode:     document.getElementById('ct-acccode').value,
    createdAt:   existingCt ? existingCt.createdAt : new Date().toISOString().slice(0,10)
  };

  if(isEdit) {
    var idx2 = DB.contacts.findIndex(function(x){ return String(x.id) === String(_ctEditId); });
    if(idx2 >= 0) DB.contacts[idx2] = ct; else DB.contacts.push(ct);
  } else {
    DB.contacts.push(ct);
  }

  sv();
  rContacts();
  closeOverlay('ov-contact');
  showToast('✅ Contact saved: ' + name);

  // If opened from Sales/Purchases: fill the name field (parent overlay stays open)
  if(_ctReturnTarget) {
    var tgt = _ctReturnTarget;
    _ctReturnTarget = null;
    var fld = document.getElementById(tgt);
    if(fld) fld.value = name;
    // VAT autofill
    if(tgt === 's-cust') {
      var vs = document.getElementById('s-vat');
      if(vs && ct.salesvat) vs.value = ct.salesvat;
      if(typeof calcS==='function') calcS();
    }
    if(tgt === 'p-sup') {
      var vp = document.getElementById('p-vat');
      if(vp && ct.purchvat) vp.value = ct.purchvat;
      if(typeof calcP==='function') calcP();
    }
  }
}

function deleteContact() {
  if(_ctEditId === null || _ctEditId === undefined) return;
  var _dSid = String(_ctEditId);
  var ct = DB.contacts.find(function(x){ return String(x.id) === _dSid; });
  if(!confirm('Delete contact: ' + (ct?ct.name:'') + '?')) return;
  DB.contacts = DB.contacts.filter(function(x){ return String(x.id) !== _dSid; });
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
    return '<div class="contact-card" onclick="openContactModal(null,\''+String(ct.id)+'\')">' +
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
    return '<div class="autocomplete-item" onmousedown="acSelect(\''+inputId+'\',\''+listId+'\',\''+ct.name.replace(/'/g,"\\'")+'\',\''+ct.id+'\')">' +
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
  var ct = DB.contacts.find(function(x){ return String(x.id) === String(ctId); });
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


// ══════════════════════════════════════════════════════════════════
// INVOICE PREVIEW & PDF
// ══════════════════════════════════════════════════════════════════

var _invSaleId = null;

function addDays(dateStr, days) {
  var d = new Date(dateStr);
  d.setDate(d.getDate() + days);
  return d.toISOString().split('T')[0];
}

function fmtDate(dateStr) {
  if(!dateStr) return '—';
  var p = dateStr.split('-');
  if(p.length === 3) return p[2]+'/'+p[1]+'/'+p[0];
  return dateStr;
}

function openInvoicePreview(saleId) {
  _invSaleId = saleId;
  var s = DB.sales.find(function(x){return x.id===saleId;});
  if(!s) return;

  // Find contact details
  var contact = DB.contacts.find(function(ct){
    return ct.name && ct.name.toLowerCase() === (s.customer||'').toLowerCase();
  });

  // Toolbar
  document.getElementById('inv-toolbar-num').textContent = s.num;
  var tb = document.getElementById('inv-toolbar-status');
  tb.innerHTML = bdg(s.status);

  // Company header
  document.getElementById('inv-co-name').textContent = DB.co.name || 'My Company Ltd.';
  var coDetails = [];
  if(DB.co.addr)  coDetails.push(DB.co.addr);
  if(DB.co.taxid) coDetails.push('VAT: ' + DB.co.taxid);
  if(DB.user.email) coDetails.push(DB.user.email);
  if(DB.user.phone) coDetails.push(DB.user.phone);
  document.getElementById('inv-co-details').innerHTML = coDetails.join('<br>');

  // Invoice number
  document.getElementById('inv-num').textContent = s.num;

  // Customer
  document.getElementById('inv-customer').textContent = s.customer || '—';
  var custDetail = [];
  if(contact) {
    if(contact.nif)      custDetail.push('NIF: ' + contact.nif);
    if(contact.addr)     custDetail.push(contact.addr);
    if(contact.city)     custDetail.push([contact.postal, contact.city, contact.country].filter(Boolean).join(', '));
    if(contact.email)    custDetail.push(contact.email);
  }
  document.getElementById('inv-customer-detail').innerHTML = custDetail.join('<br>') || '';

  // Dates
  document.getElementById('inv-date').textContent = fmtDate(s.date);
  // Due date: payment terms from contact or default 30 days
  var termDays = 30;
  if(contact && contact.payterms) {
    var match = contact.payterms.match(/\d+/);
    if(match) termDays = parseInt(match[0]);
    if(contact.payterms === 'immediate') termDays = 0;
  }
  document.getElementById('inv-due').textContent = fmtDate(addDays(s.date || td(), termDays));

  // Line items
  var tbody = document.getElementById('inv-lines');
  tbody.innerHTML =
    '<tr>' +
    '<td>'+(s.desc || 'Services')+'</td>' +
    '<td style="text-align:right;">1</td>' +
    '<td style="text-align:right;">'+f(s.net)+'</td>' +
    '<td style="text-align:right;">'+s.vatRate+'%</td>' +
    '<td style="text-align:right;font-weight:700;">'+f(s.net)+'</td>' +
    '</tr>';

  // Totals footer
  var tfoot = document.getElementById('inv-tfoot');
  tfoot.innerHTML =
    '<tr><td colspan="4" style="text-align:right;color:#666;">Subtotal</td><td style="text-align:right;font-weight:600;">'+f(s.net)+'</td></tr>' +
    '<tr><td colspan="4" style="text-align:right;color:#666;">VAT ('+s.vatRate+'%)</td><td style="text-align:right;font-weight:600;">'+f(s.vatAmt)+'</td></tr>' +
    '<tr class="inv-total-row"><td colspan="4" style="text-align:right;">TOTAL</td><td style="text-align:right;">'+f(s.total)+'</td></tr>';

  // Notes / footer
  var notes = s.notes || DB.prefs.invnotes || '';
  document.getElementById('inv-notes').textContent = notes;

  // Status badge
  var statusMap = {paid:'paid',pending:'pending',partial:'partial'};
  var stClass = statusMap[s.status] || 'pending';
  var stLabel = {paid:'✓ Paid',pending:'⏳ Payment Pending',partial:'◑ Partially Paid'}[s.status] || s.status;
  document.getElementById('inv-status-badge').innerHTML =
    '<span class="inv-footer-status '+stClass+'">'+stLabel+'</span>';

  openOverlay('ov-invoice');
}

function printInvoice() {
  window.print();
}

function downloadInvoicePDF() {
  // Use print dialog with PDF option
  var s = DB.sales.find(function(x){return x.id===_invSaleId;});
  var oldTitle = document.title;
  document.title = 'Invoice_' + (s ? s.num : 'INV') + '_' + (s ? s.customer : '') + '.pdf';
  window.print();
  document.title = oldTitle;
}

function editInvoice() {
  var s = DB.sales.find(function(x){return x.id===_invSaleId;});
  if(!s) return;
  document.getElementById('ie-date').value     = s.date || '';
  document.getElementById('ie-num').value      = s.num  || '';
  document.getElementById('ie-customer').value = s.customer || '';
  document.getElementById('ie-desc').value     = s.desc || '';
  document.getElementById('ie-net').value      = s.net || '';
  document.getElementById('ie-vat').value      = s.vatRate || '21';
  document.getElementById('ie-vatamt').value   = s.vatAmt ? s.vatAmt.toFixed(2) : '';
  document.getElementById('ie-total').value    = s.total ? s.total.toFixed(2) : '';
  document.getElementById('ie-status').value   = s.status || 'pending';
  document.getElementById('ie-method').value   = s.method || 'bank';
  document.getElementById('ie-notes').value    = s.notes || '';
  calcIE();
  openOverlay('ov-invoice-edit');
}

function calcIE() {
  var n = parseFloat(document.getElementById('ie-net').value)||0;
  var v = parseFloat(document.getElementById('ie-vat').value)||0;
  var va = n*v/100;
  document.getElementById('ie-vatamt').value = va.toFixed(2);
  document.getElementById('ie-total').value  = (n+va).toFixed(2);
}

function saveEditedInvoice() {
  var s = DB.sales.find(function(x){return x.id===_invSaleId;});
  if(!s) return;
  var net = parseFloat(document.getElementById('ie-net').value)||0;
  var vat = parseFloat(document.getElementById('ie-vat').value)||0;
  var va  = net*vat/100;
  s.date     = document.getElementById('ie-date').value;
  s.num      = document.getElementById('ie-num').value;
  s.customer = document.getElementById('ie-customer').value;
  s.desc     = document.getElementById('ie-desc').value;
  s.net      = net;
  s.vatRate  = vat;
  s.vatAmt   = va;
  s.total    = net + va;
  s.status   = document.getElementById('ie-status').value;
  s.method   = document.getElementById('ie-method').value;
  s.notes    = document.getElementById('ie-notes').value;
  sv();
  closeOverlay('ov-invoice-edit');
  openInvoicePreview(_invSaleId); // Refresh preview
  renderAll();
  showToast('✅ Invoice updated: ' + s.num);
}


// ══════════════════════════════════════════════════════════════════
// RECURRING INVOICES MODULE
// ══════════════════════════════════════════════════════════════════

var _salesTab = 'invoices';

function setSalesTab(tab) {
  _salesTab = tab;
  document.getElementById('stab-invoices').classList.toggle('active', tab==='invoices');
  document.getElementById('stab-recurring').classList.toggle('active', tab==='recurring');
  document.getElementById('sales-view-invoices').style.display  = tab==='invoices'  ? '' : 'none';
  document.getElementById('sales-view-recurring').style.display = tab==='recurring' ? '' : 'none';
  var newBtn = document.getElementById('sales-new-btn');
  if(newBtn) newBtn.textContent = tab==='invoices' ? '+ New Invoice' : '+ New Recurring';
  if(newBtn) newBtn.onclick = tab==='invoices'
    ? function(){ openOverlay('ov-sale'); }
    : function(){ openNewRecurring(); };
}

function toggleConvertMenu() {
  var m = document.getElementById('convert-menu');
  m.style.display = m.style.display==='none' ? 'block' : 'none';
  document.addEventListener('click', function closeMenu(e){
    if(!e.target.closest('#convert-btn') && !e.target.closest('#convert-menu')){
      m.style.display='none';
      document.removeEventListener('click', closeMenu);
    }
  });
}

// Interval display labels
var intervalLabels = {
  daily:'Daily', weekly:'Weekly', biweekly:'Biweekly',
  monthly:'Monthly', bimonthly:'Every 2 months',
  quarterly:'Quarterly', biannual:'Every 6 months', annually:'Annually'
};

// Days to add per interval
var intervalDays = {
  daily:1, weekly:7, biweekly:14, monthly:30,
  bimonthly:60, quarterly:90, biannual:180, annually:365
};

function addIntervalDays(dateStr, interval) {
  var d = new Date(dateStr);
  var days = intervalDays[interval] || 30;
  d.setDate(d.getDate() + days);
  return d.toISOString().split('T')[0];
}

function convertToRecurring() {
  document.getElementById('convert-menu').style.display = 'none';
  var s = DB.sales.find(function(x){return x.id===_invSaleId;});
  if(!s) return;
  // Pre-fill modal
  document.getElementById('rc-source-label').textContent = 'Based on: ' + s.num;
  document.getElementById('rc-source-preview').textContent =
    s.customer + ' — ' + (s.desc||'') + ' — ' + f(s.total) + ' (VAT ' + s.vatRate + '%)';
  document.getElementById('rc-interval').value = 'monthly';
  document.getElementById('rc-duedays').value  = '30';
  document.getElementById('rc-start').value    = td();
  document.getElementById('rc-end').value      = '';
  document.getElementById('rc-method').value   = s.method || 'bank';
  document.getElementById('rc-notes').value    = s.desc || '';
  // Store source sale id
  document.getElementById('ov-recurring').dataset.sourceId = s.id;
  openOverlay('ov-recurring');
}

function openNewRecurring() {
  document.getElementById('rc-source-label').textContent = 'New recurring — fill in source details below';
  document.getElementById('rc-source-preview').textContent = 'Not linked to an existing invoice';
  document.getElementById('rc-interval').value = 'monthly';
  document.getElementById('rc-duedays').value  = '30';
  document.getElementById('rc-start').value    = td();
  document.getElementById('rc-end').value      = '';
  document.getElementById('rc-method').value   = 'bank';
  document.getElementById('rc-notes').value    = '';
  document.getElementById('ov-recurring').dataset.sourceId = '';
  openOverlay('ov-recurring');
}

function saveRecurring() {
  var sourceId = parseInt(document.getElementById('ov-recurring').dataset.sourceId)||null;
  var s = sourceId ? DB.sales.find(function(x){return x.id===sourceId;}) : null;
  if(!s && !sourceId) {
    alert('Please select an invoice first, then use Convert → Recurring Invoice.');
    return;
  }
  var interval = document.getElementById('rc-interval').value;
  var start    = document.getElementById('rc-start').value || td();
  var end      = document.getElementById('rc-end').value || null;
  var duedays  = parseInt(document.getElementById('rc-duedays').value)||30;
  var method   = document.getElementById('rc-method').value;
  var notes    = document.getElementById('rc-notes').value;

  var rc = {
    id:        DB.ids.rc++,
    sourceId:  sourceId,
    customer:  s ? s.customer : '',
    desc:      s ? (s.desc||'') : notes,
    net:       s ? s.net : 0,
    vatRate:   s ? s.vatRate : 21,
    vatAmt:    s ? s.vatAmt : 0,
    total:     s ? s.total : 0,
    interval:  interval,
    duedays:   duedays,
    startDate: start,
    endDate:   end,
    nextDate:  start,
    method:    method,
    notes:     notes,
    status:    'active',
    createdAt: td(),
    generated: 0  // count of invoices generated
  };

  if(!DB.recurring) DB.recurring = [];
  DB.recurring.push(rc);

  // Run immediately if start is today or past
  processRecurringInvoices();
  sv();
  closeOverlay('ov-recurring');
  closeOverlay('ov-invoice');
  setSalesTab('recurring');
  renderAll();
  showToast('✅ Recurring invoice activated — ' + intervalLabels[interval] + ' from ' + fmtDate(start));
}

function processRecurringInvoices() {
  if(!DB.recurring) return;
  var today = td();
  var generated = 0;
  DB.recurring.forEach(function(rc){
    if(rc.status !== 'active') return;
    // Respect autoCreate toggle (default true)
    if(rc.autoCreate === false) return;
    if(rc.endDate && rc.nextDate > rc.endDate) {
      rc.status = 'ended';
      return;
    }
    // Generate all due invoices up to today
    while(rc.nextDate <= today){
      if(rc.endDate && rc.nextDate > rc.endDate) { rc.status='ended'; break; }
      // Create invoice
      var pfx = DB.prefs.invpfx || 'INV-';
      var num = pfx + String(DB.ids.s).padStart(3,'0');
      var dueDate = addDays(rc.nextDate, rc.duedays);
      var rec = {
        id: DB.ids.s++, date: rc.nextDate, num: num,
        customer: rc.customer, desc: rc.desc,
        vatRate: rc.vatRate, net: rc.net, vatAmt: rc.vatAmt,
        total: rc.total, status: 'pending', method: rc.method,
        notes: rc.notes, recurringId: rc.id, dueDate: dueDate
      };
      DB.sales.push(rec);
      // Auto JE
      var _rcp = getActivePlan();
      var saleLines = [
        {account:_rcp.ar, debit:rec.total, credit:0},
        {account:_rcp.revenue, debit:0, credit:rc.net}
      ];
      if(rc.vatAmt > 0) saleLines.push({account:_rcp.vatIn, debit:0, credit:rc.vatAmt});
      DB.je.push({id:DB.ids.j++, date:rc.nextDate, desc:'Sale (Recurring) — '+rc.customer+' / '+num,
        lines:saleLines, amount:rec.total, auto:true, sourceType:'sale', sourceId:rec.id});
      rc.generated++;
      rc.nextDate = addIntervalDays(rc.nextDate, rc.interval);
      generated++;
      // Safety: max 12 iterations per run to avoid infinite loop
      if(rc.generated > 1200) break;
    }
  });
  return generated;
}

function pauseRecurring(rcId) {
  var rc = DB.recurring.find(function(x){return x.id===rcId;});
  if(!rc) return;
  rc.status = rc.status==='active' ? 'paused' : 'active';
  sv(); rRecurring();
  showToast(rc.status==='active' ? '▶ Recurring resumed' : '⏸ Recurring paused');
}

function stopRecurring(rcId) {
  if(!confirm('Stop this recurring invoice? No more invoices will be generated.')) return;
  var rc = DB.recurring.find(function(x){return x.id===rcId;});
  if(rc) { rc.status='ended'; rc.endDate=td(); }
  sv(); closeRCPanel(); rRecurring();
  showToast('⏹ Recurring stopped');
}

var _rcPanelId = null;

function rRecurring() {
  if(!DB.recurring) DB.recurring = [];
  var tbl      = document.getElementById('recurringTbl');
  var badge    = document.getElementById('rc-count-badge');
  var activeEl = document.getElementById('rc-active');
  var pausedEl = document.getElementById('rc-paused');
  var totalEl  = document.getElementById('rc-total');
  var mrrEl    = document.getElementById('rc-mrr');

  var active = DB.recurring.filter(function(r){return r.status==='active';}).length;
  var paused = DB.recurring.filter(function(r){return r.status==='paused';}).length;
  var mrr    = DB.recurring.filter(function(r){return r.status==='active';}).reduce(function(a,r){
    var factor = {daily:30,weekly:4.33,biweekly:2.17,monthly:1,bimonthly:.5,quarterly:.33,biannual:.17,annually:.083};
    return a + r.total*(factor[r.interval]||1);
  },0);

  if(badge)    badge.textContent  = DB.recurring.length || '';
  if(activeEl) activeEl.textContent = active;
  if(pausedEl) pausedEl.textContent = paused;
  if(totalEl)  totalEl.textContent  = DB.recurring.length;
  if(mrrEl)    mrrEl.textContent    = f(mrr);

  if(!tbl) return;
  if(!DB.recurring.length){
    tbl.innerHTML='<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:32px;">No recurring invoices yet. Open any invoice and click ⇄ Convert → Recurring Invoice.</td></tr>';
    return;
  }

  tbl.innerHTML='';
  var stColors = {active:'var(--green)',paused:'var(--yellow)',ended:'var(--text3)'};
  var stLabels = {active:'Up to date',paused:'Paused',ended:'Finished'};

  DB.recurring.slice().sort(function(a,b){
    // Sort: active first, then by customer name
    if(a.status===b.status) return (a.customer||'').localeCompare(b.customer||'');
    return a.status==='active'?-1:b.status==='active'?1:0;
  }).forEach(function(rc){
    var stColor = stColors[rc.status]||'var(--text3)';
    var stLabel = stLabels[rc.status]||rc.status;
    var isSelected = _rcPanelId === rc.id;

    var tr = document.createElement('tr');
    tr.style.cssText = 'cursor:pointer;transition:background .1s;'+(isSelected?'background:var(--surface2);':'');
    tr.onclick = function(){ openRCPanel(rc.id); };
    tr.onmouseover = function(){ if(!isSelected) this.style.background='var(--surface2)'; };
    tr.onmouseout  = function(){ if(!isSelected) this.style.background=''; };

    var initials = (rc.customer||'?').split(' ').map(function(w){return w[0]||'';}).slice(0,2).join('').toUpperCase();

    // Count converted invoices for this recurring
    var converted = DB.sales.filter(function(s){return s.recurringId===rc.id;}).length;

    var td = function(content, style) {
      var t = document.createElement('td');
      t.style.cssText = 'padding:11px 12px;border-bottom:1px solid var(--border);' + (style||'');
      t.innerHTML = content;
      return t;
    };

    tr.appendChild(td(
      '<div style="display:flex;align-items:center;gap:8px;">' +
      '<div style="width:30px;height:30px;border-radius:50%;background:var(--teal,#0E9AA7);display:flex;align-items:center;justify-content:center;font-weight:700;color:#fff;font-size:11px;flex-shrink:0;">'+initials+'</div>'+
      '<div><div style="font-size:13px;font-weight:600;color:var(--text);">'+rc.customer+'</div></div></div>'
    ));
    tr.appendChild(td('<span class="recur-badge active" style="font-size:10px;">'+intervalLabels[rc.interval]+'</span>'));
    tr.appendChild(td('<span style="font-size:12px;color:var(--text3);">'+fmtDate(rc.startDate)+'</span>'));
    tr.appendChild(td('<span style="font-size:12px;font-family:monospace;color:var(--text);">'+(rc.status==='ended'?'—':fmtDate(rc.nextDate))+'</span>'));
    tr.appendChild(td('<span style="font-size:12px;color:var(--text3);">'+(rc.endDate?fmtDate(rc.endDate):'—')+'</span>'));
    tr.appendChild(td(
      '<div style="display:flex;align-items:center;gap:6px;">'+
      '<span style="width:7px;height:7px;border-radius:50%;background:'+stColor+';display:inline-block;"></span>'+
      '<span style="font-size:12px;color:'+stColor+';">'+stLabel+'</span></div>'
    ));
    tr.appendChild(td('<span style="font-size:12px;color:var(--text3);">'+(rc.desc||'—')+'</span>'));
    tr.appendChild(td('<span style="font-size:13px;font-weight:600;color:var(--text);">'+f(rc.total)+'</span>', 'text-align:right;'));

    // no per-row dots — use side panel menu instead

    tbl.appendChild(tr);
  });
}

// ── Side panel ────────────────────────────────────────────────────
function openRCPanel(rcId) {
  _rcPanelId = rcId;
  var rc = DB.recurring.find(function(r){return r.id===rcId;});
  if(!rc) return;

  var panel = document.getElementById('rc-side-panel');
  panel.classList.add('open');

  // Header
  document.getElementById('rcp-title').textContent = 'Recurring Invoice';
  document.getElementById('rcp-desc').textContent = rc.desc || '—';

  // Contact
  var initials = (rc.customer||'?').split(' ').map(function(w){return w[0]||'';}).slice(0,2).join('').toUpperCase();
  document.getElementById('rcp-avatar').textContent = initials;
  document.getElementById('rcp-customer').textContent = rc.customer || '—';
  // Find contact email
  var contact = (DB.contacts||[]).find(function(ct){
    return ct.name && ct.name.toLowerCase() === (rc.customer||'').toLowerCase();
  });
  document.getElementById('rcp-customer-email').textContent = contact ? (contact.email||'No email on file') : 'Not in contacts';

  // Dates row
  document.getElementById('rcp-interval').textContent = intervalLabels[rc.interval] || rc.interval;
  document.getElementById('rcp-start').textContent    = fmtDate(rc.startDate);
  document.getElementById('rcp-end').textContent      = rc.endDate ? fmtDate(rc.endDate) : '∞';

  // Toggles
  document.getElementById('rcp-autocreate').checked = rc.autoCreate !== false;
  document.getElementById('rcp-autosend').checked   = rc.autoSend   === true;

  // Edit fields
  document.getElementById('rcp-net').value          = rc.net || 0;
  document.getElementById('rcp-vat').value          = rc.vatRate || 21;
  document.getElementById('rcp-total-display').value= f(rc.total || 0);
  document.getElementById('rcp-enddate').value      = rc.endDate || '';

  // Build cascade
  buildRCCascade(rc);

  // Re-render list to highlight selected row
  rRecurring();
}

function closeRCPanel() {
  _rcPanelId = null;
  var panel = document.getElementById('rc-side-panel');
  if(panel) panel.classList.remove('open');
  rRecurring();
}

function recalcRCP() {
  var net = parseFloat(document.getElementById('rcp-net').value)||0;
  var vat = parseFloat(document.getElementById('rcp-vat').value)||0;
  var total = net + net*vat/100;
  document.getElementById('rcp-total-display').value = f(total);
}

function saveRCPSettings() {
  if(!_rcPanelId) return;
  var rc = DB.recurring.find(function(r){return r.id===_rcPanelId;});
  if(!rc) return;
  rc.autoCreate = document.getElementById('rcp-autocreate').checked;
  rc.autoSend   = document.getElementById('rcp-autosend').checked;
  sv();
}

function saveRCPanel() {
  if(!_rcPanelId) return;
  var rc = DB.recurring.find(function(r){return r.id===_rcPanelId;});
  if(!rc) return;
  var net   = parseFloat(document.getElementById('rcp-net').value)||0;
  var vat   = parseFloat(document.getElementById('rcp-vat').value)||0;
  var va    = net*vat/100;
  rc.net     = net;
  rc.vatRate = vat;
  rc.vatAmt  = va;
  rc.total   = net + va;
  rc.endDate = document.getElementById('rcp-enddate').value || null;
  rc.autoCreate = document.getElementById('rcp-autocreate').checked;
  rc.autoSend   = document.getElementById('rcp-autosend').checked;
  sv(); rRecurring(); buildRCCascade(rc);
  showToast('✅ Recurring updated: ' + rc.customer);
}

function buildRCCascade(rc) {
  var container = document.getElementById('rcp-cascade');
  var rangeEl   = document.getElementById('rcp-daterange');
  if(!container) return;

  // Get all sales generated by this recurring, indexed by date
  var genSales = {};
  DB.sales.filter(function(s){return s.recurringId===rc.id;}).forEach(function(s){
    genSales[s.date] = s;
  });

  // Build list of all periods: past converted + upcoming pending
  var periods = [];
  var today   = td();

  // Past converted periods (from generated sales)
  Object.keys(genSales).sort().forEach(function(date){
    periods.push({date:date, sale:genSales[date], converted:true});
  });

  // Upcoming: project next dates up to 6 periods ahead (or until endDate)
  var nextDate = rc.nextDate || rc.startDate;
  var maxPeriods = 6;
  var count = 0;
  while(count < maxPeriods && nextDate <= today) {
    // Skip already generated
    nextDate = addIntervalDays(nextDate, rc.interval);
  }
  for(var i=0; i<maxPeriods; i++) {
    if(rc.endDate && nextDate > rc.endDate) break;
    periods.push({date:nextDate, sale:null, converted:false});
    nextDate = addIntervalDays(nextDate, rc.interval);
    count++;
  }

  if(!periods.length) {
    container.innerHTML = '<div style="color:var(--text3);font-size:12px;text-align:center;padding:16px;">No periods to show.</div>';
    return;
  }

  var monthNames = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  rangeEl.textContent = fmtDate(periods[0].date) + ' → ' + fmtDate(periods[periods.length-1].date);

  container.innerHTML = '';
  periods.forEach(function(p) {
    var d = new Date(p.date);
    var monthName = monthNames[d.getMonth()];
    var year      = d.getFullYear();

    var item = document.createElement('div');
    item.className = 'rc-cascade-item';
    item.style.cssText = p.converted ? '' : 'opacity:.7;';

    // Month pill
    var pill = document.createElement('div');
    pill.className = 'rc-month-pill';
    pill.innerHTML =
      '<div style="background:var(--surface2);border:1px solid var(--border);border-radius:6px;padding:3px 4px;">' +
      '<div class="month">'+monthName+'</div>' +
      '<div class="year">'+year+'</div>' +
      '</div>';

    // Qty
    var qty = document.createElement('div');
    qty.className = 'rc-cascade-qty';
    qty.textContent = '1';

    // Amount — use sale's actual total if converted, else current rc.total
    var amt = document.createElement('div');
    amt.className = 'rc-cascade-amt';
    if(p.sale) {
      var changed = Math.abs(p.sale.total - rc.total) > 0.01;
      amt.innerHTML =
        f(p.sale.total) + (changed ? ' <span style="font-size:9px;color:var(--yellow);margin-left:3px;" title="Price was different">★</span>' : '') + '<br>' +
        '<span class="rc-cascade-inv" onclick="openInvoicePreview('+p.sale.id+')">' +
        p.sale.num + '</span>';
    } else {
      // Show any scheduled price change
      amt.textContent = f(rc.total);
    }

    // Status badge
    var badge = document.createElement('div');
    badge.className = 'rc-cascade-badge ' + (p.converted ? 'converted' : 'pending');
    badge.textContent = p.converted ? 'Converted' : 'Pending';

    item.appendChild(pill);
    item.appendChild(qty);
    item.appendChild(amt);
    item.appendChild(badge);
    container.appendChild(item);
  });
}


// ══════════════════════════════════════════════════════════════════
// INVOICE NUMBERING SERIES
// ══════════════════════════════════════════════════════════════════

var _serEditId = null;

function genSeriesNum(format, nextNum) {
  var now = new Date();
  var yy   = String(now.getFullYear()).slice(2);
  var yyyy = String(now.getFullYear());
  var s = format.replace('[YY]', yy).replace('[YYYY]', yyyy);
  // Count % signs to determine padding
  var pcts = (s.match(/%/g)||[]).length;
  var numStr = String(nextNum).padStart(pcts, '0');
  return s.replace(/%+/g, numStr);
}

function getNextSeriesNum(seriesId) {
  if(!DB.series) return null;
  var ser = DB.series.find(function(s){ return s.id===seriesId && s.active; });
  if(!ser) return null;
  ser.lastNum++;
  return genSeriesNum(ser.format, ser.lastNum);
}

function getDefaultSeriesForType(type) {
  if(!DB.series) return null;
  return DB.series.find(function(s){ return s.type===type && s.active; });
}

function previewSeriesNum() {
  var fmt  = (document.getElementById('ser-format')||{}).value || '';
  var last = parseInt((document.getElementById('ser-lastnum')||{}).value)||0;
  var prev = document.getElementById('ser-preview');
  if(prev && fmt) prev.textContent = genSeriesNum(fmt, last+1);
}

function openSeriesModal(id) {
  _serEditId = id || null;
  var delBtn = document.getElementById('ser-delete-btn');
  if(id) {
    var ser = DB.series.find(function(s){return s.id===id;});
    if(!ser) return;
    document.getElementById('series-modal-title').textContent = 'Edit Series';
    delBtn.style.display = 'inline-flex';
    document.getElementById('ser-name').value    = ser.name;
    document.getElementById('ser-code').value    = ser.code;
    document.getElementById('ser-type').value    = ser.type;
    document.getElementById('ser-format').value  = ser.format;
    document.getElementById('ser-lastnum').value = ser.lastNum;
  } else {
    document.getElementById('series-modal-title').textContent = 'New Numbering Series';
    delBtn.style.display = 'none';
    document.getElementById('ser-name').value    = '';
    document.getElementById('ser-code').value    = '';
    document.getElementById('ser-type').value    = 'sale';
    document.getElementById('ser-format').value  = '';
    document.getElementById('ser-lastnum').value = '0';
  }
  previewSeriesNum();
  openOverlay('ov-series');
}

function saveSeries() {
  var name   = document.getElementById('ser-name').value.trim();
  var code   = document.getElementById('ser-code').value.trim().toUpperCase();
  var type   = document.getElementById('ser-type').value;
  var format = document.getElementById('ser-format').value.trim();
  var lastNum= parseInt(document.getElementById('ser-lastnum').value)||0;
  if(!name||!code||!format){ alert('Please fill in Name, Code and Format.'); return; }
  if(!DB.series) DB.series = [];
  if(!DB.ids.ser) DB.ids.ser = 4;
  var ser = {
    id:      _serEditId || DB.ids.ser++,
    name:    name,
    code:    code,
    type:    type,
    format:  format,
    lastNum: lastNum,
    active:  true
  };
  if(_serEditId) {
    var idx = DB.series.findIndex(function(s){return s.id===_serEditId;});
    if(idx>=0) DB.series[idx] = ser;
  } else {
    DB.series.push(ser);
  }
  sv(); closeOverlay('ov-series'); rSeriesList();
  showToast('✅ Series saved: ' + code + ' — Preview: ' + genSeriesNum(format, lastNum+1));
}

function deleteSeries() {
  if(!_serEditId) return;
  var ser = DB.series.find(function(s){return s.id===_serEditId;});
  if(ser && [1,2,3].indexOf(ser.id)>=0){ alert('Cannot delete default series.'); return; }
  if(!confirm('Delete series: '+(ser?ser.name:'')+'?')) return;
  DB.series = DB.series.filter(function(s){return s.id!==_serEditId;});
  sv(); closeOverlay('ov-series'); rSeriesList();
  showToast('🗑 Series deleted');
}

function rSeriesList() {
  var el = document.getElementById('series-list');
  if(!el || !DB.series) return;
  var typeLabels = {sale:'Sales Invoice',credit:'Credit Note',purchase:'Purchase Invoice',other:'Other'};
  el.innerHTML = '';
  DB.series.forEach(function(ser){
    var nextPreview = genSeriesNum(ser.format, ser.lastNum+1);
    var div = document.createElement('div');
    div.className = 'series-card';
    div.innerHTML =
      '<div class="series-code">'+ser.code+'</div>'+
      '<div class="series-info">'+
        '<div class="series-name">'+ser.name+'</div>'+
        '<div class="series-format">'+ser.format+' &nbsp;→&nbsp; <strong>'+nextPreview+'</strong></div>'+
        '<div style="font-size:10px;color:var(--text3);margin-top:2px;">'+typeLabels[ser.type]+' &nbsp;|&nbsp; Last: '+ser.lastNum+'</div>'+
      '</div>'+
      '<div class="series-actions">'+
        '<button class="btn btn-ghost btn-sm" onclick="openSeriesModal('+ser.id+')">✏️ Edit</button>'+
      '</div>';
    el.appendChild(div);
  });
}

// Call rSeriesList when opening Settings prefs tab
var _origOpenSettings = openSettings;
openSettings = function(tab) {
  _origOpenSettings(tab);
  if(tab==='prefs')   setTimeout(rSeriesList, 50);
  if(tab==='company') setTimeout(refreshPlanUI, 50);
};


// ══════════════════════════════════════════════════════════════════
// DRILL-DOWN: P&L / BS → Journal Entries
// ══════════════════════════════════════════════════════════════════

var _jeFilter = null; // {account: '4000', label: 'Sales Revenue'}

function drillToJE(account, label) {
  _jeFilter = {account: account, label: label};
  nav('journal');
  rJE();
}

function clearJEFilter() {
  _jeFilter = null;
  rJE();
}


// ══════════════════════════════════════════════════════════════════
// IMPORT SYSTEM
// ══════════════════════════════════════════════════════════════════

var _importData   = null;   // parsed data ready to import
var _importType   = null;   // 'sales' | 'purchases' | 'contacts' | 'backup'

function handleImportDrop(e) {
  e.preventDefault();
  document.getElementById('import-drop-zone').classList.remove('drag-over');
  var file = e.dataTransfer.files[0];
  if(file) processImportFile(file);
}

function handleImportFile(input) {
  var file = input.files[0];
  if(file) processImportFile(file);
  input.value = '';
}

function processImportFile(file) {
  var reader = new FileReader();
  var isJson = file.name.toLowerCase().endsWith('.json');
  reader.onload = function(e) {
    try {
      if(isJson) {
        parseBackupJSON(e.target.result);
      } else {
        parseImportCSV(e.target.result, file.name);
      }
    } catch(err) {
      showImportResult('err', '❌ Error parsing file: ' + err.message);
    }
  };
  reader.readAsText(file);
}

// ── CSV Parser ────────────────────────────────────────────────────
function parseCSVRow(line) {
  var result = [], cur = '', inQ = false;
  for(var i=0; i<line.length; i++) {
    var ch = line[i];
    if(ch==='"') {
      if(inQ && line[i+1]==='"') { cur+='"'; i++; }
      else inQ = !inQ;
    } else if(ch===',' && !inQ) {
      result.push(cur.trim()); cur='';
    } else {
      cur += ch;
    }
  }
  result.push(cur.trim());
  return result;
}

function parseImportCSV(text, filename) {
  // Strip BOM
  text = text.replace(/^﻿/, '');
  var lines = text.replace(/\r/g,'').split('\n').filter(function(l){ return l.trim(); });
  if(!lines.length) { showImportResult('err', '❌ Empty file.'); return; }

  var headers = parseCSVRow(lines[0]).map(function(h){ return h.toLowerCase().trim(); });

  // Auto-detect type from headers
  var type = detectCSVType(headers, filename);
  if(!type) {
    showImportResult('err', '❌ Cannot detect import type. Please use a FinLedger template. Headers found: ' + headers.slice(0,5).join(', '));
    return;
  }

  var rows = [];
  for(var i=1; i<lines.length; i++) {
    var cells = parseCSVRow(lines[i]);
    if(cells.every(function(c){return !c.trim();})) continue; // skip blank rows
    var obj = {};
    headers.forEach(function(h,j){ obj[h] = cells[j] || ''; });
    rows.push(obj);
  }

  _importType = type;
  _importData = rows;

  showImportPreview(type, headers, rows.slice(0,8));
  var msg = '✅ Detected: <strong>' + type.toUpperCase() + '</strong> · ' + rows.length + ' rows ready to import.';
  if(type === 'sales') msg += ' Journal Entries (Dr AR / Cr Revenue) will be auto-generated.';
  if(type === 'purchases') msg += ' Journal Entries (Dr Expense / Cr AP) will be auto-generated.';
  showImportResult('ok', msg);
}

function detectCSVType(headers, filename) {
  var fn = (filename||'').toLowerCase();
  var h  = headers.join(' ');
  if(h.indexOf('customer') >= 0 && h.indexOf('vat') >= 0 && h.indexOf('supplier') < 0) return 'sales';
  if(h.indexOf('supplier') >= 0 && (h.indexOf('category') >= 0 || h.indexOf('cat') >= 0)) return 'purchases';
  if(h.indexOf('nif') >= 0 || (h.indexOf('name') >= 0 && h.indexOf('type') >= 0 && h.indexOf('iban') >= 0)) return 'contacts';
  if(fn.indexOf('sales') >= 0) return 'sales';
  if(fn.indexOf('purch') >= 0 || fn.indexOf('purchase') >= 0) return 'purchases';
  if(fn.indexOf('contact') >= 0) return 'contacts';
  return null;
}

function showImportPreview(type, headers, rows) {
  var ta = document.getElementById('import-preview-table');
  var thead = '<thead><tr>' + headers.slice(0,8).map(function(h){
    return '<th>' + h + '</th>';
  }).join('') + (headers.length>8?'<th>...</th>':'') + '</tr></thead>';
  var tbody = '<tbody>' + rows.map(function(r){
    return '<tr>' + headers.slice(0,8).map(function(h){
      return '<td>' + (r[h]||'') + '</td>';
    }).join('') + (headers.length>8?'<td>…</td>':'') + '</tr>';
  }).join('') + '</tbody>';
  ta.innerHTML = '<table>' + thead + tbody + '</table>';
  document.getElementById('import-result-area').style.display = 'block';
}

function showImportResult(cls, msg) {
  var el = document.getElementById('import-result-msg');
  el.className = 'import-result ' + cls;
  el.innerHTML = msg;
  document.getElementById('import-result-area').style.display = 'block';
}

function clearImport() {
  _importData = null; _importType = null;
  document.getElementById('import-result-area').style.display = 'none';
  document.getElementById('import-drop-zone').classList.remove('drag-over');
}

// ── JSON Backup restore ───────────────────────────────────────────
function parseBackupJSON(text) {
  var parsed = JSON.parse(text);
  if(!parsed || !parsed.ids) {
    showImportResult('err', '❌ Invalid backup file — not a FinLedger backup.');
    return;
  }
  _importType = 'backup';
  _importData = parsed;
  var counts = [
    'Sales: ' + (parsed.sales||[]).length,
    'Purchases: ' + (parsed.purch||[]).length,
    'Journal Entries: ' + (parsed.je||[]).length,
    'Contacts: ' + (parsed.contacts||[]).length,
  ];
  document.getElementById('import-preview-table').innerHTML =
    '<div style="padding:12px;font-size:13px;color:var(--text2);">' +
    '<div style="font-weight:600;color:var(--text);margin-bottom:8px;">📦 Backup contents:</div>' +
    counts.map(function(c){return '<div style="margin-bottom:4px;">• '+c+'</div>';}).join('') +
    '</div>';
  document.getElementById('import-result-area').style.display = 'block';
  showImportResult('warn', '⚠️ This will <strong>replace all current data</strong> with the backup. Make sure you have exported your current data first.');
}

// ── The actual import ─────────────────────────────────────────────
function confirmImport() {
  if(!_importData || !_importType) return;
  var btn = document.getElementById('import-confirm-btn');
  btn.textContent = '⏳ Processing...';
  btn.disabled = true;

  setTimeout(function(){
    try {
      var result;
      if(_importType === 'backup')     result = importBackup(_importData);
      else if(_importType === 'sales') result = importSales(_importData);
      else if(_importType === 'purchases') result = importPurchases(_importData);
      else if(_importType === 'contacts')  result = importContacts(_importData);

      sv();
      renderAll();
      showImportResult('ok', '✅ ' + result);
      btn.textContent = '✅ Import & Process';
      btn.disabled = false;
      _importData = null; _importType = null;
      showToast('✅ Import complete!');
    } catch(err) {
      showImportResult('err', '❌ Import failed: ' + err.message);
      btn.textContent = '✅ Import & Process';
      btn.disabled = false;
    }
  }, 100);
}

function importBackup(data) {
  // Full restore — replace DB entirely
  Object.keys(data).forEach(function(k){ DB[k] = data[k]; });
  // Ensure new fields exist
  if(!DB.contacts)  DB.contacts  = [];
  if(!DB.recurring) DB.recurring = [];
  if(!DB.series)    DB.series    = [];
  if(!DB.ids.ct)    DB.ids.ct    = 1;
  if(!DB.ids.rc)    DB.ids.rc    = 1;
  if(!DB.ids.ser)   DB.ids.ser   = 4;
  return 'Full backup restored. Sales: ' + DB.sales.length + ', JE: ' + DB.je.length + ', Contacts: ' + DB.contacts.length;
}

function importSales(rows) {
  var added = 0, skipped = 0, jeAdded = 0;
  var colMap = {
    num:     ['invoice #','invoice#','num','number','ref'],
    date:    ['date','fecha','date (yyyy-mm-dd)'],
    customer:['customer','cliente','client','name'],
    desc:    ['description','descripcion','desc','concept','concepto'],
    vatRate: ['vat rate (%)','vat rate','vat%','iva%','vat','iva'],
    net:     ['net amount','net','neto','subtotal','base imponible','base'],
    status:  ['status','estado'],
    method:  ['payment method','method','metodo','método'],
  };

  function getVal(row, keys) {
    for(var i=0;i<keys.length;i++){
      var v = row[keys[i]];
      if(v !== undefined && v !== '') return v;
    }
    return '';
  }

  rows.forEach(function(row) {
    var net = parseFloat(getVal(row, colMap.net)) || 0;
    if(!net) { skipped++; return; }
    var vat   = parseFloat(getVal(row, colMap.vatRate)) || parseFloat(DB.co.defvat) || 21;
    var va    = net * vat / 100;
    var total = net + va;
    var dt    = getVal(row, colMap.date) || td();
    var cust  = getVal(row, colMap.customer) || 'Unknown';
    var stat  = (getVal(row, colMap.status)||'pending').toLowerCase();
    var meth  = getVal(row, colMap.method) || 'bank';
    var pfx   = DB.prefs.invpfx || 'INV-';
    var num   = getVal(row, colMap.num) || (pfx + String(DB.ids.s).padStart(6,'0'));

    // Check for duplicate invoice number
    if(DB.sales.some(function(s){return s.num===num;})) { skipped++; return; }

    var rec = {
      id:DB.ids.s++, date:dt, num:num, customer:cust,
      desc:getVal(row,colMap.desc)||'', vatRate:vat,
      net:net, vatAmt:va, total:total, status:stat, method:meth
    };
    DB.sales.push(rec);

    // Auto JE: Dr AR / Cr Revenue / Cr VAT (active plan)
    var _isp = getActivePlan();
    var lines = [{account:_isp.ar,debit:total,credit:0},{account:_isp.revenue,debit:0,credit:net}];
    if(va > 0) lines.push({account:_isp.vatIn,debit:0,credit:va});
    DB.je.push({
      id:DB.ids.j++, date:dt,
      desc:'Sale (Import) — '+cust+' / '+num,
      lines:lines, amount:total, auto:true, sourceType:'sale', sourceId:rec.id
    });

    // If paid, also create collection JE
    if(stat === 'paid') {
      DB.coll.push({id:DB.ids.c++,date:dt,customer:cust,ref:num,method:meth,amount:total,notes:'Auto from import'});
      var _icsp = getActivePlan();
      DB.je.push({
        id:DB.ids.j++, date:dt,
        desc:'Collection (Import) — '+cust+' / '+num,
        lines:[{account:_icsp.cash,debit:total,credit:0},{account:_icsp.ar,debit:0,credit:total}],
        amount:total, auto:true, sourceType:'collection'
      });
      jeAdded++;
    }
    added++; jeAdded++;
  });
  return 'Imported ' + added + ' sales invoices · ' + jeAdded + ' journal entries generated · ' + skipped + ' skipped (duplicate or empty)';
}

function importPurchases(rows) {
  var added = 0, skipped = 0, jeAdded = 0;
  var _impPlan = getActivePlan();
  var catAccMap = _impPlan.id === 'pgc' ? {
    'cogs':'600','cost of goods sold':'600','compras':'600',
    'materias primas':'601','raw materials':'601',
    'rent':'621','renting':'621','arrendamientos':'621',
    'salaries':'640','salaries & wages':'640','sueldos':'640',
    'utilities':'628','suministros':'628',
    'marketing':'627','publicidad':'627',
    'professional':'623','professional services':'623','servicios profesionales':'623',
    'depreciation':'681','amortización':'681',
    'financial':'662',
    'other opex':'629','other':'629','otros':'629'
  } : {
    'cogs':'5000','cost of goods sold':'5000',
    'salaries':'6000','rent':'6100','utilities':'6200',
    'marketing':'6300','professional':'6400','professional services':'6400',
    'depreciation':'6500','other opex':'6900','other':'6900'
  };

  var colMap = {
    num:     ['invoice #','invoice#','num','number','ref'],
    date:    ['date','fecha','date (yyyy-mm-dd)'],
    supplier:['supplier','proveedor','vendor','name'],
    desc:    ['description','descripcion','desc','concept'],
    cat:     ['category','categoria','cat'],
    vatRate: ['vat rate (%)','vat rate','vat%','iva%','vat','iva'],
    net:     ['net amount','net','neto','subtotal','base'],
    status:  ['status','estado'],
    method:  ['payment method','method','metodo'],
  };

  function getVal(row, keys) {
    for(var i=0;i<keys.length;i++){var v=row[keys[i]];if(v!==undefined&&v!=='')return v;}
    return '';
  }

  rows.forEach(function(row) {
    var net = parseFloat(getVal(row, colMap.net)) || 0;
    if(!net) { skipped++; return; }
    var vat   = parseFloat(getVal(row, colMap.vatRate)) || 21;
    var va    = net * vat / 100;
    var total = net + va;
    var dt    = getVal(row, colMap.date) || td();
    var sup   = getVal(row, colMap.supplier) || 'Unknown';
    var cat   = getVal(row, colMap.cat) || 'Other OpEx';
    var stat  = (getVal(row, colMap.status)||'pending').toLowerCase();
    var meth  = getVal(row, colMap.method) || 'bank';
    var pfx   = DB.prefs.purpfx || 'PINV-';
    var num   = getVal(row, colMap.num) || (pfx + String(DB.ids.p).padStart(6,'0'));

    if(DB.purch.some(function(p){return p.num===num;})) { skipped++; return; }

    var rec = {
      id:DB.ids.p++, date:dt, num:num, supplier:sup,
      desc:getVal(row,colMap.desc)||'', cat:cat,
      vatRate:vat, net:net, vatAmt:va, total:total, status:stat, method:meth
    };
    DB.purch.push(rec);

    // Auto JE: Dr Expense / Dr VAT / Cr AP (active plan)
    var _ipp = getActivePlan();
    var _fallbackExpAcc = _ipp.id === 'pgc' ? '629' : '6900';
    var expAcc = (_ipp.expCatMap && _ipp.expCatMap[cat]) || catAccMap[cat.toLowerCase()] || _fallbackExpAcc;
    var lines = [{account:expAcc,debit:net,credit:0},{account:_ipp.ap,debit:0,credit:total}];
    if(va > 0) lines.splice(1,0,{account:_ipp.vatOut,debit:va,credit:0});
    DB.je.push({
      id:DB.ids.j++, date:dt,
      desc:'Purchase (Import) — '+sup+' / '+num,
      lines:lines, amount:total, auto:true, sourceType:'purchase', sourceId:rec.id
    });

    if(stat === 'paid') {
      DB.pay.push({id:DB.ids.py++,date:dt,supplier:sup,ref:num,method:meth,amount:total,notes:'Auto from import'});
      var _ippay = getActivePlan();
      DB.je.push({
        id:DB.ids.j++, date:dt,
        desc:'Payment (Import) — '+sup+' / '+num,
        lines:[{account:_ippay.ap,debit:total,credit:0},{account:_ippay.cash,debit:0,credit:total}],
        amount:total, auto:true, sourceType:'payment'
      });
      jeAdded++;
    }
    added++; jeAdded++;
  });
  return 'Imported ' + added + ' purchase invoices · ' + jeAdded + ' journal entries generated · ' + skipped + ' skipped';
}

function importContacts(rows) {
  var added = 0, skipped = 0;
  var colMap = {
    name:     ['name','nombre','company'],
    type:     ['type','tipo'],
    nif:      ['nif','vat number','cif'],
    email:    ['email','correo'],
    phone:    ['phone','telefono','tel'],
    city:     ['city','ciudad'],
    country:  ['country','pais','país'],
    iban:     ['iban'],
    payterms: ['payment terms','payment_terms','payterms'],
    salesvat: ['vat sales (%)','vat sales','salesvat'],
    purchvat: ['vat purchase (%)','vat purchase','purchvat'],
  };
  function getVal(row,keys){for(var i=0;i<keys.length;i++){var v=row[keys[i]];if(v!==undefined&&v!=='')return v;}return '';}

  rows.forEach(function(row){
    var name = getVal(row, colMap.name);
    if(!name) { skipped++; return; }
    if(DB.contacts.some(function(ct){return ct.name.toLowerCase()===name.toLowerCase();})) { skipped++; return; }
    DB.contacts.push({
      id: DB.ids.ct++,
      name:     name,
      type:     getVal(row,colMap.type)||'client',
      nif:      getVal(row,colMap.nif),
      email:    getVal(row,colMap.email),
      phone:    getVal(row,colMap.phone),
      city:     getVal(row,colMap.city),
      country:  getVal(row,colMap.country),
      iban:     getVal(row,colMap.iban),
      payterms: getVal(row,colMap.payterms)||'30days',
      salesvat: getVal(row,colMap.salesvat)||'21',
      purchvat: getVal(row,colMap.purchvat)||'21',
      createdAt:td()
    });
    added++;
  });
  return 'Imported ' + added + ' contacts · ' + skipped + ' skipped (duplicate or empty name)';
}


// ── 3-dot context menu ───────────────────────────────────────────
var _rcMenuOpen = null;

function toggleRCMenu(e, rcId) {
  e.stopPropagation();
  // Close any open menu
  if(_rcMenuOpen && _rcMenuOpen !== rcId) {
    var prev = document.getElementById('rc-menu-'+_rcMenuOpen);
    if(prev) prev.classList.remove('open');
  }
  var menu = document.getElementById('rc-menu-'+rcId);
  if(!menu) return;
  var isOpen = menu.classList.contains('open');
  menu.classList.toggle('open', !isOpen);
  _rcMenuOpen = isOpen ? null : rcId;

  // Close on outside click
  if(!isOpen) {
    setTimeout(function(){
      document.addEventListener('click', function closeMenu(){
        var m = document.getElementById('rc-menu-'+rcId);
        if(m) m.classList.remove('open');
        _rcMenuOpen = null;
        document.removeEventListener('click', closeMenu);
      });
    }, 0);
  }
}

// ── Edit modal ───────────────────────────────────────────────────
var _rceId = null;


// ── Duplicate ────────────────────────────────────────────────────
function duplicateRC(rcId) {
  var menu = document.getElementById('rc-menu-'+rcId);
  if(menu) menu.classList.remove('open');

  var rc = DB.recurring.find(function(r){return r.id===rcId;});
  if(!rc) return;

  var copy = JSON.parse(JSON.stringify(rc));
  copy.id        = DB.ids.rc++;
  copy.generated = 0;
  copy.nextDate  = td();
  copy.startDate = td();
  copy.endDate   = null;
  copy.status    = 'active';
  copy.desc      = (rc.desc||'') + ' (copy)';

  if(!DB.recurring) DB.recurring = [];
  DB.recurring.push(copy);
  sv(); rRecurring();
  showToast('⧉ Duplicated: '+copy.customer+' — start from today');
}

// ── Delete ───────────────────────────────────────────────────────
function deleteRC(rcId) {
  var menu = document.getElementById('rc-menu-'+rcId);
  if(menu) menu.classList.remove('open');

  var rc = DB.recurring.find(function(r){return r.id===rcId;});
  if(!rc) return;

  var count = DB.sales.filter(function(s){return s.recurringId===rcId;}).length;
  var msg = 'Delete recurring invoice for '+rc.customer+'?';
  if(count > 0) msg += '\n\nNote: '+count+' invoice(s) already generated will NOT be deleted.';

  if(!confirm(msg)) return;

  DB.recurring = DB.recurring.filter(function(r){return r.id!==rcId;});
  if(_rcPanelId === rcId) closeRCPanel();
  sv(); rRecurring();
  showToast('🗑 Recurring deleted: '+rc.customer);
}


// ── RC Edit Modal ────────────────────────────────────────────────
var _rceOrigNet = 0; // track original price for change detection

function openRCEditPage(rcId) { openRCEditModal(rcId); } // alias

function openRCEditModal(rcId) {
  // Close any open menus
  var ctxMenu = document.getElementById('rcp-ctx-menu');
  if(ctxMenu) ctxMenu.classList.remove('open');

  _rceId = rcId || _rcPanelId;
  var rc = DB.recurring.find(function(r){return r.id===_rceId;});
  if(!rc) return;

  _rceOrigNet = rc.net || 0;

  // Subtitle
  document.getElementById('rce-subtitle').textContent =
    'RC-'+String(rc.id).padStart(3,'0')+' · '+rc.customer;

  // Source preview
  document.getElementById('rce-source-preview').textContent =
    rc.customer + ' — ' + (rc.desc||'') + ' — ' + f(rc.total) + ' (VAT ' + rc.vatRate + '%)';

  // Fields
  document.getElementById('rce-interval').value      = rc.interval  || 'monthly';
  document.getElementById('rce-duedays').value       = String(rc.duedays || 30);
  document.getElementById('rce-start').value         = rc.startDate || '';
  document.getElementById('rce-end').value           = rc.endDate   || '';
  document.getElementById('rce-method').value        = rc.method    || 'bank';
  document.getElementById('rce-status').value        = rc.status    || 'active';
  document.getElementById('rce-notes').value         = rc.notes     || '';
  document.getElementById('rce-net').value           = rc.net       || 0;
  document.getElementById('rce-vat').value           = String(rc.vatRate || 21);
  document.getElementById('rce-autocreate').checked  = rc.autoCreate !== false;
  document.getElementById('rce-autosend').checked    = rc.autoSend  === true;

  // Hide price change notice
  document.getElementById('rce-price-change-notice').style.display = 'none';

  calcRCEModal();
  openOverlay('ov-rc-edit');
}

function calcRCEModal() {
  var net   = parseFloat(document.getElementById('rce-net').value)||0;
  var vat   = parseFloat(document.getElementById('rce-vat').value)||0;
  var va    = net*vat/100;
  var total = net+va;
  document.getElementById('rce-vatamt').value        = va.toFixed(2);
  document.getElementById('rce-total-display').value = f(total);

  // Show price change notice if amount changed
  var notice = document.getElementById('rce-price-change-notice');
  if(Math.abs(net - _rceOrigNet) > 0.01) {
    document.getElementById('rce-old-price').textContent = f(_rceOrigNet);
    document.getElementById('rce-new-price').textContent = f(net);
    notice.style.display = 'block';
  } else {
    notice.style.display = 'none';
  }
}

function saveRCEditModal() {
  if(!_rceId) return;
  var rc = DB.recurring.find(function(r){return r.id===_rceId;});
  if(!rc) return;

  var net = parseFloat(document.getElementById('rce-net').value)||0;
  var vat = parseFloat(document.getElementById('rce-vat').value)||0;
  var va  = net*vat/100;

  // Record price change in history if amount changed
  if(Math.abs(net - _rceOrigNet) > 0.01) {
    if(!rc.priceHistory) rc.priceHistory = [];
    rc.priceHistory.push({
      date:    td(),
      oldNet:  _rceOrigNet,
      newNet:  net,
      oldTotal: _rceOrigNet*(1+(rc.vatRate||21)/100),
      newTotal: net+va
    });
  }

  rc.net        = net;
  rc.vatRate    = vat;
  rc.vatAmt     = va;
  rc.total      = net + va;
  rc.interval   = document.getElementById('rce-interval').value;
  rc.duedays    = parseInt(document.getElementById('rce-duedays').value)||30;
  rc.startDate  = document.getElementById('rce-start').value || rc.startDate;
  rc.endDate    = document.getElementById('rce-end').value   || null;
  rc.method     = document.getElementById('rce-method').value;
  rc.status     = document.getElementById('rce-status').value;
  rc.notes      = document.getElementById('rce-notes').value;
  rc.autoCreate = document.getElementById('rce-autocreate').checked;
  rc.autoSend   = document.getElementById('rce-autosend').checked;

  sv();
  closeOverlay('ov-rc-edit');
  // Refresh panel if open
  if(_rcPanelId === _rceId) {
    openRCPanel(_rceId);
  }
  rRecurring();
  showToast('✅ Recurring saved: '+rc.customer+' — '+intervalLabels[rc.interval]);
}

function toggleRCPanelMenu(e) {
  e.stopPropagation();
  var menu = document.getElementById('rcp-ctx-menu');
  if(!menu) return;
  var isOpen = menu.classList.contains('open');
  menu.classList.toggle('open', !isOpen);
  if(!isOpen) {
    setTimeout(function(){
      document.addEventListener('click', function closeIt(){
        menu.classList.remove('open');
        document.removeEventListener('click', closeIt);
      });
    }, 0);
  }
}


// ══════════════════════════════════════════════════════════════════
// VIEW MODE: Monthly / Quarterly / Annual columnar P&L
// ══════════════════════════════════════════════════════════════════

var _viewMode = 'total'; // 'total' | 'monthly' | 'quarterly' | 'annual'
var _viewYear = new Date().getFullYear();

// Populate year selector on init
function initViewYears() {
  var sel = document.getElementById('pl-view-year');
  if(!sel) return;
  var now = new Date().getFullYear();
  sel.innerHTML = '';
  for(var y = now; y >= now-5; y--) {
    var opt = document.createElement('option');
    opt.value = y; opt.textContent = y;
    if(y === now) opt.selected = true;
    sel.appendChild(opt);
  }
  _viewYear = now;
}

function setViewMode(mode) {
  _viewMode = mode;
  var yearSel = document.getElementById('pl-view-year');
  if(yearSel) _viewYear = parseInt(yearSel.value) || new Date().getFullYear();
  var resetBtn = document.getElementById('pl-view-reset');
  if(resetBtn) resetBtn.style.display = mode && mode !== 'total' ? '' : 'none';
  rPL();
}

function resetViewMode() {
  _viewMode = 'total';
  var sel = document.getElementById('pl-view-mode');
  if(sel) sel.value = 'total';
  var resetBtn = document.getElementById('pl-view-reset');
  if(resetBtn) resetBtn.style.display = 'none';
  rPL();
}

// Compute P&L figures for a specific date range
function cFForRange(fromStr, toStr) {
  // Filter JEs to this date range
  var jes = DB.je.filter(function(je){
    return (!fromStr || je.date >= fromStr) && (!toStr || je.date <= toStr);
  });

  // Use active plan account codes
  var _rp = getActivePlan();

  function sumAccs(accs) {
    // Sum credit - debit for revenue accounts
    var t = 0;
    jes.forEach(function(je){
      je.lines.forEach(function(l){
        if(accs.indexOf(l.account) >= 0) t += (l.credit||0) - (l.debit||0);
      });
    });
    return t;
  }
  function sumAccsDr(accs) {
    // Sum debit - credit for expense/asset accounts
    var t = 0;
    jes.forEach(function(je){
      je.lines.forEach(function(l){
        if(accs.indexOf(l.account) >= 0) t += (l.debit||0) - (l.credit||0);
      });
    });
    return t;
  }
  function sumAcc(acc)   { return sumAccs([acc]);   }
  function sumAccDr(acc) { return sumAccsDr([acc]); }

  // Revenue — all plan revenue accounts
  var rev  = Math.max(0, sumAccs(_rp.revAccts));

  // COGS — all plan COGS accounts
  var cogs = Math.max(0, sumAccsDr(_rp.cogsAccts));

  // OpEx — iterate each account in plan's opexAccts
  var opex = {};
  _rp.opexAccts.forEach(function(acc){
    var v = sumAccDr(acc);
    if(v > 0.005) {
      // Get account name from COA
      var acct = COA.find(function(a){return a.c===acc;});
      var name = acct ? acct.n : acc;
      opex[name] = (opex[name]||0) + v;
    }
  });

  // Financial expenses
  var finExp = sumAccsDr(_rp.finExpAccts || []);

  var toOpEx = Object.values(opex).reduce(function(a,b){return a+b;},0);
  var ebit   = rev - cogs - toOpEx;
  var ni     = ebit - finExp;
  return { rev:rev, cogs:cogs, opex:opex, toOpEx:toOpEx, gp:rev-cogs, ebit:ebit, ni:ni };
}

function pad2(n){ return n < 10 ? '0'+n : String(n); }
function lastDay(y,m){ return new Date(y,m,0).getDate(); }

// Build column definitions for current view mode
function getViewColumns() {
  var y = _viewYear;
  if(_viewMode === 'monthly') {
    var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
    return months.map(function(mn, i){
      var m = i+1;
      return {
        label: mn,
        from:  y+'-'+pad2(m)+'-01',
        to:    y+'-'+pad2(m)+'-'+pad2(lastDay(y,m))
      };
    });
  }
  if(_viewMode === 'quarterly') {
    return ['Q1','Q2','Q3','Q4'].map(function(qn,i){
      var sm = i*3+1, em = i*3+3;
      return {
        label: qn,
        from:  y+'-'+pad2(sm)+'-01',
        to:    y+'-'+pad2(em)+'-'+pad2(lastDay(y,em))
      };
    });
  }
  if(_viewMode === 'annual') {
    return [{
      label: String(y),
      from:  y+'-01-01',
      to:    y+'-12-31'
    }];
  }
  return null; // 'total' — use existing date filter
}

// ── Override rPL to support view modes ────────────────────────────
function rPL(){
  var cols = getViewColumns();
  var b = document.getElementById('plBody');
  var head = document.getElementById('plHead');
  var colgroup = document.getElementById('plColgroup');

  if(!cols) {
    // --- TOTAL mode: original single-column render ---
    if(head) head.innerHTML = '';
    if(colgroup) colgroup.innerHTML = '<col style="width:55%"><col style="width:45%">';
    var F=cF(), gp=F.rev-F.cogs;
    var gmp=F.totRev?(gp/F.totRev*100).toFixed(1):0, npp=F.totRev?(F.ni/F.totRev*100).toFixed(1):0;
    if(plMode==='summary'){
      b.innerHTML='<tr class="rh"><td colspan="2">Summary P&L</td></tr>'+
        '<tr class="rd"><td>Total Revenue</td><td class="num pos">'+f(F.totRev)+'</td></tr>'+
        '<tr class="rd"><td>Cost of Goods Sold</td><td class="num neg">('+f(F.cogs)+')</td></tr>'+
        '<tr class="rs"><td>Gross Profit</td><td class="num">'+f(gp)+'</td></tr>'+
        '<tr class="rd"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx)+')</td></tr>'+
        '<tr class="rs"><td>EBIT</td><td class="num">'+f(F.ebit)+'</td></tr>'+
        '<tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';
      return;
    }
    var rows='<tr class="rh"><td colspan="2">Revenue</td></tr>'+
      '<tr class="rd"><td class="ind drilldown-link" data-drill="4000" data-label="Sales Revenue" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">Sales Revenue ↗</td><td class="num pos">'+f(F.rev)+'</td></tr>'+
      '<tr class="rs"><td>Total Revenue</td><td class="num">'+f(F.totRev)+'</td></tr>'+
      '<tr class="rh"><td colspan="2">Cost of Goods Sold</td></tr>'+
      '<tr class="rd"><td class="ind drilldown-link" data-drill="5000" data-label="COGS" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click for detail">COGS – Direct Purchases ↗</td><td class="num neg">('+f(F.cogs)+')</td></tr>'+
      '<tr class="rs"><td>Gross Profit <span style="font-size:11px;color:var(--text3);font-family:monospace;margin-left:8px;">'+gmp+'%</span></td><td class="num '+(gp>=0?'pos':'neg')+'">'+f(gp)+'</td></tr>'+
      '<tr class="rh"><td colspan="2">Operating Expenses</td></tr>';
    var _oaM={'Cost of Goods Sold':'5000','Salaries':'6000','Rent':'6100','Utilities':'6200','Marketing':'6300','Professional Services':'6400','Professional':'6400','Depreciation':'6500','Other OpEx':'6900'};
    Object.entries(F.opex).forEach(function(e){
      var _a=_oaM[e[0]]||'6900';
      rows+='<tr class="rd"><td class="ind drilldown-link" data-drill="'+_a+'" data-label="'+e[0]+'" onclick="drillToJE(this.dataset.drill,this.dataset.label)" title="Click">'+e[0]+' ↗</td><td class="num neg">('+f(e[1])+')</td></tr>';
    });
    if(!F.toOpEx&&!F.jeE) rows+='<tr class="rd"><td class="ind" style="color:var(--text3);">No expenses recorded</td><td class="num">—</td></tr>';
    rows+='<tr class="rs"><td>Total Operating Expenses</td><td class="num neg">('+f(F.toOpEx+F.jeE)+')</td></tr>'+
      '<tr class="rs"><td>EBIT (Operating Income)</td><td class="num">'+f(F.ebit)+'</td></tr>'+
      '<tr class="rt"><td>NET INCOME <span style="font-size:11px;font-family:monospace;opacity:.7;margin-left:8px;">'+npp+'% margin</span></td><td class="num">'+f(F.ni)+'</td></tr>';
    b.innerHTML=rows;
    return;
  }

  // --- COLUMNAR mode (monthly / quarterly / annual) ---
  var n = cols.length;
  var colW = Math.floor(50/n); // distribute 50% equally among data cols

  // Colgroup
  colgroup.innerHTML = '<col style="width:50%">' + cols.map(function(){ return '<col style="width:'+colW+'%">'; }).join('');

  // Header row
  head.innerHTML = '<tr class="rh"><th style="text-align:left;padding:10px 12px;font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">Account</th>' +
    cols.map(function(col){
      return '<th style="text-align:right;padding:10px 12px;font-size:11px;color:var(--accent);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">'+col.label+'</th>';
    }).join('') + '</tr>';

  // Compute data for each column
  var Fs = cols.map(function(col){ return cFForRange(col.from, col.to); });

  function numCell(val, cls) {
    var isNeg = val < 0;
    var display = isNeg ? '('+f(Math.abs(val))+')' : f(val);
    var color = cls==='pos'?'var(--green)':cls==='neg'?'var(--red)':'';
    return '<td style="text-align:right;padding:8px 12px;font-size:12px;font-family:monospace;'+(color?'color:'+color+';':'')+'">'+display+'</td>';
  }
  function totalCell(val) {
    var color = val >= 0 ? 'var(--green)' : 'var(--red)';
    return '<td style="text-align:right;padding:8px 12px;font-size:13px;font-weight:700;font-family:monospace;color:'+color+';">'+f(val)+'</td>';
  }
  function sectionRow(label, vals, cls, isTotal) {
    var fn = isTotal ? totalCell : function(v){ return numCell(v, cls); };
    return '<tr class="'+(isTotal?'rt':'rs')+'"><td style="padding:8px 12px;font-weight:'+(isTotal?700:600)+';">'+label+'</td>'+vals.map(fn).join('')+'</tr>';
  }
  function detailRow(label, vals, cls) {
    return '<tr class="rd"><td class="ind" style="padding:7px 12px 7px 24px;font-size:12px;color:var(--text2);">'+label+'</td>'+
      vals.map(function(v){ return numCell(v, cls); }).join('')+'</tr>';
  }
  function headerRow(label) {
    return '<tr class="rh"><td colspan="'+(n+1)+'" style="padding:9px 12px;font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;">'+label+'</td></tr>';
  }

  var rows = '';

  // REVENUE
  rows += headerRow('Revenue');
  rows += detailRow('Sales Revenue', Fs.map(function(F){return F.rev;}), 'pos');
  rows += sectionRow('Total Revenue', Fs.map(function(F){return F.rev;}), 'pos');

  // COGS
  rows += headerRow('Cost of Goods Sold');
  rows += detailRow('COGS – Direct Purchases', Fs.map(function(F){return -F.cogs;}), 'neg');
  rows += sectionRow('Gross Profit', Fs.map(function(F){return F.gp;}), '');

  // OPEX — collect all unique keys across all columns
  var allOpexKeys = {};
  Fs.forEach(function(F){ Object.keys(F.opex).forEach(function(k){ allOpexKeys[k]=1; }); });
  var opexKeys = Object.keys(allOpexKeys);
  if(opexKeys.length) {
    rows += headerRow('Operating Expenses');
    opexKeys.forEach(function(k){
      rows += detailRow(k, Fs.map(function(F){ return -(F.opex[k]||0); }), 'neg');
    });
    rows += sectionRow('Total OpEx', Fs.map(function(F){return -F.toOpEx;}), 'neg');
  }

  // EBIT & NET INCOME
  rows += sectionRow('EBIT', Fs.map(function(F){return F.ni;}), '');
  rows += sectionRow('NET INCOME', Fs.map(function(F){return F.ni;}), '', true);

  b.innerHTML = rows;
}


// ── Account Plan Switcher ─────────────────────────────────────────
function selectAccountPlan(planId) {
  if(!ACCOUNT_PLANS[planId]) return;
  var current = (DB.co && DB.co.accountPlan) || 'usgaap';
  var warning = document.getElementById('plan-warning');

  if(planId !== current && DB.je && DB.je.length > 0) {
    // Show warning if there are existing JEs
    if(warning) warning.style.display = 'block';
  } else {
    if(warning) warning.style.display = 'none';
  }

  // Update card UI
  Object.keys(ACCOUNT_PLANS).forEach(function(id){
    var card    = document.getElementById('plan-card-'+id);
    var active  = document.getElementById('plan-active-'+id);
    if(!card) return;
    var isActive = id === planId;
    card.style.border     = '2px solid ' + (isActive ? 'var(--accent)' : 'var(--border)');
    card.style.background = isActive ? 'var(--surface3)' : '';
    if(active) {
      active.style.display = isActive ? 'block' : 'none';
    }
  });

  // Save to DB
  if(!DB.co) DB.co = {};
  DB.co.accountPlan = planId;
  refreshCOA();
  initJE();   // rebuild JE modal lines with new plan's COA
  sv();
  renderAll();
  showToast('✅ Accounting plan switched to: ' + ACCOUNT_PLANS[planId].name);
}

function refreshPlanUI() {
  var planId = (DB.co && DB.co.accountPlan) || 'usgaap';
  Object.keys(ACCOUNT_PLANS).forEach(function(id){
    var card   = document.getElementById('plan-card-'+id);
    var active = document.getElementById('plan-active-'+id);
    if(!card) return;
    var isIt = id === planId;
    card.style.border     = '2px solid ' + (isIt ? 'var(--accent)' : 'var(--border)');
    card.style.background = isIt ? 'var(--surface3)' : '';
    if(active) active.style.display = isIt ? 'block' : 'none';
  });
}


// ══════════════════════════════════════════════════════════════════
// ASSETS & DEPRECIATION MODULE
// ══════════════════════════════════════════════════════════════════

var _deprAssetId = null; // purchase record id for current depr plan

// Account options per plan
var DEPR_ACCTS = {
  usgaap: {
    accum: [
      {c:'1510', n:'1510 — Accum. Depreciation (General)'},
    ],
    exp: [
      {c:'6500', n:'6500 — Depreciation Expense'},
    ],
    fixed: [
      {c:'1500', n:'1500 — Fixed Assets (General)'},
    ]
  },
  pgc: {
    accum: [
      {c:'280',  n:'280 — Amort. acum. inmovilizado intangible'},
      {c:'2800', n:'2800 — Amort. acum. investigación'},
      {c:'2801', n:'2801 — Amort. acum. desarrollo'},
      {c:'2802', n:'2802 — Amort. acum. concesiones administrativas'},
      {c:'2803', n:'2803 — Amort. acum. propiedad industrial'},
      {c:'2805', n:'2805 — Amort. acum. derechos de traspaso'},
      {c:'2806', n:'2806 — Amort. acum. aplicaciones informáticas'},
      {c:'281',  n:'281 — Amort. acum. inmovilizado material'},
      {c:'2811', n:'2811 — Amort. acum. construcciones'},
      {c:'2812', n:'2812 — Amort. acum. instalaciones técnicas'},
      {c:'2813', n:'2813 — Amort. acum. maquinaria'},
      {c:'2814', n:'2814 — Amort. acum. utillaje'},
      {c:'2815', n:'2815 — Amort. acum. otras instalaciones'},
      {c:'2816', n:'2816 — Amort. acum. mobiliario'},
      {c:'2817', n:'2817 — Amort. acum. equipos para procesos de información'},
      {c:'2818', n:'2818 — Amort. acum. elementos de transporte'},
      {c:'2819', n:'2819 — Amort. acum. otro inmovilizado material'},
    ],
    exp: [
      {c:'680',  n:'680 — Amortización inmovilizado intangible'},
      {c:'681',  n:'681 — Amortización inmovilizado material'},
    ],
    fixed: [
      {c:'210',  n:'210 — Terrenos y bienes naturales'},
      {c:'211',  n:'211 — Construcciones'},
      {c:'212',  n:'212 — Instalaciones técnicas'},
      {c:'213',  n:'213 — Maquinaria'},
      {c:'214',  n:'214 — Utillaje'},
      {c:'215',  n:'215 — Otras instalaciones'},
      {c:'216',  n:'216 — Mobiliario'},
      {c:'217',  n:'217 — Equipos para procesos de información'},
      {c:'218',  n:'218 — Elementos de transporte'},
      {c:'219',  n:'219 — Otro inmovilizado material'},
      {c:'200',  n:'200 — Investigación'},
      {c:'201',  n:'201 — Desarrollo'},
      {c:'206',  n:'206 — Aplicaciones informáticas'},
    ]
  }
};

function onPurchTypeChange(val) {
  var assetRow = document.getElementById('p-asset-name-row');
  var catSel   = document.getElementById('p-cat');
  var catLabel = catSel ? catSel.parentElement.querySelector('label') : null;
  if(assetRow) assetRow.style.display = val === 'asset' ? '' : 'none';

  if(val === 'asset') {
    if(catLabel) catLabel.textContent = 'Asset Account (Non-Current Assets)';
    if(catSel) {
      var planId = (DB.co && DB.co.accountPlan) || 'usgaap';
      if(planId === 'pgc') {
        catSel.innerHTML =
          '<optgroup label="Inmovilizado Material">' +
          '<option value="210">210 — Terrenos y bienes naturales</option>' +
          '<option value="211">211 — Construcciones</option>' +
          '<option value="212">212 — Instalaciones técnicas</option>' +
          '<option value="213" selected>213 — Maquinaria</option>' +
          '<option value="214">214 — Utillaje</option>' +
          '<option value="215">215 — Otras instalaciones</option>' +
          '<option value="216">216 — Mobiliario</option>' +
          '<option value="217">217 — Equipos para procesos de información</option>' +
          '<option value="218">218 — Elementos de transporte</option>' +
          '<option value="219">219 — Otro inmovilizado material</option>' +
          '<option value="221">221 — Inversiones en construcciones</option>' +
          '</optgroup>' +
          '<optgroup label="Inmovilizado Intangible">' +
          '<option value="200">200 — Investigación</option>' +
          '<option value="201">201 — Desarrollo</option>' +
          '<option value="202">202 — Concesiones administrativas</option>' +
          '<option value="203">203 — Propiedad industrial</option>' +
          '<option value="204">204 — Fondo de comercio</option>' +
          '<option value="205">205 — Derechos de traspaso</option>' +
          '<option value="206">206 — Aplicaciones informáticas</option>' +
          '<option value="209">209 — Anticipos inmovilizaciones intangibles</option>' +
          '</optgroup>';
      } else {
        // US GAAP asset accounts
        catSel.innerHTML =
          '<option value="1500" selected>1500 — Fixed Assets (General)</option>' +
          '<option value="1510">1510 — Equipment</option>' +
          '<option value="1520">1520 — Furniture & Fixtures</option>' +
          '<option value="1530">1530 — Vehicles</option>' +
          '<option value="1540">1540 — Buildings</option>' +
          '<option value="1550">1550 — Land</option>' +
          '<option value="1560">1560 — Intangible Assets</option>' +
          '<option value="1570">1570 — Leasehold Improvements</option>';
      }
    }
  } else {
    if(catLabel) catLabel.textContent = 'Category';
    if(catSel) {
      catSel.innerHTML =
        '<option value="COGS">Cost of Goods Sold</option>' +
        '<option value="Rent">Rent</option>' +
        '<option value="Salaries">Salaries</option>' +
        '<option value="Utilities">Utilities</option>' +
        '<option value="Marketing">Marketing</option>' +
        '<option value="Professional">Professional Services</option>' +
        '<option value="Depreciation">Depreciation</option>' +
        '<option value="Other OpEx">Other OpEx</option>';
    }
  }
}

function openDeprModal(purchId) {
  _deprAssetId = purchId;
  var purch = DB.purch.find(function(p){return p.id===purchId;});
  if(!purch) return;

  // Label
  document.getElementById('depr-asset-label').textContent =
    purch.num + ' · ' + purch.supplier;
  document.getElementById('depr-asset-summary').textContent =
    purch.assetName || purch.desc || '' + ' — ' + f(purch.net) + ' net (' + f(purch.total) + ' incl. VAT)';

  // Pre-fill dates
  document.getElementById('depr-start').value = purch.date || td();
  document.getElementById('depr-rate').value  = '10';
  document.getElementById('depr-residual').value = '0';
  document.getElementById('depr-freq').value  = 'annually';

  // Populate account selectors based on active plan
  var planId  = (DB.co && DB.co.accountPlan) || 'usgaap';
  var deprAcc = DEPR_ACCTS[planId] || DEPR_ACCTS.usgaap;

  var accumSel = document.getElementById('depr-accum-acc');
  accumSel.innerHTML = deprAcc.accum.map(function(a){
    return '<option value="'+a.c+'">'+a.n+'</option>';
  }).join('');

  var expSel = document.getElementById('depr-exp-acc');
  expSel.innerHTML = deprAcc.exp.map(function(a){
    return '<option value="'+a.c+'">'+a.n+'</option>';
  }).join('');

  // Set sensible defaults
  if(planId === 'pgc') {
    accumSel.value = '281'; // material assets default
    expSel.value   = '681';
  } else {
    accumSel.value = '1510';
    expSel.value   = '6500';
  }

  calcDeprPreview();
  openOverlay('ov-depr');
}

function calcDeprPreview() {
  var purch = _deprAssetId ? DB.purch.find(function(p){return p.id===_deprAssetId;}) : null;
  if(!purch) return;

  var rate      = parseFloat(document.getElementById('depr-rate').value)||10;
  var residual  = parseFloat(document.getElementById('depr-residual').value)||0;
  var freq      = document.getElementById('depr-freq').value;
  var startStr  = document.getElementById('depr-start').value;
  var depreciable = purch.net - residual;
  if(depreciable <= 0) depreciable = 0;

  // Rate = useful life in years (e.g. rate=10 → 10 years; rate=2 → 2 years)
  // Annual amount = depreciable / rate
  // Period amount = annual / periodsPerYear
  var periodsPerYear = freq === 'monthly' ? 12 : freq === 'quarterly' ? 4 : 1;
  var annualAmt  = depreciable / (rate || 1);
  var periodAmt  = annualAmt / periodsPerYear;
  var totalPeriods = periodsPerYear * (rate || 1); // total periods = years * periods/year

  var annualStr = depreciable > 0 ? f(annualAmt)+'/yr' : '—';
  document.getElementById('depr-life').textContent = annualStr + ' (' + f(periodAmt) + '/period)';
  document.getElementById('depr-total-depreciable').textContent = f(depreciable);
  document.getElementById('depr-per-period').textContent = f(periodAmt);

  // Build schedule preview
  var preview = document.getElementById('depr-schedule-preview');
  if(!startStr || !periodAmt) {
    preview.innerHTML = '<div style="color:var(--text3);font-size:12px;text-align:center;padding:16px;">Fill in all fields to see the schedule.</div>';
    return;
  }

  var rows = '';
  var cumDepr = 0;
  var maxRows = Math.min(totalPeriods, 12);
  var d = new Date(startStr);
  var freqMonths = freq==='monthly' ? 1 : freq==='quarterly' ? 3 : 12;

  for(var i=0; i<maxRows; i++) {
    var dateStr = d.toISOString().slice(0,10);
    var thisAmt = Math.min(periodAmt, depreciable - cumDepr);
    if(thisAmt <= 0) break;
    cumDepr += thisAmt;
    var remaining = Math.max(0, depreciable - cumDepr);
    rows += '<div class="depr-schedule-row">' +
      '<span style="color:var(--text3);min-width:90px;">' + dateStr + '</span>' +
      '<span style="color:var(--text2);">Period '+(i+1)+'</span>' +
      '<span style="color:var(--red);">(' + f(thisAmt) + ')</span>' +
      '<span style="color:var(--text3);">Accum: '+f(cumDepr)+'</span>' +
      '<span style="color:var(--text2);">NBV: '+f(purch.net-cumDepr)+'</span>' +
    '</div>';
    d.setMonth(d.getMonth() + freqMonths);
  }
  if(totalPeriods > 12) {
    rows += '<div style="text-align:center;color:var(--text3);font-size:11px;padding:8px;">... and '+(totalPeriods-12)+' more periods until fully depreciated</div>';
  }
  preview.innerHTML = rows || '<div style="color:var(--text3);font-size:12px;text-align:center;padding:12px;">Rate too high or no depreciable amount.</div>';
}

function saveDeprPlan() {
  var purch = _deprAssetId ? DB.purch.find(function(p){return p.id===_deprAssetId;}) : null;
  if(!purch) { closeOverlay('ov-depr'); return; }

  var rate      = parseFloat(document.getElementById('depr-rate').value)||10;
  var residual  = parseFloat(document.getElementById('depr-residual').value)||0;
  var freq      = document.getElementById('depr-freq').value;
  var startStr  = document.getElementById('depr-start').value;
  var accumAcc  = document.getElementById('depr-accum-acc').value;
  var expAcc    = document.getElementById('depr-exp-acc').value;
  var depreciable = purch.net - residual;
  var periodsPerYear = freq==='monthly' ? 12 : freq==='quarterly' ? 4 : 1;
  var annualAmt   = depreciable / (rate || 1);
  var periodAmt   = annualAmt / periodsPerYear;
  var freqMonths  = freq==='monthly' ? 1 : freq==='quarterly' ? 3 : 12;
  var totalPeriods = periodsPerYear * (rate || 1);

  var plan = {
    id:           DB.ids.dp++,
    purchaseId:   purch.id,
    assetName:    purch.assetName || purch.desc,
    assetValue:   purch.net,
    residual:     residual,
    depreciable:  depreciable,
    rate:         rate,
    freq:         freq,
    startDate:    startStr,
    accumAcc:     accumAcc,
    expAcc:       expAcc,
    periodAmt:    periodAmt,
    totalPeriods: totalPeriods,
    periodsPosted:0,
    status:       'active',
    createdAt:    td()
  };

  if(!DB.deprPlans) DB.deprPlans = [];
  DB.deprPlans.push(plan);

  // Generate all depreciation JEs up to today
  var generated = generateDeprJEs(plan, true);

  sv();
  closeOverlay('ov-depr');
  renderAll();
  showToast('✅ Depreciation plan created — ' + generated + ' JEs generated');
}

function generateDeprJEs(plan, upToToday) {
  var generated = 0;
  var d = new Date(plan.startDate);
  var freqMonths = plan.freq==='monthly' ? 1 : plan.freq==='quarterly' ? 3 : 12;
  var cumDepr = 0;
  var today = td();

  for(var i=0; i<plan.totalPeriods; i++) {
    var dateStr = d.toISOString().slice(0,10);
    if(upToToday && dateStr > today) break;
    var thisAmt = Math.min(plan.periodAmt, plan.depreciable - cumDepr);
    if(thisAmt <= 0.005) break;
    cumDepr += thisAmt;

    // JE: Dr Depreciation Expense / Cr Accumulated Depreciation
    DB.je.push({
      id:         DB.ids.j++,
      date:       dateStr,
      desc:       'Depreciation — ' + plan.assetName + ' (period '+(i+1)+')',
      lines: [
        {account: plan.expAcc,   debit: thisAmt, credit: 0},
        {account: plan.accumAcc, debit: 0, credit: thisAmt}
      ],
      amount:     thisAmt,
      auto:       true,
      sourceType: 'depreciation',
      planId:     plan.id
    });
    plan.periodsPosted = i + 1;
    generated++;
    d.setMonth(d.getMonth() + freqMonths);
  }
  return generated;
}

function skipDeprPlan() {
  _deprAssetId = null;
  closeOverlay('ov-depr');
  showToast('ℹ️ Asset saved without depreciation plan. You can add one later.');
}

// Process pending depreciation JEs on startup
function processDeprPlans() {
  if(!DB.deprPlans) return 0;
  var total = 0;
  var today = td();
  DB.deprPlans.forEach(function(plan){
    if(plan.status !== 'active') return;
    // Find last posted JE for this plan
    var planJEs = DB.je.filter(function(je){return je.planId===plan.id;});
    var lastDate = planJEs.length > 0
      ? planJEs.map(function(je){return je.date;}).sort().pop()
      : null;

    // Find next date to post from
    var d = new Date(plan.startDate);
    var freqMonths = plan.freq==='monthly' ? 1 : plan.freq==='quarterly' ? 3 : 12;
    // Advance past already-posted periods
    for(var i=0; i<planJEs.length; i++){
      d.setMonth(d.getMonth() + freqMonths);
    }

    var cumDepr = planJEs.reduce(function(a,je){return a+(je.amount||0);},0);
    var periodIdx = planJEs.length;

    while(periodIdx < plan.totalPeriods) {
      var dateStr = d.toISOString().slice(0,10);
      if(dateStr > today) break;
      var thisAmt = Math.min(plan.periodAmt, plan.depreciable - cumDepr);
      if(thisAmt <= 0.005) { plan.status='completed'; break; }
      cumDepr += thisAmt;
      DB.je.push({
        id: DB.ids.j++, date: dateStr,
        desc: 'Depreciation — ' + plan.assetName + ' (period '+(periodIdx+1)+')',
        lines:[
          {account:plan.expAcc,   debit:thisAmt, credit:0},
          {account:plan.accumAcc, debit:0, credit:thisAmt}
        ],
        amount:thisAmt, auto:true, sourceType:'depreciation', planId:plan.id
      });
      plan.periodsPosted = periodIdx + 1;
      periodIdx++;
      total++;
      d.setMonth(d.getMonth() + freqMonths);
    }
    if(cumDepr >= plan.depreciable - 0.01) plan.status = 'completed';
  });
  return total;
}


// ── Edit Purchase ────────────────────────────────────────────────
var _peId = null;

function onEditPurchTypeChange(val) {
  var assetRow = document.getElementById('pe-asset-name-row');
  if(assetRow) assetRow.style.display = val==='asset' ? '' : 'none';
  // Update category options
  var catSel = document.getElementById('pe-cat');
  if(!catSel) return;
  if(val === 'asset') {
    var planId = (DB.co && DB.co.accountPlan) || 'usgaap';
    if(planId === 'pgc') {
      catSel.innerHTML =
        '<optgroup label="Inmovilizado Material">' +
        '<option value="210">210 — Terrenos y bienes naturales</option>' +
        '<option value="211">211 — Construcciones</option>' +
        '<option value="212">212 — Instalaciones técnicas</option>' +
        '<option value="213">213 — Maquinaria</option>' +
        '<option value="214">214 — Utillaje</option>' +
        '<option value="215">215 — Otras instalaciones</option>' +
        '<option value="216">216 — Mobiliario</option>' +
        '<option value="217">217 — Equipos para procesos de información</option>' +
        '<option value="218">218 — Elementos de transporte</option>' +
        '<option value="219">219 — Otro inmovilizado material</option>' +
        '<option value="221">221 — Inversiones en construcciones</option>' +
        '</optgroup>' +
        '<optgroup label="Inmovilizado Intangible">' +
        '<option value="200">200 — Investigación</option>' +
        '<option value="201">201 — Desarrollo</option>' +
        '<option value="202">202 — Concesiones administrativas</option>' +
        '<option value="203">203 — Propiedad industrial</option>' +
        '<option value="204">204 — Fondo de comercio</option>' +
        '<option value="205">205 — Derechos de traspaso</option>' +
        '<option value="206">206 — Aplicaciones informáticas</option>' +
        '<option value="209">209 — Anticipos inmovilizaciones intangibles</option>' +
        '</optgroup>';
    } else {
      catSel.innerHTML =
        '<option value="1500">1500 — Fixed Assets (General)</option>' +
        '<option value="1510">1510 — Equipment</option>' +
        '<option value="1520">1520 — Furniture & Fixtures</option>' +
        '<option value="1530">1530 — Vehicles</option>' +
        '<option value="1540">1540 — Buildings</option>' +
        '<option value="1550">1550 — Land</option>' +
        '<option value="1560">1560 — Intangible Assets</option>';
    }
  } else {
    catSel.innerHTML =
      '<option value="COGS">Cost of Goods Sold</option>' +
      '<option value="Rent">Rent</option>' +
      '<option value="Salaries">Salaries</option>' +
      '<option value="Utilities">Utilities</option>' +
      '<option value="Marketing">Marketing</option>' +
      '<option value="Professional">Professional Services</option>' +
      '<option value="Depreciation">Depreciation</option>' +
      '<option value="Other OpEx">Other OpEx</option>';
  }
}

function openEditPurch(purchId) {
  _peId = purchId;
  var p = DB.purch.find(function(x){return x.id===purchId;});
  if(!p) return;
  document.getElementById('pe-date').value   = p.date   || '';
  document.getElementById('pe-num').value    = p.num    || '';
  document.getElementById('pe-sup').value    = p.supplier || '';
  document.getElementById('pe-desc').value   = p.desc   || '';
  document.getElementById('pe-net').value    = p.net    || 0;
  document.getElementById('pe-vat').value    = String(p.vatRate || 21);
  document.getElementById('pe-stat').value   = p.status || 'pending';
  document.getElementById('pe-meth').value   = p.method || 'bank';
  document.getElementById('pe-invtype').value= p.invType || 'expense';
  document.getElementById('pe-asset-name').value = p.assetName || '';
  // Trigger type change to set correct category options
  onEditPurchTypeChange(p.invType || 'expense');
  // Set saved category
  var catSel = document.getElementById('pe-cat');
  if(catSel) catSel.value = p.cat || '';
  calcPE();
  openOverlay('ov-purch-edit');
}

function calcPE() {
  var net = parseFloat(document.getElementById('pe-net').value)||0;
  var vat = parseFloat(document.getElementById('pe-vat').value)||0;
  var va  = net*vat/100;
  document.getElementById('pe-vatamt').value = va.toFixed(2);
  document.getElementById('pe-total').value  = (net+va).toFixed(2);
}

function saveEditPurch() {
  if(!_peId) return;
  var p = DB.purch.find(function(x){return x.id===_peId;});
  if(!p) return;
  var net = parseFloat(document.getElementById('pe-net').value)||0;
  var vat = parseFloat(document.getElementById('pe-vat').value)||0;
  var va  = net*vat/100;
  p.date      = document.getElementById('pe-date').value;
  p.num       = document.getElementById('pe-num').value;
  p.supplier  = document.getElementById('pe-sup').value;
  p.desc      = document.getElementById('pe-desc').value;
  p.cat       = document.getElementById('pe-cat').value;
  p.net       = net;
  p.vatRate   = vat;
  p.vatAmt    = va;
  p.total     = net+va;
  p.status    = document.getElementById('pe-stat').value;
  p.method    = document.getElementById('pe-meth').value;
  p.invType   = document.getElementById('pe-invtype').value;
  p.assetName = document.getElementById('pe-asset-name').value;
  sv();
  closeOverlay('ov-purch-edit');
  rPurch();
  showToast('✅ Purchase updated: '+p.num);
}


// ══════════════════════════════════════════════════════════════════
// CFO INTELLIGENCE MODULE
// ══════════════════════════════════════════════════════════════════

function initCFOYear() {
  var sel = document.getElementById('cfo-year');
  if(!sel) return;
  var now = new Date().getFullYear();
  sel.innerHTML = '';
  for(var y=now; y>=now-4; y--) {
    var o = document.createElement('option');
    o.value = y; o.textContent = y;
    if(y===now) o.selected = true;
    sel.appendChild(o);
  }
}

function rCFO() {
  initCFOYear();
  var sel = document.getElementById('cfo-year');
  var year = sel ? parseInt(sel.value) : new Date().getFullYear();

  document.getElementById('cfo-chart-year').textContent = year;

  var F  = cF();       // full period financials
  var FA = cFAll();    // all-time for BS ratios

  renderCFOKPIs(F, FA, year);
  renderCFORevChart(year);
  renderCFORatios(F, FA);
  renderCFOCohorts(year);
  renderCFOMRR();
  renderCFORunway(F, FA);
}

// cFAll — all-time BS snapshot (no date filter)
function cFAll() {
  var _p = getActivePlan();
  var bsB = {};
  DB.je.forEach(function(je){
    je.lines.forEach(function(l){
      if(!bsB[l.account]) bsB[l.account] = {dr:0,cr:0};
      bsB[l.account].dr += (l.debit||0);
      bsB[l.account].cr += (l.credit||0);
    });
  });
  function bal(acc) {
    var b = bsB[acc]; if(!b) return 0;
    var a = COA.find(function(x){return x.c===acc;});
    if(!a) return b.dr - b.cr;
    return (a.t==='asset'||a.t==='expense') ? b.dr-b.cr : b.cr-b.dr;
  }
  function sumBal(accs) { return accs.reduce(function(s,a){return s+bal(a);},0); }

  var cash    = sumBal(_p.cashAccts);
  var ar      = sumBal(_p.arAccts);
  var vatRec  = _p.id==='pgc' ? bal('472') : 0;
  var tca     = cash + ar + vatRec;

  // Fixed assets net
  var grossFixed=0, accumD=0;
  DB.je.forEach(function(je){ je.lines.forEach(function(l){
    var n=parseInt(l.account);
    if(_p.id==='pgc'){
      if(n>=200&&n<=221&&!(n>=280&&n<=289)) grossFixed+=(l.debit||0)-(l.credit||0);
      if(n>=280&&n<=289) accumD+=(l.credit||0)-(l.debit||0);
    } else {
      if(n>=1500&&n<=1570&&l.account!=='1510') grossFixed+=(l.debit||0)-(l.credit||0);
      if(l.account==='1510') accumD+=(l.credit||0)-(l.debit||0);
    }
  });});
  var fixedNet = Math.max(0, grossFixed - accumD);
  var ta = tca + fixedNet;

  var ap   = sumBal(_p.apAccts);
  var vatP = sumBal(_p.vatAccts);
  var vatNet = Math.max(0, vatP - vatRec);
  var tcl  = ap + vatNet;
  var ltd  = sumBal(_p.ltDebtAccts||[]);
  var tl   = tcl + ltd;
  var eq   = sumBal(_p.capitalAccts||[]);

  // P&L all time
  var revB={};
  DB.je.forEach(function(je){je.lines.forEach(function(l){
    if(!revB[l.account]) revB[l.account]={dr:0,cr:0};
    revB[l.account].dr+=(l.debit||0); revB[l.account].cr+=(l.credit||0);
  });});
  function plBal(acc){ var b=revB[acc]; if(!b)return 0; var a=COA.find(function(x){return x.c===acc;}); if(!a)return b.dr-b.cr; return a.t==='revenue'?b.cr-b.dr:b.dr-b.cr; }
  var rev   = _p.revAccts.reduce(function(s,a){return s+plBal(a);},0);
  var cogs  = _p.cogsAccts.reduce(function(s,a){return s+plBal(a);},0);
  var opex  = _p.opexAccts.reduce(function(s,a){return s+plBal(a);},0);
  var finExp= (_p.finExpAccts||[]).reduce(function(s,a){return s+plBal(a);},0);
  var ni    = rev - cogs - opex - finExp;

  return {cash:cash, ar:ar, tca:tca, fixedNet:fixedNet, ta:ta,
          ap:ap, tcl:tcl, tl:tl, eq:eq,
          rev:rev, cogs:cogs, opex:opex, finExp:finExp, ni:ni};
}

// ── KPI Row ───────────────────────────────────────────────────────
function renderCFOKPIs(F, FA, year) {
  var el = document.getElementById('cfo-kpis');
  if(!el) return;

  // MRR from recurring
  var mrr = (DB.recurring||[]).filter(function(r){return r.status==='active';}).reduce(function(a,r){
    var fac={daily:30,weekly:4.33,biweekly:2.17,monthly:1,bimonthly:.5,quarterly:.33,biannual:.17,annually:.083};
    return a + r.total*(fac[r.interval]||1);
  },0);

  var totExp = (FA.cogs||0) + (FA.opex||0) + (FA.finExp||0);

  var kpis = [
    { label:'Annual Revenue',  value:f(FA.rev),    sub:'All time · from JE',          color:'#c8ff00',                               icon:'📊' },
    { label:'Total Expenses',  value:f(totExp),    sub:'COGS + OpEx + Financial',      color:'var(--red)',                            icon:'📉' },
    { label:'Net Income',      value:f(FA.ni),     sub:'Revenue − Expenses',           color: FA.ni>=0?'var(--green)':'var(--red)',   icon:'📈' },
    { label:'MRR',             value:f(mrr),       sub:'Monthly Recurring Revenue',    color:'#0E9AA7',                               icon:'🔁' },
    { label:'Cash & Bank',     value:f(FA.cash),   sub:'Current balance',              color:'var(--green)',                          icon:'💰' },
  ];

  // Override grid to 5 cols when we have 5 KPIs
  el.style.gridTemplateColumns = 'repeat(5,1fr)';

  el.innerHTML = kpis.map(function(k){
    return '<div class="cfo-kpi">'+
      '<div class="cfo-kpi-accent" style="background:'+k.color+';"></div>'+
      '<div class="cfo-kpi-label">'+k.icon+' '+k.label+'</div>'+
      '<div class="cfo-kpi-value" style="color:'+k.color+';">'+k.value+'</div>'+
      '<div class="cfo-kpi-sub">'+k.sub+'</div>'+
    '</div>';
  }).join('');
}

// ── Revenue vs Net Result SVG bar chart ───────────────────────────
function renderCFORevChart(year) {
  var el = document.getElementById('cfo-rev-chart');
  if(!el) return;
  var _p = getActivePlan();
  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];

  // Compute monthly rev and ni
  var data = months.map(function(mn, i){
    var m  = i+1;
    var from = year+'-'+(m<10?'0':'')+m+'-01';
    var to   = year+'-'+(m<10?'0':'')+m+'-'+(new Date(year,m,0).getDate());
    var fd   = cFForRange(from, to);
    return { month:mn, rev:fd.rev, ni:fd.ni };
  });

  var maxV = Math.max.apply(null, data.map(function(d){return Math.max(d.rev, Math.abs(d.ni), 1);}));
  var W=560, H=180, pad=32, barW=18, gap=24;
  var scale = function(v){ return H - (Math.abs(v)/maxV)*H*0.9; };
  var baseline = H;

  var svg = '<svg viewBox="0 0 '+W+' '+(H+40)+'" class="bar-chart-svg" xmlns="http://www.w3.org/2000/svg">';
  // Baseline
  svg += '<line x1="'+pad+'" y1="'+baseline+'" x2="'+(W-10)+'" y2="'+baseline+'" stroke="var(--border)" stroke-width="1"/>';
  // Grid lines
  [0.25,0.5,0.75].forEach(function(t){
    var y = H*(1-t*0.9);
    svg += '<line x1="'+pad+'" y1="'+y+'" x2="'+(W-10)+'" y2="'+y+'" stroke="var(--border)" stroke-dasharray="3,3" stroke-width="0.5"/>';
    svg += '<text x="'+(pad-4)+'" y="'+(y+4)+'" fill="var(--text3)" font-size="8" text-anchor="end">'+f(maxV*t)+'</text>';
  });

  data.forEach(function(d, i){
    var x = pad + i*(barW*2+gap);
    // Revenue bar
    var revH = Math.max(2, (d.rev/maxV)*H*0.9);
    svg += '<rect x="'+x+'" y="'+(H-revH)+'" width="'+barW+'" height="'+revH+'" fill="var(--accent)" opacity="0.85" rx="3"/>';
    // Net result bar
    var niH  = Math.max(2, (Math.abs(d.ni)/maxV)*H*0.9);
    var niY  = d.ni >= 0 ? H-niH : H;
    var niCol= d.ni >= 0 ? '#0E9AA7' : 'var(--red)';
    svg += '<rect x="'+(x+barW+2)+'" y="'+niY+'" width="'+barW+'" height="'+niH+'" fill="'+niCol+'" opacity="0.85" rx="3"/>';
    // Month label
    svg += '<text x="'+(x+barW)+'" y="'+(H+14)+'" fill="var(--text3)" font-size="9" text-anchor="middle">'+d.month+'</text>';
  });

  // Legend
  svg += '<rect x="'+pad+'" y="'+(H+24)+'" width="10" height="10" fill="var(--accent)" rx="2"/>';
  svg += '<text x="'+(pad+13)+'" y="'+(H+33)+'" fill="var(--text2)" font-size="9">Revenue</text>';
  svg += '<rect x="'+(pad+70)+'" y="'+(H+24)+'" width="10" height="10" fill="#0E9AA7" rx="2"/>';
  svg += '<text x="'+(pad+83)+'" y="'+(H+33)+'" fill="var(--text2)" font-size="9">Net Result</text>';

  svg += '</svg>';
  el.innerHTML = svg;
}

// ── Financial Ratios ───────────────────────────────────────────────
function renderCFORatios(F, FA) {
  var el = document.getElementById('cfo-ratios');
  if(!el) return;

  // Solvency = Current Assets / Current Liabilities
  var solvency = FA.tcl > 0 ? FA.tca/FA.tcl : null;
  // Collateral = Total Assets / Total Liabilities
  var collateral = FA.tl > 0 ? FA.ta/FA.tl : null;
  // ROE = Net Income / Equity
  var roe = FA.eq > 0 ? (FA.ni/FA.eq)*100 : null;
  // Collection Period = (AR / Revenue) * 365
  var collPeriod = FA.rev > 0 ? (FA.ar/FA.rev)*365 : null;

  function ratioStatus(val, good, warn, isHighGood) {
    if(val===null) return 'neu';
    if(isHighGood) return val>=good?'up':val>=warn?'neu':'down';
    return val<=good?'up':val<=warn?'neu':'down';
  }
  function ratioColor(status) {
    return status==='up'?'var(--green)':status==='down'?'var(--red)':'var(--yellow)';
  }

  var ratios = [
    {
      name:'Solvency Ratio', formula:'Current Assets / Current Liabilities',
      val: solvency, fmt: solvency ? solvency.toFixed(2)+'x' : '—',
      status: ratioStatus(solvency, 2, 1, true),
      tip: solvency ? (solvency>=2?'Strong':solvency<1?'Critical':'Acceptable') : 'No liabilities'
    },
    {
      name:'Collateral Ratio', formula:'Total Assets / Total Liabilities',
      val: collateral, fmt: collateral ? collateral.toFixed(2)+'x' : '—',
      status: ratioStatus(collateral, 1.5, 1, true),
      tip: collateral ? (collateral>=1.5?'Healthy':'Low') : '—'
    },
    {
      name:'ROE', formula:'Net Income / Equity × 100',
      val: roe, fmt: roe !== null ? roe.toFixed(1)+'%' : '—',
      status: ratioStatus(roe, 10, 0, true),
      tip: roe !== null ? (roe>=10?'Excellent':roe>=0?'Positive':'Loss') : '—'
    },
    {
      name:'Collection Period', formula:'(AR / Revenue) × 365',
      val: collPeriod, fmt: collPeriod !== null ? Math.round(collPeriod)+' days' : '—',
      status: ratioStatus(collPeriod, 30, 60, false),
      tip: collPeriod !== null ? (collPeriod<=30?'Excellent':collPeriod<=60?'Good':'Slow') : '—'
    }
  ];

  el.innerHTML = ratios.map(function(r){
    var col = ratioColor(r.status);
    var icon = r.status==='up'?'↑':r.status==='down'?'↓':'→';
    return '<div class="ratio-card">'+
      '<div class="ratio-name">'+r.name+'</div>'+
      '<div class="ratio-val" style="color:'+col+';">'+r.fmt+'</div>'+
      '<div class="ratio-formula">'+r.formula+'</div>'+
      '<div class="ratio-status" style="background:'+col+'20;color:'+col+';">'+icon+' '+r.tip+'</div>'+
    '</div>';
  }).join('');
}

// ── Customer Cohort Analysis ──────────────────────────────────────
function renderCFOCohorts(year) {
  var body = document.getElementById('cfo-cohort-body');
  var chartEl = document.getElementById('cfo-cohort-chart');
  if(!body) return;

  var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  var cohorts = [];

  // For each month, find unique customers who had a sale
  var prevActive = new Set();
  months.forEach(function(mn, i){
    var m    = i+1;
    var from = year+'-'+(m<10?'0':'')+m+'-01';
    var to   = year+'-'+(m<10?'0':'')+m+'-'+(new Date(year,m,0).getDate());
    var sales = DB.sales.filter(function(s){ return s.date>=from && s.date<=to; });
    var activeSet = new Set(sales.map(function(s){return s.customer;}));

    var newCust = 0, churned = 0;
    activeSet.forEach(function(c){ if(!prevActive.has(c)) newCust++; });
    prevActive.forEach(function(c){ if(!activeSet.has(c)) churned++; });

    var retention = prevActive.size > 0
      ? Math.round(((prevActive.size - churned)/prevActive.size)*100)
      : null;

    cohorts.push({
      month: mn,
      active: activeSet.size,
      newC:   newCust,
      churned: churned,
      total:  activeSet.size,
      retention: retention
    });
    prevActive = activeSet;
  });

  // Mini bar chart for cohort
  var maxA = Math.max.apply(null, cohorts.map(function(d){return d.active||0;})) || 1;
  var cW=520, cH=60;
  var bw=28, cgap=12;
  var cSvg = '<svg viewBox="0 0 '+cW+' '+(cH+20)+'" class="bar-chart-svg">';
  cohorts.forEach(function(d,i){
    var x = i*(bw+cgap)+10;
    // Active (teal)
    var ah = Math.max(2, (d.active/maxA)*cH*0.9);
    cSvg += '<rect x="'+x+'" y="'+(cH-ah)+'" width="'+(bw*.45)+'" height="'+ah+'" fill="#0E9AA7" rx="2" opacity=".85"/>';
    // New (lime)
    var nh = Math.max(0, (d.newC/maxA)*cH*0.9);
    if(nh>0) cSvg += '<rect x="'+(x+bw*.48)+'" y="'+(cH-nh)+'" width="'+(bw*.45)+'" height="'+nh+'" fill="var(--accent)" rx="2" opacity=".85"/>';
    cSvg += '<text x="'+(x+bw*.45)+'" y="'+(cH+13)+'" fill="var(--text3)" font-size="8" text-anchor="middle">'+d.month+'</text>';
  });
  cSvg += '<rect x="10" y="'+(cH+16)+'" width="8" height="6" fill="#0E9AA7" rx="1"/><text x="21" y="'+(cH+21)+'" fill="var(--text3)" font-size="8">Active</text>';
  cSvg += '<rect x="65" y="'+(cH+16)+'" width="8" height="6" fill="var(--accent)" rx="1"/><text x="76" y="'+(cH+21)+'" fill="var(--text3)" font-size="8">New</text>';
  cSvg += '</svg>';
  if(chartEl) chartEl.innerHTML = cSvg;

  // Table rows
  body.innerHTML = cohorts.filter(function(d){return d.active>0||d.churned>0;}).map(function(d){
    var retStr = d.retention!==null ? d.retention+'%' : '—';
    var retCol = d.retention===null?'var(--text3)':d.retention>=80?'var(--green)':d.retention>=50?'var(--yellow)':'var(--red)';
    return '<tr>'+
      '<td style="font-weight:600;color:var(--text);">'+d.month+' '+year+'</td>'+
      '<td><span class="cohort-dot" style="background:#0E9AA7;"></span>'+d.active+'</td>'+
      '<td><span class="cohort-dot" style="background:var(--accent);"></span>'+d.newC+'</td>'+
      '<td><span class="cohort-dot" style="background:var(--red);"></span>'+d.churned+'</td>'+
      '<td style="font-weight:600;">'+d.total+'</td>'+
      '<td style="color:'+retCol+';font-weight:700;">'+retStr+'</td>'+
    '</tr>';
  }).join('') || '<tr><td colspan="6" style="text-align:center;color:var(--text3);padding:20px;">No sales data for '+year+'</td></tr>';
}

// ── MRR Detail ────────────────────────────────────────────────────
function renderCFOMRR() {
  var el = document.getElementById('cfo-mrr-detail');
  if(!el) return;
  var active = (DB.recurring||[]).filter(function(r){return r.status==='active';});
  if(!active.length) {
    el.innerHTML = '<div style="color:var(--text3);font-size:12px;padding:12px 0;">No active recurring invoices.</div>';
    return;
  }
  var fac={daily:30,weekly:4.33,biweekly:2.17,monthly:1,bimonthly:.5,quarterly:.33,biannual:.17,annually:.083};
  var total = active.reduce(function(s,r){return s+r.total*(fac[r.interval]||1);},0);
  el.innerHTML = active.slice(0,6).map(function(r){
    var mth = r.total*(fac[r.interval]||1);
    var pct = Math.round((mth/total)*100);
    return '<div style="margin-bottom:10px;">'+
      '<div style="display:flex;justify-content:space-between;margin-bottom:4px;">'+
        '<span style="font-size:12px;color:var(--text2);">'+r.customer+'</span>'+
        '<span style="font-size:12px;font-weight:700;color:var(--accent);">'+f(mth)+'/mo</span>'+
      '</div>'+
      '<div style="height:4px;background:var(--surface3);border-radius:2px;">'+
        '<div style="height:4px;width:'+pct+'%;background:linear-gradient(90deg,var(--accent),#0E9AA7);border-radius:2px;transition:width .3s;"></div>'+
      '</div>'+
    '</div>';
  }).join('') +
  '<div style="display:flex;justify-content:space-between;padding-top:10px;border-top:1px solid var(--border);margin-top:4px;">'+
    '<span style="font-size:12px;color:var(--text3);">Total MRR</span>'+
    '<span style="font-size:16px;font-weight:800;color:var(--accent);">'+f(total)+'</span>'+
  '</div>';
}

// ── Cash Runway ───────────────────────────────────────────────────
function renderCFORunway(F, FA) {
  var el = document.getElementById('cfo-runway');
  if(!el) return;
  var cash = FA.cash;
  // Monthly burn = average monthly OpEx over last 3 months
  var now = new Date();
  var burnSamples = [];
  for(var i=1; i<=3; i++){
    var d = new Date(now.getFullYear(), now.getMonth()-i, 1);
    var from = d.getFullYear()+'-'+(d.getMonth()+1<10?'0':'')+(d.getMonth()+1)+'-01';
    var lastD = new Date(d.getFullYear(), d.getMonth()+1, 0).getDate();
    var to   = d.getFullYear()+'-'+(d.getMonth()+1<10?'0':'')+(d.getMonth()+1)+'-'+lastD;
    var fd   = cFForRange(from, to);
    burnSamples.push(fd.toOpEx + fd.cogs);
  }
  var avgBurn = burnSamples.reduce(function(a,b){return a+b;},0)/3;
  var runway  = avgBurn > 0 ? Math.floor(cash/avgBurn) : null;

  var col = runway===null?'var(--text3)':runway>=12?'var(--green)':runway>=6?'var(--yellow)':'var(--red)';
  var msg = runway===null?'No burn data':'months runway';

  el.innerHTML =
    '<div style="text-align:center;padding:16px 0;">'+
      '<div style="font-size:52px;font-weight:900;color:'+col+';line-height:1;">'+(runway!==null?runway:'∞')+'</div>'+
      '<div style="font-size:14px;color:var(--text3);margin-top:6px;">'+msg+'</div>'+
      (avgBurn>0?'<div style="font-size:12px;color:var(--text3);margin-top:8px;">Avg monthly burn: <strong style="color:var(--text);">'+f(avgBurn)+'</strong></div>':'<div style="font-size:12px;color:var(--text3);margin-top:8px;">Record expenses to calculate runway</div>')+
      '<div style="font-size:12px;color:var(--text3);margin-top:4px;">Cash balance: <strong style="color:var(--green);">'+f(cash)+'</strong></div>'+
    '</div>';
}

// ══════════════════════════════════════════════════════════════════
// TESORERÍA NAV GROUP
// ══════════════════════════════════════════════════════════════════
var _tesoreriaOpen = false;

function toggleTesoreriaNav() {
  _tesoreriaOpen = !_tesoreriaOpen;
  var sub   = document.getElementById('nav-tesoreria-sub');
  var arrow = document.getElementById('nav-tesoreria-arrow');
  sub.style.display   = _tesoreriaOpen ? 'block' : 'none';
  arrow.style.transform = _tesoreriaOpen ? 'rotate(90deg)' : 'rotate(0deg)';
}

function navTesoreria(sub) {
  // Make sure group is open
  if (!_tesoreriaOpen) toggleTesoreriaNav();
  // Clear active state from all subitems, then set this one
  document.querySelectorAll('.nav-subitem').forEach(function(e){ e.classList.remove('active'); });
  var items = document.querySelectorAll('.nav-subitem');
  items.forEach(function(el){
    if (el.textContent.trim().toLowerCase().indexOf(sub) !== -1) el.classList.add('active');
  });
  nav(sub);
}

// ══════════════════════════════════════════════════════════════════
// WIRE TRANSFERS MODULE
// ══════════════════════════════════════════════════════════════════
var _wtLastCreated = null; // track last created wire for download

function openWireTransfers() {
  // Expand tesoreria nav if not open
  if (!_tesoreriaOpen) toggleTesoreriaNav();
  document.querySelectorAll('.nav-subitem').forEach(function(e){ e.classList.remove('active'); });
  document.getElementById('ov-wire-transfers').classList.add('open');
  wtTab('list');
  renderWTHistory();
}

function closeWireTransfers() {
  document.getElementById('ov-wire-transfers').classList.remove('open');
}

function wtTab(tab) {
  ['list','out','in'].forEach(function(t){
    document.getElementById('wt-panel-'+t).style.display = 'none';
    document.getElementById('wt-tab-'+t).classList.remove('active');
  });
  document.getElementById('wt-panel-'+tab).style.display = tab === 'list' ? 'flex' : 'flex';
  document.getElementById('wt-panel-'+tab).style.flexDirection = tab === 'list' ? 'column' : 'row';
  document.getElementById('wt-tab-'+tab).classList.add('active');
  if (tab === 'out') { renderWTOut(); setWTDates('out'); }
  if (tab === 'in')  { renderWTIn();  setWTDates('in');  }
  if (tab === 'list') renderWTHistory();
}

function setWTDates(dir) {
  var t = td();
  document.getElementById('wt-'+dir+'-date').value = t;
  document.getElementById('wt-'+dir+'-due').value  = t;
}

// ── Render pending purchases for outbound ─────────────────────────
function renderWTOut() {
  var search = (document.getElementById('wt-out-search').value || '').toLowerCase();
  var pending = DB.purch.filter(function(p){
    var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
    var rem = p.total - paid;
    if (rem < 0.01) return false;
    if (search && p.supplier.toLowerCase().indexOf(search) === -1 && p.num.toLowerCase().indexOf(search) === -1) return false;
    return true;
  });

  var tbody = document.getElementById('wt-out-tbl');
  if (!pending.length) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No pending purchase invoices.</td></tr>';
    wtUpdateTotal('out');
    return;
  }

  tbody.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(p){
    var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
    var rem  = p.total - paid;
    var due  = p.dueDate || p.date;
    return '<tr>' +
      '<td><input type="checkbox" class="wt-out-chk" value="'+p.id+'" onchange="wtUpdateTotal(\'out\')"></td>' +
      '<td><span style="font-family:monospace;font-size:11px;color:var(--red);">'+p.num+'</span></td>' +
      '<td style="font-size:12px;">'+p.date+'</td>' +
      '<td style="font-weight:600;color:var(--text);">'+p.supplier+'</td>' +
      '<td style="color:var(--text3);font-size:12px;">'+(p.desc||'—')+'</td>' +
      '<td style="font-size:12px;color:var(--text3);">'+(due||'—')+'</td>' +
      '<td class="amt">'+f(p.total)+'</td>' +
      '<td class="amt" style="color:var(--yellow);">'+f(rem)+'</td>' +
    '</tr>';
  }).join('');
  wtUpdateTotal('out');
}

// ── Render pending sales for inbound ──────────────────────────────
function renderWTIn() {
  var search = (document.getElementById('wt-in-search').value || '').toLowerCase();
  var pending = DB.sales.filter(function(s){
    var coll = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
    var rem  = s.total - coll;
    if (rem < 0.01) return false;
    if (search && s.customer.toLowerCase().indexOf(search) === -1 && s.num.toLowerCase().indexOf(search) === -1) return false;
    return true;
  });

  var tbody = document.getElementById('wt-in-tbl');
  if (!pending.length) {
    tbody.innerHTML = '<tr><td colspan="8" style="text-align:center;color:var(--text3);padding:24px;">No pending sales invoices.</td></tr>';
    wtUpdateTotal('in');
    return;
  }

  tbody.innerHTML = pending.sort(function(a,b){return b.id-a.id;}).map(function(s){
    var coll = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
    var rem  = s.total - coll;
    var due  = s.dueDate || s.date;
    return '<tr>' +
      '<td><input type="checkbox" class="wt-in-chk" value="'+s.id+'" onchange="wtUpdateTotal(\'in\')"></td>' +
      '<td><span style="font-family:monospace;font-size:11px;color:var(--accent);">'+s.num+'</span></td>' +
      '<td style="font-size:12px;">'+s.date+'</td>' +
      '<td style="font-weight:600;color:var(--text);">'+s.customer+'</td>' +
      '<td style="color:var(--text3);font-size:12px;">'+(s.desc||'—')+'</td>' +
      '<td style="font-size:12px;color:var(--text3);">'+(due||'—')+'</td>' +
      '<td class="amt">'+f(s.total)+'</td>' +
      '<td class="amt" style="color:var(--green);">'+f(rem)+'</td>' +
    '</tr>';
  }).join('');
  wtUpdateTotal('in');
}

// ── Select/deselect all checkboxes ────────────────────────────────
function wtSelectAll(dir, checked) {
  document.querySelectorAll('.wt-'+dir+'-chk').forEach(function(cb){ cb.checked = checked; });
  wtUpdateTotal(dir);
}

// ── Calculate and display total ───────────────────────────────────
function wtUpdateTotal(dir) {
  var total = 0;
  var count = 0;
  document.querySelectorAll('.wt-'+dir+'-chk:checked').forEach(function(cb){
    var id = parseInt(cb.value);
    if (dir === 'out') {
      var p = DB.purch.find(function(x){return x.id===id;});
      if (p) {
        var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
        total += p.total - paid;
        count++;
      }
    } else {
      var s = DB.sales.find(function(x){return x.id===id;});
      if (s) {
        var coll = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
        total += s.total - coll;
        count++;
      }
    }
  });
  document.getElementById('wt-'+dir+'-total').textContent = f(total);
  document.getElementById('wt-'+dir+'-count').textContent = count;
}

// ── Create Wire Transfer → grouped payment/collection ─────────────
function createWireTransfer(dir) {
  var checked = Array.from(document.querySelectorAll('.wt-'+dir+'-chk:checked'));
  if (!checked.length) { alert('Select at least one invoice.'); return; }

  var concept = document.getElementById('wt-'+dir+'-concept').value || (dir==='out'?'PAYMENTS SUPPLIERS':'REMITTANCES');
  var date    = document.getElementById('wt-'+dir+'-date').value   || td();
  var bank    = document.getElementById('wt-'+dir+'-bank').value   || '';
  var due     = document.getElementById('wt-'+dir+'-due').value    || date;
  var creditor= dir==='in' ? (document.getElementById('wt-in-creditor').value||'') : '';

  if (!DB.wires) DB.wires = [];
  if (!DB.ids.wt) DB.ids.wt = 1;

  var docs = [];
  var totalAmt = 0;

  checked.forEach(function(cb){
    var id = parseInt(cb.value);
    if (dir === 'out') {
      var p = DB.purch.find(function(x){return x.id===id;});
      if (!p) return;
      var paid = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem  = p.total - paid;
      if (rem < 0.01) return;
      docs.push({ num:p.num, party:p.supplier, desc:p.desc||'', amount:rem, date:p.date, due:p.dueDate||p.date });
      // Create payment record for each invoice
      var _pp = getActivePlan();
      DB.pay.push({id:DB.ids.py++, date:date, supplier:p.supplier, ref:p.num, method:'wire', amount:rem, notes:'Wire Transfer — '+concept});
      DB.je.push({id:DB.ids.j++, date:date, desc:'Wire Payment — '+p.supplier+' / '+p.num, lines:[{account:_pp.apAccts[0], debit:rem, credit:0},{account:_pp.cashAccts[0], debit:0, credit:rem}], amount:rem, auto:true, sourceType:'payment'});
      var paid2 = DB.pay.filter(function(x){return x.ref===p.num;}).reduce(function(a,x){return a+x.amount;},0);
      if (paid2 >= p.total - 0.01) p.status = 'paid';
      totalAmt += rem;
    } else {
      var s = DB.sales.find(function(x){return x.id===id;});
      if (!s) return;
      var coll2 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
      var rem2  = s.total - coll2;
      if (rem2 < 0.01) return;
      docs.push({ num:s.num, party:s.customer, desc:s.desc||'', amount:rem2, date:s.date, due:s.dueDate||s.date });
      // Create collection record for each invoice
      var _cp = getActivePlan();
      DB.coll.push({id:DB.ids.c++, date:date, customer:s.customer, ref:s.num, method:'wire', amount:rem2, notes:'Wire Transfer — '+concept});
      DB.je.push({id:DB.ids.j++, date:date, desc:'Wire Collection — '+s.customer+' / '+s.num, lines:[{account:_cp.cashAccts[0], debit:rem2, credit:0},{account:_cp.arAccts[0], debit:0, credit:rem2}], amount:rem2, auto:true, sourceType:'collection'});
      var coll3 = DB.coll.filter(function(x){return x.ref===s.num;}).reduce(function(a,x){return a+x.amount;},0);
      if (coll3 >= s.total - 0.01) s.status = 'paid';
      totalAmt += rem2;
    }
  });

  // Save wire record
  var wire = {
    id: DB.ids.wt++,
    type: dir,
    concept: concept,
    date: date,
    bank: bank,
    due: due,
    creditor: creditor,
    docs: docs,
    total: totalAmt,
    status: 'pending'
  };
  DB.wires.push(wire);
  _wtLastCreated = wire;

  sv();
  renderAll();
  showToast('✅ Wire transfer created — ' + docs.length + ' invoices · ' + f(totalAmt));

  // Enable download button
  document.getElementById('wt-'+dir+'-dl').disabled = false;
  document.getElementById('wt-'+dir+'-dl').onclick = function(){ downloadWireHTML(dir, wire); };

  wtTab('list');
}

// ── Render wire history ───────────────────────────────────────────
function renderWTHistory() {
  var el = document.getElementById('wt-history-list');
  if (!DB.wires || !DB.wires.length) {
    el.innerHTML = '<div style="color:var(--text3);text-align:center;padding:40px;font-size:13px;">No wire transfers yet. Create an outbound or inbound transfer.</div>';
    return;
  }
  el.innerHTML = DB.wires.slice().sort(function(a,b){return b.id-a.id;}).map(function(w){
    var badge = w.type==='out'
      ? '<span class="wt-badge-out">→ OUTBOUND</span>'
      : '<span class="wt-badge-in">← INBOUND</span>';
    var statusBadge = w.status==='reconciled'
      ? '<span style="color:var(--green);font-size:11px;font-weight:700;">✅ Reconciled</span>'
      : '<span class="wt-badge-pend">PENDING</span>';
    return '<div class="wt-history-row" onclick="wtShowDetail('+w.id+')">' +
      '<div style="display:flex;align-items:center;gap:12px;flex:1;">' +
        badge +
        '<div>' +
          '<div style="font-weight:700;color:var(--text);font-size:14px;">'+w.concept+'</div>' +
          '<div style="font-size:11px;color:var(--text3);margin-top:2px;">'+w.date+' · '+w.bank+' · '+(w.docs?w.docs.length:0)+' documents</div>' +
        '</div>' +
      '</div>' +
      '<div style="display:flex;align-items:center;gap:16px;">' +
        statusBadge +
        '<div style="font-family:\'DM Serif Display\',serif;font-size:18px;color:'+(w.type==='out'?'var(--red)':'var(--green)')+';">'+f(w.total)+'</div>' +
        '<button class="btn btn-ghost btn-sm" onclick="event.stopPropagation();downloadWireHTML(null,'+w.id+')">⬇ SEPA</button>' +
        '<button class="btn btn-danger btn-sm" onclick="event.stopPropagation();deleteWire('+w.id+')">Del</button>' +
      '</div>' +
    '</div>';
  }).join('');
}

function deleteWire(id) {
  if (!confirm('Delete this wire transfer record?')) return;
  DB.wires = DB.wires.filter(function(w){ return w.id !== id; });
  sv(); renderWTHistory();
  showToast('Wire transfer deleted.');
}

function wtShowDetail(id) {
  var w = (DB.wires||[]).find(function(x){return x.id===id;});
  if (!w) return;
  var lines = (w.docs||[]).map(function(d){
    return '<tr><td style="font-family:monospace;font-size:11px;color:'+(w.type==='out'?'var(--red)':'var(--accent)')+';">'+d.num+'</td>' +
    '<td style="font-weight:600;color:var(--text);">'+d.party+'</td>' +
    '<td style="color:var(--text3);font-size:12px;">'+(d.desc||'—')+'</td>' +
    '<td>'+d.date+'</td><td>'+d.due+'</td>' +
    '<td class="amt" style="color:'+(w.type==='out'?'var(--red)':'var(--green)')+';">'+f(d.amount)+'</td></tr>';
  }).join('');
  alert('Wire: '+w.concept+'\nDate: '+w.date+'\nBank: '+w.bank+'\nDocs: '+(w.docs?w.docs.length:0)+'\nTotal: '+f(w.total));
}

// ── Download SEPA-compatible HTML file ────────────────────────────
function downloadWireHTML(dir, wireOrId) {
  var wire = wireOrId;
  if (typeof wireOrId === 'number') {
    wire = (DB.wires||[]).find(function(w){ return w.id === wireOrId; });
  }
  if (!wire) {
    // Try last created
    wire = _wtLastCreated;
  }
  if (!wire) { alert('No wire transfer data to export.'); return; }

  var isOut = wire.type === 'out';
  var co    = DB.co.name || 'My Company';
  var cur   = DB.co.cur  || '€';
  var docs  = wire.docs  || [];

  var rows = docs.map(function(d, i){
    return '<tr style="border-bottom:1px solid #dde0e4;">' +
      '<td style="padding:10px 14px;font-family:monospace;font-size:12px;color:'+(isOut?'#dc2626':'#2563eb')+';">'+(i+1)+'</td>' +
      '<td style="padding:10px 14px;font-family:monospace;font-size:12px;">'+(d.num||'')+'</td>' +
      '<td style="padding:10px 14px;font-weight:600;font-size:13px;">'+(d.party||'')+'</td>' +
      '<td style="padding:10px 14px;color:#5c6070;font-size:12px;">'+(d.desc||'—')+'</td>' +
      '<td style="padding:10px 14px;font-size:12px;">'+(d.date||'')+'</td>' +
      '<td style="padding:10px 14px;font-size:12px;">'+(d.due||'')+'</td>' +
      '<td style="padding:10px 14px;text-align:right;font-weight:700;font-family:monospace;font-size:13px;color:'+(isOut?'#dc2626':'#16a34a')+';">'+cur+Number(d.amount).toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2})+'</td>' +
    '</tr>';
  }).join('');

  var html = '<!DOCTYPE html><html lang="es"><head><meta charset="UTF-8">' +
    '<title>Wire Transfer — '+wire.concept+'</title>' +
    '<style>body{font-family:Arial,sans-serif;margin:0;padding:40px;background:#f4f5f7;color:#1a1d23;}' +
    '.container{background:#fff;border-radius:12px;padding:40px;max-width:900px;margin:0 auto;box-shadow:0 2px 20px rgba(0,0,0,.08);}' +
    '.header{display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:32px;padding-bottom:24px;border-bottom:2px solid #dde0e4;}' +
    '.company{font-size:22px;font-weight:800;color:#1a1d23;margin-bottom:4px;}' +
    '.subtitle{font-size:12px;color:#9198a6;text-transform:uppercase;letter-spacing:1px;}' +
    '.badge{display:inline-block;padding:4px 12px;border-radius:20px;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;}' +
    '.badge-out{background:#fee2e2;color:#dc2626;}' +
    '.badge-in{background:#dcfce7;color:#16a34a;}' +
    '.meta-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;background:#f8f9fa;border-radius:8px;padding:20px;margin-bottom:28px;}' +
    '.meta-item label{display:block;font-size:10px;color:#9198a6;text-transform:uppercase;letter-spacing:1px;margin-bottom:4px;}' +
    '.meta-item span{font-size:14px;font-weight:600;color:#1a1d23;}' +
    'table{width:100%;border-collapse:collapse;}' +
    'th{padding:10px 14px;text-align:left;font-size:10px;color:#9198a6;font-family:monospace;text-transform:uppercase;letter-spacing:1px;background:#f8f9fa;border-bottom:2px solid #dde0e4;}' +
    'th:last-child{text-align:right;}' +
    '.total-row{display:flex;justify-content:space-between;align-items:center;padding:20px 14px;background:'+(isOut?'#fee2e2':'#dcfce7')+';border-radius:8px;margin-top:20px;}' +
    '.total-label{font-size:14px;color:#5c6070;}' +
    '.total-val{font-size:28px;font-weight:800;color:'+(isOut?'#dc2626':'#16a34a')+';}' +
    '.footer{margin-top:32px;padding-top:20px;border-top:1px solid #dde0e4;font-size:11px;color:#9198a6;display:flex;justify-content:space-between;}' +
    '@media print{body{background:#fff;padding:0;}.container{box-shadow:none;border-radius:0;}}' +
    '</style></head><body><div class="container">' +
    '<div class="header">' +
      '<div><div class="company">'+co+'</div><div class="subtitle">Wire Transfer Document</div></div>' +
      '<div style="text-align:right;">' +
        '<span class="badge '+(isOut?'badge-out':'badge-in')+'">'+(isOut?'→ OUTBOUND TRANSFER':'← INBOUND TRANSFER')+'</span>' +
        '<div style="font-size:11px;color:#9198a6;margin-top:8px;">Ref: WT-'+String(wire.id).padStart(4,'0')+'</div>' +
      '</div>' +
    '</div>' +
    '<div class="meta-grid">' +
      '<div class="meta-item"><label>Concept</label><span>'+wire.concept+'</span></div>' +
      '<div class="meta-item"><label>Transfer Date</label><span>'+wire.date+'</span></div>' +
      '<div class="meta-item"><label>Due Date</label><span>'+(wire.due||wire.date)+'</span></div>' +
      '<div class="meta-item"><label>Bank</label><span>'+(wire.bank||'—')+'</span></div>' +
      (wire.creditor?'<div class="meta-item" style="grid-column:1/-1;"><label>Creditor ID (SEPA)</label><span style="font-family:monospace;">'+wire.creditor+'</span></div>':'')+
    '</div>' +
    '<table><thead><tr><th>#</th><th>Document</th><th>'+(isOut?'Supplier':'Customer')+'</th><th>Description</th><th>Invoice Date</th><th>Due Date</th><th style="text-align:right;">Amount</th></tr></thead>' +
    '<tbody>'+rows+'</tbody></table>' +
    '<div class="total-row">' +
      '<div class="total-label">'+(isOut?'Total Outbound Payment':'Total Inbound Collection')+' · '+docs.length+' documents</div>' +
      '<div class="total-val">'+cur+Number(wire.total).toLocaleString('en-GB',{minimumFractionDigits:2,maximumFractionDigits:2})+'</div>' +
    '</div>' +
    '<div class="footer">' +
      '<div>Generated by FinLedger · '+new Date().toLocaleDateString('es-ES')+'</div>' +
      '<div>WT-'+String(wire.id).padStart(4,'0')+' · '+co+'</div>' +
    '</div>' +
    '</div></body></html>';

  // Download via server or fallback
  var filename = 'WT-'+String(wire.id).padStart(4,'0')+'_'+wire.concept.replace(/\s+/g,'_')+'_'+wire.date+'.html';
  var blob = new Blob([html], {type:'text/html'});
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url; a.download = filename;
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
  showToast('⬇ SEPA file downloaded: '+filename);
}



// ══════════════════════════════════════════════════════════════════
// BANK ACCOUNTS MODULE
// ══════════════════════════════════════════════════════════════════

var _currentAccountId = null;
var _baImportData     = null;
var _baEditId         = null;
var _bankRecMovIdx    = null;
var _bankRecType      = 'sales';

// Bank icon map
var BANK_ICONS = {
  'santander':'🏦','sabadell':'🟠','bbva':'💙','caixabank':'⭐','cajamar':'🌾',
  'ruralvia':'🌿','ing':'🧡','unicaja':'🦁','ibercaja':'🔵','bankinter':'🔴',
  'abanca':'🔷','kutxabank':'⬜','liberbank':'🟦','openbank':'⚡','revolut':'🔲',
  'wise':'💚','stripe':'🟣','paypal':'🔵','n26':'⬛','holded':'🟤'
};

function getBankIcon(name) {
  if (!name) return '🏦';
  var lower = name.toLowerCase();
  for (var key in BANK_ICONS) {
    if (lower.indexOf(key) !== -1) return BANK_ICONS[key];
  }
  return '🏦';
}

function updateBankIcon() {
  var name = document.getElementById('acc-bank-name').value;
  var icon = document.getElementById('acc-bank-icon-preview');
  if (icon) icon.textContent = getBankIcon(name);
}

// ── Init DB.bankAccounts ──────────────────────────────────────────
function ensureBADB() {
  if (!DB.bankAccounts)  DB.bankAccounts  = [];
  if (!DB.bankMovements) DB.bankMovements = [];
  if (!DB.ids.ba)        DB.ids.ba        = 1;
  if (!DB.ids.bm)        DB.ids.bm        = 1;
}

// ── Open Add Account ─────────────────────────────────────────────
function openAddAccount() {
  _baEditId = null;
  document.getElementById('add-acc-title').textContent = 'Add Bank Account';
  ['acc-bank-name','acc-name','acc-iban','acc-bic','acc-opening-balance'].forEach(function(id){
    var el = document.getElementById(id);
    if (el) el.value = id === 'acc-opening-balance' ? '0' : '';
  });
  document.getElementById('acc-currency').value = 'EUR';
  document.getElementById('acc-bank-icon-preview').textContent = '🏦';
  openOverlay('ov-add-account');
}

function openEditAccount() {
  ensureBADB();
  var acc = DB.bankAccounts.find(function(a){ return a.id === _currentAccountId; });
  if (!acc) return;
  _baEditId = acc.id;
  document.getElementById('add-acc-title').textContent = 'Edit Account';
  document.getElementById('acc-bank-name').value = acc.bankName || '';
  document.getElementById('acc-name').value      = acc.name || '';
  document.getElementById('acc-iban').value      = acc.iban || '';
  document.getElementById('acc-bic').value       = acc.bic  || '';
  document.getElementById('acc-currency').value  = acc.currency || 'EUR';
  document.getElementById('acc-opening-balance').value = acc.openingBalance || 0;
  document.getElementById('acc-bank-icon-preview').textContent = getBankIcon(acc.bankName);
  openOverlay('ov-add-account');
}

function saveAccount() {
  ensureBADB();
  var bankName = document.getElementById('acc-bank-name').value.trim();
  var name     = document.getElementById('acc-name').value.trim() || bankName;
  if (!bankName) { alert('Please enter a bank name.'); return; }

  if (_baEditId) {
    var acc = DB.bankAccounts.find(function(a){ return a.id === _baEditId; });
    if (acc) {
      acc.bankName = bankName; acc.name = name;
      acc.iban = document.getElementById('acc-iban').value.trim();
      acc.bic  = document.getElementById('acc-bic').value.trim();
      acc.currency = document.getElementById('acc-currency').value;
      acc.openingBalance = parseFloat(document.getElementById('acc-opening-balance').value)||0;
    }
  } else {
    DB.bankAccounts.push({
      id: DB.ids.ba++,
      bankName: bankName,
      name: name,
      iban: document.getElementById('acc-iban').value.trim(),
      bic:  document.getElementById('acc-bic').value.trim(),
      currency: document.getElementById('acc-currency').value,
      openingBalance: parseFloat(document.getElementById('acc-opening-balance').value)||0,
      createdAt: td()
    });
  }
  sv(); closeOverlay('ov-add-account'); rBankAccounts();
  showToast('✅ Account saved: ' + name);
}

// ── Render Bank Accounts list page ───────────────────────────────
function rBankAccounts() {
  ensureBADB();
  var grid = document.getElementById('ba-accounts-grid');
  if (!grid) return;

  // Compute totals per account
  var cards = DB.bankAccounts.map(function(acc) {
    var movs = DB.bankMovements.filter(function(m){ return m.accountId === acc.id; });
    var inflows  = movs.filter(function(m){ return m.amount > 0; }).reduce(function(a,m){ return a+m.amount; }, 0);
    var outflows = movs.filter(function(m){ return m.amount < 0; }).reduce(function(a,m){ return a+m.amount; }, 0);
    var balance  = (acc.openingBalance||0) + inflows + outflows;
    var pending  = movs.filter(function(m){ return !m.reconciled; }).length;
    return { acc, inflows, outflows, balance, pending, count: movs.length };
  });

  // KPI chart data
  renderBAChart(cards);

  // KPIs
  var totalIn  = cards.reduce(function(a,c){ return a+c.inflows;  }, 0);
  var totalOut = cards.reduce(function(a,c){ return a+Math.abs(c.outflows); }, 0);
  var totalBal = cards.reduce(function(a,c){ return a+c.balance;  }, 0);
  var kIn  = document.getElementById('ba-kpi-in');
  var kOut = document.getElementById('ba-kpi-out');
  var kBal = document.getElementById('ba-kpi-bal');
  if(kIn)  kIn.textContent  = f(totalIn);
  if(kOut) kOut.textContent = f(totalOut);
  if(kBal) { kBal.textContent = f(totalBal); kBal.style.color = totalBal >= 0 ? 'var(--green)' : 'var(--red)'; }

  // Cards
  grid.innerHTML = cards.map(function(c) {
    var icon = getBankIcon(c.acc.bankName);
    var balColor = c.balance >= 0 ? '' : ' neg';
    return '<div class="ba-card" onclick="openBADetail('+c.acc.id+')">' +
      '<div class="ba-card-actions">' +
        '<div class="ba-action-btn" onclick="event.stopPropagation();_currentAccountId='+c.acc.id+';openEditAccount()" title="Edit">✏️</div>' +
        '<div class="ba-action-btn" onclick="event.stopPropagation();_currentAccountId='+c.acc.id+';openImportMovements()" title="Import">⬆</div>' +
        '<div class="ba-action-btn" onclick="event.stopPropagation();deleteAccount('+c.acc.id+')" title="Delete" style="color:var(--red);">🗑</div>' +
      '</div>' +
      '<div class="ba-card-header">' +
        '<div class="ba-bank-icon">'+icon+'</div>' +
        '<div><div class="ba-bank-name">'+c.acc.name+'</div><div class="ba-bank-iban">'+(c.acc.iban||'No IBAN')+'</div></div>' +
      '</div>' +
      '<div class="ba-balance'+balColor+'">'+f(c.balance)+'</div>' +
      '<div class="ba-stats">' +
        '<div class="ba-stat"><label>Inflows</label><span style="color:var(--green);">'+f(c.inflows)+'</span></div>' +
        '<div class="ba-stat"><label>Outflows</label><span style="color:var(--red);">'+f(Math.abs(c.outflows))+'</span></div>' +
        '<div class="ba-stat"><label>Movements</label><span>'+c.count+'</span></div>' +
        (c.pending > 0 ? '<div class="ba-stat"><label>Pending</label><span style="color:var(--yellow);">'+c.pending+'</span></div>' : '') +
      '</div>' +
    '</div>';
  }).join('') +
  '<div class="ba-add-card" onclick="openAddAccount()"><div class="ba-add-icon">+</div><div class="ba-add-label">Add Account</div></div>';
}

// ── Treasury cash flow chart (SVG) ───────────────────────────────
function renderBAChart(cards) {
  var el = document.getElementById('ba-chart-svg');
  if (!el) return;

  // Group movements by month (last 12 months)
  var months = [];
  var now = new Date();
  for (var i = 11; i >= 0; i--) {
    var d = new Date(now.getFullYear(), now.getMonth() - i, 1);
    months.push({ key: d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0'), label: ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][d.getMonth()] });
  }

  var allMovs = DB.bankMovements || [];
  var monthData = months.map(function(m) {
    var movs = allMovs.filter(function(mv){ return (mv.date||'').startsWith(m.key); });
    var inflow  = movs.filter(function(mv){ return mv.amount > 0; }).reduce(function(a,mv){ return a+mv.amount; }, 0);
    var outflow = movs.filter(function(mv){ return mv.amount < 0; }).reduce(function(a,mv){ return a+Math.abs(mv.amount); }, 0);
    return { label: m.label, inflow, outflow };
  });

  // Running balance
  var totalOpeningBal = (DB.bankAccounts||[]).reduce(function(a,acc){ return a+(acc.openingBalance||0); }, 0);
  var runBal = totalOpeningBal;
  var balData = monthData.map(function(d) {
    runBal += d.inflow - d.outflow;
    return runBal;
  });

  var maxV = Math.max.apply(null, monthData.map(function(d){ return Math.max(d.inflow, d.outflow, 1); }));
  var maxBal = Math.max.apply(null, balData.map(function(v){ return Math.abs(v); })) || 1;
  var W=700, H=140, pad=40, barW=16, gap=12;
  var scaleBar = function(v){ return H - (v/maxV)*H*0.85; };
  var scaleBal = function(v){ return H/2 - (v/maxBal)*(H/2)*0.85; };

  var svg = '<svg viewBox="0 0 '+W+' '+(H+30)+'" style="width:100%;overflow:visible;" xmlns="http://www.w3.org/2000/svg">';
  // Baseline
  svg += '<line x1="'+pad+'" y1="'+H+'" x2="'+(W-10)+'" y2="'+H+'" stroke="var(--border)" stroke-width="1"/>';
  // Gridlines
  [0.25,0.5,0.75].forEach(function(t){
    var y = H*(1-t*0.85);
    svg += '<line x1="'+pad+'" y1="'+y+'" x2="'+(W-10)+'" y2="'+y+'" stroke="var(--border)" stroke-dasharray="3,3" stroke-width="0.5"/>';
  });

  // Bars
  monthData.forEach(function(d, i) {
    var x = pad + i*(barW*2+gap+4);
    var inH  = Math.max(2, (d.inflow/maxV)*H*0.85);
    var outH = Math.max(2, (d.outflow/maxV)*H*0.85);
    svg += '<rect x="'+x+'" y="'+(H-inH)+'" width="'+barW+'" height="'+inH+'" fill="var(--green)" opacity="0.75" rx="3" title="Inflow: '+d.inflow+'"/>';
    svg += '<rect x="'+(x+barW+2)+'" y="'+(H-outH)+'" width="'+barW+'" height="'+outH+'" fill="var(--red)" opacity="0.75" rx="3" title="Outflow: '+d.outflow+'"/>';
    svg += '<text x="'+(x+barW)+'" y="'+(H+14)+'" fill="var(--text3)" font-size="9" text-anchor="middle">'+d.label+'</text>';
  });

  // Balance line
  var balPoints = balData.map(function(v, i) {
    var x = pad + i*(barW*2+gap+4) + barW;
    var y = H/2 + (v >= 0 ? -(v/maxBal)*(H/2)*0.85 : (Math.abs(v)/maxBal)*(H/2)*0.85);
    return x+','+y;
  });
  if (balPoints.length > 1) {
    svg += '<polyline points="'+balPoints.join(' ')+'" fill="none" stroke="var(--accent)" stroke-width="2" stroke-linejoin="round"/>';
    balData.forEach(function(v, i) {
      var x = pad + i*(barW*2+gap+4) + barW;
      var y = H/2 + (v >= 0 ? -(v/maxBal)*(H/2)*0.85 : (Math.abs(v)/maxBal)*(H/2)*0.85);
      svg += '<circle cx="'+x+'" cy="'+y+'" r="3" fill="var(--accent)"/>';
    });
  }
  svg += '</svg>';
  el.innerHTML = svg;
}

// ── Open account detail page ──────────────────────────────────────
function openBADetail(accId) {
  ensureBADB();
  _currentAccountId = accId;
  var acc = DB.bankAccounts.find(function(a){ return a.id === accId; });
  if (!acc) return;
  document.getElementById('bad-title').textContent = acc.name;
  document.getElementById('bad-sub').textContent   = (acc.iban||'') + (acc.bic ? ' · '+acc.bic : '');
  nav('badetail');
  rBADetail();
}

function rBADetail() {
  ensureBADB();
  if (!_currentAccountId) return;
  var acc  = DB.bankAccounts.find(function(a){ return a.id === _currentAccountId; });
  if (!acc) return;
  var filter = (document.getElementById('bad-reconcile-filter')||{value:'all'}).value;
  var movs = DB.bankMovements.filter(function(m){ return m.accountId === _currentAccountId; });
  if (filter === 'pending')    movs = movs.filter(function(m){ return !m.reconciled; });
  if (filter === 'reconciled') movs = movs.filter(function(m){ return m.reconciled; });
  movs = movs.slice().sort(function(a,b){ return b.date > a.date ? 1 : -1; });

  var allMovs  = DB.bankMovements.filter(function(m){ return m.accountId === _currentAccountId; });
  var inflows  = allMovs.filter(function(m){ return m.amount > 0; }).reduce(function(a,m){ return a+m.amount; }, 0);
  var outflows = allMovs.filter(function(m){ return m.amount < 0; }).reduce(function(a,m){ return a+m.amount; }, 0);
  var balance  = (acc.openingBalance||0) + inflows + outflows;
  var pending  = allMovs.filter(function(m){ return !m.reconciled; }).length;

  var bd = document.getElementById('bad-balance'); if(bd){ bd.textContent=f(balance); bd.style.color=balance>=0?'var(--accent)':'var(--red)'; }
  var bi = document.getElementById('bad-in');      if(bi) bi.textContent=f(inflows);
  var bo = document.getElementById('bad-out');     if(bo) bo.textContent=f(Math.abs(outflows));
  var bc = document.getElementById('bad-count');   if(bc) bc.textContent=allMovs.length;
  var bp = document.getElementById('bad-pending-count'); if(bp){ bp.textContent=pending; bp.style.color=pending>0?'var(--yellow)':'var(--green)'; }

  var list = document.getElementById('bad-movements-list');
  if (!list) return;
  if (!movs.length) {
    list.innerHTML = '<div style="text-align:center;color:var(--text3);padding:40px;font-size:13px;">No movements yet. Import your bank statement.</div>';
    return;
  }

  list.innerHTML = movs.map(function(m, i) {
    var isIn  = m.amount >= 0;
    var badge = m.reconciled
      ? '<span class="ba-reconcile-badge done">✓ Reconciled</span>'
      : '<span class="ba-reconcile-badge pending">⏳ Pending</span>';
    return '<div class="ba-mov-row" onclick="openBankReconcile('+m.id+')">' +
      '<div class="ba-mov-sign '+(isIn?'in':'out')+'">'+(isIn?'↑':'↓')+'</div>' +
      '<div class="ba-mov-desc">' +
        '<div class="ba-mov-concept">'+m.concept+'</div>' +
        '<div class="ba-mov-date">'+m.date+(m.valueDate&&m.valueDate!==m.date?' · Val: '+m.valueDate:'')+'</div>' +
      '</div>' +
      badge +
      '<div class="ba-mov-amount '+(isIn?'pos':'neg')+'">'+f(m.amount)+'</div>' +
    '</div>';
  }).join('');
}

// ── Delete account ────────────────────────────────────────────────
function deleteAccount(accId) {
  if (!confirm('Delete this account and all its movements?')) return;
  DB.bankAccounts  = DB.bankAccounts.filter(function(a){ return a.id !== accId; });
  DB.bankMovements = DB.bankMovements.filter(function(m){ return m.accountId !== accId; });
  sv(); rBankAccounts(); showToast('Account deleted.');
}

// ── Import movements ─────────────────────────────────────────────
function openImportMovements() {
  _baImportData = null;
  document.getElementById('ba-import-preview').innerHTML = '';
  document.getElementById('ba-import-result').innerHTML  = '';
  document.getElementById('ba-import-confirm').disabled  = true;
  document.getElementById('ba-file-input').value = '';
  openOverlay('ov-import-movements');
}

function handleBADrop(e) {
  e.preventDefault();
  document.getElementById('ba-drop-zone').classList.remove('drag-over');
  var file = e.dataTransfer.files[0];
  if (file) processBAFile(file);
}

function handleBAFileInput(e) {
  var file = e.target.files[0];
  if (file) processBAFile(file);
}

function processBAFile(file) {
  var reader = new FileReader();
  reader.onload = function(e) {
    try {
      var data = new Uint8Array(e.target.result);
      // Parse XLSX using SheetJS (loaded from CDN if needed)
      parseBAXLSX(data, file.name);
    } catch(err) {
      document.getElementById('ba-import-result').innerHTML =
        '<div style="color:var(--red);padding:10px;background:rgba(248,113,113,.1);border-radius:8px;">Error reading file: '+err.message+'</div>';
    }
  };
  reader.readAsArrayBuffer(file);
}

function parseBAXLSX(data, filename) {
  // Load SheetJS dynamically if not present
  if (typeof XLSX === 'undefined') {
    var s = document.createElement('script');
    s.src = 'https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js';
    s.onload = function(){ doParseBAXLSX(data, filename); };
    document.head.appendChild(s);
  } else {
    doParseBAXLSX(data, filename);
  }
}

function doParseBAXLSX(data, filename) {
  try {
    var wb = XLSX.read(data, { type: 'array' });
    var ws = wb.Sheets[wb.SheetNames[0]];
    var rows = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '' });

    // Find header row (contains "Fecha" and "Importe")
    var headerIdx = -1;
    var headers   = [];
    for (var i = 0; i < Math.min(rows.length, 15); i++) {
      var row = rows[i].map(function(v){ return String(v||'').toLowerCase(); });
      if (row.some(function(v){ return v.indexOf('fecha') !== -1; }) &&
          row.some(function(v){ return v.indexOf('importe') !== -1 || v.indexOf('amount') !== -1; })) {
        headerIdx = i;
        headers   = rows[i].map(function(v){ return String(v||'').toLowerCase(); });
        break;
      }
    }

    if (headerIdx === -1) {
      document.getElementById('ba-import-result').innerHTML =
        '<div style="color:var(--red);padding:10px;background:rgba(248,113,113,.1);border-radius:8px;">Could not find header row. File must have columns: Fecha Operación, Concepto, Importe, Saldo.</div>';
      return;
    }

    // Column map
    function colIdx(keywords) {
      for (var k = 0; k < keywords.length; k++) {
        for (var h = 0; h < headers.length; h++) {
          if (headers[h].indexOf(keywords[k]) !== -1) return h;
        }
      }
      return -1;
    }

    var iDate    = colIdx(['fecha operac','fecha op','operation date','date']);
    var iValDate = colIdx(['fecha valor','value date']);
    var iConcept = colIdx(['concepto','concept','description','descripción']);
    var iAmount  = colIdx(['importe','amount','cantidad']);
    var iBalance = colIdx(['saldo','balance']);
    var iRef1    = colIdx(['referencia 1','ref1','reference']);

    // Parse data rows
    var parsed = [];
    for (var r = headerIdx + 1; r < rows.length; r++) {
      var row = rows[r];
      if (!row || !row[iDate]) continue;

      var rawDate = String(row[iDate] || '');
      var dateStr = '';
      // Handle DD/MM/YYYY format
      var dm = rawDate.match(/(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})/);
      if (dm) dateStr = dm[3]+'-'+String(dm[2]).padStart(2,'0')+'-'+String(dm[1]).padStart(2,'0');
      else dateStr = rawDate.slice(0,10);

      var rawAmount = String(row[iAmount] || '0').replace(/\./g,'').replace(',','.');
      var amount = parseFloat(rawAmount) || 0;
      if (!amount && amount !== 0) continue;

      var rawBalance = iBalance >= 0 ? String(row[iBalance]||'0').replace(/\./g,'').replace(',','.') : '';
      var balance    = parseFloat(rawBalance) || 0;

      var concept  = String(iConcept >= 0 ? row[iConcept]||'' : '').trim();
      var valDate  = '';
      if (iValDate >= 0) {
        var vd = String(row[iValDate]||'');
        var vm = vd.match(/(\d{1,2})[\/\-\.](\d{1,2})[\/\-\.](\d{4})/);
        if (vm) valDate = vm[3]+'-'+String(vm[2]).padStart(2,'0')+'-'+String(vm[1]).padStart(2,'0');
      }

      if (dateStr && concept) {
        parsed.push({ date: dateStr, valueDate: valDate, concept, amount, balance,
          ref: iRef1>=0?String(row[iRef1]||''):'', raw: row });
      }
    }

    if (!parsed.length) {
      document.getElementById('ba-import-result').innerHTML =
        '<div style="color:var(--yellow);padding:10px;background:rgba(255,217,61,.1);border-radius:8px;">No movements found in file.</div>';
      return;
    }

    _baImportData = parsed;
    document.getElementById('ba-import-confirm').disabled = false;

    // Preview
    var previewRows = parsed.slice(0,8).map(function(m) {
      var isIn = m.amount >= 0;
      return '<tr>' +
        '<td style="padding:5px 8px;font-size:11px;font-family:monospace;">'+m.date+'</td>' +
        '<td style="padding:5px 8px;font-size:11px;max-width:200px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">'+m.concept+'</td>' +
        '<td style="padding:5px 8px;font-size:11px;font-family:monospace;color:'+(isIn?'var(--green)':'var(--red)')+';">'+f(m.amount)+'</td>' +
        '<td style="padding:5px 8px;font-size:11px;font-family:monospace;color:var(--text3);">'+f(m.balance)+'</td>' +
      '</tr>';
    }).join('');

    document.getElementById('ba-import-preview').innerHTML =
      '<div style="font-size:11px;color:var(--text3);margin-bottom:8px;">Preview (first 8 of '+parsed.length+' movements)</div>' +
      '<div style="overflow-x:auto;"><table style="width:100%;border-collapse:collapse;font-size:11px;">' +
      '<thead><tr style="background:var(--surface3);">' +
        '<th style="padding:5px 8px;text-align:left;font-size:10px;font-family:monospace;text-transform:uppercase;">Date</th>' +
        '<th style="padding:5px 8px;text-align:left;font-size:10px;font-family:monospace;text-transform:uppercase;">Concept</th>' +
        '<th style="padding:5px 8px;text-align:right;font-size:10px;font-family:monospace;text-transform:uppercase;">Amount</th>' +
        '<th style="padding:5px 8px;text-align:right;font-size:10px;font-family:monospace;text-transform:uppercase;">Balance</th>' +
      '</tr></thead><tbody>'+previewRows+'</tbody></table></div>';

    document.getElementById('ba-import-result').innerHTML =
      '<div style="color:var(--green);padding:8px 12px;background:rgba(74,222,128,.1);border-radius:8px;font-size:12px;">✅ '+parsed.length+' movements ready to import</div>';

  } catch(err) {
    document.getElementById('ba-import-result').innerHTML =
      '<div style="color:var(--red);padding:10px;background:rgba(248,113,113,.1);border-radius:8px;">Parse error: '+err.message+'</div>';
  }
}

function confirmImportMovements() {
  ensureBADB();
  if (!_baImportData || !_currentAccountId) return;
  var plan = getActivePlan();
  var cashAcc = plan.cashAccts ? plan.cashAccts[0] : (plan.id==='pgc'?'572':'1000');
  var added = 0, skipped = 0;

  _baImportData.forEach(function(m) {
    // Skip duplicates (same date + concept + amount)
    var dup = DB.bankMovements.some(function(existing){
      return existing.accountId === _currentAccountId &&
             existing.date === m.date &&
             Math.abs(existing.amount - m.amount) < 0.01 &&
             existing.concept === m.concept;
    });
    if (dup) { skipped++; return; }

    var mov = {
      id: DB.ids.bm++,
      accountId: _currentAccountId,
      date:      m.date,
      valueDate: m.valueDate || m.date,
      concept:   m.concept,
      amount:    m.amount,
      balance:   m.balance,
      ref:       m.ref || '',
      reconciled: false,
      jeId: null
    };
    DB.bankMovements.push(mov);
    added++;
  });

  sv();
  _baImportData = null;
  document.getElementById('ba-import-confirm').disabled = true;
  closeOverlay('ov-import-movements');
  rBADetail();
  showToast('✅ Imported '+added+' movements'+(skipped>0?' · '+skipped+' duplicates skipped':''));
}

// ── Download sample XLSX ──────────────────────────────────────────
function downloadSampleXLSX() {
  var csv = 'Fecha Operación\tFecha Valor\tConcepto\tImporte\tDivisa\tSaldo\n' +
    '22/04/2026\t22/04/2026\tTransferencia De Cliente SL, Concepto Factura INV-001\t1500.00\tEUR\t5500.00\n' +
    '21/04/2026\t21/04/2026\tPago Proveedor ACME - Factura PINV-001\t-800.00\tEUR\t4000.00\n' +
    '20/04/2026\t20/04/2026\tDomiciliacion Impuesto: IVA Trimestral\t-1200.00\tEUR\t4800.00\n' +
    '18/04/2026\t18/04/2026\tTransferencia De Empresa XYZ, Cobro Servicios\t2200.00\tEUR\t6000.00\n' +
    '15/04/2026\t15/04/2026\tNomina Empleado 1\t-1500.00\tEUR\t3800.00\n';
  var blob = new Blob(['\uFEFF'+csv], {type:'text/tab-separated-values;charset=utf-8'});
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url; a.download = 'MovimientosCuenta_Sample.xls';
  document.body.appendChild(a); a.click();
  document.body.removeChild(a); URL.revokeObjectURL(url);
}

// ── Bank Reconcile ────────────────────────────────────────────────
var _bankRecMovId = null;

function openBankReconcile(movId) {
  ensureBADB();
  var mov = DB.bankMovements.find(function(m){ return m.id === movId; });
  if (!mov) return;
  if (mov.reconciled) {
    if (!confirm('This movement is already reconciled. Un-reconcile it?')) return;
    // Un-reconcile
    if (mov.jeId) {
      DB.je = DB.je.filter(function(je){ return je.id !== mov.jeId; });
      mov.jeId = null;
    }
    mov.reconciled = false;
    sv(); rBADetail(); renderAll();
    showToast('Movement un-reconciled.');
    return;
  }
  _bankRecMovId = movId;
  _bankRecType  = mov.amount >= 0 ? 'sales' : 'purchases';
  var isIn = mov.amount >= 0;
  document.getElementById('rec-bank-mov-info').innerHTML =
    '<div style="display:flex;justify-content:space-between;align-items:center;">' +
      '<div>' +
        '<div style="font-weight:700;color:var(--text);font-size:14px;">'+mov.concept+'</div>' +
        '<div style="font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;">'+mov.date+(mov.valueDate?' · Val: '+mov.valueDate:'')+'</div>' +
      '</div>' +
      '<div style="font-family:\'DM Serif Display\',serif;font-size:22px;color:'+(isIn?'var(--green)':'var(--red)')+';">'+f(mov.amount)+'</div>' +
    '</div>';
  setBankRecType(_bankRecType);
  // Initialize diff panel (starts at €0 allocated — button disabled)
  var movAmt = Math.abs(mov.amount);
  var elTotal = document.getElementById('rec-diff-total');
  if (elTotal) elTotal.textContent = f(movAmt);
  var elAlloc = document.getElementById('rec-diff-allocated');
  if (elAlloc) elAlloc.textContent = f(0);
  var elPendWrap = document.getElementById('rec-diff-pending-wrap');
  if (elPendWrap) elPendWrap.style.display = 'none';
  var elOkWrap = document.getElementById('rec-diff-ok-wrap');
  if (elOkWrap) elOkWrap.style.display = 'none';
  var confirmBtn = document.getElementById('rec-confirm-btn');
  if (confirmBtn) { confirmBtn.disabled = true; confirmBtn.style.opacity = '0.4'; confirmBtn.style.cursor = 'not-allowed'; }
  openOverlay('ov-reconcile-bank');
}

function setBankRecType(type) {
  _bankRecType = type;
  ['sales','purchases','manual'].forEach(function(t) {
    var btn = document.getElementById('rec-type-'+t);
    if (btn) {
      btn.style.background  = t === type ? 'var(--accent)' : '';
      btn.style.color       = t === type ? '#0f0f11' : '';
      btn.style.borderColor = t === type ? 'var(--accent)' : '';
    }
  });
  var listEl = document.getElementById('rec-bank-invoice-list');
  var manEl  = document.getElementById('rec-bank-manual-acc');
  listEl.style.display = type === 'manual' ? 'none' : 'block';
  manEl.style.display  = type === 'manual' ? 'block' : 'none';

  if (type === 'manual') {
    var sel = document.getElementById('rec-bank-acc-sel');
    sel.innerHTML = '<option value="">-- Select account --</option>' + coaOpts();
    var mov2 = DB.bankMovements.find(function(m){ return m.id === _bankRecMovId; });
    if (mov2) document.getElementById('rec-bank-manual-amt').value = Math.abs(mov2.amount).toFixed(2);
    updateRecDiff();
    return;
  }

  var mov = DB.bankMovements.find(function(m){ return m.id === _bankRecMovId; });
  var amt = mov ? Math.abs(mov.amount) : 0;

  // Build invoice rows with onchange to update diff
  function makeInvRow(id, num, party, date, rem, isMatch) {
    return '<label style="display:flex;align-items:center;gap:10px;padding:10px 4px;border-bottom:1px solid var(--border);cursor:pointer;'+(isMatch?'background:rgba(200,255,0,.05);':'')+'">' +
      '<input type="checkbox" name="rec-inv" value="'+id+'" '+(isMatch?'checked':'')+' onchange="updateRecDiff()" style="cursor:pointer;width:16px;height:16px;">' +
      '<div style="flex:1;">' +
        '<div style="font-size:13px;font-weight:600;color:var(--text);">'+num+' — '+party+'</div>' +
        '<div style="font-size:11px;color:var(--text3);">'+date+' · Pending: <strong style="color:var(--yellow);">'+f(rem)+'</strong></div>' +
      '</div>' +
      (isMatch ? '<span style="font-size:10px;background:rgba(200,255,0,.15);color:var(--accent);padding:2px 6px;border-radius:6px;font-weight:700;">MATCH</span>' : '') +
    '</label>';
  }

  if (type === 'sales') {
    var pending = DB.sales.filter(function(s){
      var c = DB.coll.filter(function(x){ return x.ref===s.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
      return c < s.total - 0.01;
    });
    listEl.innerHTML = pending.length
      ? pending.slice().sort(function(a,b){ return b.id-a.id; }).map(function(s){
          var c   = DB.coll.filter(function(x){ return x.ref===s.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
          var rem = s.total - c;
          return makeInvRow(s.id, s.num, s.customer, s.date, rem, Math.abs(rem - amt) < 0.01);
        }).join('')
      : '<div style="color:var(--text3);padding:20px;text-align:center;font-size:12px;">No pending sales invoices.</div>';
  } else {
    var pendingP = DB.purch.filter(function(p){
      var pd = DB.pay.filter(function(x){ return x.ref===p.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
      return pd < p.total - 0.01;
    });
    listEl.innerHTML = pendingP.length
      ? pendingP.slice().sort(function(a,b){ return b.id-a.id; }).map(function(p){
          var pd  = DB.pay.filter(function(x){ return x.ref===p.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
          var rem = p.total - pd;
          return makeInvRow(p.id, p.num, p.supplier, p.date, rem, Math.abs(rem - amt) < 0.01);
        }).join('')
      : '<div style="color:var(--text3);padding:20px;text-align:center;font-size:12px;">No pending purchase invoices.</div>';
  }
  updateRecDiff();
}

// Live-update difference panel whenever checkboxes or manual amount changes
function updateRecDiff() {
  var mov = DB.bankMovements.find(function(m){ return m.id === _bankRecMovId; });
  if (!mov) return;
  var movAmt   = Math.abs(mov.amount);
  var allocated = 0;

  if (_bankRecType === 'manual') {
    var manAmt = parseFloat(document.getElementById('rec-bank-manual-amt').value) || 0;
    allocated  = manAmt;
  } else {
    document.querySelectorAll('input[name="rec-inv"]:checked').forEach(function(cb) {
      var id = parseInt(cb.value);
      if (_bankRecType === 'sales') {
        var s = DB.sales.find(function(x){ return x.id===id; });
        if (s) {
          var c = DB.coll.filter(function(x){ return x.ref===s.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
          allocated += Math.min(movAmt, s.total - c);
        }
      } else {
        var p = DB.purch.find(function(x){ return x.id===id; });
        if (p) {
          var pd = DB.pay.filter(function(x){ return x.ref===p.num; }).reduce(function(a,x){ return a+x.amount; }, 0);
          allocated += Math.min(movAmt, p.total - pd);
        }
      }
    });
  }

  var diff = movAmt - allocated;
  var isBalanced = Math.abs(diff) < 0.01;

  // Update display
  var elAlloc   = document.getElementById('rec-diff-allocated');
  var elTotal   = document.getElementById('rec-diff-total');
  var elPending = document.getElementById('rec-diff-pending');
  var elPendWrap= document.getElementById('rec-diff-pending-wrap');
  var elOkWrap  = document.getElementById('rec-diff-ok-wrap');
  var confirmBtn= document.getElementById('rec-confirm-btn');

  if (elAlloc)   elAlloc.textContent  = f(allocated);
  if (elTotal)   elTotal.textContent  = f(movAmt);
  if (elPending) elPending.textContent = f(diff);
  if (elPendWrap) elPendWrap.style.display = (!isBalanced && allocated > 0) ? 'block' : 'none';
  if (elOkWrap)   elOkWrap.style.display   = isBalanced ? 'block' : 'none';

  // Enable/disable reconcile button
  if (confirmBtn) {
    var canReconcile = isBalanced && allocated > 0;
    confirmBtn.disabled = !canReconcile;
    confirmBtn.style.opacity = canReconcile ? '1' : '0.4';
    confirmBtn.style.cursor  = canReconcile ? 'pointer' : 'not-allowed';
  }
}

function confirmBankReconcile() {
  ensureBADB();
  var mov = DB.bankMovements.find(function(m){ return m.id === _bankRecMovId; });
  if (!mov) return;
  var plan    = getActivePlan();
  var cashAcc = plan.cashAccts ? plan.cashAccts[0] : (plan.id==='pgc'?'572':'1000');
  var isIn    = mov.amount >= 0;
  var amt     = Math.abs(mov.amount);

  if (_bankRecType === 'manual') {
    var counterAcc = document.getElementById('rec-bank-acc-sel').value;
    var manAmt     = parseFloat(document.getElementById('rec-bank-manual-amt').value) || amt;
    var desc       = document.getElementById('rec-bank-acc-desc').value || mov.concept;
    if (!counterAcc) { alert('Select a counterpart account.'); return; }
    var lines = isIn
      ? [{account:cashAcc, debit:manAmt, credit:0},{account:counterAcc, debit:0, credit:manAmt}]
      : [{account:counterAcc, debit:manAmt, credit:0},{account:cashAcc, debit:0, credit:manAmt}];
    var je = {id:DB.ids.j++, date:mov.date, desc:desc, lines:lines, amount:manAmt, auto:true, sourceType:'bank_reconcile'};
    DB.je.push(je);
    mov.reconciled = true; mov.jeId = je.id;

  } else {
    var checked = Array.from(document.querySelectorAll('input[name="rec-inv"]:checked'));
    if (!checked.length) { alert('Select at least one invoice.'); return; }

    var lastJeId = null;
    checked.forEach(function(cb) {
      var id = parseInt(cb.value);
      if (_bankRecType === 'sales') {
        var s = DB.sales.find(function(x){ return x.id===id; });
        if (!s) return;
        var coll = DB.coll.filter(function(c){ return c.ref===s.num; }).reduce(function(a,c){ return a+c.amount; }, 0);
        var rem  = Math.min(amt, s.total - coll);
        if (rem <= 0.001) return;
        DB.coll.push({id:DB.ids.c++, date:mov.date, customer:s.customer, ref:s.num, method:'bank_transfer', amount:rem, notes:'Bank reconcile: '+mov.concept});
        var arAcc = plan.arAccts ? plan.arAccts[0] : (plan.id==='pgc'?'430':'1100');
        var je2 = {id:DB.ids.j++, date:mov.date, desc:'Bank Collection — '+s.customer+' / '+s.num, lines:[{account:cashAcc,debit:rem,credit:0},{account:arAcc,debit:0,credit:rem}], amount:rem, auto:true, sourceType:'collection'};
        DB.je.push(je2); lastJeId = je2.id;
        var totColl = DB.coll.filter(function(c){ return c.ref===s.num; }).reduce(function(a,c){ return a+c.amount; }, 0);
        if (totColl >= s.total - 0.01) s.status = 'paid';
      } else {
        var p = DB.purch.find(function(x){ return x.id===id; });
        if (!p) return;
        var paid2 = DB.pay.filter(function(py){ return py.ref===p.num; }).reduce(function(a,py){ return a+py.amount; }, 0);
        var rem2  = Math.min(amt, p.total - paid2);
        if (rem2 <= 0.001) return;
        DB.pay.push({id:DB.ids.py++, date:mov.date, supplier:p.supplier, ref:p.num, method:'bank_transfer', amount:rem2, notes:'Bank reconcile: '+mov.concept});
        var apAcc = plan.apAccts ? plan.apAccts[0] : (plan.id==='pgc'?'400':'2000');
        var je3 = {id:DB.ids.j++, date:mov.date, desc:'Bank Payment — '+p.supplier+' / '+p.num, lines:[{account:apAcc,debit:rem2,credit:0},{account:cashAcc,debit:0,credit:rem2}], amount:rem2, auto:true, sourceType:'payment'};
        DB.je.push(je3); lastJeId = je3.id;
        var totPaid = DB.pay.filter(function(py){ return py.ref===p.num; }).reduce(function(a,py){ return a+py.amount; }, 0);
        if (totPaid >= p.total - 0.01) p.status = 'paid';
      }
    });
    mov.reconciled = true; mov.jeId = lastJeId;
  }

  sv(); closeOverlay('ov-reconcile-bank'); rBADetail(); renderAll();
  showToast('✅ Movement reconciled — Journal Entry created.');
}


function toggleUserDropdown(e) {
  e.stopPropagation();
  var dd = document.getElementById('user-dropdown');
  dd.style.display = dd.style.display === 'none' ? 'block' : 'none';
}
function closeUserDropdown() {
  var dd = document.getElementById('user-dropdown');
  if(dd) dd.style.display = 'none';
}
// Close dropdown when clicking anywhere else
document.addEventListener('click', function(e) {
  var dd = document.getElementById('user-dropdown');
  if(dd && !dd.contains(e.target)) dd.style.display = 'none';
});

// Fallback signOut for desktop version (no Supabase)
if(typeof signOut === 'undefined') {
  function signOut() {
    if(confirm('Sign out of FinLedger?')) {
      window.location.reload();
    }
  }
}

function renderAll(){rDash();rContacts();rSales();rRecurring();rPurch();rColl();rPay();rJE();rPL();rBS();rCF();rCFO();rBankAccounts();}

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
    rows.push(['Invoice #','Date','Type','Supplier','Description','Category','VAT %','Net','VAT Amount','Total','Status','Method','Asset Name']);
    DB.purch.forEach(function(p){rows.push([p.num,p.date,p.invType||'expense',p.supplier,p.desc||'',p.cat,p.vatRate,p.net,p.vatAmt,p.total,p.status,p.method,p.assetName||'']);});
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

function exportFullBackup() {
  var json = JSON.stringify(DB, null, 2);
  var fname = 'FinLedger_Backup_' + td().replace(/-/g,'') + '.json';
  // Download via hidden link
  var blob = new Blob([json], {type:'application/json'});
  var url  = URL.createObjectURL(blob);
  var a    = document.createElement('a');
  a.href = url; a.download = fname;
  document.body.appendChild(a); a.click();
  setTimeout(function(){ document.body.removeChild(a); URL.revokeObjectURL(url); }, 500);
  showToast('✅ Backup downloaded: ' + fname);
}

function downloadImportTemplate() {
  var rows = [
    ['TYPE: sales — Required columns below (do not change headers)'],
    ['Invoice #','Date (YYYY-MM-DD)','Customer','Description','VAT Rate (%)','Net Amount','Status (pending/paid/partial)','Payment Method'],
    ['INV26-00001','2026-01-15','Acme Corp','Consulting services Q1','21','1000','paid','bank'],
    ['INV26-00002','2026-02-01','Beta SL','Monthly retainer','21','2000','pending','bank'],
    [''],
    ['TYPE: purchases — Required columns below'],
    ['Invoice #','Date (YYYY-MM-DD)','Supplier','Description','Category','VAT Rate (%)','Net Amount','Status','Payment Method'],
    ['PINV26-0001','2026-01-10','Office Pro','Office supplies','Other OpEx','21','500','paid','cash'],
    [''],
    ['TYPE: contacts — Required columns below'],
    ['Name','Type (client/supplier/both)','NIF','Email','Phone','City','Country','IBAN','Payment Terms','VAT Sales (%)','VAT Purchase (%)'],
    ['Acme Corp','client','A12345678','acme@example.com','+34 91 123 4567','Madrid','Spain','','30days','21','21'],
  ];
  var csv = rows.map(function(r){
    return r.map(function(v){
      var s = String(v); 
      if(s.indexOf(',')>=0||s.indexOf('"')>=0) s='"'+s.replace(/"/g,'""')+'"';
      return s;
    }).join(',');
  }).join('\r\n');
  var fname = 'FinLedger_Import_Template.csv';
  fetch('/export', {method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({filename:fname,content:csv})})
    .then(function(r){return r.blob();})
    .then(function(blob){
      var url=URL.createObjectURL(blob);
      var a=document.createElement('a'); a.href=url; a.download=fname;
      document.body.appendChild(a); a.click();
      setTimeout(function(){document.body.removeChild(a);URL.revokeObjectURL(url);},500);
    }).catch(function(){
      // fallback for desktop
      var blob=new Blob(['﻿'+csv],{type:'text/csv'});
      var url=URL.createObjectURL(blob);
      var a=document.createElement('a'); a.href=url; a.download=fname;
      document.body.appendChild(a); a.click();
      setTimeout(function(){document.body.removeChild(a);URL.revokeObjectURL(url);},500);
    });
  showToast('✅ Template downloaded');
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
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
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
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Invoice</div>
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
        <div style="font-size:11px;color:var(--text3);font-family:monospace;margin-top:2px;">
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
            <select id="ct-debtacc" onchange="onCtAccChange('debt',this.value)"></select>
            <div id="ct-debtacc-preview" style="font-size:11px;color:var(--accent);font-family:monospace;margin-top:4px;min-height:16px;"></div>
          </div>
          <div class="fg full">
            <label>Supplier / Creditor Account</label>
            <select id="ct-credacc" onchange="onCtAccChange('cred',this.value)"></select>
            <div id="ct-credacc-preview" style="font-size:11px;color:var(--accent);font-family:monospace;margin-top:4px;min-height:16px;"></div>
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
          💡 Al seleccionar "✦ Nueva subcuenta (430XXXXX)" el sistema asigna automáticamente el siguiente número de subcuenta correlativo. El código se guarda en el contacto y se usa en los asientos contables.
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

<!-- ═══════════════════ INVOICE PREVIEW MODAL ═══════════════════ -->
<div class="overlay" id="ov-invoice">
  <div class="inv-modal">
    <div class="inv-toolbar">
      <div class="inv-toolbar-left">
        <button class="btn btn-ghost btn-sm" onclick="closeOverlay('ov-invoice')">← Back</button>
        <span style="font-size:13px;color:var(--text2);font-family:monospace;" id="inv-toolbar-num">INV-001</span>
        <span id="inv-toolbar-status"></span>
      </div>
      <div class="inv-toolbar-right">
        <button class="btn btn-ghost btn-sm" onclick="editInvoice()">✏️ Edit</button>
        <button class="btn btn-ghost btn-sm" onclick="printInvoice()">🖨 Print</button>
        <div style="position:relative;display:inline-block;">
          <button class="btn btn-ghost btn-sm" onclick="toggleConvertMenu()" id="convert-btn">⇄ Convert ▾</button>
          <div id="convert-menu" style="display:none;position:absolute;right:0;top:110%;background:var(--surface);border:1px solid var(--border);border-radius:8px;min-width:200px;z-index:300;box-shadow:0 4px 20px rgba(0,0,0,.3);padding:4px;">
            <div onclick="convertToRecurring()" style="padding:10px 14px;cursor:pointer;font-size:13px;color:var(--text2);border-radius:6px;" onmouseover="this.style.background='var(--surface2)'" onmouseout="this.style.background='transparent'">🔁 Recurring Invoice</div>
          </div>
        </div>
        <button class="btn btn-primary btn-sm" onclick="downloadInvoicePDF()">⬇ PDF</button>
      </div>
    </div>
    <div id="inv-paper-wrap">
      <div class="inv-paper" id="inv-paper">
        <div class="inv-accent-bar"></div>
        <!-- Header -->
        <div class="inv-header">
          <div class="inv-logo-area">
            <div class="inv-company-name" id="inv-co-name">My Company Ltd.</div>
            <div class="inv-company-details" id="inv-co-details"></div>
          </div>
          <div class="inv-title-area">
            <div class="inv-title">Invoice</div>
            <div class="inv-num" id="inv-num">INV-001</div>
          </div>
        </div>
        <!-- Bill to + Dates -->
        <div class="inv-meta-row">
          <div class="inv-bill-to">
            <div class="inv-bill-label">Bill To</div>
            <div class="inv-bill-name" id="inv-customer">—</div>
            <div class="inv-bill-detail" id="inv-customer-detail"></div>
          </div>
          <div class="inv-dates">
            <div class="inv-date-row">
              <span class="inv-date-label">Issue Date</span>
              <span class="inv-date-val" id="inv-date">—</span>
            </div>
            <div class="inv-date-row">
              <span class="inv-date-label">Due Date</span>
              <span class="inv-date-val" id="inv-due">—</span>
            </div>
            <div class="inv-date-row" id="inv-ref-row" style="display:none;">
              <span class="inv-date-label">Reference</span>
              <span class="inv-date-val" id="inv-ref">—</span>
            </div>
          </div>
        </div>
        <!-- Line items table -->
        <table class="inv-table">
          <thead>
            <tr>
              <th style="width:50%">Description</th>
              <th style="width:15%;text-align:right;">Qty</th>
              <th style="width:15%;text-align:right;">Unit Price</th>
              <th style="width:10%;text-align:right;">VAT</th>
              <th style="width:10%;text-align:right;">Total</th>
            </tr>
          </thead>
          <tbody id="inv-lines"></tbody>
          <tfoot id="inv-tfoot"></tfoot>
        </table>
        <!-- Footer -->
        <div class="inv-footer">
          <div class="inv-footer-notes" id="inv-notes"></div>
          <div id="inv-status-badge"></div>
        </div>
      </div>
    </div>
  </div>
</div>

<!-- EDIT INVOICE MODAL -->
<div class="overlay" id="ov-invoice-edit">
  <div class="modal" style="width:min(640px,95vw)">
    <div class="mhdr"><div class="mtitle">Edit Invoice</div><div class="mclose" onclick="closeOverlay('ov-invoice-edit')">✕</div></div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="ie-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="ie-num"></div>
        <div class="fg full"><label>Customer</label><input type="text" id="ie-customer"></div>
        <div class="fg full"><label>Description</label><input type="text" id="ie-desc"></div>
        <div class="fg"><label>Net Amount (€)</label><input type="number" id="ie-net" step="0.01" oninput="calcIE()"></div>
        <div class="fg"><label>VAT Rate (%)</label>
          <select id="ie-vat" onchange="calcIE()">
            <option value="0">0%</option><option value="4">4%</option>
            <option value="10">10%</option><option value="21">21%</option>
          </select>
        </div>
        <div class="fg"><label>VAT Amount</label><input type="text" id="ie-vatamt" readonly style="background:var(--surface3);"></div>
        <div class="fg"><label>Total</label><input type="text" id="ie-total" readonly style="background:var(--surface3);color:var(--accent);font-family:monospace;font-weight:600;"></div>
        <div class="fg"><label>Status</label>
          <select id="ie-status"><option value="pending">Pending</option><option value="paid">Paid</option><option value="partial">Partial</option></select>
        </div>
        <div class="fg"><label>Payment Method</label>
          <select id="ie-method"><option value="bank">Bank Transfer</option><option value="cash">Cash</option><option value="card">Card</option><option value="other">Other</option></select>
        </div>
        <div class="fg full"><label>Notes (appears on invoice)</label><textarea id="ie-notes" rows="2"></textarea></div>
      </div>
    </div>
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-invoice-edit')">Cancel</button>
      <button class="btn btn-primary" onclick="saveEditedInvoice()">Save Changes</button>
    </div>
  </div>
</div>

<!-- ═══════════════════ RECURRING INVOICE MODAL ═══════════════════ -->
<div class="overlay" id="ov-recurring">
  <div class="modal" style="width:min(620px,95vw);">
    <div class="mhdr">
      <div>
        <div class="mtitle">🔁 Set Up Recurring Invoice</div>
        <div style="font-size:12px;color:var(--text3);margin-top:2px;" id="rc-source-label"></div>
      </div>
      <div class="mclose" onclick="closeOverlay('ov-recurring')">✕</div>
    </div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg full" style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;">
          <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:8px;">Source Invoice</div>
          <div id="rc-source-preview" style="font-size:13px;color:var(--text);font-weight:500;"></div>
        </div>
        <div class="fg">
          <label>Recurrence Interval</label>
          <select id="rc-interval">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="biweekly">Biweekly</option>
            <option value="monthly" selected>Monthly</option>
            <option value="bimonthly">Bimonthly (every 2 months)</option>
            <option value="quarterly">Quarterly (every 3 months)</option>
            <option value="biannual">Biannual (every 6 months)</option>
            <option value="annually">Annually</option>
          </select>
        </div>
        <div class="fg">
          <label>Due Days</label>
          <select id="rc-duedays">
            <option value="0">Same day</option>
            <option value="7">7 days</option>
            <option value="15">15 days</option>
            <option value="30" selected>30 days</option>
            <option value="45">45 days</option>
            <option value="60">60 days</option>
          </select>
        </div>
        <div class="fg">
          <label>Start Date</label>
          <input type="date" id="rc-start">
        </div>
        <div class="fg">
          <label>End Date <span style="color:var(--text3);font-size:11px;">(leave blank = indefinite)</span></label>
          <input type="date" id="rc-end">
        </div>
        <div class="fg full">
          <label>Payment Method</label>
          <select id="rc-method">
            <option value="bank">Bank Transfer</option>
            <option value="sepa">SEPA Direct Debit</option>
            <option value="card">Card</option>
            <option value="cash">Cash</option>
          </select>
        </div>
        <div class="fg full">
          <label>Internal Notes</label>
          <input type="text" id="rc-notes" placeholder="e.g. Contract 19214 — monthly equipment rental">
        </div>
      </div>
      <div style="margin-top:12px;padding:12px 14px;background:rgba(200,255,0,.05);border:1px solid rgba(200,255,0,.15);border-radius:8px;font-size:12px;color:var(--text3);">
        💡 The system will automatically generate a new invoice on each scheduled date. You can pause or stop it at any time.
      </div>
    </div>
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-recurring')">Cancel</button>
      <button class="btn btn-primary" onclick="saveRecurring()">🔁 Activate Recurring</button>
    </div>
  </div>
</div>

<!-- ═══════════════════ SERIES MODAL ═══════════════════ -->
<div class="overlay" id="ov-series">
  <div class="modal" style="width:min(500px,95vw);">
    <div class="mhdr">
      <div class="mtitle" id="series-modal-title">New Numbering Series</div>
      <div class="mclose" onclick="closeOverlay('ov-series')">✕</div>
    </div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg full"><label>Series Name</label><input type="text" id="ser-name" placeholder="e.g. Sales Invoices"></div>
        <div class="fg"><label>Code / Prefix</label><input type="text" id="ser-code" placeholder="INV" maxlength="10" oninput="previewSeriesNum()"></div>
        <div class="fg"><label>Type</label>
          <select id="ser-type">
            <option value="sale">Sales Invoice</option>
            <option value="credit">Credit Note</option>
            <option value="purchase">Purchase Invoice</option>
            <option value="other">Other</option>
          </select>
        </div>
        <div class="fg full">
          <label>Format</label>
          <input type="text" id="ser-format" placeholder="INV[YY]-%%%%%" oninput="previewSeriesNum()">
          <div style="font-size:11px;color:var(--text3);margin-top:4px;">Use % for sequential digits. Example: <code>INV[YY]-%%%%%</code> → INV26-00001</div>
        </div>
        <div class="fg"><label>Last Number (0 = start fresh)</label><input type="number" id="ser-lastnum" value="0" min="0"></div>
        <div class="fg">
          <label>Preview</label>
          <div id="ser-preview" style="padding:10px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;font-family:monospace;font-size:14px;color:var(--accent);font-weight:700;">INV26-00001</div>
        </div>
      </div>
    </div>
    <div class="mfoot">
      <button class="btn btn-danger btn-sm" id="ser-delete-btn" onclick="deleteSeries()" style="margin-right:auto;display:none;">🗑 Delete</button>
      <button class="btn btn-ghost" onclick="closeOverlay('ov-series')">Cancel</button>
      <button class="btn btn-primary" onclick="saveSeries()">Save Series</button>
    </div>
  </div>
</div>

<!-- ═══════════════════ RECURRING EDIT MODAL ═══════════════════ -->
<div class="overlay" id="ov-rc-edit">
  <div class="modal" style="width:min(620px,96vw);max-height:90vh;overflow-y:auto;">
    <div class="mhdr" style="position:sticky;top:0;background:var(--surface);z-index:10;border-radius:var(--radius) var(--radius) 0 0;">
      <div>
        <div class="mtitle">Set Up / Edit Recurring Invoice</div>
        <div style="font-size:12px;color:var(--text3);margin-top:2px;" id="rce-subtitle"></div>
      </div>
      <div class="mclose" onclick="closeOverlay('ov-rc-edit')">✕</div>
    </div>
    <div class="mbody">

      <!-- Source invoice info -->
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Source Invoice</div>
        <div id="rce-source-preview" style="font-size:13px;font-weight:500;color:var(--text);"></div>
      </div>

      <div class="fgrid">
        <!-- Interval + Due Days -->
        <div class="fg">
          <label>Recurrence Interval</label>
          <select id="rce-interval">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="biweekly">Biweekly</option>
            <option value="monthly">Monthly</option>
            <option value="bimonthly">Bimonthly (every 2 months)</option>
            <option value="quarterly">Quarterly (every 3 months)</option>
            <option value="biannual">Biannual (every 6 months)</option>
            <option value="annually">Annually</option>
          </select>
        </div>
        <div class="fg">
          <label>Due Days</label>
          <select id="rce-duedays">
            <option value="0">Same day</option>
            <option value="7">7 days</option>
            <option value="15">15 days</option>
            <option value="30">30 days</option>
            <option value="45">45 days</option>
            <option value="60">60 days</option>
          </select>
        </div>
        <!-- Start + End -->
        <div class="fg">
          <label>Start Date</label>
          <input type="date" id="rce-start">
        </div>
        <div class="fg">
          <label>End Date <span style="color:var(--text3);font-size:11px;">(blank = indefinite)</span></label>
          <input type="date" id="rce-end">
        </div>
        <!-- Payment method -->
        <div class="fg">
          <label>Payment Method</label>
          <select id="rce-method">
            <option value="bank">Bank Transfer</option>
            <option value="sepa">SEPA Direct Debit</option>
            <option value="card">Card</option>
            <option value="cash">Cash</option>
          </select>
        </div>
        <div class="fg">
          <label>Status</label>
          <select id="rce-status">
            <option value="active">🟢 Active</option>
            <option value="paused">⏸ Paused</option>
            <option value="ended">⏹ Ended</option>
          </select>
        </div>
        <!-- Internal notes -->
        <div class="fg full">
          <label>Internal Notes</label>
          <input type="text" id="rce-notes" placeholder="e.g. Contract 19214 — monthly equipment rental">
        </div>
      </div>

      <!-- Amount section — with price change history -->
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:16px;margin-top:4px;">
        <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:12px;">Amount (applies from next invoice)</div>
        <div style="display:grid;grid-template-columns:1fr 1fr 1fr 1fr;gap:12px;align-items:end;">
          <div>
            <label style="font-size:11px;color:var(--text3);display:block;margin-bottom:4px;">Net Amount (€)</label>
            <input type="number" id="rce-net" step="0.01" oninput="calcRCEModal()" style="width:100%;padding:8px 10px;background:var(--surface);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:14px;font-weight:600;">
          </div>
          <div>
            <label style="font-size:11px;color:var(--text3);display:block;margin-bottom:4px;">VAT Rate (%)</label>
            <select id="rce-vat" onchange="calcRCEModal()" style="width:100%;padding:8px 10px;background:var(--surface);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:13px;">
              <option value="0">0%</option><option value="4">4%</option>
              <option value="10">10%</option><option value="21">21%</option>
            </select>
          </div>
          <div>
            <label style="font-size:11px;color:var(--text3);display:block;margin-bottom:4px;">VAT Amount</label>
            <input type="text" id="rce-vatamt" readonly style="width:100%;padding:8px 10px;background:var(--surface3);border:1px solid var(--border);border-radius:7px;color:var(--text2);font-size:13px;">
          </div>
          <div>
            <label style="font-size:11px;color:var(--text3);display:block;margin-bottom:4px;">Total (incl. VAT)</label>
            <input type="text" id="rce-total-display" readonly style="width:100%;padding:8px 10px;background:var(--surface3);border:1px solid var(--border);border-radius:7px;color:var(--accent);font-size:14px;font-weight:700;">
          </div>
        </div>
        <!-- Price change notice -->
        <div id="rce-price-change-notice" style="display:none;margin-top:10px;padding:8px 12px;background:rgba(200,255,0,.07);border:1px solid rgba(200,255,0,.2);border-radius:6px;font-size:12px;color:var(--text2);">
          💡 <strong>Price change:</strong> Previously <span id="rce-old-price"></span> → New price <span id="rce-new-price"></span>.
          This change will be recorded in the invoice history.
        </div>
      </div>

      <!-- Auto create & send -->
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-top:14px;">
        <div class="rc-toggle-row">
          <div>
            <div class="rc-toggle-label">Create invoices automatically</div>
            <div class="rc-toggle-sub">Generate on each due date</div>
          </div>
          <label class="toggle-sw">
            <input type="checkbox" id="rce-autocreate">
            <div class="toggle-sw-track"><div class="toggle-sw-thumb"></div></div>
          </label>
        </div>
        <div class="rc-toggle-row">
          <div>
            <div class="rc-toggle-label">Send invoices automatically</div>
            <div class="rc-toggle-sub">Email to contact on creation</div>
          </div>
          <label class="toggle-sw">
            <input type="checkbox" id="rce-autosend">
            <div class="toggle-sw-track"><div class="toggle-sw-thumb"></div></div>
          </label>
        </div>
      </div>

      <!-- System note -->
      <div style="margin-top:12px;padding:10px 14px;background:rgba(200,255,0,.04);border:1px solid rgba(200,255,0,.12);border-radius:7px;font-size:12px;color:var(--text3);">
        💡 The system will automatically generate a new invoice on each scheduled date. You can pause or stop it at any time.
      </div>

    </div>
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-rc-edit')">Cancel</button>
      <button class="btn btn-primary" onclick="saveRCEditModal()">🔁 Save Recurring</button>
    </div>
  </div>
</div>

<!-- ═══════════════════ DEPRECIATION PLAN MODAL ═══════════════════ -->
<div class="overlay" id="ov-depr">
  <div class="modal" style="width:min(620px,96vw);max-height:92vh;overflow-y:auto;">
    <div class="mhdr" style="position:sticky;top:0;background:var(--surface);z-index:10;border-radius:var(--radius) var(--radius) 0 0;">
      <div>
        <div class="mtitle">📉 Depreciation Plan</div>
        <div style="font-size:12px;color:var(--text3);margin-top:2px;" id="depr-asset-label"></div>
      </div>
      <div class="mclose" onclick="skipDeprPlan()">✕</div>
    </div>
    <div class="mbody">

      <!-- Asset summary -->
      <div style="background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:14px;margin-bottom:18px;">
        <div style="font-size:10px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;">Asset Registered</div>
        <div id="depr-asset-summary" style="font-size:13px;font-weight:500;color:var(--text);"></div>
      </div>

      <div class="fgrid">
        <!-- Start date -->
        <div class="fg">
          <label>Depreciation Start Date</label>
          <input type="date" id="depr-start">
        </div>
        <!-- Frequency -->
        <div class="fg">
          <label>Depreciation Frequency</label>
          <select id="depr-freq">
            <option value="monthly">Monthly</option>
            <option value="quarterly">Quarterly</option>
            <option value="annually">Annually</option>
          </select>
        </div>
        <!-- Annual depreciation rate -->
        <div class="fg">
          <label>Useful Life (years)</label>
          <input type="number" id="depr-rate" value="10" min="1" max="100" step="1" oninput="calcDeprPreview()">
          <div style="font-size:11px;color:var(--text3);margin-top:3px;">
            Annual amount: <span id="depr-life">depreciable ÷ years</span>
          </div>
        </div>
        <!-- Residual value -->
        <div class="fg">
          <label>Residual Value (€)</label>
          <input type="number" id="depr-residual" value="0" min="0" step="0.01" oninput="calcDeprPreview()">
        </div>
        <!-- Accumulated depreciation account -->
        <div class="fg full">
          <label>Accumulated Depreciation Account</label>
          <select id="depr-accum-acc">
          </select>
        </div>
        <!-- Depreciation expense account -->
        <div class="fg full">
          <label>Depreciation Expense Account</label>
          <select id="depr-exp-acc">
          </select>
        </div>
      </div>

      <!-- Depreciation preview -->
      <div style="margin-top:16px;">
        <div style="font-size:11px;color:var(--text3);font-family:'DM Mono',monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:10px;">📋 Schedule Preview (first 12 periods)</div>
        <div id="depr-schedule-preview" style="max-height:240px;overflow-y:auto;background:var(--surface2);border:1px solid var(--border);border-radius:8px;padding:10px 14px;">
          <div style="color:var(--text3);font-size:12px;text-align:center;padding:16px;">Fill in the fields above to see the schedule.</div>
        </div>
        <div style="display:flex;justify-content:space-between;margin-top:8px;font-size:12px;color:var(--text3);">
          <span>Total depreciable: <strong id="depr-total-depreciable" style="color:var(--text);">€0.00</strong></span>
          <span>Per period: <strong id="depr-per-period" style="color:var(--accent);">€0.00</strong></span>
        </div>
      </div>

      <div style="margin-top:12px;padding:10px 14px;background:rgba(200,255,0,.04);border:1px solid rgba(200,255,0,.12);border-radius:7px;font-size:12px;color:var(--text3);">
        💡 Journal Entries for each depreciation period will be automatically generated: Dr. Depreciation Expense / Cr. Accumulated Depreciation.
      </div>
    </div>
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="skipDeprPlan()">Skip — no depreciation plan</button>
      <button class="btn btn-primary" onclick="saveDeprPlan()">✅ Create Depreciation Plan</button>
    </div>
  </div>
</div>

<!-- ═══════════════════ EDIT PURCHASE MODAL ═══════════════════ -->
<div class="overlay" id="ov-purch-edit">
  <div class="modal" style="width:min(600px,96vw);">
    <div class="mhdr">
      <div class="mtitle">✏️ Edit Purchase Invoice</div>
      <div class="mclose" onclick="closeOverlay('ov-purch-edit')">✕</div>
    </div>
    <div class="mbody">
      <div class="fgrid">
        <div class="fg"><label>Date</label><input type="date" id="pe-date"></div>
        <div class="fg"><label>Invoice #</label><input type="text" id="pe-num"></div>
        <div class="fg full"><label>Supplier</label><input type="text" id="pe-sup"></div>
        <div class="fg full"><label>Description</label><input type="text" id="pe-desc"></div>
        <div class="fg full">
          <label>Type of Invoice</label>
          <select id="pe-invtype" onchange="onEditPurchTypeChange(this.value)">
            <option value="expense">📋 Expense</option>
            <option value="asset">🏗 Asset</option>
          </select>
        </div>
        <div class="fg full" id="pe-asset-name-row" style="display:none;">
          <label>Asset Name</label>
          <input type="text" id="pe-asset-name">
        </div>
        <div class="fg full"><label>Category / Account</label><select id="pe-cat">
          <option value="COGS">Cost of Goods Sold</option>
          <option value="Rent">Rent</option>
          <option value="Salaries">Salaries</option>
          <option value="Utilities">Utilities</option>
          <option value="Marketing">Marketing</option>
          <option value="Professional">Professional Services</option>
          <option value="Depreciation">Depreciation</option>
          <option value="Other OpEx">Other OpEx</option>
        </select></div>
        <div class="fg"><label>VAT Rate (%)</label>
          <select id="pe-vat" onchange="calcPE()">
            <option value="0">0%</option><option value="4">4%</option>
            <option value="10">10%</option><option value="21">21%</option>
          </select>
        </div>
        <div class="fg"><label>Net Amount (€)</label>
          <input type="number" id="pe-net" step="0.01" oninput="calcPE()">
        </div>
        <div class="fg"><label>VAT Amount</label>
          <input type="text" id="pe-vatamt" readonly style="background:var(--surface3);">
        </div>
        <div class="fg"><label>Total</label>
          <input type="text" id="pe-total" readonly style="background:var(--surface3);color:var(--red);font-weight:700;font-family:monospace;">
        </div>
        <div class="fg"><label>Status</label>
          <select id="pe-stat">
            <option value="pending">Pending</option>
            <option value="paid">Paid</option>
          </select>
        </div>
        <div class="fg"><label>Payment Method</label>
          <select id="pe-meth">
            <option value="bank">Bank Transfer</option>
            <option value="cash">Cash</option>
            <option value="card">Card</option>
            <option value="other">Other</option>
          </select>
        </div>
      </div>
    </div>
    <div class="mfoot">
      <button class="btn btn-ghost" onclick="closeOverlay('ov-purch-edit')">Cancel</button>
      <button class="btn btn-primary" onclick="saveEditPurch()">Save Changes</button>
    </div>
  </div>
</div>

    <!-- ══ BANK ACCOUNTS ══ -->
    <div class="page" id="page-bankaccounts">
      <div class="sec-hdr">
        <div>
          <div class="sec-title">Bank Accounts</div>
          <div class="sec-sub">Treasury overview · Import bank movements · Reconcile</div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <select id="ba-period" onchange="rBankAccounts()" class="period-select" style="min-width:160px;">
            <option value="12">Last 12 months</option>
            <option value="6">Last 6 months</option>
            <option value="3">Last 3 months</option>
            <option value="1">This month</option>
          </select>
          <button class="btn btn-primary" onclick="openAddAccount()">+ Add Account</button>
        </div>
      </div>

      <!-- Treasury chart -->
      <div class="ba-chart-wrap">
        <div class="ba-chart-header">
          <div class="ba-chart-kpis">
            <div class="ba-kpi-item"><label>Inflows</label><span id="ba-kpi-in" style="color:var(--green);">€0.00</span></div>
            <div class="ba-kpi-item"><label>Outflows</label><span id="ba-kpi-out" style="color:var(--red);">€0.00</span></div>
            <div class="ba-kpi-item"><label>Net Balance</label><span id="ba-kpi-bal">€0.00</span></div>
          </div>
          <div style="display:flex;gap:16px;font-size:12px;color:var(--text3);">
            <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:var(--green);margin-right:4px;"></span>Inflows</span>
            <span><span style="display:inline-block;width:10px;height:10px;border-radius:2px;background:var(--red);margin-right:4px;"></span>Outflows</span>
            <span><span style="display:inline-block;width:2px;height:10px;border-radius:1px;background:var(--accent);margin-right:4px;display:inline-block;vertical-align:middle;"></span>Balance</span>
          </div>
        </div>
        <div id="ba-chart-svg" style="width:100%;overflow:hidden;"></div>
      </div>

      <!-- Account cards -->
      <div id="ba-accounts-grid" class="ba-grid"></div>
    </div>

    <!-- ══ BANK ACCOUNT DETAIL ══ -->
    <div class="page" id="page-badetail">
      <div class="sec-hdr">
        <div style="display:flex;align-items:center;gap:12px;">
          <button class="btn btn-ghost btn-sm" onclick="navTesoreria('bankaccounts')" style="padding:6px 10px;">← Back</button>
          <div>
            <div class="sec-title" id="bad-title">Account Name</div>
            <div class="sec-sub" id="bad-sub">IBAN · BIC</div>
          </div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <button class="btn btn-ghost btn-sm" onclick="openEditAccount()">✏️ Edit</button>
          <button class="btn btn-ghost btn-sm" onclick="openImportMovements()">⬆ Import Movements</button>
          <select id="bad-reconcile-filter" onchange="rBADetail()" class="period-select" style="min-width:160px;">
            <option value="all">All movements</option>
            <option value="pending">Pending only</option>
            <option value="reconciled">Reconciled only</option>
          </select>
        </div>
      </div>

      <!-- Balance summary -->
      <div class="totbar" style="margin-bottom:20px;">
        <div class="tot-item"><label>Current Balance</label><span id="bad-balance" style="color:var(--accent);font-family:'DM Serif Display',serif;font-size:20px;">€0.00</span></div>
        <div class="tot-item"><label>Total Inflows</label><span id="bad-in" style="color:var(--green);">€0.00</span></div>
        <div class="tot-item"><label>Total Outflows</label><span id="bad-out" style="color:var(--red);">€0.00</span></div>
        <div class="tot-item"><label>Movements</label><span id="bad-count" style="color:var(--text2);">0</span></div>
        <div class="tot-item"><label>Pending</label><span id="bad-pending-count" style="color:var(--yellow);">0</span></div>
      </div>

      <!-- Movements list -->
      <div class="card" style="padding:0;overflow:hidden;">
        <div id="bad-movements-list" style="max-height:600px;overflow-y:auto;"></div>
      </div>
    </div>

    <!-- ══ RECONCILE OVERLAY ══ -->
    <div class="overlay" id="ov-reconcile-bank">
      <div class="modal wide">
        <div class="mhdr">
          <div class="mtitle">Reconcile Movement</div>
          <div class="mclose" onclick="closeOverlay('ov-reconcile-bank')">✕</div>
        </div>
        <div class="mbody">
          <!-- Movement info -->
          <div style="background:var(--surface2);border:1px solid var(--border);border-radius:10px;padding:14px 18px;margin-bottom:20px;">
            <div id="rec-bank-mov-info" style="font-size:13px;color:var(--text2);"></div>
          </div>
          <!-- Counterpart type -->
          <div class="fg" style="margin-bottom:16px;">
            <label>Match with</label>
            <div style="display:flex;gap:8px;margin-top:6px;">
              <button id="rec-type-sales" class="btn btn-ghost btn-sm" onclick="setBankRecType('sales')" style="flex:1;">📊 Sales Invoices</button>
              <button id="rec-type-purchases" class="btn btn-ghost btn-sm" onclick="setBankRecType('purchases')" style="flex:1;">📋 Purchase Invoices</button>
              <button id="rec-type-manual" class="btn btn-ghost btn-sm" onclick="setBankRecType('manual')" style="flex:1;">✏️ Manual Account</button>
            </div>
          </div>
          <!-- Invoice list or manual account -->
          <div id="rec-bank-invoice-list" style="max-height:260px;overflow-y:auto;"></div>
          <div id="rec-bank-manual-acc" style="display:none;">
            <div class="fgrid">
              <div class="fg">
                <label>Counterpart Account</label>
                <select id="rec-bank-acc-sel" onchange="updateRecDiff()"></select>
              </div>
              <div class="fg">
                <label>Amount (€)</label>
                <input type="number" id="rec-bank-manual-amt" step="0.01" placeholder="0.00" oninput="updateRecDiff()">
              </div>
            </div>
            <div class="fg" style="margin-top:10px;">
              <label>Description</label>
              <input type="text" id="rec-bank-acc-desc" placeholder="e.g. Tax payment, Salary, etc.">
            </div>
          </div>
        </div>
        <!-- Difference bar + Reconcile button -->
        <div style="padding:14px 26px;border-top:1px solid var(--border);display:flex;align-items:center;justify-content:space-between;gap:16px;">
          <!-- Left: difference indicator -->
          <div id="rec-diff-panel" style="flex:1;">
            <div style="display:flex;align-items:center;gap:20px;">
              <div>
                <div style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;">Allocated</div>
                <div id="rec-diff-allocated" style="font-family:'DM Serif Display',serif;font-size:18px;color:var(--accent);">€0.00</div>
              </div>
              <div style="font-size:18px;color:var(--text3);">/</div>
              <div>
                <div style="font-size:10px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;">Movement</div>
                <div id="rec-diff-total" style="font-family:'DM Serif Display',serif;font-size:18px;color:var(--text);">€0.00</div>
              </div>
              <div id="rec-diff-pending-wrap" style="background:rgba(255,217,61,.12);border:1px solid rgba(255,217,61,.3);border-radius:8px;padding:6px 14px;display:none;">
                <div style="font-size:10px;color:var(--yellow);font-family:monospace;text-transform:uppercase;letter-spacing:1px;margin-bottom:2px;">Pending to reconcile</div>
                <div id="rec-diff-pending" style="font-family:'DM Serif Display',serif;font-size:18px;color:var(--yellow);">€0.00</div>
              </div>
              <div id="rec-diff-ok-wrap" style="background:rgba(74,222,128,.1);border:1px solid rgba(74,222,128,.3);border-radius:8px;padding:6px 14px;display:none;">
                <div style="font-size:11px;color:var(--green);font-weight:700;">✓ Fully reconciled</div>
              </div>
            </div>
          </div>
          <!-- Right: buttons -->
          <div style="display:flex;gap:8px;">
            <button class="btn btn-ghost" onclick="closeOverlay('ov-reconcile-bank')">Cancel</button>
            <button class="btn btn-primary" id="rec-confirm-btn" onclick="confirmBankReconcile()" disabled style="opacity:.4;cursor:not-allowed;">✅ Reconcile</button>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ ADD / EDIT ACCOUNT OVERLAY ══ -->
    <div class="overlay" id="ov-add-account">
      <div class="modal">
        <div class="mhdr">
          <div class="mtitle" id="add-acc-title">Add Bank Account</div>
          <div class="mclose" onclick="closeOverlay('ov-add-account')">✕</div>
        </div>
        <div class="mbody">
          <div class="fgrid">
            <div class="fg full">
              <label>Bank Name</label>
              <input type="text" id="acc-bank-name" placeholder="e.g. Banco Santander, BBVA, Caixabank..." oninput="updateBankIcon()">
            </div>
            <div class="fg full" style="text-align:center;padding:10px 0;">
              <div id="acc-bank-icon-preview" style="font-size:36px;margin-bottom:4px;">🏦</div>
              <div style="font-size:11px;color:var(--text3);">Icon auto-detected from bank name</div>
            </div>
            <div class="fg full">
              <label>Account Name / Alias</label>
              <input type="text" id="acc-name" placeholder="e.g. Cuenta Principal, BBVA Empresas...">
            </div>
            <div class="fg full">
              <label>IBAN</label>
              <input type="text" id="acc-iban" placeholder="ES90 0049 1883 3226 1037 7710" style="font-family:monospace;">
            </div>
            <div class="fg">
              <label>BIC / SWIFT</label>
              <input type="text" id="acc-bic" placeholder="BSCHESMM" style="font-family:monospace;">
            </div>
            <div class="fg">
              <label>Currency</label>
              <select id="acc-currency">
                <option value="EUR">Euro (EUR)</option>
                <option value="USD">US Dollar (USD)</option>
                <option value="GBP">British Pound (GBP)</option>
              </select>
            </div>
            <div class="fg full">
              <label>Opening Balance (€)</label>
              <input type="number" id="acc-opening-balance" value="0" step="0.01" placeholder="0.00">
            </div>
          </div>
        </div>
        <div class="mfoot">
          <button class="btn btn-ghost" onclick="closeOverlay('ov-add-account')">Cancel</button>
          <button class="btn btn-primary" onclick="saveAccount()">Save Account</button>
        </div>
      </div>
    </div>

    <!-- ══ IMPORT MOVEMENTS OVERLAY ══ -->
    <div class="overlay" id="ov-import-movements">
      <div class="modal wide">
        <div class="mhdr">
          <div class="mtitle">Import Bank Movements</div>
          <div class="mclose" onclick="closeOverlay('ov-import-movements')">✕</div>
        </div>
        <div class="mbody">
          <p style="font-size:13px;color:var(--text2);margin-bottom:16px;">
            Upload your bank statement in Excel format. The file must have columns:
            <strong style="color:var(--text);">Fecha Operación, Concepto, Importe, Saldo</strong>.
          </p>
          <!-- Download sample -->
          <button class="btn btn-ghost btn-sm" onclick="downloadSampleXLSX()" style="margin-bottom:16px;">
            ⬇ Download sample .xlsx file
          </button>
          <!-- Drop zone -->
          <div class="ba-import-zone" id="ba-drop-zone"
               ondragover="event.preventDefault();this.classList.add('drag-over')"
               ondragleave="this.classList.remove('drag-over')"
               ondrop="handleBADrop(event)"
               onclick="document.getElementById('ba-file-input').click()">
            <div class="ba-import-zone-icon">📂</div>
            <div class="ba-import-zone-title">Click or drag & drop your file here</div>
            <div class="ba-import-zone-sub">Supports .xlsx and .xls files from any Spanish bank</div>
          </div>
          <input type="file" id="ba-file-input" accept=".xlsx,.xls,.csv" style="display:none" onchange="handleBAFileInput(event)">
          <!-- Preview -->
          <div id="ba-import-preview" style="margin-top:16px;"></div>
          <div id="ba-import-result" style="margin-top:10px;"></div>
        </div>
        <div class="mfoot">
          <button class="btn btn-ghost" onclick="closeOverlay('ov-import-movements')">Cancel</button>
          <button class="btn btn-primary" id="ba-import-confirm" onclick="confirmImportMovements()" disabled>Import Movements</button>
        </div>
      </div>
    </div>

    <!-- ══ CFO MODULE ══ -->
    <div class="page" id="page-cfo">
      <div class="sec-hdr">
        <div>
          <div class="sec-title" style="display:flex;align-items:center;gap:10px;">
            <span style="background:linear-gradient(135deg,var(--accent),#0E9AA7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;font-size:26px;font-weight:900;">★ CFO Intelligence</span>
          </div>
          <div class="sec-sub">Advanced financial analytics · Ratios · Cohorts · Revenue trends</div>
        </div>
        <div style="display:flex;align-items:center;gap:8px;">
          <select id="cfo-year" onchange="rCFO()" class="period-select" style="min-width:90px;"></select>
          <button class="btn btn-primary btn-sm" onclick="rCFO()">↻ Refresh</button>
        </div>
      </div>

      <!-- KPI Row -->
      <div class="cfo-grid" id="cfo-kpis"></div>

      <!-- Revenue vs Net Result chart + Cohort table -->
      <div class="cfo-grid-3">
        <!-- Left: Revenue vs Net chart -->
        <div class="cfo-panel">
          <div class="cfo-panel-title">📈 Revenue vs Net Result <span style="font-size:10px;font-weight:400;color:var(--text3);" id="cfo-chart-year"></span></div>
          <div class="cfo-panel-sub">Monthly comparison Jan–Dec</div>
          <div class="cfo-chart-wrap" id="cfo-rev-chart"></div>
        </div>
        <!-- Right: Financial Ratios -->
        <div class="cfo-panel">
          <div class="cfo-panel-title">⚖️ Financial Ratios</div>
          <div class="cfo-panel-sub">Calculated from latest financial statements</div>
          <div class="ratio-grid" id="cfo-ratios"></div>
        </div>
      </div>

      <!-- Cohort analysis -->
      <div class="cfo-grid-2">
        <div class="cfo-panel">
          <div class="cfo-panel-title">👥 Customer Cohort Analysis</div>
          <div class="cfo-panel-sub">Active, new and churned customers per month</div>
          <div id="cfo-cohort-chart" style="margin-bottom:16px;"></div>
          <table class="cohort-tbl" id="cfo-cohort-tbl">
            <thead><tr>
              <th>Month</th><th>Active</th><th>New</th><th>Churned</th><th>Total</th><th>Retention</th>
            </tr></thead>
            <tbody id="cfo-cohort-body"></tbody>
          </table>
        </div>
        <!-- MRR + Cash Runway -->
        <div style="display:flex;flex-direction:column;gap:20px;">
          <div class="cfo-panel" style="flex:1;">
            <div class="cfo-panel-title">💰 MRR Breakdown</div>
            <div class="cfo-panel-sub">Monthly Recurring Revenue from active recurrences</div>
            <div id="cfo-mrr-detail"></div>
          </div>
          <div class="cfo-panel" style="flex:1;">
            <div class="cfo-panel-title">⏱ Cash Runway</div>
            <div class="cfo-panel-sub">Based on current cash and monthly burn rate</div>
            <div id="cfo-runway"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══ WIRE TRANSFERS OVERLAY ══ -->
    <div class="wt-overlay" id="ov-wire-transfers">
      <div class="wt-modal">
        <!-- Header -->
        <div class="wt-header">
          <div class="wt-title">⇄ Wire Transfers
            <span style="font-size:11px;font-weight:400;color:var(--text3);font-family:monospace;">Remesas bancarias</span>
          </div>
          <div style="display:flex;align-items:center;gap:10px;">
            <div class="wt-tabs">
              <div class="wt-tab active" id="wt-tab-list" onclick="wtTab('list')">📋 All Transfers</div>
              <div class="wt-tab" id="wt-tab-out" onclick="wtTab('out')">→ New Outbound</div>
              <div class="wt-tab" id="wt-tab-in" onclick="wtTab('in')">← New Inbound</div>
            </div>
            <div style="width:30px;height:30px;border-radius:7px;background:var(--surface2);border:1px solid var(--border);cursor:pointer;display:flex;align-items:center;justify-content:center;color:var(--text2);font-size:15px;" onclick="closeWireTransfers()">✕</div>
          </div>
        </div>

        <!-- PANEL: LIST -->
        <div id="wt-panel-list" class="wt-body" style="overflow-y:auto;padding:20px 24px;flex-direction:column;">
          <div style="display:flex;align-items:center;justify-content:space-between;margin-bottom:16px;">
            <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;">Wire Transfer History</div>
            <div style="display:flex;gap:8px;">
              <button class="btn btn-ghost btn-sm" onclick="wtTab('out')">→ New Outbound</button>
              <button class="btn btn-ghost btn-sm" onclick="wtTab('in')">← New Inbound</button>
            </div>
          </div>
          <div id="wt-history-list">
            <div style="color:var(--text3);text-align:center;padding:40px;font-size:13px;">No wire transfers yet. Create an outbound or inbound transfer.</div>
          </div>
        </div>

        <!-- PANEL: OUTBOUND (Purchases → Remesa Pagos) -->
        <div id="wt-panel-out" class="wt-body" style="display:none;">
          <div class="wt-list">
            <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;">→ Select Purchase Invoices to include in this outbound wire</div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
              <label style="font-size:12px;color:var(--text2);cursor:pointer;display:flex;align-items:center;gap:6px;">
                <input type="checkbox" id="wt-out-selall" onchange="wtSelectAll('out',this.checked)"> Select All Pending
              </label>
              <input type="text" id="wt-out-search" oninput="renderWTOut()" placeholder="🔍 Search supplier..." style="padding:6px 10px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:12px;width:200px;">
            </div>
            <div class="card" style="padding:0;overflow:hidden;">
              <div class="tbl-wrap">
                <table>
                  <thead><tr>
                    <th style="width:36px;"></th>
                    <th>Invoice #</th><th>Date</th><th>Supplier</th><th>Description</th><th>Due</th>
                    <th class="amt">Total</th><th class="amt">Pending</th>
                  </tr></thead>
                  <tbody id="wt-out-tbl"></tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="wt-sidebar">
            <div class="wt-total-box">
              <div class="wt-total-label">Wire Total</div>
              <div class="wt-total-val" id="wt-out-total">€0.00</div>
              <div style="font-size:11px;color:var(--text3);margin-top:4px;"><span id="wt-out-count">0</span> invoices selected</div>
            </div>
            <div class="wt-field">
              <label>Concept / Reference</label>
              <input type="text" id="wt-out-concept" placeholder="PAYMENTS SUPPLIERS">
            </div>
            <div class="wt-field">
              <label>Transfer Date</label>
              <input type="date" id="wt-out-date">
            </div>
            <div class="wt-field">
              <label>Bank Account</label>
              <input type="text" id="wt-out-bank" placeholder="BBVA **4199">
            </div>
            <div class="wt-field">
              <label>Due Date</label>
              <input type="date" id="wt-out-due">
            </div>
            <div style="border-top:1px solid var(--border);padding-top:12px;display:flex;flex-direction:column;gap:8px;">
              <button class="btn btn-primary" style="width:100%;" onclick="createWireTransfer('out')">⇄ Create Outbound Wire</button>
              <button class="btn btn-ghost" style="width:100%;font-size:12px;" onclick="downloadWireHTML('out')" id="wt-out-dl" disabled>⬇ Download SEPA File</button>
            </div>
            <div style="font-size:10px;color:var(--text3);line-height:1.5;">
              Creates a grouped payment in Payments module. Download the SEPA-compatible HTML file to upload directly to your bank.
            </div>
          </div>
        </div>

        <!-- PANEL: INBOUND (Sales → Remesa Cobros) -->
        <div id="wt-panel-in" class="wt-body" style="display:none;">
          <div class="wt-list">
            <div style="font-size:11px;color:var(--text3);font-family:monospace;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:12px;">← Select Sales Invoices to include in this inbound wire</div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:12px;">
              <label style="font-size:12px;color:var(--text2);cursor:pointer;display:flex;align-items:center;gap:6px;">
                <input type="checkbox" id="wt-in-selall" onchange="wtSelectAll('in',this.checked)"> Select All Pending
              </label>
              <input type="text" id="wt-in-search" oninput="renderWTIn()" placeholder="🔍 Search customer..." style="padding:6px 10px;background:var(--surface2);border:1px solid var(--border);border-radius:7px;color:var(--text);font-size:12px;width:200px;">
            </div>
            <div class="card" style="padding:0;overflow:hidden;">
              <div class="tbl-wrap">
                <table>
                  <thead><tr>
                    <th style="width:36px;"></th>
                    <th>Invoice #</th><th>Date</th><th>Customer</th><th>Description</th><th>Due</th>
                    <th class="amt">Total</th><th class="amt">Pending</th>
                  </tr></thead>
                  <tbody id="wt-in-tbl"></tbody>
                </table>
              </div>
            </div>
          </div>
          <div class="wt-sidebar">
            <div class="wt-total-box">
              <div class="wt-total-label">Wire Total</div>
              <div class="wt-total-val" id="wt-in-total" style="color:var(--green);">€0.00</div>
              <div style="font-size:11px;color:var(--text3);margin-top:4px;"><span id="wt-in-count">0</span> invoices selected</div>
            </div>
            <div class="wt-field">
              <label>Concept / Reference</label>
              <input type="text" id="wt-in-concept" placeholder="Remittances April">
            </div>
            <div class="wt-field">
              <label>Transfer Date</label>
              <input type="date" id="wt-in-date">
            </div>
            <div class="wt-field">
              <label>Bank Account</label>
              <input type="text" id="wt-in-bank" placeholder="CUENTA SANTANDER...">
            </div>
            <div class="wt-field">
              <label>Creditor ID (SEPA)</label>
              <input type="text" id="wt-in-creditor" placeholder="ES39001B72664329">
            </div>
            <div class="wt-field">
              <label>Due Date</label>
              <input type="date" id="wt-in-due">
            </div>
            <div style="border-top:1px solid var(--border);padding-top:12px;display:flex;flex-direction:column;gap:8px;">
              <button class="btn btn-primary" style="width:100%;background:var(--green);color:#0f0f11;" onclick="createWireTransfer('in')">⇄ Create Inbound Wire</button>
              <button class="btn btn-ghost" style="width:100%;font-size:12px;" onclick="downloadWireHTML('in')" id="wt-in-dl" disabled>⬇ Download SEPA File</button>
            </div>
            <div style="font-size:10px;color:var(--text3);line-height:1.5;">
              Creates a grouped collection in Collections module. Download the SEPA-compatible HTML file to upload to your bank.
            </div>
          </div>
        </div>

      </div>
    </div>


<style>
#auth-overlay{position:fixed;inset:0;background:#0f0f11;z-index:9999;display:flex;align-items:center;justify-content:center;}
#auth-overlay.hidden{display:none;}
.auth-box{background:#16161a;border:1px solid #2e2e38;border-radius:16px;padding:40px;width:min(420px,94vw);box-shadow:0 8px 50px rgba(0,0,0,.6);}
.auth-logo{font-family:'DM Serif Display',serif;font-size:32px;color:#c8ff00;margin-bottom:4px;}
.auth-sub{font-size:12px;color:#5a5a72;font-family:monospace;text-transform:uppercase;letter-spacing:2px;margin-bottom:32px;}
.auth-title{font-size:18px;font-weight:700;color:#f0f0f4;margin-bottom:20px;}
.auth-field{display:flex;flex-direction:column;gap:5px;margin-bottom:14px;}
.auth-field label{font-size:11px;color:#5a5a72;font-family:monospace;text-transform:uppercase;letter-spacing:1px;}
.auth-field input{background:#1e1e24;border:1px solid #2e2e38;border-radius:8px;padding:10px 14px;color:#f0f0f4;font-size:14px;font-family:'DM Sans',sans-serif;outline:none;transition:border .15s;}
.auth-field input:focus{border-color:#c8ff00;}
.auth-btn{width:100%;padding:12px;background:#c8ff00;color:#0f0f11;border:none;border-radius:8px;font-size:14px;font-weight:700;cursor:pointer;margin-top:8px;font-family:'DM Sans',sans-serif;transition:background .15s;}
.auth-btn:hover{background:#d4ff26;}
.auth-btn.secondary{background:transparent;color:#9090a8;border:1px solid #2e2e38;margin-top:6px;}
.auth-btn.secondary:hover{color:#f0f0f4;border-color:#5a5a72;}
.auth-err{color:#f87171;font-size:12px;margin-top:8px;min-height:16px;text-align:center;}
.auth-ok{color:#4ade80;font-size:12px;margin-top:8px;min-height:16px;text-align:center;}
.auth-sep{display:flex;align-items:center;gap:10px;margin:16px 0;color:#5a5a72;font-size:12px;}
.auth-sep::before,.auth-sep::after{content:'';flex:1;height:1px;background:#2e2e38;}
body.light-mode #auth-overlay{background:#f4f5f7;}
body.light-mode .auth-box{background:#fff;border-color:#dde0e4;}
body.light-mode .auth-field input{background:#f4f5f7;color:#1a1d23;}
body.light-mode .auth-title{color:#1a1d23;}
</style>

<div id="auth-overlay">
  <div class="auth-box">
    <div class="auth-logo">FinLedger</div>
    <div class="auth-sub">Accounting System</div>
    <div id="auth-login">
      <div class="auth-title">Welcome back</div>
      <div class="auth-field"><label>Email</label><input type="email" id="auth-email" placeholder="you@company.com" onkeydown="if(event.key==='Enter')authLogin()"></div>
      <div class="auth-field"><label>Password</label><input type="password" id="auth-pass" placeholder="••••••••" onkeydown="if(event.key==='Enter')authLogin()"></div>
      <div class="auth-err" id="auth-err-login"></div>
      <button class="auth-btn" onclick="authLogin()">Sign In</button>
      <div class="auth-sep">or</div>
      <button class="auth-btn secondary" onclick="showAuthPanel('register')">Create an account</button>
      <button class="auth-btn secondary" onclick="showAuthPanel('reset')" style="margin-top:4px;font-size:12px;border:none;color:#5a5a72;">Forgot password?</button>
    </div>
    <div id="auth-register" style="display:none;">
      <div class="auth-title">Create account</div>
      <div class="auth-field"><label>Email</label><input type="email" id="reg-email" placeholder="you@company.com"></div>
      <div class="auth-field"><label>Password</label><input type="password" id="reg-pass" placeholder="Min 6 characters"></div>
      <div class="auth-field"><label>Confirm Password</label><input type="password" id="reg-pass2" placeholder="Repeat password" onkeydown="if(event.key==='Enter')authRegister()"></div>
      <div class="auth-err" id="auth-err-register"></div>
      <button class="auth-btn" onclick="authRegister()">Create Account</button>
      <div class="auth-sep">or</div>
      <button class="auth-btn secondary" onclick="showAuthPanel('login')">Already have an account? Sign in</button>
    </div>
    <div id="auth-reset" style="display:none;">
      <div class="auth-title">Reset password</div>
      <div class="auth-field"><label>Email</label><input type="email" id="reset-email" placeholder="you@company.com"></div>
      <div class="auth-err" id="auth-err-reset"></div>
      <div class="auth-ok" id="auth-ok-reset"></div>
      <button class="auth-btn" onclick="authReset()">Send Reset Email</button>
      <div class="auth-sep">or</div>
      <button class="auth-btn secondary" onclick="showAuthPanel('login')">Back to sign in</button>
    </div>
  </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
<script>
const SUPA_URL = 'https://xoaujnyamjsexybjswwj.supabase.co';
const SUPA_KEY = 'sb_publishable_BcWxOGS-mTzTimjQZvFSIw_f0kyY1ka';
const _supa = supabase.createClient(SUPA_URL, SUPA_KEY);
var _currentUser = null;

function showAuthPanel(panel) {
  ['login','register','reset'].forEach(function(p){
    document.getElementById('auth-'+p).style.display = p===panel ? '' : 'none';
  });
  ['auth-err-login','auth-err-register','auth-err-reset','auth-ok-reset'].forEach(function(id){
    var el=document.getElementById(id); if(el) el.textContent='';
  });
}

async function authLogin() {
  var email = document.getElementById('auth-email').value.trim();
  var pass  = document.getElementById('auth-pass').value;
  var errEl = document.getElementById('auth-err-login');
  errEl.textContent = 'Signing in...';
  var { data, error } = await _supa.auth.signInWithPassword({ email, password: pass });
  if (error) { errEl.textContent = error.message; return; }
  _currentUser = data.user;
  onAuthSuccess();
}

async function authRegister() {
  var email = document.getElementById('reg-email').value.trim();
  var pass  = document.getElementById('reg-pass').value;
  var pass2 = document.getElementById('reg-pass2').value;
  var errEl = document.getElementById('auth-err-register');
  if (!email || !pass) { errEl.textContent = 'Email and password are required.'; return; }
  if (pass !== pass2)  { errEl.textContent = 'Passwords do not match.'; return; }
  if (pass.length < 6) { errEl.textContent = 'Password must be at least 6 characters.'; return; }
  errEl.textContent = 'Creating account...';
  var { data, error } = await _supa.auth.signUp({ email, password: pass });
  if (error) { errEl.textContent = error.message; return; }
  _currentUser = data.user;
  var { data: d2, error: e2 } = await _supa.auth.signInWithPassword({ email, password: pass });
  if (!e2 && d2.user) { _currentUser = d2.user; onAuthSuccess(); }
  else { errEl.style.color='#4ade80'; errEl.textContent = 'Account created! Check your email to confirm, then sign in.'; showAuthPanel('login'); }
}

async function authReset() {
  var email = document.getElementById('reset-email').value.trim();
  var errEl = document.getElementById('auth-err-reset');
  var okEl  = document.getElementById('auth-ok-reset');
  if (!email) { errEl.textContent = 'Enter your email address.'; return; }
  var { error } = await _supa.auth.resetPasswordForEmail(email);
  if (error) { errEl.textContent = error.message; return; }
  okEl.textContent = 'Reset email sent! Check your inbox.';
}

function onAuthSuccess() {
  document.getElementById('auth-overlay').classList.add('hidden');
  var emailShort = (_currentUser.email||'').split('@')[0];
  var greetEl = document.getElementById('topGreeting');
  if(greetEl) greetEl.textContent = emailShort;
  loadFromSupabase();
}

async function saveToSupabase(dbObj) {
  if (!_currentUser) return;
  await _supa.from('user_data').upsert({
    user_id: _currentUser.id,
    data: dbObj,
    updated_at: new Date().toISOString()
  }, { onConflict: 'user_id' });
}

async function loadFromSupabase() {
  if (!_currentUser) return;
  var { data, error } = await _supa.from('user_data')
    .select('data').eq('user_id', _currentUser.id).single();
  if (!error && data && data.data && data.data.ids) {
    DB = data.data;
    refreshCOA();
    if(!DB.wires)        DB.wires        = [];
    if(!DB.ids.wt)       DB.ids.wt       = 1;
    if(!DB.contacts)     DB.contacts     = [];
    if(!DB.recurring)    DB.recurring    = [];
    if(!DB.assets)       DB.assets       = [];
    if(!DB.deprPlans)    DB.deprPlans    = [];
    if(!DB.bankAccounts)  DB.bankAccounts  = [];
    if(!DB.bankMovements) DB.bankMovements = [];
    if(!DB.ids.ba)       DB.ids.ba       = 1;
    if(!DB.ids.bm)       DB.ids.bm       = 1;
  }
  updateUserUI();
  renderAll();
  initJE();
}

var _origSv = sv;
sv = function() {
  _origSv();
  saveToSupabase(DB);
};

async function signOut() {
  closeUserDropdown();
  await _supa.auth.signOut();
  _currentUser = null;
  document.getElementById('auth-overlay').classList.remove('hidden');
  showAuthPanel('login');
}

(async function() {
  var { data: { session } } = await _supa.auth.getSession();
  if (session && session.user) {
    _currentUser = session.user;
    onAuthSuccess();
  }
  _supa.auth.onAuthStateChange(function(event, session) {
    if (event === 'SIGNED_IN' && session) { _currentUser = session.user; onAuthSuccess(); }
    if (event === 'SIGNED_OUT') { _currentUser = null; document.getElementById('auth-overlay').classList.remove('hidden'); }
  });
})();
</script>
</body>
</html>"""

import json as _json2

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path=="/health": self._health()
        else: self._serve_app()
    def do_POST(self):
        if self.path=="/export": self._export()
        else: self.send_response(200); self._cors(); self.end_headers(); self.wfile.write(b"ok")
    def do_OPTIONS(self):
        self.send_response(200); self._cors(); self.end_headers()
    def _cors(self):
        self.send_header("Access-Control-Allow-Origin","*")
        self.send_header("Access-Control-Allow-Methods","GET,POST,OPTIONS")
        self.send_header("Access-Control-Allow-Headers","Content-Type")
    def _health(self):
        self.send_response(200); self.send_header("Content-Type","application/json"); self._cors(); self.end_headers()
        self.wfile.write(b'{"status":"ok"}')
    def _serve_app(self):
        self.send_response(200); self.send_header("Content-type","text/html; charset=utf-8")
        self.send_header("Cache-Control","no-cache"); self._cors(); self.end_headers()
        self.wfile.write(HTML.encode("utf-8"))
    def _export(self):
        try:
            length=int(self.headers.get("Content-Length",0)); body=self.rfile.read(length)
            payload=_json2.loads(body); content=payload.get("content",""); fname=payload.get("filename","export.csv")
            self.send_response(200); self.send_header("Content-Type","text/csv; charset=utf-8-sig")
            self.send_header("Content-Disposition",f'attachment; filename="{fname}"'); self._cors(); self.end_headers()
            self.wfile.write(content.encode("utf-8-sig"))
        except Exception as e:
            self.send_response(500); self._cors(); self.end_headers(); self.wfile.write(str(e).encode())
    def log_message(self,f,*a): pass

def main():
    socketserver.TCPServer.allow_reuse_address=True
    with socketserver.TCPServer(("0.0.0.0",PORT),Handler) as h:
        print(f"FinLedger running on port {PORT}"); h.serve_forever()

if __name__=="__main__": main()
