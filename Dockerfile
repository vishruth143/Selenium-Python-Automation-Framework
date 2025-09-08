# Use official Python 3.13.7 image for compatibility
FROM python:3.13.7-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies and browsers
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget curl unzip gnupg lsb-release ca-certificates \
    fonts-liberation libappindicator3-1 \
    libasound2 libatk-bridge2.0-0 libcups2 libdbus-1-3 \
    libgdk-pixbuf-xlib-2.0-0 libnspr4 libnss3 libx11-xcb1 libxcomposite1 \
    libxdamage1 libxrandr2 xdg-utils libxss1 libgtk-3-0 libu2f-udev \
    libdrm2 libgbm1 libxshmfence1 libxext6 libxfixes3 libxrender1 \
    libxtst6 libxv1 libxmu6 libxpm4 libxaw7 libxft2 libxinerama1 libxkbcommon0 \
    ffmpeg \
    chromium-driver firefox-esr \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Google Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /usr/share/keyrings/google-chrome.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-chrome.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list && \
    apt-get update && apt-get install -y --no-install-recommends google-chrome-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Microsoft Edge
RUN wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | gpg --dearmor > /usr/share/keyrings/microsoft-edge.gpg && \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/microsoft-edge.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && apt-get install -y --no-install-recommends microsoft-edge-stable && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file first (improves build caching)
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app

# Copy feature files to /features in the container
COPY tests/ui/pta/features /features
