FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV SUPABASE_URL=https://placeholder.supabase.co
ENV SUPABASE_SERVICE_KEY=placeholder
ENV WALLET_BASE=0xCf1d31020A7915421f6d66B9835Dcb6f422337E7
ENV WALLET_SOLANA=giu4VciTkfWJNG1oeP6SzHEJwmabikJSMB91GaFNWE4
ENV CDP_API_KEY_ID=placeholder
ENV CDP_API_KEY_SECRET=placeholder
ENV ANTHROPIC_API_KEY=placeholder

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
