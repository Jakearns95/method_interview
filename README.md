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

   - Set up Environment Variables (`.env.example` is present as a template for the needed variables):
     \_Ensure you have your environment variables set up in a file named `.env.localdev`.\_

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

## Potential Improvements:

## Frontend:

- **Static Typing and Interfaces for API Calls**:

  - Introduce static typing and interfaces to make sure data interacting with the API is consistent. This enhances the frontend's robustness.

- **Service Class for API Calls & Base API Layer**:

  - Centralize all API operations within a dedicated service class, streamlining the code and simplifying maintenance.

- **Structured Layouts and Folder Organization**:
  - Strategically structure frontend assets in intuitive folders. This fosters better maintainability and aids newcomers in navigating the codebase.

## Backend:

- **Static Typing**:

  - Adopt static typing to preemptively detect bugs, elevating code quality.

- **Pydantic Objects & JSON API Spec in Builders**:

  - Standardize response formats to ensure harmony between the frontend and backend, and to align with API best practices.

- **Background Job Management**:

  - Introduce background jobs for retry mechanisms and rate limiting. This ensures efficient handling of traffic surges without system overload.

- **Webhook Services for API Updates**:

  - Implement webhooks to seamlessly synchronize real-time data and capture events instigated by external services.

- **Optimal Package Usage**:

  - Consider transitioning from 'requests' to the 'Method' python package or another modern alternative for better performance and reliability.

- **Testing**:

  - Introduce diverse testing layers (unit, integration, end-to-end) to verify backend operations, ensuring functionality and facilitating safer code refactoring.

- **Function Naming Convention**:

  - Opt for clear and consistent function names to enhance code readability and maintainability.

- **Rigorous Data Validation**:
  - Strengthen data validation processes, especially for payments, to ensure the accuracy of Plaid IDs when cross-referencing with merchants.
