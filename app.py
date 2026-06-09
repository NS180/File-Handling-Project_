import streamlit as st
from pathlib import Path
import os
import time


st.set_page_config(
    page_title="FileVault",
    page_icon="🗂️",
    layout="centered",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Space+Mono:wght@400;700&display=swap');

/* ── Reset & Base ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0E0F11 !important;
    color: #E8E6E1 !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

[data-testid="stAppViewContainer"] > .main > div {
    padding-top: 2rem;
    padding-bottom: 4rem;
}

/* hide default streamlit chrome */
#MainMenu, footer, header { visibility: hidden; }
[data-testid="stDecoration"] { display: none; }

/* ── Hero header ── */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    border-bottom: 1px solid #1E2028;
    margin-bottom: 2.5rem;
}
.hero-eyebrow {
    font-family: 'Space Mono', monospace;
    font-size: 0.7rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #5B8AF0;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 3rem;
    font-weight: 700;
    letter-spacing: -0.03em;
    line-height: 1.05;
    color: #F0EDE8;
    margin: 0 0 0.6rem;
}
.hero-title span { color: #5B8AF0; }
.hero-sub {
    font-size: 0.95rem;
    color: #6B7280;
    font-weight: 400;
    margin: 0;
}

/* ── Operation tabs ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background: #151619 !important;
    border-radius: 12px;
    padding: 4px;
    border: 1px solid #1E2028;
}
.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 8px !important;
    color: #6B7280 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 500 !important;
    font-size: 0.875rem !important;
    padding: 0.5rem 1.25rem !important;
    border: none !important;
    transition: all 0.15s ease !important;
}
.stTabs [aria-selected="true"] {
    background: #1E2230 !important;
    color: #5B8AF0 !important;
}
.stTabs [data-baseweb="tab-highlight"] { display: none !important; }
.stTabs [data-baseweb="tab-border"] { display: none !important; }

/* ── Cards ── */
.op-card {
    background: #151619;
    border: 1px solid #1E2028;
    border-radius: 16px;
    padding: 2rem 2rem 2.25rem;
    margin-top: 1.5rem;
}
.op-card-title {
    font-size: 1.05rem;
    font-weight: 600;
    color: #F0EDE8;
    margin-bottom: 0.3rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}
.op-card-desc {
    font-size: 0.82rem;
    color: #6B7280;
    margin-bottom: 1.75rem;
    line-height: 1.5;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stTextArea textarea {
    background: #0E0F11 !important;
    border: 1px solid #2A2D38 !important;
    border-radius: 8px !important;
    color: #E8E6E1 !important;
    font-family: 'Space Mono', monospace !important;
    font-size: 0.85rem !important;
    padding: 0.6rem 0.85rem !important;
    transition: border-color 0.15s ease !important;
}
.stTextInput > div > div > input:focus,
.stTextArea textarea:focus {
    border-color: #5B8AF0 !important;
    box-shadow: 0 0 0 3px rgba(91,138,240,0.12) !important;
}
.stTextInput label, .stTextArea label {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #9CA3AF !important;
    font-family: 'Space Grotesk', sans-serif !important;
}

/* ── Buttons ── */
.stButton > button {
    background: #5B8AF0 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.875rem !important;
    padding: 0.6rem 1.5rem !important;
    transition: all 0.15s ease !important;
    letter-spacing: 0.01em !important;
}
.stButton > button:hover {
    background: #3B6FE8 !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(91,138,240,0.3) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* Danger button variant via extra class trick */
[data-testid="stButton"] button.danger-btn {
    background: #1A1011 !important;
    color: #F87171 !important;
    border: 1px solid #3B1818 !important;
}

/* ── Radio / select ops ── */
.stRadio [data-testid="stWidgetLabel"] {
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em !important;
    text-transform: uppercase !important;
    color: #9CA3AF !important;
}
.stRadio > div { gap: 8px; }
.stRadio > div > label {
    background: #0E0F11 !important;
    border: 1px solid #2A2D38 !important;
    border-radius: 8px !important;
    padding: 0.45rem 1rem !important;
    font-size: 0.85rem !important;
    color: #9CA3AF !important;
    cursor: pointer !important;
    transition: all 0.15s !important;
}
.stRadio > div > label:has(input:checked) {
    border-color: #5B8AF0 !important;
    color: #5B8AF0 !important;
    background: #111827 !important;
}

/* ── Alerts / feedback ── */
.stSuccess > div, .stError > div, .stWarning > div, .stInfo > div {
    border-radius: 10px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.875rem !important;
    border-left-width: 3px !important;
}
.stSuccess > div { background: #051A10 !important; border-color: #34D399 !important; color: #6EE7B7 !important; }
.stError > div   { background: #1A0505 !important; border-color: #F87171 !important; color: #FCA5A5 !important; }
.stWarning > div { background: #1A1000 !important; border-color: #FBBF24 !important; color: #FDE68A !important; }
.stInfo > div    { background: #05101A !important; border-color: #5B8AF0 !important; color: #93C5FD !important; }

/* ── File content display ── */
.file-content-box {
    background: #0B0C0E;
    border: 1px solid #1E2028;
    border-left: 3px solid #5B8AF0;
    border-radius: 10px;
    padding: 1.25rem 1.5rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.82rem;
    color: #A5B4FC;
    white-space: pre-wrap;
    word-break: break-word;
    line-height: 1.7;
    max-height: 320px;
    overflow-y: auto;
    margin-top: 1rem;
}
.file-meta {
    font-family: 'Space Mono', monospace;
    font-size: 0.72rem;
    color: #4B5563;
    margin-bottom: 0.4rem;
    letter-spacing: 0.04em;
}

/* ── File list in sidebar ── */
.file-pill {
    display: inline-block;
    background: #151619;
    border: 1px solid #2A2D38;
    border-radius: 6px;
    padding: 0.25rem 0.65rem;
    font-family: 'Space Mono', monospace;
    font-size: 0.75rem;
    color: #9CA3AF;
    margin: 3px 3px 3px 0;
}

/* ── Divider ── */
hr { border-color: #1E2028 !important; margin: 1.5rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #151619; }
::-webkit-scrollbar-thumb { background: #2A2D38; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #5B8AF0; }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────
WORKSPACE = Path("filevault_workspace")
WORKSPACE.mkdir(exist_ok=True)

def workspace_path(name: str) -> Path:
    """Resolve a filename inside the workspace, blocking traversal."""
    p = (WORKSPACE / name).resolve()
    if not str(p).startswith(str(WORKSPACE.resolve())):
        raise ValueError("Invalid file path.")
    return p

def list_files() -> list[Path]:
    return sorted(WORKSPACE.iterdir()) if WORKSPACE.exists() else []

def file_size_label(path: Path) -> str:
    sz = path.stat().st_size
    if sz < 1024: return f"{sz} B"
    if sz < 1024**2: return f"{sz/1024:.1f} KB"
    return f"{sz/1024**2:.1f} MB"


# ─── Hero ────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">Python File Manager</div>
    <h1 class="hero-title">File<span>Vault</span></h1>
    <p class="hero-sub">Create · Read · Update · Delete — clean and simple.</p>
</div>
""", unsafe_allow_html=True)


# ─── Sidebar — live file browser ────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='font-family:"Space Grotesk",sans-serif; padding:1rem 0 0.5rem'>
        <div style='font-size:0.7rem;letter-spacing:0.2em;text-transform:uppercase;color:#4B5563;margin-bottom:0.75rem'>Workspace</div>
    </div>""", unsafe_allow_html=True)

    files = list_files()
    if files:
        for f in files:
            meta = file_size_label(f)
            st.markdown(f"""
            <div style='display:flex;justify-content:space-between;align-items:center;
                        padding:0.5rem 0.75rem;margin-bottom:6px;background:#151619;
                        border:1px solid #1E2028;border-radius:8px;'>
                <span style='font-family:"Space Mono",monospace;font-size:0.78rem;color:#A5B4FC'>📄 {f.name}</span>
                <span style='font-size:0.7rem;color:#4B5563'>{meta}</span>
            </div>""", unsafe_allow_html=True)
    else:
        st.markdown("""<div style='font-size:0.82rem;color:#4B5563;font-family:"Space Grotesk",sans-serif;
            padding:1rem 0;text-align:center;border:1px dashed #1E2028;border-radius:8px;'>
            No files yet.<br><span style='font-size:0.75rem'>Create one to start.</span></div>""",
            unsafe_allow_html=True)

    st.markdown("<div style='margin-top:1.5rem;font-size:0.68rem;color:#2A2D38;font-family:\"Space Mono\",monospace;'>filevault_workspace/</div>", unsafe_allow_html=True)


# ─── Main tabs ──────────────────────────────────────────────────────────────
tab_create, tab_read, tab_update, tab_delete = st.tabs([
    "✦ Create", "◎ Read", "⟳ Update", "✕ Delete"
])



# CREATE

with tab_create:
    st.markdown("""
    <div class="op-card">
        <div class="op-card-title">✦ Create a new file</div>
        <div class="op-card-desc">Name your file (e.g. <code style='color:#5B8AF0'>notes.txt</code>), write its contents, and save it to the workspace.</div>
    </div>""", unsafe_allow_html=True)

    with st.container():
        c_name = st.text_input("File name", placeholder="e.g. hello.txt", key="c_name")
        c_data = st.text_area("File contents", placeholder="Write anything here…", height=160, key="c_data")

        if st.button("Create file", key="btn_create"):
            if not c_name.strip():
                st.error("Enter a file name first.")
            else:
                try:
                    path = workspace_path(c_name.strip())
                    if path.exists():
                        st.warning(f"**{c_name}** already exists. Use Update to edit it.")
                    else:
                        path.write_text(c_data)
                        st.success(f"**{c_name}** created successfully!")
                        time.sleep(0.4)
                        st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")


# ════════════════════════════════════════════════════════════════════════════
# READ
# ════════════════════════════════════════════════════════════════════════════
with tab_read:
    st.markdown("""
    <div class="op-card">
        <div class="op-card-title">◎ Read a file</div>
        <div class="op-card-desc">Enter a file name to view its contents below.</div>
    </div>""", unsafe_allow_html=True)

    files = list_files()
    file_names = [f.name for f in files]

    if file_names:
        r_name = st.selectbox("Choose a file", options=file_names, key="r_name")
        if st.button("Read file", key="btn_read"):
            try:
                path = workspace_path(r_name)
                content = path.read_text()
                size = file_size_label(path)
                lines = content.count("\n") + 1 if content else 0
                st.markdown(f"<div class='file-meta'>{r_name} · {size} · {lines} line{'s' if lines != 1 else ''}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='file-content-box'>{content if content else '<em style=\"color:#4B5563\">Empty file.</em>'}</div>", unsafe_allow_html=True)
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("No files in the workspace yet. Create one first.")


# ════════════════════════════════════════════════════════════════════════════
# UPDATE
# ════════════════════════════════════════════════════════════════════════════
with tab_update:
    st.markdown("""
    <div class="op-card">
        <div class="op-card-title">⟳ Update a file</div>
        <div class="op-card-desc">Rename it, append more content, or overwrite it entirely.</div>
    </div>""", unsafe_allow_html=True)

    files = list_files()
    file_names = [f.name for f in files]

    if file_names:
        u_name = st.selectbox("Choose a file", options=file_names, key="u_name")
        u_op = st.radio(
            "Operation",
            ["Rename", "Append", "Overwrite"],
            horizontal=True,
            key="u_op"
        )

        if u_op == "Rename":
            u_new = st.text_input("New file name", placeholder="new_name.txt", key="u_new")
            if st.button("Rename file", key="btn_rename"):
                if not u_new.strip():
                    st.error("Enter a new name.")
                else:
                    try:
                        src = workspace_path(u_name)
                        dst = workspace_path(u_new.strip())
                        if dst.exists():
                            st.warning(f"**{u_new}** already exists.")
                        else:
                            src.rename(dst)
                            st.success(f"Renamed to **{u_new}**.")
                            time.sleep(0.4)
                            st.rerun()
                    except Exception as e:
                        st.error(f"Error: {e}")

        elif u_op == "Append":
            u_append = st.text_area("Content to append", height=120, key="u_append")
            if st.button("Append to file", key="btn_append"):
                try:
                    path = workspace_path(u_name)
                    with open(path, "a") as f:
                        f.write("\n" + u_append)
                    st.success(f"Content appended to **{u_name}**.")
                except Exception as e:
                    st.error(f"Error: {e}")

        elif u_op == "Overwrite":
            path_preview = workspace_path(u_name)
            existing = path_preview.read_text() if path_preview.exists() else ""
            u_over = st.text_area("New contents (replaces everything)", value=existing, height=160, key="u_over")
            if st.button("Overwrite file", key="btn_overwrite"):
                try:
                    path = workspace_path(u_name)
                    path.write_text(u_over)
                    st.success(f"**{u_name}** overwritten.")
                except Exception as e:
                    st.error(f"Error: {e}")
    else:
        st.info("No files in the workspace yet. Create one first.")


# ════════════════════════════════════════════════════════════════════════════
# DELETE
# ════════════════════════════════════════════════════════════════════════════
with tab_delete:
    st.markdown("""
    <div class="op-card">
        <div class="op-card-title">✕ Delete a file</div>
        <div class="op-card-desc">Permanently removes the file. This action cannot be undone.</div>
    </div>""", unsafe_allow_html=True)

    files = list_files()
    file_names = [f.name for f in files]

    if file_names:
        d_name = st.selectbox("Choose a file to delete", options=file_names, key="d_name")

        # Preview
        if d_name:
            try:
                path = workspace_path(d_name)
                preview = path.read_text()[:300]
                size = file_size_label(path)
                st.markdown(f"<div class='file-meta' style='margin-top:1rem'>{d_name} · {size}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='file-content-box' style='border-color:#F87171;color:#FCA5A5;max-height:140px'>{preview + ('…' if len(path.read_text()) > 300 else '') if preview else '<em>Empty file.</em>'}</div>", unsafe_allow_html=True)
            except Exception:
                pass

        confirm = st.checkbox(f'Yes, permanently delete **{d_name}**', key="d_confirm")
        if st.button("Delete file", key="btn_delete", disabled=not confirm):
            try:
                path = workspace_path(d_name)
                path.unlink()
                st.success(f"**{d_name}** deleted.")
                time.sleep(0.4)
                st.rerun()
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.info("No files in the workspace yet. Create one first.")