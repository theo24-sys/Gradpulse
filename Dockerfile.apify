FROM apify/actor-python-playwright:3.12

# Copy requirements and install
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . ./

# Set the entry point
CMD ["python3", "apify_main.py"]
