# Project Environment Setup

## Steps:

1. **Create a Virtual Environment**:

   ```bash
   python3 -m venv venv
   ```

2. **Activate the Virtual Environment**:

   ```bash
   source venv/bin/activate
   ```

3. **Backend Setup**:

   - Install Poetry:

     ```bash
     pip install poetry==1.4.2
     ```

   - Install Dependencies:

     ```bash
     poetry install
     ```

   - Set up Environment Variables (`.env.example` is present as a template for the needed variables`):
_Ensure you have your environment variables set up in a file named `.env.localdev`.\_

   - Run the Backend:
     ```bash
     poetry run uvicorn main:app --reload --host 0.0.0.0 --log-level=debug
     ```

4. **Frontend Setup**:

   - Install Dependencies:

     ```bash
     yarn install
     ```

   - Start the Development Server:
     ```bash
     yarn run dev
     ```

Follow the above steps to successfully set up your project environment.
