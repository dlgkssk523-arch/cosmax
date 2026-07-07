"""
스펙노트 (SpecNote) — Streamlit Cloud 배포용 (단일 파일)

index.html 없이 app.py 하나로 동작합니다. 완전히 클라이언트 사이드(HTML/CSS/JS)로
동작하는 페이지를 아래 HTML_CONTENT 상수에 인라인으로 담아 components.html로 렌더링합니다.
- PDF 텍스트 추출: 브라우저에서 pdf.js(CDN)로 처리 (서버 전송 없음)
- AI 보완 추출: 사용자가 입력한 Anthropic API 키로 브라우저가 직접
  https://api.anthropic.com 을 호출 (Streamlit 서버는 관여하지 않음)

따라서 이 app.py에는 별도의 백엔드 로직이 없고, 인라인 HTML을
components.v1.html로 렌더링하는 역할만 합니다.
"""

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="스펙노트 (SpecNote) — 원료 스펙 관리",
    page_icon="🧪",
    layout="wide",
)

# 사이드바: iframe 높이 조절 (표에 행이 많아지면 늘려서 사용)
with st.sidebar:
    st.markdown("### ⚙️ 화면 설정")
    height = st.slider(
        "표시 영역 높이 (px)",
        min_value=800,
        max_value=3000,
        value=1500,
        step=100,
        help="원료 목록이 많아 표가 길어지면 높이를 늘려주세요.",
    )
    st.caption(
        "이 앱은 PDF 파싱과 AI 보완 추출을 모두 브라우저에서 직접 처리합니다. "
        "Anthropic API 키를 입력하면 브라우저가 api.anthropic.com을 직접 호출하며, "
        "Streamlit 서버로는 전송되지 않습니다. (프로토타입 용도 — 실서비스에는 "
        "백엔드 프록시를 두는 것을 권장합니다.)"
    )

# ---------------------------------------------------------------------------
# 아래는 원래 index.html의 내용을 그대로 인라인으로 옮긴 것입니다.
# (raw 문자열이므로 JS 정규식의 백슬래시 등이 그대로 유지됩니다.)
# ---------------------------------------------------------------------------
HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>스펙노트 (SpecNote) — 원료 스펙 관리</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700;800;900&display=swap" rel="stylesheet">
<style>
  :root{
    /* 메인: 딥블루 */
    --deep-blue:#1E3A5F;
    --deep-blue-600:#2A4E7A;   /* hover */
    --deep-blue-500:#3A5C87;   /* 밝은 키 */
    /* 보조: 차분한 틸(teal) — 신뢰감 있는 딥블루와 어울리는 포인트 */
    --accent:#1B8C9B;
    --accent-600:#15727F;      /* hover */
    --accent-soft:#E4F2F4;     /* 아주 연한 틸 */
    --bg:#FFFFFF;              /* 페이지 배경 */
    --surface:#F5F6F7;         /* 카드 배경: 아주 연한 회색 */
    --line:#E6E8EB;
    --line-strong:#D5D8DD;
    --text:#1C2A3A;
    --text-soft:#566072;
    --text-mute:#8A93A2;
    --ok:#137a4b;
    --shadow:0 1px 2px rgba(30,58,95,.05),0 8px 24px rgba(30,58,95,.07);
    --radius:14px;
  }
  *{box-sizing:border-box;margin:0;padding:0}
  html{-webkit-text-size-adjust:100%}
  body{
    font-family:"Noto Sans KR",-apple-system,BlinkMacSystemFont,"Segoe UI","Malgun Gothic","Apple SD Gothic Neo",Roboto,"Helvetica Neue",sans-serif;
    background:var(--bg);
    color:var(--text);
    font-size:16px;              /* 본문 기준: 읽기 편한 크기 */
    line-height:1.6;
    letter-spacing:-.1px;
    word-break:keep-all;         /* 한글 단어 단위 줄바꿈 */
    -webkit-font-smoothing:antialiased;
  }
  a{color:inherit;text-decoration:none}

  /* ---------- Header ---------- */
  header{
    position:sticky;top:0;z-index:50;
    background:rgba(255,255,255,.85);
    backdrop-filter:saturate(180%) blur(12px);
    border-bottom:1px solid var(--line);
  }
  .nav{
    max-width:1180px;margin:0 auto;padding:14px 24px;
    display:flex;align-items:center;justify-content:space-between;gap:16px;
  }
  .brand{display:flex;align-items:center;gap:10px;font-weight:700;font-size:18px;letter-spacing:-.2px}
  .logo{
    width:32px;height:32px;border-radius:9px;
    background:linear-gradient(135deg,var(--deep-blue),var(--accent));
    display:grid;place-items:center;color:#fff;font-size:16px;font-weight:800;
    box-shadow:0 4px 12px rgba(30,58,95,.30);
  }
  .logo svg{width:19px;height:19px}
  .brand small{display:block;font-size:11px;font-weight:500;color:var(--text-mute);letter-spacing:0}
  .nav-actions{display:flex;align-items:center;gap:10px}
  .btn{
    border:1px solid var(--line-strong);background:var(--surface);color:var(--text);
    padding:9px 16px;border-radius:10px;font-size:14px;font-weight:600;cursor:pointer;
    transition:.15s;white-space:nowrap;
  }
  .btn:hover{border-color:var(--accent);color:var(--accent)}
  .btn-primary{background:var(--accent);border-color:var(--accent);color:#fff}
  .btn-primary:hover{background:var(--accent-600);border-color:var(--accent-600);color:#fff}

  /* ---------- Layout ---------- */
  main{max-width:1080px;margin:0 auto;padding:64px 24px 96px}
  .hero{position:relative;margin-bottom:44px}
  .hero h1,.hero p{position:relative;z-index:1}
  .hero h1{font-size:34px;font-weight:900;line-height:1.3;letter-spacing:-.8px;margin-bottom:14px}
  .hero h1 .hl{color:var(--deep-blue)}
  .hero p{color:var(--text-soft);font-size:17px;line-height:1.65;max-width:660px}
  /* 히어로 배경 장식: 플라스크 + 분자 라인 그래픽 */
  .hero-deco{
    position:absolute;top:-18px;right:-6px;width:250px;height:auto;z-index:0;
    color:var(--deep-blue);opacity:.07;pointer-events:none;
  }

  /* 주요 카드 섹션 간 간격 */
  .block{margin-bottom:52px}
  .block:last-child{margin-bottom:0}

  .section-title{
    display:flex;align-items:center;gap:9px;
    font-size:19px;font-weight:800;margin-bottom:18px;color:var(--text);letter-spacing:-.3px;
  }
  .section-title .num{
    width:22px;height:22px;border-radius:6px;background:var(--accent-soft);
    color:var(--accent);font-size:12px;font-weight:800;display:grid;place-items:center;
  }

  /* ---------- Upload ---------- */
  .dropzone{
    background:var(--surface);border:2px dashed var(--line-strong);border-radius:var(--radius);
    padding:40px 24px;text-align:center;cursor:pointer;transition:.18s;box-shadow:var(--shadow);
  }
  .dropzone:hover{border-color:var(--accent);background:#EEF0F2}
  .dropzone.drag{border-color:var(--accent);background:var(--accent-soft);transform:scale(.997)}
  .dz-icon{
    width:56px;height:56px;margin:0 auto 14px;border-radius:14px;
    background:var(--accent-soft);color:var(--accent);display:grid;place-items:center;
  }
  .dz-icon svg{width:28px;height:28px}
  .dropzone h3{font-size:18px;font-weight:700;margin-bottom:6px}
  .dropzone p{color:var(--text-soft);font-size:15px}
  .dropzone .browse{color:var(--accent);font-weight:700;text-decoration:underline}
  .dz-hint{margin-top:10px;font-size:13px;color:var(--text-mute)}

  /* AI 폴백 설정 */
  .ai-box{
    margin-top:14px;background:var(--surface);border:1px solid var(--line);border-radius:12px;
    padding:12px 14px;display:flex;flex-wrap:wrap;align-items:center;gap:10px;
  }
  .ai-box .ai-label{display:flex;align-items:center;gap:8px;font-size:13px;font-weight:700;color:var(--text)}
  .ai-dot{width:8px;height:8px;border-radius:50%;background:var(--text-mute)}
  .ai-dot.on{background:var(--ok)}
  .ai-box input{
    flex:1;min-width:200px;border:1px solid var(--line);background:#fff;border-radius:8px;
    padding:9px 11px;font-size:13.5px;color:var(--text);outline:none;
  }
  .ai-box input:focus{border-color:var(--accent);box-shadow:0 0 0 3px rgba(27,140,155,.15)}
  .ai-box .ai-note{flex-basis:100%;font-size:12px;color:var(--text-mute);line-height:1.5}
  .ai-box .ai-note b{color:#DC2626;font-weight:700}

  .filelist{margin-top:14px;display:flex;flex-direction:column;gap:8px}
  .fileitem{
    display:flex;align-items:center;gap:12px;background:var(--surface);
    border:1px solid var(--line);border-radius:10px;padding:10px 14px;
    animation:pop .2s ease;
  }
  @keyframes pop{from{opacity:0;transform:translateY(4px)}to{opacity:1;transform:none}}
  .fi-badge{
    flex:none;width:38px;height:38px;border-radius:8px;background:#fdecec;color:#c53434;
    display:grid;place-items:center;font-size:10px;font-weight:800;
  }
  .fi-meta{flex:1;min-width:0}
  .fi-name{font-size:14.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
  .fi-sub{font-size:13px;color:var(--text-mute)}
  .fi-status{font-size:13px;font-weight:700;color:var(--ok);display:flex;align-items:center;gap:5px;flex:none}
  .fi-status .dot{width:7px;height:7px;border-radius:50%;background:var(--ok)}
  .fi-remove{flex:none;border:none;background:none;cursor:pointer;color:var(--text-mute);font-size:18px;line-height:1;padding:4px}
  .fi-remove:hover{color:#c53434}

  /* ---------- Search / Filter ---------- */
  .toolbar{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    padding:14px;box-shadow:var(--shadow);margin-bottom:16px;
    display:flex;gap:10px;flex-wrap:wrap;align-items:center;
  }
  .search{
    flex:1;min-width:220px;display:flex;align-items:center;gap:9px;
    background:var(--bg);border:1px solid var(--line);border-radius:10px;padding:10px 13px;
  }
  .search:focus-within{border-color:var(--accent);background:#fff;box-shadow:0 0 0 3px rgba(27,140,155,.15)}
  .search svg{width:18px;height:18px;color:var(--text-mute);flex:none}
  .search input{border:none;outline:none;background:none;width:100%;font-size:15.5px;color:var(--text)}
  select{
    border:1px solid var(--line);background:var(--surface);border-radius:10px;
    padding:10px 12px;font-size:14.5px;color:var(--text);cursor:pointer;outline:none;
  }
  select:focus{border-color:var(--accent)}
  .chips{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}
  .chip{
    border:1px solid var(--line-strong);background:var(--surface);border-radius:999px;
    padding:7px 14px;font-size:13.5px;font-weight:600;color:var(--text-soft);cursor:pointer;transition:.15s;
  }
  .chip:hover{border-color:var(--accent);color:var(--accent)}
  .chip.active{background:var(--deep-blue);border-color:var(--deep-blue);color:#fff}

  /* ---------- Table ---------- */
  .tablewrap{
    background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);
    box-shadow:var(--shadow);overflow:hidden;
  }
  .table-head{
    display:flex;align-items:center;justify-content:space-between;gap:12px;
    padding:14px 18px;border-bottom:1px solid var(--line);flex-wrap:wrap;
  }
  .table-head h3{font-size:16px;font-weight:700}
  .table-head .count{color:var(--text-mute);font-weight:500;font-size:13.5px}
  .edit-hint{font-size:13px;color:var(--accent);background:var(--accent-soft);padding:5px 11px;border-radius:8px;font-weight:600}
  .scroll{overflow-x:auto}
  table{width:100%;border-collapse:collapse;min-width:720px}
  thead th{
    text-align:left;font-size:12.5px;font-weight:700;color:var(--text-soft);
    letter-spacing:.2px;padding:13px 16px;
    background:#ECEEF1;border-bottom:1px solid var(--line);white-space:nowrap;
  }
  tbody td{padding:4px 16px;border-bottom:1px solid var(--line);font-size:15px;vertical-align:middle}
  tbody tr:last-child td{border-bottom:none}
  tbody tr:hover{background:#EEF6F7}
  .cell{
    min-height:38px;display:flex;align-items:center;padding:8px 10px;margin:2px -10px;
    border-radius:8px;cursor:text;transition:.12s;position:relative;
  }
  .cell:hover{background:var(--accent-soft);box-shadow:inset 0 0 0 1px rgba(27,140,155,.3)}
  .cell:hover::after{
    content:"✎";position:absolute;right:8px;color:var(--accent);font-size:12px;opacity:.7;
  }
  .cell.editing{background:#fff;box-shadow:inset 0 0 0 2px var(--accent)}
  .cell.editing::after{content:none}
  .cell input{border:none;outline:none;background:none;font:inherit;color:inherit;width:100%}
  /* 정규식/AI로도 못 찾은 값: '확인 필요' 빨간색 강조 */
  .cell.review{color:#DC2626;font-style:italic;font-weight:700;background:#FEECEC}
  .cell.review:hover{background:#FBD9D9;box-shadow:inset 0 0 0 1px rgba(220,38,38,.4)}
  .cell.review::after{color:#DC2626}
  /* 원료사(부제) 편집용 작은 셀 */
  .cell-sm{min-height:26px;font-size:13px;font-weight:500;color:var(--text-mute);padding:4px 8px;margin:2px -8px}
  .cell-sm.review{font-size:13px}
  .ingredient{font-weight:700;color:var(--deep-blue)}
  .supplier{font-size:13px;color:var(--text-mute);font-weight:500}
  .tag{
    display:inline-block;background:#E9EDF3;color:var(--deep-blue-500);
    font-size:12.5px;font-weight:600;padding:3px 9px;border-radius:6px;
  }
  .empty{padding:48px 20px;text-align:center;color:var(--text-mute);font-size:15px}

  footer{text-align:center;color:var(--text-mute);font-size:12.5px;padding:24px}

  /* ---------- Responsive ---------- */
  @media (max-width:640px){
    body{font-size:16px}              /* 모바일 본문 최소 16px 유지 */
    .nav{padding:12px 16px}
    .brand small{display:none}
    main{padding:40px 18px 64px}      /* 헤더-본문 여백 확보 */
    .hero{margin-bottom:34px}
    .hero-deco{width:150px;top:-6px;opacity:.05}   /* 모바일: 작게·더 옅게 */
    .hero h1{font-size:25px;line-height:1.35}   /* 모바일 제목 최소 크기 */
    .hero p{font-size:16px}
    .block{margin-bottom:40px}
    .section-title{font-size:17px}
    .dropzone{padding:32px 18px}
    .dropzone h3{font-size:17px}
    .dropzone p,.dz-hint{font-size:14px}
    .nav-actions .btn:not(.btn-primary){display:none}
    .toolbar{flex-direction:column;align-items:stretch}

    /* 손가락 탭 타깃: 최소 44px 높이 확보 */
    .btn,select,.search{min-height:44px}
    .btn{padding:11px 18px;font-size:15px}
    select{width:100%;padding:12px 14px}
    .chip{min-height:40px;display:inline-flex;align-items:center;padding:8px 16px;font-size:14px}
    .fi-remove{width:44px;height:44px;display:grid;place-items:center;font-size:22px}
    tbody td,.search input{font-size:15px}   /* 표·검색 글자 가독성 */
    .fi-sub,.fi-status,.supplier{font-size:13.5px}
  }

  /* 아주 좁은 화면(≤400px)에서 카드가 깨지지 않도록 */
  @media (max-width:400px){
    main{padding:32px 14px 56px}
    .hero h1{font-size:23px}
    .dropzone{padding:28px 14px}
    .fileitem{gap:10px;padding:10px 12px}
    .fi-badge{width:34px;height:34px}
    .table-head{padding:13px 14px}
    .edit-hint{font-size:12.5px}
    thead th,tbody td{padding-left:12px;padding-right:12px}
  }
</style>
</head>
<body>

<header>
  <div class="nav">
    <div class="brand">
      <span class="logo" aria-label="스펙노트 로고">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
          <path d="M9 3h6"/>
          <path d="M10 3v5.6L4.7 18a1.6 1.6 0 0 0 1.4 2.4h11.8A1.6 1.6 0 0 0 19.3 18L14 8.6V3"/>
          <path d="M8.3 15.2h7.4"/>
          <path d="M10 6.2h1.6M10 8h1.2"/>
        </svg>
      </span>
      <div>스펙노트<small>SpecNote · 원료 스펙 관리</small></div>
    </div>
    <div class="nav-actions">
      <button class="btn">사용 가이드</button>
      <button class="btn btn-primary">로그인</button>
    </div>
  </div>
</header>

<main>
  <section class="hero">
    <svg class="hero-deco" viewBox="0 0 260 210" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
      <!-- 삼각플라스크 -->
      <path d="M96 22h34"/>
      <path d="M104 22v36L74 120a9 9 0 0 0 8 13.5h62a9 9 0 0 0 8-13.5l-30-62V22"/>
      <path d="M88 106h52"/>
      <path d="M104 40h9M104 52h6"/>
      <!-- 분자 육각 고리 -->
      <path d="M170 44l26 0 13 22-13 22-26 0-13-22z"/>
      <circle cx="170" cy="44" r="3.6"/><circle cx="196" cy="44" r="3.6"/>
      <circle cx="209" cy="66" r="3.6"/><circle cx="196" cy="88" r="3.6"/>
      <circle cx="170" cy="88" r="3.6"/><circle cx="157" cy="66" r="3.6"/>
      <path d="M209 66h24"/><circle cx="239" cy="66" r="3.6"/>
    </svg>
    <h1>흩어진 원료 데이터시트를, <span class="hl">비교 가능한 한 장의 표</span>로.</h1>
    <p>여러 원료사의 TDS·MSDS PDF를 업로드하면 성분명·pH·점도·사용량·특징을 자동 추출해 정리합니다. 제형 연구원이 바로 비교하고 검토할 수 있습니다.</p>
  </section>

  <!-- 1. Upload -->
  <section class="block">
    <div class="section-title"><span class="num">1</span>데이터시트 업로드</div>
    <div class="dropzone" id="dropzone">
      <input type="file" id="fileInput" accept="application/pdf" multiple hidden>
      <div class="dz-icon">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </div>
      <h3>PDF를 여기로 끌어다 놓으세요</h3>
      <p>또는 <span class="browse">파일 찾아보기</span> — 여러 개를 한 번에 올릴 수 있습니다</p>
      <div class="dz-hint">지원 형식: PDF (TDS / MSDS) · 파일당 최대 20MB</div>
    </div>

    <!-- AI 폴백: 정규식으로 못 찾은 값을 Claude API로 보완 -->
    <div class="ai-box">
      <span class="ai-label"><span class="ai-dot" id="aiDot"></span>AI 보완 추출</span>
      <input type="password" id="apiKey" placeholder="Anthropic API 키 (sk-ant-...) — 정규식으로 못 찾은 값을 Claude가 보완">
      <div class="ai-note">
        정규식으로 항목을 찾지 못하면 <b>Claude API</b>로 보완 추출합니다. 키를 비우면 이 단계는 건너뛰고 값은 "확인 필요"로 남습니다.
        키는 <b>이 브라우저에만</b> 저장됩니다. 브라우저에서 직접 호출하므로 키가 노출될 수 있어 <b>로컬·프로토타입 전용</b>입니다 — 실제 배포 시 백엔드 프록시로 옮기세요.
      </div>
    </div>

    <div class="filelist" id="filelist"></div>
  </section>

  <!-- 2. Search / Filter -->
  <section class="block">
    <div class="section-title"><span class="num">2</span>원료 검색 &amp; 추출 결과</div>
    <div class="toolbar">
      <div class="search">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/>
        </svg>
        <input type="text" id="searchInput" placeholder="성분명 · 원료사명 · 특징으로 검색">
      </div>
      <select id="supplierFilter">
        <option value="">전체 원료사</option>
      </select>
      <select id="phFilter">
        <option value="">pH 조건</option>
        <option value="acid">산성 (pH &lt; 5.5)</option>
        <option value="neutral">중성 (5.5 – 7.5)</option>
        <option value="base">알칼리성 (pH &gt; 7.5)</option>
      </select>
    </div>

    <div class="chips" id="chips">
      <div class="chip active" data-tag="">전체</div>
      <div class="chip" data-tag="보습">보습</div>
      <div class="chip" data-tag="점증">점증</div>
      <div class="chip" data-tag="유화">유화</div>
      <div class="chip" data-tag="방부">방부</div>
      <div class="chip" data-tag="항산화">항산화</div>
    </div>

    <div class="tablewrap">
      <div class="table-head">
        <h3>추출 결과 미리보기 <span class="count" id="rowCount"></span></h3>
        <span class="edit-hint">✎ 셀을 클릭하면 바로 수정할 수 있어요</span>
      </div>
      <div class="scroll">
        <table>
          <thead>
            <tr>
              <th>성분명 / 원료사</th>
              <th>pH</th>
              <th>점도 (cps)</th>
              <th>권장 사용량</th>
              <th>특징</th>
            </tr>
          </thead>
          <tbody id="tbody"></tbody>
        </table>
      </div>
    </div>
  </section>
</main>

<footer>스펙노트 · SpecNote — 원료 스펙을 하나의 자산으로.</footer>

<!-- PDF 텍스트 추출: pdf.js (브라우저에서 직접 파싱, 서버 전송 없음) -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>
<script>
const REVIEW = '확인 필요';   // 정규식으로 못 찾은 값 표시

/* ---------- 데이터 모델 ----------
   데모 예시 표로 시작하고, PDF를 올리면 추출 결과가 표로 추가됩니다. */
let idSeq = 1;
const seed = [
  {ingredient:"Glycerin",                     supplier:"Emery Oleochemicals", ph:"5.5",  viscosity:"1,410 cps", usage:"3.0~10.0%", ph_class:"neutral", tag:"보습",   feature:"다목적 보습·습윤, 저자극 용제", demo:true},
  {ingredient:"Sodium Hyaluronate",           supplier:"브룸사이언스 바이오텍",  ph:"6.5",  viscosity:"1,200 cps", usage:"0.02~0.1%", ph_class:"neutral", tag:"보습",   feature:"고분자 히알루론산, 즉각·지속 보습막 형성", demo:true},
  {ingredient:"Butylene Glycol",              supplier:"OXEA",                ph:"6.0",  viscosity:"100 cps",   usage:"1.0~10.0%", ph_class:"neutral", tag:"보습",   feature:"보습·가용화 용제, 방부 시스템 보조", demo:true},
  {ingredient:"Xanthan Gum",                  supplier:"CP Kelco",            ph:"7.0",  viscosity:"1,600 cps", usage:"0.1~1.0%",  ph_class:"neutral", tag:"점증",   feature:"천연 점도 점증·현탁 안정화제", demo:true},
  {ingredient:"Carbomer 940",                 supplier:"Lubrizol",            ph:"3.0",  viscosity:"45,000 cps",usage:"0.1~0.5%",  ph_class:"acid",    tag:"점증",   feature:"고점도 투명 젤 형성 (중화 필요)", demo:true},
  {ingredient:"Cetearyl Alcohol",             supplier:"BASF",                ph:"–",    viscosity:"–",         usage:"1.0~5.0%",  ph_class:"",        tag:"유화",   feature:"O/W 유화 안정 및 경도 부여 지방알코올", demo:true},
  {ingredient:"Caprylic/Capric Triglyceride", supplier:"IOI Oleochemical",    ph:"–",    viscosity:"28 cps",    usage:"2.0~15.0%", ph_class:"",        tag:"유화",   feature:"가볍게 퍼지는 저자극 에몰리언트 오일", demo:true},
  {ingredient:"Phenoxyethanol",               supplier:"Ashland",             ph:"6.5",  viscosity:"30 cps",    usage:"0.3~1.0%",  ph_class:"neutral", tag:"방부",   feature:"광범위 스펙트럼 방부제 (파라벤 프리)", demo:true},
  {ingredient:"1,2-Hexanediol",               supplier:"현대바이오랜드",       ph:"6.2",  viscosity:"60 cps",    usage:"0.3~2.0%",  ph_class:"neutral", tag:"방부",   feature:"방부 보조·보습, 파라벤 대체 멀티사", demo:true},
  {ingredient:"Tocopheryl Acetate",           supplier:"DSM",                 ph:"–",    viscosity:"3,000 cps", usage:"0.1~1.0%",  ph_class:"",        tag:"항산화", feature:"지용성 비타민 E, 산패 방지 항산화", demo:true},
];
const ROWS = seed.map(r=>({id:'r'+(idSeq++), ...r}));

const tbody = document.getElementById('tbody');
const searchInput = document.getElementById('searchInput');
const supplierFilter = document.getElementById('supplierFilter');
const phFilter = document.getElementById('phFilter');
const chips = document.getElementById('chips');
const rowCount = document.getElementById('rowCount');
let activeTag = "";

/* ---------- 유틸 ---------- */
function esc(s){ return String(s).replace(/[&<>"]/g, c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c])); }
function isReview(v){ return !v || v===REVIEW; }
function rowById(id){ return ROWS.find(r=>r.id===id); }

/* pH 값 → 필터용 산성/중성/알칼리성 분류 */
function phClass(ph){
  const m = String(ph).match(/-?\d{1,2}(?:\.\d+)?/);
  if(!m) return '';
  const v = parseFloat(m[0]);
  if(isNaN(v)) return '';
  if(v < 5.5) return 'acid';
  if(v <= 7.5) return 'neutral';
  return 'base';
}

/* 원료사 필터 옵션 재구성(선택값 유지) */
function refreshSuppliers(){
  const cur = supplierFilter.value;
  const list = [...new Set(ROWS.map(r=>r.supplier).filter(s=>!isReview(s)))].sort();
  supplierFilter.innerHTML = '<option value="">전체 원료사</option>' +
    list.map(s=>`<option value="${esc(s)}">${esc(s)}</option>`).join('');
  if(list.includes(cur)) supplierFilter.value = cur;
}

/* ---------- 표 렌더 ---------- */
function cell(field, value, extra=''){
  const review = isReview(value);
  return `<div class="cell${extra?' '+extra:''}${review?' review':''}" data-field="${field}">${review?REVIEW:esc(value)}</div>`;
}
function render(){
  const q = searchInput.value.trim().toLowerCase();
  const sup = supplierFilter.value;
  const ph = phFilter.value;

  const rows = ROWS.filter(d=>{
    const hay = [d.ingredient,d.supplier,d.feature,d.tag].join(' ').toLowerCase();
    const hitQ = !q || hay.includes(q);
    const hitSup = !sup || d.supplier===sup;
    const hitPh = !ph || d.ph_class===ph;
    const hitTag = !activeTag || d.tag===activeTag;
    return hitQ && hitSup && hitPh && hitTag;
  });

  rowCount.textContent = `· ${rows.length}건`;

  if(!rows.length){
    tbody.innerHTML = `<tr><td colspan="5"><div class="empty">${ROWS.length? '조건에 맞는 자료가 없습니다. 검색이나 필터를 조정해 보세요.' : 'PDF를 업로드하면 추출 결과가 여기에 표시됩니다.'}</div></td></tr>`;
    return;
  }

  tbody.innerHTML = rows.map(d=>`
    <tr data-id="${d.id}">
      <td>
        ${cell('ingredient', d.ingredient, 'ingredient')}
        ${cell('supplier', d.supplier, 'cell-sm supplier')}
      </td>
      <td>${cell('ph', d.ph)}</td>
      <td>${cell('viscosity', d.viscosity)}</td>
      <td>${cell('usage', d.usage)}</td>
      <td>${d.tag?`<span class="tag">${esc(d.tag)}</span> `:''}${cell('feature', d.feature)}</td>
    </tr>`).join('');
}

/* ---------- 인라인 수정 (같은 데이터 모델에 저장) ---------- */
tbody.addEventListener('click', e=>{
  const cellEl = e.target.closest('.cell');
  if(!cellEl || cellEl.classList.contains('editing')) return;
  const tr = cellEl.closest('tr');
  const row = rowById(tr.dataset.id);
  if(!row) return;
  const field = cellEl.dataset.field;
  const orig = isReview(row[field]) ? '' : row[field];

  cellEl.classList.remove('review');
  cellEl.classList.add('editing');
  cellEl.innerHTML = `<input value="${esc(orig)}">`;
  const input = cellEl.querySelector('input');
  input.focus(); input.select();

  const commit = ()=>{
    const val = input.value.trim();
    row[field] = val || REVIEW;
    if(field==='ph') row.ph_class = phClass(row.ph);
    if(field==='supplier') refreshSuppliers();
    render();
  };
  input.addEventListener('blur', commit);
  input.addEventListener('keydown', ev=>{
    if(ev.key==='Enter'){ input.blur(); }
    if(ev.key==='Escape'){ input.removeEventListener('blur', commit); render(); }
  });
});

/* ---------- 검색 / 필터 ---------- */
searchInput.addEventListener('input', render);
supplierFilter.addEventListener('change', render);
phFilter.addEventListener('change', render);
chips.addEventListener('click', e=>{
  const chip = e.target.closest('.chip');
  if(!chip) return;
  chips.querySelectorAll('.chip').forEach(c=>c.classList.remove('active'));
  chip.classList.add('active');
  activeTag = chip.dataset.tag;
  render();
});

/* ---------- 업로드 (드래그&드롭 + 클릭) ---------- */
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const filelist = document.getElementById('filelist');

dropzone.addEventListener('click', ()=>fileInput.click());
fileInput.addEventListener('change', ()=>{ handleFiles(fileInput.files); fileInput.value=''; });

['dragenter','dragover'].forEach(ev=>dropzone.addEventListener(ev, e=>{
  e.preventDefault(); dropzone.classList.add('drag');
}));
['dragleave','drop'].forEach(ev=>dropzone.addEventListener(ev, e=>{
  e.preventDefault(); if(ev!=='drop'||!dropzone.contains(e.relatedTarget)) dropzone.classList.remove('drag');
}));
dropzone.addEventListener('drop', e=>{
  e.preventDefault(); dropzone.classList.remove('drag');
  handleFiles(e.dataTransfer.files);
});

function fmtSize(b){ return b>=1048576 ? (b/1048576).toFixed(1)+' MB' : Math.max(1,Math.round(b/1024))+' KB'; }

/* ---------- pdf.js: PDF 텍스트 추출 ---------- */
if(window.pdfjsLib){
  pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js';
}
async function extractText(file){
  const buf = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({data:buf}).promise;
  let text = '';
  for(let i=1; i<=pdf.numPages; i++){
    const page = await pdf.getPage(i);
    const content = await page.getTextContent();
    text += content.items.map(it=>it.str).join(' ') + '\n';
  }
  return text;
}

/* ---------- 정보 추출 (정규식) ---------- */
function firstMatch(t, patterns){
  for(const re of patterns){ const m = t.match(re); if(m) return m; }
  return null;
}
function parseSpec(raw, fileName){
  const t = ' ' + raw.replace(/[·•—–]/g,' ').replace(/\s+/g,' ').trim() + ' ';

  // pH (범위 인식)
  let ph = REVIEW;
  const phm = t.match(/\bpH\b\s*(?:value)?\s*(?:\(\s*[^)]*\))?\s*[:=]?\s*(?:approx\.?|about|ca\.?|약)?\s*(\d{1,2}(?:\.\d+)?)\s*(?:[-~]\s*(\d{1,2}(?:\.\d+)?))?/i);
  if(phm) ph = phm[2] ? `${phm[1]}~${phm[2]}` : phm[1];

  // 점도 (Viscosity)
  let viscosity = REVIEW;
  const vm = firstMatch(t, [
    /(?:viscosity|점도)\D{0,20}?([\d.,]+)\s*(?:[-~]\s*([\d.,]+))?\s*(cps|cp|mpa\.?\s?s|mpas|pa\.?\s?s)?/i
  ]);
  if(vm){ const unit = vm[3] ? ' '+vm[3].replace(/\s+/g,'') : ''; viscosity = (vm[2]?`${vm[1]}~${vm[2]}`:vm[1]) + unit; }

  // 사용량 (Usage / dosage)
  let usage = REVIEW;
  const um = firstMatch(t, [
    /(?:recommended\s*(?:use|usage|dosage|dose|level|concentration)|use\s*(?:level|rate)|usage\s*(?:level|rate)?|dosage|dose\s*level|사용량|권장\s*(?:사용량|첨가량)|첨가량)\D{0,20}?([\d.,]+\s*(?:[-~]\s*[\d.,]+)?\s*%)/i,
    /([\d.,]+\s*[-~]\s*[\d.,]+\s*%)/            // 폴백: 임의의 % 범위
  ]);
  if(um) usage = um[1].replace(/\s+/g,'');

  // 다음 라벨(예: "Appearance:") 직전까지 값 캡처를 돕기 위한 종료 조건
  const STOP = String.raw`(?:[.;]|\s{2,}|\s(?=[A-Z][A-Za-z]{2,}\s*[:\-])|$)`;

  // 성분명 (INCI name) — 라벨 우선, 없으면 파일명
  let ingredient = null;
  const im = firstMatch(t, [
    new RegExp(String.raw`INCI\s*(?:name)?\s*[:\-]\s*([A-Za-z][A-Za-z0-9,\-\/&() ]*?)` + STOP, 'i'),
    new RegExp(String.raw`(?:성분명|제품명|product\s*name|trade\s*name)\s*[:\-]\s*(\S[^\n]*?)` + STOP, 'i')
  ]);
  if(im) ingredient = im[1].trim().replace(/[\s,;.]+$/,'');
  if(!ingredient) ingredient = fileName.replace(/\.pdf$/i,'').trim() || REVIEW;

  // 특징 (Description / Feature)
  let feature = REVIEW;
  const fm = firstMatch(t, [
    new RegExp(String.raw`(?:description|features?|characteristics?|properties|benefits?|특징|성상|외관|용도|application)\s*[:\-]\s*(\S[^\n]{3,140}?)` + STOP, 'i')
  ]);
  if(fm) feature = fm[1].trim();

  // 원료사 (Supplier / Manufacturer)
  let supplier = REVIEW;
  const sm = firstMatch(t, [
    new RegExp(String.raw`(?:supplier|manufacturer|producer|제조사|공급사|원료사|company|maker)\s*[:\-]\s*(\S[^\n]*?)` + STOP, 'i')
  ]);
  if(sm) supplier = sm[1].trim().replace(/[\s,;.]+$/,'');

  return {ingredient, supplier, ph, viscosity, usage, feature, ph_class: phClass(ph), tag:''};
}

/* ---------- AI 보완 추출 (Claude API, 브라우저 직접 호출) ---------- */
const AI_MODEL = 'claude-opus-4-8';
const apiKeyInput = document.getElementById('apiKey');
const aiDot = document.getElementById('aiDot');
const KEY_STORE = 'specnote_anthropic_key';

// 저장된 키 복원 + 상태 표시
apiKeyInput.value = localStorage.getItem(KEY_STORE) || '';
function refreshAiDot(){ aiDot.classList.toggle('on', !!apiKeyInput.value.trim()); }
refreshAiDot();
apiKeyInput.addEventListener('input', ()=>{
  const v = apiKeyInput.value.trim();
  if(v) localStorage.setItem(KEY_STORE, v); else localStorage.removeItem(KEY_STORE);
  refreshAiDot();
});
function getApiKey(){ return apiKeyInput.value.trim(); }

// 정규식이 못 찾은 필드를 Claude에게 JSON으로 요청해 보완
async function aiExtract(text, missingFields){
  const key = getApiKey();
  if(!key || !missingFields.length) return null;

  const labelKo = {ingredient:'성분명(INCI name)', ph:'pH', viscosity:'점도(viscosity)', usage:'권장 사용량', feature:'특징(description)', supplier:'원료사(제조사)'};
  const wanted = missingFields.map(f=>`"${f}"(${labelKo[f]||f})`).join(', ');

  const body = {
    model: AI_MODEL,
    max_tokens: 1024,
    system: '너는 화장품 원료 데이터시트(TDS/MSDS)에서 스펙을 추출하는 도우미다. 반드시 JSON 객체 하나만 출력한다. 코드펜스나 설명 문구를 절대 덧붙이지 마라.',
    messages: [{
      role: 'user',
      content:
        `다음 원료 데이터시트 텍스트에서 아래 항목만 추출해 JSON으로 반환해줘: ${wanted}.\n` +
        `- 값을 찾을 수 없으면 해당 키는 null 로 둬.\n` +
        `- pH는 범위면 "5.5~7.0" 형식, 점도는 단위 포함(예 "1200 cps"), 사용량은 "% 범위" 형식으로.\n` +
        `- 키 이름은 영어(${missingFields.join(', ')})로만 사용.\n\n` +
        `<텍스트>\n${text.slice(0, 12000)}\n</텍스트>`
    }]
  };

  const resp = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      'x-api-key': key,
      'anthropic-version': '2023-06-01',
      'anthropic-dangerous-direct-browser-access': 'true'
    },
    body: JSON.stringify(body)
  });
  if(!resp.ok){
    const detail = await resp.text().catch(()=> '');
    throw new Error(`Claude API ${resp.status}: ${detail.slice(0,200)}`);
  }
  const data = await resp.json();
  const out = (data.content || []).filter(b=>b.type==='text').map(b=>b.text).join('');
  const m = out.match(/\{[\s\S]*\}/);           // 혹시 모를 여분 텍스트 제거
  if(!m) return null;
  return JSON.parse(m[0]);
}

/* ---------- 파일 처리: 추출 → 표 추가 ---------- */
function makeCard(f){
  const item = document.createElement('div');
  item.className = 'fileitem';
  item.innerHTML = `
    <span class="fi-badge">PDF</span>
    <div class="fi-meta">
      <div class="fi-name">${esc(f.name)}</div>
      <div class="fi-sub">${fmtSize(f.size)} · 추출 중…</div>
    </div>
    <span class="fi-status" style="color:var(--text-mute)"><span class="dot" style="background:var(--text-mute)"></span>분석 중</span>
    <button class="fi-remove" title="제거">&times;</button>`;
  filelist.appendChild(item);
  item.querySelector('.fi-remove').addEventListener('click', ()=>item.remove());
  return item;
}

const RED = '#DC2626';
function setStatus(st, sub, color, label, subText){
  st.style.color = color;
  st.innerHTML = `<span class="dot" style="background:${color}"></span>${label}`;
  if(subText!=null) sub.textContent = subText;
}
const AI_FIELDS = ['ingredient','supplier','ph','viscosity','usage','feature'];

async function handleFiles(files){
  for(const f of [...files]){
    if(f.type && f.type!=='application/pdf' && !/\.pdf$/i.test(f.name)) continue;
    const card = makeCard(f);
    const sub = card.querySelector('.fi-sub');
    const st  = card.querySelector('.fi-status');
    try{
      const text = await extractText(f);
      const row = parseSpec(text, f.name);
      row.id = 'r'+(idSeq++);
      ROWS.push(row);
      refreshSuppliers();
      render();

      // 1) 정규식으로 못 찾은 필드 목록
      let missing = AI_FIELDS.filter(k=>isReview(row[k]));

      // 2) AI 보완 (키가 있고 남은 필드가 있을 때)
      let aiUsed = false;
      if(missing.length && getApiKey()){
        setStatus(st, sub, 'var(--accent)', 'AI 보완 중', `${fmtSize(f.size)} · AI로 ${missing.length}개 항목 보완 중…`);
        try{
          const ai = await aiExtract(text, missing);
          if(ai){
            aiUsed = true;
            for(const k of missing){
              const v = ai[k];
              if(v!=null && String(v).trim()){
                row[k] = String(v).trim();
                if(k==='ph') row.ph_class = phClass(row.ph);
              }
            }
            refreshSuppliers();
            render();
            missing = AI_FIELDS.filter(k=>isReview(row[k]));   // 보완 후 남은 것 재계산
          }
        }catch(aiErr){
          console.error('AI 보완 실패:', aiErr);
          setStatus(st, sub, RED, '완료(AI 실패)',
            `${fmtSize(f.size)} · 정규식 추출 완료 · AI 보완 실패 (${String(aiErr.message||aiErr).slice(0,60)})`);
          continue;
        }
      }

      // 3) 최종 상태 — 남은 확인 필요는 빨간색
      const via = aiUsed ? ' · AI 보완' : '';
      if(missing.length){
        setStatus(st, sub, RED, '검토 필요',
          `${fmtSize(f.size)} · 추출 완료${via} · 확인 필요 ${missing.length}개`);
      }else{
        setStatus(st, sub, 'var(--ok)', '추출 완료', `${fmtSize(f.size)} · 추출 완료${via}`);
      }
    }catch(err){
      console.error('PDF 추출 실패:', err);
      setStatus(st, sub, RED, '실패', `${fmtSize(f.size)} · 추출 실패 (텍스트 없는 스캔본일 수 있음)`);
    }
  }
}

refreshSuppliers();
render();
</script>
</body>
</html>"""

components.html(HTML_CONTENT, height=height, scrolling=True)
