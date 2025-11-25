import asyncio
import aiohttp
from bs4 import BeautifulSoup
import streamlit as st


# --------------------- LISTA DE SITES ---------------------
NEWS_SITES = {
    "G1": "https://g1.globo.com/",
    "UOL Notícias": "https://uol.com.br/",
    "BBC Brasil": "https://www.bbc.com/portuguese",
    "CNN Brasil": "https://www.cnnbrasil.com.br/",
    "Folha de S.Paulo": "https://www.folha.uol.com.br/",
    "Pipeline": "https://pipelinevalor.globo.com/"
}


# --------------------- SCRAPER ---------------------

async def fetch_html(session, url):
    try:
        async with session.get(url, timeout=10) as response:
            return await response.text()
    except Exception:
        return None


async def scrape_headlines(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch_html(session, url)
        if not html:
            return ["Não foi possível obter conteúdo do site."]

        soup = BeautifulSoup(html, "html.parser")

        selectors = ["h1", "h2", "h3", "h4", ".headline", ".title"]

        headlines = []

        for sel in selectors:
            for tag in soup.select(sel):
                text = tag.get_text(strip=True)
                if len(text) > 35:
                    headlines.append(text)

        unique = list(dict.fromkeys(headlines))
        return unique[:10] if unique else ["Nenhuma manchete encontrada."]


def run_scraper(url):
    return asyncio.run(scrape_headlines(url))


# --------------------- INTERFACE STREAMLIT ---------------------

st.set_page_config(
    page_title="Scraper de Notícias",
    page_icon="🗣️",
    layout="centered"
)

st.title("🗣️ Scraper de Notícias")
st.write("Selecione um portal e visualize as **principais manchetes**.")

site = st.selectbox("Portal de notícias:", list(NEWS_SITES.keys()))

if st.button("Coletar Manchetes"):
    url = NEWS_SITES[site]
    with st.spinner("Coletando dados..."):
        headlines = run_scraper(url)

    st.subheader(f"Resultados — {site}")
    
    st.markdown(f"[Acessar o portal {site}]({url})")
     for h in headlines:
        st.write(f"- **{h}**")
