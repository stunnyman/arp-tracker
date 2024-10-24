from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import asyncpg
import plotly.graph_objs as go
from visualizer.utils import get_database_url

app = FastAPI()

async def get_db_connection():
    database_url = get_database_url()

    if not database_url:
        raise RuntimeError("an error with link to database")

    conn = await asyncpg.connect(dsn=database_url)
    return conn


@app.get("/", response_class=HTMLResponse)
async def read_root():
    conn = await get_db_connection()

    try:
        rows = await conn.fetch("SELECT timestamp, arp_value FROM arp_values ORDER BY timestamp")
        if not rows:
            return HTMLResponse(content="No data found")

        timestamps = [row["timestamp"] for row in rows]
        values = [float(row["arp_value"]) for row in rows]

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=timestamps, y=values, mode='lines+markers', name='ARP Value'))
        fig.update_layout(title='ARP for USDT at Binance',
                          xaxis_title='Time',
                          yaxis_title='%')

        graph_html = fig.to_html(full_html=False)
        html_content = f"""
        <html>
            <head>
                <title>Chart</title>
            </head>
            <body>
                <h1>Binance x USDT</h1>
                {graph_html}
            </body>
        </html>
        """
        return HTMLResponse(content=html_content)

    finally:
        await conn.close()

@app.get("/health")
async def healthcheck():
    return {"status": "healthy"}