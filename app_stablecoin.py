# -*- coding: utf-8 -*-
# XPay Minimal Demo (Landing -> Auth -> App)
# 简洁首页（Logo + 语言切换 + 登录按钮 + Slogan）
# 登录页含“登录/注册”Tab；功能保留 转账 + 兑换 + 历史 + 设置（去掉出入金）
# 注意：把 logo.png 与可选 bg.jpg 放在同目录

import time
import datetime as dt
import numpy as np
import pandas as pd
import streamlit as st

APP_NAME = "XPay"
SUPPORTED = ["USDT", "USDC", "BUSD", "DAI"]
FEE = 0.005  # 0.5%

# ---------------- i18n ----------------
I18N = {
    "ZH": {
        "slogan": "一键转账，跨币种无缝到达",
        "landing_sub": "演示环境，数据随刷新重置",
        "login_btn": "登录",
        "signin": "登录",
        "signup": "注册",
        "email": "邮箱",
        "password": "密码",
        "confirm_pwd": "确认密码",
        "agree": "我已阅读并同意服务条款",
        "welcome": "欢迎回来。",
        "exists": "邮箱已存在",
        "created": "账户已创建，请登录",
        "invalid": "账号或密码错误",
        "signout": "退出登录",
        "balances": "资产概览",
        "ratever": "汇率版本",
        "transfer": "转账",
        "swap": "兑换",
        "history": "流水",
        "settings": "设置",
        "instant": "账户内转账（≤200ms 即时确认）",
        "asset": "币种",
        "amount": "金额",
        "to": "收款方（账号/备注）",
        "balance": "可用余额",
        "send": "转账",
        "sent_ok": "已提交转账：{amt:.2f} {a} → {to}，≤200ms 确认。",
        "swap_title": "稳定币兑换（固定汇率，零滑点）",
        "from": "从",
        "to2": "兑到",
        "rate_info": "汇率：1 {src} = {rate} {dst} • 手续费：{fee_pct:.2f}%（${fee:,.2f}）• 版本 {ver}",
        "swap_btn": "确认兑换",
        "swap_ok": "已兑换 {amt:.2f} {src} → {out:.2f} {dst}（汇率 {rate}，手续费 ${fee:,.2f}）。",
        "activity": "交易与对账",
        "no_activity": "暂无记录",
        "download": "导出 CSV",
        "settings_title": "设置与合规",
        "kyc": "实名状态",
        "verified": "已通过",
        "pending": "待完成",
        "demo_only": "演示环境。在生产环境将接入 KYC/KYT 与制裁名单。",
        "matrix": "每日 07:00 固定汇率矩阵",
        "regen": "重新生成演示汇率",
        "lang": "语言",
        "theme": "主题",
    },
    "EN": {
        "slogan": "One-click transfer, cross-currency seamless delivery",
        "landing_sub": "Demo only. Data resets on refresh.",
        "login_btn": "Sign in",
        "signin": "Sign in",
        "signup": "Sign up",
        "email": "Email",
        "password": "Password",
        "confirm_pwd": "Confirm password",
        "agree": "I agree to Terms",
        "welcome": "Welcome back.",
        "exists": "Email already exists",
        "created": "Account created. Please sign in",
        "invalid": "Invalid credentials",
        "signout": "Sign out",
        "balances": "Balances",
        "ratever": "Rate version",
        "transfer": "Transfer",
        "swap": "Swap",
        "history": "History",
        "settings": "Settings",
        "instant": "Internal transfer (≤200ms confirm)",
        "asset": "Asset",
        "amount": "Amount",
        "to": "To (account id / memo)",
        "balance": "Available",
        "send": "Send",
        "sent_ok": "Transfer submitted: {amt:.2f} {a} to {to}. ≤200ms confirmation.",
        "swap_title": "Stablecoin swap (fixed rate, zero slippage)",
        "from": "From",
        "to2": "To",
        "rate_info": "Rate: 1 {src} = {rate} {dst} • Fee: {fee_pct:.2f}% (${fee:,.2f}) • Version {ver}",
        "swap_btn": "Confirm swap",
        "swap_ok": "Swapped {amt:.2f} {src} → {out:.2f} {dst} (rate {rate}, fee ${fee:,.2f}).",
        "activity": "Activity & Statements",
        "no_activity": "No activity yet",
        "download": "Download CSV",
        "settings_title": "Settings & Compliance",
        "kyc": "KYC status",
        "verified": "Verified",
        "pending": "Pending",
        "demo_only": "Demo only. Production will integrate KYC/KYT and sanctions.",
        "matrix": "Rate matrix (published 07:00 UTC)",
        "regen": "Regenerate demo rates",
        "lang": "Language",
        "theme": "Theme",
    },
}

def t(key):
    return I18N[st.session_state.get("lang", "ZH")][key]

# -------------- theme & CSS --------------
def inject_css():
    BG1 = "#062b3a"   # 深蓝
    BG2 = "#041e2a"   # 更深蓝
    TEXT = "#F9FAFB"  # 主文字（近白）
    SUB  = "#D5DFEA"  # 次级文字
    DANGER = "#ff5a5f"  # 按钮色
    BORDER = "#334155"  # 深色描边

    st.markdown(f"""
    <style>
      /* 背景渐变 + 全局文字色 */
      .stApp {{
        background: linear-gradient(180deg, {BG1} 0%, {BG2} 70%);
        color: {TEXT};
      }}
      .main .block-container {{ background: transparent !important; }}
      header {{ background: transparent !important; }}

      /* 标题与正文对比度 */
      h1,h2,h3,h4,h5,h6 {{ color: {TEXT}; }}
      p, span, label, .stMarkdown, .stText, .stCaption {{ color: {TEXT}; }}
      .muted, .stCaption {{ color: {SUB}; }}

      /* 顶部品牌 */
      .x-brand {{ font-weight: 800; font-size: 20px; letter-spacing: .6px; color: {TEXT}; }}
      .x-logo {{ height: 38px; width: auto; border-radius: 8px; }}
      .x-slogan {{ 
        font-size: 42px; font-weight: 800; margin: 80px 0 8px 0; color: {TEXT};
        text-shadow: 0 2px 10px rgba(0,0,0,.35);
      }}
      .x-sub {{ color: {SUB}; text-shadow: 0 1px 6px rgba(0,0,0,.25); }}

      /* 卡片/面板 */
      .card {{
        background: rgba(15,23,42,.72);  /* 深色半透明 */
        border: 1px solid {BORDER};
        border-radius: 14px; padding: 14px; color: {TEXT};
      }}

      /* Tab 高对比 */
      .stTabs [data-baseweb="tab"] {{
        color: {TEXT};
      }}
      .stTabs [aria-selected="true"] {{
        border-bottom: 3px solid {TEXT};
      }}

      /* 按钮高对比 */
      .stButton>button {{
        background: {DANGER}; color: #FFFFFF; border: none; border-radius: 10px;
        font-weight: 700; box-shadow: 0 2px 8px rgba(0,0,0,.25);
      }}
      .stButton>button:focus {{ outline: 3px solid #fca5a5; }}

      /* 输入框：白底深字 + 深色边 + 聚焦高亮 */
      .stTextInput input, .stNumberInput input {{
        background: #FFFFFF !important; color: #0B1220 !important;
        border: 1px solid {BORDER} !important; border-radius: 10px !important;
      }}
      .stTextInput input:focus, .stNumberInput input:focus {{
        border-color: #22d3ee !important; box-shadow: 0 0 0 3px rgba(34,211,238,.35) !important;
      }}
      /* Select（BaseWeb）白底深字 */
      div[data-baseweb="select"] > div {{
        background: #FFFFFF !important; color: #0B1220 !important; border-radius: 10px !important;
        border: 1px solid {BORDER} !important;
      }}
      div[data-baseweb="select"] svg {{ fill: #0B1220 !important; }}

      /* Alert 提示条：重置为深色底高对比 */
      .stAlert {{
        background: rgba(15,23,42,.85) !important;
        border: 1px solid {BORDER} !important;
        color: {TEXT} !important;
        border-radius: 12px;
      }}

      /* 数据表标题也用浅色 */
      .stDataFrame thead tr th {{ color: {TEXT}; }}
    </style>
    """, unsafe_allow_html=True)

# -------------- util --------------
def today_rate_version():
    now = dt.datetime.utcnow()
    v = dt.datetime(now.year, now.month, now.day, 7, 0, 0)
    return f"v{v.strftime('%Y-%m-%d-07:00')}Z"

def build_rates():
    rng = np.random.default_rng(42)
    rates = {}
    for a in SUPPORTED:
        for b in SUPPORTED:
            if a == b:
                continue
            drift = (rng.random() - 0.5) * 0.002
            rates[f"{a}->{b}"] = round(1.0 + drift, 6)
    return rates

def add_history(kind, asset_from, asset_to, amount_in, amount_out, fee, cpty="", note=""):
    df = st.session_state.history
    row = {
        "time": dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
        "type": kind,
        "asset_from": asset_from,
        "asset_to": asset_to,
        "amount_in": round(float(amount_in or 0), 2),
        "amount_out": round(float(amount_out or 0), 2),
        "fee": round(float(fee or 0), 2),
        "counterparty": cpty,
        "note": note,
    }
    st.session_state.history = pd.concat([pd.DataFrame([row]), df], ignore_index=True)

def stat_card(label, value, hint=""):
    st.markdown(
        f"<div class='card'><div style='font-size:13px; color:#D5DFEA;'>{label}</div>"
        f"<div style='font-size:22px; font-weight:800; margin-top:4px; color:#F9FAFB;'>{value}</div>"
        f"<div class='muted'>{hint}</div></div>",
        unsafe_allow_html=True,
    )

# -------------- state --------------
def init_state():
    s = st.session_state
    s.setdefault("lang", "ZH")
    s.setdefault("route", "landing")  # landing | auth | app
    s.setdefault("users", {"demo@xpay.io": {"password": "demo123", "kyc": "Verified"}})
    s.setdefault("auth", {"logged_in": False, "email": None})
    s.setdefault("balances", {"USDT": 12500.00, "USDC": 5200.00, "BUSD": 3000.00, "DAI": 2500.00})
    s.setdefault("history", pd.DataFrame(columns=["time","type","asset_from","asset_to","amount_in","amount_out","fee","counterparty","note"]))
    s.setdefault("rates", build_rates())
    s.setdefault("rate_version", today_rate_version())

# -------------- auth forms --------------
def view_auth():
    st.markdown("### " + t("signin"))
    tabs = st.tabs([t("signin"), t("signup")])
    with tabs[0]:
        email = st.text_input(t("email"), value="demo@xpay.io")
        pwd = st.text_input(t("password"), type="password", value="demo123")
        if st.button(t("signin"), use_container_width=True, type="primary"):
            users = st.session_state.users
            if email in users and users[email]["password"] == pwd:
                st.session_state.auth = {"logged_in": True, "email": email}
                st.session_state.route = "app"
                st.success(t("welcome"))
                st.rerun()
            else:
                st.error(t("invalid"))
    with tabs[1]:
        email2 = st.text_input(t("email") + " *", key="reg_email")
        pwd2 = st.text_input(t("password") + " *", type="password", key="reg_pwd")
        pwd3 = st.text_input(t("confirm_pwd") + " *", type="password", key="reg_pwd2")
        agree = st.checkbox(t("agree"))
        ok = email2 and pwd2 and pwd3 and (pwd2 == pwd3) and agree
        if st.button(t("signup"), use_column_width=True, type="primary", disabled=not ok):
            users = st.session_state.users
            if email2 in users:
                st.error(t("exists"))
            else:
                users[email2] = {"password": pwd2, "kyc": "Pending"}
                st.success(t("created"))
                st.session_state.route = "auth"
                st.rerun()

# -------------- landing --------------
def view_landing():
    top = st.container()
    with top:
        c1, c2, c3 = st.columns([0.08, 0.74, 0.18])
        with c1:
            st.image("logo.png", use_column_width=True)
        with c2:
            st.markdown(f"<div class='x-left'><div class='x-brand'></div></div>", unsafe_allow_html=True)
        with c3:
            # 右上角：语言切换 + 登录按钮
            st.selectbox(t("lang"), ["ZH","EN"], index=["ZH","EN"].index(st.session_state["lang"]),
                         key="lang", label_visibility="collapsed")
            if st.button(t("login_btn"), use_container_width=True):
                st.session_state.route = "auth"
                st.rerun()

    st.markdown(f"<div class='x-slogan'>{t('slogan')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='x-sub'>{t('landing_sub')}</div>", unsafe_allow_html=True)


# -------------- app main --------------
def view_app():
    auth = st.session_state.auth
    # 顶栏：logo + 品牌 + 语言 + 退出
    top = st.container()
    with top:
        c1, c2, c3 = st.columns([0.08, 0.72, 0.20])
        with c1: st.image("logo.png", use_column_width=True)
        with c2: st.markdown(f"<div class='x-brand'></div>", unsafe_allow_html=True)
        with c3:
            st.selectbox(t("lang"), ["ZH","EN"], index=["ZH","EN"].index(st.session_state["lang"]),
                         key="lang", label_visibility="collapsed")
            if st.button(t("signout"), use_container_width=True):
                st.session_state.auth = {"logged_in": False, "email": None}
                st.session_state.route = "landing"
                st.rerun()
    st.markdown("---")


    balances = st.session_state.balances
    cA, cB, cC, cD, cE = st.columns([0.22,0.22,0.22,0.22,0.12])
    with cA: stat_card("USDT", f"${balances['USDT']:,.2f}", "5000")
    with cB: stat_card("USDC", f"${balances['USDC']:,.2f}", "4000")
    with cC: stat_card("BUSD", f"${balances['BUSD']:,.2f}", "1000")
    with cD: stat_card("DAI", f"${balances['DAI']:,.2f}", "200")
    with cE: stat_card(t("ratever"), st.session_state.rate_version, "07:00am UTC")

    tabs = st.tabs([t("transfer"), t("swap"), t("history"), t("settings")])

    # --- Transfer ---
    with tabs[0]:
        st.subheader(t("instant"))
        col1, col2, col3 = st.columns(3)
        with col1:
            asset = st.selectbox(t("asset"), SUPPORTED, index=0, key="xfer_asset")
        with col2:
            amount = st.number_input(t("amount"), min_value=0.0, value=250.0, step=10.0, key="xfer_amount")
        with col3:
            to_acct = st.text_input(t("to"), value="supplier_001", key="xfer_to")

        cross = st.checkbox("跨币种转账（A 用一种，B 收另一种）", value=True,
                            help="勾选后可选择收款方币种，系统按固定汇率+手续费计算到账")

        dst_asset = asset
        rate = 1.0
        fee = 0.0
        out_amt = amount

        if cross:
            c1, c2 = st.columns([0.35, 0.65])
            with c1:
                dst_asset = st.selectbox("收款币种", [x for x in SUPPORTED if x != asset], index=1, key="xfer_dst")
            with c2:
                rate_key = f"{asset}->{dst_asset}"
                rate = st.session_state.rates.get(rate_key, 1.0)
                fee = amount * FEE
                # 下取整到分：演示目的（生产中按币种精度）
                out_amt = np.floor((amount * rate * (1 - FEE)) * 100) / 100
                st.info(t("rate_info").format(src=asset, rate=rate, dst=dst_asset,
                                              fee_pct=FEE * 100, fee=fee, ver=st.session_state.rate_version))

        st.caption(f"{t('balance')}: ${st.session_state.balances[asset]:,.2f} {asset}")

        can_send = (amount > 0) and (amount <= st.session_state.balances[asset]) and (len(to_acct) >= 3)
        btn_label = t("send") if not cross else "提交转账（含兑币）"
        if st.button(btn_label, type="primary", use_container_width=True, disabled=not can_send, key="xfer_btn"):
            time.sleep(0.15)  # 模拟 ≤200ms 确认

            # 扣减发起人余额
            st.session_state.balances[asset] -= amount

            # 写入历史：区分同币种 vs 跨币种
            if cross:
                add_history(
                    kind="xfer_cross",
                    asset_from=asset,
                    asset_to=dst_asset,
                    amount_in=amount,
                    amount_out=out_amt,
                    fee=fee,
                    cpty=to_acct,
                    note=f"rate {rate} ver {st.session_state.rate_version}"
                )
                st.success(
                    f"已向 {to_acct} 支付 {amount:.2f} {asset}，收款方将到账 {out_amt:.2f} {dst_asset}（汇率 {rate}，手续费 ${fee:,.2f}，版本 {st.session_state.rate_version}）。")
            else:
                add_history(
                    kind="transfer",
                    asset_from=asset,
                    asset_to=asset,
                    amount_in=amount,
                    amount_out=amount,
                    fee=0,
                    cpty=to_acct,
                    note="internal"
                )
                st.success(t('sent_ok').format(amt=amount, a=asset, to=to_acct))

    # --- Swap ---
    with tabs[1]:
        st.subheader(t("swap_title"))
        c1, c2, c3, c4 = st.columns([0.25,0.25,0.25,0.25])
        with c1: src = st.selectbox(t("from"), SUPPORTED, index=0, key="swap_from")
        with c2: dst = st.selectbox(t("to2"), [x for x in SUPPORTED if x != src], index=1, key="swap_to")
        with c3: amt = st.number_input(t("amount"), min_value=0.0, value=500.0, step=10.0, key="swap_amt")
        with c4: st.write(""); st.write(f"**{t('balance')}:** ${balances[src]:,.2f}")

        rate_key = f"{src}->{dst}"
        rate = st.session_state.rates.get(rate_key, 1.0)
        fee = amt * FEE
        out = np.floor((amt * rate * (1 - FEE)) * 100) / 100

        st.info(t("rate_info").format(src=src, rate=rate, dst=dst, fee_pct=FEE*100, fee=fee, ver=st.session_state.rate_version))

        can = (src != dst) and amt > 0 and amt <= balances[src]
        if st.button(t("swap_btn"), type="primary", use_column_width=True, disabled=not can):
            balances[src] -= amt
            balances[dst] += out
            st.session_state.balances = balances
            add_history("swap", src, dst, amt, out, fee, note=f"rate {rate}")
            st.success(t("swap_ok").format(amt=amt, src=src, out=out, dst=dst, rate=rate, fee=fee))

    # --- History ---
    with tabs[2]:
        st.subheader(t("activity"))
        df = st.session_state.history.copy()
        if df.empty:
            st.info(t("no_activity"))
        else:
            st.dataframe(df, use_column_width=True, height=360)
            st.download_button(t("download"), df.to_csv(index=False).encode(), file_name="xpay_history.csv")

    # --- Settings ---
    with tabs[3]:
        st.subheader(t("settings_title"))
        users = st.session_state.users
        email = st.session_state.auth["email"]
        kyc = users[email]["kyc"]
        st.write(f"**{t('kyc')}:** {'✅ '+t('verified') if kyc=='Verified' else '⏳ '+t('pending')}")
        st.caption(t("demo_only"))
        st.markdown(f"**{t('matrix')}**")
        st.code("\n".join([f"{k}: {v}" for k, v in st.session_state.rates.items()]))
        if st.button(t("regen")):
            st.session_state.rates = build_rates()
            st.session_state.rate_version = today_rate_version()
            st.rerun()

# -------------- main --------------
st.set_page_config(page_title=f"{APP_NAME} Demo", page_icon="💸", layout="wide")
init_state()
inject_css()

route = st.session_state["route"]
if route == "landing":
    view_landing()
elif route == "auth":
    view_auth()
else:
    # app
    if not st.session_state.auth["logged_in"]:
        st.session_state.route = "auth"
        view_auth()
    else:
        view_app()
